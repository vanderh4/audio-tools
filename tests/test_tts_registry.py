"""Tests for Text-to-Speech models endpoint integration."""
from unittest.mock import Mock, patch

import pytest
import requests

from src.text_to_speech import TextToSpeech


def test_get_model_from_models_endpoint():
    """Test that TTS fetches model from models endpoint with task filter."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "data": [
            {
                "id": "speaches-ai/Kokoro-82M-v1.0-ONNX",
                "language": ["multilingual"],
                "task": "text-to-speech",
                "voices": [
                    {"name": "af_alloy", "language": "en-us", "gender": "female", "id": "af_alloy"},
                    {"name": "pf_dora", "language": "pt-br", "gender": "female", "id": "pf_dora"},
                    {"name": "pm_alex", "language": "pt-br", "gender": "male", "id": "pm_alex"},
                ],
            }
        ],
        "object": "list",
    }
    mock_response.raise_for_status = Mock()
    
    with patch("requests.get", return_value=mock_response) as mock_get:
        tts = TextToSpeech()
        
        # Should call models endpoint with params
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "v1/models" in call_args[0][0]  # URL
        assert call_args[1].get("params") == {"task": "text-to-speech"}  # params
        
        # Should use first model
        assert tts._model == "speaches-ai/Kokoro-82M-v1.0-ONNX"
        
        # Should load voices from first model
        voices = tts.get_voices()
        assert len(voices) == 3
        assert "af_alloy-EN-US" in voices
        assert "pf_dora-PT-BR" in voices
        assert "pm_alex-PT-BR" in voices


def test_get_model_fallback_on_error():
    """Test that TTS falls back to defaults when registry fails."""
    with patch("requests.get", side_effect=requests.exceptions.RequestException("API error")):
        tts = TextToSpeech()
        
        # Should fallback to default
        assert tts._model == "tts-1"
        
        # Should have fallback voices
        voices = tts.get_voices()
        assert len(voices) > 0


def test_voice_formatting():
    """Test that voices are formatted as 'name-LANGUAGE'."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "data": [
            {
                "id": "test-model",
                "voices": [
                    {"name": "alice", "language": "en-gb", "id": "alice_gb"},
                    {"name": "joao", "language": "pt-br", "id": "joao_br"},
                ],
            }
        ],
        "object": "list",
    }
    mock_response.raise_for_status = Mock()
    
    with patch("requests.get", return_value=mock_response):
        tts = TextToSpeech()
        
        voices = tts.get_voices()
        assert "alice-EN-GB" in voices
        assert "joao-PT-BR" in voices


def test_default_portuguese_voice():
    """Test that Portuguese voice is selected as default when available."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "data": [
            {
                "id": "test-model",
                "voices": [
                    {"name": "alice", "language": "en-us", "id": "alice_us"},
                    {"name": "maria", "language": "pt-br", "id": "maria_br"},
                    {"name": "bob", "language": "en-gb", "id": "bob_gb"},
                ],
            }
        ],
        "object": "list",
    }
    mock_response.raise_for_status = Mock()
    
    with patch("requests.get", return_value=mock_response):
        tts = TextToSpeech()
        
        # Should default to Portuguese voice
        assert tts._current_voice == "maria_br"


def test_voice_id_mapping():
    """Test that voice display names map correctly to voice IDs."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "data": [
            {
                "id": "test-model",
                "voices": [
                    {"name": "alice", "language": "en-us", "id": "voice_alice_001"},
                ],
            }
        ],
        "object": "list",
    }
    mock_response.raise_for_status = Mock()
    
    with patch("requests.get", return_value=mock_response):
        tts = TextToSpeech()
        
        # Display name should be formatted
        assert "alice-EN-US" in tts.get_voices()
        
        # But internal mapping should use actual voice ID
        tts.set_voice(0)
        assert tts._current_voice == "voice_alice_001"


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
                        "id": "speaches-ai/Kokoro-82M-v1.0-ONNX-int8",
                        "object": "model",
                        "voices": [
                            {"id": "pf_dora", "name": "dora", "language": "pt-br", "gender": "female"},
                            {"id": "af_alloy", "name": "alloy", "language": "en-us", "gender": "female"},
                        ],
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
        tts = TextToSpeech(api_base_url="http://localhost:8000")
        
        # Verify POST was called with correct URL
        mock_post.assert_called_once_with(
            "http://localhost:8000/v1/models/speaches-ai%2FKokoro-82M-v1.0-ONNX-int8",
            timeout=30
        )
        
        # Verify model was loaded after download
        assert tts._model == "speaches-ai/Kokoro-82M-v1.0-ONNX-int8"
        assert len(tts._voice_names) == 2
        assert "dora-PT-BR" in tts._voice_names
