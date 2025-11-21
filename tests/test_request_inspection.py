class TestRequestInspection:
    """Test request inspection endpoints"""

    def test_headers(self, client):
        """Test headers endpoint"""
        custom_headers = {
            "X-Custom-Header": "test-value",
            "User-Agent": "pytest-client"
        }
        response = client.get("/headers", headers=custom_headers)
        assert response.status_code == 200
        data = response.json()
        assert "headers" in data
        headers = data["headers"]
        assert headers["x-custom-header"] == "test-value"
        assert headers["user-agent"] == "pytest-client"

    def test_ip(self, client):
        """Test IP endpoint"""
        response = client.get("/ip")
        assert response.status_code == 200
        data = response.json()
        assert "origin" in data
        assert isinstance(data["origin"], str)

    def test_user_agent(self, client):
        """Test user-agent endpoint"""
        custom_ua = "Custom-Test-Agent/1.0"
        response = client.get("/user-agent", headers={"User-Agent": custom_ua})
        assert response.status_code == 200
        data = response.json()
        assert data["user-agent"] == custom_ua

    def test_user_agent_default(self, client):
        """Test user-agent endpoint with default UA"""
        response = client.get("/user-agent")
        assert response.status_code == 200
        data = response.json()
        assert "user-agent" in data
