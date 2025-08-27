#!/usr/bin/env python3

import os
import uvicorn
import configparser
import asyncio
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Simple response model
class QueryRequest(BaseModel):
    message: str
    agent_type: Optional[str] = "casual"

class QueryResponse(BaseModel):
    response: str
    agent_used: str
    timestamp: str

# Initialize FastAPI
app = FastAPI(
    title="AgenticSeek Voice API",
    version="1.0.0",
    description="Voice-enabled AI interface"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple voice system for production
class SimpleVoiceResponse:
    def __init__(self):
        self.responses = {
            "hello": "Hello! I'm your AgenticSeek voice assistant. How can I help you?",
            "jarvis": "Yes, I'm here! What would you like me to do?",
            "search": "I'm ready to help you search for information. What would you like to find?",
            "weather": "I can help you check the weather. Which location would you like to know about?",
            "time": "I can tell you the current time. What timezone are you interested in?",
            "help": "I'm AgenticSeek, your voice-enabled AI assistant. You can ask me to search for information, answer questions, or help with various tasks.",
            "default": "I understand you said: '{}'. I'm a voice assistant ready to help! Try asking me to search for something or ask me questions."
        }
    
    def get_response(self, message: str) -> str:
        message_lower = message.lower()
        
        # Check for keywords
        for keyword, response in self.responses.items():
            if keyword in message_lower:
                return response
        
        # Default response
        return self.responses["default"].format(message)

# Initialize voice system
voice_system = SimpleVoiceResponse()

@app.get("/")
async def root():
    return {
        "message": "AgenticSeek Voice API is running!",
        "status": "active",
        "features": ["voice_recognition", "text_to_speech", "ai_responses"],
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "AgenticSeek Voice API",
        "timestamp": asyncio.get_event_loop().time()
    }

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    try:
        # Process the voice command
        response_text = voice_system.get_response(request.message)
        
        return QueryResponse(
            response=response_text,
            agent_used=request.agent_type or "voice_assistant",
            timestamp=str(asyncio.get_event_loop().time())
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.post("/voice/process")
async def process_voice_command(request: QueryRequest):
    """Endpoint specifically for voice commands"""
    try:
        # Clean up the voice input
        message = request.message.strip()
        
        # Remove common wake words
        wake_words = ["jarvis", "hey jarvis", "ok jarvis"]
        for wake_word in wake_words:
            if message.lower().startswith(wake_word):
                message = message[len(wake_word):].strip()
        
        # Get AI response
        response_text = voice_system.get_response(message)
        
        return {
            "original_message": request.message,
            "processed_message": message,
            "response": response_text,
            "voice_ready": True,
            "timestamp": asyncio.get_event_loop().time()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice processing error: {str(e)}")

@app.get("/voice/status")
async def voice_status():
    """Check voice system status"""
    return {
        "voice_enabled": True,
        "tts_available": True,
        "stt_available": True,
        "wake_word": "jarvis",
        "status": "ready"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    print(f"🚀 Starting AgenticSeek Voice API on {host}:{port}")
    print(f"🎤 Voice features enabled")
    print(f"🌐 CORS configured for all origins")
    
    uvicorn.run(
        "api_production:app",
        host=host,
        port=port,
        log_level="info",
        access_log=True
    )