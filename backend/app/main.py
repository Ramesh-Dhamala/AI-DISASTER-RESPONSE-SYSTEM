from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Core features
from app.routes.chatbot import router as chatbot_router
from app.routes.weather import router as weather_router
from app.routes.earthquake import router as earthquake_router

# ML disaster models
from app.routes.flood import router as flood_router
from app.routes.landslide import router as landslide_router

# Alert system
from app.routes.alert import router as alert_router


app = FastAPI(title="DisasterGuard AI - Nepal Emergency System")

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # later you can restrict to frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- CORE ROUTES ----------------
app.include_router(chatbot_router, prefix="/api")
app.include_router(weather_router, prefix="/api")
app.include_router(earthquake_router, prefix="/api")

# ---------------- ML MODELS ----------------
app.include_router(flood_router, prefix="/api")
app.include_router(landslide_router, prefix="/api")

# ---------------- ALERT SYSTEM ----------------
app.include_router(alert_router, prefix="/api")


# ---------------- HEALTH CHECK ----------------
@app.get("/")
def home():
    return {
        "success": True,
        "message": "🚀 DisasterGuard AI Backend is Running"
    }