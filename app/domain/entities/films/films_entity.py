from __future__ import annotations

from typing import List, Optional
from dataclasses import asdict

from app.interfaces.dtos.planets.planets_dto import PlanetDTO
from app.interfaces.dtos.species.species_dto import SpeciesDTO
from app.interfaces.dtos.starships.starships_dto import StarshipDTO
from app.interfaces.dtos.vehicles.vehicles_dto import VehicleDTO
from app.interfaces.dtos.people.people_dto import PeopleDTO


class FilmEntity:

    def __init__(
        self,
        title: str,
        episode_id: Optional[int] = None,
        opening_crawl: Optional[str] = None,
        director: Optional[str] = None,
        producer: Optional[str] = None,
        release_date: Optional[str] = None,
        species: Optional[List[SpeciesDTO]] = None,
        starships: Optional[List[StarshipDTO]] = None,
        vehicles: Optional[List[VehicleDTO]] = None,
        characters: Optional[List[PeopleDTO]] = None,
        planets: Optional[List[PlanetDTO]] = None,
        url: Optional[str] = None,
        created: Optional[str] = None,
        edited: Optional[str] = None,
    ) -> None:
        self.title = title
        self.episode_id = episode_id
        self.opening_crawl = opening_crawl
        self.director = director
        self.producer = producer
        self.release_date = release_date
        self.species = list(species) if species is not None else []
        self.starships = list(starships) if starships is not None else []
        self.vehicles = list(vehicles) if vehicles is not None else []
        self.characters = list(characters) if characters is not None else []
        self.planets = list(planets) if planets is not None else []
        self.url = url
        self.created = created
        self.edited = edited

    @classmethod
    def from_swapi(cls, data: dict[str, object]) -> FilmEntity:
        return cls(
            title=data.get("title", ""),
            episode_id=data.get("episode_id"),
            opening_crawl=data.get("opening_crawl"),
            director=data.get("director"),
            producer=data.get("producer"),
            release_date=data.get("release_date"),
            species=list(data.get("species", [])),
            starships=list(data.get("starships", [])),
            vehicles=list(data.get("vehicles", [])),
            characters=list(data.get("characters", [])),
            planets=list(data.get("planets", [])),
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
            "title": self.title,
            "episode_id": self.episode_id,
            "opening_crawl": self.opening_crawl,
            "director": self.director,
            "producer": self.producer,
            "release_date": self.release_date,
            "species": [_asdict_or_value(species) for species in self.species],
            "starships": [_asdict_or_value(starship) for starship in self.starships],
            "vehicles": [_asdict_or_value(vehicle) for vehicle in self.vehicles],
            "characters": [_asdict_or_value(character) for character in self.characters],
            "planets": [_asdict_or_value(planet) for planet in self.planets],
            "url": self.url,
            "created": self.created,
            "edited": self.edited,
        }