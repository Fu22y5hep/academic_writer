from sqlalchemy import Boolean, Column, Integer, String, DateTime, JSON, Enum
import enum
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func
from app.core.security import get_password_hash

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

    @validates('password')
    def _validate_password(self, key, password):
        """Hash password before storing."""
        return get_password_hash(password)

    def __init__(self, **kwargs):
        """Initialize user with password hashing."""
        if 'password' in kwargs:
            kwargs['hashed_password'] = get_password_hash(kwargs.pop('password'))
        super().__init__(**kwargs)
