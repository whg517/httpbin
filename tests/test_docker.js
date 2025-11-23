import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');

// Test configuration
export const options = {
  vus: 1, // Virtual users
  iterations: 1, // Run once for integration testing
  thresholds: {
    errors: ['rate<0.1'], // Error rate should be less than 10%
    http_req_duration: ['p(95)<2000'], // 95% of requests should be below 2s
  },
};

// Get base URL from environment variable or use default
const BASE_URL = __ENV.BASE_URL || 'http://localhost:8080';

export default function () {
  console.log(`Testing httpbin container at ${BASE_URL}`);

  // Test 1: GET endpoint with query parameters
  {
    console.log('Test 1: GET endpoint with query parameters');
    const res = http.get(`${BASE_URL}/get?test=value&foo=bar`);
    const success = check(res, {
      'GET status is 200': (r) => r.status === 200,
      'GET response contains test param': (r) => r.body.includes('test'),
      'GET response contains foo param': (r) => r.body.includes('foo'),
      'GET response is JSON': (r) => r.headers['Content-Type'].includes('application/json'),
    });
    errorRate.add(!success);
  }

  // Test 2: POST endpoint with JSON data
  {
    console.log('Test 2: POST endpoint with JSON data');
    const payload = JSON.stringify({
      key: 'value',
      number: 42,
    });
    const params = {
      headers: {
        'Content-Type': 'application/json',
      },
    };
    const res = http.post(`${BASE_URL}/post`, payload, params);
    const success = check(res, {
      'POST status is 200': (r) => r.status === 200,
      'POST response contains key': (r) => r.body.includes('key'),
      'POST response contains value': (r) => r.body.includes('value'),
      'POST response is JSON': (r) => r.headers['Content-Type'].includes('application/json'),
    });
    errorRate.add(!success);
  }

  // Test 3: PUT endpoint
  {
    console.log('Test 3: PUT endpoint');
    const payload = JSON.stringify({ update: 'data' });
    const params = {
      headers: {
        'Content-Type': 'application/json',
      },
    };
    const res = http.put(`${BASE_URL}/put`, payload, params);
    const success = check(res, {
      'PUT status is 200': (r) => r.status === 200,
      'PUT response is JSON': (r) => r.headers['Content-Type'].includes('application/json'),
    });
    errorRate.add(!success);
  }

  // Test 4: PATCH endpoint
  {
    console.log('Test 4: PATCH endpoint');
    const payload = JSON.stringify({ patch: 'data' });
    const params = {
      headers: {
        'Content-Type': 'application/json',
      },
    };
    const res = http.patch(`${BASE_URL}/patch`, payload, params);
    const success = check(res, {
      'PATCH status is 200': (r) => r.status === 200,
      'PATCH response is JSON': (r) => r.headers['Content-Type'].includes('application/json'),
    });
    errorRate.add(!success);
  }

  // Test 5: DELETE endpoint
  {
    console.log('Test 5: DELETE endpoint');
    const res = http.del(`${BASE_URL}/delete`);
    const success = check(res, {
      'DELETE status is 200': (r) => r.status === 200,
      'DELETE response is JSON': (r) => r.headers['Content-Type'].includes('application/json'),
    });
    errorRate.add(!success);
  }

  // Test 6: Status code endpoints
  {
    console.log('Test 6: Status code endpoints');
    const statusCodes = [200, 201, 204, 400, 404, 500];
    
    for (const code of statusCodes) {
      const res = http.get(`${BASE_URL}/status/${code}`);
      const success = check(res, {
        [`Status ${code} returns correct code`]: (r) => r.status === code,
      });
      errorRate.add(!success);
    }
  }

  // Test 7: Headers endpoint
  {
    console.log('Test 7: Headers endpoint');
    const params = {
      headers: {
        'X-Custom-Header': 'TestValue',
        'User-Agent': 'k6-test',
      },
    };
    const res = http.get(`${BASE_URL}/headers`, params);
    const success = check(res, {
      'Headers status is 200': (r) => r.status === 200,
      'Headers response contains custom header': (r) => r.body.includes('X-Custom-Header'),
      'Headers response is JSON': (r) => r.headers['Content-Type'].includes('application/json'),
    });
    errorRate.add(!success);
  }

  // Test 8: IP endpoint
  {
    console.log('Test 8: IP endpoint');
    const res = http.get(`${BASE_URL}/ip`);
    const success = check(res, {
      'IP status is 200': (r) => r.status === 200,
      'IP response contains origin': (r) => r.body.includes('origin'),
      'IP response is JSON': (r) => r.headers['Content-Type'].includes('application/json'),
    });
    errorRate.add(!success);
  }

  // Test 9: User-Agent endpoint
  {
    console.log('Test 9: User-Agent endpoint');
    const res = http.get(`${BASE_URL}/user-agent`);
    const success = check(res, {
      'User-Agent status is 200': (r) => r.status === 200,
      'User-Agent response contains user-agent': (r) => r.body.includes('user-agent'),
      'User-Agent response is JSON': (r) => r.headers['Content-Type'].includes('application/json'),
    });
    errorRate.add(!success);
  }

  // Test 10: Delay endpoint
  {
    console.log('Test 10: Delay endpoint (2 seconds)');
    const startTime = Date.now();
    const res = http.get(`${BASE_URL}/delay/2`);
    const duration = (Date.now() - startTime) / 1000;
    const success = check(res, {
      'Delay status is 200': (r) => r.status === 200,
      'Delay took at least 2 seconds': () => duration >= 2,
      'Delay response is JSON': (r) => r.headers['Content-Type'].includes('application/json'),
    });
    errorRate.add(!success);
  }

  // Test 11: UUID endpoint
  {
    console.log('Test 11: UUID endpoint');
    const res = http.get(`${BASE_URL}/uuid`);
    const success = check(res, {
      'UUID status is 200': (r) => r.status === 200,
      'UUID response contains uuid': (r) => r.body.includes('uuid'),
      'UUID response is JSON': (r) => r.headers['Content-Type'].includes('application/json'),
    });
    errorRate.add(!success);
  }

  // Test 12: Base64 decode endpoint
  {
    console.log('Test 12: Base64 decode endpoint');
    const encoded = 'aGVsbG8gd29ybGQ='; // "hello world"
    const res = http.get(`${BASE_URL}/base64/${encoded}`);
    const success = check(res, {
      'Base64 decode status is 200': (r) => r.status === 200,
      'Base64 decoded correctly': (r) => r.body.includes('hello world'),
    });
    errorRate.add(!success);
  }

  // Test 13: JSON format endpoint
  {
    console.log('Test 13: JSON format endpoint');
    const res = http.get(`${BASE_URL}/json`);
    const success = check(res, {
      'JSON status is 200': (r) => r.status === 200,
      'JSON response is valid': (r) => r.body.includes('slideshow'),
      'JSON content-type is correct': (r) => r.headers['Content-Type'].includes('application/json'),
    });
    errorRate.add(!success);
  }

  // Test 14: HTML format endpoint
  {
    console.log('Test 14: HTML format endpoint');
    const res = http.get(`${BASE_URL}/html`);
    const success = check(res, {
      'HTML status is 200': (r) => r.status === 200,
      'HTML response is valid': (r) => r.body.includes('<html>'),
      'HTML content-type is correct': (r) => r.headers['Content-Type'].includes('text/html'),
    });
    errorRate.add(!success);
  }

  // Test 15: XML format endpoint
  {
    console.log('Test 15: XML format endpoint');
    const res = http.get(`${BASE_URL}/xml`);
    const success = check(res, {
      'XML status is 200': (r) => r.status === 200,
      'XML response is valid': (r) => r.body.includes('<?xml'),
      'XML content-type is correct': (r) => r.headers['Content-Type'].includes('application/xml'),
    });
    errorRate.add(!success);
  }

  console.log('All tests completed');
}
