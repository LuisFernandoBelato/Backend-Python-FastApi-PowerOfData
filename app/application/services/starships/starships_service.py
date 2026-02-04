"""Service to resolve starships entities from the SWAPI."""

from __future__ import annotations

from typing import Optional

from app.application.services.base_service import BaseSwapiService
from app.domain.entities.starships.starships_entity import StarshipEntity
from app.interfaces.dtos.starships.starships_dto import StarshipDTO
from app.interfaces.query_params.starships.starships_query_params import StarshipsQueryParams


class StarshipsService(BaseSwapiService):
    """Entry point for fetching `StarshipEntity` objects from SWAPI."""

    ################### Funções Públicas ###################

    async def create_entities(
        self,
        url: str,
        query_params: StarshipsQueryParams,
    ) -> list[StarshipEntity]:
        payloads = self._collect_payloads(url, query_params)
        if not payloads:
            return []

        entities: list[StarshipEntity] = []
        for payload in payloads:
            starship = self._instance_payload(payload)
            entity = await self._hydrate_starship_entity(starship, query_params)
            entities.append(entity)

        if query_params.order:
            return self._order_entities(entities, query_params.order)
        return entities

    async def create_entity(
        self,
        url: str,
        query_params: StarshipsQueryParams,
    ) -> StarshipEntity | None:
        starships = await self.create_entities(url, query_params)
        return starships[0] if starships else None

    def resolve_url(self, url: str, search_params: dict[str, object] | None = None) -> StarshipDTO:
        payload = self._resolve_payload(url, params=search_params)
        results = payload.get("results")
        if isinstance(results, list):
            if not results:
                raise ValueError("Nenhuma nave corresponde ao filtro solicitado")
            return self._instance_payload(results[0])

        return self._instance_payload(payload)

    resolveUrl = resolve_url

    ################### Funções Internas ###################

    def _build_search_params(self, query_params: StarshipsQueryParams) -> dict[str, str] | None:
        if query_params.name:
            return {"search": query_params.name}
        if query_params.model:
            return {"search": query_params.model}
        return None

    def _collect_payloads(self, url: str, query_params: StarshipsQueryParams) -> list[dict[str, object]]:
        payload = self._resolve_payload(url, params=self._build_search_params(query_params))
        results = payload.get("results")
        if isinstance(results, list):
            return results
        return [payload]

    def _instance_payload(self, payload: dict[str, object]) -> StarshipDTO:
        return StarshipDTO(
            name=payload.get("name", ""),
            model=payload.get("model"),
            starship_class=payload.get("starship_class"),
            manufacturer=payload.get("manufacturer"),
            cost_in_credits=payload.get("cost_in_credits"),
            length=payload.get("length"),
            crew=payload.get("crew"),
            passengers=payload.get("passengers"),
            max_atmosphering_speed=payload.get("max_atmosphering_speed"),
            hyperdrive_rating=payload.get("hyperdrive_rating"),
            MGLT=payload.get("MGLT"),
            cargo_capacity=payload.get("cargo_capacity"),
            consumables=payload.get("consumables"),
            films=payload.get("films", []),
            pilots=payload.get("pilots", []),
            url=payload.get("url"),
            created=payload.get("created"),
            edited=payload.get("edited"),
        )

    def _order_entities(
        self,
        entities: list[StarshipEntity],
        order: Optional[str],
    ) -> list[StarshipEntity]:
        if not order:
            return entities

        normalized = order.strip().lower()
        if normalized not in {"asc", "desc"}:
            return entities

        return sorted(
            entities,
            key=lambda starship: (starship.name or "").lower(),
            reverse=normalized == "desc",
        )

    async def _hydrate_starship_entity(
        self,
        starship: StarshipDTO,
        query_params: StarshipsQueryParams,
    ) -> StarshipEntity:
        # Imports locais para evitar ciclos entre services
        from app.application.services.people.people_service import PeopleService
        from app.application.services.films.films_service import FilmsService

        films = starship.films
        if query_params.films:
            films = await self._resolve_related_async(FilmsService(), starship.films)

        pilots = starship.pilots
        if query_params.pilots:
            pilots = await self._resolve_related_async(PeopleService(), starship.pilots)

        return StarshipEntity(
            name=starship.name,
            model=starship.model,
            starship_class=starship.starship_class,
            manufacturer=starship.manufacturer,
            cost_in_credits=starship.cost_in_credits,
            length=starship.length,
            crew=starship.crew,
            passengers=starship.passengers,
            max_atmosphering_speed=starship.max_atmosphering_speed,
            hyperdrive_rating=starship.hyperdrive_rating,
            MGLT=starship.MGLT,
            cargo_capacity=starship.cargo_capacity,
            consumables=starship.consumables,
            films=films,
            pilots=pilots,
            url=starship.url,
            created=starship.created,
            edited=starship.edited,
        )