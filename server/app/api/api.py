from fastapi import APIRouter

from app.api.endpoints import (
    essay_plans,
    ai_outline
)

api_router = APIRouter()

api_router.include_router(
    essay_plans.router,
    prefix="/essay-plans",
    tags=["essay-plans"]
)

# Remove the /api prefix since the main app already includes it
api_router.include_router(ai_outline.router, tags=["ai"])
