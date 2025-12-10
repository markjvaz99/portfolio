# services/api/app/schemas/document.py
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.models.document import DocumentStatus

class DocumentCreate(BaseModel):
    filename: str

class DocumentRead(BaseModel):
    id: UUID
    filename: str
    status: DocumentStatus
    created_at: datetime

    class Config:
        orm_mode = True
