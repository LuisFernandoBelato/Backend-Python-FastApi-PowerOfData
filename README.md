# API em Python FastAPI que consome a SWAPI (Star Wars API) com arquitetura DDD.

# <a href="https://github.com/LuisFernandoBelato/Backend-Python-FastApi-PowerOfData/blob/main/Documenta%C3%A7%C3%A3o%20T%C3%A9cnica%20de%20Software.pdf" title="Link para PDF da Documentação Técnica" target="_blank" rel="doc">Documentação Técnica</a>

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
