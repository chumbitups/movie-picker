from models import WatchlistItem, Movie
from tmdb_client import fetch_movie, search_movie

def enrich_watchlist(items: list[WatchlistItem]) -> tuple[list[Movie], list[WatchlistItem]]:
    
    movies = []
    unmatched = []

    for item in items:
        movie = fetch_movie(item.title, item.year)

        if movie is None:
            unmatched.append(item)
            continue

        movies.append(movie)

    return movies, unmatched

if __name__ == "__main__":
    items = [
        WatchlistItem("Arrival", 2016, "arrival"),
        WatchlistItem("Perfect Blue", 1997, "perfect-blue"),
        WatchlistItem(
            "This Movie Definitely Does Not Exist",
            1900,
            "nothing"
        ),
    ]
    movies, unmatched = enrich_watchlist(items=items)

    for item in unmatched:
        print(item.title, item.year)

    print("Matched:", len(movies))
    print("Unmatched", len(unmatched))

    results = search_movie("Perfect Blue", 1997)

    for result in results[:5]:
        print(
            result.get("title"),
            result.get("original_title"),
            result.get("release_date"),
            result.get("id")
        )