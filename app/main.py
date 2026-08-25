from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(title="ServiceMind")

app.include_router(router)


@app.get("/")
def root():
    return {"message": "ServiceMind API is running."}


@app.get("/health")
def health():
    return {"status": "ok"}