import math

# -----------------------------
# SAMPLE SAFE PLACES DATABASE
# (later you can replace with Google Maps API / real DB)
# -----------------------------
SAFE_PLACES = [
    {
        "name": "Kathmandu Emergency Shelter",
        "type": "shelter",
        "lat": 27.7172,
        "lon": 85.3240
    },
    {
        "name": "Tribhuvan University Teaching Hospital",
        "type": "hospital",
        "lat": 27.7350,
        "lon": 85.3300
    },
    {
        "name": "Local School Safe Zone",
        "type": "school",
        "lat": 27.7100,
        "lon": 85.3200
    }
]

# -----------------------------
# DISTANCE CALCULATOR (Haversine Formula)
# -----------------------------
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in KM

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2 +
        math.cos(math.radians(lat1)) *
        math.cos(math.radians(lat2)) *
        math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # distance in KM


# -----------------------------
# MAIN FUNCTION
# -----------------------------
def get_safe_place(user_location: dict):
    """
    user_location = {
        "lat": 27.72,
        "lon": 85.32
    }
    """

    if not user_location:
        return {
            "message": "Location not provided",
            "place": None
        }

    user_lat = user_location.get("lat")
    user_lon = user_location.get("lon")

    if user_lat is None or user_lon is None:
        return {
            "message": "Invalid location",
            "place": None
        }

    nearest_place = None
    min_distance = float("inf")

    # -----------------------------
    # FIND NEAREST SAFE PLACE
    # -----------------------------
    for place in SAFE_PLACES:
        dist = calculate_distance(
            user_lat,
            user_lon,
            place["lat"],
            place["lon"]
        )

        if dist < min_distance:
            min_distance = dist
            nearest_place = place

    return {
        "name": nearest_place["name"],
        "type": nearest_place["type"],
        "distance_km": round(min_distance, 2),
        "lat": nearest_place["lat"],
        "lon": nearest_place["lon"],
        "map_link": f"https://www.google.com/maps?q={nearest_place['lat']},{nearest_place['lon']}"
    }