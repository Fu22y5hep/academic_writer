from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from app.core.deps import get_db, get_current_user, check_rate_limit
from app.models.user import User
from app.services.ai_service import generate_outline

router = APIRouter()

class OutlineRequest(BaseModel):
    topic: str
    essay_type: str
    word_count: Optional[int] = None
    thesis_statement: Optional[str] = None

@router.post("/generate-outline", response_model=Dict[str, Any])
async def create_ai_outline(
    request: OutlineRequest,
    current_request: Request,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user),
) -> Dict[str, Any]:
    """Generate an outline for a given topic using AI."""
    # Check rate limit first
    await check_rate_limit(current_request, current_user)
    
    try:
        outline = await generate_outline(
            topic=request.topic,
            essay_type=request.essay_type,
            word_count=request.word_count,
            thesis_statement=request.thesis_statement
        )
        return outline
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
