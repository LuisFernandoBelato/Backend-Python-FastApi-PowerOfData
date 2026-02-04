from __future__ import annotations

from dataclasses import asdict
from typing import List, Optional

from app.interfaces.dtos.people.people_dto import PeopleDTO
from app.interfaces.dtos.films.films_dto import FilmDTO


class PlanetEntity:
    
    def __init__(
        self,
        name: str,
        rotation_period: Optional[str] = None,
        orbital_period: Optional[str] = None,
        diameter: Optional[str] = None,
        climate: Optional[str] = None,
        gravity: Optional[str] = None,
        terrain: Optional[str] = None,
        surface_water: Optional[str] = None,
        population: Optional[str] = None,
        residents: Optional[List[PeopleDTO]] = None,
        films: Optional[List[FilmDTO]] = None,
        url: Optional[str] = None,
        created: Optional[str] = None,
        edited: Optional[str] = None,
    ) -> None:
        self.name = name
        self.rotation_period = rotation_period
        self.orbital_period = orbital_period
        self.diameter = diameter
        self.climate = climate
        self.gravity = gravity
        self.terrain = terrain
        self.surface_water = surface_water
        self.population = population
        self.residents = list(residents) if residents is not None else []
        self.films = list(films) if films is not None else []
        self.url = url
        self.created = created
        self.edited = edited

    @classmethod
    def from_swapi(cls, data: dict[str, object]) -> PlanetEntity:
        return cls(
            name=data.get("name", ""),
            rotation_period=data.get("rotation_period"),
            orbital_period=data.get("orbital_period"),
            diameter=data.get("diameter"),
            climate=data.get("climate"),
            gravity=data.get("gravity"),
            terrain=data.get("terrain"),
            surface_water=data.get("surface_water"),
            population=data.get("population"),
            residents=[asdict(PeopleDTO.from_dict(resident)) for resident in data.get("residents", [])],
            films=[asdict(FilmDTO.from_dict(film)) for film in data.get("films", [])],
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
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "climate": self.climate,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "population": self.population,
            "residents": [_asdict_or_value(resident) for resident in self.residents],
            "films": [_asdict_or_value(film) for film in self.films],
            "url": self.url,
            "created": self.created,
            "edited": self.edited,
        }