from models import Movie
import random

def pick_random_movie(movies: list[Movie]) -> Movie | None:
    unwatched_movies = [movie for movie in movies if not movie.watched]

    if not unwatched_movies:
        return None

    weights = [
        calculate_movie_weight(movie)
        for movie in unwatched_movies
    ]

    selected_movie = random.choices(
        population=unwatched_movies,
        weights=weights,
        k=1
    )
    return selected_movie[0]

def calculate_movie_weight(movie: Movie) -> float:
    weight = 1 / (movie.recommendation_count + 1)
    return weight

def register_recommendation(movie: Movie) -> None:
    movie.recommendation_count += 1

def mark_movie_as_watched(movie: Movie):
    movie.watched = True






