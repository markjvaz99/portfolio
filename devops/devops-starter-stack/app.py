from fastapi import FastAPI
import os


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": os.environ.get("MESSAGE", "Hello from FastAPI running in Docker & Kubernetes!")}


@app.get("/health")
def health():
    return {"status": "ok"}