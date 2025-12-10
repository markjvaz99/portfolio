# services/api/app/api/v1/documents.py
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from sqlalchemy.future import select
from uuid import UUID
from app.crud import document
from app.utils.s3 import upload_fileobj_to_s3
from app.tasks.enqueue import enqueue_document_processing
from app.models.document import Document
from app.schemas.document import DocumentRead

router = APIRouter()

@router.post("/upload", response_model=dict)
async def upload_document(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="filename required")
    # create db record
    doc = await document.create_document(db, filename=file.filename, uploaded_by="test@example.com")
    s3_key = f"{doc.id}/{file.filename}"
    # Upload to S3 (file.file is SpooledTemporaryFile / file-like)
    await upload_fileobj_to_s3(file.file, key=s3_key)
    await document.set_s3_key(db, doc.id, s3_key)
    # enqueue background job
    enqueue_document_processing(str(doc.id), s3_key)
    return {"id": str(doc.id), "status": doc.status.value}

@router.get("/{doc_id}", response_model=DocumentRead)
async def get_document(doc_id: str, db: AsyncSession = Depends(get_db)):
    # Convert doc_id string to UUID
    try:
        doc_uuid = UUID(doc_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID")

    # Query the document
    result = await db.execute(select(Document).where(Document.id == doc_uuid))
    doc = result.scalar_one_or_none()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    return doc