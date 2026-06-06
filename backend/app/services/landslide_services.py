import numpy as np
import joblib
import os

# -----------------------------
# LOAD MODEL
# -----------------------------
MODEL_PATH = os.path.join("app", "models", "landslide_model.pkl")

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    print("⚠️ Landslide model not loaded:", e)


# -----------------------------
# MAIN PREDICTION FUNCTION
# -----------------------------
def predict_landslide(data: dict):
    """
    Predict landslide risk using ML model
    """

    if model is None:
        return {
            "type": "LANDSLIDE",
            "risk": "UNKNOWN",
            "alert": False,
            "message": "Model not loaded"
        }

    try:
        # Convert API input → model format
        features = np.array([[
            data.get("rainfall", 0),
            data.get("slope", 0),
            data.get("soil_moisture", 0),
            data.get("temperature", 0)
        ]])

        prediction = model.predict(features)[0]

        # -----------------------------
        # RISK MAPPING
        # -----------------------------
        if prediction == 2:
            risk = "HIGH"
            alert = True
            message = "High landslide risk detected"

        elif prediction == 1:
            risk = "MEDIUM"
            alert = True
            message = "Moderate landslide risk detected"

        else:
            risk = "LOW"
            alert = False
            message = "No landslide risk"

        return {
            "type": "LANDSLIDE",
            "risk": risk,
            "alert": alert,
            "message": message
        }

    except Exception as e:
        return {
            "type": "LANDSLIDE",
            "risk": "ERROR",
            "alert": False,
            "message": str(e)
        }