from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user import User, SubscriptionTier
from app.core.subscription import SubscriptionConfig
from app.schemas.subscription import SubscriptionCreate, SubscriptionUpdate

class SubscriptionService:
    @staticmethod
    async def get_subscription_info(user: User) -> Dict[str, Any]:
        """Get detailed subscription information for a user."""
        tier_info = SubscriptionConfig.get_tier_info(user.subscription_tier)
        return {
            "user_id": user.id,
            "email": user.email,
            "subscription_tier": user.subscription_tier,
            "custom_token_limit": user.custom_token_limit,
            "tier_info": tier_info
        }

    @staticmethod
    async def update_subscription(
        db: Session,
        user: User,
        new_tier: SubscriptionTier,
        custom_token_limit: Optional[int] = None
    ) -> User:
        """Update a user's subscription tier."""
        # Validate the new tier
        if new_tier not in SubscriptionTier:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid subscription tier: {new_tier}"
            )

        # Update user's subscription
        user.subscription_tier = new_tier
        if custom_token_limit is not None:
            user.custom_token_limit = custom_token_limit

        try:
            db.commit()
            db.refresh(user)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error updating subscription: {str(e)}"
            )

        return user

    @staticmethod
    async def get_usage_stats(
        db: Session,
        user: User,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get usage statistics for a user."""
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=30)
        if not end_date:
            end_date = datetime.utcnow()

        # Query usage statistics from the database
        usage_stats = db.query(UsageStats).filter(
            UsageStats.user_id == user.id,
            UsageStats.timestamp.between(start_date, end_date)
        ).all()

        # Aggregate statistics
        total_tokens = sum(stat.tokens_used for stat in usage_stats)
        total_requests = len(usage_stats)
        feature_usage = {}
        
        for stat in usage_stats:
            if stat.feature not in feature_usage:
                feature_usage[stat.feature] = {
                    "total_requests": 0,
                    "total_tokens": 0
                }
            feature_usage[stat.feature]["total_requests"] += 1
            feature_usage[stat.feature]["total_tokens"] += stat.tokens_used

        return {
            "period": {
                "start": start_date,
                "end": end_date
            },
            "total_tokens_used": total_tokens,
            "total_requests": total_requests,
            "feature_usage": feature_usage,
            "subscription_tier": user.subscription_tier,
            "token_limit": SubscriptionConfig.get_token_limit(
                user.subscription_tier,
                user.custom_token_limit
            )
        }

    @staticmethod
    async def record_usage(
        db: Session,
        user: User,
        feature: str,
        tokens_used: int,
        success: bool = True,
        error_message: Optional[str] = None
    ) -> None:
        """Record usage statistics for a request."""
        try:
            usage_stat = UsageStats(
                user_id=user.id,
                feature=feature,
                tokens_used=tokens_used,
                success=success,
                error_message=error_message,
                timestamp=datetime.utcnow()
            )
            db.add(usage_stat)
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error recording usage stats: {str(e)}")

    @staticmethod
    async def get_available_upgrades(user: User) -> Dict[str, Any]:
        """Get available subscription upgrade options."""
        current_tier = user.subscription_tier
        upgrades = {}
        
        for tier in SubscriptionTier:
            if tier.value > current_tier.value:
                upgrades[tier.value] = {
                    "name": tier.value,
                    "features": SubscriptionConfig.get_tier_features(tier),
                    "token_limit": SubscriptionConfig.get_token_limit(tier),
                    "concurrent_limit": SubscriptionConfig.get_concurrent_limit(tier),
                    "token_cost_multiplier": SubscriptionConfig.get_token_cost_multiplier(tier)
                }

        return {
            "current_tier": current_tier.value,
            "available_upgrades": upgrades
        }

subscription_service = SubscriptionService()
