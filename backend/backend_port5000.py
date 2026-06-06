from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI(title="Disaster Response API")

# Enable CORS for frontend
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

@app.post("/api/v1/chat")
async def chat(request: ChatRequest):
    msg = request.message.lower()
    
    if "flood" in msg:
        response = """🌊 **FLOOD SAFETY**
        
• Move to HIGHER GROUND immediately
• NEVER walk or drive through flood water
• 6 inches of water can knock you down
• 12 inches can float a car
• Turn off gas and electricity if safe
• Listen to official alerts"""
    
    elif "earthquake" in msg:
        response = """🏠 **EARTHQUAKE SAFETY - DROP, COVER, HOLD ON**
        
• DROP to your hands and knees
• COVER your head and neck under sturdy table
• HOLD ON until shaking stops
• Stay away from windows and heavy furniture
• If outside, move to open area"""
    
    elif "landslide" in msg:
        response = """⛰️ **LANDSLIDE SAFETY**
        
• EVACUATE immediately if you suspect danger
• Move to higher ground away from slopes
• Watch for cracking sounds or falling rocks
• Listen for rumbling sounds"""
    
    elif "cyclone" in msg or "hurricane" in msg:
        response = """🌀 **CYCLONE PREPAREDNESS**
        
• Board up windows or use shutters
• Prepare 7-day emergency supply kit
• Know your evacuation zone
• Stay indoors away from windows"""
    
    elif "kit" in msg or "supplies" in msg:
        response = """🎒 **EMERGENCY KIT CHECKLIST**
        
• Water: 1 gallon per person per day (7 days)
• Non-perishable food (7 days supply)
• First aid kit and medications
• Flashlight and extra batteries
• Whistle to signal for help
• Important documents in waterproof bag"""
    
    else:
        response = """🤖 **Disaster Response Assistant**
        
I can help you with:
• Floods - Safety and evacuation
• Earthquakes - Drop, Cover, Hold On
• Landslides - Warning signs and evacuation
• Cyclones/Hurricanes - Preparation
• Emergency kits - What to include

Try asking: "What to do during a flood?" or "Earthquake safety tips" """
    
    return {"success": True, "response": response, "session_id": request.session_id}

@app.get("/health")
async def health():
    return {"status": "healthy", "port": 5000}

@app.get("/")
async def root():
    return {"message": "Disaster Response API is running", "port": 5000}

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 BACKEND RUNNING ON PORT 5000")
    print("📍 http://127.0.0.1:5000")
    print("📚 API Docs: http://127.0.0.1:5000/docs")
    print("="*50 + "\n")
    uvicorn.run(app, host="127.0.0.1", port=5000)