from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from app.models.user import SubscriptionTier

class SubscriptionBase(BaseModel):
    subscription_tier: SubscriptionTier
    custom_token_limit: Optional[int] = None

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(SubscriptionBase):
    pass

class UsageStatsBase(BaseModel):
    feature: str
    tokens_used: int
    success: bool = True
    error_message: Optional[str] = None

class UsageStatsCreate(UsageStatsBase):
    user_id: int
    timestamp: datetime = datetime.utcnow()

class UsageStats(UsageStatsBase):
    id: int
    user_id: int
    timestamp: datetime

    class Config:
        orm_mode = True

class SubscriptionInfo(BaseModel):
    user_id: int
    email: str
    subscription_tier: SubscriptionTier
    custom_token_limit: Optional[int]
    tier_info: dict

    class Config:
        orm_mode = True

class UsageStatsPeriod(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
