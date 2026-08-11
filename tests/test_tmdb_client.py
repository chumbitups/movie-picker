import pytest
from tmdb_client import search_movie, find_movie_match, movie_from_tmdb

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



