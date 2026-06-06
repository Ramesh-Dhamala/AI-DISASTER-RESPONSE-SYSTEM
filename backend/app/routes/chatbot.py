from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

router = APIRouter()

class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = "anonymous"
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    success: bool
    response: str
    intent: str
    confidence: float
    timestamp: str
    suggestions: List[str]

# Disaster response knowledge base
DISASTER_INFO = {
    "flood": {
        "info": "Floods are caused by heavy rainfall, storm surges, or river overflow.",
        "precautions": [
            "Move to higher ground immediately",
            "Do not walk or drive through flood waters",
            "Turn off gas and electricity",
            "Keep emergency supplies ready"
        ],
        "emergency": "Call flood control: 911 or local emergency services"
    },
    "earthquake": {
        "info": "Earthquakes are sudden ground shaking caused by tectonic plate movements.",
        "precautions": [
            "Drop, Cover, and Hold On",
            "Stay away from windows and heavy furniture",
            "If outside, move to open area",
            "Check for gas leaks after shaking stops"
        ],
        "emergency": "Call emergency services if injured"
    },
    "landslide": {
        "info": "Landslides occur on steep slopes, often triggered by heavy rain or earthquakes.",
        "precautions": [
            "Watch for signs: cracking sounds, falling debris",
            "Evacuate immediately if you see moving ground",
            "Avoid river valleys and steep slopes",
            "Stay alert during heavy rainfall"
        ],
        "emergency": "Contact local authorities for evacuation assistance"
    },
    "cyclone": {
        "info": "Cyclones are intense storm systems with strong winds and heavy rain.",
        "precautions": [
            "Secure your home and windows",
            "Store emergency food and water",
            "Follow evacuation orders",
            "Stay indoors away from windows"
        ],
        "emergency": "Listen to official cyclone warnings"
    },
    "tsunami": {
        "info": "Tsunamis are large ocean waves caused by underwater earthquakes.",
        "precautions": [
            "Move to high ground immediately after strong shaking",
            "Do not wait for official warning",
            "Stay at least 3 km inland or 30m above sea level",
            "Do not return until authorities declare safety"
        ],
        "emergency": "Tsunami warning: Move to higher ground NOW"
    }
}

@router.post("/chat", response_model=ChatResponse)
async def chat_with_assistant(message: ChatMessage):
    """
    Chat with AI Disaster Response Assistant
    """
    user_message = message.message.lower()
    
    # Detect intent
    intent = "general"
    confidence = 0.5
    response = ""
    suggestions = []
    
    # Check for disaster types
    for disaster_type in DISASTER_INFO.keys():
        if disaster_type in user_message:
            intent = disaster_type
            confidence = 0.9
            info = DISASTER_INFO[disaster_type]
            response = f"{info['info']}\n\nPrecautions:\n" + "\n".join(f"• {p}" for p in info['precautions'])
            suggestions = info['precautions'][:2]
            break
    
    # Check for safety/help queries
    if any(word in user_message for word in ["help", "safety", "prepare", "emergency"]):
        intent = "safety"
        confidence = 0.85
        response = "General Safety Tips:\n• Prepare emergency kit with food, water, medicine\n• Have a family emergency plan\n• Know evacuation routes\n• Keep important documents safe\n• Stay informed through official channels"
        suggestions = ["Prepare emergency kit", "Make family plan", "Learn evacuation routes"]
    
    # Check for real-time alerts
    elif any(word in user_message for word in ["alert", "warning", "current", "now"]):
        intent = "alerts"
        confidence = 0.75
        response = "For real-time alerts, check:\n• Local news channels\n• Weather service apps\n• Emergency management agency\n• NOAA Weather Radio"
        suggestions = ["Check weather app", "Monitor local news", "Enable emergency alerts"]
    
    # Default response
    elif intent == "general":
        response = "I'm your AI Disaster Response Assistant. I can help with:\n• Floods, Earthquakes, Landslides\n• Cyclones, Tsunamis\n• Safety precautions and emergency preparedness\n• Real-time alerts\n\nWhat would you like to know about?"
        suggestions = ["Flood safety", "Earthquake preparation", "Current alerts"]
    
    return ChatResponse(
        success=True,
        response=response,
        intent=intent,
        confidence=confidence,
        timestamp=datetime.now().isoformat(),
        suggestions=suggestions
    )

@router.get("/chat/health")
async def chat_health():
    """
    Check if chatbot service is healthy
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "disaster_types": list(DISASTER_INFO.keys())
    }

@router.post("/chat/feedback")
async def submit_feedback(message_id: str, rating: int, feedback: str):
    """
    Submit feedback for chatbot responses
    """
    return {
        "success": True,
        "message": "Thank you for your feedback!",
        "rating": rating
    }