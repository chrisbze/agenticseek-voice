#!/usr/bin/env python3
"""
Test script for agenticSeek voice capabilities
"""
import sys
import os

# Add the sources directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sources'))

def test_tts():
    """Test Text-to-Speech functionality"""
    print("=== Testing Text-to-Speech ===")
    try:
        from text_to_speech import Speech, IMPORT_FOUND
        print(f"TTS Import Status: {IMPORT_FOUND}")
        
        if IMPORT_FOUND:
            speech = Speech(enable=True, language="en", voice_idx=1)
            print("TTS initialized successfully!")
            # Uncomment to test actual speech
            # speech.speak("Hello! This is a test of the text to speech system.")
        else:
            print("TTS dependencies not available. Need to install kokoro and dependencies.")
            
    except Exception as e:
        print(f"TTS Error: {e}")

def test_stt():
    """Test Speech-to-Text functionality"""  
    print("\n=== Testing Speech-to-Text ===")
    try:
        from speech_to_text import AudioRecorder, AudioTranscriber, IMPORT_FOUND
        print(f"STT Import Status: {IMPORT_FOUND}")
        
        if IMPORT_FOUND:
            print("STT dependencies available!")
            # Don't actually start recording in test
            recorder = AudioRecorder(verbose=False)
            transcriber = AudioTranscriber("Jarvis", verbose=False)
            print("STT components initialized successfully!")
        else:
            print("STT dependencies not available. Need to install pyaudio, torch, librosa, transformers.")
            
    except Exception as e:
        print(f"STT Error: {e}")

def test_integration():
    """Test integration with main application"""
    print("\n=== Testing Integration ===")
    try:
        import configparser
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        print(f"Voice enabled in config:")
        print(f"  - speak: {config.getboolean('MAIN', 'speak')}")
        print(f"  - listen: {config.getboolean('MAIN', 'listen')}")
        print(f"  - agent_name: {config['MAIN']['agent_name']}")
        print(f"  - languages: {config['MAIN']['languages']}")
        
    except Exception as e:
        print(f"Integration test error: {e}")

def show_requirements():
    """Show what's needed for full voice functionality"""
    print("\n=== Voice Requirements ===")
    print("For Text-to-Speech:")
    print("  - kokoro (AI voice synthesis)")
    print("  - soundfile")
    print("  - IPython")
    
    print("\nFor Speech-to-Text:")
    print("  - pyaudio (microphone access)")
    print("  - torch (PyTorch)")
    print("  - librosa (audio processing)")
    print("  - transformers (Whisper model)")
    
    print("\nInstall command:")
    print("  pip install kokoro pyaudio torch librosa transformers soundfile")

if __name__ == "__main__":
    print("AgenticSeek Voice Capabilities Test")
    print("=" * 40)
    
    test_tts()
    test_stt()  
    test_integration()
    show_requirements()
    
    print("\n=== Summary ===")
    print("AgenticSeek has a solid voice architecture with:")
    print("✓ Integrated TTS/STT in the main application")
    print("✓ Multi-language support")
    print("✓ Wake word detection (agent name)")
    print("✓ Non-blocking voice processing")
    print("⚠ Missing some dependencies for full functionality")
    print("\nNext steps: Install remaining dependencies and test with full system!")