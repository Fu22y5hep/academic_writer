from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Convert PostgresDsn to string for SQLAlchemy
SQLALCHEMY_DATABASE_URL = str(settings.DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create all tables
def init_db():
    # Import all models here to ensure they are registered with SQLAlchemy
    from app.models.base import Base
    from app.models.user import User
    from app.models.usage_stats import UsageStats
    
    Base.metadata.create_all(bind=engine)
