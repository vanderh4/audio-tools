from __future__ import annotations

import threading
from pathlib import Path

import wx

try:
    from .audio_utils import AudioSettings, build_recording_path, write_audio
    from .recorder import AudioRecorder
    from .speech_to_text import SpeechToText
    from .text_to_speech import TextToSpeech
except ImportError:  # pragma: no cover
    from audio_utils import AudioSettings, build_recording_path, write_audio
    from recorder import AudioRecorder
    from speech_to_text import SpeechToText
    from text_to_speech import TextToSpeech


class RecorderPanel(wx.Panel):
    def __init__(self, parent: wx.Window) -> None:
        super().__init__(parent)

        self._settings = AudioSettings()
        self._recorder = AudioRecorder(self._settings)
        self._recordings_dir = Path.cwd() / "recordings"
        self._last_recording: Path | None = None

        self._status = wx.StaticText(self, label="Pronto para gravar.")
        self._countdown = wx.StaticText(self, label="")

        # Format selector
        format_box = wx.StaticBox(self, label="Formato")
        format_sizer = wx.StaticBoxSizer(format_box, wx.HORIZONTAL)
        self._format_wav = wx.RadioButton(self, label="WAV", style=wx.RB_GROUP)
        self._format_mp3 = wx.RadioButton(self, label="MP3")
        self._format_wav.SetValue(True)
        format_sizer.Add(self._format_wav, 0, wx.ALL, 5)
        format_sizer.Add(self._format_mp3, 0, wx.ALL, 5)

        self._start_btn = wx.Button(self, label="Iniciar")
        self._stop_btn = wx.Button(self, label="Parar")
        self._stop_btn.Disable()

        self._start_btn.Bind(wx.EVT_BUTTON, self.on_start)
        self._stop_btn.Bind(wx.EVT_BUTTON, self.on_stop)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._status, 0, wx.ALL | wx.CENTER, 10)
        sizer.Add(self._countdown, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(format_sizer, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self._start_btn, 0, wx.ALL | wx.CENTER, 10)
        sizer.Add(self._stop_btn, 0, wx.ALL | wx.CENTER, 5)
        self.SetSizer(sizer)

    def get_last_recording(self) -> Path | None:
        return self._last_recording

    def on_start(self, event: wx.CommandEvent) -> None:  # noqa: ARG002
        self._start_btn.Disable()
        self._stop_btn.Disable()
        self._format_wav.Disable()
        self._format_mp3.Disable()
        self._status.SetLabel("Aguardando microfone...")
        self._countdown.SetLabel("3")

        threading.Thread(target=self._run_countdown, daemon=True).start()

    def on_stop(self, event: wx.CommandEvent) -> None:  # noqa: ARG002
        frames = self._recorder.stop()
        if not frames:
            self._status.SetLabel("Nenhum audio capturado.")
            self._countdown.SetLabel("")
            self._start_btn.Enable()
            self._stop_btn.Disable()
            self._format_wav.Enable()
            self._format_mp3.Enable()
            return

        # Get selected format
        audio_format = "mp3" if self._format_mp3.GetValue() else "wav"
        file_path = build_recording_path(self._recordings_dir, extension=audio_format)
        
        try:
            write_audio(file_path, frames, self._settings, format=audio_format)
            self._last_recording = file_path
            self._status.SetLabel(f"Gravado em: {file_path.name}")
        except Exception as exc:  # noqa: BLE001
            self._status.SetLabel(f"Erro ao salvar: {exc}")
        finally:
            self._countdown.SetLabel("")
            self._start_btn.Enable()
            self._stop_btn.Disable()
            self._format_wav.Enable()
            self._format_mp3.Enable()

    def _run_countdown(self) -> None:
        for value in (3, 2, 1):
            wx.CallAfter(self._countdown.SetLabel, str(value))
            if value == 3:
                wx.CallAfter(self._status.SetLabel, "Começando em breve...")
            elif value == 2:
                wx.CallAfter(self._start_recording)
            
            wx.MilliSleep(1000)
        
        wx.CallAfter(self._countdown.SetLabel, "")

        self._status.SetLabel("Gravando...")
        self._countdown.SetLabel("")
        self._stop_btn.Enable()

    def _start_recording(self) -> None:
        try:
            self._recorder.start()
        except Exception as exc:  # noqa: BLE001
            self._status.SetLabel(f"Erro no microfone: {exc}")
            self._start_btn.Enable()
            return

class SpeechToTextPanel(wx.Panel):
    def __init__(self, parent: wx.Window, recorder_panel: RecorderPanel) -> None:
        super().__init__(parent)
        self._recorder_panel = recorder_panel
        self._stt = SpeechToText()

        self._status = wx.StaticText(self, label="Selecione um arquivo ou use a última gravação.")
        
        # Model info
        model_name = self._stt._model if hasattr(self._stt, "_model") else "Desconhecido"
        self._model_label = wx.StaticText(self, label=f"Modelo: {model_name}")
        font = self._model_label.GetFont()
        font.PointSize -= 1
        self._model_label.SetFont(font)
        self._model_label.SetForegroundColour(wx.Colour(100, 100, 100))
        
        self._file_picker = wx.FilePickerCtrl(
            self,
            message="Escolha um arquivo de áudio",
            wildcard="Arquivos de áudio (*.wav)|*.wav",
            style=wx.FLP_OPEN | wx.FLP_FILE_MUST_EXIST,
        )
        
        self._transcribe_file_btn = wx.Button(self, label="Transcrever Arquivo")
        self._transcribe_last_btn = wx.Button(self, label="Transcrever Última Gravação")
        
        self._result_label = wx.StaticText(self, label="Transcrição:")
        self._result_text = wx.TextCtrl(
            self,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_WORDWRAP,
            size=(400, 150),
        )
        
        self._transcribe_file_btn.Bind(wx.EVT_BUTTON, self.on_transcribe_file)
        self._transcribe_last_btn.Bind(wx.EVT_BUTTON, self.on_transcribe_last)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._status, 0, wx.ALL | wx.CENTER, 10)
        sizer.Add(self._model_label, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self._file_picker, 0, wx.ALL | wx.EXPAND, 10)
        sizer.Add(self._transcribe_file_btn, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self._transcribe_last_btn, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self._result_label, 0, wx.ALL | wx.LEFT, 10)
        sizer.Add(self._result_text, 1, wx.ALL | wx.EXPAND, 10)
        self.SetSizer(sizer)

    def on_transcribe_file(self, event: wx.CommandEvent) -> None:  # noqa: ARG002
        file_path = self._file_picker.GetPath()
        if not file_path:
            self._status.SetLabel("Selecione um arquivo primeiro.")
            return
        
        self._transcribe(Path(file_path))

    def on_transcribe_last(self, event: wx.CommandEvent) -> None:  # noqa: ARG002
        last_recording = self._recorder_panel.get_last_recording()
        if not last_recording or not last_recording.exists():
            self._status.SetLabel("Nenhuma gravação encontrada.")
            return
        
        self._transcribe(last_recording)

    def _transcribe(self, audio_file: Path) -> None:
        self._status.SetLabel("Transcrevendo...")
        self._result_text.SetValue("")
        
        def do_transcribe():
            try:
                text = self._stt.transcribe_file(audio_file)
                wx.CallAfter(self._result_text.SetValue, text)
                wx.CallAfter(self._status.SetLabel, "Transcrição concluída.")
            except Exception as exc:  # noqa: BLE001
                wx.CallAfter(self._status.SetLabel, f"Erro: {exc}")
        
        threading.Thread(target=do_transcribe, daemon=True).start()


