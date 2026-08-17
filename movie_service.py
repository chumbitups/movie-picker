from models import WatchlistItem, Movie
from tmdb_client import fetch_movie, search_movie
from letterboxd_client import fetch_watchlist

def enrich_watchlist(items: list[WatchlistItem]) -> tuple[list[Movie], list[WatchlistItem]]:
    
    movies = []
    unmatched = []

    for index, item in enumerate(items, start=1):
        print(f"[{index}/{len(items)}] {item.title}")

        movie = fetch_movie(item.title, item.year)

        if movie is None:
            unmatched.append(item)
            continue

        movies.append(movie)

    return movies, unmatched

if __name__ == "__main__":
    items = fetch_watchlist("chumbitups")

    print("Letterboxd:", len(items))

    movies, unmatched = enrich_watchlist(items)

    print("Matched:", len(movies))
    print("Unmatched:", len(unmatched))

    for item in unmatched:
        print(item.title, item.year)
