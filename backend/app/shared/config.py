# shared/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Project paths
    PROJECT_ROOT = Path(__file__).parent.parent
    MODEL_DIR = PROJECT_ROOT / 'ml' / 'trained_models'
    
    # API Keys - Use environment variables
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', '')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
    
    # Server settings
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Model settings
    MODEL_NAMES = ['landslide', 'flood', 'earthquake', 'forestfire']
    PREDICTION_CACHE_TTL = int(os.getenv('PREDICTION_CACHE_TTL', 3600))