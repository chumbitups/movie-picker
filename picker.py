from models import Movie, MovieFilter
import random


def pick_random_movie(movies: list[Movie]) -> Movie | None:
    unwatched_movies = [movie for movie in movies if not movie.watched and movie.is_in_watchlist]

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

def print_movie_info(movie: Movie):
    print(f"{movie.title} ({movie.year})")
    print()

    if movie.rating is not None:
        print(f"Rating: {movie.rating:.1f}")

    if movie.runtime is not None:
        print(f"Runtime: {movie.runtime} Minutes")

    if movie.genres:
        print(f"Genres: {", ".join(movie.genres)}")

    if movie.countries:
        print(f"Countries: {", ".join(movie.countries)}")

    if movie.description:
        print()
        print(movie.description)

def filter_movies(
    movies: list[Movie],
    filters: MovieFilter,
) -> list[Movie]:

    result = []

    for movie in movies:
        if filters.genre is not None:
            normalized_genres = [
                genre.casefold()
                for genre in movie.genres
            ]   

            if filters.genre.casefold() not in normalized_genres:
                continue

        if filters.year_from is not None:
            if movie.year < filters.year_from:
                continue

        if filters.year_to is not None:
            if movie.year > filters.year_to:
                continue

        if filters.country is not None:
            normalized_countries = [
                country.casefold()
                for country in movie.countries
            ]

            if filters.country.casefold() not in normalized_countries:
                continue

        if filters.max_runtime is not None:
            if movie.runtime is None:
                continue
            if movie.runtime > filters.max_runtime:
                continue

        if filters.min_rating is not None:
            if movie.rating is None:
                continue
            if movie.rating < filters.min_rating:
                continue

        result.append(movie)

    return result


    








