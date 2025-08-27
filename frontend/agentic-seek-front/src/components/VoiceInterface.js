import React, { useState, useEffect, useRef, useCallback } from 'react';
import './VoiceInterface.css';

const VoiceInterface = ({ onVoiceCommand, onVoiceStateChange, isProcessing }) => {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [voiceSupported, setVoiceSupported] = useState(false);
  const [status, setStatus] = useState('Ready');
  
  const recognitionRef = useRef(null);
  const isActiveRef = useRef(true);
  
  const cleanup = useCallback(() => {
    isActiveRef.current = false;
    if (recognitionRef.current) {
      try {
        recognitionRef.current.stop();
      } catch (error) {
        console.log('Recognition cleanup error:', error);
      }
    }
  }, []);

  const initializeSpeechRecognition = useCallback(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) return false;

    recognitionRef.current = new SpeechRecognition();
    
    recognitionRef.current.continuous = false;
    recognitionRef.current.interimResults = false;
    recognitionRef.current.lang = 'en-US';
    
    recognitionRef.current.onstart = () => {
      if (!isActiveRef.current) return;
      console.log('Voice recognition started');
      setIsListening(true);
      setStatus('Listening... Say "Jarvis [command]"');
      if (onVoiceStateChange) {
        onVoiceStateChange({ listening: true, transcript: '' });
      }
    };
    
    recognitionRef.current.onresult = (event) => {
      if (!isActiveRef.current) return;
      
      const result = event.results[0][0].transcript.trim();
      setTranscript(result);
      
      console.log('Voice result:', result);
      
      // Check for wake words
      const lowerResult = result.toLowerCase();
      const wakeWords = ['jarvis', 'hey jarvis', 'hello jarvis'];
      const hasWakeWord = wakeWords.some(word => lowerResult.includes(word));
      
      if (hasWakeWord && onVoiceCommand) {
        setStatus('Processing command...');
        onVoiceCommand(result);
      } else {
        setStatus('Please say "Jarvis" followed by your command');
      }
    };
    
    recognitionRef.current.onerror = (event) => {
      if (!isActiveRef.current) return;
      console.log('Speech recognition error:', event.error);
      setIsListening(false);
      
      switch(event.error) {
        case 'no-speech':
          setStatus('No speech detected');
          break;
        case 'not-allowed':
          setStatus('Microphone access denied');
          break;
        default:
          setStatus('Voice recognition error');
      }
    };
    
    recognitionRef.current.onend = () => {
      if (!isActiveRef.current) return;
      console.log('Speech recognition ended');
      setIsListening(false);
      
      setTimeout(() => {
        if (isActiveRef.current) {
          setStatus('Click microphone to speak');
        }
      }, 1000);
    };
    
    return true;
  }, [onVoiceCommand, onVoiceStateChange]);

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      setVoiceSupported(true);
      initializeSpeechRecognition();
    } else {
      setStatus('Voice recognition not supported in this browser');
    }
    
    return cleanup;
  }, [initializeSpeechRecognition, cleanup]);

  const toggleListening = () => {
    if (isProcessing) return;
    
    if (isListening) {
      stopListening();
    } else {
      startListening();
    }
  };

  const startListening = () => {
    if (!voiceSupported || !recognitionRef.current || isProcessing) return;
    
    try {
      setTranscript('');
      setStatus('Starting...');
      recognitionRef.current.start();
    } catch (error) {
      console.error('Error starting voice recognition:', error);
      setStatus('Failed to start listening');
    }
  };

  const stopListening = () => {
    if (recognitionRef.current) {
      try {
        recognitionRef.current.stop();
      } catch (error) {
        console.log('Error stopping recognition:', error);
      }
    }
    setIsListening(false);
    setStatus('Click microphone to speak');
  };

  if (!voiceSupported) {
    return (
      <div className="voice-unsupported">
        <p>🚫 Voice recognition is not supported in this browser.</p>
        <p>Please use Chrome, Edge, or Safari for the best experience.</p>
      </div>
    );
  }

  return (
    <div className="voice-interface">
      <div className="voice-controls">
        <button
          className={`voice-button ${isListening ? 'listening' : ''} ${isProcessing ? 'processing' : ''}`}
          onClick={toggleListening}
          disabled={isProcessing}
          aria-label={isListening ? 'Stop listening' : 'Start listening'}
        >
          <span className="voice-icon">🎤</span>
          {isListening && <div className="audio-visualizer"></div>}
        </button>
        
        <div className="voice-status">
          <div className={`status-indicator ${isListening ? 'active' : ''}`}>
            <div className="status-dot"></div>
            <span className="status-text">{status}</span>
          </div>
        </div>
      </div>

      {transcript && (
        <div className="transcript">
          <strong>You said:</strong> "{transcript}"
        </div>
      )}

      <div className="voice-instructions">
        <h3>How to use voice commands:</h3>
        <div className="instruction-steps">
          <div className="step">
            <div className="step-number">1</div>
            <span>Click mic</span>
          </div>
          <div className="step">
            <div className="step-number">2</div>
            <span>Say "Jarvis"</span>
          </div>
          <div className="step">
            <div className="step-number">3</div>
            <span>Give command</span>
          </div>
        </div>
        
        <div className="example-commands">
          <h4>Try saying:</h4>
          <ul>
            <li>"Jarvis, hello"</li>
            <li>"Jarvis, what can you do?"</li>
            <li>"Jarvis, help me"</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default VoiceInterface;