from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_service import call_openai_with_retry
from app.core.config import settings

router = APIRouter()

class Message(BaseModel):
    message: str

@router.post("/test-openai")
async def test_openai_connection(message: Message):
    """
    Test the OpenAI API connection by making a completion request with the user's message.
    """
    try:
        messages = [
            {"role": "system", "content": settings.OPENAI_SYSTEM_PROMPT},
            {"role": "user", "content": message.message}
        ]
        
        response = await call_openai_with_retry(messages)
        
        return {
            "status": "success",
            "message": "OpenAI API is working correctly",
            "response": response.choices[0].message.content
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error testing OpenAI connection: {str(e)}"
        )
