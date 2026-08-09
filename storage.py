import json
from dataclasses import asdict
from models import Movie    
from pathlib import Path

def save_movies(movies: list[Movie], path: str | None) -> None:
    file_path = Path(path)

    movies_dict = [
        asdict(movie)
        for movie in movies
    ]

    movies_json = json.dumps(
        movies_dict,
        ensure_ascii=False,
        indent=2
    )

    file_path.parent.mkdir(parents=True, exist_ok=True)

    file_path.write_text(
        movies_json,
        encoding="utf-8"
    )


def load_movies(path) -> list[Movie]:
    file_path = Path(path)

    if not file_path.exists():
        return []

    movies_json = file_path.read_text(
        encoding="utf-8"
    )

    movies_dict = json.loads(movies_json)

    return [
        Movie(**movie_dict)
        for movie_dict in movies_dict
    ]


