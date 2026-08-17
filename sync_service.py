from models import Movie, WatchlistItem
from tmdb_client import fetch_movie
from letterboxd_client import fetch_watchlist

def sync_watchlist(
    movies: list[Movie],
    items: list[WatchlistItem],
    unmatched: list[WatchlistItem]
) -> list[WatchlistItem]:

    unmatched_slugs = {
        item.slug
        for item in unmatched
    }
    
    current_slugs = {
        item.slug
        for item in items
    }

    local_slugs = {
        movie.letterboxd_slug
        for movie in movies
        if movie.letterboxd_slug is not None
    }

    new_items = []

    for movie in movies:
        movie.is_in_watchlist = movie.letterboxd_slug in current_slugs

    for item in items:
        if (
            item.slug not in local_slugs
            and item.slug not in unmatched_slugs
        ):
            new_items.append(item)

    return new_items

def import_new_movies(
    movies: list[Movie],
    new_items: list[WatchlistItem],
) -> list[WatchlistItem]:

    unmatched = []

    for item in new_items:
        movie = fetch_movie(item.title, item.year)

        if movie is None:
            unmatched.append(item)
            continue

        movie.letterboxd_slug = item.slug
        movie.is_in_watchlist = True

        movies.append(movie)

    return unmatched

def sync_movies(
    username: str,
    movies: list[Movie],
    unmatched: list[WatchlistItem]
) -> list[WatchlistItem]:
    
    watchlist = fetch_watchlist(username=username)

    new_items = sync_watchlist(movies=movies, items=watchlist, unmatched=unmatched)

    new_unmatched = import_new_movies(movies=movies, new_items=new_items)

    return new_unmatched

    
    

    
