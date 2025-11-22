# Copilot Instructions for httpbin

## Project Overview

This is a FastAPI-based HTTP testing service (like httpbin.org) that echoes back request details for testing HTTP clients. The architecture follows a modular router pattern with strict separation between routers, schemas, utilities, and configuration.

## Architecture

- **Entry Point**: `src/httpbin/main.py` creates the app via `create_app()` factory, includes all routers, and configures CORS. The module is runnable (`python -m httpbin.main`).
- **Routers**: Modular endpoints in `src/httpbin/routers/` - each router is isolated by functionality (HTTP methods, status codes, dynamic behavior, etc.)
- **Schemas**: Pydantic models in `src/httpbin/schemas/responses.py` for type-safe API responses
- **Utils**: Shared logic in `src/httpbin/utils.py` - particularly `get_request_data()` which extracts comprehensive request information
- **Config**: Single `Settings` class in `src/httpbin/config.py` with application-wide constants (no environment variables, no pydantic-settings)

## Key Patterns

### Router Structure
All routers follow this pattern:
```python
from fastapi import APIRouter
router = APIRouter(tags=["Category Name"])
```
Routers are imported in `routers/__init__.py` and included in `main.py` via `app.include_router()`.

### Request Data Extraction
Use `get_request_data(request)` from utils - it handles JSON, form data, files, and raw body parsing automatically. Returns standardized dict with `args`, `data`, `files`, `form`, `headers`, `json`, `method`, `origin`, `url`.

### Response Models
All endpoints use Pydantic models with `response_model` parameter. Note: Use `Field(alias="json")` for JSON field names that conflict with Python keywords (see `RequestInfo.json_data`).

### Status Code Endpoints
The `/status/{codes}` endpoint accepts all HTTP methods via decorator stacking and uses FastAPI's `Response` object to set status codes dynamically.

### Configuration Limits
Limits are enforced via `settings` (e.g., `MAX_DELAY_SECONDS`, `MAX_REDIRECT_COUNT`). Always cap user input against these constants.

## Development Workflow

### Setup & Run
```bash
uv sync                           # Install dependencies (uses pyproject.toml, not uv.lock)
uv run python -m httpbin.main     # Run server on 0.0.0.0:8000 with auto-reload
```

### Testing
```bash
uv run pytest                     # Run all tests
uv run pytest tests/test_*.py     # Run specific test file
```

Tests use `TestClient` fixture from `conftest.py`. All test classes follow `TestFeatureName` naming pattern.

### Code Quality
```bash
ruff check src tests              # Lint code (uses pyproject.toml config)
ruff check --fix src tests        # Auto-fix issues
ruff format src tests             # Format code (100 char line length, double quotes)
```

### Docker Build & Run
```bash
docker build -t httpbin:0.1.0 .   # Multi-stage RockyLinux UBI build
docker run --rm -it -p 8080:8080 httpbin:0.1.0  # Runs uvicorn on 0.0.0.0:8080
```

The Dockerfile uses:
- Multi-stage build (base → builder → final) with RockyLinux 9 UBI
- Dedicated user (uid/gid 1680) for security
- uv for wheel building and dependency export
- Environment variables: `UVICORN_APP`, `UVICORN_HOST`, `UVICORN_PORT`, `UVICORN_WORKERS` (default 4)

### Adding New Endpoints

1. Create/update router in `src/httpbin/routers/`
2. Define response schema in `src/httpbin/schemas/responses.py` if needed
3. Export router in `routers/__init__.py`
4. Include in `main.py` if new router
5. Add tests in `tests/test_*.py` matching router name

### Project Structure Convention
```
src/httpbin/
├── routers/          # One router per feature category
├── schemas/          # Pydantic models only
├── config.py         # Settings class (no env vars)
├── utils.py          # Shared helper functions
└── main.py           # App factory and entry point
```

## Common Tasks

### Adding Request Limits
Update `Settings` class in `config.py`, then enforce in router endpoint logic.

### Handling New Content Types
Extend `get_request_data()` in `utils.py` with new content-type parsing logic.

### Custom Response Formats
See `routers/response_formats.py` for examples of returning HTML, XML, plain text using FastAPI's `Response` classes.

## Testing Conventions

- Use the `client` fixture (TestClient) for all endpoint tests
- Test class structure: `class TestFeatureName` with methods like `test_specific_behavior`
- Always verify response status code, response structure, and key fields
- Test both happy paths and error conditions (e.g., invalid input)
- Each test file mirrors a router file (e.g., `test_http_methods.py` tests `routers/http_methods.py`)

## Package Management

This project uses **uv** (not pip or poetry):
- No `uv.lock` file - dependencies are specified in `pyproject.toml` only
- Install with `uv sync` (installs both main and dev dependencies)
- Dev dependencies include: pytest, pytest-asyncio, httpx, ruff
- Python 3.12+ required (specified in `pyproject.toml`)
- CLI entry point: `httpbin = "httpbin.main:main"` (can run `uv run httpbin`)
