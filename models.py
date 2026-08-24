from dataclasses import dataclass, field

@dataclass
class Movie:
    title: str
    year: int
    watched: bool = False
    recommendation_count: int = 0
    tmdb_id: int | None = None
    description: str = ""
    runtime: int | None = None
    rating: float | None = None
    poster_path: str | None = None
    genres: list[str] = field(default_factory=list)
    countries: list[str] = field(default_factory=list)
    letterboxd_slug: str | None = None
    is_in_watchlist: bool = True

@dataclass
class WatchlistItem:
    title: str
    year: int
    slug: str

@dataclass
class MovieFilter:
    genre: str | None = None
    year_from: int | None = None
    year_to: int | None = None
    country: str | None = None
    max_runtime: int | None = None
    min_rating: float | None = None