from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_message():
    r = client.post("/messages", json={"text": "hola"})
    assert r.status_code == 200
    assert r.json() == {"received": "hola"}
