import time

import numpy as np
import sounddevice as sd
import pytest

from src.audio_utils import AudioSettings
from src.recorder import AudioRecorder


class FakeStream:
    def __init__(self, *args, **kwargs) -> None:
        self.callback = kwargs["callback"]
        self.started = False
        self.stopped = False
        self.closed = False

    def start(self) -> None:
        self.started = True

    def stop(self) -> None:
        self.stopped = True

    def close(self) -> None:
        self.closed = True


@pytest.mark.skipif(not hasattr(sd, "InputStream"), reason="sounddevice not available")
def test_recorder_collects_frames(monkeypatch) -> None:
    holder = {}

    def fake_input_stream(*args, **kwargs):
        stream = FakeStream(*args, **kwargs)
        holder["stream"] = stream
        return stream

    monkeypatch.setattr(sd, "InputStream", fake_input_stream)

    settings = AudioSettings()
    recorder = AudioRecorder(settings)
    recorder.start()

    chunk = np.zeros((50, settings.channels), dtype=np.int16)
    recorder._callback(chunk, chunk.shape[0], None, None)
    recorder._callback(chunk, chunk.shape[0], None, None)

    time.sleep(0.2)
    frames = recorder.stop()

    assert holder["stream"].started
    assert holder["stream"].stopped
    assert holder["stream"].closed
    assert len(frames) >= 2
    assert frames[0].shape == (50, settings.channels)


def test_stop_without_start() -> None:
    settings = AudioSettings()
    recorder = AudioRecorder(settings)

    assert recorder.stop() == []
