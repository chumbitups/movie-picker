import pytest
import tmdb_client
import httpx
from tmdb_client import find_movie_match, movie_from_tmdb, normalize_title


results = [
        {
            "id": 1,
            "title": "Arrival",
            "release_date": "2016-11-10"
        },
        {
            "id": 2,
            "title": "Arrival",
            "release_date": "1996-05-31"
        }
    ]

def test_id_return():
    matched_movie = find_movie_match(results, "Arrival", 2016)
    assert matched_movie["id"] == 1

def test_unmatched_year():
    matched_movie = find_movie_match(results, "Arrival", 292848)
    assert matched_movie is None

def test_empty_results():
    empty_results = []
    matched_movie = find_movie_match(empty_results, "Arrival", 2016)
    assert matched_movie is None

def test_empty_release_date():
    results_without_release = [
        {
            "id": 1,
            "title": "Arrival",
            "release_date": ""
        },
        {
            "id": 2,
            "title": "Arrival",
            "release_date": "2016-05-31"
        }
    ]
    matched_movie = find_movie_match(results_without_release, "Arrival", 2016)
    assert matched_movie is not None 
    assert matched_movie["id"] == 2

def test_casefold():
    matched_movie = find_movie_match(results, "arrival", 2016)
    assert matched_movie is not None

def test_movie_from_tmdb():
    details = {
        "id": 123,
        "title": "Test Movie",
        "release_date": "2020-05-12",
        "overview": "Description",
        "runtime": 110,
        "vote_average": 8.1,
        "poster_path": "/poster.jpg",
        "genres": [
            {"id": 1, "name": "Drama"},
            {"id": 2, "name": "Thriller"},
        ],
        "production_countries": [
            {"iso_3166_1": "JP", "name": "Japan"}
        ],
    }

    test_movie = movie_from_tmdb(details=details)
    assert test_movie.genres == ["Drama", "Thriller"]
    assert test_movie.countries == ["Japan"]

def test_fetch_movie(monkeypatch):
    def fake_search_movie(title, year=None):
        if title == "Arrival" and year == 2016:
            return [
                {
                    "id": 123,
                    "title": "Arrival",
                    "release_date": "2016-11-10",
                }
            ]

        if title == "Perfect Blue" and year == 1997:
            return []

        if title == "Perfect Blue" and year is None:
            return [
                {
                    "id": 456,
                    "title": "Perfect Blue",
                    "release_date": "1998-02-28",
                }
            ]
        return []

    def fake_get_movie_details(movie_id):
        if movie_id == 123:
            return {
                "id": 123,
                "title": "Arrival",
                "release_date": "2016-11-10",
                "overview": "Test description",
                "runtime": 116,
                "vote_average": 7.6,
                "poster_path": "/arrival.jpg",
                "genres": [
                    {"id": 1, "name": "Drama"},
                ],
                "production_countries": [
                    {
                        "iso_3166_1": "US",
                        "name": "United States",
                    }
                ],
            }

        if movie_id == 456:
            return {
                "id": 456,
                "title": "Perfect Blue",
                "release_date": "1998-02-28",
                "overview": "Perfect Blue description",
                "runtime": 81,
                "vote_average": 8.3,
                "poster_path": "/perfect-blue.jpg",
                "genres": [
                    {"id": 2, "name": "Animation"},
                ],
                "production_countries": [
                    {
                        "iso_3166_1": "JP",
                        "name": "Japan",
                    }
                ],
            }

    monkeypatch.setattr(
        tmdb_client,
        "search_movie",
        fake_search_movie,
    )

    monkeypatch.setattr(
        tmdb_client,
        "get_movie_details",
        fake_get_movie_details,
    )

    movie = tmdb_client.fetch_movie("Arrival", 2016)
    movie2 = tmdb_client.fetch_movie("Perfect Blue", 1997)

    assert movie is not None
    assert movie.tmdb_id == 123
    assert movie.title == "Arrival"
    assert movie.year == 2016

    assert movie2 is not None
    assert movie2.tmdb_id == 456
    assert movie2.title == "Perfect Blue"
    assert movie2.year == 1998

def test_find_movie_match_allows_one_year_diff():
    results = [
        {
            "id": 123,
            "title": "Perfect Blue",
            "release_date": "1998-02-28",
        }
    ]

    match = find_movie_match(
        results,
        "Perfect Blue",
        1997
    )

    assert match is not None
    assert match["id"] == 123

def test_normalize_title_dashes():
    letterboxd_title = "Mission: Impossible – The Final Reckoning"
    tmdb_title = "Mission: Impossible - The Final Reckoning"

    assert normalize_title(letterboxd_title) == normalize_title(tmdb_title)

def test_normalize_title_case_and_spaces():
    assert normalize_title("  PERFECT   BLUE ") == "perfect blue"

def test_get_retries_on_read_error(monkeypatch):
    attempts = 0

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"result": "ok"}

    def fake_get(endpoint, params=None):
        nonlocal attempts

        attempts += 1

        if attempts < 3:
            raise httpx.ReadError("Test read error")
        
        return FakeResponse()

    monkeypatch.setattr(
        tmdb_client.client,
        "get",
        fake_get
    )

    monkeypatch.setattr(
        tmdb_client.time,
        "sleep",
        lambda _: None
    )

    result = tmdb_client._get("https://example.test")

    assert attempts == 3
    assert result == {"result": "ok"}

def test_get_raises_after_three_read_errors(monkeypatch):
    attempts = 0

    def fake_get(endpoint, params=None):
        nonlocal attempts
        attempts += 1

        raise httpx.ReadError("Test read error")

    monkeypatch.setattr(
        tmdb_client.client,
        "get",
        fake_get
    )

    monkeypatch.setattr(
        tmdb_client.time,
        "sleep",
        lambda _: None
    )

    with pytest.raises(httpx.ReadError):
        tmdb_client._get("https://example.test")
        
    assert attempts == 3



