from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import joblib
import os

app = FastAPI(title="AI Disaster Response System")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models
model = None
vectorizer = None

class MessageRequest(BaseModel):
    message: str

class PredictionResponse(BaseModel):
    success: bool
    prediction: str
    confidence: float = None
    timestamp: str

@app.on_event("startup")
async def load_models():
    global model, vectorizer
    try:
        model = joblib.load('models/saved/disaster_model.pkl')
        vectorizer = joblib.load('models/saved/vectorizer.pkl')
        print("✅ Models loaded successfully")
    except Exception as e:
        print(f"❌ Error loading models: {e}")

@app.get("/")
async def root():
    return {"message": "AI Disaster Response System API", "status": "running"}

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "models_loaded": model is not None,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: MessageRequest):
    if model is None or vectorizer is None:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    X = vectorizer.transform([request.message])
    prediction = model.predict(X)[0]
    
    confidence = None
    if hasattr(model, 'predict_proba'):
        proba = model.predict_proba(X)[0]
        confidence = float(max(proba))
    
    return PredictionResponse(
        success=True,
        prediction=prediction,
        confidence=confidence,
        timestamp=datetime.now().isoformat()
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
