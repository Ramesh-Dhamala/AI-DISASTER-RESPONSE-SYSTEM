import os
import joblib
import numpy as np

# -----------------------------
# LOAD MODEL (your friend's ML model)
# -----------------------------
MODEL_PATH = os.path.join("ml", "models", "flood_model.pkl")

try:
    flood_model = joblib.load(MODEL_PATH)
except Exception as e:
    flood_model = None
    print("⚠️ Flood model not loaded:", e)


# -----------------------------
# PREDICTION FUNCTION
# -----------------------------
def predict_flood_risk(data: dict):
    """
    Predict flood risk based on input parameters.

    Expected input example:
    {
        "rainfall": 120,
        "river_level": 5.2,
        "humidity": 80,
        "temperature": 28
    }
    """

    if flood_model is None:
        return {
            "status": "error",
            "message": "Flood model not loaded"
        }

    try:
        # Convert input into model format
        features = np.array([[
            data.get("rainfall", 0),
            data.get("river_level", 0),
            data.get("humidity", 0),
            data.get("temperature", 0)
        ]])

        prediction = flood_model.predict(features)[0]

        # If model gives probability
        try:
            probability = flood_model.predict_proba(features)[0][1]
        except:
            probability = None

        # -----------------------------
        # ALERT LOGIC
        # -----------------------------
        if prediction == 1 or (probability and probability > 0.5):
            risk_level = "HIGH"
            alert = True
        else:
            risk_level = "LOW"
            alert = False

        return {
            "status": "success",
            "risk_level": risk_level,
            "alert": alert,
            "prediction": int(prediction),
            "probability": float(probability) if probability else None
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }