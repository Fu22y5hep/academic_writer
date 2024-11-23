from typing import Generator, Optional
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.core import security
from app.core.config import settings
from app.database import SessionLocal
from app.models.user import User
from app.core.rate_limiter import rate_limiter

oauth2_scheme = security.oauth2_scheme

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    user_id = security.verify_token(token)
    if user_id is None:
        raise credentials_exception
        
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

async def check_rate_limit(
    request: Request,
    current_user: User = Depends(get_current_user)
) -> None:
    """
    Check rate limits for AI endpoints.
    Must be used as a dependency in AI-related endpoints.
    """
    await rate_limiter.check_rate_limit(request, current_user)

async def get_rate_limit_info(
    request: Request,
    current_user: User = Depends(get_current_user)
) -> dict:
    """Get rate limit information for the current user."""
    return await rate_limiter.get_rate_limit_info(request, current_user)

async def mark_request_completed(
    request: Request,
    current_user: User = Depends(get_current_user)
) -> None:
    """Mark a request as completed to update concurrent request count."""
    await rate_limiter.mark_request_completed(request, current_user)
