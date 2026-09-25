"""
Motor de Síntesi de Veu UPC FestCat — Ona i Pau (Piper Neural 100% Offline).
Models basats en les gravacions del corpus FestCat de la Universitat Politècnica de Catalunya (UPC),
entrenats amb l'arquitectura VITS / Piper i optimitzats per a ONNX (Ona: 63 MB, Pau: 28 MB).
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
    """Motor autònom de síntesi de veu catalana basat en les veus FestCat de la UPC (Ona i Pau)."""

    UPC_SPEAKERS = {
        "ona": {
            "id": 0,
            "name": "Ona (UPC FestCat)",
            "gender": "Femenina",
            "accent": "Central (FestCat UPC)",
            "desc": "Veu neural femenina d'alta fidelitat del corpus FestCat de la Universitat Politècnica de Catalunya",
            "model_file": "ca_ES-upc_ona-medium.onnx",
            "json_file": "ca_ES-upc_ona-medium.onnx.json",
            "url_subpath": "upc_ona/medium",
            "size_threshold": 60000000
        },
        "pau": {
            "id": 1,
            "name": "Pau (UPC FestCat)",
            "gender": "Masculina",
            "accent": "Central (FestCat UPC)",
            "desc": "Veu neural masculina del corpus FestCat de la Universitat Politècnica de Catalunya",
            "model_file": "ca_ES-upc_pau-x_low.onnx",
            "json_file": "ca_ES-upc_pau-x_low.onnx.json",
            "url_subpath": "upc_pau/x_low",
            "size_threshold": 25000000
        }
    }

    def __init__(self, models_dir: Optional[str] = None):
        self.name = "UPC Ona FestCat"
        self.sample_rate = 22050
        self.text_normalizer = CatalanTextNormalizer()
        self.downloader = ModelDownloader(models_dir)
        self.models_dir = self.downloader.cache_dir
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self._load_lock = threading.Lock()
        self._voices: Dict[str, Any] = {}
        self._voice: Optional[Any] = None

    def _get_speaker_info(self, voice_id: str) -> Dict[str, Any]:
        v_key = str(voice_id).lower().strip() if voice_id else "ona"
        if v_key in self.UPC_SPEAKERS:
            return self.UPC_SPEAKERS[v_key]
        # Si no coincideix exactament, cercar per coincidència parcial
        for k, info in self.UPC_SPEAKERS.items():
            if k in v_key:
                return info
        return self.UPC_SPEAKERS["ona"]

    def get_voice_paths(self, voice_id: str = "ona") -> Tuple[str, str]:
        """Localitza les rutes locals dels fitxers ONNX i JSON per a la veu especificada."""
        spk_info = self._get_speaker_info(voice_id)
        model_file = spk_info["model_file"]
        json_file = spk_info["json_file"]

        candidates = [
            os.path.join(self.models_dir, "piper_voices"),
            os.path.join(self.base_dir, "models", "piper_voices"),
        ]
        if hasattr(sys, "_MEIPASS"):
            candidates.insert(0, os.path.join(sys._MEIPASS, "models", "piper_voices"))
        if getattr(sys, "executable", None):
            candidates.append(os.path.join(os.path.dirname(sys.executable), "_internal", "models", "piper_voices"))
            candidates.append(os.path.join(os.path.dirname(sys.executable), "models", "piper_voices"))

        for cand in candidates:
            p_onnx = os.path.join(cand, model_file)
            p_json = os.path.join(cand, json_file)
            if os.path.exists(p_onnx) and os.path.exists(p_json):
                return p_onnx, p_json

        return (
            os.path.join(self.models_dir, "piper_voices", model_file),
            os.path.join(self.models_dir, "piper_voices", json_file)
        )

    def ensure_loaded(self, voice_id: str = "ona", on_status_callback: Optional[Callable[[str], None]] = None) -> bool:
        """Carrega el model neuronal de la veu sol·licitada a la memòria RAM de forma thread-safe."""
        spk_info = self._get_speaker_info(voice_id)
        v_key = "pau" if spk_info["name"].startswith("Pau") else "ona"

        with self._load_lock:
            if v_key in self._voices and self._voices[v_key] is not None:
                self._voice = self._voices[v_key]
                return True

            onnx_path, json_path = self.get_voice_paths(v_key)

            if not os.path.exists(onnx_path) or not os.path.exists(json_path):
                if on_status_callback:
                    on_status_callback(f"Descarregant veu UPC {spk_info['name']}...")
                success = self._download_voice_files(v_key, onnx_path, json_path, on_status_callback)
                if not success or not os.path.exists(onnx_path):
                    print(f"Error: no s'ha trobat el model UPC {spk_info['name']} a {onnx_path}")
                    return False

            if not HAS_PIPER:
                print("Error: el paquet piper-tts no està disponible.")
                return False

            if on_status_callback:
                on_status_callback(f"Carregant veu UPC {spk_info['name']} a la memòria...")

            try:
                espeak_data_dir = None
                if hasattr(sys, "_MEIPASS"):
                    meipass_espeak = os.path.join(sys._MEIPASS, "piper", "espeak-ng-data")
                    if os.path.exists(meipass_espeak):
                        espeak_data_dir = meipass_espeak

                if espeak_data_dir:
                    voice_inst = PiperVoice.load(
                        onnx_path,
                        config_path=json_path,
                        espeak_data_dir=espeak_data_dir
                    )
                else:
                    voice_inst = PiperVoice.load(
                        onnx_path,
                        config_path=json_path
                    )
                self._voices[v_key] = voice_inst
                self._voice = voice_inst
                return True
            except Exception as e:
                print(f"Error carregant veu UPC {spk_info['name']}: {e}")
                return False

    def _download_voice_files(self, voice_key: str, onnx_path: str, json_path: str,
                              on_status_callback: Optional[Callable[[str], None]] = None) -> bool:
        """Descarrega el model ONNX i JSON de Hugging Face si no estan presents."""
        try:
            import requests
            spk_info = self.UPC_SPEAKERS.get(voice_key, self.UPC_SPEAKERS["ona"])
            os.makedirs(os.path.dirname(onnx_path), exist_ok=True)
            base_url = f"https://huggingface.co/rhasspy/piper-voices/resolve/main/ca/ca_ES/{spk_info['url_subpath']}"

            # JSON
            if not os.path.exists(json_path):
                r = requests.get(f"{base_url}/{spk_info['json_file']}", timeout=20)
                r.raise_for_status()
                with open(json_path, "wb") as f:
                    f.write(r.content)

            # ONNX
            if not os.path.exists(onnx_path) or os.path.getsize(onnx_path) < spk_info["size_threshold"]:
                r = requests.get(f"{base_url}/{spk_info['model_file']}", stream=True, timeout=60)
                r.raise_for_status()
                with open(onnx_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)
            return True
        except Exception as e:
            print(f"Error descarregant model UPC {voice_key}: {e}")
            return False

    def unload(self, voice_id: Optional[str] = None):
        """Allibera la memòria ocupada pels models UPC."""
        with self._load_lock:
            if voice_id:
                v_key = "pau" if "pau" in str(voice_id).lower() else "ona"
                if v_key in self._voices:
                    del self._voices[v_key]
                if self._voice == self._voices.get(v_key):
                    self._voice = next(iter(self._voices.values())) if self._voices else None
            else:
                self._voices.clear()
                self._voice = None
            gc.collect()

    def is_loaded(self, voice_id: Optional[str] = None) -> bool:
        if voice_id:
            v_key = "pau" if "pau" in str(voice_id).lower() else "ona"
            return v_key in self._voices and self._voices[v_key] is not None
        return len(self._voices) > 0 or self._voice is not None

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
        Sintetitza una frase amb la veu neuronal UPC especificada (Ona o Pau).
        Retorna un array numpy float32 a 22.050 Hz.
        """
        normalized_text = self.text_normalizer.normalize(text)
        if not normalized_text:
            return np.zeros(0, dtype=np.float32)

        spk_info = self._get_speaker_info(voice_id)
        v_key = "pau" if spk_info["name"].startswith("Pau") else "ona"

        if not self.ensure_loaded(voice_id=v_key):
            print(f"Error: no s'ha pogut carregar el motor UPC per a la veu '{v_key}'.")
            return np.zeros(0, dtype=np.float32)

        voice = self._voices.get(v_key)
        if voice is None:
            return np.zeros(0, dtype=np.float32)

        try:
            # Control de velocitat mitjançant length_scale a Piper
            safe_speed = max(0.5, min(2.0, speed))
            length_scale = 1.0 / safe_speed
            syn_config = SynthesisConfig(length_scale=length_scale)

            chunks = list(voice.synthesize(normalized_text, syn_config=syn_config))
            if not chunks:
                return np.zeros(0, dtype=np.float32)

            audio_arrays = [c.audio_float_array for c in chunks if c.audio_float_array is not None]
            if not audio_arrays:
                return np.zeros(0, dtype=np.float32)

            audio = np.concatenate(audio_arrays)

            # Resample a 22.050 Hz si cal (Pau és 16.000 Hz nativament, Ona és 22.050 Hz)
            sr = voice.config.sample_rate
            if sr != self.sample_rate:
                num_samples = int(len(audio) * (self.sample_rate / sr))
                audio = scipy.signal.resample(audio, num_samples)

            # Desplaçament de to si pitch != 0.0 (opcional)
            if abs(pitch) > 0.1:
                pitch_factor = 2.0 ** (pitch / 12.0)
                target_len = int(len(audio) / pitch_factor)
                resampled = scipy.signal.resample(audio, target_len)
                audio = scipy.signal.resample(resampled, len(audio))

            # Suavitzat d'extrems per evitar espetecs
            fade_len = int(0.012 * self.sample_rate)
            if len(audio) > 2 * fade_len:
                audio[:fade_len] *= np.linspace(0.0, 1.0, fade_len)
                audio[-fade_len:] *= np.linspace(1.0, 0.0, fade_len)

            return audio.astype(np.float32)

        except Exception as e:
            print(f"Error en la síntesi UPC ({v_key}): {e}")
            return np.zeros(0, dtype=np.float32)

    def synthesize_podcast_stream(self, segments: List[Any],
                                  on_progress: Optional[Callable[[int, int, str], None]] = None,
                                  is_cancelled: Optional[Callable[[], bool]] = None) -> List[Tuple[np.ndarray, float, int]]:
        """
        Sintetitza la llista de segments d'un guió de pòdcast amb les veus de la UPC (Ona o Pau).
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


# Àlies per a màxima compatibilitat
UPCFestCatCatalanEngine = UPCOnaCatalanEngine
