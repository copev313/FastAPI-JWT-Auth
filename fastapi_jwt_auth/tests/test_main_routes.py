"""
    Tests for the main API routes.
"""
from fastapi.testclient import TestClient

from fastapi_jwt_auth.main import app


client = TestClient(app)


def test_root_route():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_not_secret_data():
    response = client.get("/api/v1/notsecret-stuff")
    assert response.status_code == 200
    assert response.json() == {"message": "Not secret data..."}


def test_secret_data_unauthenticated():
    response = client.get("/api/v1/secret-stuff")
    assert response.status_code == 403
    assert response.json() == {
        "detail": "Not authenticated"
    }
