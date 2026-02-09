"""
Text-to-Speech Module
Simple text-to-speech functionality using pyttsx3
"""

import pyttsx3
import os


class TextToSpeech:
    """
    A simple text-to-speech converter using pyttsx3.
    """
    
    def __init__(self, rate=150, volume=1.0):
        """
        Initialize the text-to-speech converter.
        
        Args:
            rate (int): Speech rate (default: 150)
            volume (float): Volume level 0.0 to 1.0 (default: 1.0)
        """
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)
        
    def speak(self, text):
        """
        Speak the given text.
        
        Args:
            text (str): Text to speak
        """
        print(f"Speaking: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
        
    def save_to_file(self, text, filename):
        """
        Save speech to an audio file.
        
        Args:
            text (str): Text to convert to speech
            filename (str): Output filename
        """
        # Ensure the file has an appropriate extension
        if not (filename.endswith('.wav') or filename.endswith('.mp3')):
            filename += '.wav'
        
        print(f"Generating speech and saving to {filename}...")
        self.engine.save_to_file(text, filename)
        self.engine.runAndWait()
        print(f"Speech saved to {filename}")
        
    def set_voice(self, voice_index=0):
        """
        Set the voice to use.
        
        Args:
            voice_index (int): Index of the voice to use (default: 0)
        """
        voices = self.engine.getProperty('voices')
        if 0 <= voice_index < len(voices):
            self.engine.setProperty('voice', voices[voice_index].id)
        else:
            print(f"Invalid voice index. Available: 0 to {len(voices)-1}")
    
    def set_rate(self, rate):
        """
        Set the speech rate.
        
        Args:
            rate (int): Speech rate (words per minute)
        """
        self.engine.setProperty('rate', rate)
        
    def set_volume(self, volume):
        """
        Set the volume level.
        
        Args:
            volume (float): Volume level from 0.0 to 1.0
        """
        if 0.0 <= volume <= 1.0:
            self.engine.setProperty('volume', volume)
        else:
            print("Volume must be between 0.0 and 1.0")
    
    def get_voices(self):
        """
        Get list of available voices.
        
        Returns:
            list: Available voices
        """
        voices = self.engine.getProperty('voices')
        return [(i, voice.name, voice.languages) for i, voice in enumerate(voices)]


def main():
    """
    Command-line interface for text-to-speech.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Simple Text-to-Speech Converter')
    parser.add_argument('text', type=str, nargs='?',
                        help='Text to convert to speech')
    parser.add_argument('-f', '--file', type=str,
                        help='Read text from file')
    parser.add_argument('-o', '--output', type=str,
                        help='Save speech to audio file')
    parser.add_argument('-r', '--rate', type=int, default=150,
                        help='Speech rate (default: 150)')
    parser.add_argument('-v', '--volume', type=float, default=1.0,
                        help='Volume level 0.0 to 1.0 (default: 1.0)')
    parser.add_argument('--voice', type=int, default=0,
                        help='Voice index (default: 0)')
    parser.add_argument('--list-voices', action='store_true',
                        help='List available voices')
    
    args = parser.parse_args()
    
    tts = TextToSpeech(rate=args.rate, volume=args.volume)
    tts.set_voice(args.voice)
    
    if args.list_voices:
        print("Available voices:")
        for idx, name, languages in tts.get_voices():
            print(f"{idx}: {name} - {languages}")
    elif args.file:
        if not os.path.exists(args.file):
            print(f"File not found: {args.file}")
            return
        with open(args.file, 'r') as f:
            text = f.read()
        if args.output:
            tts.save_to_file(text, args.output)
        else:
            tts.speak(text)
    elif args.text:
        if args.output:
            tts.save_to_file(args.text, args.output)
        else:
            tts.speak(args.text)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
