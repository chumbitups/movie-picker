from models import Movie, MovieFilter
from storage import save_movies, load_movies
from picker import (
    pick_random_movie,
    register_recommendation,
    mark_movie_as_watched,
    print_movie_info,
    filter_movies
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

def ask_optional_int(prompt: str) -> int | None:
    while True:
        value = input(prompt).strip()

        if value == "": 
            return None 

        try:
            return int(value)
        except ValueError:
            print("Please enter a number or leave empty.")

def check_min_rating(prompt: str) -> float | None:
    while True:
        value = input(prompt).strip()

        if value == "":
            return None

        try:
            number = float(value) 
        except ValueError:
            print("Please enter a number or leave empty")
            continue

        if 0 <= number <= 10:
            return number

        print("Rating must be between 0 and 10")

def check_year_range() -> tuple[int | None, int | None]:
    while True:
        year_from = ask_optional_int("Year from: ")
        year_to = ask_optional_int("Year to: ")

        if (
            year_from is not None
            and year_to is not None
            and year_from > year_to
        ):
            print("Year from can not be greater than year to.")
            continue
        return year_from, year_to

def check_max_runtime() -> int | None:
    while True:
        runtime = ask_optional_int("Max runtime (minutes): ")

        if runtime is None:
            return None

        if runtime > 0:
            return runtime

        print("Runtime must be greater than 0")

def ask_movie_filters() -> MovieFilter:
    genre_input = input("Genre (empty = any): ").strip()

    genre = None if genre_input == "" else genre_input

    year_from, year_to = check_year_range()

    country_input = input("Country: ").strip()
    country = country_input or None

    max_runtime = check_max_runtime()

    min_rating = check_min_rating("Min rating (0-10): ")
    
    return MovieFilter(
        genre=genre,
        year_from=year_from,
        year_to=year_to,
        country=country,
        max_runtime=max_runtime,
        min_rating=min_rating
    )            

def run_app(movies: list[Movie]) -> None:
    filters = ask_movie_filters()

    while True:
        filtered_movies = filter_movies(movies, filters)

        if not filtered_movies:
            print("No movies match your filters")
            filters = ask_movie_filters()
            continue

        selected_movie = pick_random_movie(filtered_movies)

        if selected_movie is None:
            print("No unwatched movies match your filters")
            filters = ask_movie_filters()
            continue

        register_recommendation(selected_movie)
        save_movies(movies, "data/movies.json")

        print()
        print_movie_info(selected_movie)

        while True:
            print()
            print("1 - I watched this")
            print("2 - Recommend another with same filters")
            print("3 - Change filters")
            print("0 - Exit")

            command = input("Your pick is: ")

            if command == "1":
                mark_movie_as_watched(selected_movie)
                print(f"'{selected_movie.title}' marked as watched")
                save_movies(movies, "data/movies.json")
                break

            elif command == "2":
                break

            elif command == "3":
                filters = ask_movie_filters()
                break

            elif command == "0":
                return

            else:
                print("Unknown command. Please input 1, 2, 3 or 0")


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
    

