from fastapi import APIRouter
from app.schemas.query import QueryRequest
from app.rag.pipeline import query_rag
from app.config import *
from app.services.ingestion_service import ingest
from app.utils.logger import get_logger
import time
import uuid
from app.services.rag_service import run_rag_pipeline

logger = get_logger(__name__)

router = APIRouter()

@router.get("/ingest")
def query(q: str):
    ingest()
    return {"response": "Ingested"}

@router.post("/test-rag")
def test_rag(request: QueryRequest):
    request_id = str(uuid.uuid4())
    logger.info(f"[{request_id}] Incoming query: {request.question}")

    try:
        start_time = time.time()

        answer, sources = run_rag_pipeline(
            query=request.question,
            logger=logger,
            request_id=request_id
        )

        total_time = time.time() - start_time
        logger.info(f"[{request_id}] Total time: {total_time:.2f}s")

        return {
            "request_id": request_id,
            "query": request.question,
            "answer": answer,
            "sources": sources
        }

    except Exception as e:
        logger.error(f"[{request_id}] Error: {str(e)}", exc_info=True)
        return {
            "request_id": request_id,
            "error": str(e)
        }
