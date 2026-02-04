# Python-FastApi-SWAPI

API em Python FastAPI que consome a SWAPI (Star Wars API) com arquitetura DDD.

## Comandos para rodar aplicação

### Windows

```bash
.\venv\Scripts\Activate.ps1
```

```bash
pip install -r requirements.txt
```

```bash
uvicorn app.main:app --reload
```

---

## Linux

```bash
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

```bash
uvicorn app.main:app --reload
```

---

## Testes

Este projeto possui cobertura completa de testes unitários para todos os endpoints.

### Executar Testes

**Windows (PowerShell):**

```bash
.\run_tests.ps1
```

**Linux/Mac:**

```bash
chmod +x run_tests.sh
./run_tests.sh
```

**Manual:**

```bash
pytest
```

### Cobertura de Testes

Para ver o relatório de cobertura:

```bash
pytest --cov=app --cov-report=html
```

Depois abra `htmlcov/index.html` no navegador.

### Endpoints Testados

- ✅ `/films/` - Filmes
- ✅ `/people/` - Personagens
- ✅ `/planets/` - Planetas
- ✅ `/species/` - Espécies
- ✅ `/starships/` - Naves
- ✅ `/vehicles/` - Veículos
- ✅ `/health` - Healthcheck

Veja mais detalhes em [tests/README.md](tests/README.md)
