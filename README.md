# beon.tech-python

RAG service: FastAPI + Postgres/pgvector + Ollama (local, no API key).

```sh
docker compose up -d --build   # first run pulls models (~2.3 GB)
uv run pytest                  # e2e tests against http://localhost:8000
```

```sh
curl -X POST localhost:8000/ask -H 'content-type: application/json' -d '{"question":"What services does BEON.tech offer?"}'
```

Docs at http://localhost:8000/docs. Models are configurable via `EMBED_MODEL` / `LLM_MODEL` (any Ollama model).
