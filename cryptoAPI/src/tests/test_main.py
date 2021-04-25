from fastapi.testclient import TestClient

from cryptoAPI.src.main import app

client = TestClient(app)

# I wanted to test code and write frontend but i have problem with relative/absolute paths and terminal

def test_endpoints():
    response = client.get("/symmetric/key")
    assert response.status_code == 200
