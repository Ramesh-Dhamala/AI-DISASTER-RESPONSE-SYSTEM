#!/usr/bin/env python3
"""
AI Disaster Response System - Main Entry Point
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
import os
from datetime import datetime

# Create FastAPI app
app = FastAPI(
    title="AI Disaster Response System",
    description="ML-powered disaster prediction and alert system",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ Request Models ============
class FloodRequest(BaseModel):
    rainfall: float
    river_level: float
    humidity: float
    temperature: float

class LandslideRequest(BaseModel):
    rainfall: float
    slope: float
    soil_moisture: float
    vegetation: Optional[float] = 50

class EarthquakeRequest(BaseModel):
    latitude: float
    longitude: float
    magnitude_threshold: Optional[float] = 2.5

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = "anonymous"

# ============ Root Endpoints ============
@app.get("/")
async def root():
    return {
        "message": "AI Disaster Response System",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "flood": "/api/v1/flood/predict",
            "landslide": "/api/v1/landslide/predict",
            "earthquake": "/api/v1/earthquake/predict",
            "chat": "/api/v1/chat",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "AI Disaster Response",
        "timestamp": datetime.now().isoformat()
    }

# ============ Flood Prediction ============
@app.post("/api/v1/flood/predict")
async def predict_flood(request: FloodRequest):
    """Predict flood risk"""
    risk_score = 0
    
    if request.rainfall > 100:
        risk_score += 3
    elif request.rainfall > 50:
        risk_score += 2
    
    if request.river_level > 6:
        risk_score += 3
    elif request.river_level > 4:
        risk_score += 2
    
    if request.humidity > 85:
        risk_score += 2
    
    if risk_score >= 6:
        risk = "HIGH"
        alert = True
        message = "⚠️ Severe flood risk! Take immediate action."
    elif risk_score >= 4:
        risk = "MEDIUM"
        alert = True
        message = "⚠️ Moderate flood risk. Stay alert."
    else:
        risk = "LOW"
        alert = False
        message = "✓ Low flood risk."
    
    return {
        "success": True,
        "disaster_type": "flood",
        "risk_level": risk,
        "risk_score": risk_score,
        "alert": alert,
        "message": message
    }

# ============ Landslide Prediction ============
@app.post("/api/v1/landslide/predict")
async def predict_landslide(request: LandslideRequest):
    """Predict landslide risk"""
    risk_score = 0
    
    if request.rainfall > 100:
        risk_score += 3
    if request.slope > 35:
        risk_score += 3
    elif request.slope > 25:
        risk_score += 2
    
    if request.soil_moisture > 80:
        risk_score += 2
    
    if risk_score >= 6:
        risk = "HIGH"
        alert = True
        message = "⚠️ High landslide risk! Evacuate if in vulnerable area."
    elif risk_score >= 4:
        risk = "MEDIUM"
        alert = True
        message = "⚠️ Moderate landslide risk. Monitor conditions."
    else:
        risk = "LOW"
        alert = False
        message = "✓ Low landslide risk."
    
    return {
        "success": True,
        "disaster_type": "landslide",
        "risk_level": risk,
        "risk_score": risk_score,
        "alert": alert,
        "message": message
    }

# ============ Earthquake Prediction ============
@app.post("/api/v1/earthquake/predict")
async def predict_earthquake(request: EarthquakeRequest):
    """Predict earthquake risk"""
    risk_score = 0
    
    # Pacific Ring of Fire zones
    ring_of_fire = [
        (-60, -80, -20, -60),  # South America
        (20, 130, 50, 150),     # Japan/Philippines
        (30, -130, 60, -120),   # West US
        (-10, 100, 10, 140)     # Indonesia
    ]
    
    for lat_min, lon_min, lat_max, lon_max in ring_of_fire:
        if lat_min <= request.latitude <= lat_max and lon_min <= request.longitude <= lon_max:
            risk_score += 50
            break
    
    if risk_score > 70:
        risk = "HIGH"
        alert = True
        message = "⚠️ High earthquake risk zone. Prepare emergency kit."
    elif risk_score > 40:
        risk = "MEDIUM"
        alert = True
        message = "⚠️ Moderate earthquake risk. Stay prepared."
    else:
        risk = "LOW"
        alert = False
        message = "✓ Low earthquake risk."
    
    return {
        "success": True,
        "disaster_type": "earthquake",
        "risk_level": risk,
        "risk_score": risk_score,
        "alert": alert,
        "message": message,
        "location": {"lat": request.latitude, "lon": request.longitude}
    }

# ============ Chatbot ============
@app.post("/api/v1/chat")
async def chat(request: ChatRequest):
    """AI Chatbot for disaster assistance"""
    msg = request.message.lower()
    
    if "flood" in msg:
        response = """🌊 **Flood Safety:**
• Move to higher ground
• Avoid flood waters
• Turn off utilities
• Keep emergency kit ready"""
    
    elif "earthquake" in msg:
        response = """🌍 **Earthquake Safety:**
• Drop, Cover, Hold On
• Stay away from windows
• After shaking, check for gas leaks
• Be ready for aftershocks"""
    
    elif "landslide" in msg:
        response = """🏔️ **Landslide Safety:**
• Watch for warning signs
• Evacuate immediately
• Move to higher ground
• Avoid steep slopes"""
    
    elif "prepare" in msg or "kit" in msg:
        response = """🎒 **Emergency Kit:**
• Water (3 days)
• Non-perishable food
• First aid kit
• Flashlight & batteries
• Important documents
• Medications"""
    
    else:
        response = """�� **AI Disaster Assistant**

I can help with:
• 🌊 Flood predictions & safety
• 🌍 Earthquake guidelines
• 🏔️ Landslide warnings
• 🎒 Emergency preparation

Ask me anything about natural disasters!"""
    
    return {
        "success": True,
        "response": response,
        "intent": "disaster_info",
        "user_id": request.user_id
    }

# ============ Models Info ============
@app.get("/api/v1/models")
async def list_models():
    return {
        "success": True,
        "models": [
            {"name": "flood_prediction", "version": "1.0.0", "status": "active"},
            {"name": "landslide_prediction", "version": "1.0.0", "status": "active"},
            {"name": "earthquake_prediction", "version": "1.0.0", "status": "active"}
        ]
    }

# ============ Run Server ============
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🚀 AI Disaster Response System API")
    print("=" * 60)
    print("📍 Server: http://0.0.0.0:8000")
    print("📚 API Docs: http://0.0.0.0:8000/docs")
    print("🔍 Health Check: http://0.0.0.0:8000/health")
    print("=" * 60 + "\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
