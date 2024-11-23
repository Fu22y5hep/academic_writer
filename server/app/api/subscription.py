from typing import Any, List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.models.user import User, SubscriptionTier
from app.schemas.subscription import (
    SubscriptionInfo,
    SubscriptionUpdate,
    UsageStats,
    UsageStatsPeriod
)
from app.services.subscription_service import subscription_service

router = APIRouter()

@router.get("/info", response_model=SubscriptionInfo)
async def get_subscription_info(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get current user's subscription information.
    """
    return await subscription_service.get_subscription_info(current_user)

@router.put("/update", response_model=SubscriptionInfo)
async def update_subscription(
    subscription: SubscriptionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update user's subscription tier.
    """
    return await subscription_service.update_subscription(
        db,
        current_user,
        subscription.subscription_tier,
        subscription.custom_token_limit
    )

@router.get("/usage", response_model=dict)
async def get_usage_stats(
    period: UsageStatsPeriod,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get usage statistics for the current user.
    """
    return await subscription_service.get_usage_stats(
        db,
        current_user,
        period.start_date,
        period.end_date
    )

@router.get("/upgrades")
async def get_upgrade_options(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get available subscription upgrade options.
    """
    return await subscription_service.get_available_upgrades(current_user)

@router.get("/features")
async def get_feature_access(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get feature access information for current subscription tier.
    """
    from app.core.subscription import SubscriptionConfig
    return {
        "subscription_tier": current_user.subscription_tier,
        "features": SubscriptionConfig.get_tier_features(current_user.subscription_tier)
    }

@router.get("/tiers")
async def get_subscription_tiers() -> Any:
    """
    Get information about all subscription tiers.
    """
    from app.core.subscription import SubscriptionConfig
    tiers = {}
    for tier in SubscriptionTier:
        tiers[tier.value] = SubscriptionConfig.get_tier_info(tier)
    return tiers
