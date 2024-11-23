from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    document_type = Column(String, index=True)  # e.g., "paper", "thesis", "notes"
    metadata = Column(JSON, default={})
    current_version = Column(Integer, default=1)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="documents")
    references = relationship("Reference", back_populates="document", cascade="all, delete-orphan")
    versions = relationship("DocumentVersion", back_populates="document", cascade="all, delete-orphan")

class Reference(Base):
    __tablename__ = "references"

    id = Column(Integer, primary_key=True, index=True)
    citation_key = Column(String, index=True)
    title = Column(String)
    authors = Column(JSON)  # List of authors
    year = Column(Integer)
    source = Column(String)  # e.g., "journal", "conference", "book"
    metadata = Column(JSON, default={})
    document_id = Column(Integer, ForeignKey("documents.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    document = relationship("Document", back_populates="references")
    user = relationship("User", back_populates="references")
