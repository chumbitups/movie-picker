from models import Movie
from storage import save_movies, load_movies
from picker import (
    pick_random_movie,
    register_recommendation,
    mark_movie_as_watched,
)
from tmdb_client import (
    search_movie, 
    find_movie_match, 
    get_movie_details
)

movies = load_movies("data/movies.json")

if not movies:
    movies = [
    Movie("Arrival", 2019),
    Movie("The Avatar", 2008),
    Movie("The Odyssey", 2026),
    ]


def run_app(movies: list[Movie]) -> None:
    while True:
        selected_movie = pick_random_movie(movies)

        if selected_movie is None:
            print("No movies left")
            break

        register_recommendation(selected_movie)
        save_movies(movies, "data/movies.json")

        print()
        print(f"Your next movie is: {selected_movie.title} ({selected_movie.year})")

        while True:
            print("1 - I have watched this movie")
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
    details = get_movie_details(329865)
    
    print(details.get("title"))
    print(details.get("runtime"))
    print(details.get("genres"))
    print(details.get("production_countries"))
    
    run_app(movies)

    

