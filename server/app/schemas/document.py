from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any

class DocumentBase(BaseModel):
    """Base document schema with shared attributes."""
    title: str
    content: Optional[str] = None
    document_type: str
    document_metadata: Dict[str, Any] = {}

class DocumentCreate(DocumentBase):
    """Schema for creating a new document."""
    pass

class DocumentUpdate(BaseModel):
    """Schema for updating a document."""
    title: Optional[str] = None
    content: Optional[str] = None
    document_type: Optional[str] = None
    document_metadata: Optional[Dict[str, Any]] = None
    current_version: Optional[int] = None

class Document(DocumentBase):
    """Schema for document responses."""
    id: int
    user_id: int
    current_version: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ReferenceBase(BaseModel):
    """Base reference schema with shared attributes."""
    citation_key: str
    title: str
    authors: List[str]
    year: int
    source: str
    reference_metadata: Dict[str, Any] = {}

class ReferenceCreate(ReferenceBase):
    """Schema for creating a new reference."""
    document_id: int

class ReferenceUpdate(BaseModel):
    """Schema for updating a reference."""
    citation_key: Optional[str] = None
    title: Optional[str] = None
    authors: Optional[List[str]] = None
    year: Optional[int] = None
    source: Optional[str] = None
    reference_metadata: Optional[Dict[str, Any]] = None

class Reference(ReferenceBase):
    """Schema for reference responses."""
    id: int
    document_id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
