"""Controller for people endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated

from app.application.services.people.people_service import PeopleService
from app.interfaces.query_params.people.people_query_params import PeopleQueryParams


class PeopleController:
    """Exposes people read endpoints backed by the SWAPI."""

    SWAPI_BASE_URL: str = "https://swapi.dev/api/people/"

    def __init__(self) -> None:
        self._service = PeopleService()

    def _validate_params(self, query_params: PeopleQueryParams) -> PeopleQueryParams:
        if query_params.all:
            query_params.films = True
            query_params.species = True
            query_params.starships = True
            query_params.vehicles = True

        if query_params.id:
            query_params.name = None

        if query_params.name:
            query_params.id = None

        return query_params

    def register_routes(self) -> APIRouter:
        router = APIRouter(prefix="/people", tags=["people"])

        @router.get("/")
        async def get_people(query_params: Annotated[PeopleQueryParams, Depends()]) -> list[dict]:
            query_params = self._validate_params(query_params)

            swapi_url = f"{self.SWAPI_BASE_URL}"
            if query_params.id:
                swapi_url = f"{self.SWAPI_BASE_URL}{query_params.id}/"

            try:
                people_entities = await self._service.create_entities(swapi_url, query_params)
                return [person.to_dict() for person in people_entities]
            except Exception as exc:
                raise HTTPException(status_code=500, detail=str(exc)) from exc

        return router


controller = PeopleController()
router = controller.register_routes()
