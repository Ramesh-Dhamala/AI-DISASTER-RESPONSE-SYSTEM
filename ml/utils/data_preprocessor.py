def preprocess_weather_data(weather_data: dict) -> list:
    """Convert weather API data to model features"""
    return [
        weather_data['main']['temp'],
        weather_data['main']['humidity'],
        weather_data['wind']['speed'],
        weather_data.get('rain', {}).get('1h', 0)
    ]