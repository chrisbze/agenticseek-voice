from fastapi import FastAPI
import uvicorn
import os

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello from AgenticSeek!", "status": "working"}

@app.get("/health")  
def health():
    return {"status": "ok"}

@app.post("/api/voice")
def voice(data: dict):
    return {"echo": data.get("message", ""), "response": "Voice received!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)