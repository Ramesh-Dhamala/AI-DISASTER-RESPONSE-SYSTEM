from fastapi import APIRouter
from app.services.alert_service import generate_alert

router = APIRouter()

@router.post("/disaster-alert")
def disaster_alert(request: dict):

    flood_risk = request.get("flood_risk")
    landslide_risk = request.get("landslide_risk")
    earthquake_risk = request.get("earthquake_risk")

    if not flood_risk or not landslide_risk or not earthquake_risk:
        return {
            "success": False,
            "message": "All risk values are required"
        }

    alert = generate_alert(
        flood_risk,
        landslide_risk,
        earthquake_risk
    )

    return {
        "success": True,
        "alert": alert
    }