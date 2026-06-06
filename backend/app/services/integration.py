# backend/services/integration.py
import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import logging
import json

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import ML modules
from ml.utils.model_loader import get_model_loader

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MLIntegrationService:
    """Complete ML integration service connecting backend APIs with ML models"""
    
    def __init__(self):
        """Initialize all services and ML models"""
        logger.info("Initializing ML Integration Service...")
        
        # Load ML models
        try:
            self.model_loader = get_model_loader()
            self.models_available = self._check_models()
            logger.info(f"ML Models loaded: {self.models_available}")
        except Exception as e:
            logger.warning(f"Could not load ML models: {e}")
            self.model_loader = None
            self.models_available = {}
        
        # Cache for predictions
        self.prediction_cache = {}
        self.cache_ttl = 3600  # 1 hour
        
        # Initialize API services (mock if keys not available)
        self.openweather_api_key = os.getenv('OPENWEATHER_API_KEY', '')
        self.groq_api_key = os.getenv('GROQ_API_KEY', '')
        
        logger.info("ML Integration Service initialized")
    
    def _check_models(self) -> Dict[str, bool]:
        """Check which models are available"""
        if not self.model_loader:
            return {}
        
        models = ['landslide', 'flood', 'earthquake', 'forestfire']
        available = {}
        
        for model_name in models:
            try:
                self.model_loader.load_model(model_name)
                available[model_name] = True
                logger.info(f"✓ {model_name} model loaded successfully")
            except Exception as e:
                available[model_name] = False
                logger.warning(f"✗ {model_name} model not available: {e}")
        
        return available
    
    def _get_mock_weather_data(self, lat: float, lon: float) -> Dict:
        """Generate mock weather data when API key is not available"""
        return {
            'main': {
                'temp': 22.5,
                'humidity': 75,
                'pressure': 1013
            },
            'wind': {
                'speed': 5.2
            },
            'rain': {
                '1h': 12.5
            },
            'weather': [{'description': 'moderate rain'}]
        }
    
    def _get_weather_data(self, lat: float, lon: float) -> Dict:
        """Fetch real weather data or use mock if API key missing"""
        if not self.openweather_api_key or self.openweather_api_key == 'your_openweather_api_key_here':
            logger.info(f"Using mock weather data for {lat}, {lon}")
            return self._get_mock_weather_data(lat, lon)
        
        try:
            import requests
            url = "http://api.openweathermap.org/data/2.5/weather"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.openweather_api_key,
                'units': 'metric'
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch weather data: {e}")
            return self._get_mock_weather_data(lat, lon)
    
    def _prepare_landslide_features(self, weather_data: Dict) -> List[float]:
        """Prepare features for landslide prediction"""
        main = weather_data.get('main', {})
        wind = weather_data.get('wind', {})
        rain = weather_data.get('rain', {})
        
        features = [
            main.get('temp', 20.0),           # Temperature
            main.get('humidity', 70.0),       # Humidity
            rain.get('1h', 0.0),              # Rainfall (1h)
            wind.get('speed', 5.0),           # Wind speed
            main.get('pressure', 1013),       # Pressure
            (main.get('humidity', 70) / 100) * rain.get('1h', 0)  # Soil moisture proxy
        ]
        
        logger.debug(f"Prepared landslide features: {features}")
        return features
    
    def predict_landslide(self, latitude: float, longitude: float, use_cache: bool = True) -> Dict[str, Any]:
        """Predict landslide risk for a location"""
        cache_key = f"landslide_{latitude}_{longitude}"
        
        # Check cache
        if use_cache and cache_key in self.prediction_cache:
            cached = self.prediction_cache[cache_key]
            if datetime.now() - cached['timestamp'] < timedelta(seconds=self.cache_ttl):
                logger.info(f"Returning cached prediction for {cache_key}")
                return cached['result']
        
        try:
            # Get weather data
            weather_data = self._get_weather_data(latitude, longitude)
            
            # Prepare features
            features = self._prepare_landslide_features(weather_data)
            
            # Make prediction
            risk_score = 0.5  # Default
            risk_confidence = 0.5
            
            if self.model_loader and self.models_available.get('landslide', False):
                try:
                    model = self.model_loader.load_model('landslide')
                    prediction = model.predict([features])
                    risk_score = float(prediction[0])
                    
                    if hasattr(model, 'predict_proba'):
                        proba = model.predict_proba([features])
                        risk_confidence = float(max(proba[0]))
                except Exception as e:
                    logger.error(f"Model prediction failed: {e}")
                    risk_score = self._rule_based_landslide_risk(features)
            else:
                risk_score = self._rule_based_landslide_risk(features)
            
            # Determine risk level
            if risk_score < 0.3:
                risk_level = "LOW"
                severity = "No immediate danger"
                recommendations = ["Monitor weather conditions", "No action needed"]
            elif risk_score < 0.6:
                risk_level = "MEDIUM"
                severity = "Possible landslides in vulnerable areas"
                recommendations = ["Stay alert", "Avoid steep slopes", "Monitor updates"]
            else:
                risk_level = "HIGH"
                severity = "High risk of landslides - Take immediate precautions"
                recommendations = ["Evacuate if in vulnerable area", "Avoid travel on mountain roads", "Follow emergency instructions"]
            
            result = {
                'status': 'success',
                'prediction_type': 'landslide',
                'prediction': {
                    'risk_score': round(risk_score, 3),
                    'risk_level': risk_level,
                    'confidence': round(risk_confidence, 3),
                    'severity': severity,
                    'recommendations': recommendations
                },
                'location': {
                    'latitude': latitude,
                    'longitude': longitude
                },
                'weather_data': {
                    'temperature': weather_data['main']['temp'],
                    'humidity': weather_data['main']['humidity'],
                    'rainfall_mm': weather_data.get('rain', {}).get('1h', 0),
                    'wind_speed': weather_data['wind']['speed']
                },
                'timestamp': datetime.now().isoformat()
            }
            
            # Cache result
            self.prediction_cache[cache_key] = {
                'result': result,
                'timestamp': datetime.now()
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Landslide prediction failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def predict_flood(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """Predict flood risk"""
        try:
            weather_data = self._get_weather_data(latitude, longitude)
            rainfall = weather_data.get('rain', {}).get('1h', 0)
            humidity = weather_data.get('main', {}).get('humidity', 70)
            
            # Simple flood risk calculation
            risk_score = min(1.0, (rainfall / 100) * 0.7 + (humidity / 100) * 0.3)
            
            if risk_score < 0.3:
                risk_level = "LOW"
            elif risk_score < 0.6:
                risk_level = "MEDIUM"
            else:
                risk_level = "HIGH"
            
            return {
                'status': 'success',
                'prediction_type': 'flood',
                'prediction': {
                    'risk_score': round(risk_score, 3),
                    'risk_level': risk_level,
                    'rainfall_mm': rainfall
                },
                'location': {'latitude': latitude, 'longitude': longitude},
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def predict_earthquake(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """Predict earthquake risk (simplified)"""
        # This is a simplified version - in reality you'd need historical data
        import random
        risk_score = random.uniform(0, 0.5)  # Random for demo
        
        return {
            'status': 'success',
            'prediction_type': 'earthquake',
            'prediction': {
                'risk_score': round(risk_score, 3),
                'risk_level': "LOW" if risk_score < 0.3 else "MEDIUM" if risk_score < 0.6 else "HIGH"
            },
            'location': {'latitude': latitude, 'longitude': longitude},
            'timestamp': datetime.now().isoformat()
        }
    
    def predict_all_hazards(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """Predict all hazards"""
        results = {
            'landslide': self.predict_landslide(latitude, longitude, use_cache=False),
            'flood': self.predict_flood(latitude, longitude),
            'earthquake': self.predict_earthquake(latitude, longitude)
        }
        
        # Calculate overall risk
        risks = []
        for hazard, result in results.items():
            if result.get('status') == 'success':
                risks.append(result['prediction']['risk_score'])
        
        overall_risk = sum(risks) / len(risks) if risks else 0
        
        if overall_risk < 0.3:
            overall_level = "LOW"
        elif overall_risk < 0.6:
            overall_level = "MEDIUM"
        else:
            overall_level = "HIGH"
        
        return {
            'status': 'success',
            'overall_risk': {
                'score': round(overall_risk, 3),
                'level': overall_level
            },
            'hazards': results,
            'timestamp': datetime.now().isoformat()
        }
    
    def list_available_models(self) -> Dict[str, Any]:
        """List all available models and their status"""
        return {
            'models': self.models_available,
            'cache_size': len(self.prediction_cache),
            'cache_ttl_seconds': self.cache_ttl
        }
    
    def _rule_based_landslide_risk(self, features: List[float]) -> float:
        """Fallback rule-based risk calculation"""
        rainfall = features[2] if len(features) > 2 else 0
        humidity = features[1] if len(features) > 1 else 70
        
        # Simple heuristic: high rainfall + high humidity = higher risk
        risk = (rainfall / 100) * 0.6 + (humidity / 100) * 0.4
        return min(1.0, max(0.0, risk))


# Singleton instance
_integration_service = None

def get_integration_service() -> MLIntegrationService:
    """Get singleton MLIntegrationService instance"""
    global _integration_service
    if _integration_service is None:
        _integration_service = MLIntegrationService()
    return _integration_service