from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(docs_url=None)


class exampleRequest(BaseModel):
    name: str = "BEON.tech"


@app.post("/")
def root(body: exampleRequest) -> dict:
    return {"message": f"Hello, {body.name}!"}


@app.get("/docs", include_in_schema=False)
def docs() -> FileResponse:
    return FileResponse("docs.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
