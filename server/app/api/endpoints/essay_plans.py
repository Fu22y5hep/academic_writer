from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.essay_plan import EssayPlan, EssayPlanCreate, EssayPlanUpdate
from app.services.essay_plan_service import EssayPlanService

router = APIRouter()

@router.post("/", response_model=EssayPlan)
def create_essay_plan(
    plan: EssayPlanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new essay plan."""
    return EssayPlanService(db).create_plan(current_user.id, plan)

@router.get("/", response_model=List[EssayPlan])
def get_user_plans(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all essay plans for the current user."""
    return EssayPlanService(db).get_user_plans(current_user.id, skip, limit)

@router.get("/{plan_id}", response_model=EssayPlan)
def get_essay_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific essay plan by ID."""
    plan = EssayPlanService(db).get_plan(plan_id)
    if not plan or plan.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Essay plan not found")
    return plan

@router.put("/{plan_id}", response_model=EssayPlan)
def update_essay_plan(
    plan_id: int,
    plan_update: EssayPlanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an essay plan."""
    plan = EssayPlanService(db).get_plan(plan_id)
    if not plan or plan.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Essay plan not found")
    return EssayPlanService(db).update_plan(plan_id, plan_update)

@router.delete("/{plan_id}")
def delete_essay_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete an essay plan."""
    plan = EssayPlanService(db).get_plan(plan_id)
    if not plan or plan.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Essay plan not found")
    EssayPlanService(db).delete_plan(plan_id)
    return {"message": "Essay plan deleted successfully"}
