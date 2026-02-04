"""Service to resolve film entities from the SWAPI."""

from __future__ import annotations

from typing import Optional

from app.application.services.base_service import BaseSwapiService
from app.domain.entities.films.films_entity import FilmEntity
from app.interfaces.dtos.films.films_dto import FilmDTO
from app.interfaces.query_params.films.films_query_params import FilmsQueryParams

class FilmsService(BaseSwapiService):
    """Entry point for fetching `FilmEntity` objects from SWAPI."""

    # def __init__(self) -> None:
    #     self._planetsService = PlanetsService()
    #     self._speciesService = SpeciesService()
    #     self._starshipsService = StarshipsService()
    #     self._vehiclesService = VehiclesService()

    ################### Funções Públicas ###################

    async def create_entities(
        self,
        url: str,
        query_params: FilmsQueryParams,
    ) -> list[FilmEntity]:
        """Busca um ou mais filmes na SWAPI e resolve os relacionamentos solicitados."""

        payloads = self._collect_payloads(url, query_params)
        if not payloads:
            return []

        entities: list[FilmEntity] = []
        for payload in payloads:
            film = self._instance_payload(payload)
            entity = await self._hydrate_film_entity(film, query_params)
            entities.append(entity)

        if query_params.order:
            return self._order_entities(entities, query_params.order)
        return entities

    async def create_entity(
        self,
        url: str,
        query_params: FilmsQueryParams,
    ) -> FilmEntity | None:
        """Compatibilidade: retorna o primeiro filme (ou None) como antes."""

        films = await self.create_entities(url, query_params)
        return films[0] if films else None


    def resolve_url(self, url: str, search_params: dict[str, object] | None = None) -> FilmDTO:
        payload = self._resolve_payload(url, params=search_params)
        results = payload.get("results")
        if isinstance(results, list):
            if not results:
                raise ValueError("Nenhum filme corresponde ao filtro solicitado")
            return self._instance_payload(results[0])

        return self._instance_payload(payload)

    

    ################### Funções Internas ###################

    
    def _build_search_params(self, query_params: FilmsQueryParams) -> dict[str, str] | None:

        if query_params.title:
            return {"search": query_params.title}

        return None
    

    resolveUrl = resolve_url


    def _instance_payload(self, payload: dict[str, object]) -> FilmDTO:
        return FilmDTO(
            title=payload.get("title", ""),
            episode_id=payload.get("episode_id"),
            opening_crawl=payload.get("opening_crawl"),
            director=payload.get("director"),
            producer=payload.get("producer"),
            release_date=payload.get("release_date"),
            characters=payload.get("characters", []),
            planets=payload.get("planets", []),
            starships=payload.get("starships", []),
            vehicles=payload.get("vehicles", []),
            species=payload.get("species", []),
            url=payload.get("url"),
            created=payload.get("created"),
            edited=payload.get("edited"),
        )


    def _collect_payloads(self, url: str, query_params: FilmsQueryParams) -> list[dict[str, object]]:
        payload = self._resolve_payload(url, params=self._build_search_params(query_params))
        results = payload.get("results")
        if isinstance(results, list):
            return results
        return [payload]
    

    def _order_entities(
        self,
        entities: list[FilmEntity],
        order: Optional[str],
    ) -> list[FilmEntity]:
        if not order or not isinstance(order, str):
            return entities

        normalized = order.strip().lower()
        if normalized not in {"asc", "desc"}:
            return entities

        return sorted(
            entities,
            key=lambda film: (film.title or "").lower(),
            reverse=normalized == "desc",
        )


    async def _hydrate_film_entity(
        self,
        film: FilmDTO,
        query_params: FilmsQueryParams,
    ) -> FilmEntity:
        
        # Imports locais para evitar ciclos entre services
        from app.application.services.people.people_service import PeopleService
        from app.application.services.planets.planets_service import PlanetsService
        from app.application.services.species.species_service import SpeciesService
        from app.application.services.starships.starships_service import StarshipsService
        from app.application.services.vehicles.vehicles_service import VehiclesService

        planets = film.planets
        if query_params.planets:
            planets = await self._resolve_related_async(PlanetsService(), film.planets)

        starships = film.starships
        if query_params.starships:
            starships = await self._resolve_related_async(StarshipsService(), film.starships)

        vehicles = film.vehicles
        if query_params.vehicles:
            vehicles = await self._resolve_related_async(VehiclesService(), film.vehicles)

        species = film.species
        if query_params.species:
            species = await self._resolve_related_async(SpeciesService(), film.species)

        characters = film.characters
        if query_params.characters:
            characters = await self._resolve_related_async(PeopleService(), film.characters)

        return FilmEntity(
            title=film.title,
            episode_id=film.episode_id,
            opening_crawl=film.opening_crawl,
            director=film.director,
            producer=film.producer,
            release_date=film.release_date,
            characters=characters,
            planets=planets,
            starships=starships,
            vehicles=vehicles,
            species=species,
            url=film.url,
            created=film.created,
            edited=film.edited,
        )