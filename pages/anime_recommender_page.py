import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
import requests
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from scipy.spatial.distance import jaccard
import os
import webbrowser
import requests
from PIL import Image
from io import BytesIO
import shutil

# Set page configuration

# Load the preprocessed anime dataset

# Get the current working directory (where the script is run from)
base_dir = os.getcwd()

# Build the path to your file from the working directory
file_path = os.path.join(base_dir, 'preprocess_data', 'preprocessed_anime_data.csv')

df_encoded = pd.read_csv(file_path,low_memory=False)

#Function to clear cache files
def delete_pycache():
    pycache_path = os.path.join(os.path.dirname(__file__), '__pycache__')
    if os.path.exists(pycache_path) and os.path.isdir(pycache_path):
        shutil.rmtree(pycache_path)
        print("__pycache__ deleted successfully.")
    else:
        print("__pycache__ does not exist.")

# Function to recommend anime based on similarity
def recommend_anime_v2(target_anime, df, measure='cosine', top_n=5):
    if target_anime not in df['name'].values:
        raise ValueError(f"Anime '{target_anime}' not found. Please try a different name.")

    target_index = df[df['name'] == target_anime].index[0]
    target_features = df.iloc[target_index].drop(['anime_id', 'name', 'episodes']).values.reshape(1, -1)

    if measure == 'cosine':
        similarity_scores = cosine_similarity(target_features, df.drop(['anime_id', 'name', 'episodes'], axis=1).values)
    elif measure == 'euclidean':
        similarity_scores = -euclidean_distances(target_features, df.drop(['anime_id', 'name', 'episodes'], axis=1).values)
    elif measure == 'jaccard':
        similarity_scores = np.array([1 - jaccard(target_features.flatten(), row) 
                                      for row in df.drop(['anime_id', 'name', 'episodes'], axis=1).values])
    else:
        raise ValueError("Unknown distance measure.")
    
    similar_indices = similarity_scores.argsort()[0][-top_n-1:-1][::-1]
    return df.iloc[similar_indices][['name', 'rating', 'members']]

# Function to fetch anime info via Jikan API
def fetch_anime_info(anime_name):
    url = f"https://api.jikan.moe/v4/anime?q={anime_name}&sfw"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get('data', [])
        if data:
            return data[0]
    return None

# Function to load the trained model
@st.cache_resource
def load_model_and_weights():
    try:
        model = tf.keras.models.load_model("anime_model.h5")
        anime_ids = df_encoded["anime_id"].unique().tolist()
        anime2anime_encoded = {x: i for i, x in enumerate(anime_ids)}
        anime_encoded2anime = {i: x for i, x in enumerate(anime_ids)}
        weights = model.get_layer('anime_embedding').get_weights()[0]
        return model, anime2anime_encoded, anime_encoded2anime, weights / np.linalg.norm(weights, axis=1).reshape((-1, 1))
    except Exception as e:
        st.error("Model loading failed. Ensure 'anime_model.h5' exists and is accessible.")
        return None, None, None, None

