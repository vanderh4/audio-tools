import re
from pathlib import Path

import numpy as np
import pytest
import soundfile as sf

from src.audio_utils import AudioSettings, build_recording_path, write_wav


def test_build_recording_path(tmp_path: Path) -> None:
    path = build_recording_path(tmp_path)

    assert path.parent == tmp_path
    assert re.fullmatch(r"\d{8}_\d{6}\.wav", path.name)


def test_write_wav_creates_file(tmp_path: Path) -> None:
    settings = AudioSettings()
    frames = [np.zeros((100, settings.channels), dtype=np.int16)]
    file_path = tmp_path / "test.wav"

    write_wav(file_path, frames, settings)

    assert file_path.exists()
    data, samplerate = sf.read(file_path, dtype="int16")
    assert samplerate == settings.samplerate
    assert data.shape[0] == 100


def test_write_wav_raises_on_empty(tmp_path: Path) -> None:
    settings = AudioSettings()

    with pytest.raises(ValueError):
        write_wav(tmp_path / "empty.wav", [], settings)
