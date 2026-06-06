import requests

# 🌍 OpenWeather API key (replace this)
API_KEY = "aed21e0573060c3d85e36edae7d8e18a"


def get_weather(city: str):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    # ❌ Handle invalid city or API error
    if response.status_code != 200:
        return {
            "error": True,
            "message": "City not found or API error",
            "details": data
        }

    # 🌦️ Extract useful weather data
    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    rain = "rain" in data and "1h" in data.get("rain", {})

    result = {
        "city": city,
        "temperature": temperature,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "rain": rain
    }

    # ⚠️ DISASTER RISK LOGIC (VERY IMPORTANT FOR HACKATHON)

    # 🌊 Flood risk
    if rain and humidity > 70:
        result["risk"] = "HIGH"
        result["disaster"] = "Flood"
        result["message"] = "Heavy rain + high humidity → Flood risk"

    # 🔥 Heatwave risk
    elif temperature >= 35:
        result["risk"] = "HIGH"
        result["disaster"] = "Heatwave"
        result["message"] = "Extreme temperature → Heatwave risk"

    # 🌬️ Storm risk
    elif wind_speed >= 15:
        result["risk"] = "MEDIUM"
        result["disaster"] = "Storm"
        result["message"] = "High wind speed → Storm risk"

    # 🟢 Safe
    else:
        result["risk"] = "LOW"
        result["disaster"] = "None"
        result["message"] = "Normal weather conditions"

    return result