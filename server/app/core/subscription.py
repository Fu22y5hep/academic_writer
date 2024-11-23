from typing import Dict, Any
from app.models.user import SubscriptionTier

class SubscriptionConfig:
    # Token limits per hour for each tier
    TOKEN_LIMITS = {
        SubscriptionTier.FREE: 50,
        SubscriptionTier.BASIC: 200,
        SubscriptionTier.PREMIUM: 500,
        SubscriptionTier.UNLIMITED: float('inf')
    }

    # Concurrent requests limits
    CONCURRENT_LIMITS = {
        SubscriptionTier.FREE: 2,
        SubscriptionTier.BASIC: 5,
        SubscriptionTier.PREMIUM: 10,
        SubscriptionTier.UNLIMITED: 20
    }

    # Token cost multipliers (lower means cheaper)
    TOKEN_COST_MULTIPLIERS = {
        SubscriptionTier.FREE: 1.0,
        SubscriptionTier.BASIC: 0.8,
        SubscriptionTier.PREMIUM: 0.6,
        SubscriptionTier.UNLIMITED: 0.5
    }

    # Feature access by tier
    FEATURE_ACCESS = {
        SubscriptionTier.FREE: {
            "suggestions": True,
            "grammar": True,
            "citations": True,
            "tone": True,
            "research_questions": False,
            "outline": False,
            "literature_analysis": False,
            "methodology": False,
            "abstract": False,
            "keywords": True,
            "format_reference": True,
            "check_style": True,
            "extract_citations": True,
            "suggest_transitions": False,
            "check_arguments": False,
            "suggest_evidence": False
        },
        SubscriptionTier.BASIC: {
            "suggestions": True,
            "grammar": True,
            "citations": True,
            "tone": True,
            "research_questions": True,
            "outline": True,
            "literature_analysis": False,
            "methodology": False,
            "abstract": True,
            "keywords": True,
            "format_reference": True,
            "check_style": True,
            "extract_citations": True,
            "suggest_transitions": True,
            "check_arguments": False,
            "suggest_evidence": True
        },
        SubscriptionTier.PREMIUM: {
            "suggestions": True,
            "grammar": True,
            "citations": True,
            "tone": True,
            "research_questions": True,
            "outline": True,
            "literature_analysis": True,
            "methodology": True,
            "abstract": True,
            "keywords": True,
            "format_reference": True,
            "check_style": True,
            "extract_citations": True,
            "suggest_transitions": True,
            "check_arguments": True,
            "suggest_evidence": True
        },
        SubscriptionTier.UNLIMITED: {
            "suggestions": True,
            "grammar": True,
            "citations": True,
            "tone": True,
            "research_questions": True,
            "outline": True,
            "literature_analysis": True,
            "methodology": True,
            "abstract": True,
            "keywords": True,
            "format_reference": True,
            "check_style": True,
            "extract_citations": True,
            "suggest_transitions": True,
            "check_arguments": True,
            "suggest_evidence": True
        }
    }

    @classmethod
    def get_token_limit(cls, tier: SubscriptionTier, custom_limit: int = None) -> int:
        """Get token limit for a subscription tier."""
        if custom_limit is not None:
            return custom_limit
        return cls.TOKEN_LIMITS[tier]

    @classmethod
    def get_concurrent_limit(cls, tier: SubscriptionTier) -> int:
        """Get concurrent request limit for a subscription tier."""
        return cls.CONCURRENT_LIMITS[tier]

    @classmethod
    def get_token_cost_multiplier(cls, tier: SubscriptionTier) -> float:
        """Get token cost multiplier for a subscription tier."""
        return cls.TOKEN_COST_MULTIPLIERS[tier]

    @classmethod
    def has_feature_access(cls, tier: SubscriptionTier, feature: str) -> bool:
        """Check if a tier has access to a specific feature."""
        return cls.FEATURE_ACCESS[tier].get(feature, False)

    @classmethod
    def get_tier_features(cls, tier: SubscriptionTier) -> Dict[str, bool]:
        """Get all features and their access status for a tier."""
        return cls.FEATURE_ACCESS[tier].copy()

    @classmethod
    def get_tier_info(cls, tier: SubscriptionTier) -> Dict[str, Any]:
        """Get complete information about a subscription tier."""
        return {
            "token_limit": cls.get_token_limit(tier),
            "concurrent_limit": cls.get_concurrent_limit(tier),
            "token_cost_multiplier": cls.get_token_cost_multiplier(tier),
            "features": cls.get_tier_features(tier)
        }
