import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
import os
import requests

# Suppress TensorFlow oneDNN logs
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Function to read CSV with memory optimization
def load_csv_with_optimization(filepath, usecols, dtype_spec=None, chunksize=None):
    try:
        if chunksize:
            chunks = pd.read_csv(filepath, usecols=usecols, dtype=dtype_spec, chunksize=chunksize)
            df = pd.concat(chunks, ignore_index=True)
        else:
            df = pd.read_csv(filepath, usecols=usecols, dtype=dtype_spec)
        return df
    except MemoryError:
        st.error(f"MemoryError: Unable to load {filepath}. Reduce chunk size or increase memory.")
        return None

# Fetch poster from Jikan API
def fetch_anime_poster(anime_id):
    base_url = "https://api.jikan.moe/v4/anime/"
    try:
        response = requests.get(f"{base_url}{anime_id}")
        response.raise_for_status()
        data = response.json()
        if "data" in data:
            return data["data"]["images"]["jpg"]["image_url"]
        return None
    except Exception as e:
        st.error(f"Error fetching poster: {e}")
        return None

# Function to extract model weights
def extract_weights(name, model):
    weights = model.get_layer(name).get_weights()[0]
    return weights / np.linalg.norm(weights, axis=1).reshape((-1, 1))

# Function to filter out inappropriate recommendations
def filter_inappropriate_recommendations(recommendations):
    inappropriate_keywords = ['hentai', 'ecchi', '18+', 'adult', 'yuri', 'yaoi', 'uncensored']
    filtered_recommendations = recommendations[~recommendations['Genres'].str.lower().str.contains('|'.join(inappropriate_keywords))]
    return filtered_recommendations

# Recommendation functions
def recommend_based_on_user(anime_name, n=10):
    target_anime = anime_df[anime_df.eng_version.str.lower() == anime_name.lower()]
    if target_anime.empty:
        return pd.DataFrame()

    watched_anime_id = target_anime.iloc[0].anime_id
    encoded_id = anime2anime_encoded.get(watched_anime_id)
    
    combined_weights = anime_weights[encoded_id]
    dists = np.dot(anime_weights, combined_weights)
    similar_ids = np.argsort(dists)[-n-1:][::-1]
    
    recommendations = anime_df[anime_df.anime_id.isin([anime_encoded2anime[x] for x in similar_ids])]
    recommendations = recommendations[recommendations["eng_version"] != anime_name]
    
    return recommendations.head(n)

# Streamlit Frontend UI
st.title("AniFlix - Anime Recommendation System")
st.markdown("### Discover Your Next Favorite Anime!")

# Load datasets
st.info("Loading datasets. Please wait...")
anime_df = load_csv_with_optimization(
    './anime.csv',
    usecols=["MAL_ID", "English name", "Genres", "Studios"],
    dtype_spec={"MAL_ID": "int32", "English name": "str", "Genres": "str", "Studios": "str"}
)

if anime_df is not None:
    anime_df.rename(columns={'MAL_ID': 'anime_id', 'English name': 'eng_version'}, inplace=True)
    anime_df.fillna("", inplace=True)

# Load synopsis data
sypnopsis_df = load_csv_with_optimization(
    './anime_with_synopsis.csv',
    usecols=["MAL_ID", "Name", "sypnopsis"],
    dtype_spec={"MAL_ID": "int32", "Name": "str", "sypnopsis": "str"}
)

if sypnopsis_df is not None:
    sypnopsis_df.rename(columns={'MAL_ID': 'anime_id'}, inplace=True)

# Load model
try:
    model = tf.keras.models.load_model("anime_model.h5")
    anime_ids = anime_df["anime_id"].unique().tolist()
    anime2anime_encoded = {x: i for i, x in enumerate(anime_ids)}
    anime_encoded2anime = {i: x for i, x in enumerate(anime_ids)}
    anime_weights = extract_weights('anime_embedding', model)
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# Sidebar for inputs
st.sidebar.header("Recommendation Options")
anime_name = st.sidebar.text_input("Enter the name of an anime:")
num_recommendations = st.sidebar.slider("Number of Recommendations", 5, 20, 10)

if st.sidebar.button("Get Recommendations"):
    if anime_name.strip():
        recommendations = recommend_based_on_user(anime_name, n=num_recommendations)
        if not recommendations.empty:
            # Filter inappropriate recommendations
            recommendations = filter_inappropriate_recommendations(recommendations)
            
            if not recommendations.empty:
                st.markdown(f"### Recommendations Based on **{anime_name}**:")
                for _, row in recommendations.iterrows():
                    poster_url = fetch_anime_poster(row['anime_id'])

                    # Horizontal Layout using st.columns()
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        if poster_url:
                            st.image(poster_url, caption=row['eng_version'], use_container_width=True)
                        else:
                            st.write("No Poster Available")

                    with col2:
                        st.markdown(f"**{row['eng_version']}**")
                        st.markdown(f"**Genres**: {row['Genres']}")
                        st.markdown(f"**Studios**: {row['Studios']}")
                        synopsis = sypnopsis_df[sypnopsis_df['anime_id'] == row['anime_id']]['sypnopsis'].values
                        if len(synopsis) > 0:
                            st.markdown(f"**Synopsis**: {synopsis[0]}")
                    st.write("---")
            else:
                st.error("No appropriate recommendations found. Try adjusting your input.")
        else:
            st.error("No recommendations found. Please check the anime name or try another.")
    else:
        st.error("Please enter an anime name.")
