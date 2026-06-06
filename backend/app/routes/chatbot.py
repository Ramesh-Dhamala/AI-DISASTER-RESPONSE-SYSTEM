from fastapi import APIRouter
from app.services.groq_service import disaster_chat

router = APIRouter()


@router.post("/chat")
def chat(request: dict):

    message = request.get("message")

    if not message:
        return {"response": "Message is required"}

    reply = disaster_chat(message)

    return {"response": reply}