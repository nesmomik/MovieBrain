from random import randint
from statistics import median, mean
from dotenv import dotenv_values
import requests

# switch between json and sql storage
# from db_handler import movie_storage_json as storage
from db_handler import movie_storage_sql as storage
from html_display import html_generator

from ui_helper import (
    print_intro,
    print_exit,
    print_menu,
    print_title,
    clear_screen,
    wait_for_enter,
    print_message,
    print_sub_menu,
)

# read api key from .env file
OMDB_API_KEY = dotenv_values(".env")["OMDB_API_KEY"]


def list_movies():
    """list all movies"""
    # load movies from the database
    movies = storage.get_movies()

    if movies:
        print(f"\n  There are {len(movies)} movies in the database.\n")

        # print all movies by iterating through dict items
        for movie, info in movies.items():
            print(f"  {movie} ({info['year']}): {info['rating']}")
    else:
        print_message("\n  The database is empty!")


def get_rating(message):
    """prints the message and returns a rating"""
    while True:
        try:
            rating = float(input(message))
            if 0 <= rating <= 10:
                return rating
        except ValueError:
            print("\n  That was not a number.")

        print("\n  Please enter a valid number between 0 and 10!")

    return rating


def get_year(message):
    """prints the message and returns a year"""
    while True:
        try:
            year = int(input(message))
            break
        except ValueError:
            print("\n  Sorry, that was not a number.")

    return year


def add_movie():
    """adds a movie"""
    is_not_valid = True
    while is_not_valid:
        name = input(
            "\n  Please enter the name of the movie you want to add:\n\n  "
        )
        # check if movie name given
        if not name:
            print_message("Error! Movie name cannot be empty.")
            wait_for_enter()
            clear_screen()
            print_title()
        else:
            is_not_valid = False
            break

    movies = storage.get_movies()

    payload = {'apikey': OMDB_API_KEY, 't': name}
    try:
        response = requests.get(
            'https://www.omdbapi.com/',
            params=payload,
            timeout=5
            )
    except requests.exceptions.ConnectionError:
        print_message("Sorry, can't connect to the search API.")
        return
    except requests.exceptions.Timeout:
        print_message("Sorry, the connection timed out.")
        return

    # response is a json object so data is a dictionary
    data = response.json()

    if data['Response'] == "True":
        # check if movie name already exists in the database
        if movies.get(data['Title']) is None:
            # save movie
            storage.add_movie(
                data['Title'],
                data['Year'],
                data['imdbRating'],
                data['Poster']
            )

            print_message(
                f"Added {data['Title']} ({data['Year']}) "
                + f"with the rating {data['imdbRating']} to the database."
            )
        else:
            print_message("Sorry, no movie found!")
    else:
        print_message(f"Error! Movie {name} is already in the database.")


def delete_movie():
    """delete a movie"""
    list_movies()

    name = input(
        "\n  Please enter the name of the movie you want to delete:\n\n  "
    )

    if not name:
        print_message("Sorry, you did not enter a movie name!")
    else:
        movies = storage.get_movies()

        if movies.get(name) is not None:
            info = movies[name]
            storage.delete_movie(name)
            print_message(
                f"Removed {name} ({info['year']}) "
                + f"with the rating {info['rating']} from the database."
            )
        else:
            print_message(
                f"Sorry, the movie with the name {name} "
                + "is not in the database."
            )


def update_movie():
    """change the rating of a movie"""
    list_movies()

    name = input(
        "\n  Please enter the name of the movie you want to update:\n\n  "
    )

    if not name:
        print_message("Sorry, you did not enter a movie name!")
    else:
        movies = storage.get_movies()

        if movies.get(name) is not None:
            new_rating = get_rating(
                "\n  Please enter a new rating" + " for the movie:\n\n  "
            )
            info = movies[name]
            storage.update_movie(name, new_rating)
            print_message(
                f"Updated the movie {name} from {info['year']} "
                + f"with the new rating {new_rating}."
            )
        else:
            print_message(
                f"Sorry, the movie with the name {name} "
                + "is not in the database."
            )


