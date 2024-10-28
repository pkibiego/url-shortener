import sys
import os
import pytest
from fastapi.testclient import TestClient

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app  # Absolute import

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
