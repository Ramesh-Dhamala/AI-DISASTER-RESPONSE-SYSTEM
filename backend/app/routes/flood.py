from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.flood_service import predict_flood_risk

router = APIRouter()

class FloodRequest(BaseModel):
    rainfall: float
    river_level: float
    humidity: float
    temperature: float
    additional_features: Optional[dict] = None

@router.post("/flood/predict")
async def predict_flood_endpoint(request: FloodRequest):
    try:
        # Convert request to dictionary
        data = {
            "rainfall": request.rainfall,
            "river_level": request.river_level,
            "humidity": request.humidity,
            "temperature": request.temperature
        }
        
        # Get prediction from service
        result = predict_flood_risk(data)
        
        return {
            "success": True,
            "disaster": "flood",
            "risk_level": result.get("risk", "UNKNOWN"),
            "alert": result.get("alert", False),
            "message": result.get("message", ""),
            "probability": result.get("probability")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/flood/health")
async def flood_health():
    return {"status": "healthy", "service": "flood_prediction"}
