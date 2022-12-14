
import sqlite3
from flask import jsonify


def get_data_by_db(query):
    with sqlite3.connect("netflix.db") as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return result


def search_movie_by_name(title):
    query_title = f"""SELECT title, country, release_year, listed_in, description
                   FROM netflix 
                   WHERE title LIKE '{title}%'
                   ORDER BY release_year DESC 
                   LIMIT 1
                   """
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        cursor.execute(query_title)
        movies_data = []
        for row in cursor.fetchone():
            movies_data.append(row)
        search_result = {
            "title": movies_data[0],
            "country": movies_data[1],
            "release_year": movies_data[2],
            "genre": movies_data[3],
            "description": movies_data[4]
        }
    return jsonify(search_result)


def search_by_years(first_year, second_year):
    query_years = f"""
                    SELECT title, release_year  FROM netflix
                    WHERE release_year BETWEEN {first_year} AND {second_year}
                    ORDER BY release_year LIMIT 1000
                    """
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        cursor.execute(query_years)
        movies = cursor.fetchall()
        search_result = []
        for movie in movies:
            movie_data = {
                'title': movie[0],
                'release_year': movie[1],
                }
            search_result.append(movie_data)
    return search_result


def search_by_rating(ratings):
    if ratings == 'children':
        query_rating = f"""
                        SELECT title, rating, description   
                        FROM netflix
                        WHERE rating IN ('G')
                        ORDER BY rating 
                        """
    if ratings == 'family':
        query_rating = f"""
                        SELECT title, rating, description   
                        FROM netflix
                        WHERE rating IN ('G', 'PG', 'PG-13')
                        ORDER BY rating 
                        """
    if ratings == 'adult':
        query_rating = f"""
                        SELECT title, rating, description   
                        FROM netflix
                        WHERE rating IN ('R', 'NC-17')
                        ORDER BY rating 
                        """
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        cursor.execute(query_rating)
        movies = cursor.fetchall()
        search_result = []
        for movie in movies:
            movie_data = {
                'title': movie[0],
                'rating': movie[1],
                'description': movie[2],
                }
            search_result.append(movie_data)
    return search_result


def search_by_genre(genre):
    query_genre = f"""
                    SELECT title, description, listed_in
                    FROM netflix
                    WHERE listed_in LIKE '%{genre}%'
                    ORDER BY release_year DESC 
                    LIMIT 10
                    """
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        cursor.execute(query_genre)
        movies = cursor.fetchall()
        search_result = []
        for movie in movies:
            movie_data = {
                'title': movie[0],
                'description': movie[1],
                }
            search_result.append(movie_data)
    return search_result


def cast_by_cast(first_name, second_name):
    """???????????????? ?? ???????????????? ?????????????????? ?????????? ???????? ??????????????,
       ?????????????????? ???????? ?????????????? ???? ?????????????? cast ?? ???????????????????? ???????????? ??????,
       ?????? ???????????? ?? ???????? ?? ???????? ???????????? 2 ??????."""
    query_stars = f"""
                    SELECT netflix.cast as stars
                    FROM netflix
                    WHERE stars LIKE '%{first_name}%' 
                    AND stars LIKE '%{second_name}%' 
                    """
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        cursor.execute(query_stars)
        movies = cursor.fetchall()
        search_stars = []
        search_result = []
        for stars in movies:
            for star in stars:
                name_list = star.split(", ")
                for name in name_list:
                    if name in search_stars:
                        if name not in search_result and name != first_name and name != second_name:
                            search_result.append(name)
                    else:
                        search_stars.append(name)

        return search_result


def movies_search(movies_type='', movies_year='', movies_genre=''):
    """???????????????????? ???????????? ???????????????? ???????????? ?? ???? ???????????????????? ?? JSON."""
    query_movies = f"""
                    SELECT title, description
                    FROM netflix
                    WHERE netflix.type LIKE '%{movies_type}%'
                    AND release_year LIKE '%{movies_year}%'
                    AND listed_in LIKE '%{movies_genre}%'
                    """
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        cursor.execute(query_movies)
        movies = cursor.fetchall()
        search_result = []
        for movie in movies:
            movie_data = {
                'title': movie[0],
                'description': movie[1],
            }
            search_result.append(movie_data)
    return search_result





