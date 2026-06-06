from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.chatbot import router as chatbot_router
from app.routes.weather import router as weather_router   # 👈 ADD THIS

app = FastAPI(title="Nova AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chatbot_router, prefix="/api")
app.include_router(weather_router, prefix="/api")   # 👈 ADD THIS


@app.get("/")
def home():
    return {"message": "Server Running"}