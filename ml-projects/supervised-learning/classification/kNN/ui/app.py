import streamlit as st
import pickle

def recommend(movie):
    idx = movies[movies['title'] == movie].index[0]
    distances, indices = model.kneighbors(vectors[idx], n_neighbors=6)

    recommended = []
    for i in indices[0][1:]:
        recommended.append(movies.iloc[i].title)

    return recommended

# Load data
model = pickle.load(open('../notebooks/model.pkl', 'rb'))
movies = pickle.load(open('../notebooks/movies.pkl', 'rb'))
vectors = pickle.load(open('../notebooks/vectors.pkl', 'rb'))

st.title("🎬 Movie Recommender System")

movie_list = movies['title'].values
selected_movie = st.selectbox("Select a movie", movie_list)

if st.button("Recommend"):
    results = recommend(selected_movie)
    
    st.subheader("Recommended Movies:")
    for movie in results:
        st.write(movie)
