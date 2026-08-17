import pytest
from models import Movie, WatchlistItem
import sync_service

def test_sync_watchlist():
    arrival = Movie(
        title="Arrival",
        year=2016,
        letterboxd_slug="arrival"
    )

    heat = Movie(
        title="Heat",
        year=1995,
        letterboxd_slug="heat"
    )

    items = [
        WatchlistItem(
            title="Arrival",
            year=2016,
            slug="arrival"
        ),
        WatchlistItem(
            title="Heat",
            year=1995,
            slug="heat"
        ),
        WatchlistItem(
            title="Perfect Blue",
            year=1997,
            slug="perfect-blue"
        )
    ]
    movies = [arrival, heat]

    new_items = sync_service.sync_watchlist(movies, items, unmatched=[])

    assert len(new_items) == 1
    assert new_items[0].title == "Perfect Blue"
    assert new_items[0].slug == "perfect-blue"

def test_import_new_movies(monkeypatch):
    movies = [
        Movie(title="Arrival", year=2016)
    ]

    new_items = [
        WatchlistItem(
            title="Perfect Blue",
            year=1997,
            slug="perfect-blue"
        )
    ]

    def fake_fetch_movie(title, year):
        return Movie(
            title="Perfect Blue",
            year=1998,
            tmdb_id=123
        )
    
    monkeypatch.setattr(
        sync_service,
        "fetch_movie",
        fake_fetch_movie
    )

    unmatched = sync_service.import_new_movies(
        movies,
        new_items
    )

    assert unmatched == []
    assert len(movies) == 2
    assert movies[1].letterboxd_slug == "perfect-blue"
    assert movies[1].tmdb_id == 123
    assert movies[1].is_in_watchlist is True

def test_import_new_movies_adds_unmatched(monkeypatch):
    movies = []

    new_items = [
        WatchlistItem(
            title="Adolescence",
            year=2025,
            slug="adolescence"
        )
    ]

    def fake_fetch_movie(title, year):
        return None

    monkeypatch.setattr(
        sync_service,
        "fetch_movie",
        fake_fetch_movie
    )

    unmatched = sync_service.import_new_movies(
        movies,
        new_items
    )

    assert len(movies) == 0
    assert len(unmatched) == 1
    assert unmatched[0].title == "Adolescence"
    assert unmatched[0].slug == "adolescence" 

def test_sync_movies_does_not_refetch_existing_movies(monkeypatch):
    calls = 0

    movies = [
        Movie(
            title="Arrival",
            year=2016,
            letterboxd_slug="arrival"
        )
    ]

    def fake_fetch_watchlist(username):
        return [
            WatchlistItem(
                title="Arrival",
                year=2016,
                slug="arrival"
            ),
            WatchlistItem(
                title="Perfect Blue",
                year=1997,
                slug="perfect-blue"
            )
        ]

    def fake_fetch_movie(title, year):
        nonlocal calls
        calls += 1

        return Movie(
            title=title,
            year=year,
            tmdb_id=123
        )

    monkeypatch.setattr(
        sync_service,
        "fetch_watchlist",
        fake_fetch_watchlist
    )

    monkeypatch.setattr(
        sync_service,
        "fetch_movie",
        fake_fetch_movie
    )

    unmatched = []

    sync_service.sync_movies("test-user", movies, unmatched)

    assert calls == 1
    assert len(movies) == 2

    sync_service.sync_movies("test-user", movies, unmatched)

    assert calls == 1
    assert len(movies) == 2

def test_sync_watchlist_skips_known_unmatched():
    movies = [
        Movie(
            title="Arrival",
            year=2016,
            letterboxd_slug="arrival"
        )
    ]

    unmatched = [
        WatchlistItem(
            title="Adolescence",
            year=2025,
            slug="adolescence"
        )
    ]

    items = [
        WatchlistItem(
            title="Arrival",
            year=2016,
            slug="arrival"
        ),
        WatchlistItem(
            title="Adolescence",
            year=2025,
            slug="adolescence"
        ),
        WatchlistItem(
            title="Perfect Blue",
            year=1997,
            slug="perfect-blue"
        ),
    ]

    new_items = sync_service.sync_watchlist(
        movies=movies,
        items=items,
        unmatched=unmatched
    )

    assert len(new_items) == 1
    assert new_items[0].title == "Perfect Blue"
    assert new_items[0].slug == "perfect-blue"

