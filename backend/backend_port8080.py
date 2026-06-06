from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI(title="Disaster Response API")

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
• 6 inches can knock you down
• 12 inches can float a car
• Turn off gas and electricity if safe"""
    
    elif "earthquake" in msg:
        response = """🏠 **EARTHQUAKE SAFETY**
        
• DROP to your hands and knees
• COVER your head and neck
• HOLD ON until shaking stops
• Stay away from windows"""
    
    elif "landslide" in msg:
        response = "⛰️ EVACUATE immediately! Move to higher ground away from slopes."
    
    elif "kit" in msg or "supplies" in msg:
        response = "🎒 Emergency kit: Water (1 gal/day), food, flashlight, batteries, first aid kit."
    
    else:
        response = "I can help with floods, earthquakes, landslides, and emergency kits. What would you like to know?"
    
    return {"success": True, "response": response}

@app.get("/health")
async def health():
    return {"status": "healthy", "port": 8080}

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 BACKEND RUNNING ON PORT 8080")
    print("📍 http://127.0.0.1:8080")
    print("="*50 + "\n")
    uvicorn.run(app, host="127.0.0.1", port=8080)