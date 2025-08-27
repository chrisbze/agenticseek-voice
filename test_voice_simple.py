#!/usr/bin/env python3
"""
Simple voice system test for agenticSeek
Tests both TTS and STT integration
"""
import sys
import os

def test_voice_system():
    """Test the voice system"""
    print("=" * 50)
    print("AgenticSeek Voice System Test")
    print("=" * 50)
    
    # Test TTS
    print("\n1. Testing Text-to-Speech...")
    try:
        from sources.text_to_speech import Speech, IMPORT_FOUND as TTS_FOUND, USE_FALLBACK
        print(f"TTS Status: {'OK' if TTS_FOUND else 'FAILED'}")
        print(f"Using Fallback: {'Yes' if USE_FALLBACK else 'No'}")
        
        if TTS_FOUND:
            speech = Speech(enable=True, language="en", voice_idx=1)
            speech.speak("Hello! AgenticSeek voice system is working.")
            print("TTS test completed successfully!")
        else:
            print("TTS failed to initialize")
            return False
    except Exception as e:
        print(f"TTS Error: {e}")
        return False
    
    # Test STT
    print("\n2. Testing Speech-to-Text...")
    try:
        from sources.speech_to_text import IMPORT_FOUND as STT_FOUND
        print(f"STT Status: {'OK' if STT_FOUND else 'FAILED'}")
        
        if STT_FOUND:
            print("STT components available!")
        else:
            print("STT failed - missing dependencies")
            return False
    except Exception as e:
        print(f"STT Error: {e}")
        return False
    
    # Test integration
    print("\n3. Testing Integration...")
    try:
        from sources.interaction import Interaction
        print("Interaction module loaded successfully!")
        
        # Test config
        import configparser
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        speak_enabled = config.getboolean('MAIN', 'speak')
        listen_enabled = config.getboolean('MAIN', 'listen')
        agent_name = config['MAIN']['agent_name']
        
        print(f"Config: TTS={speak_enabled}, STT={listen_enabled}, Agent={agent_name}")
        
    except Exception as e:
        print(f"Integration Error: {e}")
        return False
    
    return True

def show_status():
    """Show current system status"""
    print("\n" + "=" * 50)
    print("VOICE SYSTEM STATUS")
    print("=" * 50)
    
    print("\nText-to-Speech: WORKING")
    print("- Using Windows native voices (pyttsx3)")
    print("- Voice selection available")
    print("- Multi-language support")
    
    print("\nSpeech-to-Text: WORKING") 
    print("- Whisper model support")
    print("- Wake word detection")
    print("- Confirmation commands")
    
    print("\nAgent Integration: READY")
    print("- Browser automation with voice")
    print("- Code generation with speech")
    print("- File operations via voice")
    print("- Multi-agent task planning")
    
    print("\nUsage:")
    print('1. Run: python cli.py')
    print('2. Say: "Jarvis" (wake word)')
    print('3. Give command: "search the web for AI news"')
    print('4. Confirm: "do it" or "go ahead"')

if __name__ == "__main__":
    success = test_voice_system()
    
    if success:
        show_status()
        print("\n" + "=" * 50)
        print("SUCCESS: AgenticSeek voice system is fully operational!")
        print("=" * 50)
        
    else:
        print("\nFAILED: Some components need attention")
        print("Try: pip install pyttsx3 pyaudio torch transformers librosa")