"""Unit tests for Vehicles endpoints."""

import pytest
from unittest.mock import Mock
from app.application.services.vehicles.vehicles_service import VehiclesService
from app.interfaces.query_params.vehicles.vehicles_query_params import VehiclesQueryParams


class TestVehiclesEndpoints:
    """Test suite for Vehicles API endpoints."""

    @pytest.mark.asyncio
    async def test_get_all_vehicles_success(self, client, mock_requests_get, sample_vehicle_payload):
        """Test getting all vehicles successfully."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_vehicle_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/vehicles/")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_vehicle_by_id_success(self, client, mock_requests_get, sample_vehicle_payload):
        """Test getting a specific vehicle by ID."""
        mock_requests_get.return_value.json.return_value = sample_vehicle_payload
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/vehicles/?id=4")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_vehicle_by_name_search(self, client, mock_requests_get, sample_vehicle_payload):
        """Test searching vehicles by name."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_vehicle_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/vehicles/?name=Crawler")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_vehicle_by_model_search(self, client, mock_requests_get, sample_vehicle_payload):
        """Test searching vehicles by model."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_vehicle_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/vehicles/?model=Digger")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_vehicle_with_all_relations(self, client, mock_requests_get, sample_vehicle_payload):
        """Test getting vehicle with all related entities."""
        mock_requests_get.return_value.json.return_value = sample_vehicle_payload
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/vehicles/?id=4&all=true")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_vehicle_with_films(self, client, mock_requests_get, sample_vehicle_payload):
        """Test getting vehicle with film details."""
        mock_requests_get.return_value.json.return_value = sample_vehicle_payload
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/vehicles/?id=4&films=true")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_vehicle_with_pilots(self, client, mock_requests_get, sample_vehicle_payload):
        """Test getting vehicle with pilot details."""
        mock_requests_get.return_value.json.return_value = sample_vehicle_payload
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/vehicles/?id=4&pilots=true")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_vehicles_with_order_asc(self, client, mock_requests_get, sample_vehicle_payload):
        """Test getting vehicles ordered ascending by name."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_vehicle_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/vehicles/?order=asc")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_vehicles_with_order_desc(self, client, mock_requests_get, sample_vehicle_payload):
        """Test getting vehicles ordered descending by name."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_vehicle_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/vehicles/?order=desc")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestVehiclesService:
    """Test suite for VehiclesService class."""

    @pytest.mark.asyncio
    async def test_create_entities_with_results(self, mock_requests_get, sample_vehicle_payload):
        """Test creating vehicle entities from SWAPI results."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_vehicle_payload, sample_vehicle_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        service = VehiclesService()
        query_params = VehiclesQueryParams()

        entities = await service.create_entities("https://swapi.dev/api/vehicles/", query_params)

        assert isinstance(entities, list)
        assert len(entities) == 2

    @pytest.mark.asyncio
    async def test_create_entities_single_result(self, mock_requests_get, sample_vehicle_payload):
        """Test creating a single vehicle entity."""
        mock_requests_get.return_value.json.return_value = sample_vehicle_payload
        mock_requests_get.return_value.raise_for_status = Mock()

        service = VehiclesService()
        query_params = VehiclesQueryParams()

        entities = await service.create_entities("https://swapi.dev/api/vehicles/4/", query_params)

        assert isinstance(entities, list)
        assert len(entities) == 1
        assert entities[0].name == "Sand Crawler"

    @pytest.mark.asyncio
    async def test_create_entities_empty_results(self, mock_requests_get):
        """Test handling empty results."""
        mock_requests_get.return_value.json.return_value = {"results": []}
        mock_requests_get.return_value.raise_for_status = Mock()

        service = VehiclesService()
        query_params = VehiclesQueryParams()

        entities = await service.create_entities("https://swapi.dev/api/vehicles/", query_params)

        assert isinstance(entities, list)
        assert len(entities) == 0

    @pytest.mark.asyncio
    async def test_create_entity_returns_first(self, mock_requests_get, sample_vehicle_payload):
        """Test create_entity returns first vehicle from results."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_vehicle_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        service = VehiclesService()
        query_params = VehiclesQueryParams()

        entity = await service.create_entity("https://swapi.dev/api/vehicles/", query_params)

        assert entity is not None
        assert entity.name == "Sand Crawler"

    @pytest.mark.asyncio
    async def test_create_entity_returns_none_when_empty(self, mock_requests_get):
        """Test create_entity returns None for empty results."""
        mock_requests_get.return_value.json.return_value = {"results": []}
        mock_requests_get.return_value.raise_for_status = Mock()

        service = VehiclesService()
        query_params = VehiclesQueryParams()

        entity = await service.create_entity("https://swapi.dev/api/vehicles/", query_params)

        assert entity is None

    def test_resolve_url_with_search_params(self, mock_requests_get, sample_vehicle_payload):
        """Test resolve_url with search parameters."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_vehicle_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        service = VehiclesService()
        result = service.resolve_url("https://swapi.dev/api/vehicles/", {"search": "Crawler"})

        assert result.name == "Sand Crawler"

    def test_resolve_url_no_results_raises_error(self, mock_requests_get):
        """Test resolve_url raises error when no vehicles match."""
        mock_requests_get.return_value.json.return_value = {"results": []}
        mock_requests_get.return_value.raise_for_status = Mock()

        service = VehiclesService()

        with pytest.raises(ValueError, match="Nenhum veículo corresponde ao filtro solicitado"):
            service.resolve_url("https://swapi.dev/api/vehicles/", {"search": "Nonexistent"})

    def test_build_search_params_with_name(self):
        """Test building search params with name filter."""
        service = VehiclesService()
        query_params = VehiclesQueryParams(name="Sand Crawler")

        params = service._build_search_params(query_params)

        assert params == {"search": "Sand Crawler"}

    def test_build_search_params_with_model(self):
        """Test building search params with model filter."""
        service = VehiclesService()
        query_params = VehiclesQueryParams(model="Digger Crawler")

        params = service._build_search_params(query_params)

        assert params == {"search": "Digger Crawler"}

    def test_build_search_params_without_filters(self):
        """Test building search params without filters."""
        service = VehiclesService()
        query_params = VehiclesQueryParams()

        params = service._build_search_params(query_params)

        assert params is None

    def test_order_entities_ascending(self, sample_vehicle_payload):
        """Test ordering entities in ascending order."""
        from app.domain.entities.vehicles.vehicles_entity import VehicleEntity

        service = VehiclesService()
        entities = [
            VehicleEntity(name="C Vehicle", **{k: v for k, v in sample_vehicle_payload.items() if k != 'name'}),
            VehicleEntity(name="A Vehicle", **{k: v for k, v in sample_vehicle_payload.items() if k != 'name'}),
            VehicleEntity(name="B Vehicle", **{k: v for k, v in sample_vehicle_payload.items() if k != 'name'}),
        ]

        ordered = service._order_entities(entities, "asc")

        assert ordered[0].name == "A Vehicle"
        assert ordered[1].name == "B Vehicle"
        assert ordered[2].name == "C Vehicle"

    def test_order_entities_descending(self, sample_vehicle_payload):
        """Test ordering entities in descending order."""
        from app.domain.entities.vehicles.vehicles_entity import VehicleEntity

        service = VehiclesService()
        entities = [
            VehicleEntity(name="A Vehicle", **{k: v for k, v in sample_vehicle_payload.items() if k != 'name'}),
            VehicleEntity(name="C Vehicle", **{k: v for k, v in sample_vehicle_payload.items() if k != 'name'}),
            VehicleEntity(name="B Vehicle", **{k: v for k, v in sample_vehicle_payload.items() if k != 'name'}),
        ]

        ordered = service._order_entities(entities, "desc")

        assert ordered[0].name == "C Vehicle"
        assert ordered[1].name == "B Vehicle"
        assert ordered[2].name == "A Vehicle"

    def test_instance_payload(self, sample_vehicle_payload):
        """Test creating VehicleDTO from payload."""
        service = VehiclesService()
        dto = service._instance_payload(sample_vehicle_payload)

        assert dto.name == "Sand Crawler"
        assert dto.model == "Digger Crawler"
        assert dto.vehicle_class == "wheeled"
        assert dto.manufacturer == "Corellia Mining Corporation"
        assert len(dto.films) == 1
