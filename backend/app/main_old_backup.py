# Create minimal main
New-Item -Path app/main_minimal.py -Force -Value @"
from fastapi import FastAPI

app = FastAPI(title="AI Disaster Response API")

@app.get("/")
async def root():
    return {"message": "AI Disaster Response System API is running!", "status": "active"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2026-06-06"}

# Simple flood prediction endpoint
@app.post("/api/v1/flood")
async def simple_flood_prediction(rainfall: float = 0, river_level: float = 0):
    risk = "HIGH" if rainfall > 100 or river_level > 5 else "LOW"
    return {
        "success": True,
        "disaster": "flood",
        "risk_level": risk,
        "alert": risk == "HIGH",
        "message": f"Flood risk is {risk}"
    }

# Simple weather endpoint
@app.get("/api/v1/weather")
async def simple_weather():
    return {
        "temperature": 25.5,
        "humidity": 70,
        "rainfall": 10.2
    }

print("✅ Server is running! Visit http://127.0.0.1:8000/docs")
"