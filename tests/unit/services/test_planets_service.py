"""Unit tests for Planets endpoints."""

import pytest
from unittest.mock import Mock
from app.application.services.planets.planets_service import PlanetsService
from app.interfaces.query_params.planets.planets_query_params import PlanetsQueryParams


class TestPlanetsEndpoints:
    """Test suite for Planets API endpoints."""

    @pytest.mark.asyncio
    async def test_get_all_planets_success(self, client, mock_requests_get, sample_planet_payload):
        """Test getting all planets successfully."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_planet_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/planets/")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_planet_by_id_success(self, client, mock_requests_get, sample_planet_payload):
        """Test getting a specific planet by ID."""
        mock_requests_get.return_value.json.return_value = sample_planet_payload
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/planets/?id=1")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_planet_by_name_search(self, client, mock_requests_get, sample_planet_payload):
        """Test searching planets by name."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_planet_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/planets/?name=Tatooine")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_planet_with_all_relations(self, client, mock_requests_get, sample_planet_payload):
        """Test getting planet with all related entities."""
        mock_requests_get.return_value.json.return_value = sample_planet_payload
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/planets/?id=1&all=true")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_planet_with_residents(self, client, mock_requests_get, sample_planet_payload):
        """Test getting planet with resident details."""
        mock_requests_get.return_value.json.return_value = sample_planet_payload
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/planets/?id=1&residents=true")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_planet_with_films(self, client, mock_requests_get, sample_planet_payload):
        """Test getting planet with film details."""
        mock_requests_get.return_value.json.return_value = sample_planet_payload
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/planets/?id=1&films=true")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_planets_with_order_asc(self, client, mock_requests_get, sample_planet_payload):
        """Test getting planets ordered ascending by name."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_planet_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/planets/?order=asc")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_planets_with_order_desc(self, client, mock_requests_get, sample_planet_payload):
        """Test getting planets ordered descending by name."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_planet_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/planets/?order=desc")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestPlanetsService:
    """Test suite for PlanetsService class."""

    @pytest.mark.asyncio
    async def test_create_entities_with_results(self, mock_requests_get, sample_planet_payload):
        """Test creating planet entities from SWAPI results."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_planet_payload, sample_planet_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        service = PlanetsService()
        query_params = PlanetsQueryParams()

        entities = await service.create_entities("https://swapi.dev/api/planets/", query_params)

        assert isinstance(entities, list)
        assert len(entities) == 2

    @pytest.mark.asyncio
    async def test_create_entities_single_result(self, mock_requests_get, sample_planet_payload):
        """Test creating a single planet entity."""
        mock_requests_get.return_value.json.return_value = sample_planet_payload
        mock_requests_get.return_value.raise_for_status = Mock()

        service = PlanetsService()
        query_params = PlanetsQueryParams()

        entities = await service.create_entities("https://swapi.dev/api/planets/1/", query_params)

        assert isinstance(entities, list)
        assert len(entities) == 1
        assert entities[0].name == "Tatooine"

    @pytest.mark.asyncio
    async def test_create_entities_empty_results(self, mock_requests_get):
        """Test handling empty results."""
        mock_requests_get.return_value.json.return_value = {"results": []}
        mock_requests_get.return_value.raise_for_status = Mock()

        service = PlanetsService()
        query_params = PlanetsQueryParams()

        entities = await service.create_entities("https://swapi.dev/api/planets/", query_params)

        assert isinstance(entities, list)
        assert len(entities) == 0

    @pytest.mark.asyncio
    async def test_create_entity_returns_first(self, mock_requests_get, sample_planet_payload):
        """Test create_entity returns first planet from results."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_planet_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        service = PlanetsService()
        query_params = PlanetsQueryParams()

        entity = await service.create_entity("https://swapi.dev/api/planets/", query_params)

        assert entity is not None
        assert entity.name == "Tatooine"

    @pytest.mark.asyncio
    async def test_create_entity_returns_none_when_empty(self, mock_requests_get):
        """Test create_entity returns None for empty results."""
        mock_requests_get.return_value.json.return_value = {"results": []}
        mock_requests_get.return_value.raise_for_status = Mock()

        service = PlanetsService()
        query_params = PlanetsQueryParams()

        entity = await service.create_entity("https://swapi.dev/api/planets/", query_params)

        assert entity is None

    def test_resolve_url_with_search_params(self, mock_requests_get, sample_planet_payload):
        """Test resolve_url with search parameters."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_planet_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        service = PlanetsService()
        result = service.resolve_url("https://swapi.dev/api/planets/", {"search": "Tatooine"})

        assert result.name == "Tatooine"

    def test_resolve_url_no_results_raises_error(self, mock_requests_get):
        """Test resolve_url raises error when no planets match."""
        mock_requests_get.return_value.json.return_value = {"results": []}
        mock_requests_get.return_value.raise_for_status = Mock()

        service = PlanetsService()

        with pytest.raises(ValueError, match="Nenhum planeta corresponde ao filtro solicitado"):
            service.resolve_url("https://swapi.dev/api/planets/", {"search": "Nonexistent"})

    def test_build_search_params_with_name(self):
        """Test building search params with name filter."""
        service = PlanetsService()
        query_params = PlanetsQueryParams(name="Tatooine")

        params = service._build_search_params(query_params)

        assert params == {"search": "Tatooine"}

    def test_build_search_params_without_name(self):
        """Test building search params without name."""
        service = PlanetsService()
        query_params = PlanetsQueryParams()

        params = service._build_search_params(query_params)

        assert params is None

    def test_order_entities_ascending(self, sample_planet_payload):
        """Test ordering entities in ascending order."""
        from app.domain.entities.planets.planets_entity import PlanetEntity

        service = PlanetsService()
        entities = [
            PlanetEntity(name="C Planet", **{k: v for k, v in sample_planet_payload.items() if k != 'name'}),
            PlanetEntity(name="A Planet", **{k: v for k, v in sample_planet_payload.items() if k != 'name'}),
            PlanetEntity(name="B Planet", **{k: v for k, v in sample_planet_payload.items() if k != 'name'}),
        ]

        ordered = service._order_entities(entities, "asc")

        assert ordered[0].name == "A Planet"
        assert ordered[1].name == "B Planet"
        assert ordered[2].name == "C Planet"

    def test_order_entities_descending(self, sample_planet_payload):
        """Test ordering entities in descending order."""
        from app.domain.entities.planets.planets_entity import PlanetEntity

        service = PlanetsService()
        entities = [
            PlanetEntity(name="A Planet", **{k: v for k, v in sample_planet_payload.items() if k != 'name'}),
            PlanetEntity(name="C Planet", **{k: v for k, v in sample_planet_payload.items() if k != 'name'}),
            PlanetEntity(name="B Planet", **{k: v for k, v in sample_planet_payload.items() if k != 'name'}),
        ]

        ordered = service._order_entities(entities, "desc")

        assert ordered[0].name == "C Planet"
        assert ordered[1].name == "B Planet"
        assert ordered[2].name == "A Planet"

    def test_instance_payload(self, sample_planet_payload):
        """Test creating PlanetDTO from payload."""
        service = PlanetsService()
        dto = service._instance_payload(sample_planet_payload)

        assert dto.name == "Tatooine"
        assert dto.climate == "arid"
        assert dto.terrain == "desert"
        assert dto.population == "200000"
        assert len(dto.residents) == 2
