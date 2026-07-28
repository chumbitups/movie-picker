from models import Movie
from picker import pick_random_movie, pick_random_movies

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

def test_6_unwatched():
    test_movies = [movie2, movie7, movie8, movie9, movie10, movie11]

    selected_movies = pick_random_movies(test_movies, 5)

    assert len(selected_movies) == 5

def test_2_unwatched():
    test_movies = [movie2, movie7]

    selected_movies = pick_random_movies(test_movies, 2)

    assert len(selected_movies) == 2

def test_empty_list():
    test_movies = []

    selected_movies = pick_random_movies(test_movies, 5)

    assert len(selected_movies) == 0

def test_zero_count():
    test_movies = [movie1, movie2, movie3]

    selected_movies = pick_random_movies(test_movies, 0)

    assert len(selected_movies) == 0

def test_no_repeating():
    test_movies = [movie1, movie1, movie2, movie2, movie3, movie4, movie4]

    selected_movies = pick_random_movies(test_movies, 5)

    titles = [movie.title for movie in selected_movies]

    assert len(titles) == len(set(titles))
