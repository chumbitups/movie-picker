import pytest
from models import Movie
from picker import pick_random_movie, calculate_movie_weight, register_recommendation

movie1 = Movie("The Reader", 2008, watched=True)
movie2 = Movie("Nosferatu", 2024)
movie3 = Movie("The Witch", 2015, watched=True)
movie4 = Movie("Finally Dawn", 2023, watched=True)
movie5 = Movie("Everytime", 2026, watched=True)
movie6 = Movie("Hope", 2026, watched=True)
movie7 = Movie("Big Dawgs", 2014)
movie8 = Movie("Shawshank Redemption", 2009)
movie9 = Movie("The Dictator", 2014)
movie10 = Movie("God of War", 2018)
movie11 = Movie("Uncharted 4", 2016)

def test_only_unwatched_movies():
    test_movies = [movie1, movie2]

    selected_movie = pick_random_movie(test_movies)

    assert selected_movie != None
    assert selected_movie.watched == False


def test_only_watched_movies():
    test_movies = [movie3, movie4, movie5, movie6]

    selected_movie = pick_random_movie(test_movies)

    assert selected_movie is None

def test_list_is_none():
    test_movies = []

    selected_movie = pick_random_movie(test_movies)

    assert selected_movie is None

def test_movie_weight_without_recommendations():
    movie = Movie(
        title="Arrival",
        year=2016,
        recommendation_count=0
    )
    actual_weight = calculate_movie_weight(movie)
    assert actual_weight == 1

def test_movie_weight_with_one_recommendation():
    movie = Movie(
        title="Arrival",
        year=2016,
        recommendation_count=1
    )
    actual_weight = calculate_movie_weight(movie)
    assert actual_weight == pytest.approx(0.5)

def test_movie_weight_with_three_recommendations():
    movie = Movie(
        title="Arrival",
        year=2016,
        recommendation_count=3
    )
    actual_weight = calculate_movie_weight(movie)
    assert actual_weight == pytest.approx(0.25)

def test_registered_counts():
    movie1 = Movie(
        title="Arrival",
        year=2016,
        recommendation_count=0
        )

    movie2 = Movie(
        title="Departure",
        year=2015,
        recommendation_count=3
    )

    register_recommendation(movie1)
    register_recommendation(movie2)

    assert movie1.recommendation_count == 1
    assert movie2.recommendation_count == 4

def test_register_unselected_movie():
    register_recommendation(movie1)
    register_recommendation(movie2)

    assert movie1.recommendation_count == 1
    assert movie2.recommendation_count == 1
    assert movie3.recommendation_count == 0


