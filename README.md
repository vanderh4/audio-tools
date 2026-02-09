# audio-tools

Simple implementations of audio tools for recording, speech-to-text, and text-to-speech.

## Features

- **Audio Recorder**: Record audio from your microphone and save to WAV files
- **Speech-to-Text (STT)**: Convert speech in audio files or from microphone to text
- **Text-to-Speech (TTS)**: Convert text to speech with customizable voice and speed

## Installation

```bash
pip install -r requirements.txt
```

Or install in development mode:

```bash
pip install -e .
```

## Requirements

- Python 3.7+
- sounddevice
- scipy
- numpy
- SpeechRecognition
- pyttsx3

## Usage

### Audio Recorder

**As a Python module:**

```python
from audio_tools import AudioRecorder

# Create recorder
recorder = AudioRecorder(sample_rate=44100, channels=1)

# Record for 5 seconds
recorder.record(duration=5.0, filename='my_recording.wav')
```

**Command-line:**

```bash
# Record 5 seconds of audio
python -m audio_tools.recorder -d 5 -o recording.wav

# Record with custom sample rate
python -m audio_tools.recorder -d 10 -o recording.wav -r 48000

# List available audio devices
python -m audio_tools.recorder --list-devices
```

### Speech-to-Text (STT)

**As a Python module:**

```python
from audio_tools import SpeechToText

# Create speech-to-text converter
stt = SpeechToText()

# Transcribe from audio file
text = stt.transcribe_file('recording.wav')
print(text)

# Transcribe from microphone
text = stt.transcribe_microphone(duration=5)
print(text)
```

**Command-line:**

```bash
# Transcribe audio file
python -m audio_tools.stt -f recording.wav

# Transcribe from microphone
python -m audio_tools.stt -m -d 5

# Transcribe with specific language
python -m audio_tools.stt -f recording.wav -l es-ES

# List supported languages
python -m audio_tools.stt --list-languages
```

### Text-to-Speech (TTS)

**As a Python module:**

```python
from audio_tools import TextToSpeech

# Create text-to-speech converter
tts = TextToSpeech(rate=150, volume=1.0)

# Speak text
tts.speak("Hello, world!")

# Save speech to file
tts.save_to_file("Hello, world!", "output.wav")

# Change voice
tts.set_voice(1)

# List available voices
voices = tts.get_voices()
for idx, name, languages in voices:
    print(f"{idx}: {name}")
```

**Command-line:**

```bash
# Speak text
python -m audio_tools.tts "Hello, world!"

# Save speech to file
python -m audio_tools.tts "Hello, world!" -o output.wav

# Read from text file and speak
python -m audio_tools.tts -f input.txt

# Customize speech rate and volume
python -m audio_tools.tts "Hello" -r 200 -v 0.8

# List available voices
python -m audio_tools.tts --list-voices

# Use specific voice
python -m audio_tools.tts "Hello" --voice 1
```

## Examples

See the `examples/` directory for complete usage examples:

- `examples/example_recorder.py` - Audio recording example
- `examples/example_stt.py` - Speech-to-text example
- `examples/example_tts.py` - Text-to-speech example

Run examples:

```bash
cd examples
python example_recorder.py
python example_stt.py
python example_tts.py
```

## API Reference

### AudioRecorder

- `__init__(sample_rate=44100, channels=1)` - Initialize recorder
- `record(duration, filename=None)` - Record audio for specified duration
- `save(filename)` - Save recorded audio to file
- `get_devices()` - List available audio input devices

### SpeechToText

- `__init__()` - Initialize speech-to-text converter
- `transcribe_file(audio_file, language='en-US')` - Transcribe audio file
- `transcribe_microphone(duration=5, language='en-US')` - Transcribe from microphone
- `get_supported_languages()` - Get list of supported languages

### TextToSpeech

- `__init__(rate=150, volume=1.0)` - Initialize text-to-speech converter
- `speak(text)` - Speak the given text
- `save_to_file(text, filename)` - Save speech to audio file
- `set_voice(voice_index)` - Set the voice to use
- `set_rate(rate)` - Set speech rate
- `set_volume(volume)` - Set volume level
- `get_voices()` - Get list of available voices

## Notes

- Speech-to-Text uses Google's speech recognition API, which requires an internet connection
- Text-to-Speech uses the system's built-in TTS engine (pyttsx3)
- Audio recording requires a working microphone
- The quality and features available may vary depending on your operating system

## License

MIT License

## Author

vanderh4