def show_stats():
    """
    shows the average and median rating values of all movies and also
    information about the worst and best movies
    """
    movies = storage.get_movies()

    if movies:
        print("\n  Here are some fresh stats from the database:")

        # get list of all movie ratings
        rating_list = []
        for movie in movies.values():
            rating_list.append(movie["rating"])
        # calculate and print average
        avg_rating = mean(rating_list)
        print(
            "\n\n  The average rating of the movies is: "
            + f"{round(avg_rating, 1)}"
        )

        # calculate and print median value
        print(
            "\n  The median rating of the movies is: "
            + f"{round(median(rating_list), 1)}"
        )

        # get maximum rating and print movie(s) with max rating
        max_rating = max(rating_list)
        best_movies = []
        # build list by iterating through dict items
        for movie in movies:
            if movies[movie]["rating"] == max_rating:
                best_movies.append(movie)

        print("\n  The best rated movie(s):")
        for movie in best_movies:
            print(
                f"\n  {movie} ({movies[movie]['year']}): "
                + f"{movies[movie]['rating']}"
            )

        # get minimum rating and print movie(s) with min rating
        min_rating = min(rating_list)
        # build list with list comprehension
        worst_movies = [
            movie for movie in movies if movies[movie]["rating"] == min_rating
        ]
        print("\n  The worst rated movie(s):")
        for movie in worst_movies:
            print(
                f"\n  {movie} ({movies[movie]['year']}): "
                + f"{movies[movie]['rating']}"
            )
    else:
        print_message("\n  The database is empty!")


def random_movie():
    """show a random movie"""
    movies = storage.get_movies()

    # check for movies in database
    if movies:
        print("\n  Here is a random movie from the database:")
        # generate random index
        index = randint(0, len(movies))
        # get movie info for index
        names = list(movies.keys())
        info = movies[names[index]]
        # print movie info
        print(f"\n\n\n  {names[index]} ({info['year']}): {info['rating']}\n\n")
    else:
        print_message("\n  The database is empty!")


def search_movie():
    """case insensitive search by partial name"""
    search_term = input("\n  Enter the search term:\n\n  ")

    if not search_term:
        print("\n  No search term given. Listing all movies!")
        list_movies()
    else:
        movies = storage.get_movies()
        # adds value movie to the list while iterating
        # through the dict keys the condition is met
        search_results = [
            movie for movie in movies if search_term.lower() in movie.lower()
        ]

        if search_results:
            print("\n  Here are the search results:")
            for result in search_results:
                print(
                    f"\n  {result} ({movies[result]['year']})"
                    + f": {movies[result]['rating']}"
                )
        else:
            print("\n  Sorry, no matching movie found.")


def sorted_movies(movies, info_type, bool_direction):
    """
    Takes a list of movies, the info_type to sort by and a bool value to
    specify to sort direction (False for ascending, True for descending)
    """
    sorted_list = sorted(
        movies,
        key=lambda movie: movies[movie][info_type],
        reverse=bool_direction,
    )

    for movie in sorted_list:
        info = movies[movie]
        print(f"  {movie} ({info['year']}): {info['rating']}")


def sort_movies():
    """
    Shows a menu with the sort options and calls the functions
    to display the results.
    """
    try:
        _, info_type, bool_direction = print_sub_menu("sort")
    except TypeError:
        return

    print(f"\n  Here is the movie list sorted by {info_type}:\n")

    movies = storage.get_movies()
    sorted_movies(movies, info_type, bool_direction)


def filter_movies():
    """
    Shows a menu with the filter options and calls the functions
    to display the results.
    """
    try:
        choice, info_type, bool_direction = print_sub_menu("filter")
    except TypeError:
        return

    print("\n  Please enter the start and end value to filter by.")


    if choice == "1" or choice == "2":
        start = get_rating("\n  Please enter the start rating:\n\n  ")
        end = get_rating("\n  Please enter the end rating:\n\n  ")
    elif choice == "3" or choice == "4":
        start = get_year("\n  Please enter the start year:\n\n  ")
        end = get_year("\n  Please enter the end year:\n\n  ")

    print(f"\n  Here is the movie list filtered by {info_type}:\n")

    movies = storage.get_movies()
    filtered_movies = get_filtered_movies(movies, info_type, start, end)
    sorted_movies(filtered_movies, info_type, bool_direction)



def get_filtered_movies(movies, info_type, start, end):
    """
    Filters a dict of dict of movies according to info_type
    and start and end values
    """
    movies = storage.get_movies()

    results = {}

    for movie in movies:
        info = movies[movie]
        if start <= info[info_type] <= end:
            results[movie] = info

    return results


menu = {
    "1": list_movies,
    "2": add_movie,
    "3": delete_movie,
    "4": update_movie,
    "5": show_stats,
    "6": random_movie,
    "7": search_movie,
    "8": sort_movies,
    "9": filter_movies,
}

def main():
    """displays an intro screen and enters the main program loop"""
    print_intro()

    wait_for_enter()

    clear_screen()

    # the main loop
    while True:
        # show menu screen
        print_menu()

        html_generator.show_link()

        html_generator.generate_html_file()

        choice = input("  Enter choice! ")

        clear_screen()

        # screen selection
        print_title()

        if choice in map(str, range(1, 10)):
            menu[choice]()
        elif choice == "0":
            clear_screen()
            print_exit()
            break
        else:
            print_message("Sorry, invalid choice!")

        wait_for_enter()

        clear_screen()


if __name__ == "__main__":
    main()
