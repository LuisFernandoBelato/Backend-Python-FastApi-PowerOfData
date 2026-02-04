from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class VehicleDTO:
    name: str
    model: Optional[str] = None
    vehicle_class: Optional[str] = None
    manufacturer: Optional[str] = None
    length: Optional[str] = None
    cost_in_credits: Optional[str] = None
    crew: Optional[str] = None
    passengers: Optional[str] = None
    max_atmosphering_speed: Optional[str] = None
    cargo_capacity: Optional[str] = None
    consumables: Optional[str] = None
    url: Optional[str] = None
    created: Optional[str] = None
    edited: Optional[str] = None

    films: Optional[List[str]] = field(default_factory=list)
    pilots: Optional[List[str]] = field(default_factory=list)

    # NÃO PRECISA DE to_dict, POIS COMO É UM DATACLASS, JÁ TEM ESSE MÉTODO IMPLÍCITO
        # vehicle_dict = asdict(seu_objeto_vehicle_dto)