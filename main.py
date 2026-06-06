from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import joblib
import os
import numpy as np

app = Flask(__name__)
CORS(app)

# Global variables
model = None
vectorizer = None

def load_ml_models():
    """Load ML models if available"""
    global model, vectorizer
    
    try:
        model_path = 'models/saved/disaster_model.pkl'
        vectorizer_path = 'models/saved/vectorizer.pkl'
        
        if os.path.exists(model_path) and os.path.exists(vectorizer_path):
            model = joblib.load(model_path)
            vectorizer = joblib.load(vectorizer_path)
            print("✅ ML models loaded successfully!")
            return True
        else:
            print(f"⚠️  Model files not found at: {model_path}")
            print("   Train a model first with: python train_simple_model.py")
            return False
    except Exception as e:
        print(f"❌ Error loading models: {e}")
        return False

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'name': 'AI Disaster Response System',
        'version': '1.0.0',
        'status': 'running',
        'ml_available': model is not None,
        'endpoints': {
            'GET /health': 'System health check',
            'GET /model-info': 'Get model information',
            'GET /api/models': 'List available models',
            'POST /predict': 'Predict disaster from text message',
            'POST /api/predict/landslide': 'Predict landslide risk',
            'POST /api/predict/flood': 'Predict flood risk',
            'POST /api/predict/earthquake': 'Predict earthquake risk',
            'POST /api/predict/all': 'Predict all disaster types'
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'ml_models_loaded': model is not None,
        'ml_library_available': True,
        'service': 'disaster-response-api'
    })

@app.route('/model-info', methods=['GET'])
def model_info():
    """Get detailed information about loaded models"""
    if model is None:
        return jsonify({'error': 'No models loaded'}), 503
    
    return jsonify({
        'status': 'success',
        'model_type': type(model).__name__,
        'is_loaded': True,
        'features_count': vectorizer.get_feature_names_out().shape[0] if vectorizer else 0,
        'classes': list(model.classes_) if hasattr(model, 'classes_') else [],
        'sample_classes': ['earthquake', 'flood', 'hurricane', 'wildfire', 'tornado', 'normal'],
        'endpoints_available': [
            'POST /predict - Text classification',
            'POST /api/predict/landslide - Geo-spatial prediction',
            'POST /api/predict/flood - Geo-spatial prediction',
            'POST /api/predict/earthquake - Geo-spatial prediction',
            'POST /api/predict/all - All disaster types'
        ]
    })

@app.route('/api/models', methods=['GET'])
def list_models():
    """List all available models"""
    models_list = {
        'text_classifier': {
            'name': 'Disaster Message Classifier',
            'type': 'RandomForestClassifier',
            'status': 'loaded' if model else 'not_loaded',
            'endpoint': '/predict'
        },
        'landslide_model': {
            'name': 'Landslide Risk Predictor',
            'type': 'Geo-spatial Model',
            'status': 'simulation_mode',
            'endpoint': '/api/predict/landslide',
            'description': 'Predicts landslide risk based on location'
        },
        'flood_model': {
            'name': 'Flood Risk Predictor',
            'type': 'Geo-spatial Model',
            'status': 'simulation_mode',
            'endpoint': '/api/predict/flood',
            'description': 'Predicts flood risk based on location'
        },
        'earthquake_model': {
            'name': 'Earthquake Risk Predictor',
            'type': 'Geo-spatial Model',
            'status': 'simulation_mode',
            'endpoint': '/api/predict/earthquake',
            'description': 'Predicts earthquake risk based on location'
        }
    }
    
    return jsonify({
        'status': 'success',
        'models': models_list,
        'total_models': len(models_list),
        'active_models': sum(1 for m in models_list.values() if m['status'] == 'loaded')
    })

def calculate_risk_score(latitude, longitude, disaster_type):
    """Simulate risk calculation based on coordinates"""
    # This is a simplified risk calculation for demonstration
    # In production, you would use actual geological data
    
    # Basic risk factors (for demo purposes)
    lat_risk = abs(latitude - 27.7172) / 180  # Distance from reference point
    lon_risk = abs(longitude - 85.3240) / 360
    
    if disaster_type == 'landslide':
        base_risk = 0.3
        risk = min(0.95, base_risk + lat_risk * 0.5 + lon_risk * 0.3)
    elif disaster_type == 'flood':
        base_risk = 0.25
        risk = min(0.95, base_risk + (1 - lat_risk) * 0.4 + lon_risk * 0.4)
    elif disaster_type == 'earthquake':
        base_risk = 0.35
        risk = min(0.95, base_risk + lat_risk * 0.6 + lon_risk * 0.2)
    else:
        risk = 0.5
    
    return round(risk, 3)

