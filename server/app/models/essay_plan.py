from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.models.base import Base

class EssayPlan(Base):
    __tablename__ = "essay_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, index=True)
    essay_type = Column(String)  # argumentative, analytical, expository, etc.
    topic = Column(String)
    thesis_statement = Column(String)
    outline = Column(JSON)  # Stores the hierarchical outline structure
    guidelines = Column(JSON, nullable=True)  # Optional assignment guidelines/rubrics
    word_count_target = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="essay_plans")

    class Config:
        orm_mode = True
