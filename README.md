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
# Install dependencies
uv sync

# Or manually install
uv add fastapi uvicorn python-multipart
```

## Usage

### Run the server

```bash
# Using uv
uv run python -m httpbin.main

# Or directly with Python
python src/httpbin/main.py

# Or with uvicorn
uvicorn httpbin.main:app --reload
```

The server will start on `http://localhost:8000`

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
# Install development dependencies
pip install -e .[dev]

# Or with uv
uv sync --dev
```

### Code Quality

This project uses [ruff](https://docs.astral.sh/ruff/) for linting and code formatting.

#### Run Linting

```bash
# Check code for issues
ruff check src tests

# Auto-fix issues
ruff check --fix src tests
```

#### Format Code

```bash
# Check code formatting
ruff format --check src tests

# Format code
ruff format src tests
```

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_http_methods.py
```

## License

MIT
