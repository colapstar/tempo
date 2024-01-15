import pandas as pd

class Preprocessor:
    def __init__(self, ratings_file, movies_file, users_file):
        self.ratings_file = ratings_file
        self.movies_file = movies_file
        self.users_file = users_file
        self.ratings_df = None
        self.movies_df = None
        self.users_df = None
        self.full_dataset = None

    def preprocess_ratings(self):
        self.ratings_df = pd.read_csv(self.ratings_file, sep=';')
        self.ratings_df['timestamp'] = pd.to_datetime(self.ratings_df['timestamp'], unit='s', errors='coerce')

    def preprocess_movies(self):
        try:
            self.movies_df = pd.read_csv(self.movies_file, sep=';', on_bad_lines='skip')
        except UnicodeDecodeError:
            self.movies_df = pd.read_csv(self.movies_file, sep=';', encoding='ISO-8859-1', on_bad_lines='skip')
        self.movies_df['genres'] = self.movies_df['genres'].apply(lambda x: x.split('|'))
        self.movies_df['year'] = self.movies_df['title'].str.extract('(\(\d{4}\))', expand=False)
        self.movies_df['year'] = self.movies_df['year'].str.extract('(\d{4})', expand=False)

    def preprocess_users(self):
        self.users_df = pd.read_csv(self.users_file, sep=';')

    def merge_datasets(self):
        ratings_movies_df = pd.merge(self.ratings_df, self.movies_df, on='movieId')
        self.full_dataset = pd.merge(ratings_movies_df, self.users_df, on='userId')


    def run_preprocessing(self):
        self.preprocess_ratings()
        self.preprocess_movies()
        self.preprocess_users()
        self.merge_datasets()
        return self.full_dataset


