import pandas as pd
from preprocessor import Preprocessor
from sklearn.metrics.pairwise import cosine_similarity

def get_recommendations(movie_id, cosine_sim, movies_df):
    
    sim_scores = list(enumerate(cosine_sim[movie_id]))

    
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    
    sim_scores = sim_scores[1:11]

    
    movie_indices = [i[0] for i in sim_scores]

    
    movie_titles = movies_df[movies_df['movieId'].isin(movie_indices)]['title'].tolist()

    return movie_titles



def calculate_similarity(user_profile, other_user_profile, ratings_df, movies_df, favorite_movie_id):
    similarity = 0

    
    if user_profile['age'] == other_user_profile['age']:
        similarity += 1

    condition = (ratings_df['userId'] == other_user_profile['userId']) & \
                (ratings_df['movieId'] == favorite_movie_id) & \
                (ratings_df['rating'] == 5)
                
    if condition.any():
        similarity += 1
    
    if user_profile['gender'] == other_user_profile['gender']:
        similarity += 1

    
    high_ratings = ratings_df[(ratings_df['userId'] == other_user_profile['userId']) & 
                              (ratings_df['rating'] >= 4)]
    high_ratings_with_genre = high_ratings.merge(movies_df, on='movieId')

    if any(genre in user_profile['favorite_genres'] for genre in high_ratings_with_genre['genres'].str.split('|').explode()):
        similarity += 1
        
    if user_profile['occupation'] == other_user_profile['occupation']:
        similarity += 1

    return similarity

def find_closest_user(user_profile, users_df, ratings_df, movies_df, favorite_movie_id):
    max_similarity = -1
    closest_user_id = None
    for index, row in users_df.iterrows():
        other_user_profile = {
            'userId': row['userId'],  
            'age': row['age'],
            'gender': row['gender'],
            'occupation': row['occupation']
        }
        similarity = calculate_similarity(user_profile, other_user_profile, ratings_df, movies_df, favorite_movie_id)
        if similarity > max_similarity:
            max_similarity = similarity
            closest_user_id = row['userId']
    return closest_user_id


def recommend_movies(closest_user_id, ratings_df, movies_df, user_favorite_genres):
    
    high_rated_movies = ratings_df[(ratings_df['userId'] == closest_user_id) & (ratings_df['rating'] >= 4)]
    
    
    recommended_movies = movies_df[movies_df['movieId'].isin(high_rated_movies['movieId'])]
    recommended_movies = recommended_movies[recommended_movies['genres'].apply(lambda genres: any(genre in user_favorite_genres for genre in genres))]

    return recommended_movies['title'].tolist()
