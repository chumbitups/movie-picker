import json
from dataclasses import asdict
from models import Movie, WatchlistItem
from pathlib import Path

def save_movies(movies: list[Movie], path: str | None) -> None:
    file_path = Path(path)

    movies_dict = [
        asdict(movie)
        for movie in movies
    ]

    movies_json = json.dumps(
        movies_dict,
        ensure_ascii=False,
        indent=2
    )

    file_path.parent.mkdir(parents=True, exist_ok=True)

    file_path.write_text(
        movies_json,
        encoding="utf-8"
    )


def load_movies(path) -> list[Movie]:
    file_path = Path(path)

    if not file_path.exists():
        return []

    movies_json = file_path.read_text(
        encoding="utf-8"
    )

    movies_dict = json.loads(movies_json)

    return [
        Movie(**movie_dict)
        for movie_dict in movies_dict
    ]

def save_watchlist_items(
    items: list[WatchlistItem],
    path: str,
) -> None:
    
    file_path = Path(path)

    items_dict = [
        asdict(item)
        for item in items
    ]

    items_json = json.dumps(
        items_dict,
        ensure_ascii=False,
        indent=2
    )

    file_path.parent.mkdir(parents=True, exist_ok=True)

    file_path.write_text(
        items_json,
        encoding="utf-8"
    )

def load_watchlist_items(path: str) -> list[WatchlistItem]:
    file_path = Path(path)

    if not file_path.exists():
        return []

    items_json = file_path.read_text(
        encoding="utf-8"
    )

    items_dict = json.loads(items_json)

    return [
        WatchlistItem(**item_dict)
        for item_dict in items_dict
    ]

