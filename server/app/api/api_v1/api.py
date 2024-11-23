from fastapi import APIRouter
from app.api.api_v1.endpoints import test, ai_outline, auth

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(test.router, prefix="/test", tags=["test"])
api_router.include_router(ai_outline.router, tags=["ai"])
