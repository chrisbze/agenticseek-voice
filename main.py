from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "AgenticSeek Voice API is running!", "status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/voice/process")
def process_voice(data: dict):
    message = data.get("message", "")
    return {
        "response": f"Voice command received: {message}",
        "processed": True
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)