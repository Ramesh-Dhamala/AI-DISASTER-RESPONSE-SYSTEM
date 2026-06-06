import math

# -----------------------------
# SAMPLE SAFE LOCATIONS DATABASE
# (Later you can replace with real API like Google Places)
# -----------------------------
SAFE_PLACES = [
    {
        "name": "Kathmandu Hospital",
        "type": "hospital",
        "lat": 27.7172,
        "lon": 85.3240
    },
    {
        "name": "Bir Hospital",
        "type": "hospital",
        "lat": 27.7040,
        "lon": 85.3070
    },
    {
        "name": "Tundikhel Open Ground",
        "type": "safe_zone",
        "lat": 27.7025,
        "lon": 85.3150
    },
    {
        "name": "Police Headquarters",
        "type": "police",
        "lat": 27.7050,
        "lon": 85.3200
    }
]


# -----------------------------
# DISTANCE CALCULATOR (Haversine Formula)
# -----------------------------
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2 +
        math.cos(math.radians(lat1)) *
        math.cos(math.radians(lat2)) *
        math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


# -----------------------------
# MAIN FUNCTION
# -----------------------------
def get_nearest_safe_places(user_lat: float, user_lon: float, limit: int = 3):
    results = []

    for place in SAFE_PLACES:
        dist = calculate_distance(
            user_lat,
            user_lon,
            place["lat"],
            place["lon"]
        )

        results.append({
            "name": place["name"],
            "type": place["type"],
            "distance_km": round(dist, 2)
        })

    # sort by nearest
    results = sorted(results, key=lambda x: x["distance_km"])

    return {
        "status": "success",
        "nearest_safe_places": results[:limit]
    }