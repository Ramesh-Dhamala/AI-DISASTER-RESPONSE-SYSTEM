# backend/services/openweather_service.py
import os
import requests
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class OpenWeatherService:
    """Service for OpenWeather API integration"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('OPENWEATHER_API_KEY', '')
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    def get_current_weather(self, lat: float, lon: float) -> Dict:
        """Get current weather data"""
        if not self.api_key:
            logger.warning("No OpenWeather API key provided")
            return self._get_mock_data(lat, lon)
        
        try:
            endpoint = f"{self.base_url}/weather"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric'
            }
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get weather data: {e}")
            return self._get_mock_data(lat, lon)
    
    def _get_mock_data(self, lat: float, lon: float) -> Dict:
        """Return mock data for testing"""
        return {
            'main': {'temp': 22.5, 'humidity': 75, 'pressure': 1013},
            'wind': {'speed': 5.2},
            'rain': {'1h': 12.5},
            'weather': [{'description': 'moderate rain', 'main': 'Rain'}]
        }