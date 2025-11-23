#!/usr/bin/env bash
# Docker container integration tests
# This script tests the httpbin Docker container to ensure it works correctly

set -e

# Generate random suffix with multiple fallbacks for portability
RANDOM_SUFFIX=$(shuf -i 1000-9999 -n 1 2>/dev/null || echo "${RANDOM:-$(date +%N | cut -c6-9)}")
CONTAINER_NAME="httpbin-test-$(date +%s)-${RANDOM_SUFFIX}"
IMAGE_TAG="${IMAGE_TAG:-httpbin:test}"
PORT="${PORT:-8080}"
STARTUP_TIMEOUT="${STARTUP_TIMEOUT:-30}"
CLEANUP_ON_EXIT=true

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# Cleanup function
cleanup() {
    if [ "$CLEANUP_ON_EXIT" = true ]; then
        log_info "Cleaning up containers..."
        docker stop "$CONTAINER_NAME" 2>/dev/null || true
        docker rm "$CONTAINER_NAME" 2>/dev/null || true
    fi
}

# Set trap to cleanup on exit
trap cleanup EXIT

# Test 1: Container starts successfully
test_container_start() {
    log_info "Test 1: Starting container..."
    
    docker run -d --name "$CONTAINER_NAME" -p "$PORT:8080" "$IMAGE_TAG"
    
    # Wait for container to be ready (configurable via STARTUP_TIMEOUT)
    log_info "Waiting for container to be ready (timeout: ${STARTUP_TIMEOUT}s)..."
    for i in $(seq 1 "$STARTUP_TIMEOUT"); do
        if curl -s -f "http://localhost:$PORT/status/200" > /dev/null 2>&1; then
            log_info "✓ Container started successfully"
            return 0
        fi
        sleep 1
    done
    
    log_error "✗ Container failed to start within ${STARTUP_TIMEOUT} seconds"
    docker logs "$CONTAINER_NAME"
    return 1
}

# Test 2: GET endpoint
test_get_endpoint() {
    log_info "Test 2: Testing GET endpoint..."
    
    response=$(curl -s "http://localhost:$PORT/get?test=value&foo=bar")
    
    if echo "$response" | grep -q "test"; then
        log_info "✓ GET endpoint works correctly"
        return 0
    else
        log_error "✗ GET endpoint test failed"
        echo "Response: $response"
        return 1
    fi
}

# Test 3: POST endpoint with JSON
test_post_endpoint() {
    log_info "Test 3: Testing POST endpoint with JSON..."
    
    response=$(curl -s -X POST "http://localhost:$PORT/post" \
        -H "Content-Type: application/json" \
        -d '{"key": "value", "number": 42}')
    
    if echo "$response" | grep -q "key" && echo "$response" | grep -q "value"; then
        log_info "✓ POST endpoint works correctly"
        return 0
    else
        log_error "✗ POST endpoint test failed"
        echo "Response: $response"
        return 1
    fi
}

# Test 4: Status code endpoint
test_status_codes() {
    log_info "Test 4: Testing status code endpoints..."
    
    # Test various status codes
    for code in 200 201 204 400 404 500; do
        status=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:$PORT/status/$code")
        if [ "$status" = "$code" ]; then
            log_info "  ✓ Status code $code works"
        else
            log_error "  ✗ Expected status $code, got $status"
            return 1
        fi
    done
    
    log_info "✓ All status code tests passed"
    return 0
}

# Test 5: Headers endpoint
test_headers_endpoint() {
    log_info "Test 5: Testing headers endpoint..."
    
    response=$(curl -s "http://localhost:$PORT/headers" \
        -H "X-Custom-Header: TestValue")
    
    if echo "$response" | grep -q "X-Custom-Header"; then
        log_info "✓ Headers endpoint works correctly"
        return 0
    else
        log_error "✗ Headers endpoint test failed"
        echo "Response: $response"
        return 1
    fi
}

# Test 6: IP endpoint
test_ip_endpoint() {
    log_info "Test 6: Testing IP endpoint..."
    
    response=$(curl -s "http://localhost:$PORT/ip")
    
    if echo "$response" | grep -q "origin"; then
        log_info "✓ IP endpoint works correctly"
        return 0
    else
        log_error "✗ IP endpoint test failed"
        echo "Response: $response"
        return 1
    fi
}

# Test 7: Delay endpoint
test_delay_endpoint() {
    log_info "Test 7: Testing delay endpoint..."
    
    start_time=$(date +%s)
    response=$(curl -s "http://localhost:$PORT/delay/2")
    end_time=$(date +%s)
    elapsed=$((end_time - start_time))
    
    if [ $elapsed -ge 2 ] && echo "$response" | grep -q "args"; then
        log_info "✓ Delay endpoint works correctly (elapsed: ${elapsed}s)"
        return 0
    else
        log_error "✗ Delay endpoint test failed (elapsed: ${elapsed}s)"
        echo "Response: $response"
        return 1
    fi
}

# Test 8: UUID endpoint
test_uuid_endpoint() {
    log_info "Test 8: Testing UUID endpoint..."
    
    response=$(curl -s "http://localhost:$PORT/uuid")
    
    if echo "$response" | grep -q "uuid"; then
        log_info "✓ UUID endpoint works correctly"
        return 0
    else
        log_error "✗ UUID endpoint test failed"
        echo "Response: $response"
        return 1
    fi
}

# Test 9: JSON format endpoint
test_json_endpoint() {
    log_info "Test 9: Testing JSON format endpoint..."
    
    response=$(curl -s "http://localhost:$PORT/json")
    
    if echo "$response" | grep -q "slideshow"; then
        log_info "✓ JSON format endpoint works correctly"
        return 0
    else
        log_error "✗ JSON format endpoint test failed"
        echo "Response: $response"
        return 1
    fi
}

# Test 10: Container runs as non-root user
test_nonroot_user() {
    log_info "Test 10: Verifying container runs as non-root user..."
    
    user_id=$(docker exec "$CONTAINER_NAME" id -u)
    
    if [ "$user_id" = "1680" ]; then
        log_info "✓ Container runs as expected user (uid 1680)"
        return 0
    else
        log_error "✗ Container is not running as expected user (uid 1680), got: $user_id"
        return 1
    fi
}

# Main test execution
main() {
    log_info "Starting Docker container tests for $IMAGE_TAG"
    log_info "================================================"
    echo
    
    # Run all tests
    test_container_start || exit 1
    echo
    test_get_endpoint || exit 1
    echo
    test_post_endpoint || exit 1
    echo
    test_status_codes || exit 1
    echo
    test_headers_endpoint || exit 1
    echo
    test_ip_endpoint || exit 1
    echo
    test_delay_endpoint || exit 1
    echo
    test_uuid_endpoint || exit 1
    echo
    test_json_endpoint || exit 1
    echo
    test_nonroot_user || exit 1
    echo
    
    log_info "================================================"
    log_info "All tests passed! ✓"
}

# Run main function
main
