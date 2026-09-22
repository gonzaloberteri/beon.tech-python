import json
import os
from contextlib import asynccontextmanager

import httpx
import psycopg
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

KNOWLEDGE_BASE = [
    "BEON.tech mission is to place the brightest tech talent in the most disruptive and innovative U.S. companies.",
    "BEON.tech offer IT staff augmentation services for every modern tech need, from backend and frontend to AI, machine learning, DevOps and QA.",
    "At BEON.tech, building software means far more than just filling roles — it's about creating strong relationships, empowering careers and helping people grow.",
]

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2:3b")
TOP_K = int(os.getenv("TOP_K", "2"))

SYSTEM_PROMPT = """You are BEON.tech's assistant. Answer the user's question using ONLY the context below.
Rules:
- Answer in one or two short sentences.
- Do not add facts that are not in the context.
- If the context does not contain the answer, reply exactly: "I don't know based on the available information."

Context:
{context}"""


def embed(text: str) -> str:
    r = httpx.post(f"{OLLAMA_URL}/api/embed", json={"model": EMBED_MODEL, "input": text}, timeout=60)
    r.raise_for_status()
    return json.dumps(r.json()["embeddings"][0])  # pgvector accepts '[x, y, ...]' text


def generate(question: str, context: list[str]) -> str:
    r = httpx.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": LLM_MODEL,
            "stream": False,
            "options": {"temperature": 0},
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT.format(context="\n".join(f"- {s}" for s in context))},
                {"role": "user", "content": question},
            ],
        },
        timeout=120,
    )
    r.raise_for_status()
    return r.json()["message"]["content"].strip()


@asynccontextmanager
async def lifespan(_: FastAPI):
    # ponytail: KB is 3 static sentences, so rebuild the table on every boot; switch to a migration + upsert when it grows.
    vectors = [embed(s) for s in KNOWLEDGE_BASE]
    dim = len(json.loads(vectors[0]))
    with psycopg.connect(DATABASE_URL) as conn:
        conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        conn.execute("DROP TABLE IF EXISTS snippets")
        conn.execute(f"CREATE TABLE snippets (id serial PRIMARY KEY, text text NOT NULL, embedding vector({dim}) NOT NULL)")
        conn.cursor().executemany("INSERT INTO snippets (text, embedding) VALUES (%s, %s)", zip(KNOWLEDGE_BASE, vectors))
    yield


app = FastAPI(title="BEON.tech RAG", docs_url=None, lifespan=lifespan)


class Question(BaseModel):
    question: str = "What is BEON.tech's mission?"


class Answer(BaseModel):
    question: str
    answer: str
    sources: list[str]


@app.post("/ask")
def ask(body: Question) -> Answer:
    with psycopg.connect(DATABASE_URL) as conn:
        rows = conn.execute(
            "SELECT text FROM snippets ORDER BY embedding <=> %s::vector LIMIT %s", (embed(body.question), TOP_K)
        ).fetchall()
    sources = [text for (text,) in rows]
    return Answer(question=body.question, answer=generate(body.question, sources), sources=sources)


@app.get("/docs", include_in_schema=False)
def docs() -> FileResponse:
    return FileResponse("docs.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
