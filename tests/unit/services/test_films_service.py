"""Unit tests for Films endpoints."""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from app.application.services.films.films_service import FilmsService
from app.interfaces.query_params.films.films_query_params import FilmsQueryParams


class TestFilmsEndpoints:
    """Test suite for Films API endpoints."""

    @pytest.mark.asyncio
    async def test_get_all_films_success(self, client, mock_requests_get, sample_film_payload):
        """Test getting all films successfully."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_film_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/films/")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 0

    @pytest.mark.asyncio
    async def test_get_film_by_id_success(self, client, mock_requests_get, sample_film_payload):
        """Test getting a specific film by ID."""
        mock_requests_get.return_value.json.return_value = sample_film_payload
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/films/?id=1")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_film_by_title_search(self, client, mock_requests_get, sample_film_payload):
        """Test searching films by title."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_film_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/films/?title=Hope")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_film_with_all_relations(self, client, mock_requests_get, sample_film_payload):
        """Test getting film with all related entities."""
        mock_requests_get.return_value.json.return_value = sample_film_payload
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/films/?id=1&all=true")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_film_with_characters(self, client, mock_requests_get, sample_film_payload):
        """Test getting film with character details."""
        mock_requests_get.return_value.json.return_value = sample_film_payload
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/films/?id=1&characters=true")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_film_with_planets(self, client, mock_requests_get, sample_film_payload):
        """Test getting film with planet details."""
        mock_requests_get.return_value.json.return_value = sample_film_payload
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/films/?id=1&planets=true")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_film_with_order_asc(self, client, mock_requests_get, sample_film_payload):
        """Test getting films ordered ascending by title."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_film_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/films/?order=asc")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_film_with_order_desc(self, client, mock_requests_get, sample_film_payload):
        """Test getting films ordered descending by title."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_film_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/films/?order=desc")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestFilmsService:
    """Test suite for FilmsService class."""

    @pytest.mark.asyncio
    async def test_create_entities_with_results(self, mock_requests_get, sample_film_payload):
        """Test creating film entities from SWAPI results."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_film_payload, sample_film_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        service = FilmsService()
        query_params = FilmsQueryParams()

        entities = await service.create_entities("https://swapi.dev/api/films/", query_params)

        assert isinstance(entities, list)
        assert len(entities) == 2

    @pytest.mark.asyncio
    async def test_create_entities_single_result(self, mock_requests_get, sample_film_payload):
        """Test creating a single film entity."""
        mock_requests_get.return_value.json.return_value = sample_film_payload
        mock_requests_get.return_value.raise_for_status = Mock()

        service = FilmsService()
        query_params = FilmsQueryParams()

        entities = await service.create_entities("https://swapi.dev/api/films/1/", query_params)

        assert isinstance(entities, list)
        assert len(entities) == 1
        assert entities[0].title == "A New Hope"

    @pytest.mark.asyncio
    async def test_create_entities_empty_results(self, mock_requests_get):
        """Test handling empty results."""
        mock_requests_get.return_value.json.return_value = {"results": []}
        mock_requests_get.return_value.raise_for_status = Mock()

        service = FilmsService()
        query_params = FilmsQueryParams()

        entities = await service.create_entities("https://swapi.dev/api/films/", query_params)

        assert isinstance(entities, list)
        assert len(entities) == 0

    @pytest.mark.asyncio
    async def test_create_entity_returns_first(self, mock_requests_get, sample_film_payload):
        """Test create_entity returns first film from results."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_film_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        service = FilmsService()
        query_params = FilmsQueryParams()

        entity = await service.create_entity("https://swapi.dev/api/films/", query_params)

        assert entity is not None
        assert entity.title == "A New Hope"

    @pytest.mark.asyncio
    async def test_create_entity_returns_none_when_empty(self, mock_requests_get):
        """Test create_entity returns None for empty results."""
        mock_requests_get.return_value.json.return_value = {"results": []}
        mock_requests_get.return_value.raise_for_status = Mock()

        service = FilmsService()
        query_params = FilmsQueryParams()

        entity = await service.create_entity("https://swapi.dev/api/films/", query_params)

        assert entity is None

    def test_resolve_url_with_search_params(self, mock_requests_get, sample_film_payload):
        """Test resolve_url with search parameters."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_film_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        service = FilmsService()
        result = service.resolve_url("https://swapi.dev/api/films/", {"search": "Hope"})

        assert result.title == "A New Hope"

    def test_resolve_url_no_results_raises_error(self, mock_requests_get):
        """Test resolve_url raises error when no films match."""
        mock_requests_get.return_value.json.return_value = {"results": []}
        mock_requests_get.return_value.raise_for_status = Mock()

        service = FilmsService()

        with pytest.raises(ValueError, match="Nenhum filme corresponde ao filtro solicitado"):
            service.resolve_url("https://swapi.dev/api/films/", {"search": "Nonexistent"})

    def test_build_search_params_with_title(self):
        """Test building search params with title filter."""
        service = FilmsService()
        query_params = FilmsQueryParams(title="Hope")

        params = service._build_search_params(query_params)

        assert params == {"search": "Hope"}

    def test_build_search_params_without_title(self):
        """Test building search params without title."""
        service = FilmsService()
        query_params = FilmsQueryParams()

        params = service._build_search_params(query_params)

        assert params is None

    def test_order_entities_ascending(self, sample_film_payload):
        """Test ordering entities in ascending order."""
        from app.domain.entities.films.films_entity import FilmEntity

        service = FilmsService()
        entities = [
            FilmEntity(title="C Film", **{k: v for k, v in sample_film_payload.items() if k != 'title'}),
            FilmEntity(title="A Film", **{k: v for k, v in sample_film_payload.items() if k != 'title'}),
            FilmEntity(title="B Film", **{k: v for k, v in sample_film_payload.items() if k != 'title'}),
        ]

        ordered = service._order_entities(entities, "asc")

        assert ordered[0].title == "A Film"
        assert ordered[1].title == "B Film"
        assert ordered[2].title == "C Film"

    def test_order_entities_descending(self, sample_film_payload):
        """Test ordering entities in descending order."""
        from app.domain.entities.films.films_entity import FilmEntity

        service = FilmsService()
        entities = [
            FilmEntity(title="A Film", **{k: v for k, v in sample_film_payload.items() if k != 'title'}),
            FilmEntity(title="C Film", **{k: v for k, v in sample_film_payload.items() if k != 'title'}),
            FilmEntity(title="B Film", **{k: v for k, v in sample_film_payload.items() if k != 'title'}),
        ]

        ordered = service._order_entities(entities, "desc")

        assert ordered[0].title == "C Film"
        assert ordered[1].title == "B Film"
        assert ordered[2].title == "A Film"

    def test_order_entities_invalid_order(self, sample_film_payload):
        """Test that invalid order parameter returns unordered list."""
        from app.domain.entities.films.films_entity import FilmEntity

        service = FilmsService()
        entities = [
            FilmEntity(title="B Film", **{k: v for k, v in sample_film_payload.items() if k != 'title'}),
        ]

        ordered = service._order_entities(entities, "invalid")

        assert ordered == entities

    def test_instance_payload(self, sample_film_payload):
        """Test creating FilmDTO from payload."""
        service = FilmsService()
        dto = service._instance_payload(sample_film_payload)

        assert dto.title == "A New Hope"
        assert dto.episode_id == 4
        assert dto.director == "George Lucas"
        assert len(dto.characters) == 2
