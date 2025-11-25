from random import randint
from statistics import median, mean

from movie_db import movies
from ui_helper_functions import (
    print_intro,
    print_menu,
    print_title,
    clear_screen,
    wait_for_enter,
    print_message,
)


def list_movies():
    """list all movies"""
    if movies:
        print(f"\n  There are {len(movies)} movies in the database.\n")

        # print all movies by iterating through dict items
        for movie, info in movies.items():
            print(f"  {movie} ({info['year']}): {info['rating']}")
    else:
        print("\n  The database is empty!")


def add_movie():
    """adds a movie"""
    name = input(
        "\n  Please enter the name of the movie you want to add:\n\n  "
    )
    # check if movie name given
    if len(name) == 0:
        print_message("Error! Movie name cannot be empty.")
    # check if movie name already exists in the database
    elif movies.get(name) is None:
        year = int(
            input(
                "\n  Please enter the year of the movie you want to add:"
                + "\n\n  "
            )
            or "0"
        )
        rating = float(
            input(
                "\n  Please enter the rating of the movie you want to add:"
                + "\n\n  "
            )
            or "0"
        )
        # check if rating was given
        if year == 0 or rating == 0:
            print_message("Error! Movie info not complete.")
        else:
            # update dict with new key:value pair
            movies[name] = {"year": year, "rating": rating}
            print_message(
                f"Added {name} ({year}) "
                + f"with the rating {rating} to the database."
            )
        # no rating given
    # key name already in dict
    else:
        print_message(f"Error! Movie {name} is already in the database.")


def delete_movie():
    """delete a movie"""
    list_movies()

    name = input(
        "\n  Please enter the name of the movie you want to delete:\n\n  "
    )

    if movies.get(name) is not None:
        # remove dict item by passing key to pop() method, returns value
        info = movies.pop(name)
        print_message(
            f"Removed {name} ({info['year']}) "
            + f"with the rating {info['rating']} from the database."
        )
    else:
        print_message(
            f"Sorry, the movie with the name {name} is not in the database."
        )


def update_movie():
    """change the rating of a movie"""
    list_movies()

    name = input(
        "\n  Please enter the name of the movie you want to update:\n\n  "
    )

    if movies.get(name) is not None:
        rating = float(
            input("\n  Please enter the new rating of the movie:\n\n  ") or "0"
        )
        movies[name].update(rating=rating)
        info = movies[name]
        print_message(
            f"Updated the movie {name} from {info['year']} "
            + f"with the new rating {info['rating']}."
        )
    else:
        print_message(
            f"Sorry, the movie with the name {name} is not in the database."
        )


def show_stats():
    """
    shows the average and median rating values of all movies and also
    information about the worst and best movies
    """
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
        print("\n  The database is empty!")


def random_movie():
    """show a random movie"""
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
        print("\n  The database is empty!")


def search_movie():
    """case insensitive search by partial name"""
    search_term = input("\n  Enter the search term:\n\n  ")

    # adds value movie to the list while iterating
    # through the dict keys the condition is met
    search_results = [
        movie for movie in movies.keys() if search_term.lower() in movie.lower()
    ]

    if search_results:
        print("\n  Here are the search results:")
        for result in search_results:
            print(f"\n  {result}: {movies.get(result)}")
    else:
        print("\n  Sorry, no matching movie found.")


def sorted_movies():
    """show a list of all movies sorted by rating"""
    print("\n  Here is the movie list sorted by rating:\n")

    sorted_list = sorted(
        movies, key=lambda movie: movies[movie]["rating"], reverse=True
    )

    for movie in sorted_list:
        info = movies[movie]
        print(f"  {movie} ({info['year']}): {info['rating']}")


menu = {
    "1": list_movies,
    "2": add_movie,
    "3": delete_movie,
    "4": update_movie,
    "5": show_stats,
    "6": random_movie,
    "7": search_movie,
    "8": sorted_movies,
    "9": print_intro,
    "0": clear_screen,
}


def main():
    """displays an intro screen and enters the main program loop"""
    print_intro()

    wait_for_enter()

    clear_screen()

    isTrue = True

    # the main loop
    while isTrue:
        # show menu screen
        print_menu()

        choice = input("  Enter choice! ")

        clear_screen()

        # screen selection
        print_title()

        if choice in map(str, range(1, 10)):
            menu[choice]()
        elif choice == "0":
            isTrue = False
            clear_screen()
            break
        else:
            print_message("Sorry, wrong Choice!")

        wait_for_enter()

        clear_screen()


if __name__ == "__main__":
    main()
