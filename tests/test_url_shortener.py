import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the URL Shortener API"}

def test_create_url():
    response = client.post("/urls/", json={"original_url": "https://nation.africa"})
    assert response.status_code == 200
    data = response.json()
    assert "short_url" in data
    assert data["original_url"] == "https://nation.africa"
