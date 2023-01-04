from fastapi.testclient import TestClient

from ..server import app

client = TestClient(app)


def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}