class TextToSpeechPanel(wx.Panel):
    def __init__(self, parent: wx.Window) -> None:
        super().__init__(parent)
        self._tts = TextToSpeech()
        self._recordings_dir = Path.cwd() / "recordings"

        self._status = wx.StaticText(self, label="Digite o texto para converter em fala.")
        
        # Model info
        model_name = self._tts._model if hasattr(self._tts, "_model") else "Desconhecido"
        self._model_label = wx.StaticText(self, label=f"Modelo: {model_name}")
        font = self._model_label.GetFont()
        font.PointSize -= 1
        self._model_label.SetFont(font)
        self._model_label.SetForegroundColour(wx.Colour(100, 100, 100))
        
        # Voice selector
        voice_box = wx.StaticBox(self, label="Voz")
        voice_sizer = wx.StaticBoxSizer(voice_box, wx.HORIZONTAL)
        
        voices = self._tts.get_voices()
        self._voice_choice = wx.Choice(self, choices=voices)
        if voices:
            self._voice_choice.SetSelection(0)
        
        voice_sizer.Add(self._voice_choice, 1, wx.ALL | wx.EXPAND, 5)
        self._voice_choice.Bind(wx.EVT_CHOICE, self.on_voice_changed)
        
        self._input_label = wx.StaticText(self, label="Texto:")
        self._input_text = wx.TextCtrl(
            self,
            style=wx.TE_MULTILINE | wx.TE_WORDWRAP,
            size=(400, 120),
        )
        
        self._speak_btn = wx.Button(self, label="Falar Agora")
        self._save_btn = wx.Button(self, label="Salvar em Arquivo")
        
        self._speak_btn.Bind(wx.EVT_BUTTON, self.on_speak)
        self._save_btn.Bind(wx.EVT_BUTTON, self.on_save)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._status, 0, wx.ALL | wx.CENTER, 10)
        sizer.Add(self._model_label, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(voice_sizer, 0, wx.ALL | wx.EXPAND, 10)
        sizer.Add(self._input_label, 0, wx.ALL | wx.LEFT, 10)
        sizer.Add(self._input_text, 1, wx.ALL | wx.EXPAND, 10)
        
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(self._speak_btn, 0, wx.ALL, 5)
        btn_sizer.Add(self._save_btn, 0, wx.ALL, 5)
        
        sizer.Add(btn_sizer, 0, wx.ALL | wx.CENTER, 10)
        self.SetSizer(sizer)

    def on_voice_changed(self, event: wx.CommandEvent) -> None:  # noqa: ARG002
        selected = self._voice_choice.GetSelection()
        if selected != wx.NOT_FOUND:
            self._tts.set_voice(selected)
            self._status.SetLabel(f"Voz alterada: {self._voice_choice.GetStringSelection()}")

    def on_speak(self, event: wx.CommandEvent) -> None:  # noqa: ARG002
        text = self._input_text.GetValue().strip()
        if not text:
            self._status.SetLabel("Digite algum texto primeiro.")
            return
        
        self._status.SetLabel("Falando...")
        
        def do_speak():
            try:
                self._tts.speak(text)
                wx.CallAfter(self._status.SetLabel, "Finalizado.")
            except Exception as exc:  # noqa: BLE001
                wx.CallAfter(self._status.SetLabel, f"Erro: {exc}")
        
        threading.Thread(target=do_speak, daemon=True).start()

    def on_save(self, event: wx.CommandEvent) -> None:  # noqa: ARG002
        text = self._input_text.GetValue().strip()
        if not text:
            self._status.SetLabel("Digite algum texto primeiro.")
            return
        
        file_path = build_recording_path(self._recordings_dir, extension="mp3")
        self._status.SetLabel("Salvando...")
        
        def do_save():
            try:
                self._tts.save_to_file(text, file_path)
                wx.CallAfter(self._status.SetLabel, f"Salvo: {file_path.name}")
            except Exception as exc:  # noqa: BLE001
                wx.CallAfter(self._status.SetLabel, f"Erro: {exc}")
        
        threading.Thread(target=do_save, daemon=True).start()


class RecorderFrame(wx.Frame):
    def __init__(self) -> None:
        super().__init__(parent=None, title="Gravador de Áudio", size=(500, 400))
        
        notebook = wx.Notebook(self)
        
        recorder_panel = RecorderPanel(notebook)
        stt_panel = SpeechToTextPanel(notebook, recorder_panel)
        tts_panel = TextToSpeechPanel(notebook)
        
        notebook.AddPage(recorder_panel, "Gravação")
        notebook.AddPage(stt_panel, "Fala → Texto")
        notebook.AddPage(tts_panel, "Texto → Fala")
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.EXPAND)
        self.SetSizer(sizer)


class RecorderApp(wx.App):
    def OnInit(self) -> bool:
        frame = RecorderFrame()
        frame.Show()
        return True
