from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(docs_url=None)


class exampleRequest(BaseModel):
    name: str = "BEON.tech"


@app.post("/")
def root(body: exampleRequest) -> dict:
    return {"message": f"Hello, {body.name}!"}


@app.get("/docs", include_in_schema=False)
def docs() -> HTMLResponse:
    return HTMLResponse("""
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@stoplight/elements/styles.min.css">
        <script src="https://cdn.jsdelivr.net/npm/@stoplight/elements/web-components.min.js"></script>
        <elements-api apiDescriptionUrl="/openapi.json" router="hash" layout="sidebar"></elements-api>
    """)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
