package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
)

type Response struct {
	Message string `json:"message"`
	Status  string `json:"status"`
}

type VoiceRequest struct {
	Message   string `json:"message"`
	AgentType string `json:"agent_type,omitempty"`
}

type VoiceResponse struct {
	Response  string `json:"response"`
	Processed bool   `json:"processed"`
	Echo      string `json:"echo,omitempty"`
}

func enableCORS(w http.ResponseWriter) {
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
	w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
}

func rootHandler(w http.ResponseWriter, r *http.Request) {
	enableCORS(w)
	
	if r.Method == "OPTIONS" {
		w.WriteHeader(http.StatusOK)
		return
	}
	
	w.Header().Set("Content-Type", "application/json")
	
	response := Response{
		Message: "🎤 AgenticSeek Voice API is running!",
		Status:  "active",
	}
	
	json.NewEncoder(w).Encode(response)
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
	enableCORS(w)
	w.Header().Set("Content-Type", "application/json")
	
	response := Response{
		Status: "healthy",
	}
	
	json.NewEncoder(w).Encode(response)
}

func voiceHandler(w http.ResponseWriter, r *http.Request) {
	enableCORS(w)
	
	if r.Method == "OPTIONS" {
		w.WriteHeader(http.StatusOK)
		return
	}
	
	if r.Method != "POST" {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}
	
	w.Header().Set("Content-Type", "application/json")
	
	var req VoiceRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		req.Message = "Unknown command"
	}
	
	// Simple voice processing
	response := VoiceResponse{
		Response:  fmt.Sprintf("Voice command received: %s", req.Message),
		Processed: true,
		Echo:      req.Message,
	}
	
	// Basic keyword responses
	switch {
	case contains(req.Message, "hello"):
		response.Response = "Hello! I'm your AgenticSeek voice assistant."
	case contains(req.Message, "jarvis"):
		response.Response = "Yes, I'm here! How can I help you?"
	case contains(req.Message, "help"):
		response.Response = "I'm ready to assist you with voice commands!"
	default:
		response.Response = fmt.Sprintf("I heard: %s. How can I help?", req.Message)
	}
	
	json.NewEncoder(w).Encode(response)
}

func contains(text, substr string) bool {
	return len(text) >= len(substr) && 
		   (text == substr || 
		    len(text) > len(substr) && 
		    (text[:len(substr)] == substr || 
		     text[len(text)-len(substr):] == substr ||
		     findInString(text, substr)))
}

func findInString(text, substr string) bool {
	for i := 0; i <= len(text)-len(substr); i++ {
		if text[i:i+len(substr)] == substr {
			return true
		}
	}
	return false
}

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	
	http.HandleFunc("/", rootHandler)
	http.HandleFunc("/health", healthHandler)
	http.HandleFunc("/api/voice", voiceHandler)
	
	fmt.Printf("🚀 AgenticSeek Voice API starting on port %s\n", port)
	fmt.Printf("🎤 Voice endpoints ready\n")
	fmt.Printf("🌐 CORS enabled for all origins\n")
	
	log.Fatal(http.ListenAndServe(":"+port, nil))
}