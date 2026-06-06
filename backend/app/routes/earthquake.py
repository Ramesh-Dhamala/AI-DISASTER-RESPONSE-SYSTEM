from fastapi import APIRouter
from app.services.usgs_service import fetch_nepal_earthquakes

router = APIRouter()


@router.get("/earthquake")
def get_earthquakes():

    earthquakes = fetch_nepal_earthquakes()

    if len(earthquakes) == 0:
        return {
            "message": "No earthquakes detected in Nepal"
        }

    return {
        "count": len(earthquakes),
        "earthquakes": earthquakes
    }