class TestResponseFormats:
    """Test response format endpoints"""

    def test_json_response(self, client):
        """Test JSON response"""
        response = client.get("/json")
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("application/json")
        data = response.json()
        assert "slideshow" in data
        assert data["slideshow"]["author"] == "Yours Truly"

    def test_html_response(self, client):
        """Test HTML response"""
        response = client.get("/html")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "<!DOCTYPE html>" in response.text
        assert "<title>httpbin - HTML Response</title>" in response.text

    def test_xml_response(self, client):
        """Test XML response"""
        response = client.get("/xml")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/xml"
        assert '<?xml version="1.0"' in response.text
        assert "<slideshow>" in response.text

    def test_robots_txt(self, client):
        """Test robots.txt"""
        response = client.get("/robots.txt")
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/plain; charset=utf-8"
        assert "User-agent: *" in response.text
        assert "Disallow: /deny" in response.text
