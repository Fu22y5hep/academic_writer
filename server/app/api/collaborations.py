from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.models.document import Document
from app.models.collaboration import DocumentCollaboration, Comment, CollaborationRole
from app.schemas.collaboration import (
    Collaboration as CollaborationSchema,
    CollaborationCreate,
    CollaborationUpdate,
    Comment as CommentSchema,
    CommentCreate,
    CommentUpdate,
)

router = APIRouter()

def check_document_access(
    document_id: int,
    user: User,
    db: Session,
    required_role: CollaborationRole = CollaborationRole.VIEWER
) -> Document:
    """
    Check if user has required access to document.
    """
    # Document owner has all permissions
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if document.user_id == user.id:
        return document
    
    # Check collaboration role
    collab = db.query(DocumentCollaboration).filter(
        DocumentCollaboration.document_id == document_id,
        DocumentCollaboration.user_id == user.id
    ).first()
    
    if not collab:
        raise HTTPException(
            status_code=403,
            detail="You don't have access to this document"
        )
    
    role_hierarchy = {
        CollaborationRole.OWNER: 4,
        CollaborationRole.EDITOR: 3,
        CollaborationRole.COMMENTER: 2,
        CollaborationRole.VIEWER: 1
    }
    
    if role_hierarchy[collab.role] < role_hierarchy[required_role]:
        raise HTTPException(
            status_code=403,
            detail=f"This action requires {required_role} access"
        )
    
    return document

@router.post("/documents/{document_id}/collaborators", response_model=CollaborationSchema)
def add_collaborator(
    document_id: int,
    collaboration_in: CollaborationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Add a collaborator to document.
    """
    document = check_document_access(
        document_id, current_user, db, CollaborationRole.OWNER
    )
    
    # Check if user exists
    user = db.query(User).filter(User.id == collaboration_in.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if collaboration already exists
    existing_collab = db.query(DocumentCollaboration).filter(
        DocumentCollaboration.document_id == document_id,
        DocumentCollaboration.user_id == collaboration_in.user_id
    ).first()
    if existing_collab:
        raise HTTPException(
            status_code=400,
            detail="User is already a collaborator"
        )
    
    collaboration = DocumentCollaboration(
        document_id=document_id,
        user_id=collaboration_in.user_id,
        role=collaboration_in.role
    )
    db.add(collaboration)
    db.commit()
    db.refresh(collaboration)
    return collaboration

@router.get("/documents/{document_id}/collaborators", response_model=List[CollaborationSchema])
def get_collaborators(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get document collaborators.
    """
    check_document_access(document_id, current_user, db)
    return db.query(DocumentCollaboration).filter(
        DocumentCollaboration.document_id == document_id
    ).all()

@router.put("/documents/{document_id}/collaborators/{user_id}", response_model=CollaborationSchema)
def update_collaborator(
    document_id: int,
    user_id: int,
    collaboration_in: CollaborationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Update collaborator role.
    """
    check_document_access(document_id, current_user, db, CollaborationRole.OWNER)
    
    collaboration = db.query(DocumentCollaboration).filter(
        DocumentCollaboration.document_id == document_id,
        DocumentCollaboration.user_id == user_id
    ).first()
    if not collaboration:
        raise HTTPException(status_code=404, detail="Collaborator not found")
    
    collaboration.role = collaboration_in.role
    db.add(collaboration)
    db.commit()
    db.refresh(collaboration)
    return collaboration

@router.delete("/documents/{document_id}/collaborators/{user_id}")
def remove_collaborator(
    document_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Remove collaborator from document.
    """
    check_document_access(document_id, current_user, db, CollaborationRole.OWNER)
    
    collaboration = db.query(DocumentCollaboration).filter(
        DocumentCollaboration.document_id == document_id,
        DocumentCollaboration.user_id == user_id
    ).first()
    if not collaboration:
        raise HTTPException(status_code=404, detail="Collaborator not found")
    
    db.delete(collaboration)
    db.commit()
    return {"status": "success"}

# Comment endpoints
@router.post("/documents/{document_id}/comments", response_model=CommentSchema)
def create_comment(
    document_id: int,
    comment_in: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Create new comment.
    """
    check_document_access(document_id, current_user, db, CollaborationRole.COMMENTER)
    
    if comment_in.parent_id:
        parent_comment = db.query(Comment).get(comment_in.parent_id)
        if not parent_comment or parent_comment.document_id != document_id:
            raise HTTPException(status_code=404, detail="Parent comment not found")
    
    comment = Comment(
        **comment_in.dict(),
        document_id=document_id,
        user_id=current_user.id
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

@router.get("/documents/{document_id}/comments", response_model=List[CommentSchema])
def get_comments(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get document comments.
    """
    check_document_access(document_id, current_user, db)
    return db.query(Comment).filter(
        Comment.document_id == document_id,
        Comment.parent_id.is_(None)  # Only get top-level comments
    ).all()

@router.put("/documents/{document_id}/comments/{comment_id}", response_model=CommentSchema)
def update_comment(
    document_id: int,
    comment_id: int,
    comment_in: CommentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Update comment.
    """
    check_document_access(document_id, current_user, db, CollaborationRole.COMMENTER)
    
    comment = db.query(Comment).filter(
        Comment.id == comment_id,
        Comment.document_id == document_id
    ).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if comment.user_id != current_user.id:
        check_document_access(document_id, current_user, db, CollaborationRole.EDITOR)
    
    for field, value in comment_in.dict(exclude_unset=True).items():
        setattr(comment, field, value)
    
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

@router.delete("/documents/{document_id}/comments/{comment_id}")
def delete_comment(
    document_id: int,
    comment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Delete comment.
    """
    check_document_access(document_id, current_user, db, CollaborationRole.COMMENTER)
    
    comment = db.query(Comment).filter(
        Comment.id == comment_id,
        Comment.document_id == document_id
    ).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if comment.user_id != current_user.id:
        check_document_access(document_id, current_user, db, CollaborationRole.EDITOR)
    
    db.delete(comment)
    db.commit()
    return {"status": "success"}
