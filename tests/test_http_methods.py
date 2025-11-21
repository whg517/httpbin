import pytest


class TestHTTPMethods:
    """Test HTTP method endpoints"""

    def test_get_method(self, client):
        """Test GET endpoint"""
        response = client.get("/get?foo=bar&test=123")
        assert response.status_code == 200
        data = response.json()
        assert data["method"] == "GET"
        assert data["args"] == {"foo": "bar", "test": "123"}
        assert "headers" in data
        assert data["url"].endswith("/get?foo=bar&test=123")

    def test_post_method_json(self, client):
        """Test POST endpoint with JSON"""
        payload = {"name": "test", "value": 123}
        response = client.post("/post", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["method"] == "POST"
        assert data["json"] == payload
        assert data["headers"]["content-type"] == "application/json"

    def test_post_method_form(self, client):
        """Test POST endpoint with form data"""
        form_data = {"key": "value", "foo": "bar"}
        response = client.post("/post", data=form_data)
        assert response.status_code == 200
        data = response.json()
        assert data["method"] == "POST"
        assert data["form"] == form_data

    def test_put_method(self, client):
        """Test PUT endpoint"""
        payload = {"update": "data"}
        response = client.put("/put", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["method"] == "PUT"
        assert data["json"] == payload

    def test_patch_method(self, client):
        """Test PATCH endpoint"""
        payload = {"patch": "field"}
        response = client.patch("/patch", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["method"] == "PATCH"
        assert data["json"] == payload

    def test_delete_method(self, client):
        """Test DELETE endpoint"""
        response = client.delete("/delete")
        assert response.status_code == 200
        data = response.json()
        assert data["method"] == "DELETE"
        assert "headers" in data
