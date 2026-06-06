# backend/api/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
from pathlib import Path
import logging

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import config first (no circular dependency)
from shared.config import Config

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lazy import to avoid circular imports
_integration_service = None

def get_integration_service():
    """Lazy load integration service to avoid circular imports"""
    global _integration_service
    if _integration_service is None:
        from backend.services.integration import MLIntegrationService
        _integration_service = MLIntegrationService()
    return _integration_service

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'ML Integration Service',
        'version': '1.0.0'
    })

@app.route('/model-info', methods=['GET'])
def model_info():
    """Get detailed information about available models and endpoints"""
    try:
        service = get_integration_service()
        
        # Get model status
        models_status = service.list_available_models()
        
        # Get detailed model info
        model_details = {}
        for model_name in ['landslide', 'flood', 'earthquake', 'forestfire']:
            if service.models_available.get(model_name, False):
                try:
                    model = service.model_loader.load_model(model_name)
                    model_details[model_name] = {
                        'available': True,
                        'type': type(model).__name__,
                        'has_predict_proba': hasattr(model, 'predict_proba')
                    }
                    
                    if hasattr(model, 'classes_'):
                        model_details[model_name]['classes'] = model.classes_.tolist()
                        
                except Exception as e:
                    model_details[model_name] = {
                        'available': False,
                        'error': str(e)
                    }
            else:
                model_details[model_name] = {
                    'available': False,
                    'reason': 'Model file not found or failed to load'
                }
        
        return jsonify({
            'status': 'success',
            'service_name': 'AI Disaster Response System',
            'version': '1.0.0',
            'available_endpoints': {
                'GET': [
                    '/health',
                    '/model-info',
                    '/api/models'
                ],
                'POST': [
                    '/api/predict/landslide',
                    '/api/predict/flood',
                    '/api/predict/earthquake',
                    '/api/predict/all'
                ]
            },
            'models': model_details,
            'cache_info': models_status,
            'example_request': {
                'endpoint': '/api/predict/landslide',
                'method': 'POST',
                'body': {
                    'latitude': 27.7172,
                    'longitude': 85.3240
                }
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error in model-info: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/models', methods=['GET'])
def list_models():
    """List all available models"""
    try:
        service = get_integration_service()
        models = service.list_available_models()
        return jsonify(models), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict/landslide', methods=['POST'])
def predict_landslide():
    """Predict landslide risk for a location"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        lat = data.get('latitude')
        lon = data.get('longitude')
        
        if lat is None or lon is None:
            return jsonify({'error': 'latitude and longitude are required'}), 400
        
        service = get_integration_service()
        result = service.predict_landslide(lat, lon)
        
        status_code = 200 if result.get('status') == 'success' else 500
        return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Error in predict_landslide: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict/flood', methods=['POST'])
def predict_flood():
    """Predict flood risk for a location"""
    try:
        data = request.json
        lat = data.get('latitude')
        lon = data.get('longitude')
        
        if lat is None or lon is None:
            return jsonify({'error': 'latitude and longitude are required'}), 400
        
        service = get_integration_service()
        result = service.predict_flood(lat, lon)
        
        return jsonify(result), 200 if result.get('status') == 'success' else 500
        
    except Exception as e:
        logger.error(f"Error in predict_flood: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict/earthquake', methods=['POST'])
def predict_earthquake():
    """Predict earthquake risk for a location"""
    try:
        data = request.json
        lat = data.get('latitude')
        lon = data.get('longitude')
        
        if lat is None or lon is None:
            return jsonify({'error': 'latitude and longitude are required'}), 400
        
        service = get_integration_service()
        result = service.predict_earthquake(lat, lon)
        
        return jsonify(result), 200 if result.get('status') == 'success' else 500
        
    except Exception as e:
        logger.error(f"Error in predict_earthquake: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict/all', methods=['POST'])
def predict_all_hazards():
    """Predict all hazards for a location"""
    try:
        data = request.json
        lat = data.get('latitude')
        lon = data.get('longitude')
        
        if lat is None or lon is None:
            return jsonify({'error': 'latitude and longitude are required'}), 400
        
        service = get_integration_service()
        result = service.predict_all_hazards(lat, lon)
        
        return jsonify(result), 200 if result.get('status') == 'success' else 500
        
    except Exception as e:
        logger.error(f"Error in predict_all_hazards: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host=Config.API_HOST, port=Config.API_PORT, debug=Config.DEBUG)