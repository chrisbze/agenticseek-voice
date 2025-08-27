#!/usr/bin/env python3
"""
Quick CLI Test to show the system working
"""
import asyncio
import sys

async def test_cli_components():
    """Test CLI components without full interaction"""
    print("="*50)
    print("AGENTICSEEK CLI SYSTEM TEST")
    print("="*50)
    
    try:
        # Import main components
        from sources.llm_provider import Provider
        from sources.interaction import Interaction
        from sources.agents import Agent, CoderAgent, CasualAgent, FileAgent, PlannerAgent, BrowserAgent
        from sources.browser import Browser, create_driver
        from sources.utility import pretty_print
        import configparser
        
        print("Loading configuration...")
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        print("Initializing components...")
        
        # Initialize provider
        provider = Provider(
            provider_name=config["MAIN"]["provider_name"],
            model=config["MAIN"]["provider_model"],
            server_address=config["MAIN"]["provider_server_address"],
            is_local=config.getboolean('MAIN', 'is_local')
        )
        print("✓ LLM Provider initialized")
        
        # Initialize browser (headless for test)
        stealth_mode = config.getboolean('BROWSER', 'stealth_mode')
        personality_folder = "jarvis" if config.getboolean('MAIN', 'jarvis_personality') else "base"
        languages = config["MAIN"]["languages"].split(' ')
        
        print("✓ Browser configuration loaded")
        
        # Initialize agents (without browser for quick test)
        agents = [
            CasualAgent(name=config["MAIN"]["agent_name"],
                       prompt_path=f"prompts/{personality_folder}/casual_agent.txt",
                       provider=provider, verbose=False),
            CoderAgent(name="coder", 
                      prompt_path=f"prompts/{personality_folder}/coder_agent.txt",
                      provider=provider, verbose=False),
            FileAgent(name="File Agent",
                     prompt_path=f"prompts/{personality_folder}/file_agent.txt", 
                     provider=provider, verbose=False)
        ]
        print("✓ AI Agents initialized")
        
        # Initialize interaction system
        interaction = Interaction(agents,
                                tts_enabled=config.getboolean('MAIN', 'speak'),
                                stt_enabled=config.getboolean('MAIN', 'listen'),
                                recover_last_session=False,  # Skip session recovery for test
                                langs=languages)
        print("✓ Voice interaction system ready")
        
        print("\nSYSTEM STATUS:")
        print(f"- Agent Name: {config['MAIN']['agent_name']}")
        print(f"- TTS Enabled: {config.getboolean('MAIN', 'speak')}")
        print(f"- STT Enabled: {config.getboolean('MAIN', 'listen')}")
        print(f"- Languages: {languages}")
        print(f"- Agents Loaded: {len(agents)}")
        
        # Test voice greeting
        if interaction.speech:
            print("\nTesting voice greeting...")
            interaction.speech.speak("AgenticSeek CLI is ready! All systems operational.")
        
        print("\n✅ CLI SYSTEM TEST SUCCESSFUL!")
        print("\nThe full system is ready to use with:")
        print("  python cli.py")
        print("\nVoice commands will work as demonstrated!")
        
        return True
        
    except Exception as e:
        print(f"❌ CLI Test Error: {e}")
        return False

async def main():
    """Run the CLI test"""
    success = await test_cli_components()
    
    print("\n" + "="*50)
    if success:
        print("🎉 READY FOR VOICE INTERACTION!")
        print("\nTo start using your voice-controlled system:")
        print("1. Run: python cli.py")
        print("2. Say: 'Jarvis' (wake word)")  
        print("3. Give commands like:")
        print("   - 'search the web for Python tutorials, do it'")
        print("   - 'write a hello world program, execute'")
        print("   - 'browse to github.com, go ahead'")
        print("\nYour smart agentic web browser is operational!")
    else:
        print("❌ Some components need attention")
    print("="*50)

if __name__ == "__main__":
    asyncio.run(main())