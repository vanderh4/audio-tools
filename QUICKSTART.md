# Quick Start Guide

This guide will help you get started with the audio-tools package quickly.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/vanderh4/audio-tools.git
   cd audio-tools
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install system dependencies (Linux):
   ```bash
   # For audio recording
   sudo apt-get install portaudio19-dev
   
   # For text-to-speech
   sudo apt-get install espeak espeak-ng
   ```

## Quick Examples

### 1. Record Audio (5 seconds)
```bash
python -m audio_tools.recorder -d 5 -o my_recording.wav
```

### 2. Convert Text to Speech
```bash
python -m audio_tools.tts "Hello, this is a test!" -o hello.wav
```

### 3. Transcribe Audio to Text
```bash
python -m audio_tools.stt -f my_recording.wav
```

### 4. Use in Python Code

```python
from audio_tools import AudioRecorder, SpeechToText, TextToSpeech

# Record audio
recorder = AudioRecorder()
recorder.record(duration=5.0, filename='recording.wav')

# Convert text to speech
tts = TextToSpeech()
tts.speak("Hello, world!")
tts.save_to_file("Save this to a file", "output.wav")

# Convert speech to text
stt = SpeechToText()
text = stt.transcribe_file('recording.wav')
print(f"Transcription: {text}")
```

## Running Tests

```bash
python tests/test_audio_tools.py
```

## Running Examples

```bash
cd examples
python example_recorder.py
python example_tts.py
python example_stt.py
```

## Common Issues

### PortAudio not found
If you get a "PortAudio library not found" error, install it:
```bash
sudo apt-get install portaudio19-dev
```

### eSpeak not found
If you get an eSpeak error, install it:
```bash
sudo apt-get install espeak espeak-ng
```

### Microphone permission denied
Make sure your user has permission to access the microphone.

## Getting Help

For more detailed information, see the [README.md](README.md) file.
