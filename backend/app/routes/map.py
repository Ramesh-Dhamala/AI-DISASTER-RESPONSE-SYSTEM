from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

router = APIRouter()

class DisasterZone(BaseModel):
    zone_id: str
    type: str  # flood, earthquake, landslide, cyclone
    risk_level: str  # low, medium, high
    coordinates: List[Dict[str, float]]
    alert_count: int
    last_updated: str

@router.get("/map/layers")
async def get_map_layers():
    """
    Get available map layers for disaster visualization
    """
    return {
        "success": True,
        "layers": [
            {
                "id": "flood_zones",
                "name": "Flood Risk Zones",
                "type": "polygon",
                "visible": True,
                "opacity": 0.7
            },
            {
                "id": "earthquake_faults",
                "name": "Earthquake Fault Lines",
                "type": "line",
                "visible": True,
                "opacity": 0.8
            },
            {
                "id": "landslide_susceptibility",
                "name": "Landslide Susceptibility",
                "type": "heatmap",
                "visible": False,
                "opacity": 0.6
            },
            {
                "id": "weather_radar",
                "name": "Weather Radar",
                "type": "raster",
                "visible": True,
                "opacity": 0.5
            },
            {
                "id": "evacuation_routes",
                "name": "Evacuation Routes",
                "type": "line",
                "visible": False,
                "opacity": 0.9
            }
        ]
    }

@router.get("/map/disaster-zones")
async def get_disaster_zones(
    zone_type: Optional[str] = Query(None, description="Filter by zone type"),
    risk_level: Optional[str] = Query(None, description="Filter by risk level")
):
    """
    Get disaster affected zones with their risk levels
    """
    # Mock data - replace with actual database
    zones = [
        {
            "zone_id": "Z001",
            "type": "flood",
            "risk_level": "high",
            "coordinates": [
                {"lat": 28.5, "lon": 77.0},
                {"lat": 28.6, "lon": 77.1},
                {"lat": 28.4, "lon": 77.2}
            ],
            "affected_population": 15000,
            "alert_count": 3,
            "last_updated": datetime.now().isoformat()
        },
        {
            "zone_id": "Z002",
            "type": "earthquake",
            "risk_level": "medium",
            "coordinates": [
                {"lat": 29.0, "lon": 78.0},
                {"lat": 29.1, "lon": 78.1},
                {"lat": 28.9, "lon": 78.2}
            ],
            "affected_population": 5000,
            "alert_count": 1,
            "last_updated": datetime.now().isoformat()
        },
        {
            "zone_id": "Z003",
            "type": "landslide",
            "risk_level": "high",
            "coordinates": [
                {"lat": 27.5, "lon": 79.0},
                {"lat": 27.6, "lon": 79.1},
                {"lat": 27.4, "lon": 79.2}
            ],
            "affected_population": 8000,
            "alert_count": 2,
            "last_updated": datetime.now().isoformat()
        }
    ]
    
    # Apply filters
    if zone_type:
        zones = [z for z in zones if z["type"] == zone_type]
    if risk_level:
        zones = [z for z in zones if z["risk_level"] == risk_level]
    
    return {
        "success": True,
        "count": len(zones),
        "zones": zones
    }

@router.post("/map/update-zone")
async def update_disaster_zone(zone_data: Dict[str, Any]):
    """
    Update disaster zone information (requires admin authentication)
    """
    return {
        "success": True,
        "message": f"Zone {zone_data.get('zone_id', 'unknown')} updated successfully",
        "data": zone_data
    }

@router.get("/map/evacuation-routes/{zone_id}")
async def get_evacuation_routes(zone_id: str):
    """
    Get evacuation routes for a specific disaster zone
    """
    routes = {
        "Z001": {
            "primary_route": [
                {"lat": 28.5, "lon": 77.0},
                {"lat": 28.7, "lon": 77.3},
                {"lat": 28.9, "lon": 77.5}
            ],
            "alternate_route": [
                {"lat": 28.5, "lon": 77.0},
                {"lat": 28.4, "lon": 76.8},
                {"lat": 28.3, "lon": 76.6}
            ],
            "shelters": [
                {"name": "City Shelter", "lat": 28.9, "lon": 77.5, "capacity": 500},
                {"name": "School Shelter", "lat": 28.8, "lon": 77.4, "capacity": 300}
            ]
        }
    }
    
    result = routes.get(zone_id, {
        "primary_route": [],
        "alternate_route": [],
        "shelters": [],
        "message": "No evacuation routes defined for this zone"
    })
    
    return {
        "success": True,
        "zone_id": zone_id,
        "evacuation_data": result
    }

@router.get("/map/heatmap/{disaster_type}")
async def get_risk_heatmap(disaster_type: str):
    """
    Get heatmap data for risk visualization
    """
    # Mock heatmap data
    heatmap_data = []
    for i in range(20):
        heatmap_data.append({
            "lat": round(28.0 + (i * 0.1), 2),
            "lon": round(77.0 + (i * 0.1), 2),
            "intensity": round(i / 20, 2),
            "risk_score": round(i * 5, 2)
        })
    
    return {
        "success": True,
        "disaster_type": disaster_type,
        "data": heatmap_data
    }