# important information while fetching poster data from IMDB api
# --> create imdb account and get api
# --> go on imdb api website -> search movies -> create website url or code from chatgpt -> paste to chrome to cross verify the posters
#        -> we get the json output -> use json viewer to get title easily and also get poster path -> create the fetch folder function


import streamlit as st
import pickle
import requests # used to hit the api request

# The dataframe created in the pickle file
movies_df = pickle.load(open('movies.pkl','rb'))
movie_titles = movies_df['title'].values
st.title('Movie Recommender System') # for the title

# similarity
similarity_mat = pickle.load(open('similarity.pkl','rb'))

# the following function used to fetching the recommended system
def fetch_poster(movie_id):
    movie_id = movies_df.iloc[movie_id].id
    # Make the API request
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=9c2827aa15c2779fff17f9633eb070ba&language=en-US')
    data = response.json()

    # Base URL for images
    base_url = "https://image.tmdb.org/t/p/w500/"

    # Full poster URL
    return base_url + data['poster_path']
#

def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    obtained_movies = sorted(enumerate(similarity_mat[movie_index]), key=lambda x: x[1], reverse=True)[1:6]
    recommend_movies = []
    recommend_movies_posters = []
    for i in obtained_movies:
        movie_id = i[0]
        # fetch poster from API
        recommend_movies_posters.append(fetch_poster(movie_id))
        recommend_movies.append(movies_df.iloc[movie_id].title)
    return recommend_movies, recommend_movies_posters

# select box will provide dropdown list
selected_movie_name = st.selectbox(
    'Select your most favourite movie :- ',
    movie_titles
)

if st.button('Recommend'):
    # Call the recommend function to get recommended movies and their posters
    recommended_movies, recommended_posters = recommend(selected_movie_name)

    # Create 5 columns for the layout
    col1, col2, col3, col4, col5 = st.columns(5)
    # Display the recommended movies and posters in a grid layout
    for idx, (movie, poster) in enumerate(zip(recommended_movies, recommended_posters)):
        with [col1, col2, col3, col4, col5][idx]:
            st.text(movie)
            st.image(poster, width=150)

