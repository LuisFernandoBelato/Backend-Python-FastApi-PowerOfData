from __future__ import annotations

from dataclasses import asdict
from typing import List, Optional

from app.interfaces.dtos.films.films_dto import FilmDTO
from app.interfaces.dtos.people.people_dto import PeopleDTO

class VehicleEntity:

    def __init__(
        self,
        name: str,
        model: Optional[str] = None,
        vehicle_class: Optional[str] = None,
        manufacturer: Optional[str] = None,
        length: Optional[str] = None,
        cost_in_credits: Optional[str] = None,
        crew: Optional[str] = None,
        passengers: Optional[str] = None,
        max_atmosphering_speed: Optional[str] = None,
        cargo_capacity: Optional[str] = None,
        consumables: Optional[str] = None,
        films: Optional[List[FilmDTO]] = None,
        pilots: Optional[List[PeopleDTO]] = None,
        url: Optional[str] = None,
        created: Optional[str] = None,
        edited: Optional[str] = None,
    ) -> None:
        self.name = name
        self.model = model
        self.vehicle_class = vehicle_class
        self.manufacturer = manufacturer
        self.length = length
        self.cost_in_credits = cost_in_credits
        self.crew = crew
        self.passengers = passengers
        self.max_atmosphering_speed = max_atmosphering_speed
        self.cargo_capacity = cargo_capacity
        self.consumables = consumables
        self.films = list(films) if films is not None else []
        self.pilots = list(pilots) if pilots is not None else []
        self.url = url
        self.created = created
        self.edited = edited

    @classmethod
    def from_swapi(cls, data: dict[str, object]) -> VehicleEntity:
        return cls(
            name=data.get("name", ""),
            model=data.get("model"),
            vehicle_class=data.get("vehicle_class"),
            manufacturer=data.get("manufacturer"),
            length=data.get("length"),
            cost_in_credits=data.get("cost_in_credits"),
            crew=data.get("crew"),
            passengers=data.get("passengers"),
            max_atmosphering_speed=data.get("max_atmosphering_speed"),
            cargo_capacity=data.get("cargo_capacity"),
            consumables=data.get("consumables"),
            films=[asdict(FilmDTO.from_dict(film)) for film in data.get("films", [])],
            pilots=[asdict(PeopleDTO.from_dict(pilot)) for pilot in data.get("pilots", [])],
            url=data.get("url"),
            created=data.get("created"),
            edited=data.get("edited"),
        )

    def to_dict(self) -> dict[str, object]:
        def _asdict_or_value(value: object) -> object:
            try:
                return asdict(value)
            except Exception:
                return value

        return {
            "name": self.name,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer,
            "length": self.length,
            "cost_in_credits": self.cost_in_credits,
            "crew": self.crew,
            "passengers": self.passengers,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "films": [_asdict_or_value(film) for film in self.films],
            "pilots": [_asdict_or_value(pilot) for pilot in self.pilots],
            "url": self.url,
            "created": self.created,
            "edited": self.edited,
        }