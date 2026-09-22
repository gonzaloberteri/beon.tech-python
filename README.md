# beon.tech-python

```sh
uv sync                    # creates .venv and installs deps
uv run main.py             # http://127.0.0.1:8000/docs
uv run pytest              # tests
```

```sh
curl -X POST localhost:8000/hello -H 'content-type: application/json' -d '{"name":"Gonza"}'
```
