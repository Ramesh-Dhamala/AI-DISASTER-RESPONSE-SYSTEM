import requests
from datetime import datetime

USGS_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"

# Nepal bounding box
MIN_LAT = 26.0
MAX_LAT = 31.0

MIN_LON = 80.0
MAX_LON = 89.0


def fetch_nepal_earthquakes():
    response = requests.get(USGS_URL)
    data = response.json()

    earthquakes = []

    for feature in data["features"]:

        props = feature["properties"]
        coords = feature["geometry"]["coordinates"]

        longitude = coords[0]
        latitude = coords[1]

        # Check if earthquake is inside Nepal region
        if (
            MIN_LAT <= latitude <= MAX_LAT
            and
            MIN_LON <= longitude <= MAX_LON
        ):

            magnitude = props["mag"]

            # Skip invalid magnitudes
            if magnitude is None:
                continue

            # Only show earthquakes above 0 magnitude
            if magnitude > 0:

                readable_time = datetime.fromtimestamp(
                    props["time"] / 1000
                ).strftime("%Y-%m-%d %H:%M:%S")

                if magnitude >= 6:
                    risk = "HIGH"
                elif magnitude >= 4:
                    risk = "MEDIUM"
                else:
                    risk = "LOW"

                earthquakes.append({
                    "magnitude": magnitude,
                    "location": props["place"],
                    "time": readable_time,
                    "risk": risk,
                    "latitude": latitude,
                    "longitude": longitude
                })

    return earthquakes