"""
Speech-to-Text Module
Simple speech recognition functionality using SpeechRecognition
"""

import speech_recognition as sr
import os


class SpeechToText:
    """
    A simple speech-to-text converter using Google Speech Recognition.
    """
    
    def __init__(self):
        """
        Initialize the speech-to-text converter.
        """
        self.recognizer = sr.Recognizer()
        
    def transcribe_file(self, audio_file, language='en-US'):
        """
        Transcribe audio from a file.
        
        Args:
            audio_file (str): Path to the audio file
            language (str): Language code (default: 'en-US')
            
        Returns:
            str: Transcribed text
        """
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Audio file not found: {audio_file}")
        
        with sr.AudioFile(audio_file) as source:
            print(f"Loading audio from {audio_file}...")
            audio_data = self.recognizer.record(source)
            
        try:
            print("Transcribing...")
            text = self.recognizer.recognize_google(audio_data, language=language)
            print("Transcription complete.")
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Error with the speech recognition service: {e}"
    
    def transcribe_microphone(self, duration=5, language='en-US'):
        """
        Transcribe audio directly from the microphone.
        
        Args:
            duration (int): Duration in seconds (default: 5)
            language (str): Language code (default: 'en-US')
            
        Returns:
            str: Transcribed text
        """
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print(f"Listening for {duration} seconds...")
            audio_data = self.recognizer.record(source, duration=duration)
            
        try:
            print("Transcribing...")
            text = self.recognizer.recognize_google(audio_data, language=language)
            print("Transcription complete.")
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Error with the speech recognition service: {e}"
    
    def get_supported_languages(self):
        """
        Get information about supported languages.
        
        Returns:
            str: Information about language support
        """
        return """
        Common language codes:
        - en-US: English (US)
        - en-GB: English (UK)
        - es-ES: Spanish (Spain)
        - fr-FR: French
        - de-DE: German
        - it-IT: Italian
        - pt-BR: Portuguese (Brazil)
        - zh-CN: Chinese (Simplified)
        - ja-JP: Japanese
        - ko-KR: Korean
        """


def main():
    """
    Command-line interface for speech-to-text.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Simple Speech-to-Text Converter')
    parser.add_argument('-f', '--file', type=str,
                        help='Audio file to transcribe')
    parser.add_argument('-m', '--microphone', action='store_true',
                        help='Transcribe from microphone')
    parser.add_argument('-d', '--duration', type=int, default=5,
                        help='Duration in seconds for microphone input (default: 5)')
    parser.add_argument('-l', '--language', type=str, default='en-US',
                        help='Language code (default: en-US)')
    parser.add_argument('--list-languages', action='store_true',
                        help='List supported languages')
    
    args = parser.parse_args()
    
    stt = SpeechToText()
    
    if args.list_languages:
        print(stt.get_supported_languages())
    elif args.file:
        text = stt.transcribe_file(args.file, args.language)
        print(f"\nTranscription: {text}")
    elif args.microphone:
        text = stt.transcribe_microphone(args.duration, args.language)
        print(f"\nTranscription: {text}")
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
