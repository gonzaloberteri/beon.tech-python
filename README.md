<p align="center">
  <a href="https://beon.tech"><img src="assets/beon-logo.svg" alt="BEON.tech" width="80"></a>
</p>
<h1 align="center"><a href="https://beon.tech">BEON.tech</a> RAG service</h1>

Answers questions about [BEON.tech](https://beon.tech) from a small knowledge base. FastAPI + Postgres/pgvector + Ollama (local, no API key).

```sh
docker compose up -d --build   # first run pulls ~2.3 GB of models
uv run pytest                  # e2e tests against http://localhost:8000
```

```sh
curl -X POST localhost:8000/ask -H 'content-type: application/json' -d '{"question":"What services does BEON.tech offer?"}'
```

Docs at http://localhost:8000/docs. Models are configurable via `EMBED_MODEL` / `LLM_MODEL` (any Ollama model).
