#!/usr/bin/env python3
"""
Example: Transcribe audio using Speech-to-Text
"""

from audio_tools import SpeechToText

def main():
    # Create a speech-to-text converter
    stt = SpeechToText()
    
    # Example 1: Transcribe from a file
    print("Example 1: Transcribe from audio file")
    try:
        text = stt.transcribe_file('example_recording.wav')
        print(f"Transcription: {text}")
    except FileNotFoundError:
        print("Audio file not found. Please run example_recorder.py first.")
    
    # Example 2: Transcribe from microphone (uncomment to use)
    # print("\nExample 2: Transcribe from microphone")
    # text = stt.transcribe_microphone(duration=5)
    # print(f"Transcription: {text}")

if __name__ == '__main__':
    main()
