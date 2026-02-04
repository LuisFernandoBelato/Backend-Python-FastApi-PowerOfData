"""Service to resolve vehicle entities from the SWAPI."""

from __future__ import annotations

from typing import Optional

from app.application.services.base_service import BaseSwapiService
from app.domain.entities.vehicles.vehicles_entity import VehicleEntity
from app.interfaces.dtos.vehicles.vehicles_dto import VehicleDTO
from app.interfaces.query_params.vehicles.vehicles_query_params import VehiclesQueryParams


class VehiclesService(BaseSwapiService):
    """Entry point for fetching `VehicleEntity` objects from SWAPI."""

    ################### Funções Públicas ###################

    async def create_entities(
        self,
        url: str,
        query_params: VehiclesQueryParams,
    ) -> list[VehicleEntity]:
        payloads = self._collect_payloads(url, query_params)
        if not payloads:
            return []

        entities: list[VehicleEntity] = []
        for payload in payloads:
            vehicle = self._instance_payload(payload)
            entity = await self._hydrate_vehicle_entity(vehicle, query_params)
            entities.append(entity)

        if query_params.order:
            return self._order_entities(entities, query_params.order)
        return entities

    async def create_entity(
        self,
        url: str,
        query_params: VehiclesQueryParams,
    ) -> VehicleEntity | None:
        vehicles = await self.create_entities(url, query_params)
        return vehicles[0] if vehicles else None

    def resolve_url(self, url: str, search_params: dict[str, object] | None = None) -> VehicleDTO:
        payload = self._resolve_payload(url, params=search_params)
        results = payload.get("results")
        if isinstance(results, list):
            if not results:
                raise ValueError("Nenhum veículo corresponde ao filtro solicitado")
            return self._instance_payload(results[0])

        return self._instance_payload(payload)

    resolveUrl = resolve_url

    ################### Funções Internas ###################

    def _build_search_params(self, query_params: VehiclesQueryParams) -> dict[str, str] | None:
        if query_params.name:
            return {"search": query_params.name}
        if query_params.model:
            return {"search": query_params.model}
        return None

    def _collect_payloads(self, url: str, query_params: VehiclesQueryParams) -> list[dict[str, object]]:
        payload = self._resolve_payload(url, params=self._build_search_params(query_params))
        results = payload.get("results")
        if isinstance(results, list):
            return results
        return [payload]

    def _instance_payload(self, payload: dict[str, object]) -> VehicleDTO:
        return VehicleDTO(
            name=payload.get("name", ""),
            model=payload.get("model"),
            vehicle_class=payload.get("vehicle_class"),
            manufacturer=payload.get("manufacturer"),
            length=payload.get("length"),
            cost_in_credits=payload.get("cost_in_credits"),
            crew=payload.get("crew"),
            passengers=payload.get("passengers"),
            max_atmosphering_speed=payload.get("max_atmosphering_speed"),
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
        entities: list[VehicleEntity],
        order: Optional[str],
    ) -> list[VehicleEntity]:
        if not order:
            return entities

        normalized = order.strip().lower()
        if normalized not in {"asc", "desc"}:
            return entities

        return sorted(
            entities,
            key=lambda vehicle: (vehicle.name or "").lower(),
            reverse=normalized == "desc",
        )

    async def _hydrate_vehicle_entity(
        self,
        vehicle: VehicleDTO,
        query_params: VehiclesQueryParams,
    ) -> VehicleEntity:
        # Imports locais para evitar ciclos entre services
        from app.application.services.people.people_service import PeopleService
        from app.application.services.films.films_service import FilmsService

        films = vehicle.films
        if query_params.films:
            films = await self._resolve_related_async(FilmsService(), vehicle.films)

        pilots = vehicle.pilots
        if query_params.pilots:
            pilots = await self._resolve_related_async(PeopleService(), vehicle.pilots)

        return VehicleEntity(
            name=vehicle.name,
            model=vehicle.model,
            vehicle_class=vehicle.vehicle_class,
            manufacturer=vehicle.manufacturer,
            length=vehicle.length,
            cost_in_credits=vehicle.cost_in_credits,
            crew=vehicle.crew,
            passengers=vehicle.passengers,
            max_atmosphering_speed=vehicle.max_atmosphering_speed,
            cargo_capacity=vehicle.cargo_capacity,
            consumables=vehicle.consumables,
            films=films,
            pilots=pilots,
            url=vehicle.url,
            created=vehicle.created,
            edited=vehicle.edited,
        )