@app.route('/api/predict/landslide', methods=['POST'])
def predict_landslide():
    """Predict landslide risk for given coordinates"""
    try:
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if latitude is None or longitude is None:
            return jsonify({'error': 'Latitude and longitude required'}), 400
        
        risk_score = calculate_risk_score(latitude, longitude, 'landslide')
        
        risk_level = 'HIGH' if risk_score > 0.7 else 'MEDIUM' if risk_score > 0.4 else 'LOW'
        
        return jsonify({
            'disaster_type': 'landslide',
            'latitude': latitude,
            'longitude': longitude,
            'risk_score': risk_score,
            'risk_level': risk_level,
            'recommendation': 'Evacuate immediately' if risk_score > 0.7 else 'Monitor conditions' if risk_score > 0.4 else 'Low risk',
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict/flood', methods=['POST'])
def predict_flood():
    """Predict flood risk for given coordinates"""
    try:
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if latitude is None or longitude is None:
            return jsonify({'error': 'Latitude and longitude required'}), 400
        
        risk_score = calculate_risk_score(latitude, longitude, 'flood')
        
        risk_level = 'HIGH' if risk_score > 0.7 else 'MEDIUM' if risk_score > 0.4 else 'LOW'
        
        return jsonify({
            'disaster_type': 'flood',
            'latitude': latitude,
            'longitude': longitude,
            'risk_score': risk_score,
            'risk_level': risk_level,
            'recommendation': 'Move to higher ground' if risk_score > 0.7 else 'Prepare sandbags' if risk_score > 0.4 else 'Normal conditions',
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict/earthquake', methods=['POST'])
def predict_earthquake():
    """Predict earthquake risk for given coordinates"""
    try:
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if latitude is None or longitude is None:
            return jsonify({'error': 'Latitude and longitude required'}), 400
        
        risk_score = calculate_risk_score(latitude, longitude, 'earthquake')
        
        risk_level = 'HIGH' if risk_score > 0.7 else 'MEDIUM' if risk_score > 0.4 else 'LOW'
        
        return jsonify({
            'disaster_type': 'earthquake',
            'latitude': latitude,
            'longitude': longitude,
            'risk_score': risk_score,
            'risk_level': risk_level,
            'recommendation': 'Drop, cover, and hold on' if risk_score > 0.7 else 'Prepare emergency kit' if risk_score > 0.4 else 'Normal seismic activity',
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict/all', methods=['POST'])
def predict_all():
    """Predict all disaster types for given coordinates"""
    try:
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if latitude is None or longitude is None:
            return jsonify({'error': 'Latitude and longitude required'}), 400
        
        predictions = {
            'landslide': calculate_risk_score(latitude, longitude, 'landslide'),
            'flood': calculate_risk_score(latitude, longitude, 'flood'),
            'earthquake': calculate_risk_score(latitude, longitude, 'earthquake')
        }
        
        # Determine highest risk
        highest_risk = max(predictions, key=predictions.get)
        highest_score = predictions[highest_risk]
        
        return jsonify({
            'location': {'latitude': latitude, 'longitude': longitude},
            'predictions': predictions,
            'highest_risk': highest_risk,
            'highest_risk_score': highest_score,
            'overall_risk_level': 'HIGH' if highest_score > 0.7 else 'MEDIUM' if highest_score > 0.4 else 'LOW',
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict_text():
    """Predict disaster type from text message"""
    try:
        if model is None or vectorizer is None:
            return jsonify({'error': 'ML models not loaded'}), 503
        
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Make prediction
        X = vectorizer.transform([message])
        prediction = model.predict(X)[0]
        
        # Get confidence
        confidence = None
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(X)[0]
            confidence = float(max(probabilities))
        
        return jsonify({
            'success': True,
            'prediction': prediction,
            'confidence': confidence,
            'original_message': message,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

if __name__ == '__main__':
    print("\n" + "="*50)
    print("�� AI DISASTER RESPONSE SYSTEM - BACKEND")
    print("="*50)
    
    # Load ML models
    if load_ml_models():
        print("\n✅ System ready with ML capabilities")
    else:
        print("\n⚠️  Running in demo mode (no ML models)")
        print("   Train models with: python train_simple_model.py")
    
    print("\n📡 Starting server...")
    print("   URL: http://localhost:5000")
    print("   Health: http://localhost:5000/health")
    print("   Model Info: http://localhost:5000/model-info")
    print("   List Models: http://localhost:5000/api/models")
    print("   Text Predict: POST to http://localhost:5000/predict")
    print("\n📝 Example requests:")
    print('   # Text classification')
    print('   curl -X POST http://localhost:5000/predict \\')
    print('        -H "Content-Type: application/json" \\')
    print('        -d \'{"message": "earthquake building collapse"}\'')
    print('\n   # Geo-spatial prediction')
    print('   curl -X POST http://localhost:5000/api/predict/landslide \\')
    print('        -H "Content-Type: application/json" \\')
    print('        -d \'{"latitude": 27.7172, "longitude": 85.3240}\'')
    print("\n" + "="*50 + "\n")
    
    # Run on different port if 5000 is busy
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except OSError:
        print("⚠️  Port 5000 is busy. Trying port 5001...")
        app.run(debug=True, host='0.0.0.0', port=5001)
