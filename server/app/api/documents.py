from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.models.document import Document, Reference
from app.models.version import DocumentVersion
from app.schemas.document import (
    Document as DocumentSchema,
    DocumentCreate,
    DocumentUpdate,
    Reference as ReferenceSchema,
    ReferenceCreate,
    ReferenceUpdate,
)
from app.schemas.version import DocumentVersion as VersionSchema, DocumentVersionCreate

router = APIRouter()

@router.get("/", response_model=List[DocumentSchema])
def get_documents(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Retrieve user's documents.
    """
    return db.query(Document).filter(
        Document.user_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.post("/", response_model=DocumentSchema)
def create_document(
    document_in: DocumentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Create new document.
    """
    document = Document(
        **document_in.dict(),
        user_id=current_user.id
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document

@router.get("/{document_id}", response_model=DocumentSchema)
def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get document by ID.
    """
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@router.put("/{document_id}", response_model=DocumentSchema)
def update_document(
    document_id: int,
    document_in: DocumentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Update document and create a new version.
    """
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Create a new version before updating
    if document_in.content is not None and document_in.content != document.content:
        version = DocumentVersion(
            document_id=document.id,
            content=document.content,
            version_num=document.current_version,
            commit_message=document_in.metadata.get("commit_message", "Update document"),
            created_by=current_user.id
        )
        db.add(version)
        document.current_version += 1
    
    # Update document
    for field, value in document_in.dict(exclude_unset=True).items():
        setattr(document, field, value)
    
    db.add(document)
    db.commit()
    db.refresh(document)
    return document

@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Delete document.
    """
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    db.delete(document)
    db.commit()
    return {"status": "success"}

# Reference endpoints
@router.post("/{document_id}/references", response_model=ReferenceSchema)
def create_reference(
    document_id: int,
    reference_in: ReferenceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Create new reference for document.
    """
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    reference = Reference(
        **reference_in.dict(),
        document_id=document_id,
        user_id=current_user.id
    )
    db.add(reference)
    db.commit()
    db.refresh(reference)
    return reference

@router.get("/{document_id}/references", response_model=List[ReferenceSchema])
def get_references(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get all references for a document.
    """
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return document.references

# Version management endpoints
@router.get("/{document_id}/versions", response_model=List[VersionSchema])
def get_document_versions(
    document_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get document version history.
    """
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return db.query(DocumentVersion).filter(
        DocumentVersion.document_id == document_id
    ).order_by(DocumentVersion.version_num.desc()).offset(skip).limit(limit).all()

@router.get("/{document_id}/versions/{version_num}", response_model=VersionSchema)
def get_document_version(
    document_id: int,
    version_num: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get specific document version.
    """
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    version = db.query(DocumentVersion).filter(
        DocumentVersion.document_id == document_id,
        DocumentVersion.version_num == version_num
    ).first()
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")
    
    return version

@router.post("/{document_id}/versions/restore/{version_num}", response_model=DocumentSchema)
def restore_document_version(
    document_id: int,
    version_num: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Restore document to a specific version.
    """
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    version = db.query(DocumentVersion).filter(
        DocumentVersion.document_id == document_id,
        DocumentVersion.version_num == version_num
    ).first()
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")
    
    # Create a new version of the current state before restoring
    current_version = DocumentVersion(
        document_id=document.id,
        content=document.content,
        version_num=document.current_version,
        commit_message=f"Auto-save before restoring to version {version_num}",
        created_by=current_user.id
    )
    db.add(current_version)
    
    # Update document with version content
    document.content = version.content
    document.current_version += 1
    
    db.add(document)
    db.commit()
    db.refresh(document)
    return document
