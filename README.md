# beon.tech-python

```sh
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/fastapi dev main.py     # http://127.0.0.1:8000/docs
.venv/bin/python -m pytest        # tests
```

```sh
curl -X POST localhost:8000/messages -H 'content-type: application/json' -d '{"text":"hola"}'
```
