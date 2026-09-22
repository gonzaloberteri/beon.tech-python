from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Message(BaseModel):
    text: str


@app.post("/messages")
def create_message(message: Message) -> dict:
    return {"received": message.text}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
