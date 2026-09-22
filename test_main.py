"""End-to-end tests: run against the real stack (`docker compose up -d`), then `uv run pytest`."""

import os

import httpx
import pytest

API_URL = os.getenv("API_URL", "http://localhost:8000")


@pytest.fixture(scope="module")
def client():
    c = httpx.Client(base_url=API_URL, timeout=180)
    try:
        c.get("/openapi.json").raise_for_status()
    except httpx.HTTPError:
        pytest.skip(f"API not reachable at {API_URL}; start it with `docker compose up -d`")
    return c


def test_answers_from_knowledge_base(client):
    r = client.post("/ask", json={"question": "What services does BEON.tech offer?"})
    assert r.status_code == 200
    body = r.json()
    assert set(body) == {"question", "answer", "sources"}
    assert "staff augmentation" in body["sources"][0]
    assert "staff augmentation" in body["answer"].lower()


def test_retrieves_most_relevant_snippet(client):
    r = client.post("/ask", json={"question": "What is the company's mission?"})
    assert "mission" in r.json()["sources"][0]


def test_refuses_out_of_context(client):
    r = client.post("/ask", json={"question": "What is the capital of France?"})
    assert "don't know" in r.json()["answer"].lower()


def test_validation(client):
    assert client.post("/ask", json={"question": 42}).status_code == 422


def test_retrieves_culture_snippet(client):
    r = client.post("/ask", json={"question": "Does BEON.tech care about career growth?"})
    assert "empowering careers" in r.json()["sources"][0]
