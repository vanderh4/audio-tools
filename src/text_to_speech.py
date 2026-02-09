from __future__ import annotations

from pathlib import Path

import requests


class TextToSpeech:
    def __init__(self, api_base_url: str = "http://localhost:8000") -> None:
        self._api_base_url = api_base_url.rstrip("/")
        self._speech_endpoint = f"{self._api_base_url}/v1/audio/speech"
        self._models_endpoint = f"{self._api_base_url}/v1/models"
        self._current_voice = "alloy"  # Default voice
        self._voice_names: list[str] = []  # Formatted names for display
        self._voice_id_map: dict[str, str] = {}  # Map display name -> voice ID
        self._model = "tts-1"
        self._load_model_and_voices_from_api()

    def _download_default_model(self) -> None:
        """Download default TTS model if none exists."""
        try:
            model_id = "speaches-ai%2FKokoro-82M-v1.0-ONNX-int8"
            download_url = f"{self._api_base_url}/v1/models/{model_id}"
            response = requests.post(download_url, timeout=30)
            response.raise_for_status()
        except Exception:
            # If download fails, continue with fallback
            pass
    
    def _load_model_and_voices_from_api(self) -> None:
        """Load first TTS model from API with its voices."""
        try:
            params = {"task": "text-to-speech"}
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
                self._model = first_model.get("id", "tts-1")
                voices = first_model.get("voices", [])
                
                if voices:
                    # Create formatted names and mapping
                    for voice in voices:
                        voice_id = voice.get("id", voice.get("name", ""))
                        voice_name = voice.get("name", voice_id)
                        language = voice.get("language", "unknown").upper()
                        
                        # Format: "name-LANGUAGE"
                        display_name = f"{voice_name}-{language}"
                        self._voice_names.append(display_name)
                        self._voice_id_map[display_name] = voice_id
                    
                    # Prefer Portuguese voices as default
                    for display_name, voice_id in self._voice_id_map.items():
                        if "PT-BR" in display_name or "PT" in display_name:
                            self._current_voice = voice_id
                            return
                    
                    # Use first voice as default
                    if self._voice_names:
                        self._current_voice = self._voice_id_map[self._voice_names[0]]
                    return
            
            # Fallback if no models/voices found
            self._setup_fallback_voices()
        except Exception:
            # Fallback to default voices if API call fails
            self._setup_fallback_voices()
    
    def _setup_fallback_voices(self) -> None:
        """Setup fallback voices when API is unavailable."""
        fallback = [
            ("af_alloy", "alloy", "EN-US"),
            ("am_echo", "echo", "EN-US"),
            ("bm_fable", "fable", "EN-GB"),
            ("am_onyx", "onyx", "EN-US"),
            ("af_nova", "nova", "EN-US"),
            ("pf_dora", "dora", "PT-BR"),
            ("pm_alex", "alex", "PT-BR"),
        ]
        for voice_id, name, lang in fallback:
            display_name = f"{name}-{lang}"
            self._voice_names.append(display_name)
            self._voice_id_map[display_name] = voice_id
        
        self._current_voice = "pf_dora"  # Portuguese female voice as default

    def speak(self, text: str) -> None:
        """Speak the text immediately (saves to temp file and plays)."""
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        
        try:
            self.save_to_file(text, tmp_path)
            # Play the audio file
            os.startfile(str(tmp_path))
        finally:
            # Note: file cleanup happens after playback
            pass

    def save_to_file(self, text: str, output_path: Path) -> None:
        """Convert text to speech and save to file using Speaches API."""
        try:
            payload = {
                "input": text,
                "voice": self._current_voice,
                "model": self._model,
            }
            
            response = requests.post(
                self._speech_endpoint,
                json=payload,
                timeout=60,
            )
            response.raise_for_status()
            
            # Save audio content to file
            with open(output_path, "wb") as f:
                f.write(response.content)
        except requests.exceptions.HTTPError as exc:
            error_detail = ""
            try:
                error_detail = exc.response.json()
            except Exception:
                error_detail = exc.response.text
            raise ValueError(f"Erro na API de síntese ({exc.response.status_code}): {error_detail}")
        except requests.exceptions.RequestException as exc:
            raise ValueError(f"Erro na API de síntese: {exc}")
        except Exception as exc:
            raise ValueError(f"Erro ao salvar arquivo: {exc}")

    def get_voices(self) -> list[str]:
        """Get available voice names (formatted as 'name-LANGUAGE')."""
        return self._voice_names

    def set_voice(self, voice_index: int) -> None:
        """Set voice by index."""
        if 0 <= voice_index < len(self._voice_names):
            display_name = self._voice_names[voice_index]
            self._current_voice = self._voice_id_map[display_name]
