from fastapi.testclient import TestClient

from src.api import app

client = TestClient(app)


def test_hello_world():
    payload = {"text": "test message"}
    response = client.post("/api/v1/messages", json=payload)

    assert response.status_code == 200
    assert response.json() == {"text": "# TODO: implement rag!!!"}
