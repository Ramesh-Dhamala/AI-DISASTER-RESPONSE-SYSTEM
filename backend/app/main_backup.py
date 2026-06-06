# main.py
#!/usr/bin/env python3
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from shared.config import Config

# Import app after path is set
from backend.api.app import app

if __name__ == '__main__':
    print(f"""
    🚀 ML Integration Service Starting...
    📍 Host: {Config.API_HOST}
    🔌 Port: {Config.API_PORT}
    🐛 Debug: {Config.DEBUG}
    
    Available endpoints:
    • POST http://localhost:{Config.API_PORT}/api/predict/landslide
    • POST http://localhost:{Config.API_PORT}/api/predict/flood  
    • POST http://localhost:{Config.API_PORT}/api/predict/earthquake
    • POST http://localhost:{Config.API_PORT}/api/predict/all
    • GET  http://localhost:{Config.API_PORT}/health
    • GET  http://localhost:{Config.API_PORT}/api/models
    """)
    
    app.run(
        host=Config.API_HOST,
        port=Config.API_PORT,
        debug=Config.DEBUG
    )