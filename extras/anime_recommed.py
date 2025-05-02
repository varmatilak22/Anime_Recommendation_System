import streamlit as st
import pandas as pd
import numpy as np
import requests
from PIL import Image
from io import BytesIO
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from scipy.spatial.distance import jaccard

# Load the preprocessed anime dataset
df_encoded = pd.read_csv('preprocessed_anime_data.csv')

# Function to recommend anime based on different distance measures
def recommend_anime_v2(target_anime, df, measure='cosine', top_n=5):
    if target_anime not in df['name'].values:
        raise ValueError(f"Anime '{target_anime}' not found in the dataset. Please try a different name.")
    
    target_index = df[df['name'] == target_anime].index[0]
    target_features = df.iloc[target_index].drop(['anime_id', 'name', 'episodes']).values.reshape(1, -1)
    
    if measure == 'cosine':
        similarity_scores = cosine_similarity(target_features, df.drop(['anime_id', 'name', 'episodes'], axis=1).values)
    elif measure == 'euclidean':
        similarity_scores = -euclidean_distances(target_features, df.drop(['anime_id', 'name', 'episodes'], axis=1).values)
    elif measure == 'jaccard':
        similarity_scores = np.array([1 - jaccard(target_features.flatten(), row) for row in df.drop(['anime_id', 'name', 'episodes'], axis=1).values])
    else:
        raise ValueError(f"Unknown distance measure: {measure}")
    
    similar_indices = similarity_scores.argsort()[0][-top_n-1:-1][::-1]
    return df.iloc[similar_indices][['name', 'rating', 'members']]

# Function to fetch anime details and resize poster to 64x64
def fetch_anime_info(anime_name):
    url = f"https://api.jikan.moe/v4/anime?q={anime_name}&sfw"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get('data', [])
        if data:
            anime_data = data[0]
            # Resize the poster image to 64x64
            poster_url = anime_data['images']['jpg']['image_url']
            try:
                poster_response = requests.get(poster_url)
                if poster_response.status_code == 200:
                    image = Image.open(BytesIO(poster_response.content))
                    image = image.resize((128, 128))  # Resize to 64x64
                    anime_data['resized_image'] = image
            except Exception as e:
                anime_data['resized_image'] = None
            return anime_data
    return None

# Streamlit app interface
def anime_recommendation_app():
    # Set page configuration
    st.set_page_config(
        page_title="Anime Recommendation System",
        page_icon="🎥",
        layout="wide",
    )
    
    # Title and subtitle
    st.markdown("<h1 style='text-align: center; color: #4e73df;'>Anime Recommendation System</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #6c757d;'>Discover your next favorite anime!</h3>", unsafe_allow_html=True)

    # Input form
    with st.form("anime_form"):
        st.write("### Enter Details")
        col1, col2 = st.columns(2)
        with col1:
            anime_name = st.text_input("Enter an anime name:", placeholder="e.g., Attack on Titan")
        with col2:
            num_recommendations = st.number_input("Number of recommendations:", min_value=1, max_value=10, value=5)
        
        distance_measure = st.radio("Choose a similarity measure:", ['cosine', 'euclidean', 'jaccard'], horizontal=True)
        submit = st.form_submit_button("Get Recommendations")
    
    # Recommendation logic
    if submit and anime_name:
        try:
            recommendations = recommend_anime_v2(anime_name, df_encoded, measure=distance_measure, top_n=num_recommendations)
            
            st.write(f"### Recommendations for '{anime_name}':")
            for _, row in recommendations.iterrows():
                anime_info = fetch_anime_info(row['name'])
                if anime_info:
                    # Display resized poster alongside content
                    st.write("---")
                    col1, col2 = st.columns([1, 2])  # Smaller column for the poster
                    with col1:
                        if anime_info.get('resized_image'):
                            st.image(anime_info['resized_image'], caption="Anime Poster", use_container_width=True)
                        else:
                            st.warning("No poster available.")
                    with col2:
                        st.markdown(f"**Title:** {anime_info['title']}")
                        st.markdown(f"**Rating:** {anime_info.get('score', 'N/A')}")
                        st.markdown(f"**Synopsis:** {anime_info.get('synopsis', 'No description available')}")
                        st.markdown(f"**Members:** {row['members']}")
                else:
                    st.warning(f"Details for {row['name']} not found.")
        except ValueError as e:
            st.error(e)

# Run the app
anime_recommendation_app()
