from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="ServiceMind")


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return {"message": "ServiceMind API is running."}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):
    return {
        "message": f"ServiceMind received: {request.message}"
    }