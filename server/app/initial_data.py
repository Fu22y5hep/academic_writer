import asyncio
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine, Base
from app.models import user, usage_stats
from app.core.security import get_password_hash
from app.models.user import SubscriptionTier

def init_db(db: Session) -> None:
    Base.metadata.create_all(bind=engine)
    
    # Create test user if it doesn't exist
    test_user = db.query(user.User).filter_by(email="test@example.com").first()
    if not test_user:
        test_user = user.User(
            email="test@example.com",
            full_name="Test User",
            hashed_password=get_password_hash("test123"),
            is_active=True,
            subscription_tier=SubscriptionTier.FREE
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)

    # Add some test usage stats
    test_stats = usage_stats.UsageStats(
        user_id=test_user.id,
        feature="grammar_check",
        tokens_used=100,
        success=True
    )
    db.add(test_stats)
    db.commit()

def main() -> None:
    db = SessionLocal()
    init_db(db)
    db.close()

if __name__ == "__main__":
    main()
