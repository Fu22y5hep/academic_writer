from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.models.base import Base

class UsageStats(Base):
    __tablename__ = "usage_stats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    tokens_used = Column(Integer, default=0)
    last_request = Column(DateTime, default=datetime.utcnow)
    feature_usage = Column(JSON, default={})
    
    # Relationships
    user = relationship("User", back_populates="usage_stats")
