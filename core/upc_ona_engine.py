"""
Motor de Síntesi de Veu UPC Ona FestCat (Piper Neural 100% Offline).
Model basat en les gravacions del corpus FestCat de la Universitat Politècnica de Catalunya (UPC),
entrenat amb l'arquitectura VITS / Piper i optimitzat per a ONNX (63 MB).
100% autònom, local, privat i d'alta fidelitat acústica a 22.050 Hz.
"""

import os
import sys
import gc
import re
import threading
import numpy as np
import scipy.signal
import soundfile as sf
from typing import Dict, List, Optional, Callable, Tuple, Any

try:
    from piper import PiperVoice, SynthesisConfig
    HAS_PIPER = True
except ImportError:
    HAS_PIPER = False

from core.text_normalizer import CatalanTextNormalizer
from core.model_downloader import ModelDownloader


class UPCOnaCatalanEngine:
    """Motor autònom de síntesi de veu catalana basat en la veu Ona FestCat de la UPC."""

    UPC_SPEAKERS = {
        "ona": {
            "id": 0,
            "name": "Ona (UPC FestCat)",
            "gender": "Femenina",
            "accent": "Central (FestCat UPC)",
            "desc": "Veu neural d'alta fidelitat del corpus FestCat de la Universitat Politècnica de Catalunya"
        }
    }

    def __init__(self, models_dir: Optional[str] = None):
        self.name = "UPC Ona FestCat"
        self.sample_rate = 22050
        self.text_normalizer = CatalanTextNormalizer()
        self.downloader = ModelDownloader(models_dir)
        self.models_dir = self.downloader.cache_dir

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        candidates = [
            os.path.join(self.models_dir, "piper_voices"),
            os.path.join(base_dir, "models", "piper_voices"),
        ]
        if hasattr(sys, "_MEIPASS"):
            candidates.insert(0, os.path.join(sys._MEIPASS, "models", "piper_voices"))
        if getattr(sys, "executable", None):
            candidates.append(os.path.join(os.path.dirname(sys.executable), "_internal", "models", "piper_voices"))
            candidates.append(os.path.join(os.path.dirname(sys.executable), "models", "piper_voices"))

        self.model_onnx_path = ""
        self.model_json_path = ""
        for cand in candidates:
            p_onnx = os.path.join(cand, "ca_ES-upc_ona-medium.onnx")
            p_json = os.path.join(cand, "ca_ES-upc_ona-medium.onnx.json")
            if os.path.exists(p_onnx) and os.path.exists(p_json):
                self.model_onnx_path = p_onnx
                self.model_json_path = p_json
                break

        if not self.model_onnx_path:
            self.model_onnx_path = os.path.join(self.models_dir, "piper_voices", "ca_ES-upc_ona-medium.onnx")
            self.model_json_path = os.path.join(self.models_dir, "piper_voices", "ca_ES-upc_ona-medium.onnx.json")

        self._load_lock = threading.Lock()
        self._voice: Optional[Any] = None

    def ensure_loaded(self, on_status_callback: Optional[Callable[[str], None]] = None) -> bool:
        """Carrega el model neuronal de la UPC a la memòria RAM de forma thread-safe."""
        with self._load_lock:
            if self._voice is not None:
                return True

            if not os.path.exists(self.model_onnx_path) or not os.path.exists(self.model_json_path):
                # Intent de descàrrega automàtica si no existeix
                if on_status_callback:
                    on_status_callback("Descarregant veu UPC Ona FestCat (63 MB)...")
                success = self._download_model_files(on_status_callback)
                if not success or not os.path.exists(self.model_onnx_path):
                    print(f"Error: no s'ha trobat el model UPC Ona a {self.model_onnx_path}")
                    return False

            if not HAS_PIPER:
                print("Error: el paquet piper-tts no està disponible.")
                return False

            if on_status_callback:
                on_status_callback("Carregant veu UPC Ona FestCat a la memòria...")

            try:
                # Comprovació de la ruta interna d'espeak-ng-data per a aplicacions compilades
                espeak_data_dir = None
                if hasattr(sys, "_MEIPASS"):
                    meipass_espeak = os.path.join(sys._MEIPASS, "piper", "espeak-ng-data")
                    if os.path.exists(meipass_espeak):
                        espeak_data_dir = meipass_espeak

                if espeak_data_dir:
                    self._voice = PiperVoice.load(
                        self.model_onnx_path,
                        config_path=self.model_json_path,
                        espeak_data_dir=espeak_data_dir
                    )
                else:
                    self._voice = PiperVoice.load(
                        self.model_onnx_path,
                        config_path=self.model_json_path
                    )
                return True
            except Exception as e:
                print(f"Error carregant veu UPC Ona: {e}")
                return False

    def _download_model_files(self, on_status_callback: Optional[Callable[[str], None]] = None) -> bool:
        """Descarrega el model ONNX i JSON de Hugging Face si no estan presents."""
        try:
            import requests
            os.makedirs(os.path.dirname(self.model_onnx_path), exist_ok=True)
            base_url = "https://huggingface.co/rhasspy/piper-voices/resolve/main/ca/ca_ES/upc_ona/medium"
            
            # JSON
            if not os.path.exists(self.model_json_path):
                r = requests.get(f"{base_url}/ca_ES-upc_ona-medium.onnx.json", timeout=20)
                r.raise_for_status()
                with open(self.model_json_path, "wb") as f:
                    f.write(r.content)

            # ONNX
            if not os.path.exists(self.model_onnx_path) or os.path.getsize(self.model_onnx_path) < 60000000:
                r = requests.get(f"{base_url}/ca_ES-upc_ona-medium.onnx", stream=True, timeout=60)
                r.raise_for_status()
                with open(self.model_onnx_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)
            return True
        except Exception as e:
            print(f"Error descarregant model UPC Ona: {e}")
            return False

    def unload(self):
        """Allibera la memòria ocupada pel model UPC Ona."""
        with self._load_lock:
            if self._voice is not None:
                self._voice = None
                gc.collect()

    def is_loaded(self) -> bool:
        return self._voice is not None

    def split_sentences(self, text: str) -> List[str]:
        """Divideix el text en frases respectant els punts i signes catalans."""
        text = re.sub(r"\b(Dr|Dra|Prof|Profa|Sr|Sra|pàg|núm)\.", r"\1__PUNT__", text)
        sentences = re.split(r"([.!?;\n]+)", text)

        result = []
        current = ""
        for part in sentences:
            if not part:
                continue
            if re.match(r"^[.!?;\n]+$", part):
                current += part
                current_clean = current.replace("__PUNT__", ".").strip()
                if current_clean:
                    result.append(current_clean)
                current = ""
            else:
                current += part

        if current:
            current_clean = current.replace("__PUNT__", ".").strip()
            if current_clean:
                result.append(current_clean)

        return result if result else [text]

    def synthesize_utterance(self, text: str, voice_id: str = "ona",
                             speed: float = 1.0, pitch: float = 0.0,
                             clone_audio_path: Optional[str] = None) -> np.ndarray:
        """
        Sintetitza una frase amb la veu neuronal Ona FestCat de la UPC.
        Retorna un array numpy float32 a 22.050 Hz.
        """
        normalized_text = self.text_normalizer.normalize(text)
        if not normalized_text:
            return np.zeros(0, dtype=np.float32)

        if not self.ensure_loaded():
            print("Error: no s'ha pogut carregar el motor UPC Ona.")
            return np.zeros(0, dtype=np.float32)

        try:
            # Control de velocitat mitjançant length_scale a Piper
            # speed > 1.0 -> length_scale < 1.0 (més ràpid)
            safe_speed = max(0.5, min(2.0, speed))
            length_scale = 1.0 / safe_speed
            syn_config = SynthesisConfig(length_scale=length_scale)

            chunks = list(self._voice.synthesize(normalized_text, syn_config=syn_config))
            if not chunks:
                return np.zeros(0, dtype=np.float32)

            audio_arrays = [c.audio_float_array for c in chunks if c.audio_float_array is not None]
            if not audio_arrays:
                return np.zeros(0, dtype=np.float32)

            audio = np.concatenate(audio_arrays)

            # Resample a 22.050 Hz si cal
            sr = self._voice.config.sample_rate
            if sr != self.sample_rate:
                num_samples = int(len(audio) * (self.sample_rate / sr))
                audio = scipy.signal.resample(audio, num_samples)

            # Desplaçament de to si pitch != 0.0 (opcional)
            if abs(pitch) > 0.1:
                # Modulació subtil de to via mostreig
                pitch_factor = 2.0 ** (pitch / 12.0)
                target_len = int(len(audio) / pitch_factor)
                resampled = scipy.signal.resample(audio, target_len)
                # Reajustar longitud original per mantenir tempo
                audio = scipy.signal.resample(resampled, len(audio))

            # Suavitzat d'extrems per evitar espetecs
            fade_len = int(0.012 * self.sample_rate)
            if len(audio) > 2 * fade_len:
                audio[:fade_len] *= np.linspace(0.0, 1.0, fade_len)
                audio[-fade_len:] *= np.linspace(1.0, 0.0, fade_len)

            return audio.astype(np.float32)

        except Exception as e:
            print(f"Error en la síntesi UPC Ona: {e}")
            return np.zeros(0, dtype=np.float32)

    def synthesize_podcast_stream(self, segments: List[Any],
                                  on_progress: Optional[Callable[[int, int, str], None]] = None,
                                  is_cancelled: Optional[Callable[[], bool]] = None) -> List[Tuple[np.ndarray, float, int]]:
        """
        Sintetitza la llista de segments d'un guió de pòdcast amb la veu UPC Ona.
        """
        output_audio_list = []
        total_segments = len(segments)

        for idx, seg in enumerate(segments, start=1):
            if is_cancelled and is_cancelled():
                break

            if seg.segment_type == "pause":
                if on_progress:
                    on_progress(idx, total_segments, f"Pausa ({seg.pause_ms} ms)")
                output_audio_list.append((None, 0.0, seg.pause_ms))
                continue

            elif seg.segment_type == "dialogue":
                text = seg.text.strip()
                if not text:
                    continue

                if on_progress:
                    preview = text[:45] + ("..." if len(text) > 45 else "")
                    on_progress(idx, total_segments, f"{seg.speaker}: \"{preview}\"")

                sentences = self.split_sentences(text)
                for s_idx, sentence in enumerate(sentences):
                    if is_cancelled and is_cancelled():
                        break

                    sentence_audio = self.synthesize_utterance(
                        text=sentence,
                        voice_id=seg.voice_id,
                        speed=seg.speed,
                        pitch=seg.pitch,
                        clone_audio_path=seg.clone_audio_path
                    )

                    is_last_sentence = (s_idx == len(sentences) - 1)
                    pause_ms = seg.pause_ms if is_last_sentence else 220

                    output_audio_list.append((sentence_audio, seg.pan, pause_ms))

        return output_audio_list
