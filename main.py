from models import Movie
from storage import save_movies, load_movies
from picker import (
    pick_random_movie,
    register_recommendation,
    mark_movie_as_watched,
    print_movie_info
)

from tmdb_client import (
    search_movie, 
    find_movie_match, 
    get_movie_details,
    movie_from_tmdb
)
from letterboxd_client import fetch_watchlist_page, parse_watchlist_page

from storage import (
    load_movies,
    save_movies,
    load_watchlist_items,
    save_watchlist_items,
)

from sync_service import sync_movies

import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("LETTERBOXD_USERNAME")

if username is None: 
    raise RuntimeError("LETTERBOXD_USERNAME is not set")

def run_app(movies):
    while True:
        selected_movie = pick_random_movie(movies)

        if selected_movie is None:
            print("No movies left")
            break

        register_recommendation(selected_movie)
        save_movies(movies, "data/movies.json")

        print()
        print_movie_info(selected_movie)

        while True:
            print()
            print("1 - I like this one!")
            print("2 - Recommend another one")
            print("0 - Exit")

            command = input("Your pick is: ")

            if command == "1":
                mark_movie_as_watched(selected_movie)
                print(f"'{selected_movie.title}' marked as watched")
                save_movies(movies, "data/movies.json")
                break

            elif command == "2":
                break

            elif command == "0":
                break

            else:
                print("Unknown command. Please input 1, 2 or 0")

        if command == "1" or command == "0":
            break

if __name__ == "__main__":
    movies = load_movies("data/movies.json")

    unmatched = load_watchlist_items("data/unmatched.json")

    sync_movies(
        username=username,
        movies=movies,
        unmatched=unmatched
    )

    save_movies(movies, "data/movies.json")

    save_watchlist_items(unmatched, "data/unmatched.json")

    run_app(movies)
    

