# beon.tech-python

```sh
uv sync                    # creates .venv and installs deps
uv run fastapi dev main.py # http://127.0.0.1:8000/docs
uv run pytest              # tests
```

```sh
curl -X POST localhost:8000/messages -H 'content-type: application/json' -d '{"text":"hola"}'
```
