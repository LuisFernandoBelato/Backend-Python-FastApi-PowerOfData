"""Service to resolve species entities from the SWAPI."""

from __future__ import annotations

from typing import Optional

from app.application.services.base_service import BaseSwapiService
from app.domain.entities.species.species_entity import SpeciesEntity
from app.interfaces.dtos.species.species_dto import SpeciesDTO
from app.interfaces.query_params.species.species_query_params import SpeciesQueryParams


class SpeciesService(BaseSwapiService):
    """Entry point for fetching `SpeciesEntity` objects from SWAPI."""

    ################### Funções Públicas ###################

    async def create_entities(
        self,
        url: str,
        query_params: SpeciesQueryParams,
    ) -> list[SpeciesEntity]:
        payloads = self._collect_payloads(url, query_params)
        if not payloads:
            return []

        entities: list[SpeciesEntity] = []
        for payload in payloads:
            specie = self._instance_payload(payload)
            entity = await self._hydrate_species_entity(specie, query_params)
            entities.append(entity)

        if query_params.order:
            return self._order_entities(entities, query_params.order)
        return entities

    async def create_entity(
        self,
        url: str,
        query_params: SpeciesQueryParams,
    ) -> SpeciesEntity | None:
        species = await self.create_entities(url, query_params)
        return species[0] if species else None

    def resolve_url(self, url: str, search_params: dict[str, object] | None = None) -> SpeciesDTO:
        payload = self._resolve_payload(url, params=search_params)
        results = payload.get("results")
        if isinstance(results, list):
            if not results:
                raise ValueError("Nenhuma espécie corresponde ao filtro solicitado")
            return self._instance_payload(results[0])

        return self._instance_payload(payload)

    resolveUrl = resolve_url

    ################### Funções Internas ###################

    def _build_search_params(self, query_params: SpeciesQueryParams) -> dict[str, str] | None:
        if query_params.name:
            return {"search": query_params.name}
        return None

    def _collect_payloads(self, url: str, query_params: SpeciesQueryParams) -> list[dict[str, object]]:
        payload = self._resolve_payload(url, params=self._build_search_params(query_params))
        results = payload.get("results")
        if isinstance(results, list):
            return results
        return [payload]

    def _instance_payload(self, payload: dict[str, object]) -> SpeciesDTO:
        return SpeciesDTO(
            name=payload.get("name", ""),
            classification=payload.get("classification"),
            designation=payload.get("designation"),
            average_height=payload.get("average_height"),
            average_lifespan=payload.get("average_lifespan"),
            eye_colors=payload.get("eye_colors"),
            hair_colors=payload.get("hair_colors"),
            skin_colors=payload.get("skin_colors"),
            language=payload.get("language"),
            homeworld=payload.get("homeworld"),
            people=payload.get("people", []),
            films=payload.get("films", []),
            url=payload.get("url"),
            created=payload.get("created"),
            edited=payload.get("edited"),
        )

    def _order_entities(
        self,
        entities: list[SpeciesEntity],
        order: Optional[str],
    ) -> list[SpeciesEntity]:
        if not order:
            return entities

        normalized = order.strip().lower()
        if normalized not in {"asc", "desc"}:
            return entities

        return sorted(
            entities,
            key=lambda specie: (specie.name or "").lower(),
            reverse=normalized == "desc",
        )

    async def _hydrate_species_entity(
        self,
        specie: SpeciesDTO,
        query_params: SpeciesQueryParams,
    ) -> SpeciesEntity:
        # Imports locais para evitar ciclos entre services
        from app.application.services.planets.planets_service import PlanetsService
        from app.application.services.people.people_service import PeopleService
        from app.application.services.films.films_service import FilmsService

        homeworld = None
        if specie.homeworld:
            homeworld = await self._resolve_related_async(PlanetsService(), [specie.homeworld])
            homeworld = homeworld[0] if homeworld else None

        people = specie.people
        if query_params.people:
            people = await self._resolve_related_async(PeopleService(), specie.people)

        films = specie.films
        if query_params.films:
            films = await self._resolve_related_async(FilmsService(), specie.films)

        return SpeciesEntity(
            name=specie.name,
            classification=specie.classification,
            designation=specie.designation,
            average_height=specie.average_height,
            average_lifespan=specie.average_lifespan,
            eye_colors=specie.eye_colors,
            hair_colors=specie.hair_colors,
            skin_colors=specie.skin_colors,
            language=specie.language,
            homeworld=homeworld,
            people=people,
            films=films,
            url=specie.url,
            created=specie.created,
            edited=specie.edited,
        )