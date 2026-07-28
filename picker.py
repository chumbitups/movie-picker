from models import Movie
import random

def pick_random_movie(movies: list[Movie]) -> Movie | None:
    unwatched_movies = [movie for movie in movies if not movie.watched]

    if not unwatched_movies:
        return None
    
    return random.choice(unwatched_movies)

def pick_random_movies(movies: list[Movie], count: int = 5) -> list[Movie]:
    unwatched_movies = [movie for movie in movies if not movie.watched]

    if not unwatched_movies or count <= 0:
        return []

    movies_to_pick = min(count, len(unwatched_movies))
    return random.sample(unwatched_movies, movies_to_pick)




