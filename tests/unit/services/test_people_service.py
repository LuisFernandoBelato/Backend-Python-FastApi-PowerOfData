"""Unit tests for People endpoints."""

import pytest
from unittest.mock import Mock
from app.application.services.people.people_service import PeopleService
from app.interfaces.query_params.people.people_query_params import PeopleQueryParams


class TestPeopleEndpoints:
    """Test suite for People API endpoints."""

    @pytest.mark.asyncio
    async def test_get_all_people_success(self, client, mock_requests_get, sample_person_payload):
        """Test getting all people successfully."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_person_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/people/")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_person_by_id_success(self, client, mock_requests_get, sample_person_payload):
        """Test getting a specific person by ID."""
        mock_requests_get.return_value.json.return_value = sample_person_payload
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/people/?id=1")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_person_by_name_search(self, client, mock_requests_get, sample_person_payload):
        """Test searching people by name."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_person_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/people/?name=Luke")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_person_with_all_relations(self, client, mock_requests_get, sample_person_payload):
        """Test getting person with all related entities."""
        mock_requests_get.return_value.json.return_value = sample_person_payload
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/people/?id=1&all=true")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_person_with_films(self, client, mock_requests_get, sample_person_payload):
        """Test getting person with film details."""
        mock_requests_get.return_value.json.return_value = sample_person_payload
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/people/?id=1&films=true")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_person_with_species(self, client, mock_requests_get, sample_person_payload):
        """Test getting person with species details."""
        mock_requests_get.return_value.json.return_value = sample_person_payload
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/people/?id=1&species=true")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_person_with_starships(self, client, mock_requests_get, sample_person_payload):
        """Test getting person with starship details."""
        mock_requests_get.return_value.json.return_value = sample_person_payload
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/people/?id=1&starships=true")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_person_with_vehicles(self, client, mock_requests_get, sample_person_payload):
        """Test getting person with vehicle details."""
        mock_requests_get.return_value.json.return_value = sample_person_payload
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/people/?id=1&vehicles=true")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_people_with_order_asc(self, client, mock_requests_get, sample_person_payload):
        """Test getting people ordered ascending by name."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_person_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/people/?order=asc")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_people_with_order_desc(self, client, mock_requests_get, sample_person_payload):
        """Test getting people ordered descending by name."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_person_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        response = client.get("/people/?order=desc")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestPeopleService:
    """Test suite for PeopleService class."""

    @pytest.mark.asyncio
    async def test_create_entities_with_results(self, mock_requests_get, sample_person_payload):
        """Test creating person entities from SWAPI results."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_person_payload, sample_person_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        service = PeopleService()
        query_params = PeopleQueryParams()

        entities = await service.create_entities("https://swapi.dev/api/people/", query_params)

        assert isinstance(entities, list)
        assert len(entities) == 2

    @pytest.mark.asyncio
    async def test_create_entities_single_result(self, mock_requests_get, sample_person_payload):
        """Test creating a single person entity."""
        mock_requests_get.return_value.json.return_value = sample_person_payload
        mock_requests_get.return_value.raise_for_status = Mock()

        service = PeopleService()
        query_params = PeopleQueryParams()

        entities = await service.create_entities("https://swapi.dev/api/people/1/", query_params)

        assert isinstance(entities, list)
        assert len(entities) == 1
        assert entities[0].name == "Luke Skywalker"

    @pytest.mark.asyncio
    async def test_create_entities_empty_results(self, mock_requests_get):
        """Test handling empty results."""
        mock_requests_get.return_value.json.return_value = {"results": []}
        mock_requests_get.return_value.raise_for_status = Mock()

        service = PeopleService()
        query_params = PeopleQueryParams()

        entities = await service.create_entities("https://swapi.dev/api/people/", query_params)

        assert isinstance(entities, list)
        assert len(entities) == 0

    @pytest.mark.asyncio
    async def test_create_entity_returns_first(self, mock_requests_get, sample_person_payload):
        """Test create_entity returns first person from results."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_person_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        service = PeopleService()
        query_params = PeopleQueryParams()

        entity = await service.create_entity("https://swapi.dev/api/people/", query_params)

        assert entity is not None
        assert entity.name == "Luke Skywalker"

    @pytest.mark.asyncio
    async def test_create_entity_returns_none_when_empty(self, mock_requests_get):
        """Test create_entity returns None for empty results."""
        mock_requests_get.return_value.json.return_value = {"results": []}
        mock_requests_get.return_value.raise_for_status = Mock()

        service = PeopleService()
        query_params = PeopleQueryParams()

        entity = await service.create_entity("https://swapi.dev/api/people/", query_params)

        assert entity is None

    def test_resolve_url_with_search_params(self, mock_requests_get, sample_person_payload):
        """Test resolve_url with search parameters."""
        mock_requests_get.return_value.json.return_value = {
            "results": [sample_person_payload]
        }
        mock_requests_get.return_value.raise_for_status = Mock()

        service = PeopleService()
        result = service.resolve_url("https://swapi.dev/api/people/", {"search": "Luke"})

        assert result.name == "Luke Skywalker"

    def test_resolve_url_no_results_raises_error(self, mock_requests_get):
        """Test resolve_url raises error when no people match."""
        mock_requests_get.return_value.json.return_value = {"results": []}
        mock_requests_get.return_value.raise_for_status = Mock()

        service = PeopleService()

        with pytest.raises(ValueError, match="Nenhuma pessoa corresponde ao filtro solicitado"):
            service.resolve_url("https://swapi.dev/api/people/", {"search": "Nonexistent"})

    def test_build_search_params_with_name(self):
        """Test building search params with name filter."""
        service = PeopleService()
        query_params = PeopleQueryParams(name="Luke")

        params = service._build_search_params(query_params)

        assert params == {"search": "Luke"}

    def test_build_search_params_without_name(self):
        """Test building search params without name."""
        service = PeopleService()
        query_params = PeopleQueryParams()

        params = service._build_search_params(query_params)

        assert params is None

    def test_order_entities_ascending(self, sample_person_payload):
        """Test ordering entities in ascending order."""
        from app.domain.entities.people.people_entity import PeopleEntity

        service = PeopleService()
        entities = [
            PeopleEntity(name="C Person", **{k: v for k, v in sample_person_payload.items() if k != 'name'}),
            PeopleEntity(name="A Person", **{k: v for k, v in sample_person_payload.items() if k != 'name'}),
            PeopleEntity(name="B Person", **{k: v for k, v in sample_person_payload.items() if k != 'name'}),
        ]

        ordered = service._order_entities(entities, "asc")

        assert ordered[0].name == "A Person"
        assert ordered[1].name == "B Person"
        assert ordered[2].name == "C Person"

    def test_order_entities_descending(self, sample_person_payload):
        """Test ordering entities in descending order."""
        from app.domain.entities.people.people_entity import PeopleEntity

        service = PeopleService()
        entities = [
            PeopleEntity(name="A Person", **{k: v for k, v in sample_person_payload.items() if k != 'name'}),
            PeopleEntity(name="C Person", **{k: v for k, v in sample_person_payload.items() if k != 'name'}),
            PeopleEntity(name="B Person", **{k: v for k, v in sample_person_payload.items() if k != 'name'}),
        ]

        ordered = service._order_entities(entities, "desc")

        assert ordered[0].name == "C Person"
        assert ordered[1].name == "B Person"
        assert ordered[2].name == "A Person"

    def test_instance_payload(self, sample_person_payload):
        """Test creating PersonDTO from payload."""
        service = PeopleService()
        dto = service._instance_payload(sample_person_payload)

        assert dto.name == "Luke Skywalker"
        assert dto.height == "172"
        assert dto.mass == "77"
        assert dto.gender == "male"
        assert len(dto.films) == 2
