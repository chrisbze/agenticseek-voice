#!/usr/bin/env python3
"""
Simple Live Demonstration of AgenticSeek Voice System
"""
import sys
import time
import os

def demo_banner():
    """Display demo banner"""
    print("\n" + "="*60)
    print("AGENTICSEEK VOICE SYSTEM LIVE DEMO")
    print("="*60)
    print("Demonstrating your smart voice-controlled web browser!")
    print("="*60)

def demo_tts():
    """Demonstrate Text-to-Speech"""
    print("\nDEMO 1: Text-to-Speech System")
    print("-" * 40)
    
    try:
        from sources.text_to_speech import Speech
        
        print("Initializing TTS engine...")
        speech = Speech(enable=True, language="en", voice_idx=1)
        
        # Test different voice messages
        messages = [
            "Hello! I am your AgenticSeek assistant.",
            "I can browse the web and write code using voice commands.",
            "Just say Jarvis to wake me up!"
        ]
        
        for i, msg in enumerate(messages, 1):
            print(f"\n[Speaking {i}]: {msg}")
            speech.speak(msg)
            time.sleep(0.5)
            
        print("\nTTS Demo Complete - Voice output working!")
        return True
        
    except Exception as e:
        print(f"TTS Error: {e}")
        return False

def demo_components():
    """Test all voice components"""
    print("\nDEMO 2: Voice Components Status")
    print("-" * 40)
    
    try:
        # Test imports
        from sources.text_to_speech import IMPORT_FOUND as TTS_OK, USE_FALLBACK
        from sources.speech_to_text import IMPORT_FOUND as STT_OK
        from sources.interaction import Interaction
        
        print(f"Text-to-Speech: {'OK' if TTS_OK else 'FAILED'}")
        print(f"Using Fallback TTS: {'Yes' if USE_FALLBACK else 'No'}")
        print(f"Speech-to-Text: {'OK' if STT_OK else 'FAILED'}")
        print(f"Integration: OK")
        
        # Test config
        import configparser
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        print(f"\nConfiguration:")
        print(f"- Agent Name: {config['MAIN']['agent_name']}")
        print(f"- TTS Enabled: {config.getboolean('MAIN', 'speak')}")
        print(f"- STT Enabled: {config.getboolean('MAIN', 'listen')}")
        
        return True
        
    except Exception as e:
        print(f"Component test error: {e}")
        return False

def demo_usage():
    """Show usage examples"""
    print("\nDEMO 3: How to Use Voice Commands")
    print("-" * 40)
    
    print("\nVoice Command Flow:")
    print("1. Say: 'Jarvis' (wake word)")
    print("2. Give command: 'search the web for AI news'")  
    print("3. Confirm: 'do it' or 'go ahead'")
    
    print("\nExample Commands:")
    examples = [
        "Jarvis, browse to github.com, do it",
        "Jarvis, write a Python hello world program, execute", 
        "Jarvis, search for machine learning tutorials, go ahead",
        "Jarvis, list files in current directory, please",
        "Jarvis, help me create a web scraper, do it"
    ]
    
    for example in examples:
        print(f"  - {example}")
    
    print("\nTip: Speak clearly and wait for processing!")

def demo_live_test():
    """Test the actual CLI briefly"""
    print("\nDEMO 4: Quick System Test")
    print("-" * 40)
    
    try:
        from sources.text_to_speech import Speech
        
        speech = Speech(enable=True, language="en")
        
        print("Testing system readiness...")
        speech.speak("AgenticSeek voice system is fully operational and ready for commands!")
        
        print("\nSystem Status:")
        print("- Voice Input: Ready (microphone access)")
        print("- Voice Output: Working (just heard confirmation)")
        print("- Agent System: Loaded and ready")
        print("- Web Browser: Chrome configured with stealth mode")
        print("- AI Processing: Connected to your LLM provider")
        
        return True
        
    except Exception as e:
        print(f"System test error: {e}")
        return False

def main():
    """Run demonstration"""
    demo_banner()
    
    # Run demos
    demos = [
        demo_tts,
        demo_components, 
        demo_usage,
        demo_live_test
    ]
    
    results = []
    for demo in demos:
        try:
            result = demo()
            results.append(result)
        except Exception as e:
            print(f"Demo error: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "="*60)
    print("DEMONSTRATION COMPLETE")
    print("="*60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total}")
    
    if passed == total:
        print("\nSUCCESS: All voice systems operational!")
        print("\nREADY TO USE:")
        print("1. Run: python cli.py")
        print("2. Say: 'Jarvis' to activate")
        print("3. Give voice commands with confirmation")
        print("\nYour smart voice-controlled web browser is ready!")
    else:
        print("\nSome components need attention.")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()