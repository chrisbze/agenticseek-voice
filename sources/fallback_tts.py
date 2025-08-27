"""
Fallback Text-to-Speech implementation using pyttsx3 as an alternative to kokoro
This provides basic TTS functionality when kokoro is not available
"""
import re
import platform

IMPORT_FOUND = True

try:
    import pyttsx3
except ImportError:
    print("Fallback TTS disabled. Please install pyttsx3.")
    IMPORT_FOUND = False

class FallbackSpeech:
    """
    Fallback Speech class using pyttsx3 for basic text-to-speech functionality
    """
    def __init__(self, enable: bool = True, language: str = "en", voice_idx: int = 0):
        self.language = language
        self.engine = None
        self.voices = []
        
        if enable and IMPORT_FOUND:
            try:
                self.engine = pyttsx3.init()
                self.voices = self.engine.getProperty('voices')
                
                # Set voice based on language and index
                if self.voices and voice_idx < len(self.voices):
                    self.engine.setProperty('voice', self.voices[voice_idx].id)
                
                # Set speech rate (slower for better understanding)
                self.engine.setProperty('rate', 150)
                
                # Set volume
                self.engine.setProperty('volume', 0.8)
                
            except Exception as e:
                print(f"Error initializing fallback TTS: {e}")
                self.engine = None

    def speak(self, sentence: str, voice_idx: int = 0):
        """
        Convert text to speech using pyttsx3
        
        Args:
            sentence (str): The text to convert to speech
            voice_idx (int): Voice index (optional, uses default)
        """
        if not self.engine or not IMPORT_FOUND:
            print(f"[TTS Fallback]: {sentence}")
            return
            
        try:
            # Change voice if specified
            if voice_idx < len(self.voices):
                self.engine.setProperty('voice', self.voices[voice_idx].id)
            
            # Clean the sentence for better speech
            clean_sentence = self.clean_sentence(sentence)
            
            # Speak the text
            self.engine.say(clean_sentence)
            self.engine.runAndWait()
            
        except Exception as e:
            print(f"Error in fallback TTS: {e}")
            print(f"[TTS Fallback]: {sentence}")

    def clean_sentence(self, sentence: str) -> str:
        """
        Clean text for better speech synthesis
        
        Args:
            sentence (str): Input text
            
        Returns:
            str: Cleaned text
        """
        # Remove URLs
        sentence = re.sub(r'https?://\S+', '', sentence)
        
        # Remove code blocks
        sentence = re.sub(r'`.*?`', '', sentence)
        
        # Remove markdown formatting
        sentence = re.sub(r'\*\*', '', sentence)
        sentence = re.sub(r'\*', '', sentence)
        
        # Remove file paths (keep just filename)
        sentence = re.sub(r'[/\\][\w/\\.-]+', lambda m: m.group().split('/')[-1].split('\\')[-1], sentence)
        
        # Remove excessive whitespace
        sentence = re.sub(r'\s+', ' ', sentence).strip()
        
        # Limit length for better speech
        if len(sentence) > 200:
            sentence = sentence[:200] + "..."
            
        return sentence

    def list_voices(self):
        """List available voices for debugging"""
        if not self.engine or not IMPORT_FOUND:
            return []
            
        voices = []
        for i, voice in enumerate(self.voices):
            voices.append({
                'index': i,
                'id': voice.id,
                'name': voice.name,
                'languages': getattr(voice, 'languages', [])
            })
        return voices

if __name__ == "__main__":
    # Test the fallback TTS
    print("Testing Fallback TTS...")
    
    speech = FallbackSpeech(enable=True, language="en")
    
    # List available voices
    voices = speech.list_voices()
    print(f"Available voices: {len(voices)}")
    for voice in voices[:3]:  # Show first 3 voices
        print(f"  {voice['index']}: {voice['name']}")
    
    # Test speech
    test_text = "Hello! This is a test of the fallback text-to-speech system for agenticSeek."
    print(f"Speaking: {test_text}")
    speech.speak(test_text)
    
    print("Fallback TTS test completed!")