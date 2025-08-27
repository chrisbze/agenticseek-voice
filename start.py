#!/usr/bin/env python3

import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import time

# Initialize FastAPI
app = FastAPI(title="AgenticSeek Voice API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    message: str
    agent_type: Optional[str] = "voice"

@app.get("/")
def root():
    return {
        "message": "🎤 AgenticSeek Voice API is running!",
        "status": "active",
        "version": "1.0.0"
    }

@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": time.time()}

@app.post("/query")
def query(request: QueryRequest):
    return {
        "response": f"Voice command received: {request.message}",
        "status": "processed",
        "agent": request.agent_type
    }

@app.post("/voice/process")
def voice_process(request: QueryRequest):
    message = request.message.lower()
    
    responses = {
        "hello": "Hello! I'm your AgenticSeek voice assistant.",
        "jarvis": "Yes, I'm here! How can I help?",
        "help": "I'm ready to assist you with voice commands!",
    }
    
    for keyword, response in responses.items():
        if keyword in message:
            return {"response": response, "processed": True}
    
    return {
        "response": f"I heard: {request.message}. How can I help?",
        "processed": True
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("start:app", host="0.0.0.0", port=port)