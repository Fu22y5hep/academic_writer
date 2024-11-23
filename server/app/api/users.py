from typing import Any, List, Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.user import User as UserSchema, UserUpdate

router = APIRouter()

@router.get("/me", response_model=UserSchema)
def read_user_me(
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get current user."""
    return current_user

@router.put("/me", response_model=UserSchema)
def update_user_me(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Update current user."""
    if user_in.email and user_in.email != current_user.email:
        if db.query(User).filter(User.email == user_in.email).first():
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )
    
    update_data = user_in.dict(exclude_unset=True)
    if 'password' in update_data:
        from app.core.security import get_password_hash
        update_data['hashed_password'] = get_password_hash(update_data.pop('password'))
    
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/me/preferences", response_model=Dict[str, Any])
def get_user_preferences(
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get current user's preferences."""
    return current_user.preferences or {}

@router.put("/me/preferences", response_model=Dict[str, Any])
def update_user_preferences(
    preferences: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """Update current user's preferences."""
    current_user.preferences = preferences
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user.preferences
