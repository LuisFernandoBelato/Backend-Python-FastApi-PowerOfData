from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class PlanetDTO:
    name: str 
    rotation_period: Optional[str] = None
    orbital_period: Optional[str] = None
    diameter: Optional[str] = None
    climate: Optional[str] = None
    gravity: Optional[str] = None
    terrain: Optional[str] = None
    surface_water: Optional[str] = None
    population: Optional[str] = None
    url: Optional[str] = None
    created: Optional[str] = None
    edited: Optional[str] = None

    residents: Optional[List[str]] = field(default_factory=list)
    films: Optional[List[str]] = field(default_factory=list)
    
    # NÃO PRECISA DE to_dict, POIS COMO É UM DATACLASS, JÁ TEM ESSE MÉTODO IMPLÍCITO
        # planet_dict = asdict(seu_objeto_planet_dto)