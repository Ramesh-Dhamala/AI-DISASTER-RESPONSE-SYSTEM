from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.chatbot import router as chatbot_router
from app.routes.weather import router as weather_router
from app.routes.earthquake import router as earthquake_router
from app.routes.flood import router as flood_router
from app.routes.landslide import router as landslide_router
from app.routes.alert import router as alert_router

app = FastAPI(title="Disaster AI System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(chatbot_router, prefix="/api")
app.include_router(weather_router, prefix="/api")
app.include_router(earthquake_router, prefix="/api")
app.include_router(flood_router, prefix="/api")
app.include_router(landslide_router, prefix="/api")
app.include_router(alert_router, prefix="/api")


@app.get("/")
def home():
    return {"message": "🚀 Disaster AI Server Running"}