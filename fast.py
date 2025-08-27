from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "AgenticSeek API Working!", "status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/api/voice")
def voice(data: dict = None):
    return {"response": "Voice API working", "data": data}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)