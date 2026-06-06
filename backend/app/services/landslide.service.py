def predict_landslide(data: dict):
    """
    Rule-based landslide prediction (NO ML MODEL REQUIRED)
    """

    rainfall = data.get("rainfall", 0)
    slope = data.get("slope", 0)
    soil_moisture = data.get("soil_moisture", 0)
    temperature = data.get("temperature", 25)

    # -----------------------------
    # SIMPLE DISASTER LOGIC
    # -----------------------------

    score = 0

    # rainfall impact
    if rainfall > 120:
        score += 3
    elif rainfall > 80:
        score += 2
    elif rainfall > 50:
        score += 1

    # slope impact (VERY IMPORTANT for landslide)
    if slope > 35:
        score += 3
    elif slope > 25:
        score += 2
    elif slope > 15:
        score += 1

    # soil moisture impact
    if soil_moisture > 75:
        score += 2
    elif soil_moisture > 50:
        score += 1

    # -----------------------------
    # FINAL RISK DECISION
    # -----------------------------

    if score >= 6:
        risk = "HIGH"
        alert = True
        message = "⚠️ High landslide risk detected. Evacuate immediately."

    elif score >= 3:
        risk = "MEDIUM"
        alert = True
        message = "⚠️ Moderate landslide risk. Stay alert."

    else:
        risk = "LOW"
        alert = False
        message = "✅ Low landslide risk."

    return {
        "type": "LANDSLIDE",
        "risk": risk,
        "alert": alert,
        "message": message,
        "score": score
    }