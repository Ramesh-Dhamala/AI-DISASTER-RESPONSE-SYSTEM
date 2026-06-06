from flask import Flask, request, jsonify
import joblib
from datetime import datetime

app = Flask(__name__)

# Load models
print("Loading ML models...")
model = joblib.load('models/saved/disaster_model.pkl')
vectorizer = joblib.load('models/saved/vectorizer.pkl')
print("✅ Models loaded successfully!")

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'ml_models_loaded': True,
        'timestamp': str(datetime.now())
    })

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    message = data.get('message', '')
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Make prediction
    X = vectorizer.transform([message])
    prediction = model.predict(X)[0]
    
    return jsonify({
        'status': 'success',
        'prediction': prediction,
        'message': message,
        'timestamp': str(datetime.now())
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
