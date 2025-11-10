from random import randint

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
    print(f"\n  There are {len(movies)} movies in the database.\n")

    # print all movies by iterating through dict items
    for movie, rating in movies.items():
        print(f"  {movie}: {rating}")


def add_movie():
    name = input("\n  Please enter the name of the movie you want to add:\n\n  ")
    # check if movie name given
    if len(name) == 0:
        print_message("Error! Movie name cannot be empty.")
    # check if movie name already exists in the database
    elif movies.get(name) is None:
        rating = float(
            input("\n  Please enter the rating of the movie you want to add:\n\n  ") or "0"
        )
        # check if rating was given
        if rating == 0:
            print_message("Error! Movie rating cannot be empty.")
        else:
            # update dict with new key:value pair
            movies.update({name: rating})
            print_message(f"Added {name} with the rating {rating} to the database.")
        # no rating given
    # key name already in dict
    else:
        print_message(f"Error! Movie {name} is already in the database.")


def delete_movie():
    list_movies()

    name = input("\n  Please enter the name of the movie you want to delete:\n\n  ")

    if movies.get(name) is not None:
        # remove dict item by passing key to pop() method, returns value
        rating = movies.pop(name)
        print_message(f"Removed {name} with the rating {rating} from the database.")
    else:
        print_message(f"Sorry, the movie with the name {name} is not in the database.")


def update_movie():
    list_movies()

    name = input("\n  Please enter the name of the movie you want to update:\n\n  ")

    if movies.get(name) is not None:
        rating = float(
            input("\n  Please enter the new rating of the movie:\n\n  ") or "0"
        )
        movies.update({name: rating})
        print_message(f"Updated the movie {name} with the new rating {rating}.")
    else:
        print_message(f"Sorry, the movie with the name {name} is not in the database.")


def show_stats():
    print("\n  Here are some fresh stats from the database:")

    # calculate and print average
    rating_list = list(movies.values())
    list_length = len(movies)
    avg_rating = sum(rating_list) / list_length
    print(f"\n\n  The average rating of the movies is: {round(avg_rating, 1)}")

    # calculate and print median value
    if list_length % 2 != 0:
        # if list length uneven take the middle element
        median_rating = rating_list[(list_length - 1) // 2]
    else:
        # else calculate average of both middle elements
        median_rating = (
            rating_list[(list_length // 2) - 1] + rating_list[list_length // 2]
        ) / 2
    print(f"\n  The median rating of the movies is: {round(median_rating, 1)}")

    # get maximum rating and print movie(s) with max rating
    max_rating = max(rating_list)
    best_movies = []
    # build list by iterating through dict items
    for movie, rating in movies.items():
        if rating == max_rating:
            best_movies.append(movie)

    if len(best_movies) == 1:
        print(f"\n  The best rated movie is: {best_movies[0]}")
    else:
        print("\n  The best rated movies are:")
        for i in range(len(best_movies)):
            print(f"\n  {best_movies[i]}")

    # get minimum rating and print movie(s) with min rating
    min_rating = min(rating_list)
    # build list with list comprehension
    worst_movies = [movie for movie, rating in movies.items() if rating == min_rating]

    if len(worst_movies) == 1:
        print(f"\n  The worst rated movie is: {worst_movies[0]}")
    else:
        print("\n  The worst rated movies are:")
        for i in range(len(worst_movies)):
            print(f"\n  {worst_movies[i]}")


def random_movie():
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


def search_movie():
    search_term = input("\n  Enter the search term:\n\n  ")

    # adds value movie to the list when while iterating through the dict keys the condition is met
    search_results = [movie for movie in movies.keys() if search_term in movie]

    print("\n  Here are the search results:")

    for result in search_results:
        print(f"\n  {result}: {movies.get(result)}")


def sorted_movies():
    print("\n  Here is the movie list sorted by rating:\n")

    sorted_rating_list = list(movies.values())
    # sort rating in descending order
    sorted_rating_list.sort(reverse=True)
    sorted_movie_list = []
    i = 0
    # repeat as often as the count of movies in the list
    # i also used to index sorted_rating_list
    while i < len(movies):
        # go through sorted_rating_list in order and add tupel
        # to sorted_movie_list in the right order
        for movie, rating in movies.items():
            if rating == sorted_rating_list[i]:
                sorted_movie_list.append((movie, rating))
                break
        i += 1

    for movie, rating in sorted_movie_list:
        print(f"  {movie}: {rating}")


def main():
    print_intro()

    wait_for_enter()

    clear_screen()

    isTrue = True

    while isTrue:
        # show menu screen
        print_menu()

        choice = input("  Enter choice! ")

        clear_screen()

        # screen selection
        print_title()

        if choice == "1":
            list_movies()
        elif choice == "2":
            add_movie()
        elif choice == "3":
            delete_movie()
        elif choice == "4":
            update_movie()
        elif choice == "5":
            show_stats()
        elif choice == "6":
            random_movie()
        elif choice == "7":
            search_movie()
        elif choice == "8":
            sorted_movies()
        elif choice == "9":
            print_intro()
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
