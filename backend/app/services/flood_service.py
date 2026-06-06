import numpy as np

def predict_flood_risk(data: dict):
    # Simple rule-based flood prediction
    risk_score = 0
    
    # Rainfall factor (mm)
    rainfall = data.get("rainfall", 0)
    if rainfall > 100:
        risk_score += 3
    elif rainfall > 50:
        risk_score += 2
    elif rainfall > 25:
        risk_score += 1
    
    # River level factor (meters)
    river_level = data.get("river_level", 0)
    if river_level > 6:
        risk_score += 3
    elif river_level > 4:
        risk_score += 2
    elif river_level > 2:
        risk_score += 1
    
    # Humidity factor (%)
    humidity = data.get("humidity", 0)
    if humidity > 85:
        risk_score += 2
    elif humidity > 70:
        risk_score += 1
    
    # Calculate risk level
    if risk_score >= 6:
        risk = "HIGH"
        alert = True
        message = "Severe flood risk! Take immediate action."
        probability = 0.85
    elif risk_score >= 4:
        risk = "MEDIUM"
        alert = True
        message = "Moderate flood risk. Stay alert."
        probability = 0.60
    elif risk_score >= 2:
        risk = "LOW"
        alert = False
        message = "Low flood risk."
        probability = 0.30
    else:
        risk = "VERY_LOW"
        alert = False
        message = "Minimal flood risk."
        probability = 0.10
    
    return {
        "type": "FLOOD",
        "risk": risk,
        "alert": alert,
        "message": message,
        "probability": probability,
        "risk_score": risk_score
    }
