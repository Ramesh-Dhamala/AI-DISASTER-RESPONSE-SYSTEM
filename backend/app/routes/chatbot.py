from fastapi import APIRouter
from pydantic import BaseModel
from app.services.groq_service import disaster_chat

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/chat")
async def chat(request: ChatRequest):
    reply = disaster_chat(request.message)
    return ChatResponse(response=reply)