from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root_default():
    r = client.post("/", json={})
    assert r.status_code == 200
    assert r.json() == {"message": "Hello, BEON.tech!"}


def test_root_name():
    r = client.post("/", json={"name": "Gonza"})
    assert r.json() == {"message": "Hello, Gonza!"}
