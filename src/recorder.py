from __future__ import annotations

import queue
import threading
from dataclasses import dataclass
from typing import Optional

import numpy as np
import sounddevice as sd

try:
    from .audio_utils import AudioSettings
except ImportError:  # pragma: no cover
    from audio_utils import AudioSettings


@dataclass
class RecorderState:
    is_recording: bool = False
    frames: list[np.ndarray] | None = None


class AudioRecorder:
    def __init__(self, settings: AudioSettings) -> None:
        self._settings = settings
        self._state = RecorderState(is_recording=False, frames=[])
        self._queue: queue.Queue = queue.Queue()
        self._stream: Optional[sd.InputStream] = None
        self._worker: Optional[threading.Thread] = None

    @property
    def is_recording(self) -> bool:
        return self._state.is_recording

    def start(self) -> None:
        if self._state.is_recording:
            return

        self._state = RecorderState(is_recording=True, frames=[])
        self._queue = queue.Queue()

        self._stream = sd.InputStream(
            samplerate=self._settings.samplerate,
            channels=self._settings.channels,
            dtype=self._settings.dtype,
            callback=self._callback,
        )
        self._stream.start()

        self._worker = threading.Thread(target=self._collect_frames, daemon=True)
        print("Starting recording thread...")
        self._worker.start()

    def stop(self) -> list[np.ndarray]:
        if not self._state.is_recording:
            return []

        self._state.is_recording = False
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()
            self._stream = None

        if self._worker is not None:
            self._worker.join(timeout=1)
            self._worker = None

        frames = self._state.frames or []
        self._state = RecorderState(is_recording=False, frames=[])
        return frames

    def _callback(self, indata, frames, time, status) -> None:  # noqa: ARG002
        if status:
            return
        self._queue.put(indata.copy())

    def _collect_frames(self) -> None:
        while self._state.is_recording:
            try:
                chunk = self._queue.get(timeout=0.1)
                if self._state.frames is not None:
                    self._state.frames.append(chunk)
            except queue.Empty:
                continue
