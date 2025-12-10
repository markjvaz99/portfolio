# services/api/app/crud/document.py
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.document import Document, DocumentStatus
from uuid import UUID

async def create_document(db: AsyncSession, filename: str, uploaded_by: str):
    doc = Document(filename=filename, uploaded_by=uploaded_by, status=DocumentStatus.uploaded)
    db.add(doc)
    await db.commit()
    await db.refresh(doc)
    return doc

async def set_s3_key(db: AsyncSession, doc_id: UUID, s3_key: str):
    q = await db.execute(select(Document).where(Document.id == doc_id))
    doc = q.scalar_one_or_none()
    if not doc:
        return None
    doc.s3_key = s3_key
    await db.commit()
    await db.refresh(doc)
    return doc

async def update_status(db: AsyncSession, doc_id: UUID, status: DocumentStatus):
    q = await db.execute(select(Document).where(Document.id == doc_id))
    doc = q.scalar_one_or_none()
    if not doc:
        return None
    doc.status = status
    await db.commit()
    await db.refresh(doc)
    return doc

async def set_extracted_text(db: AsyncSession, doc_id: UUID, text: str):
    q = await db.execute(select(Document).where(Document.id == doc_id))
    doc = q.scalar_one_or_none()
    if not doc:
        return None
    doc.extracted_text = text
    doc.status = DocumentStatus.ready
    await db.commit()
    await db.refresh(doc)
    return doc
