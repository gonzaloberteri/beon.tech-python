from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_hello_default():
    r = client.post("/hello", json={})
    assert r.status_code == 200
    assert r.json() == {"message": "Hello, World!"}


def test_hello_name():
    r = client.post("/hello", json={"name": "Gonza"})
    assert r.json() == {"message": "Hello, Gonza!"}
