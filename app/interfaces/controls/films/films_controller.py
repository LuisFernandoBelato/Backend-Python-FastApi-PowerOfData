"""Controller for film endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated

from app.application.services.films.films_service import FilmsService
from app.interfaces.query_params.films.films_query_params import FilmsQueryParams


class FilmsController:
	"""Exposes film read endpoints backed by the SWAPI."""

	SWAPI_BASE_URL: str = "https://swapi.dev/api/films/"

	def __init__(self) -> None:
		self._service = FilmsService()

	def _validate_params(self, query_params: FilmsQueryParams) -> FilmsQueryParams:
		if query_params.all:
			query_params.characters = True
			query_params.planets = True
			query_params.starships = True
			query_params.vehicles = True
			query_params.species = True

		if query_params.id:
			query_params.title = None
			
		if query_params.title:
			query_params.id = None

		return query_params

	def register_routes(self) -> APIRouter:
		router = APIRouter(prefix="/films", tags=["films"])

		@router.get("/")
		async def get_films(query_params: Annotated[FilmsQueryParams, Depends()]) -> list[dict]:
			query_params = self._validate_params(query_params)

			swapi_url = f"{self.SWAPI_BASE_URL}"

			if query_params.id:
				swapi_url = f"{self.SWAPI_BASE_URL}{query_params.id}/"
			try:
				film_entities = await self._service.create_entities(swapi_url, query_params)
				return [film_entity.to_dict() for film_entity in film_entities]
			except Exception as exc:
				raise HTTPException(status_code=500, detail=str(exc)) from exc

		return router


# Convenience for router inclusion
controller = FilmsController()
router = controller.register_routes()
