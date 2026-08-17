import os
import httpx
import time
from dotenv import load_dotenv
from models import Movie

load_dotenv()
token = os.getenv("TMDB_TOKEN")
if token is None:
    raise RuntimeError("TMDB_TOKEN is not set")

def _get(endpoint: str, params:dict | None = None) -> dict:
    headers = {
        "Authorization": f"Bearer {token}" 
    }

    for attempt in range(3):
        try:
            response = httpx.get(endpoint, params=params, headers=headers, timeout=10.0)
            response.raise_for_status()
            return response.json()

        except httpx.ReadError:
            if attempt == 2:
                raise

            time.sleep(1)


def search_movie(title: str, year: int | None = None)   :
    url = "https://api.themoviedb.org/3/search/movie"

    params = {
        "query": title,
    }

    if year is not None:
        params["primary_release_year"] = year
    
    return _get(url, params=params)["results"]

def find_movie_match(results: list, title: str, year: int | None = None):
    for movie in results:
        movie_title = movie.get("title")
        release_date = movie.get("release_date")

        if not release_date:
            continue

        release_year = int(release_date[:4])


        if (
            normalize_title(movie_title) == normalize_title(title) 
            and abs(release_year - year) <= 1
        ):
            return movie

    return None

def get_movie_details(movie_id: int) -> dict:
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    return _get(url)

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

def fetch_movie(title: str, year: int) -> Movie | None:
    results = search_movie(title, year)

    match = find_movie_match(results, title, year)

    if match is None:
        results = search_movie(title)
        match = find_movie_match(results=results, title=title, year=year)

    if match is None:
        return None 

    tmdb_id = match.get("id")

    details = get_movie_details(tmdb_id)

    return movie_from_tmdb(details=details)

def normalize_title(title: str) -> str:
    normalized = title.casefold()

    normalized = normalized.replace("–", "-")
    normalized = normalized.replace("—", "-")

    normalized = " ".join(normalized.split())

    return normalized

