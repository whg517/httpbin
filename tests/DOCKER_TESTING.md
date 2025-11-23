# Docker Testing with k6

This directory contains automated tests for the Docker container using [k6](https://k6.io/), a modern load testing tool for building and testing reliable systems.

## Why k6?

k6 is a powerful, developer-centric performance testing tool that offers:
- **Simple scripting**: Write tests in JavaScript (ES6+)
- **Easy maintenance**: Clean, readable test code
- **Rich assertions**: Built-in checks and custom metrics
- **CI/CD friendly**: Designed for automation in GitHub Actions
- **Professional-grade**: Used by teams worldwide for API testing

## Docker Container Tests

### Test Script

The `test_docker.js` script provides comprehensive integration tests for the Docker container, covering:

1. **HTTP Methods**: GET, POST, PUT, PATCH, DELETE
2. **Status Codes**: Tests various HTTP status codes (200, 201, 204, 400, 404, 500)
3. **Request Inspection**: Headers, IP address, User-Agent
4. **Response Formats**: JSON, HTML, XML
5. **Dynamic Behavior**: Delays, UUID generation, Base64 encoding/decoding
6. **Performance**: Validates response times (95th percentile < 2s)

### Running Tests Locally

**Prerequisites:**
- Docker installed
- k6 installed ([installation guide](https://k6.io/docs/getting-started/installation/))

```bash
# Build the Docker image
docker build -t httpbin:test .

# Start the container
docker run -d --name httpbin-test -p 8080:8080 httpbin:test

# Run k6 tests
k6 run --env BASE_URL=http://localhost:8080 tests/test_docker.js

# Clean up
docker stop httpbin-test
docker rm httpbin-test
```

### Test with Custom Configuration

```bash
# Start container with custom port
docker run -d --name httpbin-test -p 9000:9000 -e UVICORN_PORT=9000 httpbin:test

# Run tests against custom port
k6 run --env BASE_URL=http://localhost:9000 tests/test_docker.js
```

### Understanding k6 Output

k6 provides detailed test results including:
- **checks**: Pass/fail status of all assertions
- **http_req_duration**: Request duration metrics (avg, min, max, p95)
- **http_reqs**: Total number of HTTP requests
- **errors**: Custom error rate metric

Example output:
```
✓ GET status is 200
✓ GET response contains test param
✓ POST status is 200
✓ Status 200 returns correct code
...

checks.........................: 100.00% ✓ 45 ✗ 0
errors.........................: 0.00%   ✓ 0  ✗ 0
http_req_duration..............: avg=150ms min=10ms med=120ms max=2.5s p(95)=500ms
```

## GitHub Actions Workflow

The `.github/workflows/docker.yml` workflow automatically:

1. **Lints the Dockerfile** using hadolint
2. **Builds the Docker image** with proper build arguments
3. **Starts the container** and waits for readiness
4. **Runs k6 integration tests** to verify all endpoints
5. **Tests environment variables** with custom port configuration
6. **Runs k6 tests again** on the custom-configured container
7. **Verifies security** by checking non-root user execution

The workflow runs on every push and pull request to the main branch.

## Test Configuration

The k6 test script supports the following environment variables:

- `BASE_URL`: The base URL of the httpbin service (default: `http://localhost:8080`)

Test options can be modified in `test_docker.js`:
```javascript
export const options = {
  vus: 1,              // Number of virtual users
  iterations: 1,       // Number of test iterations
  thresholds: {
    errors: ['rate<0.1'],              // Max 10% error rate
    http_req_duration: ['p(95)<2000'], // 95th percentile < 2s
  },
};
```

## Installing k6

### Linux
```bash
# Debian/Ubuntu
sudo gpg -k
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6

# Fedora/CentOS
sudo dnf install https://dl.k6.io/rpm/repo.rpm
sudo dnf install k6
```

### macOS
```bash
brew install k6
```

### Windows
```powershell
choco install k6
# or
winget install k6
```

For other installation methods, see the [official k6 documentation](https://k6.io/docs/getting-started/installation/).

## Extending Tests

To add new tests, edit `tests/test_docker.js` and add new test blocks:

```javascript
// Test 16: New endpoint test
{
  console.log('Test 16: New endpoint test');
  const res = http.get(`${BASE_URL}/new-endpoint`);
  const success = check(res, {
    'New endpoint status is 200': (r) => r.status === 200,
    'New endpoint has expected data': (r) => r.body.includes('expected'),
  });
  errorRate.add(!success);
}
```

## Advantages Over Shell Scripts

Using k6 instead of shell scripts provides:

1. **Better Maintainability**: Clean JavaScript code vs complex bash
2. **Rich Assertions**: Built-in check() function with clear pass/fail
3. **Professional Metrics**: Automatic performance metrics and thresholds
4. **Better Error Reporting**: Clear, structured output
5. **Industry Standard**: Used by major companies for API testing
6. **Extensibility**: Easy to add load testing, stress testing, etc.
7. **Cross-platform**: Works consistently across Linux, macOS, Windows
