import streamlit as st
import pickle
import pandas as pd
import requests
from dotenv import load_dotenv
import os

import time
load_dotenv()
tmdb_api_key = os.getenv("tmdb_api_key")
print("TMDB API Key Loaded:", tmdb_api_key is not None)

def fetch_poster(movie_id):
    url=f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_api_key}&language=en-US"
    try:
        data=requests.get(url, timeout=5).json()
        poster_path=data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/"+poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(option):
    m=movies[movies['title']==option].index[0]
    d=similarity[m]
    movies_list=sorted(list(enumerate(d)),reverse=True,key=lambda x:x[1])[1:6]
    recommended=[]
    recommended_posters=[]
    for i in movies_list:
        id=movies.iloc[i[0]]["id"]
        recommended.append(movies.iloc[i[0]]["title"])
        recommended_posters.append(fetch_poster(id))
    return recommended,recommended_posters

movies_dict=pickle.load(open("movies_dict.pkl","rb"))
movies=pd.DataFrame(movies_dict)
similarity=pickle.load(open("similarity.pkl","rb"))
st.title('Movie Recommender')
option=st.selectbox(
    'Select a movie',
    (movies['title'].values)
)
if st.button('Recommend'):
    names,posters=recommend(option)
    col1,col2,col3,col4,col5=st.columns(5)
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