import pytest
from models import Movie, WatchlistItem
from storage import save_movies, load_movies, save_watchlist_items, load_watchlist_items


def test_save_and_load(tmp_path: str):
    file_path = tmp_path / "movies.json"

    movies = [
        Movie("Inception", 2008),
        Movie("Interstellar", 2013),
    ]

    save_movies(movies, file_path)
    loaded_movies = load_movies(file_path)

    assert len(loaded_movies) == 2
    assert movies[0].title == "Inception" and movies[0].year == 2008 
    assert movies[1].title == "Interstellar" and movies[1].year == 2013

def test_save_state(tmp_path: str):
    file_path = tmp_path / "movies.json"

    movies = [
            Movie("Inception", 2008, True, 4),
            Movie("Interstellar", 2013, True, 4),
        ]
    
    save_movies(movies, file_path)
    loaded_movies = load_movies(file_path)

    assert movies[0].watched == True and movies[0].recommendation_count == 4
    assert movies[1].watched == True and movies[1].recommendation_count == 4

def test_empty_file(tmp_path: str):
    loaded_movies = load_movies(tmp_path / "missing.json")
    assert loaded_movies == []

def test_save_and_load_items(tmp_path: str):
    items = [
        WatchlistItem(
            title="Adolescence",
            year=2025,
            slug="adolescence"
        )
    ]

    path = tmp_path / "unmatched.json"

    save_watchlist_items(items, path)
    loaded = load_watchlist_items(path)

    assert len(loaded) == 1
    assert loaded[0].title == "Adolescence"
    assert loaded[0].year == 2025
    assert loaded[0].slug == "adolescence"