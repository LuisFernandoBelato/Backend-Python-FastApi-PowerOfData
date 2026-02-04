"""Controller for planet endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated

from app.application.services.planets.planets_service import PlanetsService
from app.interfaces.query_params.planets.planets_query_params import PlanetsQueryParams


class PlanetsController:
    """Exposes planet read endpoints backed by the SWAPI."""

    SWAPI_BASE_URL: str = "https://swapi.dev/api/planets/"

    def __init__(self) -> None:
        self._service = PlanetsService()

    def _validate_params(self, query_params: PlanetsQueryParams) -> PlanetsQueryParams:
        if query_params.all:
            query_params.residents = True
            query_params.films = True

        if query_params.id:
            query_params.name = None

        if query_params.name:
            query_params.id = None

        return query_params

    def register_routes(self) -> APIRouter:
        router = APIRouter(prefix="/planets", tags=["planets"])

        @router.get("/")
        async def get_planets(query_params: Annotated[PlanetsQueryParams, Depends()]) -> list[dict]:
            query_params = self._validate_params(query_params)

            swapi_url = f"{self.SWAPI_BASE_URL}"
            if query_params.id:
                swapi_url = f"{self.SWAPI_BASE_URL}{query_params.id}/"

            try:
                planet_entities = await self._service.create_entities(swapi_url, query_params)
                return [planet.to_dict() for planet in planet_entities]
            except Exception as exc:
                raise HTTPException(status_code=500, detail=str(exc)) from exc

        return router


controller = PlanetsController()
router = controller.register_routes()
