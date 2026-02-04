"""Controller for species endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated

from app.application.services.species.species_service import SpeciesService
from app.interfaces.query_params.species.species_query_params import SpeciesQueryParams


class SpeciesController:
    """Exposes species read endpoints backed by the SWAPI."""

    SWAPI_BASE_URL: str = "https://swapi.dev/api/species/"

    def __init__(self) -> None:
        self._service = SpeciesService()

    def _validate_params(self, query_params: SpeciesQueryParams) -> SpeciesQueryParams:
        if query_params.all:
            query_params.people = True
            query_params.films = True

        if query_params.id:
            query_params.name = None

        if query_params.name:
            query_params.id = None

        return query_params

    def register_routes(self) -> APIRouter:
        router = APIRouter(prefix="/species", tags=["species"])

        @router.get("/")
        async def get_species(query_params: Annotated[SpeciesQueryParams, Depends()]) -> list[dict]:
            query_params = self._validate_params(query_params)

            swapi_url = f"{self.SWAPI_BASE_URL}"
            if query_params.id:
                swapi_url = f"{self.SWAPI_BASE_URL}{query_params.id}/"

            try:
                species_entities = await self._service.create_entities(swapi_url, query_params)
                return [specie.to_dict() for specie in species_entities]
            except Exception as exc:
                raise HTTPException(status_code=500, detail=str(exc)) from exc

        return router


controller = SpeciesController()
router = controller.register_routes()