# Main app function
def anime_recommendation_app():
    # Apply custom CSS for black background with white text
    st.markdown("""
    <style>
        /* General Dark Theme */
        body {
            background-color: #121212;
            color: #ffffff;
        }
        /* Offcanvas Sidebar */
        [data-testid="stSidebar"] {
            background-color: #181818;
        }
        .title-text {
            color: #E50914;
            font-size: 36px;
            font-weight: bold;
            text-align: center;
        }
        .stButton>button {
            background-color: #E50914;
            color: white;
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)

    # Title
    with st.sidebar:
        st.markdown("<div class='title-text'>ANIFLIX 🎥</div>", unsafe_allow_html=True)
        st.write(" Choose your mode of recommendation to get started!")
        prof = st.session_state.get("profile")
        if not prof:
            st.error("No profile found. Please log in first.")
            return
        
        image_url = prof.get("picture", None)

        with st.spinner("Loading Image"):
            if image_url:
                try:
                    response = requests.get(image_url, timeout=5)
                    if response.status_code == 200:
                        image = Image.open(BytesIO(response.content))
                        st.image(image, width=120)
                    else:
                        st.warning("Unable to load profile image (invalid status code).")
                        st.image("default_profile.png", width=120)  # Use a fallback image
                except Exception as e:
                    st.warning(f"Image load failed: {e}")
                    st.image("default_profile.png", width=120)
            else:
                st.warning("Profile picture not available.")
                st.image("default_profile.png", width=120)
        st.write(f"**Name:**   {prof.get('name','–')}")
        st.write(f"**Email:**  {prof.get('email','–')}")
        #st.write(f"**Locale:** {prof.get('locale','–')}")
    
        if st.button("Logout"):
            # clear session and send back to login
           #st.session_state.pop("token",   None)
           #st.session_state.pop("profile", None)
           for k in list(st.session_state.keys()):
               del st.session_state[k]
           st.cache_resource.clear()
           delete_pycache()
           st.switch_page("main.py")
          
        # User Options
        mode = st.radio("Choose Mode:", ["🎯 Neural Collaborative Filtering", "🧩 Content-Based Filtering"])
        
    if st.button("🎥 ANIFLIX (Go to Home)", use_container_width=True):
        st.switch_page("main.py")   
    if mode == "🎯 Neural Collaborative Filtering":
        st.write("### 🎯 Item-Based Recommendation System")
        with st.form("rec_form"):
            anime_name = st.text_input("Anime Name:")
            num_recommendations = st.slider("Number of Recommendations:", 5, 20, 10)
            submitted= st.form_submit_button("Recommend")
        if submitted:
            
            if anime_name.strip():
                with st.spinner("Fetching recommendations... Please wait ⏳"):
                    model, anime2anime_encoded, anime_encoded2anime, anime_weights = load_model_and_weights()
                    if model:
                        try:
                            target_id = df_encoded.loc[df_encoded['name'] == anime_name, 'anime_id'].values[0]
                            if target_id in anime2anime_encoded:
                                target_encoded_id = anime2anime_encoded[target_id]
                                similarity_scores = np.dot(anime_weights, anime_weights[target_encoded_id])
                                recommended_indices = np.argsort(similarity_scores)[-num_recommendations-1:-1][::-1]
                        
                                recommended_anime = df_encoded.iloc[recommended_indices]
                                st.write(f"### Recommendations for '{anime_name}':")
                        
                                for _, row in recommended_anime.iterrows():
                                    anime_info = fetch_anime_info(row['name'])
                                    if anime_info:
                                        with st.expander(f"**{anime_info['title']}**"):
                                            col1, col2 = st.columns([1, 2])
                                            with col1:
                                                st.image(anime_info['images']['jpg']['image_url'], width=200)
                                            with col2:
                                                st.write(f"**Name:** {anime_info['title']}")
                                                genres = anime_info.get('genres', [])
                                                genre_names = [genre['name'] for genre in genres]
                                                st.write(f"**Genres:** {', '.join(genre_names)}" if genre_names else "**Genres:**         Not available")
                                                st.write(f"**Synopsis:** {anime_info.get('synopsis', 'No synopsis available.')}") 
                                                #st.write(f"**Members Watched:** {int(row['members']):,}")
                                                #st.write(f"**Average Rating:** {row['rating']}")
                                    else:
                                        st.warning(f"Details for '{row['name']}' not found.")
                            else:
                                st.warning("Anime not found in the model database.")
                        except Exception as e:
                            st.error(f"Error: {e}")
            else:
                st.error("Please enter a valid anime name.")

    elif mode == "🧩 Content-Based Filtering":
        st.write("### 🧩 Content-Based Recommendation Systen")
        with st.form("con_form"):
            anime_name = st.text_input("Anime Name:")
            num_recommendations = st.slider("Number of Recommendations:", 1, 20, 5)
            similarity_measure = st.radio("Similarity Measure:", ["cosine", "euclidean", "jaccard"], horizontal=True)
            submit=st.form_submit_button("Get Recommendations")
        if submit:
            with st.spinner("🔍 Fetching your recommendations..."):
                try:
                    recommendations = recommend_anime_v2(anime_name, df_encoded, measure=similarity_measure, top_n=num_recommendations)
                    st.write(f"### Recommendations for '{anime_name}':")
                    for _, row in recommendations.iterrows():
                        anime_info = fetch_anime_info(row['name'])
                        if anime_info:
                            with st.expander(f"**{anime_info['title']}**"):
                                col1, col2 = st.columns([1, 2])
                                with col1:
                                    st.image(anime_info['images']['jpg']['image_url'], width=200)
                                with col2:
                                    st.write(f"**Name:** {anime_info['title']}")

                                    genres = anime_info.get('genres', [])
                                    genre_names = [genre['name'] for genre in genres]
                                    st.write(f"**Genres:** {', '.join(genre_names)}" if genre_names else "**Genres:** Not available")

                                    st.write(f"**Synopsis:** {anime_info.get('synopsis', 'No synopsis available.')}") 
                                    st.write(f"**Members Watched:** {int(row['members']):,}")
                                    st.write(f"**Average Rating:** {row['rating']}")
                        else:
                            st.warning(f"Details for '{row['name']}' not found.")
                except ValueError as e:
                    st.error(e)


# Run the app
anime_recommendation_app()
