from preprocessor import Preprocessor
from encoder import MovieEncoder
from recommender import find_closest_user, recommend_movies
from sklearn.metrics.pairwise import cosine_similarity


def main():
    
    pre_processor = Preprocessor('data/ratings.csv', 'data/movies.csv', 'data/users.csv')
    pre_processor.run_preprocessing()
    
    encoder = MovieEncoder()
    
    
    _, movies_df, ratings_df, users_df = encoder.encode_data()
    
    
    user_profile = {
        'age': '45',
        'gender': 'M',
        'favorite_genres': ['Western'],
        'occupation': 4, 
        'favorite_movie_id': 1201
    }

    
    closest_user_id = find_closest_user(user_profile, users_df, ratings_df, movies_df, user_profile['favorite_movie_id'])
    user_favorite_genres = user_profile['favorite_genres']
    recommended_movies = recommend_movies(closest_user_id, ratings_df, movies_df, user_favorite_genres)

    print("Recommended Movies:", recommended_movies)
    
if __name__ == '__main__':
    main()