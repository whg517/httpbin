import pytest
from fastapi.testclient import TestClient

from httpbin.main import app


@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)
