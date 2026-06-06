from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import random

router = APIRouter()

class EarthquakePredictionRequest(BaseModel):
    latitude: float
    longitude: float
    magnitude_threshold: Optional[float] = 2.5

class EarthquakeInfo(BaseModel):
    magnitude: float
    place: str
    time: str
    latitude: float
    longitude: float
    alert_level: str

@router.get("/earthquakes/recent")
async def get_recent_earthquakes(
    min_magnitude: float = 2.5, 
    limit: int = 10
):
    """
    Get recent earthquake data (mock data - replace with USGS API)
    """
    # Mock earthquake data (replace with actual USGS API call)
    mock_earthquakes = []
    for i in range(min(limit, 5)):
        mock_earthquakes.append({
            "magnitude": round(random.uniform(min_magnitude, 7.5), 1),
            "place": f"Location {i+1}",
            "time": datetime.now().isoformat(),
            "latitude": round(random.uniform(-90, 90), 2),
            "longitude": round(random.uniform(-180, 180), 2),
            "alert_level": random.choice(["green", "yellow", "orange", "red"])
        })
    
    return {
        "success": True,
        "count": len(mock_earthquakes),
        "earthquakes": mock_earthquakes,
        "message": "Using mock data. Connect to USGS API for real data."
    }

@router.post("/earthquake/predict")
async def predict_earthquake_risk(request: EarthquakePredictionRequest):
    """
    Predict earthquake risk for a specific location
    """
    # Simple risk calculation based on location
    # In reality, this would use ML models and historical data
    
    risk_score = 0
    
    # Pacific Ring of Fire (high risk areas)
    ring_of_fire_zones = [
        (-20, -70, 10, -50),  # South America
        (20, 120, 50, 150),    # Asia/Japan
        (30, -130, 60, -120)   # West US
    ]
    
    for lat_min, lon_min, lat_max, lon_max in ring_of_fire_zones:
        if lat_min <= request.latitude <= lat_max and lon_min <= request.longitude <= lon_max:
            risk_score += 60
    
    # Random factor for demo (replace with real model)
    risk_score += random.randint(0, 40)
    
    if risk_score > 70:
        risk_level = "HIGH"
        alert = True
        message = "High earthquake risk detected! Prepare emergency kit."
    elif risk_score > 40:
        risk_level = "MEDIUM"
        alert = True
        message = "Moderate earthquake risk. Stay alert."
    else:
        risk_level = "LOW"
        alert = False
        message = "Low earthquake risk."
    
    return {
        "success": True,
        "disaster_type": "earthquake",
        "risk_level": risk_level,
        "risk_score": risk_score,
        "alert": alert,
        "message": message,
        "recommendations": [
            "Secure heavy furniture",
            "Prepare emergency kit",
            "Know drop-cover-hold technique"
        ] if alert else ["Stay prepared, no immediate threat"]
    }

@router.get("/earthquake/historical")
async def get_historical_earthquakes(
    latitude: float,
    longitude: float,
    radius_km: int = 100
):
    """
    Get historical earthquake data for a location
    """
    return {
        "success": True,
        "location": {"lat": latitude, "lon": longitude},
        "radius_km": radius_km,
        "historical_events": [
            {"year": 2020, "magnitude": 5.2, "depth_km": 15},
            {"year": 2018, "magnitude": 4.8, "depth_km": 12},
            {"year": 2015, "magnitude": 6.1, "depth_km": 20}
        ],
        "message": "Historical data from database (mock data)"
    }