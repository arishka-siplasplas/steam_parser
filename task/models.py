from dataclasses import dataclass
from typing import List

@dataclass
class Game:
    title: str
    price: str
    rating: str
    developer: str
    genres: List[str]
    release_date: str
