# Testes - Python FastAPI SWAPI

## Estrutura de Testes

Esta pasta contém a cobertura completa de testes unitários para todos os endpoints da API Star Wars.

```
tests/
├── conftest.py                           # Fixtures compartilhadas
├── unit/
│   └── services/
│       ├── test_films_service.py         # Testes para films
│       ├── test_people_service.py        # Testes para people
│       ├── test_planets_service.py       # Testes para planets
│       ├── test_species_service.py       # Testes para species
│       ├── test_starships_service.py     # Testes para starships
│       └── test_vehicles_service.py      # Testes para vehicles
```

## Executar Testes

### Instalar Dependências

```bash
pip install -r requirements.txt
```

### Executar Todos os Testes

```bash
pytest
```

### Executar Testes de um Service Específico

```bash
# Testar apenas films
pytest tests/unit/services/test_films_service.py

# Testar apenas people
pytest tests/unit/services/test_people_service.py

# Testar apenas planets
pytest tests/unit/services/test_planets_service.py
```

### Executar com Cobertura

```bash
pytest --cov=app --cov-report=html
```

O relatório de cobertura HTML será gerado em `htmlcov/index.html`

### Executar Testes Específicos

```bash
# Executar apenas testes de endpoints
pytest -k "Endpoints"

# Executar apenas testes de services
pytest -k "Service"

# Executar teste específico
pytest tests/unit/services/test_films_service.py::TestFilmsEndpoints::test_get_all_films_success
```

### Modo Verbose

```bash
pytest -v
```

### Parar no Primeiro Erro

```bash
pytest -x
```

## Cobertura de Testes

Cada service tem testes para:

### Endpoints (Testes de Integração)

- ✅ Listar todos os recursos
- ✅ Buscar por ID
- ✅ Buscar por nome/título
- ✅ Buscar com todas as relações (`all=true`)
- ✅ Buscar com relações específicas (films, characters, etc.)
- ✅ Ordenação ascendente e descendente

### Services (Testes Unitários)

- ✅ `create_entities()` - múltiplos resultados
- ✅ `create_entities()` - resultado único
- ✅ `create_entities()` - resultados vazios
- ✅ `create_entity()` - retorna primeiro resultado
- ✅ `create_entity()` - retorna None quando vazio
- ✅ `resolve_url()` - com parâmetros de busca
- ✅ `resolve_url()` - erro quando não encontra resultados
- ✅ `_build_search_params()` - com e sem filtros
- ✅ `_order_entities()` - ordenação asc/desc
- ✅ `_instance_payload()` - criação de DTOs

## Fixtures Disponíveis

Definidas em `conftest.py`:

- `client` - TestClient do FastAPI
- `mock_requests_get` - Mock de requests.get
- `mock_swapi_response` - Factory para criar respostas mockadas
- `sample_film_payload` - Payload de exemplo de filme
- `sample_person_payload` - Payload de exemplo de pessoa
- `sample_planet_payload` - Payload de exemplo de planeta
- `sample_species_payload` - Payload de exemplo de espécie
- `sample_starship_payload` - Payload de exemplo de nave
- `sample_vehicle_payload` - Payload de exemplo de veículo

## Tecnologias Utilizadas

- **pytest** - Framework de testes
- **pytest-asyncio** - Suporte para testes assíncronos
- **pytest-cov** - Cobertura de código
- **httpx** - Cliente HTTP para testes do FastAPI
- **unittest.mock** - Mocking de chamadas externas
