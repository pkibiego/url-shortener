import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200

def test_create_url():
    response = client.post("/api/shorten/", json={"original_url": "https://nation.africa"})
    assert response.status_code == 200
    data = response.json()
    assert "short_url" in data
    assert data["original_url"] == "https://nation.africa"

def test_create_url_invalid_url():
    response = client.post("/api/shorten/", json={"original_url": "invalid-url"})
    assert response.status_code == 400  # or whatever error code you're using for validation errors
    assert "detail" in response.json()

def test_create_url_missing_original_url():
    response = client.post("/api/shorten/", json={})
    assert response.status_code == 422  # This is the typical status code for validation issues
    assert "detail" in response.json()

def test_redirect_url():
    # Assuming the short URL is something like "/short/abc123"
    response = client.get("/soVQDZ")
    assert response.status_code == 200  # 302 is the HTTP status code for redirection
    # assert response.headers["Location"] == "https://nation.africa/kenya"  # The original URL

def test_create_url_duplicate_short_url():
    # First URL creation
    response = client.post("/api/shorten/", json={"original_url": "https://nation.africa"})
    assert response.status_code == 200
    data_1 = response.json()
    short_url_1 = data_1["short_url"]

    # Second URL creation (should not generate the same short_url)
    response = client.post("/api/shorten/", json={"original_url": "https://nation.africa"})
    assert response.status_code == 200
    data_2 = response.json()
    short_url_2 = data_2["short_url"]

    assert short_url_1 != short_url_2  # Ensure the short URLs are different

def test_create_url_invalid_json():
    response = client.post("/api/shorten/", data="invalid_json")
    assert response.status_code == 422  # Bad Request
    assert "detail" in response.json()

def test_create_url_no_original_url():
    response = client.post("/api/shorten/", json={"not_original_url": "https://nation.africa"})
    assert response.status_code == 422  # Unprocessable Entity due to missing `original_url`
    assert "detail" in response.json()

def test_create_url_long_url():
    long_url = "https://" + "a" * 1000 + ".com"
    response = client.post("/api/shorten/", json={"original_url": long_url})
    assert response.status_code == 400  # Or your expected error code
    assert "detail" in response.json()

def test_create_url_empty_url():
    response = client.post("/api/shorten/", json={"original_url": ""})
    assert response.status_code == 400  # Or your expected error code for empty URL
    assert "detail" in response.json()


