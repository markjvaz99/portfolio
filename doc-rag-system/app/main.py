from fastapi import FastAPI
from app.api.v1 import api_router
from contextlib import asynccontextmanager
from app.services.ingestion_service import ingest

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    ingest()
    
    yield
    # Shutdown logic
    print("Shutdown: Close connections")

app = FastAPI(lifespan=lifespan)

app.include_router(api_router, prefix="/api/v1")