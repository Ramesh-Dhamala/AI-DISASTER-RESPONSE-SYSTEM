import joblib
import numpy as np
from app.config import FLOOD_MODEL_PATH
import os

# Load model
try:
    if os.path.exists(FLOOD_MODEL_PATH):
        flood_model = joblib.load(FLOOD_MODEL_PATH)
        print("✅ Flood model loaded successfully")
    else:
        flood_model = None
        print(f"⚠️ Model not found at: {FLOOD_MODEL_PATH}")
except Exception as e:
    flood_model = None
    print(f"⚠️ Flood model not loaded: {e}")

def predict_flood_risk(data: dict):
    # Rest of the function remains the same
    if flood_model is None:
        return {
            "type": "FLOOD",
            "risk": "UNKNOWN",
            "alert": False,
            "message": "Flood model not loaded"
        }
    
    try:
        features = np.array([[
            data.get("rainfall", 0),
            data.get("river_level", 0),
            data.get("humidity", 0),
            data.get("temperature", 0)
        ]])
        
        prediction = flood_model.predict(features)[0]
        
        try:
            probability = flood_model.predict_proba(features)[0][1]
        except:
            probability = None
        
        if prediction == 1 or (probability is not None and probability > 0.5):
            return {
                "type": "FLOOD",
                "risk": "HIGH",
                "alert": True,
                "message": "Flood risk detected",
                "probability": float(probability) if probability else None
            }
        
        return {
            "type": "FLOOD",
            "risk": "LOW",
            "alert": False,
            "message": "No flood risk",
            "probability": float(probability) if probability else None
        }
    
    except Exception as e:
        return {
            "type": "FLOOD",
            "risk": "ERROR",
            "alert": False,
            "message": str(e)
        }