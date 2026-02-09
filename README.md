# Gravador de Áudio com Speech AI

App gráfico para Windows que integra com a API Speaches para:
- Gravação de áudio (WAV/MP3)
- Conversão de fala para texto (STT)
- Conversão de texto para fala (TTS)
- **Download automático de modelos** quando necessário

## Pré-requisitos

1. **Speaches API** rodando em `http://localhost:8000`
   - Certifique-se que a API está ativa antes de usar as funcionalidades de STT/TTS
   - O app baixa automaticamente os modelos na primeira execução se não estiverem instalados
   
2. **Python 3.12+** com ambiente virtual configurado

3. **FFmpeg** (opcional, apenas para MP3)
   - Windows: `choco install ffmpeg` ou baixe em https://www.gyan.dev/ffmpeg/builds/

## Instalação

```bash
# Instalar dependências
pip install -r requirements.txt

# Para desenvolvimento/testes
pip install -r requirements-dev.txt
```

## Como Usar

### Executar o app

```bash
# Do diretório root
python -m src.main

# Ou do diretório src
cd src
python main.py
```

### Funcionalidades

#### Aba 1: Gravação
- Escolha formato (WAV ou MP3)
- Clique "Iniciar" → Contagem 3..2..1 → Gravação inicia no "2"
- Clique "Parar" para finalizar
- Arquivos salvos em `recordings/` com nome `YYYYMMDD_HHMMSS.{wav|mp3}`

#### Aba 2: Fala → Texto
- **Exibe modelo STT ativo** no topo da aba
- Selecione arquivo WAV ou use última gravação
- Clique "Transcrever" para converter áudio em texto
- Idiomas suportados: baseados no modelo instalado
- Requer API Speaches ativa
- **Download automático**: Se nenhum modelo STT estiver instalado, baixa `Systran/faster-whisper-large-v3`

#### Aba 3: Texto → Fala
- **Exibe modelo TTS ativo** no topo da aba
- Selecione voz disponível no dropdown (formato: `nome-IDIOMA`)
- Vozes em português priorizadas como padrão
- Digite texto
- "Falar Agora" → Reproduz imediatamente
- "Salvar em Arquivo" → Salva MP3 em `recordings/`
- Requer API Speaches ativa
- **Download automático**: Se nenhum modelo TTS estiver instalado, baixa `speaches-ai/Kokoro-82M-v1.0-ONNX-int8`

### Modelos Padrão

Quando nenhum modelo está instalado, o app automaticamente baixa:
- **STT**: `Systran/faster-whisper-large-v3` - Suporta português, inglês, espanhol, francês, alemão, russo, chinês e mais
- **TTS**: `speaches-ai/Kokoro-82M-v1.0-ONNX-int8` - Múltiplas vozes incluindo português brasileiro

## Testes

```bash
pytest
```

**Cobertura atual**: 16 testes incluindo:
- Utilitários de áudio (WAV/MP3)
- Captura de áudio com sounddevice
- Integração com API Speaches (STT/TTS)
- Download automático de modelos
- Formatação de vozes
- Mapeamento de IDs de vozes

## Estrutura do Projeto

```
.
├── recordings/          # Áudios gravados
├── src/
│   ├── app.py          # Interface wxPython
│   ├── main.py         # Entrypoint
│   ├── recorder.py     # Captura de áudio
│   ├── audio_utils.py  # Utilidades (salvar WAV/MP3)
│   ├── speech_to_text.py   # Cliente STT (Speaches API + download)
│   └── text_to_speech.py   # Cliente TTS (Speaches API + download)
├── tests/
│   ├── test_audio_utils.py      # Testes de I/O de áudio
│   ├── test_recorder.py         # Testes de captura
│   ├── test_speech_registry.py  # Testes STT + download
│   └── test_tts_registry.py     # Testes TTS + download
├── requirements.txt
└── requirements-dev.txt
```

## Dependências Principais

- **wxPython**: Interface gráfica
- **sounddevice**: Captura de áudio do microfone
- **soundfile**: Leitura/escrita de arquivos WAV
- **pydub**: Conversão para MP3
- **requests**: Comunicação com API Speaches

## Configuração da API

Por padrão, a API é acessada em `http://localhost:8000`. Para alterar:

```python
# Em src/app.py, ao instanciar os serviços:
self._stt = SpeechToText(api_base_url="http://seu-servidor:porta")
self._tts = TextToSpeech(api_base_url="http://seu-servidor:porta")
```

### Endpoints Utilizados

- **GET** `/v1/models?task=automatic-speech-recognition` - Lista modelos STT instalados
- **GET** `/v1/models?task=text-to-speech` - Lista modelos TTS instalados
- **POST** `/v1/models/{model_id}` - Download de modelo específico
- **POST** `/v1/audio/transcriptions` - Transcrição de áudio
- **POST** `/v1/audio/speech` - Síntese de fala

## Resolução de Problemas

### "Erro na API de transcrição/síntese"
- Verifique se Speaches API está rodando: `curl http://localhost:8000/health`
- Na primeira execução, o app tentará baixar modelos automaticamente (pode demorar alguns minutos)
- Monitore o download na API ou logs do Speaches

### Modelos não são baixados automaticamente
- Verifique conectividade com a API: `curl http://localhost:8000/v1/models`
- Certifique-se que a API Speaches tem acesso à internet para baixar modelos
- Baixe manualmente via interface da API em `http://localhost:8000/docs`

### "Erro no microfone"
- Verifique permissões de acesso ao microfone no Windows
- Teste com: `python -c "import sounddevice; print(sounddevice.query_devices())"`

### MP3 não funciona
- Instale FFmpeg e adicione ao PATH do sistema
- Reinicie o terminal/aplicativo após instalação

### Vozes não aparecem no TTS
- O app baixará automaticamente o modelo TTS na primeira execução
- Aguarde o download ser concluído (pode levar alguns minutos)
- Fallback: usa vozes padrão se download falhar (alloy, echo, fable, onyx, nova, dora, alex)
