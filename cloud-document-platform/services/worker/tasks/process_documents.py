# services/worker/tasks/process_document.py
from services.worker.worker import celery
import boto3
import tempfile
import os
from app.core.config import settings
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models.document import DocumentStatus, Document
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine
import time
import io

# NOTE: worker uses sync DB session for simplicity (psycopg2)
DB_URL_SYNC = os.environ.get("DATABASE_URL", "postgresql://app:password@postgres:5432/appdb")
S3_BUCKET = os.environ.get("S3_BUCKET", settings.s3_bucket)

engine = create_engine(DB_URL_SYNC)
SessionLocal = sessionmaker(bind=engine)

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", None),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", None),
    region_name=os.environ.get("AWS_REGION", "us-east-1"),
)

@celery.task(name="process_document")
def process_document(doc_id: str, s3_key: str):
    """
    1) mark processing
    2) download file from s3
    3) extract text (very simple)
    4) save extracted_text and set status ready
    """
    session = SessionLocal()
    try:
        # step 1: mark processing
        stmt = text("UPDATE documents SET status = :status WHERE id::text = :id")
        session.execute(stmt, {"status": DocumentStatus.processing.value, "id": doc_id})
        session.commit()

        # step 2: download file
        tmp = io.BytesIO()
        s3.download_fileobj(Bucket=S3_BUCKET, Key=s3_key, Fileobj=tmp)
        tmp.seek(0)
        # rudimentary extraction:
        extracted = extract_text_from_bytes(tmp.getvalue(), s3_key)

        # step 4: save text
        stmt2 = text("UPDATE documents SET extracted_text = :txt, status = :status WHERE id::text = :id")
        session.execute(stmt2, {"txt": extracted, "status": DocumentStatus.ready.value, "id": doc_id})
        session.commit()
    except Exception as exc:
        session.rollback()
        stmt3 = text("UPDATE documents SET status = :status WHERE id::text = :id")
        session.execute(stmt3, {"status": DocumentStatus.failed.value, "id": doc_id})
        session.commit()
        raise
    finally:
        session.close()

def extract_text_from_bytes(content_bytes: bytes, key: str) -> str:
    # VERY simple: if PDF use pdfminer, else return byte-ish string
    try:
        from pdfminer.high_level import extract_text_to_fp
        out = io.StringIO()
        fp = io.BytesIO(content_bytes)
        extract_text_to_fp(fp, out)
        text = out.getvalue()
        if text.strip():
            return text
    except Exception:
        pass
    # fallback
    return f"[binary content, key={key}, size={len(content_bytes)} bytes]"
