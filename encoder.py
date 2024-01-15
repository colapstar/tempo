import pandas as pd
from preprocessor import Preprocessor


class MovieEncoder:
    def __init__(self):
        self.preprocessor = Preprocessor('data/ratings.csv', 'data/movies.csv', 'data/users.csv')

    def encode_data(self):
        full_dataset = self.preprocessor.run_preprocessing()
        full_dataset = pd.get_dummies(full_dataset, columns=['gender', 'occupation'])
        user_movie_matrix = full_dataset.pivot_table(index='userId', columns='movieId', values='rating')
        user_movie_matrix_filled = user_movie_matrix.fillna(0)
        return user_movie_matrix_filled, self.preprocessor.movies_df, self.preprocessor.ratings_df, self.preprocessor.users_df




