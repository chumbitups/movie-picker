import os
import httpx
from dotenv import load_dotenv

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