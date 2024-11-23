from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class ReferenceBase(BaseModel):
    citation_key: str
    title: str
    authors: List[str]
    year: int
    source: str
    metadata: Dict[str, Any] = {}

class ReferenceCreate(ReferenceBase):
    pass

class ReferenceUpdate(ReferenceBase):
    citation_key: Optional[str] = None
    title: Optional[str] = None
    authors: Optional[List[str]] = None
    year: Optional[int] = None
    source: Optional[str] = None

class Reference(ReferenceBase):
    id: int
    document_id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class DocumentBase(BaseModel):
    title: str
    content: str
    document_type: str
    metadata: Dict[str, Any] = {}

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(DocumentBase):
    title: Optional[str] = None
    content: Optional[str] = None
    document_type: Optional[str] = None

class Document(DocumentBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    references: List[Reference] = []

    class Config:
        from_attributes = True
