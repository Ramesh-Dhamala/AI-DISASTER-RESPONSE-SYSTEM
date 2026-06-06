def predict_flood_risk(data: dict):
    """
    Rule-based flood prediction (NO ML MODEL REQUIRED)
    """

    rainfall = data.get("rainfall", 0)
    river_level = data.get("river_level", 0)
    humidity = data.get("humidity", 0)

    # -------------------------
    # SIMPLE RULE LOGIC
    # -------------------------

    if rainfall > 150 or river_level > 6.5:
        risk_level = "HIGH"
        alert = True

    elif rainfall > 80 or river_level > 4.5:
        risk_level = "MEDIUM"
        alert = True

    else:
        risk_level = "LOW"
        alert = False

    return {
        "status": "success",
        "risk_level": risk_level,
        "alert": alert,
        "message": f"Flood risk is {risk_level}"
    }