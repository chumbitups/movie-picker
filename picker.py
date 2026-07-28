from models import Movie
import random

def pick_random_movie(movies: list[Movie]) -> Movie | None:
    unwatched_movies = [movie for movie in movies if not movie.watched]

    if not unwatched_movies:
        return None
    
    return random.choice(unwatched_movies)


