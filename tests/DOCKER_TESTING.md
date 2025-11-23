# Docker Testing

This directory contains tests for the Docker container.

## Docker Container Tests

### Automated Testing Script

The `test_docker.sh` script provides comprehensive integration tests for the Docker container:

```bash
# Build the Docker image first
docker build -t httpbin:test .

# Run the tests
./tests/test_docker.sh

# Run with custom port
PORT=9000 ./tests/test_docker.sh

# Run with custom image tag
IMAGE_TAG=httpbin:latest ./tests/test_docker.sh

# Run with custom startup timeout (useful for slower environments)
STARTUP_TIMEOUT=60 ./tests/test_docker.sh
```

### Tests Included

The script tests the following functionality:

1. **Container Startup**: Verifies the container starts and becomes ready
2. **GET Endpoint**: Tests the `/get` endpoint with query parameters
3. **POST Endpoint**: Tests the `/post` endpoint with JSON data
4. **Status Codes**: Tests various HTTP status codes (200, 201, 204, 400, 404, 500)
5. **Headers Endpoint**: Tests the `/headers` endpoint with custom headers
6. **IP Endpoint**: Tests the `/ip` endpoint
7. **Delay Endpoint**: Tests the `/delay/{seconds}` endpoint
8. **UUID Endpoint**: Tests the `/uuid` endpoint
9. **JSON Format**: Tests the `/json` format endpoint
10. **Non-root User**: Verifies the container runs as uid 1680 (not root)

### GitHub Actions Workflow

The `.github/workflows/docker.yml` workflow automatically:

1. **Lints the Dockerfile** using hadolint to ensure best practices
2. **Builds the Docker image** with proper build arguments
3. **Runs integration tests** to verify all endpoints work correctly
4. **Tests environment variables** to ensure configuration works
5. **Verifies security** by checking the container runs as non-root

The workflow runs on every push and pull request to the main branch.

## Manual Testing

You can also test the container manually:

```bash
# Build the image
docker build -t httpbin:test .

# Run the container
docker run -d --name httpbin-test -p 8080:8080 httpbin:test

# Test endpoints
curl http://localhost:8080/get?test=value
curl -X POST http://localhost:8080/post -H "Content-Type: application/json" -d '{"key":"value"}'
curl http://localhost:8080/status/200
curl http://localhost:8080/headers
curl http://localhost:8080/ip

# Check container logs
docker logs httpbin-test

# Stop and remove container
docker stop httpbin-test
docker rm httpbin-test
```

## Dockerfile Linting

The Dockerfile is automatically linted using [hadolint](https://github.com/hadolint/hadolint):

```bash
# Run hadolint locally
docker run --rm -i hadolint/hadolint < Dockerfile

# Or install hadolint and run directly
hadolint Dockerfile
```

### Ignored Rules

- `DL3041`: We intentionally don't specify package versions for DNF packages to ensure we get the latest security updates.
