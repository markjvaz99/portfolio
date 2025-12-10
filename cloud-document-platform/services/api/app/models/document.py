# services/api/app/models/document.py
import enum
import uuid
from sqlalchemy import Column, String, Text, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func

from app.db.base import Base

class DocumentStatus(str, enum.Enum):
    uploaded = "uploaded"
    processing = "processing"
    ready = "ready"
    failed = "failed"

class Document(Base):
    __tablename__ = "documents"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String, nullable=False)
    s3_key = Column(String, nullable=True, unique=True)
    uploaded_by = Column(String, nullable=False)
    status = Column(Enum(DocumentStatus), default=DocumentStatus.uploaded, nullable=False)
    extracted_text = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
