from random import randint
from statistics import median

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
    print(f"\n  There are {len(movies)} movies in the database.\n")

    # print all movies by iterating through dict items
    for movie, rating in movies.items():
        print(f"  {movie}: {rating}")


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
        rating = float(
            input(
                "\n  Please enter the rating of the movie you want to add:"
                + "\n\n  "
            )
            or "0"
        )
        # check if rating was given
        if rating == 0:
            print_message("Error! Movie rating cannot be empty.")
        else:
            # update dict with new key:value pair
            movies.update({name: rating})
            print_message(
                f"Added {name} with the rating {rating} to the database."
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
        rating = movies.pop(name)
        print_message(
            f"Removed {name} with the rating {rating} from the database."
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
        movies.update({name: rating})
        print_message(f"Updated the movie {name} "
                      + "with the new rating {rating}.")
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

        # calculate and print average
        rating_list = list(movies.values())
        list_length = len(movies)
        avg_rating = sum(rating_list) / list_length
        print("\n\n  The average rating of the movies is: "
              + f"{round(avg_rating, 1)}")

        # calculate and print median value
        print(
            "\n  The median rating of the movies is: "
            + f"{round(median(rating_list), 1)}"
        )

        # get maximum rating and print movie(s) with max rating
        max_rating = max(rating_list)
        best_movies = []
        # build list by iterating through dict items
        for movie, rating in movies.items():
            if rating == max_rating:
                best_movies.append(movie)

        print("\n  The best rated movie(s):")
        for movie in best_movies:
            print(f"\n  {movie}: {movies.get(movie)}")

        # get minimum rating and print movie(s) with min rating
        min_rating = min(rating_list)
        # build list with list comprehension
        worst_movies = [
            movie for movie, rating in movies.items() if rating == min_rating
        ]
        print("\n  The worst rated movie(s):")
        for movie in worst_movies:
            print(f"\n  {movie}: {movies.get(movie)}")
    else:
        print("\n  The database is empty!")


def random_movie():
    """show a random movie"""
    # check for movies in database
    if movies:
        print("\n  Here is a random movie from the database:")

        i = 0
        # generate random index
        movie_index = randint(0, len(movies))
        # get movie info for index
        for movie, rating in movies.items():
            if i == movie_index:
                break
            i += 1
        # print movie info
        print(f"\n\n\n  {movie}: {rating}\n\n")
    else:
        print("\n  The database is empty!")

def search_movie():
    """case insensitive search by partial name"""
    search_term = input("\n  Enter the search term:\n\n  ")

    # adds value movie to the list when while iterating
    # through the dict keys the condition is met
    search_results = [
        movie for movie in movies.keys() \
        if search_term.lower() in movie.lower()
    ]

    print("\n  Here are the search results:")

    for result in search_results:
        print(f"\n  {result}: {movies.get(result)}")


def get_rating(list_item):
    """used to provide the key for the sort in sorted_movies"""
    return list_item[1]


def sorted_movies():
    """show a sorted list of all movies"""
    print("\n  Here is the movie list sorted by rating:\n")

    movie_tuple_list = []
    # create list of tupels
    for movie, rating in movies.items():
        movie_tuple_list.append((movie, rating))
    # sort tuple list by rating in descending order
    movie_tuple_list.sort(reverse=True, key=get_rating)

    for movie, rating in movie_tuple_list:
        print(f"  {movie}: {rating}")


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
    "0": clear_screen
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

#        # TODO: Refactor to dispatch table
#        if choice == "1":
#            list_movies()
#        elif choice == "2":
#            add_movie()
#        elif choice == "3":
#            delete_movie()
#        elif choice == "4":
#            update_movie()
#        elif choice == "5":
#            show_stats()
#        elif choice == "6":
#            random_movie()
#        elif choice == "7":
#            search_movie()
#        elif choice == "8":
#            sorted_movies()
#        elif choice == "9":
#            print_intro()
#        elif choice == "0":
#            isTrue = False
#            clear_screen()
#            break
#        else:
#            print_message("Sorry, wrong Choice!")

        wait_for_enter()

        clear_screen()


if __name__ == "__main__":
    main()
