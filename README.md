# httpbin

A simple HTTP Request & Response Service built with FastAPI.

## Features

This is a lightweight implementation of httpbin.org's core functionality, providing endpoints for testing HTTP requests and responses.

### Available Endpoints

#### HTTP Methods
- `GET /get` - Returns GET request data
- `POST /post` - Returns POST request data
- `PUT /put` - Returns PUT request data
- `PATCH /patch` - Returns PATCH request data
- `DELETE /delete` - Returns DELETE request data

#### Status Codes
- `GET/POST/PUT/PATCH/DELETE /status/{codes}` - Returns specified HTTP status code

#### Request Inspection
- `GET /headers` - Returns request headers
- `GET /ip` - Returns origin IP address
- `GET /user-agent` - Returns user-agent string

#### Response Formats
- `GET /json` - Returns a JSON response
- `GET /html` - Returns an HTML page
- `GET /xml` - Returns an XML response
- `GET /robots.txt` - Returns a robots.txt file

#### Dynamic Behavior
- `GET /delay/{seconds}` - Delays response for n seconds (max 10)
- `GET /base64/{value}` - Decodes base64-encoded string
- `POST /base64/encode` - Encodes text to base64
- `GET /uuid` - Returns a random UUID
- `GET /bytes/{n}` - Returns n random bytes

## Installation

This project uses `uv` for dependency management. Make sure you have Python 3.12+ installed.

```bash
# Install dependencies (production mode, no editable install)
uv sync --no-editable --frozen
```

## Usage

### Run the server

```bash
# Recommended: Using the CLI entry point
uv run httpbin

# Or run as Python module (with auto-reload)
uv run python -m httpbin.main

# Or directly with uvicorn
uv run uvicorn httpbin.main:app --reload --host 0.0.0.0 --port 8000
```

The server will start on `http://0.0.0.0:8000` (accessible via `http://localhost:8000`)

### Access API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Example Requests

```bash
# Test GET endpoint
curl http://localhost:8000/get?foo=bar

# Test POST with JSON
curl -X POST http://localhost:8000/post \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'

# Test status code
curl http://localhost:8000/status/404

# Test delay
curl http://localhost:8000/delay/2

# Get your IP
curl http://localhost:8000/ip

# Test headers
curl http://localhost:8000/headers
```

## Project Structure

```
src/httpbin/
├── __init__.py
├── main.py              # FastAPI application entry point
├── config.py            # Application configuration
├── utils.py             # Utility functions
├── schemas/             # Pydantic response models
│   ├── __init__.py
│   └── responses.py
└── routers/             # API route modules
    ├── __init__.py
    ├── http_methods.py
    ├── status_codes.py
    ├── request_inspection.py
    ├── response_formats.py
    └── dynamic.py
```

## Configuration

Edit `src/httpbin/config.py` to customize:

- CORS settings
- Maximum delay time
- Maximum redirect count
- Other application settings

## Development

### Setup Development Environment

```bash
# Install all dependencies including dev extras
uv sync --extra dev

# This will install: pytest, pytest-asyncio, httpx, ruff
```

### Code Quality

This project uses [ruff](https://docs.astral.sh/ruff/) for linting and code formatting.

#### Run Linting

```bash
# Check code for issues
uv run ruff check src tests

# Auto-fix issues
uv run ruff check --fix src tests
```

#### Format Code

```bash
# Check code formatting
uv run ruff format --check src tests

# Format code
uv run ruff format src tests
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_http_methods.py
```

## Docker Deployment

### Build Docker Image

```bash
# Build the image
docker build -t httpbin:0.1.0 .

# Build with custom build arguments
docker build \
  --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
  --build-arg VCS_REF=$(git rev-parse --short HEAD) \
  -t httpbin:0.1.0 .
```

### Run Docker Container

```bash
# Run with default settings (port 8080, 4 workers)
docker run --rm -it -p 8080:8080 httpbin:0.1.0

# Run with custom configuration
docker run --rm -it \
  -p 8000:8000 \
  -e UVICORN_PORT=8000 \
  -e UVICORN_WORKERS=2 \
  httpbin:0.1.0

# Run in detached mode
docker run -d -p 8080:8080 --name httpbin httpbin:0.1.0
```

### Docker Configuration

The Docker image supports the following environment variables:

- `UVICORN_APP`: Application module (default: `httpbin.main:app`)
- `UVICORN_HOST`: Host to bind (default: `0.0.0.0`)
- `UVICORN_PORT`: Port to bind (default: `8080`)
- `UVICORN_WORKERS`: Number of worker processes (default: `4`)

The image uses:

- **Base**: RockyLinux 9 UBI
- **Python**: 3.12
- **User**: Non-root user (uid/gid: 1680)
- **Security**: Multi-stage build with minimal runtime dependencies

### Docker Testing

The project uses [k6](https://k6.io/) for automated Docker container testing:

- **k6 Integration Tests**: Professional-grade API testing with clear assertions
- **GitHub Actions**: Automatic Dockerfile linting and container testing on every PR
- **Documentation**: See [tests/DOCKER_TESTING.md](tests/DOCKER_TESTING.md) for details

```bash
# Build and test the Docker image
docker build -t httpbin:test .
docker run -d --name httpbin-test -p 8080:8080 httpbin:test
k6 run --env BASE_URL=http://localhost:8080 tests/test_docker.js
docker stop httpbin-test && docker rm httpbin-test
```
```

## License

MIT
