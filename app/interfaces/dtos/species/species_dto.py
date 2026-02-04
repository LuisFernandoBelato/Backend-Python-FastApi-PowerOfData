from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SpeciesDTO:
    name: str
    classification: Optional[str] = None
    designation: Optional[str] = None
    average_height: Optional[str] = None
    average_lifespan: Optional[str] = None
    eye_colors: Optional[str] = None
    hair_colors: Optional[str] = None
    skin_colors: Optional[str] = None
    language: Optional[str] = None
    homeworld: Optional[str] = None
    url: Optional[str] = None
    created: Optional[str] = None
    edited: Optional[str] = None

    people: Optional[List[str]] = field(default_factory=list)
    films: Optional[List[str]] = field(default_factory=list)

    # NÃO PRECISA DE to_dict, POIS COMO É UM DATACLASS, JÁ TEM ESSE MÉTODO IMPLÍCITO
        # species_dict = asdict(seu_objeto_species_dto)