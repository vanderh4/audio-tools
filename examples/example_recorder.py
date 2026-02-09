#!/usr/bin/env python3
"""
Example: Record audio using the AudioRecorder
"""

from audio_tools import AudioRecorder

def main():
    # Create an audio recorder with default settings
    recorder = AudioRecorder(sample_rate=44100, channels=1)
    
    # Record for 5 seconds and save to file
    print("Recording will start in 3 seconds...")
    print("3...")
    import time
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    
    recorder.record(duration=5.0, filename='example_recording.wav')
    print("Recording saved as 'example_recording.wav'")

if __name__ == '__main__':
    main()
