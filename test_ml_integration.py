import sys
import json
import joblib
import numpy as np
from datetime import datetime

def test_model_loading():
    """Test if ML model loads successfully"""
    try:
        model = joblib.load('models/saved/disaster_model.pkl')
        vectorizer = joblib.load('models/saved/vectorizer.pkl')
        print("✅ Model and vectorizer loaded successfully")
        return True, model, vectorizer
    except FileNotFoundError:
        print("❌ Model files not found. Train model first: python src/models/train_model.py")
        return False, None, None
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False, None, None

def test_prediction(model, vectorizer):
    """Test if model makes predictions correctly"""
    test_messages = [
        "earthquake shaking building collapse",
        "flood water rising need rescue",
        "normal weather today no emergency"
    ]
    
    print("\n📊 Testing predictions:")
    for msg in test_messages:
        try:
            X = vectorizer.transform([msg])
            prediction = model.predict(X)[0]
            print(f"  Input: '{msg[:50]}...' -> Prediction: {prediction}")
        except Exception as e:
            print(f"  ❌ Prediction failed for '{msg}': {e}")
            return False
    return True

def test_api_endpoint():
    """Test if backend API endpoint exists"""
    import requests
    try:
        response = requests.get('http://localhost:5000/health', timeout=5)
        if response.status_code == 200:
            print("✅ Backend API is running and healthy")
            return True
    except requests.exceptions.ConnectionError:
        print("⚠️  Backend API not running (start with: python app.py)")
        return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def test_data_flow():
    """Test end-to-end data flow"""
    print("\n🔄 Testing end-to-end data flow:")
    
    # Simulate backend receiving request
    test_request = {
        'message': 'hurricane approaching coast evacuate now',
        'timestamp': str(datetime.now()),
        'user_id': 'test_user'
    }
    
    # Simulate preprocessing
    try:
        processed = test_request['message'].lower().strip()
        print(f"  ✓ Data received: {test_request['message']}")
        print(f"  ✓ Data preprocessed: {processed}")
        
        # Simulate ML prediction flow
        _, model, vectorizer = test_model_loading()
        if model:
            X = vectorizer.transform([processed])
            prediction = model.predict(X)[0]
            
            # Simulate backend response
            response = {
                'status': 'success',
                'prediction': prediction,
                'confidence': 0.85,
                'request_id': test_request['timestamp'],
                'action_needed': f"Activate {prediction} emergency protocol"
            }
            print(f"  ✓ ML prediction: {prediction}")
            print(f"  ✓ Backend response: {json.dumps(response, indent=2)}")
            return True
    except Exception as e:
        print(f"  ❌ Data flow failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("ML BACKEND INTEGRATION TEST SUITE")
    print("=" * 50)
    
    # Run tests
    model_loaded, model, vectorizer = test_model_loading()
    
    if model_loaded:
        test_prediction(model, vectorizer)
        test_data_flow()
    
    test_api_endpoint()
    
    print("\n" + "=" * 50)
    print("Test Summary: Check ✅ marks above for successful integration")
    print("=" * 50)
