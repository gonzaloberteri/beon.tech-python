from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class HelloRequest(BaseModel):
    name: str = "World"


@app.post("/")
def hello(body: HelloRequest) -> dict:
    return {"message": f"Hello, {body.name}!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
