from fastapi import APIRouter
from app.services.flood_service import predict_flood

router = APIRouter()

@router.post("/flood")
def flood_prediction(request: dict):

    features = request.get("features")

    # validation
    if not features:
        return {
            "success": False,
            "message": "Features are required"
        }

    # get prediction
    risk = predict_flood(features)

    return {
        "success": True,
        "disaster": "flood",
        "risk_level": risk
    }