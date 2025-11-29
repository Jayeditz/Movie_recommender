import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
import os

# --------------------------
# Download similarity.pkl from Google Drive if not present
# --------------------------
similarity_file = "similarity.pkl"
file_id = "1wHH2Z1X6Iy-Lr7UtGIBTmFAKU8mnx0ty"  # Replace with your file ID if changed
similarity_url = f"https://drive.google.com/uc?id={file_id}"

if not os.path.exists(similarity_file):
    st.info("Downloading similarity.pkl from Google Drive...")
    gdown.download(similarity_url, similarity_file, quiet=False)

# --------------------------
# Load data files
# --------------------------
movies_file = "movie.pkl"
if not os.path.exists(movies_file):
    st.error("movie.pkl not found! Please upload it or provide a download method.")
    st.stop()

with open(movies_file, "rb") as f:
    movies = pickle.load(f)

with open(similarity_file, "rb") as f:
    similarity = pickle.load(f)

# --------------------------
# Function: Fetch poster
# --------------------------
def fetch_poster(movie_id):
    api_key = "625d8f254c13b59f8b55eac698470810"  # Your TMDB API key
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500" + poster_path
    return "https://via.placeholder.com/300x450?text=No+Image"

# --------------------------
# Function: Recommend movies
# --------------------------
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]

    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_names = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].id
        recommended_names.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_names, recommended_posters

# --------------------------
# Streamlit UI
# --------------------------
st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox(
    "Select a movie:",
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])



