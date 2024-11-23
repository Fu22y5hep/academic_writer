from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.essay_plan import EssayPlan
from app.schemas.essay_plan import EssayPlanCreate, EssayPlanUpdate

class EssayPlanService:
    def __init__(self, db: Session):
        self.db = db

    def create_plan(self, user_id: int, plan: EssayPlanCreate) -> EssayPlan:
        db_plan = EssayPlan(
            user_id=user_id,
            **plan.dict()
        )
        self.db.add(db_plan)
        self.db.commit()
        self.db.refresh(db_plan)
        return db_plan

    def get_plan(self, plan_id: int) -> Optional[EssayPlan]:
        return self.db.query(EssayPlan).filter(EssayPlan.id == plan_id).first()

    def get_user_plans(self, user_id: int, skip: int = 0, limit: int = 100) -> List[EssayPlan]:
        return self.db.query(EssayPlan)\
            .filter(EssayPlan.user_id == user_id)\
            .offset(skip)\
            .limit(limit)\
            .all()

    def update_plan(self, plan_id: int, plan_update: EssayPlanUpdate) -> EssayPlan:
        db_plan = self.get_plan(plan_id)
        update_data = plan_update.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_plan, field, value)
        
        self.db.commit()
        self.db.refresh(db_plan)
        return db_plan

    def delete_plan(self, plan_id: int) -> None:
        db_plan = self.get_plan(plan_id)
        self.db.delete(db_plan)
        self.db.commit()
