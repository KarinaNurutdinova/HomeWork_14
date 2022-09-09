from flask import Flask, jsonify
from utils import search_movie_by_name, search_by_years, search_by_rating, search_by_genre
app = Flask(__name__)


@app.route("/movie/<title>", methods=['GET'])
def search_by_title(title):
    return search_movie_by_name(title)


@app.route("/movie/<first_year>/to/<second_year>")
def search_by_year(first_year, second_year):
    return jsonify(search_by_years(first_year, second_year))


@app.route("/rating/<rating>")
def search_by_ratings(rating):
    return jsonify(search_by_rating(rating))


@app.route("/genre/<genre>")
def search_by_genres(genre):
    return search_by_genre(genre)


if __name__ == '__main__':
    app.run()
