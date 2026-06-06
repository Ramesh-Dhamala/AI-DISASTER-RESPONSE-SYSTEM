from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class LandslideRequest(BaseModel):
    rainfall: float
    slope: float
    soil_moisture: float
    vegetation: Optional[float] = 0.5

@router.post("/landslide/predict")
async def predict_landslide_endpoint(request: LandslideRequest):
    # Simple risk calculation (replace with your model)
    risk_score = 0
    
    if request.rainfall > 100:
        risk_score += 2
    elif request.rainfall > 50:
        risk_score += 1
    
    if request.slope > 30:
        risk_score += 2
    elif request.slope > 15:
        risk_score += 1
    
    if request.soil_moisture > 70:
        risk_score += 1
    
    if risk_score >= 4:
        risk_level = "HIGH"
        alert = True
        message = "High landslide risk! Evacuate if in vulnerable area."
    elif risk_score >= 2:
        risk_level = "MEDIUM"
        alert = True
        message = "Moderate landslide risk. Stay alert."
    else:
        risk_level = "LOW"
        alert = False
        message = "Low landslide risk."
    
    return {
        "success": True,
        "disaster": "landslide",
        "risk_level": risk_level,
        "risk_score": risk_score,
        "alert": alert,
        "message": message
    }
