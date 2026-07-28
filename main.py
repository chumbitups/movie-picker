from models import Movie
from picker import pick_random_movie

movie1 = Movie("The Reader", 2008, True)
movie2 = Movie("Nosferatu", 2024, True)
movie3 = Movie("The Witch", 2015)
movie4 = Movie("Finally Dawn", 2023)
movie5 = Movie("Everytime", 2026)
movie6 = Movie("Hope", 2026)

movies = [movie1, movie2, movie3, movie4, movie5, movie6]
selected_movie = pick_random_movie(movies)

if selected_movie is None:
    print("В списке не осталось непросмотренных фильмов")
else: 
    print(f"{selected_movie.title} ({selected_movie.year})")