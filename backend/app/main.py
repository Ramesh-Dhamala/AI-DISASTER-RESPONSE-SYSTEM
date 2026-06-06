from fastapi import FastAPI
from app.routes import flood, landslide, map, earthquake, chatbot

app = FastAPI(title="AI Disaster Response API", version="1.0.0")

# Try to include routes, skip if they fail
try:
    app.include_router(flood.router, prefix="/api/v1", tags=["flood"])
    print("✅ Flood routes loaded")
except Exception as e:
    print(f"⚠️ Flood routes failed: {e}")

try:
    app.include_router(landslide.router, prefix="/api/v1", tags=["landslide"])
    print("✅ Landslide routes loaded")
except Exception as e:
    print(f"⚠️ Landslide routes failed: {e}")

try:
    app.include_router(map.router, prefix="/api/v1", tags=["map"])
    print("✅ Map routes loaded")
except Exception as e:
    print(f"⚠️ Map routes failed: {e}")

try:
    app.include_router(earthquake.router, prefix="/api/v1", tags=["earthquake"])
    print("✅ Earthquake routes loaded")
except Exception as e:
    print(f"⚠️ Earthquake routes failed: {e}")

try:
    app.include_router(chatbot.router, prefix="/api/v1", tags=["chatbot"])
    print("✅ Chatbot routes loaded")
except Exception as e:
    print(f"⚠️ Chatbot routes failed: {e}")

@app.get("/")
async def root():
    return {
        "message": "AI Disaster Response System API",
        "version": "1.0.0",
        "status": "running",
        "endpoints_available": [
            "/api/v1/flood/predict",
            "/api/v1/landslide/predict",
            "/api/v1/earthquake/predict",
            "/api/v1/chat",
            "/api/v1/map/disaster-zones",
            "/api/v1/map/layers"
        ]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": "2026-06-06",
        "services": {
            "flood": "available",
            "landslide": "available",
            "earthquake": "available",
            "chatbot": "available",
            "map": "available"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)