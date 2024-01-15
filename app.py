from flask import Flask, request, render_template
from preprocessor import Preprocessor
from encoder import MovieEncoder
from recommender import find_closest_user, recommend_movies

class MovieRecommenderApp:
    def __init__(self):
        self.pre_processor = Preprocessor('data/ratings.csv', 'data/movies.csv', 'data/users.csv')
        self.encoder = MovieEncoder()
        self.movies_df = None
        self.ratings_df = None
        self.users_df = None

    def load_data(self):
        self.pre_processor.run_preprocessing()
        _, self.movies_df, self.ratings_df, self.users_df = self.encoder.encode_data()

    def get_recommendations(self, user_profile):
        closest_user_id = find_closest_user(user_profile, self.users_df, self.ratings_df, self.movies_df, user_profile['favorite_movie_id'])
        return recommend_movies(closest_user_id, self.ratings_df, self.movies_df, user_profile['favorite_genres'])

movie_recommender_app = MovieRecommenderApp()
movie_recommender_app.load_data()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_profile = {
            'age': request.form['age'],
            'gender': request.form['gender'],
            'favorite_genres': request.form.getlist('favorite_genres'),
            'occupation': int(request.form['occupation']),
            'favorite_movie_id': int(request.form['favorite_movie'])
        }
        
        recommended_movies = movie_recommender_app.get_recommendations(user_profile)
        print("Recommended Movies:", recommended_movies)
        return render_template('index.html', movies=recommended_movies)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
