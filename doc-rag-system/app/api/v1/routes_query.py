from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.query import QueryRequest
from app.config import *
from app.services.ingestion_service import ingest
from app.services.file_ingestion_service import ingest_files
from app.utils.logger import get_logger
import time
import uuid
from app.services.rag_service import run_rag_pipeline, run_rag_pipeline_stream
from fastapi.responses import StreamingResponse
from typing import List

logger = get_logger(__name__)

router = APIRouter()

@router.get("/ingest")
def query():
    return {"response": ingest()}

@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    try:
        result = await ingest_files(files)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.post("/test-rag-stream")
def test_rag_stream(request: QueryRequest):

    def token_generator():
        for token in run_rag_pipeline_stream(request.query):
            yield token

    return StreamingResponse(token_generator(), media_type="text/plain")


@router.post("/test-rag")
def test_rag(request: QueryRequest):
    request_id = str(uuid.uuid4())
    logger.info(f"[{request_id}] Incoming query: {request.query}")

    try:
        start_time = time.time()

        answer, sources = run_rag_pipeline(
            query=request.query,
            logger=logger,
            request_id=request_id
        )

        total_time = time.time() - start_time
        logger.info(f"[{request_id}] Total time: {total_time:.2f}s")

        return {
            "request_id": request_id,
            "query": request.query,
            "answer": answer,
            "sources": sources
        }

    except Exception as e:
        logger.error(f"[{request_id}] Error: {str(e)}", exc_info=True)
        return {
            "request_id": request_id,
            "error": str(e)
        }
