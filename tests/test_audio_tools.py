"""
Unit tests for the audio_tools package
"""

import unittest
import os
import sys
import tempfile

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from audio_tools import AudioRecorder, SpeechToText, TextToSpeech


class TestAudioRecorder(unittest.TestCase):
    """Test cases for AudioRecorder class"""
    
    def test_init(self):
        """Test AudioRecorder initialization"""
        recorder = AudioRecorder()
        self.assertIsNotNone(recorder)
        self.assertEqual(recorder.sample_rate, 44100)
        self.assertEqual(recorder.channels, 1)
    
    def test_custom_init(self):
        """Test AudioRecorder with custom parameters"""
        recorder = AudioRecorder(sample_rate=48000, channels=2)
        self.assertEqual(recorder.sample_rate, 48000)
        self.assertEqual(recorder.channels, 2)
    
    def test_get_devices(self):
        """Test getting audio devices"""
        recorder = AudioRecorder()
        devices = recorder.get_devices()
        # Should return some kind of device list (could be empty in CI)
        self.assertIsNotNone(devices)


class TestSpeechToText(unittest.TestCase):
    """Test cases for SpeechToText class"""
    
    def test_init(self):
        """Test SpeechToText initialization"""
        stt = SpeechToText()
        self.assertIsNotNone(stt)
        self.assertIsNotNone(stt.recognizer)
    
    def test_get_supported_languages(self):
        """Test getting supported languages"""
        stt = SpeechToText()
        languages = stt.get_supported_languages()
        self.assertIsNotNone(languages)
        self.assertIn('en-US', languages)
    
    def test_transcribe_file_not_found(self):
        """Test transcribing non-existent file raises error"""
        stt = SpeechToText()
        with self.assertRaises(FileNotFoundError):
            stt.transcribe_file('nonexistent_file.wav')


class TestTextToSpeech(unittest.TestCase):
    """Test cases for TextToSpeech class"""
    
    def test_init(self):
        """Test TextToSpeech initialization"""
        tts = TextToSpeech()
        self.assertIsNotNone(tts)
        self.assertIsNotNone(tts.engine)
    
    def test_custom_init(self):
        """Test TextToSpeech with custom parameters"""
        tts = TextToSpeech(rate=200, volume=0.5)
        self.assertIsNotNone(tts)
    
    def test_get_voices(self):
        """Test getting available voices"""
        tts = TextToSpeech()
        voices = tts.get_voices()
        self.assertIsNotNone(voices)
        self.assertIsInstance(voices, list)
    
    def test_save_to_file(self):
        """Test saving speech to file"""
        tts = TextToSpeech()
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            tts.save_to_file("Test", tmp_path)
            # Check if file was created
            self.assertTrue(os.path.exists(tmp_path))
        finally:
            # Clean up
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    def test_set_rate(self):
        """Test setting speech rate"""
        tts = TextToSpeech()
        tts.set_rate(200)
        # No exception should be raised
        self.assertTrue(True)
    
    def test_set_volume(self):
        """Test setting volume"""
        tts = TextToSpeech()
        tts.set_volume(0.5)
        # No exception should be raised
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
