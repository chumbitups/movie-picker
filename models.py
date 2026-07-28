from dataclasses import dataclass

@dataclass
class Movie:
    title: str
    year: int
    watched: bool = False
    recommendation_count: int = 0