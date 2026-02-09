#!/usr/bin/env python3
"""
Example: Convert text to speech using Text-to-Speech
"""

from audio_tools import TextToSpeech

def main():
    # Create a text-to-speech converter
    tts = TextToSpeech(rate=150, volume=1.0)
    
    # Example 1: Speak text
    print("Example 1: Speaking text")
    tts.speak("Hello! This is a simple text to speech example.")
    
    # Example 2: Save speech to file
    print("\nExample 2: Saving speech to file")
    tts.save_to_file(
        "Welcome to the audio tools library. This demonstrates text to speech functionality.",
        "example_tts_output.wav"
    )
    
    # Example 3: List available voices
    print("\nExample 3: Available voices")
    voices = tts.get_voices()
    for idx, name, languages in voices[:3]:  # Show first 3 voices
        print(f"  {idx}: {name}")

if __name__ == '__main__':
    main()
