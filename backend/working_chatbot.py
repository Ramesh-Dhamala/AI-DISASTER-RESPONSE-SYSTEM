"""
Working Disaster Response Chatbot
Run: python working_chatbot.py
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Disaster Response Chatbot", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

def get_response(user_message: str):
    """Generate disaster safety response"""
    msg = user_message.lower()
    
    responses = {
        "flood": """🌊 **FLOOD SAFETY - What You Need to Know**

**Before Flood:**
• Prepare emergency kit with 7 days of supplies
• Know evacuation routes from your area
• Keep important documents in waterproof bags

**During Flood (Critical!):**
• **Move to higher ground IMMEDIATELY**
• NEVER walk or drive through flood water
• Just 6 inches can knock you down
• Just 12 inches can float a car
• Turn off gas and electricity if safe

**After Flood:**
• Wait for authorities to declare safety
• Avoid standing water (may have electrical current)
• Check on neighbors, especially elderly

💡 **Golden Rule:** "Turn Around, Don't Drown!" Never drive through flooded roads.""",
        
        "earthquake": """🏠 **EARTHQUAKE SAFETY - DROP, COVER, HOLD ON!**

**During Earthquake:**
• **DROP** to your hands and knees
• **COVER** your head and neck under sturdy table
• **HOLD ON** until shaking stops
• Stay away from windows, glass, and heavy furniture
• If outside, move to open area away from buildings

**After Earthquake:**
• Check yourself and others for injuries
• Expect aftershocks
• Check for gas leaks and fire hazards
• Use stairs, NEVER elevators

📢 **Remember:** Drop, Cover, and Hold On saves lives!""",
        
        "landslide": """⛰️ **LANDSLIDE SAFETY**

**Warning Signs:**
• Cracking sounds from ground
• Tilting trees or poles
• Water breaking through ground
• Doors/windows suddenly sticking

**What To Do:**
• **EVACUATE IMMEDIATELY** if you suspect danger
• Move to higher ground away from slopes
• Listen for rumbling sounds
• Watch for falling rocks or debris

**After Landslide:**
• Stay away from slide area
• Report broken utilities to authorities""",
        
        "cyclone": """🌀 **CYCLONE/HURRICANE PREPAREDNESS**

**Before Storm:**
• Board up windows or use storm shutters
• Bring outdoor items inside
• Prepare 7-day emergency supply kit
• Know evacuation zone and routes

**During Storm:**
• Stay indoors, away from windows
• Listen to weather updates on radio
• If evacuation ordered, LEAVE IMMEDIATELY
• Move to interior room or basement

**After Storm:**
• Don't go outside until authorities say safe
• Watch for downed power lines
• Avoid flood waters
• Check for gas leaks""",
        
        "emergency kit": """🎒 **EMERGENCY KIT CHECKLIST (7-day supply)**

**Water & Food:**
• Water: 1 gallon per person per day (7 gallons)
• Non-perishable food (canned goods, energy bars)
• Manual can opener

**First Aid & Medicine:**
• First aid kit with bandages and antiseptic
• Prescription medications (7-day supply)
• Pain relievers, thermometer

**Safety Items:**
• Flashlight + extra batteries
• Whistle to signal for help
• Dust masks and duct tape
• Multi-tool

**Important:**
• Cell phone with power bank
• Important documents (waterproof container)
• Cash in small bills
• Local maps

**Comfort:**
• Sleeping bags or blankets
• Change of clothes and sturdy shoes
• Personal hygiene items

📋 **Review your kit every 6 months!**"""
    }
    
    # Check for keywords
    for key, response in responses.items():
        if key in msg:
            return response
    
    # Help response
    if any(word in msg for word in ["help", "hi", "hello", "hey"]):
        return """🤖 **Disaster Response Assistant**

I can help you with:
• 🌊 **Floods** - Safety, evacuation, preparation
• 🏠 **Earthquakes** - Drop/Cover/Hold On guide
• ⛰️ **Landslides** - Warning signs, evacuation
• 🌀 **Cyclones/Hurricanes** - Preparation, safety
• 🎒 **Emergency Kits** - Complete checklist

**Try asking:**
• "What to do during a flood?"
• "Earthquake safety tips"
• "How to prepare for a cyclone?"
• "What should I have in my emergency kit?"
• "Landslide warning signs"

**How can I help you stay safe today?**"""
    
    # Default
    return """📋 **I'm Your Disaster Safety Assistant**

I provide safety information for natural disasters.

**Ask me about:**
• Floods
• Earthquakes
• Landslides
• Cyclones/Hurricanes
• Emergency kits
• Safety tips

**Example:** "What to do during a flood?"

What would you like to know about?"""

@app.post("/api/v1/chat")
async def chat(request: ChatRequest):
    """Chat with Disaster Safety Assistant"""
    try:
        response = get_response(request.message)
        return {
            "success": True,
            "response": response,
            "session_id": request.session_id or "default",
            "timestamp": "2026-06-07"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {
        "service": "Disaster Response Chatbot",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "chat": "POST /api/v1/chat",
            "docs": "/docs",
            "health": "/health"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "chatbot"}

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 DISASTER RESPONSE CHATBOT")
    print("="*60)
    print("📍 Chatbot URL: http://127.0.0.1:8001")
    print("📚 API Docs: http://127.0.0.1:8001/docs")
    print("💬 Test: POST to http://127.0.0.1:8001/api/v1/chat")
    print("="*60 + "\n")
    
    uvicorn.run(app, host="127.0.0.1", port=8001, reload=False)