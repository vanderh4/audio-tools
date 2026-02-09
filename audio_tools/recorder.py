"""
Audio Recorder Module
Simple audio recording functionality using sounddevice
"""

import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import os


class AudioRecorder:
    """
    A simple audio recorder class for capturing audio from the microphone.
    """
    
    def __init__(self, sample_rate=44100, channels=1):
        """
        Initialize the audio recorder.
        
        Args:
            sample_rate (int): Sample rate in Hz (default: 44100)
            channels (int): Number of audio channels (default: 1 for mono)
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.recording = None
        
    def record(self, duration, filename=None):
        """
        Record audio for a specified duration.
        
        Args:
            duration (float): Duration in seconds
            filename (str, optional): Output filename (default: None, returns numpy array)
            
        Returns:
            numpy.ndarray: Recorded audio data if filename is None
        """
        print(f"Recording for {duration} seconds...")
        self.recording = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype='float64'
        )
        sd.wait()  # Wait until recording is finished
        print("Recording finished.")
        
        if filename:
            self.save(filename)
        
        return self.recording
    
    def save(self, filename):
        """
        Save the recorded audio to a WAV file.
        
        Args:
            filename (str): Output filename
        """
        if self.recording is None:
            raise ValueError("No recording available. Please record audio first.")
        
        # Ensure the file has a .wav extension
        if not filename.endswith('.wav'):
            filename += '.wav'
        
        # Convert to int16 for WAV file
        audio_data = np.int16(self.recording * 32767)
        write(filename, self.sample_rate, audio_data)
        print(f"Audio saved to {filename}")
        
    def get_devices(self):
        """
        Get list of available audio input devices.
        
        Returns:
            list: Available audio devices
        """
        return sd.query_devices()


def main():
    """
    Command-line interface for audio recorder.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Simple Audio Recorder')
    parser.add_argument('-d', '--duration', type=float, default=5.0,
                        help='Recording duration in seconds (default: 5.0)')
    parser.add_argument('-o', '--output', type=str, default='recording.wav',
                        help='Output filename (default: recording.wav)')
    parser.add_argument('-r', '--sample-rate', type=int, default=44100,
                        help='Sample rate in Hz (default: 44100)')
    parser.add_argument('-c', '--channels', type=int, default=1,
                        help='Number of channels (default: 1)')
    parser.add_argument('--list-devices', action='store_true',
                        help='List available audio devices')
    
    args = parser.parse_args()
    
    recorder = AudioRecorder(sample_rate=args.sample_rate, channels=args.channels)
    
    if args.list_devices:
        print("Available audio devices:")
        print(recorder.get_devices())
    else:
        recorder.record(args.duration, args.output)


if __name__ == '__main__':
    main()
