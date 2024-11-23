from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import logging

from app.core.deps import get_db, get_current_user
from app.core.security import verify_password, create_access_token
from app.models.user import User
from app.schemas.user import UserCreate, User as UserSchema
from app.core.config import settings
from app.schemas.token import Token

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/register", response_model=UserSchema)
async def register(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate
) -> Any:
    """Register a new user."""
    try:
        logger.info(f"Attempting to register user with email: {user_in.email}")
        
        # Check if user exists
        user = db.query(User).filter(User.email == user_in.email).first()
        if user:
            logger.warning(f"Registration failed: User with email {user_in.email} already exists")
            raise HTTPException(
                status_code=400,
                detail="A user with this email already exists."
            )
        
        # Create new user
        try:
            user = User(
                email=user_in.email,
                full_name=user_in.full_name,
                password=user_in.password
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            logger.info(f"Successfully registered user with email: {user_in.email}")
            return user
        except Exception as e:
            db.rollback()
            logger.error(f"Database error during user registration: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create user: {str(e)}"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during registration: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during registration"
        )

@router.post("/login/access-token", response_model=Token)
async def login_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """OAuth2 compatible token login, get an access token for future requests."""
    try:
        logger.info(f"Attempting to login user with email: {form_data.username}")
        user = db.query(User).filter(User.email == form_data.username).first()
        if not user or not verify_password(form_data.password, user.hashed_password):
            logger.warning(f"Login failed: Incorrect email or password for user {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = create_access_token(user.id)
        logger.info(f"Successfully logged in user with email: {form_data.username}")
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during login"
        )

@router.get("/test-token", response_model=UserSchema)
async def test_token(current_user: User = Depends(get_current_user)) -> Any:
    """Test access token."""
    return current_user
