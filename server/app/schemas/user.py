from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Dict, Any
from app.models.user import SubscriptionTier

class UserBase(BaseModel):
    """Base user schema with shared attributes."""
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str

class UserUpdate(BaseModel):
    """Schema for updating user information."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    subscription_tier: Optional[SubscriptionTier] = None
    preferences: Optional[Dict[str, Any]] = None

class User(UserBase):
    """Schema for user responses."""
    id: int
    is_active: bool
    created_at: datetime
    subscription_tier: SubscriptionTier = SubscriptionTier.FREE
    preferences: Dict[str, Any] = {}
    custom_token_limit: Optional[int] = None

    class Config:
        from_attributes = True
