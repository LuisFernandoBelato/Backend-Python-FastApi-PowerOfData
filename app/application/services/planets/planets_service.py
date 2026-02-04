"""Service to resolve planets entities from the SWAPI."""

from __future__ import annotations

from typing import Optional

from app.application.services.base_service import BaseSwapiService
from app.domain.entities.planets.planets_entity import PlanetEntity
from app.interfaces.dtos.planets.planets_dto import PlanetDTO
from app.interfaces.query_params.planets.planets_query_params import PlanetsQueryParams


class PlanetsService(BaseSwapiService):
    """Entry point for fetching `PlanetEntity` objects from SWAPI."""

    ################### Funções Públicas ###################

    async def create_entities(
        self,
        url: str,
        query_params: PlanetsQueryParams,
    ) -> list[PlanetEntity]:
        payloads = self._collect_payloads(url, query_params)
        if not payloads:
            return []

        entities: list[PlanetEntity] = []
        for payload in payloads:
            planet = self._instance_payload(payload)
            entity = await self._hydrate_planet_entity(planet, query_params)
            entities.append(entity)

        if query_params.order:
            return self._order_entities(entities, query_params.order)
        return entities

    async def create_entity(
        self,
        url: str,
        query_params: PlanetsQueryParams,
    ) -> PlanetEntity | None:
        planets = await self.create_entities(url, query_params)
        return planets[0] if planets else None

    def resolve_url(self, url: str, search_params: dict[str, object] | None = None) -> PlanetDTO:
        payload = self._resolve_payload(url, params=search_params)
        results = payload.get("results")
        if isinstance(results, list):
            if not results:
                raise ValueError("Nenhum planeta corresponde ao filtro solicitado")
            return self._instance_payload(results[0])

        return self._instance_payload(payload)

    resolveUrl = resolve_url

    ################### Funções Internas ###################

    def _build_search_params(self, query_params: PlanetsQueryParams) -> dict[str, str] | None:
        if query_params.name:
            return {"search": query_params.name}
        return None

    def _collect_payloads(self, url: str, query_params: PlanetsQueryParams) -> list[dict[str, object]]:
        payload = self._resolve_payload(url, params=self._build_search_params(query_params))
        results = payload.get("results")
        if isinstance(results, list):
            return results
        return [payload]

    def _instance_payload(self, payload: dict[str, object]) -> PlanetDTO:
        return PlanetDTO(
            name=payload.get("name", ""),
            rotation_period=payload.get("rotation_period"),
            orbital_period=payload.get("orbital_period"),
            diameter=payload.get("diameter"),
            climate=payload.get("climate"),
            gravity=payload.get("gravity"),
            terrain=payload.get("terrain"),
            surface_water=payload.get("surface_water"),
            population=payload.get("population"),
            residents=payload.get("residents", []),
            films=payload.get("films", []),
            url=payload.get("url"),
            created=payload.get("created"),
            edited=payload.get("edited"),
        )

    def _order_entities(
        self,
        entities: list[PlanetEntity],
        order: Optional[str],
    ) -> list[PlanetEntity]:
        if not order:
            return entities

        normalized = order.strip().lower()
        if normalized not in {"asc", "desc"}:
            return entities

        return sorted(
            entities,
            key=lambda planet: (planet.name or "").lower(),
            reverse=normalized == "desc",
        )

    async def _hydrate_planet_entity(
        self,
        planet: PlanetDTO,
        query_params: PlanetsQueryParams,
    ) -> PlanetEntity:
        # Imports locais para evitar ciclos entre services
        from app.application.services.people.people_service import PeopleService
        from app.application.services.films.films_service import FilmsService

        residents = planet.residents
        if query_params.residents:
            residents = await self._resolve_related_async(PeopleService(), planet.residents)

        films = planet.films
        if query_params.films:
            films = await self._resolve_related_async(FilmsService(), planet.films)

        return PlanetEntity(
            name=planet.name,
            rotation_period=planet.rotation_period,
            orbital_period=planet.orbital_period,
            diameter=planet.diameter,
            climate=planet.climate,
            gravity=planet.gravity,
            terrain=planet.terrain,
            surface_water=planet.surface_water,
            population=planet.population,
            residents=residents,
            films=films,
            url=planet.url,
            created=planet.created,
            edited=planet.edited,
        )