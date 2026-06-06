from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class TestRequest(BaseModel):
    name: str
    value: float

@app.get("/")
def root():
    return {"message": "FastAPI is working!"}

@app.post("/test")
def test_endpoint(request: TestRequest):
    return {"received": request.name, "value": request.value}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)