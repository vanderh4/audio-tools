from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import numpy as np
import soundfile as sf
from pydub import AudioSegment


@dataclass(frozen=True)
class AudioSettings:
    samplerate: int = 44100
    channels: int = 1
    dtype: str = "int16"


def build_recording_path(base_dir: Path, extension: str = "wav") -> Path:
    base_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{stamp}.{extension}"
    return base_dir / filename


def write_audio(file_path: Path, frames: list[np.ndarray], settings: AudioSettings, format: str = "wav") -> None:
    if not frames:
        raise ValueError("No audio data to write.")

    audio = frames[0]
    if len(frames) > 1:
        audio = np.concatenate(frames, axis=0)

    if format.lower() == "mp3":
        # Write to temporary WAV first
        temp_wav = file_path.with_suffix(".tmp.wav")
        sf.write(
            file=temp_wav,
            data=audio,
            samplerate=settings.samplerate,
            subtype="PCM_16",
        )
        # Convert to MP3
        audio_segment = AudioSegment.from_wav(str(temp_wav))
        audio_segment.export(str(file_path), format="mp3", bitrate="192k")
        temp_wav.unlink()  # Remove temporary file
    else:
        sf.write(
            file=file_path,
            data=audio,
            samplerate=settings.samplerate,
            subtype="PCM_16",
        )


def write_wav(file_path: Path, frames: list[np.ndarray], settings: AudioSettings) -> None:
    """Backward compatibility wrapper for write_audio with WAV format."""
    write_audio(file_path, frames, settings, format="wav")
