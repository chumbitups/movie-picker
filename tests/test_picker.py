from models import Movie
from picker import pick_random_movie

movie1 = Movie("The Reader", 2008, True)
movie2 = Movie("Nosferatu", 2024)

def test_only_unwatched_movies():
    test1_movies = [movie1, movie2]
    selected_movie = pick_random_movie(test1_movies)
    assert selected_movie != None
    assert selected_movie.watched == False

movie3 = Movie("The Witch", 2015, watched=True)
movie4 = Movie("Finally Dawn", 2023, watched=True)
movie5 = Movie("Everytime", 2026, watched=True)
movie6 = Movie("Hope", 2026, watched=True)

def test_only_watched_movies():
    test2_movies = [movie3, movie4, movie5, movie6]
    selected_movie = pick_random_movie(test2_movies)
    assert selected_movie is None

def test_empty_list():
    test3_movies = []
    selected_movie = pick_random_movie(test3_movies)
    assert selected_movie is None