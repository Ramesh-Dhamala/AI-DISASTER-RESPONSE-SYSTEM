from fastapi import APIRouter
from app.services.groq_service import chat_with_groq

router = APIRouter()

ALLOWED_TOPICS = [
    "earthquake",
    "flood",
    "weather",
    "landslide",
    "disaster",
    "safety",
    "rescue",
    "alert",
    "emergency"
]

def is_valid_question(message: str):
    message = message.lower()
    return any(topic in message for topic in ALLOWED_TOPICS)


@router.post("/chat")
def chat(request: dict):

    user_message = request.get("message")

    if not user_message:
        return {"response": "Message is required"}

    # ❌ BLOCK NON-DISASTER QUESTIONS
    if not is_valid_question(user_message):
        return {
            "response": "Sorry, I only answer disaster-related questions like earthquake, flood, weather, and safety."
        }

    # ✅ SEND TO AI
    reply = chat_with_groq(user_message)

    return {"response": reply}