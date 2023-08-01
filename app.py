import streamlit as st
import pickle
import pandas as pd
import requests

ml_model_dict = pickle.load(open('final_movie_data_dict', 'rb'))
ml_model_data = pd.DataFrame(ml_model_dict)

similarity_matrix = pickle.load(open('similarity_matrix_comp.pkl', 'rb'))

def get_poster(tmdb_id):
    ''' This methods returns the poster paths (tmdb urls) for given tmdb movie id'''

    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=0101b215abe64560a3f0a98d3d28b1dc&language=en-US'.format(tmdb_id))
    data = response.json()

    return 'https://image.tmdb.org/t/p/w185/'+ data['poster_path']


def recommend_movies(movie_name):
    ''' This method prints 10 closest movies to the input movie_name '''
    
    # Extracting index of input movie from data
    if movie_name in ml_model_data['title'].tolist():
        
        movie_index = ml_model_data[ml_model_data['title'] == movie_name].index[0]
    
        # Calculating input movie's distances from all other movies in data
        dist_from_other_movies = similarity_matrix[movie_index]

        # Finding top closest movie indices
        recommendation_list = sorted(list(enumerate(dist_from_other_movies)), key=lambda x: x[1], reverse=True)[1:6]

        # Printing names of recommended movies & there posters
        recommends = []
        poster_paths = []
        for i in range(5):
            recommends.append(ml_model_data.iloc[ recommendation_list[i][0] ]['title'])
            
            # Fetching poster paths of recomomended movies
            path = get_poster(ml_model_data.iloc[ recommendation_list[i][0] ]['id'])
            poster_paths.append(path)
        
        return recommends, poster_paths
    
    else:
        return "Movie not found in database!"

st.title("Movie Recommender System")

movie_name = st.selectbox(
    'For which movie would you like to get recommendations?',
    (ml_model_data['title']))

if st.button('Recommend!'):
    recommendations, posters = recommend_movies(movie_name)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col_lilst_1 = [col1, col2, col3, col4, col5]
    
    for i in range(len(col_lilst_1)): 
        with col_lilst_1[i]:
            st.text(recommendations[i])
            st.image(posters[i])