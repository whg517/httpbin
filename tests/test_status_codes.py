import pytest


class TestStatusCodes:
    """Test status code endpoints"""

    @pytest.mark.parametrize("status_code", [200, 201, 204, 301, 302, 400, 401, 403, 404, 500, 502])
    def test_status_code(self, client, status_code):
        """Test various status codes"""
        response = client.get(f"/status/{status_code}")
        assert response.status_code == status_code
        if status_code != 204:  # 204 has no content
            data = response.json()
            assert data["code"] == status_code

    def test_multiple_status_codes(self, client):
        """Test comma-separated status codes (returns first)"""
        response = client.get("/status/404,500")
        assert response.status_code == 404
        data = response.json()
        assert data["code"] == 404

    def test_invalid_status_code(self, client):
        """Test invalid status code"""
        response = client.get("/status/abc")
        assert response.status_code == 400
        data = response.json()
        assert data["code"] == 400

    def test_status_code_out_of_range(self, client):
        """Test status code out of range"""
        response = client.get("/status/999")
        assert response.status_code == 400
