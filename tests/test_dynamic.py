import time
import pytest


class TestDynamic:
    """Test dynamic behavior endpoints"""

    def test_delay(self, client):
        """Test delay endpoint"""
        start = time.time()
        response = client.get("/delay/2")
        elapsed = time.time() - start

        assert response.status_code == 200
        data = response.json()
        assert data["delay"] == 2
        assert data["requested"] == 2
        assert elapsed >= 2.0  # Should have delayed at least 2 seconds

    def test_delay_max_limit(self, client):
        """Test delay with value exceeding max"""
        response = client.get("/delay/15")
        assert response.status_code == 200
        data = response.json()
        assert data["delay"] == 10  # Should be capped at max
        assert data["requested"] == 15

    def test_delay_negative(self, client):
        """Test delay with negative value"""
        response = client.get("/delay/-1")
        assert response.status_code == 400

    def test_uuid(self, client):
        """Test UUID generation"""
        response = client.get("/uuid")
        assert response.status_code == 200
        data = response.json()
        assert "uuid" in data
        uuid_str = data["uuid"]
        # Basic UUID format check
        assert len(uuid_str) == 36
        assert uuid_str.count("-") == 4

    def test_base64_decode(self, client):
        """Test base64 decoding"""
        # "Hello World" in base64
        response = client.get("/base64/SGVsbG8gV29ybGQ=")
        assert response.status_code == 200
        data = response.json()
        assert data["decoded"] == "Hello World"
        assert data["original"] == "SGVsbG8gV29ybGQ="

    def test_base64_encode(self, client):
        """Test base64 encoding"""
        response = client.post("/base64/encode", json={"text": "Hello World"})
        assert response.status_code == 200
        data = response.json()
        assert data["encoded"] == "SGVsbG8gV29ybGQ="
        assert data["original"] == "Hello World"

    def test_base64_encode_missing_text(self, client):
        """Test base64 encoding without text"""
        response = client.post("/base64/encode", json={})
        assert response.status_code == 400

    def test_random_bytes(self, client):
        """Test random bytes generation"""
        n = 100
        response = client.get(f"/bytes/{n}")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/octet-stream"
        assert len(response.content) == n

    def test_random_bytes_limits(self, client):
        """Test random bytes with invalid size"""
        response = client.get("/bytes/0")
        assert response.status_code == 400

        response = client.get("/bytes/200000")  # Too large
        assert response.status_code == 400
