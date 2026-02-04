from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class PeopleDTO:
    name: str
    birth_year: Optional[str] = None
    eye_color: Optional[str] = None
    gender: Optional[str] = None
    hair_color: Optional[str] = None
    height: Optional[str] = None
    mass: Optional[str] = None
    skin_color: Optional[str] = None
    homeworld: Optional[str] = None
    url: Optional[str] = None
    created: Optional[str] = None
    edited: Optional[str] = None

    films: Optional[List[str]] = field(default_factory=list)
    species: Optional[List[str]] = field(default_factory=list)
    starships: Optional[List[str]] = field(default_factory=list)
    vehicles: Optional[List[str]] = field(default_factory=list)

    # NÃO PRECISA DE to_dict, POIS COMO É UM DATACLASS, JÁ TEM ESSE MÉTODO IMPLÍCITO
        # people_dict = asdict(seu_objeto_people_dto)