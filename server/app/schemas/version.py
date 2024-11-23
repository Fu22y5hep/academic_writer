from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class DocumentVersionBase(BaseModel):
    """Base document version schema with shared attributes."""
    title: str
    content: str
    version_number: int
    version_metadata: Dict[str, Any] = {}

class DocumentVersionCreate(DocumentVersionBase):
    """Schema for creating a new document version."""
    document_id: int

class DocumentVersionUpdate(BaseModel):
    """Schema for updating a document version."""
    title: Optional[str] = None
    content: Optional[str] = None
    version_number: Optional[int] = None
    version_metadata: Optional[Dict[str, Any]] = None

class DocumentVersion(DocumentVersionBase):
    """Schema for document version responses."""
    id: int
    document_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
