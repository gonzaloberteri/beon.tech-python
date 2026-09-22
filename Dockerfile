FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY main.py docs.html ./
CMD ["uv", "run", "--no-sync", "uvicorn", "main:app", "--host", "0.0.0.0"]
