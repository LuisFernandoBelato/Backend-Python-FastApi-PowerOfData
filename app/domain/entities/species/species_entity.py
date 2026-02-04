from __future__ import annotations

from dataclasses import asdict
from typing import List, Optional

from app.interfaces.dtos.films.films_dto import FilmDTO
from app.interfaces.dtos.people.people_dto import PeopleDTO
from app.interfaces.dtos.planets.planets_dto import PlanetDTO

class SpeciesEntity:

    def __init__(
        self,
        name: str,
        classification: Optional[str] = None,
        designation: Optional[str] = None,
        average_height: Optional[str] = None,
        average_lifespan: Optional[str] = None,
        eye_colors: Optional[str] = None,
        hair_colors: Optional[str] = None,
        skin_colors: Optional[str] = None,
        language: Optional[str] = None,
        homeworld: Optional[PlanetDTO] = None,
        people: Optional[List[PeopleDTO]] = None,
        films: Optional[List[FilmDTO]] = None,
        url: Optional[str] = None,
        created: Optional[str] = None,
        edited: Optional[str] = None,
    ) -> None:
        self.name = name
        self.classification = classification
        self.designation = designation
        self.average_height = average_height
        self.average_lifespan = average_lifespan
        self.eye_colors = eye_colors
        self.hair_colors = hair_colors
        self.skin_colors = skin_colors
        self.language = language
        self.homeworld = homeworld
        self.people = list(people) if people is not None else []
        self.films = list(films) if films is not None else []
        self.url = url
        self.created = created
        self.edited = edited

    @classmethod
    def from_swapi(cls, data: dict[str, object]) -> SpeciesEntity:
        return cls(
            name=data.get("name", ""),
            classification=data.get("classification"),
            designation=data.get("designation"),
            average_height=data.get("average_height"),
            average_lifespan=data.get("average_lifespan"),
            eye_colors=data.get("eye_colors"),
            hair_colors=data.get("hair_colors"),
            skin_colors=data.get("skin_colors"),
            language=data.get("language"),
            homeworld=PlanetDTO.from_dict(data.get("homeworld")) if data.get("homeworld") else None,
            people=[asdict(PeopleDTO.from_dict(person)) for person in data.get("people", [])],
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
            "classification": self.classification,
            "designation": self.designation,
            "average_height": self.average_height,
            "average_lifespan": self.average_lifespan,
            "eye_colors": self.eye_colors,
            "hair_colors": self.hair_colors,
            "skin_colors": self.skin_colors,
            "language": self.language,
            "homeworld": _asdict_or_value(self.homeworld) if self.homeworld else None,
            "people": [_asdict_or_value(person) for person in self.people],
            "films": [_asdict_or_value(film) for film in self.films],
            "url": self.url,
            "created": self.created,
            "edited": self.edited,
        }