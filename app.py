import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
import os

# --------------------------
# GOOGLE DRIVE FILE LINKS
# --------------------------
# Replace these IDs with your actual Google Drive file IDs
SIMILARITY_FILE_ID = "YOUR_SIMILARITY_FILE_ID"
MOVIE_FILE_ID = "YOUR_MOVIE_FILE_ID"

# --------------------------
# DOWNLOAD FILES IF NOT PRESENT
# --------------------------
if not os.path.exists("similarity.pkl"):
    similarity_url = f"https://drive.google.com/uc?id={SIMILARITY_FILE_ID}"
    gdown.download(similarity_url, "similarity.pkl", quiet=False)

if not os.path.exists("movie.pkl"):
    movie_url = f"https://drive.google.com/uc?id={MOVIE_FILE_ID}"
    gdown.download(movie_url, "movie.pkl", quiet=False)

# --------------------------
# FUNCTION: Fetch poster
# --------------------------
def fetch_poster(movie_id):
    # Hardcoded API key
    api_key = "625d8f254c13b59f8b55eac698470810"

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url)

    if response.status_code != 200:
        return "https://via.placeholder.com/300x450?text=No+Image"

    data = response.json()
    poster_path = data.get("poster_path")
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    else:
        return "https://via.placeholder.com/300x450?text=No+Image"


# --------------------------
# FUNCTION: Recommend movies
# --------------------------
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]

    movie_list = sorted(list(enumerate(distances)),
                        reverse=True, key=lambda x: x[1])[1:6]

    recommended_names = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].id
        recommended_names.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_names, recommended_posters

# --------------------------
# LOAD PICKLE FILES
# --------------------------
with open("movie.pkl", "rb") as f:
    movies = pickle.load(f)

with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

# --------------------------
# STREAMLIT UI
# --------------------------
st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox(
    "Select a movie:",
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.text(name)
            st.image(poster)



