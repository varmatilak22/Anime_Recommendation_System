import streamlit as st
import pandas as pd
import numpy as np
import requests
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

# Function to get detailed anime info using the Jikan API
def fetch_anime_info(anime_name):
    url = f"https://api.jikan.moe/v4/anime?q={anime_name}&sfw"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get('data', [])
        if data:
            return data[0]
    return None

# Streamlit app interface
def anime_recommendation_app():
    # Set page configuration
    st.set_page_config(
        page_title="Anime Recommendation System",
        page_icon="🎥",
        layout="wide",
    )
    
    # Custom CSS for styling
    st.markdown(
        """
        <style>
        .main {
            background-color: #f8f9fa;
            font-family: 'Arial', sans-serif;
        }
        .title {
            font-size: 36px;
            color: #4e73df;
            text-align: center;
            font-weight: bold;
        }
        .subtitle {
            font-size: 20px;
            color: #6c757d;
            text-align: center;
            margin-bottom: 30px;
        }
        .anime-title {
            font-size: 24px;
            color: #4e73df;
            font-weight: bold;
        }
        .anime-details {
            font-size: 16px;
            color: #495057;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Title and subtitle
    st.markdown('<div class="title">Anime Recommendation System</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Discover your next favorite anime!</div>', unsafe_allow_html=True)

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
                    # Display in a card-like format
                    with st.expander(f"**{anime_info['title']}**", expanded=False):
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            st.image(anime_info['images']['jpg']['image_url'], width=300)
                        with col2:
                            st.markdown(f"<div class='anime-title'>{anime_info['title']}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='anime-details'><strong>Rating:</strong> {anime_info.get('score', 'N/A')}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='anime-details'><strong>Synopsis:</strong> {anime_info.get('synopsis', 'No description available')}</div>", unsafe_allow_html=True)
                else:
                    st.warning(f"Details for {row['name']} not found.")
        except ValueError as e:
            st.error(e)

# Run the app
anime_recommendation_app()
