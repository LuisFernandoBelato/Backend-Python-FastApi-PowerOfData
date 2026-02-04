"""Controller for starship endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated

from app.application.services.starships.starships_service import StarshipsService
from app.interfaces.query_params.starships.starships_query_params import StarshipsQueryParams


class StarshipsController:
    """Exposes starship read endpoints backed by the SWAPI."""

    SWAPI_BASE_URL: str = "https://swapi.dev/api/starships/"

    def __init__(self) -> None:
        self._service = StarshipsService()

    def _validate_params(self, query_params: StarshipsQueryParams) -> StarshipsQueryParams:
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
        router = APIRouter(prefix="/starships", tags=["starships"])

        @router.get("/")
        async def get_starships(query_params: Annotated[StarshipsQueryParams, Depends()]) -> list[dict]:
            query_params = self._validate_params(query_params)

            swapi_url = f"{self.SWAPI_BASE_URL}"
            if query_params.id:
                swapi_url = f"{self.SWAPI_BASE_URL}{query_params.id}/"

            try:
                starship_entities = await self._service.create_entities(swapi_url, query_params)
                return [starship.to_dict() for starship in starship_entities]
            except Exception as exc:
                raise HTTPException(status_code=500, detail=str(exc)) from exc

        return router


controller = StarshipsController()
router = controller.register_routes()
