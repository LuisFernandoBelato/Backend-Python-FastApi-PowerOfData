"""Controller for vehicle endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated

from app.application.services.vehicles.vehicles_service import VehiclesService
from app.interfaces.query_params.vehicles.vehicles_query_params import VehiclesQueryParams


class VehiclesController:
    """Exposes vehicle read endpoints backed by the SWAPI."""

    SWAPI_BASE_URL: str = "https://swapi.dev/api/vehicles/"

    def __init__(self) -> None:
        self._service = VehiclesService()

    def _validate_params(self, query_params: VehiclesQueryParams) -> VehiclesQueryParams:
        if query_params.all:
            query_params.films = True
            query_params.pilots = True

        if query_params.id:
            query_params.name = None
            query_params.model = None

        if query_params.name or query_params.model:
            query_params.id = None

        return query_params

    def register_routes(self) -> APIRouter:
        router = APIRouter(prefix="/vehicles", tags=["vehicles"])

        @router.get("/")
        async def get_vehicles(query_params: Annotated[VehiclesQueryParams, Depends()]) -> list[dict]:
            query_params = self._validate_params(query_params)

            swapi_url = f"{self.SWAPI_BASE_URL}"
            if query_params.id:
                swapi_url = f"{self.SWAPI_BASE_URL}{query_params.id}/"

            try:
                vehicle_entities = await self._service.create_entities(swapi_url, query_params)
                return [vehicle.to_dict() for vehicle in vehicle_entities]
            except Exception as exc:
                raise HTTPException(status_code=500, detail=str(exc)) from exc

        return router


controller = VehiclesController()
router = controller.register_routes()
