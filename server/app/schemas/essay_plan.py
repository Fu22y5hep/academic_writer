from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class EssayPlanBase(BaseModel):
    title: str
    essay_type: str
    topic: str
    thesis_statement: Optional[str] = None
    outline: Dict[str, Any]
    guidelines: Optional[Dict[str, Any]] = None
    word_count_target: Optional[int] = None

class EssayPlanCreate(EssayPlanBase):
    pass

class EssayPlanUpdate(BaseModel):
    title: Optional[str] = None
    essay_type: Optional[str] = None
    topic: Optional[str] = None
    thesis_statement: Optional[str] = None
    outline: Optional[Dict[str, Any]] = None
    guidelines: Optional[Dict[str, Any]] = None
    word_count_target: Optional[int] = None

class EssayPlan(EssayPlanBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
