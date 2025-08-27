#!/usr/bin/env python3
"""
Complete voice system test for agenticSeek
Tests both TTS and STT integration
"""
import sys
import os
import time

def test_complete_system():
    """Test the complete voice system integration"""
    print("=" * 50)
    print("AgenticSeek Complete Voice System Test")
    print("=" * 50)
    
    # Test imports
    print("\n1. Testing imports...")
    try:
        from sources.text_to_speech import Speech, IMPORT_FOUND as TTS_FOUND, USE_FALLBACK
        from sources.speech_to_text import AudioRecorder, AudioTranscriber, IMPORT_FOUND as STT_FOUND
        from sources.interaction import Interaction
        
        print(f"✓ TTS Status: {'OK' if TTS_FOUND else 'FAILED'}")
        print(f"✓ TTS Fallback: {'Yes' if USE_FALLBACK else 'No'}")
        print(f"✓ STT Status: {'OK' if STT_FOUND else 'FAILED'}")
        print(f"✓ Interaction Module: OK")
        
    except Exception as e:
        print(f"✗ Import Error: {e}")
        return False
    
    # Test TTS
    print("\n2. Testing Text-to-Speech...")
    try:
        speech = Speech(enable=True, language="en", voice_idx=1)
        if speech.fallback_speech or speech.pipeline:
            print("✓ TTS Initialized successfully")
            speech.speak("AgenticSeek voice system is now operational.")
            print("✓ TTS Speech test completed")
        else:
            print("✗ TTS Failed to initialize")
            return False
    except Exception as e:
        print(f"✗ TTS Error: {e}")
        return False
    
    # Test STT (without actually recording)
    print("\n3. Testing Speech-to-Text components...")
    try:
        if STT_FOUND:
            recorder = AudioRecorder(verbose=False)
            transcriber = AudioTranscriber("Jarvis", verbose=False)
            print("✓ STT Components initialized successfully")
        else:
            print("✗ STT Dependencies missing")
            return False
    except Exception as e:
        print(f"✗ STT Error: {e}")
        return False
    
    # Test configuration
    print("\n4. Testing configuration...")
    try:
        import configparser
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        speak_enabled = config.getboolean('MAIN', 'speak')
        listen_enabled = config.getboolean('MAIN', 'listen')
        agent_name = config['MAIN']['agent_name']
        
        print(f"✓ Voice enabled: TTS={speak_enabled}, STT={listen_enabled}")
        print(f"✓ Agent name: {agent_name}")
        print(f"✓ Configuration loaded successfully")
        
    except Exception as e:
        print(f"✗ Configuration Error: {e}")
        return False
    
    return True

def demonstrate_capabilities():
    """Show the current capabilities"""
    print("\n" + "=" * 50)
    print("Current AgenticSeek Voice Capabilities:")
    print("=" * 50)
    
    print("\n🎤 Speech-to-Text (STT):")
    print("  • Wake word detection (agent name as trigger)")
    print("  • Whisper-based transcription")
    print("  • Multi-language support")
    print("  • Confirmation word detection")
    
    print("\n🔊 Text-to-Speech (TTS):")
    print("  • Fallback TTS using Windows native voices")
    print("  • Multi-language support")
    print("  • Voice selection options")
    print("  • Non-blocking speech processing")
    
    print("\n🤖 Agent Integration:")
    print("  • Browser Agent - Voice-controlled web browsing")
    print("  • Coder Agent - Speak code explanations")
    print("  • File Agent - Voice file operations")
    print("  • Planner Agent - Spoken task planning")
    print("  • Casual Agent - Natural conversation")
    
    print("\n🌍 Multi-language Support:")
    print("  • English (primary)")
    print("  • Chinese")
    print("  • French")
    print("  • Japanese")
    
    print("\n🎯 Usage Examples:")
    print('  • Say "Jarvis, search the web for Python tutorials"')
    print('  • Say "Jarvis, create a new Python file called hello.py"')
    print('  • Say "Jarvis, browse to google.com and search for AI news"')
    print('  • End commands with "do it" or "go ahead" to execute')

def show_next_steps():
    """Show what the user can do next"""
    print("\n" + "=" * 50)
    print("Ready to Use! Next Steps:")
    print("=" * 50)
    
    print("\n1. 🚀 Start AgenticSeek with voice:")
    print("   python cli.py")
    
    print("\n2. 🎙️ Voice Commands:")
    print('   - Say "Jarvis" to activate listening')
    print('   - Give your command')
    print('   - Say "do it" to confirm and execute')
    
    print("\n3. 🌐 Try Web Browsing:")
    print('   "Jarvis, search the web for the latest tech news, do it"')
    print('   "Jarvis, browse to github.com and find Python projects, go ahead"')
    
    print("\n4. 💻 Try Code Generation:")
    print('   "Jarvis, write a Python function to calculate fibonacci numbers, execute"')
    print('   "Jarvis, create a simple web scraper example, please"')
    
    print("\n5. 📁 Try File Operations:")
    print('   "Jarvis, list all Python files in the current directory, do it"')
    print('   "Jarvis, read the contents of config.ini, go ahead"')
    
    print("\n🔧 Troubleshooting:")
    print("  • Make sure microphone permissions are granted")
    print("  • Speak clearly and wait for processing")
    print("  • Check volume levels for TTS output")
    print("  • Use the exact agent name configured (default: Jarvis)")

if __name__ == "__main__":
    success = test_complete_system()
    
    if success:
        print("\n✅ All voice components working correctly!")
        demonstrate_capabilities()
        show_next_steps()
        
        print("\n🎉 AgenticSeek is ready for voice-controlled operation!")
        
    else:
        print("\n❌ Some components failed. Please check the errors above.")
        print("\nTry running: pip install pyttsx3 pyaudio torch transformers librosa")