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

@dataclass
class WatchlistItem:
    title: str
    year: int
    slug: str