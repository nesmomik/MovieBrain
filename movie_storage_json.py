import json

JSON_DATA_FILE = "data.json"


def test_func():
    print("test_func!")


def get_movies():
    """
    Returns a dictionary of dictionaries that
    contains the movies information in the database.
    """
    with open(JSON_DATA_FILE, "r") as handle:
        return json.load(handle)


def save_movies(movies):
    """
    Gets all your movies as an argument and saves them to the JSON file.
    """
    with open(JSON_DATA_FILE, "w") as handle:
        json.dump(movies, handle)


def add_movie(title, year, rating):
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    # update dict with new key:value pair
    movies[title] = {"year": year, "rating": rating}
    save_movies(movies)


def delete_movie(title):
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    movies.pop(title)
    save_movies(movies)


def update_movie(title, rating):
    """
    Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    movies[title].update(rating=rating)
    save_movies(movies)
