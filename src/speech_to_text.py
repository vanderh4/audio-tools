from __future__ import annotations

from pathlib import Path

import requests


class SpeechToText:
    def __init__(self, api_base_url: str = "http://localhost:8000") -> None:
        self._api_base_url = api_base_url.rstrip("/")
        self._transcribe_endpoint = f"{self._api_base_url}/v1/audio/transcriptions"
        self._models_endpoint = f"{self._api_base_url}/v1/models"
        self._model = "whisper-1"
        self._supported_languages: list[str] = []
        self._load_model_from_api()

    def _download_default_model(self) -> None:
        """Download default STT model if none exists."""
        try:
            model_id = "Systran%2Ffaster-whisper-large-v3"
            download_url = f"{self._api_base_url}/v1/models/{model_id}"
            response = requests.post(download_url, timeout=30)
            response.raise_for_status()
        except Exception:
            # If download fails, continue with fallback
            pass
    
    def _load_model_from_api(self) -> None:
        """Load first STT model from API with supported languages."""
        try:
            params = {"task": "automatic-speech-recognition"}
            response = requests.get(self._models_endpoint, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            models = data.get("data", [])
            
            # If no models found, try to download default model
            if not models or len(models) == 0:
                self._download_default_model()
                # Try again after download
                response = requests.get(self._models_endpoint, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                models = data.get("data", [])
            
            if models and len(models) > 0:
                first_model = models[0]
                self._model = first_model.get("id", "whisper-1")
                self._supported_languages = first_model.get("language", [])
            else:
                # Fallback
                self._model = "whisper-1"
                self._supported_languages = []
        except Exception:
            # Fallback to default
            self._model = "whisper-1"
            self._supported_languages = []
    
    def get_supported_languages(self) -> list[str]:
        """Get list of supported language codes."""
        return self._supported_languages

    def transcribe_file(self, audio_file: Path, language: str = "pt") -> str:
        """Transcribe audio file to text using Speaches API."""
        try:
            with open(audio_file, "rb") as f:
                files = {"file": (audio_file.name, f, "audio/wav")}
                data = {
                    "model": self._model,
                    "language": language,
                }
                
                response = requests.post(
                    self._transcribe_endpoint,
                    files=files,
                    data=data,
                    timeout=60,
                )
                response.raise_for_status()
                
                result = response.json()
                return result.get("text", "")
        except requests.exceptions.HTTPError as exc:
            error_detail = ""
            try:
                error_detail = exc.response.json()
            except Exception:
                error_detail = exc.response.text
            raise ValueError(f"Erro na API de transcrição ({exc.response.status_code}): {error_detail}")
        except requests.exceptions.RequestException as exc:
            raise ValueError(f"Erro na API de transcrição: {exc}")
        except Exception as exc:
            raise ValueError(f"Erro ao processar arquivo: {exc}")
