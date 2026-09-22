from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()


class HelloRequest(BaseModel):
    name: str = "BEON.tech"


@app.post("/")
def hello(body: HelloRequest) -> dict:
    return {"message": f"Hello, {body.name}!"}


@app.get("/scalar", include_in_schema=False)
def scalar_docs() -> HTMLResponse:
    return HTMLResponse("""
        <div id="app"></div>
        <script src="https://cdn.jsdelivr.net/npm/@scalar/api-reference"></script>
        <script>Scalar.createApiReference("#app", {url: "/openapi.json"})</script>
    """)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
