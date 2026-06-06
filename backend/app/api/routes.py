# backend/api/routes.py
from flask import Blueprint, request, jsonify
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Create blueprint
api_bp = Blueprint('api', __name__)

# Lazy import to avoid circular imports
_integration_service = None

def get_service():
    global _integration_service
    if _integration_service is None:
        from backend.services.integration import MLIntegrationService
        _integration_service = MLIntegrationService()
    return _integration_service

@api_bp.route('/predict/landslide', methods=['POST'])
def predict_landslide():
    data = request.json
    service = get_service()
    result = service.predict_landslide(data.get('latitude'), data.get('longitude'))
    return jsonify(result)