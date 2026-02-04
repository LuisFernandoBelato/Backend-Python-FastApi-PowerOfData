"""Unit tests for Starships endpoints."""

import pytest
from unittest.mock import Mock
from app.application.services.starships.starships_service import StarshipsService
from app.interfaces.query_params.starships.starships_query_params import StarshipsQueryParams


class TestStarshipsEndpoints:
    """Test suite for Starships API endpoints."""

    @pytest.mark.asyncio
    async def test_get_all_starships_success(self, client, mock_requests_get, sample_starship_payload):
        """Test getting all starships successfully."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_starship_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/starships/")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_starship_by_id_success(self, client, mock_requests_get, sample_starship_payload):
        """Test getting a specific starship by ID."""
        mock_requests_get.return_value.json.return_value = sample_starship_payload
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/starships/?id=9")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_starship_by_name_search(self, client, mock_requests_get, sample_starship_payload):
        """Test searching starships by name."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_starship_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/starships/?name=Death")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_starship_by_model_search(self, client, mock_requests_get, sample_starship_payload):
        """Test searching starships by model."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_starship_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/starships/?model=DS-1")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_starship_with_all_relations(self, client, mock_requests_get, sample_starship_payload):
        """Test getting starship with all related entities."""
        mock_requests_get.return_value.json.return_value = sample_starship_payload
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/starships/?id=9&all=true")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_starship_with_films(self, client, mock_requests_get, sample_starship_payload):
        """Test getting starship with film details."""
        mock_requests_get.return_value.json.return_value = sample_starship_payload
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/starships/?id=9&films=true")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_starship_with_pilots(self, client, mock_requests_get, sample_starship_payload):
        """Test getting starship with pilot details."""
        mock_requests_get.return_value.json.return_value = sample_starship_payload
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/starships/?id=9&pilots=true")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_starships_with_order_asc(self, client, mock_requests_get, sample_starship_payload):
        """Test getting starships ordered ascending by name."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_starship_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/starships/?order=asc")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_starships_with_order_desc(self, client, mock_requests_get, sample_starship_payload):
        """Test getting starships ordered descending by name."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_starship_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/starships/?order=desc")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestStarshipsService:
    """Test suite for StarshipsService class."""

    @pytest.mark.asyncio
    async def test_create_entities_with_results(self, mock_requests_get, sample_starship_payload):
        """Test creating starship entities from SWAPI results."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_starship_payload, sample_starship_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        service = StarshipsService()
        query_params = StarshipsQueryParams()

        entities = await service.create_entities("https://swapi.dev/api/starships/", query_params)

        assert isinstance(entities, list)
        assert len(entities) == 2

    @pytest.mark.asyncio
    async def test_create_entities_single_result(self, mock_requests_get, sample_starship_payload):
        """Test creating a single starship entity."""
        mock_requests_get.return_value.json.return_value = sample_starship_payload
        mock_requests_get.return_value.raise_for_status = Mock()

        service = StarshipsService()
        query_params = StarshipsQueryParams()

        entities = await service.create_entities("https://swapi.dev/api/starships/9/", query_params)

        assert isinstance(entities, list)
        assert len(entities) == 1
        assert entities[0].name == "Death Star"

    @pytest.mark.asyncio
    async def test_create_entities_empty_results(self, mock_requests_get):
        """Test handling empty results."""
        mock_requests_get.return_value.json.return_value = {"results": []}
        mock_requests_get.return_value.raise_for_status = Mock()

        service = StarshipsService()
        query_params = StarshipsQueryParams()

        entities = await service.create_entities("https://swapi.dev/api/starships/", query_params)

        assert isinstance(entities, list)
        assert len(entities) == 0

    @pytest.mark.asyncio
    async def test_create_entity_returns_first(self, mock_requests_get, sample_starship_payload):
        """Test create_entity returns first starship from results."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_starship_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        service = StarshipsService()
        query_params = StarshipsQueryParams()

        entity = await service.create_entity("https://swapi.dev/api/starships/", query_params)

        assert entity is not None
        assert entity.name == "Death Star"

    @pytest.mark.asyncio
    async def test_create_entity_returns_none_when_empty(self, mock_requests_get):
        """Test create_entity returns None for empty results."""
        mock_requests_get.return_value.json.return_value = {"results": []}
        mock_requests_get.return_value.raise_for_status = Mock()

        service = StarshipsService()
        query_params = StarshipsQueryParams()

        entity = await service.create_entity("https://swapi.dev/api/starships/", query_params)

        assert entity is None

    def test_resolve_url_with_search_params(self, mock_requests_get, sample_starship_payload):
        """Test resolve_url with search parameters."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_starship_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        service = StarshipsService()
        result = service.resolve_url("https://swapi.dev/api/starships/", {"search": "Death"})

        assert result.name == "Death Star"

    def test_resolve_url_no_results_raises_error(self, mock_requests_get):
        """Test resolve_url raises error when no starships match."""
        mock_requests_get.return_value.json.return_value = {"results": []}
        mock_requests_get.return_value.raise_for_status = Mock()

        service = StarshipsService()

        with pytest.raises(ValueError, match="Nenhuma nave corresponde ao filtro solicitado"):
            service.resolve_url("https://swapi.dev/api/starships/", {"search": "Nonexistent"})

    def test_build_search_params_with_name(self):
        """Test building search params with name filter."""
        service = StarshipsService()
        query_params = StarshipsQueryParams(name="Death Star")

        params = service._build_search_params(query_params)

        assert params == {"search": "Death Star"}

    def test_build_search_params_with_model(self):
        """Test building search params with model filter."""
        service = StarshipsService()
        query_params = StarshipsQueryParams(model="DS-1")

        params = service._build_search_params(query_params)

        assert params == {"search": "DS-1"}

    def test_build_search_params_without_filters(self):
        """Test building search params without filters."""
        service = StarshipsService()
        query_params = StarshipsQueryParams()

        params = service._build_search_params(query_params)

        assert params is None

    def test_order_entities_ascending(self, sample_starship_payload):
        """Test ordering entities in ascending order."""
        from app.domain.entities.starships.starships_entity import StarshipEntity

        service = StarshipsService()
        entities = [
            StarshipEntity(name="C Starship", **{k: v for k, v in sample_starship_payload.items() if k != 'name'}),
            StarshipEntity(name="A Starship", **{k: v for k, v in sample_starship_payload.items() if k != 'name'}),
            StarshipEntity(name="B Starship", **{k: v for k, v in sample_starship_payload.items() if k != 'name'}),
        ]

        ordered = service._order_entities(entities, "asc")

        assert ordered[0].name == "A Starship"
        assert ordered[1].name == "B Starship"
        assert ordered[2].name == "C Starship"

    def test_order_entities_descending(self, sample_starship_payload):
        """Test ordering entities in descending order."""
        from app.domain.entities.starships.starships_entity import StarshipEntity

        service = StarshipsService()
        entities = [
            StarshipEntity(name="A Starship", **{k: v for k, v in sample_starship_payload.items() if k != 'name'}),
            StarshipEntity(name="C Starship", **{k: v for k, v in sample_starship_payload.items() if k != 'name'}),
            StarshipEntity(name="B Starship", **{k: v for k, v in sample_starship_payload.items() if k != 'name'}),
        ]

        ordered = service._order_entities(entities, "desc")

        assert ordered[0].name == "C Starship"
        assert ordered[1].name == "B Starship"
        assert ordered[2].name == "A Starship"

    def test_instance_payload(self, sample_starship_payload):
        """Test creating StarshipDTO from payload."""
        service = StarshipsService()
        dto = service._instance_payload(sample_starship_payload)

        assert dto.name == "Death Star"
        assert dto.model == "DS-1 Orbital Battle Station"
        assert dto.starship_class == "Deep Space Mobile Battlestation"
        assert dto.manufacturer == "Imperial Department of Military Research"
        assert len(dto.films) == 1
