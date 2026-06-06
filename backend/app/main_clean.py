from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# Create FastAPI app
app = FastAPI(title="AI Disaster Response API", version="1.0.0")

# Request/Response Models
class FloodRequest(BaseModel):
    rainfall: float
    river_level: float
    humidity: float
    temperature: float

class FloodResponse(BaseModel):
    success: bool
    disaster: str
    risk_level: str
    alert: bool
    message: str

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "AI Disaster Response System API",
        "status": "running"
    }

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": ["flood", "weather", "landslide", "map"]
    }

# Flood prediction endpoint
@app.post("/api/v1/flood/predict", response_model=FloodResponse)
async def predict_flood(request: FloodRequest):
    # Simple risk calculation
    risk_score = 0
    
    if request.rainfall > 100:
        risk_score += 2
    elif request.rainfall > 50:
        risk_score += 1
    
    if request.river_level > 5:
        risk_score += 2
    elif request.river_level > 3:
        risk_score += 1
    
    if request.humidity > 80:
        risk_score += 1
    
    if risk_score >= 3:
        risk_level = "HIGH"
        alert = True
        message = "Severe flood risk! Take immediate action."
    elif risk_score >= 2:
        risk_level = "MEDIUM"
        alert = True
        message = "Moderate flood risk. Stay alert."
    else:
        risk_level = "LOW"
        alert = False
        message = "No immediate flood risk."
    
    return FloodResponse(
        success=True,
        disaster="flood",
        risk_level=risk_level,
        alert=alert,
        message=message
    )

# Weather endpoint
@app.get("/api/v1/weather")
async def get_weather():
    return {
        "success": True,
        "temperature": 25.5,
        "humidity": 70,
        "rainfall": 10.2,
        "wind_speed": 15.3
    }

# Landslide prediction
class LandslideRequest(BaseModel):
    rainfall: float
    slope: float
    soil_moisture: float

@app.post("/api/v1/landslide/predict")
async def predict_landslide(request: LandslideRequest):
    risk_score = 0
    
    if request.rainfall > 80:
        risk_score += 2
    if request.slope > 30:
        risk_score += 2
    if request.soil_moisture > 70:
        risk_score += 1
    
    if risk_score >= 3:
        risk = "HIGH"
        alert = True
    elif risk_score >= 2:
        risk = "MEDIUM"
        alert = True
    else:
        risk = "LOW"
        alert = False
    
    return {
        "success": True,
        "disaster": "landslide",
        "risk_level": risk,
        "alert": alert,
        "message": f"Landslide risk is {risk}"
    }

# Map data endpoint
@app.get("/api/v1/map/zones")
async def get_map_zones():
    return {
        "success": True,
        "zones": [
            {"type": "flood", "risk": "high", "coordinates": [28.5, 77.5]},
            {"type": "landslide", "risk": "medium", "coordinates": [29.5, 78.5]}
        ]
    }

print("=" * 50)
print("✅ Server is running!")
print("📍 http://127.0.0.1:8000")
print("📚 http://127.0.0.1:8000/docs")
print("=" * 50)