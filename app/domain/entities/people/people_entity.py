from __future__ import annotations

from dataclasses import asdict
from typing import List, Optional

from app.interfaces.dtos.planets.planets_dto import PlanetDTO
from app.interfaces.dtos.species.species_dto import SpeciesDTO
from app.interfaces.dtos.starships.starships_dto import StarshipDTO
from app.interfaces.dtos.vehicles.vehicles_dto import VehicleDTO
from app.interfaces.dtos.films.films_dto import FilmDTO

class PeopleEntity:

    def __init__(
        self,
        name: str,
        birth_year: Optional[str] = None,
        eye_color: Optional[str] = None,
        gender: Optional[str] = None,
        hair_color: Optional[str] = None,
        height: Optional[str] = None,
        mass: Optional[str] = None,
        skin_color: Optional[str] = None,
        homeworld: Optional[PlanetDTO] = None,
        films: Optional[List[FilmDTO]] = None,
        species: Optional[List[SpeciesDTO]] = None,
        starships: Optional[List[StarshipDTO]] = None,
        vehicles: Optional[List[VehicleDTO]] = None,
        url: Optional[str] = None,
        created: Optional[str] = None,
        edited: Optional[str] = None,
    ) -> None:
        self.name = name
        self.birth_year = birth_year
        self.eye_color = eye_color
        self.gender = gender
        self.hair_color = hair_color
        self.height = height
        self.mass = mass
        self.skin_color = skin_color
        self.homeworld = homeworld
        self.films = list(films) if films is not None else []
        self.species = list(species) if species is not None else []
        self.starships = list(starships) if starships is not None else []
        self.vehicles = list(vehicles) if vehicles is not None else []
        self.url = url
        self.created = created
        self.edited = edited

    @classmethod
    def from_swapi(cls, data: dict[str, object]) -> PeopleEntity:
        return cls(
            name=data.get("name", ""),
            birth_year=data.get("birth_year"),
            eye_color=data.get("eye_color"),
            gender=data.get("gender"),
            hair_color=data.get("hair_color"),
            height=data.get("height"),
            mass=data.get("mass"),
            skin_color=data.get("skin_color"),
            homeworld=PlanetDTO.from_dict(data.get("homeworld")) if data.get("homeworld") else None,
            films=[asdict(FilmDTO.from_dict(film)) for film in data.get("films", [])],
            species=[asdict(SpeciesDTO.from_dict(species)) for species in data.get("species", [])],
            starships=[asdict(StarshipDTO.from_dict(starship)) for starship in data.get("starships", [])],
            vehicles=[asdict(VehicleDTO.from_dict(vehicle)) for vehicle in data.get("vehicles", [])],
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
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "height": self.height,
            "mass": self.mass,
            "skin_color": self.skin_color,
            "homeworld": _asdict_or_value(self.homeworld) if self.homeworld else None,
            "films": [_asdict_or_value(film) for film in self.films],
            "species": [_asdict_or_value(species) for species in self.species],
            "starships": [_asdict_or_value(starship) for starship in self.starships],
            "vehicles": [_asdict_or_value(vehicle) for vehicle in self.vehicles],
            "url": self.url,
            "created": self.created,
            "edited": self.edited,
        }