from fastapi import APIRouter
from app.services.landslide_service import predict_landslide

router = APIRouter()

@router.post("/landslide")
def landslide_prediction(request: dict):

    features = request.get("features")

    # validation
    if not features:
        return {
            "success": False,
            "message": "Features are required"
        }

    # get ML prediction
    risk = predict_landslide(features)

    return {
        "success": True,
        "disaster": "landslide",
        "risk_level": risk
    }