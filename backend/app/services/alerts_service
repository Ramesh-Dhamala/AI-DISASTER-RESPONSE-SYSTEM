def generate_alert(flood_risk: str, landslide_risk: str, earthquake_risk: str):

    # 🔴 CRITICAL LEVEL
    if (
        flood_risk == "HIGH" or
        landslide_risk == "HIGH" or
        earthquake_risk == "CRITICAL"
    ):
        return {
            "notify": True,
            "level": "CRITICAL",
            "message": "🚨 EXTREME DISASTER RISK! Immediate evacuation required. Follow authorities."
        }

    # 🟠 WARNING LEVEL
    if (
        flood_risk == "MEDIUM" or
        landslide_risk == "MEDIUM" or
        earthquake_risk == "WARNING"
    ):
        return {
            "notify": True,
            "level": "WARNING",
            "message": "⚠️ Disaster risk detected. Stay alert and avoid dangerous areas."
        }

    # 🟢 SAFE STATE
    return {
        "notify": False,
        "level": "SAFE",
        "message": "No disaster risk detected."
    }