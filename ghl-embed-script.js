// AgenticSeek Voice Widget for GoHighLevel
// Copy and paste this script into your GHL page or funnel

(function() {
    // Create widget HTML
    const widgetHTML = `
    <div id="agenticseek-voice-widget" style="
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        max-width: 300px;
        margin: 20px auto;
        padding: 20px;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    ">
        <h4 style="margin: 0 0 15px 0;">🎤 Voice Assistant</h4>
        <button id="voice-toggle" style="
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: rgba(255,255,255,0.2);
            border: 2px solid rgba(255,255,255,0.5);
            color: white;
            font-size: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
        " onclick="agenticseekToggleVoice()">🎤</button>
        <div id="voice-status" style="margin: 10px 0; font-size: 12px;">
            Click to start listening
        </div>
        <div id="voice-response" style="
            margin: 15px 0;
            padding: 10px;
            background: rgba(255,255,255,0.9);
            color: #333;
            border-radius: 8px;
            font-size: 12px;
            display: none;
        "></div>
    </div>`;
    
    // Insert widget into page
    document.body.insertAdjacentHTML('beforeend', widgetHTML);
    
    // Voice functionality
    let recognition = null;
    let isListening = false;
    const API_URL = 'https://agenticseek-voice.onrender.com';
    
    window.agenticseekToggleVoice = function() {
        if (!recognition) {
            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                recognition = new SpeechRecognition();
                recognition.continuous = true;
                recognition.interimResults = true;
                recognition.lang = 'en-US';
                
                recognition.onresult = function(event) {
                    let transcript = '';
                    for (let i = event.resultIndex; i < event.results.length; i++) {
                        transcript += event.results[i][0].transcript;
                    }
                    
                    if (transcript.toLowerCase().includes('jarvis')) {
                        processCommand(transcript);
                    }
                };
            } else {
                document.getElementById('voice-status').textContent = 'Voice not supported';
                return;
            }
        }
        
        if (isListening) {
            recognition.stop();
            isListening = false;
            document.getElementById('voice-toggle').style.background = 'rgba(255,255,255,0.2)';
            document.getElementById('voice-status').textContent = 'Click to start';
        } else {
            recognition.start();
            isListening = true;
            document.getElementById('voice-toggle').style.background = '#4CAF50';
            document.getElementById('voice-status').textContent = 'Say "Jarvis"...';
        }
    };
    
    async function processCommand(command) {
        document.getElementById('voice-status').textContent = 'Processing...';
        
        try {
            const response = await fetch(`${API_URL}/api/voice`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: command })
            });
            
            const result = await response.json();
            const responseDiv = document.getElementById('voice-response');
            responseDiv.style.display = 'block';
            responseDiv.textContent = result.response || 'Command processed!';
            
            // Speak response
            if ('speechSynthesis' in window) {
                const utterance = new SpeechSynthesisUtterance(responseDiv.textContent);
                speechSynthesis.speak(utterance);
            }
            
            document.getElementById('voice-status').textContent = 'Ready';
            
        } catch (error) {
            document.getElementById('voice-status').textContent = 'Error occurred';
        }
    }
})();