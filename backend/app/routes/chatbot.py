from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.groq_service import disaster_chat

router = APIRouter()

# ✅ Request model (more professional than dict)
class ChatRequest(BaseModel):
    message: str

# ✅ Allowed disaster-related keywords
ALLOWED_TOPICS = [
    "earthquake",
    "flood",
    "weather",
    "rain",
    "landslide",
    "disaster",
    "safety",
    "rescue",
    "alert",
    "emergency",
    "aftershock",
    "evacuation",
    "cyclone",
    "storm"
]

def is_valid_question(message: str):
    message = message.lower()
    return any(topic in message for topic in ALLOWED_TOPICS)


@router.post("/chat")
def chat(request: ChatRequest):

    user_message = request.message

    if not user_message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # ❌ BLOCK NON-DISASTER QUESTIONS
    if not is_valid_question(user_message):
        return {
            "response": "⚠️ I can only answer disaster and emergency-related questions (flood, earthquake, landslide, weather alerts)."
        }

    # ✅ SEND TO AI
    try:
        reply = disaster_chat(user_message)
        return {"response": reply}

    except Exception as e:
        return {
            "response": "⚠️ AI service error. Please try again later."
        }