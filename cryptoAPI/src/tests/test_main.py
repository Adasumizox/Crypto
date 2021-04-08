from fastapi.testclient import TestClient

from cryptoAPI.src.main import app

client = TestClient(app)


def test_endpoints():
    response = client.get("/symmetric/key")
    assert response.status_code == 200
