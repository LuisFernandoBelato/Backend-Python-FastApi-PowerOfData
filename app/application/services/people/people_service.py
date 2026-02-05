"""Service to resolve people entities from the SWAPI."""

from __future__ import annotations

from typing import Optional

from app.application.services.base_service import BaseSwapiService
from app.domain.entities.people.people_entity import PeopleEntity
from app.interfaces.dtos.people.people_dto import PeopleDTO
from app.interfaces.query_params.people.people_query_params import PeopleQueryParams


class PeopleService(BaseSwapiService):
    """Entry point for fetching `PeopleEntity` objects from SWAPI."""

    ################### Funções Públicas ###################

    async def create_entities(
        self,
        url: str,
        query_params: PeopleQueryParams,
    ) -> list[PeopleEntity]:
        payloads = self._collect_payloads(url, query_params)
        if not payloads:
            return []

        entities: list[PeopleEntity] = []
        for payload in payloads:
            person = self._instance_payload(payload)
            entity = await self._hydrate_person_entity(person, query_params)
            entities.append(entity)

        if query_params.order:
            return self._order_entities(entities, query_params.order)
        return entities

    async def create_entity(
        self,
        url: str,
        query_params: PeopleQueryParams,
    ) -> PeopleEntity | None:
        people = await self.create_entities(url, query_params)
        return people[0] if people else None


    def resolve_url(self, url: str, search_params: dict[str, object] | None = None) -> PeopleDTO:
        payload = self._resolve_payload(url, params=search_params)
        results = payload.get("results")
        if isinstance(results, list):
            if not results:
                raise ValueError("Nenhuma pessoa corresponde ao filtro solicitado")
            return self._instance_payload(results[0])

        return self._instance_payload(payload)

    resolveUrl = resolve_url


    ################### Funções Internas ###################

    def _build_search_params(self, query_params: PeopleQueryParams) -> dict[str, str] | None:
        if query_params.name:
            return {"search": query_params.name}
        return None

    def _collect_payloads(self, url: str, query_params: PeopleQueryParams) -> list[dict[str, object]]:
        payload = self._resolve_payload(url, params=self._build_search_params(query_params))
        results = payload.get("results")
        if isinstance(results, list):
            return results
        return [payload]

    def _instance_payload(self, payload: dict[str, object]) -> PeopleDTO:
        return PeopleDTO(
            name=payload.get("name", ""),
            birth_year=payload.get("birth_year"),
            eye_color=payload.get("eye_color"),
            gender=payload.get("gender"),
            hair_color=payload.get("hair_color"),
            height=payload.get("height"),
            mass=payload.get("mass"),
            skin_color=payload.get("skin_color"),
            homeworld=payload.get("homeworld"),
            films=payload.get("films", []),
            species=payload.get("species", []),
            starships=payload.get("starships", []),
            vehicles=payload.get("vehicles", []),
            url=payload.get("url"),
            created=payload.get("created"),
            edited=payload.get("edited"),
        )

    def _order_entities(
        self,
        entities: list[PeopleEntity],
        order: Optional[str],
    ) -> list[PeopleEntity]:
        if not order or not isinstance(order, str):
            return entities

        normalized = order.strip().lower()
        if normalized not in {"asc", "desc"}:
            return entities

        return sorted(
            entities,
            key=lambda person: (person.name or "").lower(),
            reverse=normalized == "desc",
        )

    async def _hydrate_person_entity(
        self,
        person: PeopleDTO,
        query_params: PeopleQueryParams,
    ) -> PeopleEntity:
        # Imports locais para evitar ciclos entre services
        from app.application.services.planets.planets_service import PlanetsService
        from app.application.services.species.species_service import SpeciesService
        from app.application.services.starships.starships_service import StarshipsService
        from app.application.services.vehicles.vehicles_service import VehiclesService
        from app.application.services.films.films_service import FilmsService

        homeworld = None
        if person.homeworld:
            homeworld = await self._resolve_related_async(PlanetsService(), [person.homeworld])
            homeworld = homeworld[0] if homeworld else None

        films = person.films
        if query_params.films:
            films = await self._resolve_related_async(FilmsService(), person.films)

        species = person.species
        if query_params.species:
            species = await self._resolve_related_async(SpeciesService(), person.species)

        starships = person.starships
        if query_params.starships:
            starships = await self._resolve_related_async(StarshipsService(), person.starships)

        vehicles = person.vehicles
        if query_params.vehicles:
            vehicles = await self._resolve_related_async(VehiclesService(), person.vehicles)

        return PeopleEntity(
            name=person.name,
            birth_year=person.birth_year,
            eye_color=person.eye_color,
            gender=person.gender,
            hair_color=person.hair_color,
            height=person.height,
            mass=person.mass,
            skin_color=person.skin_color,
            homeworld=homeworld,
            films=films,
            species=species,
            starships=starships,
            vehicles=vehicles,
            url=person.url,
            created=person.created,
            edited=person.edited,
        )