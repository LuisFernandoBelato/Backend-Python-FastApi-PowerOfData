"""Pytest configuration and shared fixtures."""

import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(autouse=True)
def clear_cache():
    """Clear the service cache before each test."""
    from app.application.services.base_service import BaseSwapiService
    BaseSwapiService._cache.clear()
    yield
    BaseSwapiService._cache.clear()


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def mock_swapi_response():
    """Create a mock SWAPI response."""
    def _mock_response(data, status_code=200):
        mock = Mock()
        mock.status_code = status_code
        mock.json.return_value = data
        mock.raise_for_status = Mock()
        return mock
    return _mock_response


@pytest.fixture
def mock_requests_get(mock_swapi_response):
    """Mock requests.get to avoid real API calls."""
    with patch('requests.get') as mock_get:
        yield mock_get


@pytest.fixture
def sample_film_payload():
    """Sample film payload from SWAPI."""
    return {
        "title": "A New Hope",
        "episode_id": 4,
        "opening_crawl": "It is a period of civil war...",
        "director": "George Lucas",
        "producer": "Gary Kurtz, Rick McCallum",
        "release_date": "1977-05-25",
        "characters": [
            "https://swapi.dev/api/people/1/",
            "https://swapi.dev/api/people/2/"
        ],
        "planets": ["https://swapi.dev/api/planets/1/"],
        "starships": ["https://swapi.dev/api/starships/2/"],
        "vehicles": ["https://swapi.dev/api/vehicles/4/"],
        "species": ["https://swapi.dev/api/species/1/"],
        "url": "https://swapi.dev/api/films/1/",
        "created": "2014-12-10T14:23:31.880000Z",
        "edited": "2014-12-20T19:49:45.256000Z"
    }


@pytest.fixture
def sample_person_payload():
    """Sample person payload from SWAPI."""
    return {
        "name": "Luke Skywalker",
        "height": "172",
        "mass": "77",
        "hair_color": "blond",
        "skin_color": "fair",
        "eye_color": "blue",
        "birth_year": "19BBY",
        "gender": "male",
        "homeworld": "https://swapi.dev/api/planets/1/",
        "films": [
            "https://swapi.dev/api/films/1/",
            "https://swapi.dev/api/films/2/"
        ],
        "species": [],
        "vehicles": ["https://swapi.dev/api/vehicles/14/"],
        "starships": ["https://swapi.dev/api/starships/12/"],
        "url": "https://swapi.dev/api/people/1/",
        "created": "2014-12-09T13:50:51.644000Z",
        "edited": "2014-12-20T21:17:56.891000Z"
    }


@pytest.fixture
def sample_planet_payload():
    """Sample planet payload from SWAPI."""
    return {
        "name": "Tatooine",
        "rotation_period": "23",
        "orbital_period": "304",
        "diameter": "10465",
        "climate": "arid",
        "gravity": "1 standard",
        "terrain": "desert",
        "surface_water": "1",
        "population": "200000",
        "residents": [
            "https://swapi.dev/api/people/1/",
            "https://swapi.dev/api/people/2/"
        ],
        "films": ["https://swapi.dev/api/films/1/"],
        "url": "https://swapi.dev/api/planets/1/",
        "created": "2014-12-09T13:50:49.641000Z",
        "edited": "2014-12-20T20:58:18.411000Z"
    }


@pytest.fixture
def sample_species_payload():
    """Sample species payload from SWAPI."""
    return {
        "name": "Human",
        "classification": "mammal",
        "designation": "sentient",
        "average_height": "180",
        "skin_colors": "caucasian, black, asian, hispanic",
        "hair_colors": "blonde, brown, black, red",
        "eye_colors": "brown, blue, green, hazel, grey, amber",
        "average_lifespan": "120",
        "homeworld": "https://swapi.dev/api/planets/9/",
        "language": "Galactic Basic",
        "people": [
            "https://swapi.dev/api/people/1/",
            "https://swapi.dev/api/people/4/"
        ],
        "films": ["https://swapi.dev/api/films/1/"],
        "url": "https://swapi.dev/api/species/1/",
        "created": "2014-12-10T13:52:11.567000Z",
        "edited": "2014-12-20T21:36:42.136000Z"
    }


@pytest.fixture
def sample_starship_payload():
    """Sample starship payload from SWAPI."""
    return {
        "name": "Death Star",
        "model": "DS-1 Orbital Battle Station",
        "manufacturer": "Imperial Department of Military Research",
        "cost_in_credits": "1000000000000",
        "length": "120000",
        "max_atmosphering_speed": "n/a",
        "crew": "342953",
        "passengers": "843342",
        "cargo_capacity": "1000000000000",
        "consumables": "3 years",
        "hyperdrive_rating": "4.0",
        "MGLT": "10",
        "starship_class": "Deep Space Mobile Battlestation",
        "pilots": [],
        "films": ["https://swapi.dev/api/films/1/"],
        "url": "https://swapi.dev/api/starships/9/",
        "created": "2014-12-10T16:36:50.509000Z",
        "edited": "2014-12-20T21:26:24.783000Z"
    }


@pytest.fixture
def sample_vehicle_payload():
    """Sample vehicle payload from SWAPI."""
    return {
        "name": "Sand Crawler",
        "model": "Digger Crawler",
        "manufacturer": "Corellia Mining Corporation",
        "cost_in_credits": "150000",
        "length": "36.8",
        "max_atmosphering_speed": "30",
        "crew": "46",
        "passengers": "30",
        "cargo_capacity": "50000",
        "consumables": "2 months",
        "vehicle_class": "wheeled",
        "pilots": [],
        "films": ["https://swapi.dev/api/films/1/"],
        "url": "https://swapi.dev/api/vehicles/4/",
        "created": "2014-12-10T15:36:25.724000Z",
        "edited": "2014-12-20T21:30:21.661000Z"
    }
