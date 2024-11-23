from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel

class DocumentVersionBase(BaseModel):
    content: str
    commit_message: str
    metadata: Dict[str, Any] = {}

class DocumentVersionCreate(DocumentVersionBase):
    pass

class DocumentVersionUpdate(DocumentVersionBase):
    content: Optional[str] = None
    commit_message: Optional[str] = None

class DocumentVersion(DocumentVersionBase):
    id: int
    document_id: int
    version_num: int
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True
