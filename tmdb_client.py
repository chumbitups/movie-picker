import os
import httpx
from dotenv import load_dotenv
from models import Movie

load_dotenv()
token = os.getenv("TMDB_TOKEN")
if token is None:
    raise RuntimeError("TMDB_TOKEN is not set")

def search_movie(title: str, year: int):
    url = "https://api.themoviedb.org/3/search/movie"

    headers = {
        "Authorization": f"Bearer {token}" 
    }

    params = {
        "query": title,
        "primary_release_year": year,
    }
    response = httpx.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    return data["results"]

def find_movie_match(results: list, title: str, year: int):
    for movie in results:
        movie_title = movie.get("title")
        release_date = movie.get("release_date")

        if not release_date:
            continue

        release_year = int(release_date[:4])

        if movie_title.casefold() == title.casefold() and release_year == year:
            return movie    
        
    return None

def get_movie_details(movie_id: int) -> dict:
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    headers = {
        "Authorization": f"Bearer {token}" 
    }

    response = httpx.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data

def movie_from_tmdb(details: dict) -> Movie:
    release_date = details.get("release_date", "")

    if release_date:
        year = int(release_date[:4])
    else: 
        year = 0

    genres = [
        genre.get("name")
        for genre in details.get("genres", [])
    ]

    countries = [
        country.get("name")
        for country in details.get("production_countries", [])
    ]

    return Movie(
        title=details.get("title"),
        year=year,
        tmdb_id=details.get("id"),
        description=details.get("overview"),
        runtime=details.get("runtime"),
        rating=details.get("vote_average"),
        poster_path=details.get("poster_path"),
        genres=genres,
        countries=countries,
    )