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

def pick_random_movies(movies: list[Movie], count: int = 5) -> list[Movie]:
    unwatched_movies = [movie for movie in movies if not movie.watched]

    if not unwatched_movies or count <= 0:
        return []

    movies_to_pick = min(count, len(unwatched_movies))
    return random.sample(unwatched_movies, movies_to_pick)

def calculate_movie_weight(movie: Movie) -> float:
    weight = 1 / (movie.recommendation_count + 1)
    return weight

def register_recommendations(movies: list[Movie]) -> None:
    for movie in movies:
        movie.recommendation_count += 1






