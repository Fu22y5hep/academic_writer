from sqlalchemy import Boolean, Column, Integer, String, DateTime, JSON, Enum
import enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.base import Base

class SubscriptionTier(str, enum.Enum):
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"
    UNLIMITED = "unlimited"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    subscription_tier = Column(
        Enum(SubscriptionTier),
        default=SubscriptionTier.FREE
    )
    custom_token_limit = Column(Integer, nullable=True)  # For special cases
    preferences = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    documents = relationship("Document", back_populates="user")
    references = relationship("Reference", back_populates="user")
    document_versions = relationship("DocumentVersion", back_populates="user")
    collaborations = relationship("DocumentCollaboration", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    usage_stats = relationship("UsageStats", back_populates="user")
