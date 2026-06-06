from fastapi import FastAPI
from app.routes import flood, landslide, map, weather, chatbot

app = FastAPI(
    title="AI Disaster Response API",
    description="API for disaster prediction and response",
    version="1.0.0"
)

# Include routers
app.include_router(flood.router, prefix="/api/v1", tags=["flood"])
app.include_router(landslide.router, prefix="/api/v1", tags=["landslide"])
app.include_router(map.router, prefix="/api/v1", tags=["map"])
app.include_router(weather.router, prefix="/api/v1", tags=["weather"])
app.include_router(chatbot.router, prefix="/api/v1", tags=["chatbot"])

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "AI Disaster Response System API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "flood": "/api/v1/flood",
            "landslide": "/api/v1/landslide",
            "weather": "/api/v1/weather",
            "map": "/api/v1/map",
            "chatbot": "/api/v1/chat"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": ["flood", "landslide", "weather", "map", "chatbot"]
    }

print("=" * 50)
print("✅ AI Disaster Response API is running!")
print("📍 Visit: http://127.0.0.1:8000")
print("📚 API Docs: http://127.0.0.1:8000/docs")
print("=" * 50)