import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from app.routes import chatbot

app = FastAPI()
app.include_router(chatbot.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Chatbot is running!"}

if __name__ == "__main__":
    import uvicorn
    print("=" * 50)
    print("🚀 Starting Chatbot Test Server")
    print("📍 http://127.0.0.1:8000")
    print("📚 API Docs: http://127.0.0.1:8000/docs")
    print("=" * 50)
    uvicorn.run(app, host="127.0.0.1", port=8000)