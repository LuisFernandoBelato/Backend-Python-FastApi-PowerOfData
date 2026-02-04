from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class FilmDTO:
    title: str
    episode_id: Optional[int] = None
    opening_crawl: Optional[str] = None
    director: Optional[str] = None
    producer: Optional[str] = None
    release_date: Optional[str] = None
    url: Optional[str] = None
    created: Optional[str] = None
    edited: Optional[str] = None

    species: Optional[List[str]] = field(default_factory=list)
    starships: Optional[List[str]] = field(default_factory=list)
    vehicles: Optional[List[str]] = field(default_factory=list)
    characters: Optional[List[str]] = field(default_factory=list)
    planets: Optional[List[str]] = field(default_factory=list)
    
    # NÃO PRECISA DE to_dict, POIS COMO É UM DATACLASS, JÁ TEM ESSE MÉTODO IMPLÍCITO
        # film_dict = asdict(seu_objeto_film_dto)
