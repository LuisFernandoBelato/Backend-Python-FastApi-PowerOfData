"""Unit tests for Species endpoints."""

import pytest
from unittest.mock import Mock
from app.application.services.species.species_service import SpeciesService
from app.interfaces.query_params.species.species_query_params import SpeciesQueryParams


class TestSpeciesEndpoints:
    """Test suite for Species API endpoints."""

    @pytest.mark.asyncio
    async def test_get_all_species_success(self, client, mock_requests_get, sample_species_payload):
        """Test getting all species successfully."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_species_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/species/")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_species_by_id_success(self, client, mock_requests_get, sample_species_payload):
        """Test getting a specific species by ID."""
        mock_requests_get.return_value.json.return_value = sample_species_payload
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/species/?id=1")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_species_by_name_search(self, client, mock_requests_get, sample_species_payload):
        """Test searching species by name."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_species_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/species/?name=Human")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_species_with_all_relations(self, client, mock_requests_get, sample_species_payload):
        """Test getting species with all related entities."""
        mock_requests_get.return_value.json.return_value = sample_species_payload
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/species/?id=1&all=true")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_species_with_people(self, client, mock_requests_get, sample_species_payload):
        """Test getting species with people details."""
        mock_requests_get.return_value.json.return_value = sample_species_payload
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/species/?id=1&people=true")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_species_with_films(self, client, mock_requests_get, sample_species_payload):
        """Test getting species with film details."""
        mock_requests_get.return_value.json.return_value = sample_species_payload
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/species/?id=1&films=true")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_species_with_order_asc(self, client, mock_requests_get, sample_species_payload):
        """Test getting species ordered ascending by name."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_species_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/species/?order=asc")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_species_with_order_desc(self, client, mock_requests_get, sample_species_payload):
        """Test getting species ordered descending by name."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_species_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/species/?order=desc")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestSpeciesService:
    """Test suite for SpeciesService class."""

    @pytest.mark.asyncio
    async def test_create_entities_with_results(self, mock_requests_get, sample_species_payload):
        """Test creating species entities from SWAPI results."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_species_payload, sample_species_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        service = SpeciesService()
        query_params = SpeciesQueryParams()

        entities = await service.create_entities("https://swapi.dev/api/species/", query_params)

        assert isinstance(entities, list)
        assert len(entities) == 2

    @pytest.mark.asyncio
    async def test_create_entities_single_result(self, mock_requests_get, sample_species_payload):
        """Test creating a single species entity."""
        mock_requests_get.return_value.json.return_value = sample_species_payload
        mock_requests_get.return_value.raise_for_status = Mock()

        service = SpeciesService()
        query_params = SpeciesQueryParams()

        entities = await service.create_entities("https://swapi.dev/api/species/1/", query_params)

        assert isinstance(entities, list)
        assert len(entities) == 1
        assert entities[0].name == "Human"

    @pytest.mark.asyncio
    async def test_create_entities_empty_results(self, mock_requests_get):
        """Test handling empty results."""
        mock_requests_get.return_value.json.return_value = {"results": []}
        mock_requests_get.return_value.raise_for_status = Mock()

        service = SpeciesService()
        query_params = SpeciesQueryParams()

        entities = await service.create_entities("https://swapi.dev/api/species/", query_params)

        assert isinstance(entities, list)
        assert len(entities) == 0

    @pytest.mark.asyncio
    async def test_create_entity_returns_first(self, mock_requests_get, sample_species_payload):
        """Test create_entity returns first species from results."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_species_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        service = SpeciesService()
        query_params = SpeciesQueryParams()

        entity = await service.create_entity("https://swapi.dev/api/species/", query_params)

        assert entity is not None
        assert entity.name == "Human"

    @pytest.mark.asyncio
    async def test_create_entity_returns_none_when_empty(self, mock_requests_get):
        """Test create_entity returns None for empty results."""
        mock_requests_get.return_value.json.return_value = {"results": []}
        mock_requests_get.return_value.raise_for_status = Mock()

        service = SpeciesService()
        query_params = SpeciesQueryParams()

        entity = await service.create_entity("https://swapi.dev/api/species/", query_params)

        assert entity is None

    def test_resolve_url_with_search_params(self, mock_requests_get, sample_species_payload):
        """Test resolve_url with search parameters."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_species_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        service = SpeciesService()
        result = service.resolve_url("https://swapi.dev/api/species/", {"search": "Human"})

        assert result.name == "Human"

    def test_resolve_url_no_results_raises_error(self, mock_requests_get):
        """Test resolve_url raises error when no species match."""
        mock_requests_get.return_value.json.return_value = {"results": []}
        mock_requests_get.return_value.raise_for_status = Mock()

        service = SpeciesService()

        with pytest.raises(ValueError, match="Nenhuma espécie corresponde ao filtro solicitado"):
            service.resolve_url("https://swapi.dev/api/species/", {"search": "Nonexistent"})

    def test_build_search_params_with_name(self):
        """Test building search params with name filter."""
        service = SpeciesService()
        query_params = SpeciesQueryParams(name="Human")

        params = service._build_search_params(query_params)

        assert params == {"search": "Human"}

    def test_build_search_params_without_name(self):
        """Test building search params without name."""
        service = SpeciesService()
        query_params = SpeciesQueryParams()

        params = service._build_search_params(query_params)

        assert params is None

    def test_order_entities_ascending(self, sample_species_payload):
        """Test ordering entities in ascending order."""
        from app.domain.entities.species.species_entity import SpeciesEntity

        service = SpeciesService()
        entities = [
            SpeciesEntity(name="C Species", **{k: v for k, v in sample_species_payload.items() if k != 'name'}),
            SpeciesEntity(name="A Species", **{k: v for k, v in sample_species_payload.items() if k != 'name'}),
            SpeciesEntity(name="B Species", **{k: v for k, v in sample_species_payload.items() if k != 'name'}),
        ]

        ordered = service._order_entities(entities, "asc")

        assert ordered[0].name == "A Species"
        assert ordered[1].name == "B Species"
        assert ordered[2].name == "C Species"

    def test_order_entities_descending(self, sample_species_payload):
        """Test ordering entities in descending order."""
        from app.domain.entities.species.species_entity import SpeciesEntity

        service = SpeciesService()
        entities = [
            SpeciesEntity(name="A Species", **{k: v for k, v in sample_species_payload.items() if k != 'name'}),
            SpeciesEntity(name="C Species", **{k: v for k, v in sample_species_payload.items() if k != 'name'}),
            SpeciesEntity(name="B Species", **{k: v for k, v in sample_species_payload.items() if k != 'name'}),
        ]

        ordered = service._order_entities(entities, "desc")

        assert ordered[0].name == "C Species"
        assert ordered[1].name == "B Species"
        assert ordered[2].name == "A Species"

    def test_instance_payload(self, sample_species_payload):
        """Test creating SpeciesDTO from payload."""
        service = SpeciesService()
        dto = service._instance_payload(sample_species_payload)

        assert dto.name == "Human"
        assert dto.classification == "mammal"
        assert dto.designation == "sentient"
        assert dto.language == "Galactic Basic"
        assert len(dto.people) == 2
