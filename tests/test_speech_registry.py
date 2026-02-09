"""Tests for Speech-to-Text models endpoint integration."""
from unittest.mock import Mock, patch
from pathlib import Path

import pytest
import requests

from src.speech_to_text import SpeechToText


def test_get_model_from_models_endpoint():
    """Test that STT fetches model from models endpoint with task filter."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "data": [
            {
                "id": "Systran/faster-whisper-large-v3",
                "language": ["en", "zh", "de", "es", "ru", "pt", "fr"],
                "created": 1770582077,
                "object": "model",
            }
        ],
        "object": "list",
    }
    mock_response.raise_for_status = Mock()
    
    with patch("requests.get", return_value=mock_response) as mock_get:
        stt = SpeechToText()
        
        # Should call models endpoint with params
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "v1/models" in call_args[0][0]  # URL
        assert call_args[1].get("params") == {"task": "automatic-speech-recognition"}  # params
        
        # Should use first model
        assert stt._model == "Systran/faster-whisper-large-v3"
        
        # Should store supported languages
        assert hasattr(stt, "_supported_languages")
        assert "pt" in stt._supported_languages
        assert "en" in stt._supported_languages


def test_get_model_fallback_on_error():
    """Test that STT falls back to default when registry fails."""
    with patch("requests.get", side_effect=requests.exceptions.RequestException("API error")):
        stt = SpeechToText()
        
        # Should fallback to default
        assert stt._model == "whisper-1"
        assert hasattr(stt, "_supported_languages")


def test_transcribe_validates_language():
    """Test that transcribe validates language against supported list."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "data": [
            {
                "id": "Systran/faster-whisper-large-v3",
                "language": ["en", "es", "fr"],
            }
        ],
        "object": "list",
    }
    mock_response.raise_for_status = Mock()
    
    with patch("requests.get", return_value=mock_response):
        stt = SpeechToText()
        
        # Should have limited language support
        assert "en" in stt._supported_languages
        assert "pt" not in stt._supported_languages


def test_get_supported_languages():
    """Test that STT exposes supported languages."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "data": [
            {
                "id": "test-model",
                "language": ["en", "pt", "es"],
            }
        ],
        "object": "list",
    }
    mock_response.raise_for_status = Mock()
    
    with patch("requests.get", return_value=mock_response):
        stt = SpeechToText()
        
        # Should expose getter for languages
        assert hasattr(stt, "get_supported_languages")
        languages = stt.get_supported_languages()
        assert languages == ["en", "pt", "es"]


def test_download_model_when_none_available():
    """Test that default model is downloaded when no models are available."""
    # First GET returns empty list, second GET returns model after download
    mock_get_responses = [
        Mock(
            json=lambda: {"data": [], "object": "list"},
            raise_for_status=Mock(),
        ),
        Mock(
            json=lambda: {
                "data": [
                    {
                        "id": "Systran/faster-whisper-large-v3",
                        "object": "model",
                        "language": ["en", "pt", "es"],
                    }
                ],
                "object": "list",
            },
            raise_for_status=Mock(),
        ),
    ]
    
    mock_post_response = Mock(raise_for_status=Mock())
    
    with patch("requests.get", side_effect=mock_get_responses) as mock_get, \
         patch("requests.post", return_value=mock_post_response) as mock_post:
        stt = SpeechToText(api_base_url="http://localhost:8000")
        
        # Verify POST was called with correct URL
        mock_post.assert_called_once_with(
            "http://localhost:8000/v1/models/Systran%2Ffaster-whisper-large-v3",
            timeout=30
        )
        
        # Verify model was loaded after download
        assert stt._model == "Systran/faster-whisper-large-v3"
        assert "pt" in stt._supported_languages
