from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.models.collaboration import CollaborationRole

class CollaborationBase(BaseModel):
    role: CollaborationRole

class CollaborationCreate(CollaborationBase):
    user_id: int

class CollaborationUpdate(CollaborationBase):
    role: Optional[CollaborationRole] = None

class Collaboration(CollaborationBase):
    id: int
    document_id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CommentBase(BaseModel):
    content: str
    parent_id: Optional[int] = None

class CommentCreate(CommentBase):
    pass

class CommentUpdate(BaseModel):
    content: Optional[str] = None
    resolved: Optional[bool] = None

class Comment(CommentBase):
    id: int
    document_id: int
    user_id: int
    resolved: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    replies: List['Comment'] = []

    class Config:
        from_attributes = True

# Prevent circular reference issues
Comment.model_rebuild()
