from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import auth, users, documents, collaborations, ai_writing, subscription
from app.api.api_v1.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["authentication"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(documents.router, prefix=f"{settings.API_V1_STR}/documents", tags=["documents"])
app.include_router(collaborations.router, prefix=settings.API_V1_STR, tags=["collaborations"])
app.include_router(ai_writing.router, prefix=f"{settings.API_V1_STR}/ai", tags=["ai"])
app.include_router(subscription.router, prefix=f"{settings.API_V1_STR}/subscription", tags=["subscription"])

@app.get("/")
async def root():
    return {"message": "Welcome to Academic Writing Assistant API"}
