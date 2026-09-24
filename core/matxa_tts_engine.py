"""
Motor de Síntesi de Veu Matxa-TTS v2 Català Multiaccent amb Grafemes.
Model de BSC-LT: BSC-LT/matxa-tts-v2-ca-multiaccent-graphemes
Integrat amb vocoder WaveNeXt end-to-end i suport de càrrega sota demanda (Lazy Loading).
"""

import os
import sys
import gc
import re
import time
import threading
import numpy as np
import scipy.signal
import soundfile as sf
from typing import Dict, List, Optional, Callable, Tuple, Any

try:
    import onnxruntime as ort
    HAS_ONNX = True
except ImportError:
    HAS_ONNX = False

from core.text_normalizer import CatalanTextNormalizer

# Taula oficial de símbols i grafemes del BSC-LT per a Matxa-TTS v2
_pad = "_"
_punctuation = ';:,.!?¡¿—…"«»“”()- '
_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
_letters_ipa = (
    "ɑɐɒæɓʙβɔɕçɗɖðʤəɘɚɛɜɝɞɟʄɡɠɢʛɦɧħɥʜɨɪʝɭɬɫɮʟɱɯɰŋɳɲɴøɵɸθœɶʘɹɺɾɻʀʁɽʂʃʈʧʉʊʋⱱʌɣɤʍχʎʏʑʐʒʔʡʕʢǀǁǂǃˈˌːˑʼʴʰʱʲʷˠˤ˞↓↑→↗↘'̩'ᵻ"
)
_letters_accented = "àáèéìíòóùú·üïöñ’#´"

SYMBOLS_GRAPHEMES = [_pad] + list(_punctuation) + list(_letters) + list(_letters_ipa) + list(_letters_accented)
SYMBOL_TO_ID = {s: i for i, s in enumerate(SYMBOLS_GRAPHEMES)}
ID_TO_SYMBOL = {i: s for i, s in enumerate(SYMBOLS_GRAPHEMES)}

class MatxaTTSCatalanEngine:
    """Motor de síntesi de veu autònom basat en Matxa-TTS v2 (BSC-LT)."""

    # Mapeig oficial de locutors (corregit segons biaix de gènere del model ONNX)
    MATXA_SPEAKERS = {
        # Central (LaFresCat & EnVeuAlta)
        "elia": {"id": 3, "name": "Elia", "gender": "Femenina", "accent": "Central (Càlida i didàctica)"},
        "grau": {"id": 2, "name": "Grau", "gender": "Masculina", "accent": "Central (Procliu i dinàmic)"},
        "ona": {"id": 11, "name": "Ona (CF)", "gender": "Femenina", "accent": "Central (Institucional)"},
        "pau": {"id": 12, "name": "Pau (CM)", "gender": "Masculina", "accent": "Central (Narratiu)"},
        # Balear (LaFresCat & EnVeuAlta)
        "olga": {"id": 1, "name": "Olga", "gender": "Femenina", "accent": "Balear (Mallorquí)"},
        "quim": {"id": 0, "name": "Quim", "gender": "Masculina", "accent": "Balear (Menorquí)"},
        "bm": {"id": 10, "name": "Bernat (BM)", "gender": "Masculina", "accent": "Balear (Mallorquí)"},
        # Valencià (LaFresCat & ReFresCat)
        "gina": {"id": 7, "name": "Gina", "gender": "Femenina", "accent": "Valencià (Càlida)"},
        "lluc": {"id": 6, "name": "Lluc", "gender": "Masculina", "accent": "Valencià (Proper)"},
        "arnau": {"id": 8, "name": "Arnau", "gender": "Masculina", "accent": "Valencià (Dinàmic)"},
        "berta": {"id": 9, "name": "Berta", "gender": "Femenina", "accent": "Valencià (Expressiva)"},
        # Nord-occidental (LaFresCat & ReFresCat)
        "emma": {"id": 5, "name": "Emma", "gender": "Femenina", "accent": "Nord-occidental (Lleida)"},
        "pere": {"id": 4, "name": "Pere", "gender": "Masculina", "accent": "Nord-occidental (Lleida)"},
        "estel": {"id": 13, "name": "Estel", "gender": "Femenina", "accent": "Nord-occidental (Alt Pirineu)"},
        # Septentrional / Rossellonès (ReFresCat)
        "laura": {"id": 14, "name": "Laura", "gender": "Femenina", "accent": "Septentrional (Rosselló)"},
        "jordi": {"id": 15, "name": "Jordi", "gender": "Masculina", "accent": "Septentrional (Perpinyà)"}
    }

    def __init__(self, models_dir: Optional[str] = None):
        self.name = "Matxa-TTS v2"
        self.sample_rate = 22050
        self.text_normalizer = CatalanTextNormalizer()

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if not models_dir:
            candidates = [
                os.path.join(base_dir, "models"),
            ]
            if hasattr(sys, "_MEIPASS"):
                candidates.insert(0, os.path.join(sys._MEIPASS, "models"))
            if getattr(sys, "executable", None):
                candidates.append(os.path.join(os.path.dirname(sys.executable), "_internal", "models"))
                candidates.append(os.path.join(os.path.dirname(sys.executable), "models"))

            chosen_dir = os.path.join(base_dir, "models")
            for cand in candidates:
                test_path = os.path.join(cand, "matxa_tts", "matxa_v2_multiaccent_graphemes_20_steps_wavenext.onnx")
                if os.path.exists(test_path):
                    chosen_dir = cand
                    break
            self.models_dir = os.path.abspath(chosen_dir)
        else:
            self.models_dir = os.path.abspath(models_dir)

        self.matxa_onnx_path = os.path.join(self.models_dir, "matxa_tts", "matxa_v2_multiaccent_graphemes_20_steps_wavenext.onnx")

        # Càrrega thread-safe i persistent a la memòria RAM
        self._load_lock = threading.Lock()
        self.matxa_session: Optional[Any] = None
        self.cloned_profiles: Dict[str, Dict[str, Any]] = {}

    def ensure_loaded(self, on_status_callback: Optional[Callable[[str], None]] = None) -> bool:
        """Carrega el model Matxa-TTS a la memòria RAM de forma thread-safe."""
        with self._load_lock:
            if self.matxa_session is not None:
                return True

            if not os.path.exists(self.matxa_onnx_path):
                print(f"Error: no s'ha trobat el model ONNX a {self.matxa_onnx_path}")
                return False

            if not HAS_ONNX:
                print("Error: onnxruntime no està disponible.")
                return False

            if on_status_callback:
                on_status_callback("Carregant model Matxa-TTS v2 a la memòria...")

            try:
                sess_opts = ort.SessionOptions()
                sess_opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
                # Reserva nuclis per a la interfície d'usuari i el sistema perquè Tkinter sigui 100% fluid
                cpu_threads = max(1, min(4, (os.cpu_count() or 4) - 2))
                sess_opts.intra_op_num_threads = cpu_threads
                sess_opts.inter_op_num_threads = 2
                sess_opts.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL

                providers = ["CUDAExecutionProvider", "CPUExecutionProvider"]
                avail = ort.get_available_providers()
                selected = [p for p in providers if p in avail]

                self.matxa_session = ort.InferenceSession(self.matxa_onnx_path, sess_options=sess_opts, providers=selected)
                return True
            except Exception as e:
                print(f"Error carregant sessió ONNX de Matxa: {e}")
                try:
                    self.matxa_session = ort.InferenceSession(self.matxa_onnx_path, providers=["CPUExecutionProvider"])
                    return True
                except Exception as e2:
                    print(f"Error crític carregant Matxa ONNX: {e2}")
                    return False

    def unload(self):
        """Allibera completament la memòria RAM del model Matxa-TTS."""
        if self.matxa_session is not None:
            self.matxa_session = None
            gc.collect()

    def is_loaded(self) -> bool:
        return self.matxa_session is not None

    def clone_voice_from_audio(self, reference_audio_path: str, speaker_name: str) -> bool:
        """Guarda la mostra de referència per a aquest locutor."""
        self.cloned_profiles[speaker_name.lower()] = {
            "path": reference_audio_path,
            "created_at": time.time()
        }
        return True

    @staticmethod
    def trim_silence_and_fade(wav: np.ndarray, sample_rate: int = 22050,
                              threshold: float = 0.008,
                              lead_in_sec: float = 0.08,
                              lead_out_sec: float = 0.12) -> np.ndarray:
        """
        Retalla els silencis morts d'inici i final produïts pel vocoder WaveNeXt
        i elimina el pols/clic d'inicialització aplicant un micro-fundit d'entrada i sortida.
        """
        if len(wav) == 0:
            return wav

        # Ignorar els primers 50ms on sol haver-hi un pols/clic d'inicialització del graf
        offset = int(0.05 * sample_rate)
        if len(wav) <= offset:
            return wav

        indices_start = np.where(np.abs(wav[offset:]) > threshold)[0]
        if len(indices_start) == 0:
            return np.zeros(0, dtype=np.float32)

        first_sound_idx = offset + indices_start[0]
        lead_in_samples = int(lead_in_sec * sample_rate)
        start_idx = max(0, first_sound_idx - lead_in_samples)

        indices_end = np.where(np.abs(wav) > threshold)[0]
        last_sound_idx = indices_end[-1] if len(indices_end) > 0 else len(wav)
        lead_out_samples = int(lead_out_sec * sample_rate)
        end_idx = min(len(wav), last_sound_idx + lead_out_samples)

        if end_idx <= start_idx:
            return np.zeros(0, dtype=np.float32)

        trimmed = wav[start_idx:end_idx].copy()

        # Micro fade-in i micro fade-out de 10ms per garantir una arrencada suau sense espetecs
        fade_len = min(len(trimmed) // 4, int(0.01 * sample_rate))
        if fade_len > 0:
            trimmed[:fade_len] *= np.linspace(0.0, 1.0, fade_len)
            trimmed[-fade_len:] *= np.linspace(1.0, 0.0, fade_len)

        return trimmed

    def text_to_grapheme_sequence(self, text: str) -> Tuple[np.ndarray, np.ndarray]:
        """Converteix el text en català a la seqüència de grafemes oficial de Matxa-TTS."""
        # El model Matxa-TTS v2 s'ha entrenat amb basic_cleaners del BSC-LT (tot en minúscules)
        clean_text = re.sub(r'\s+', ' ', text.lower()).strip()
        sequence = [SYMBOL_TO_ID[ch] for ch in clean_text if ch in SYMBOL_TO_ID]
        if not sequence:
            # Fallback a caràcters espai si cap símbol coincideix
            sequence = [SYMBOL_TO_ID[" "]]

        # Intersperse amb símbol buit 0 (_pad) com requereix l'arquitectura Matcha
        interspersed = [0] * (len(sequence) * 2 + 1)
        interspersed[1::2] = sequence

        x = np.array(interspersed, dtype=np.int64)[None]
        x_lengths = np.array([x.shape[-1]], dtype=np.int64)
        return x, x_lengths

    def split_sentences(self, text: str) -> List[str]:
        """Divideix el text en frases naturals respectant abreviatures catalanes."""
        clean_text = re.sub(r'[\r\n]+', ' ', text).strip()
        if not clean_text:
            return []

        abbreviations = {
            r'\bDra\.\s*': 'Dra_DOT_ ',
            r'\bDr\.\s*': 'Dr_DOT_ ',
            r'\bSr\.\s*': 'Sr_DOT_ ',
            r'\bSra\.\s*': 'Sra_DOT_ ',
            r'\bProf\.\s*': 'Prof_DOT_ ',
            r'\bpàg\.\s*': 'pàg_DOT_ ',
            r'\bex\.\s*': 'ex_DOT_ ',
            r'\betc\.\s*': 'etc_DOT_ '
        }
        for pattern, repl in abbreviations.items():
            clean_text = re.sub(pattern, repl, clean_text, flags=re.IGNORECASE)

        raw_sentences = re.split(r'(?<=[.!?…])\s+', clean_text)
        sentences = []
        for s in raw_sentences:
            for pattern, repl in abbreviations.items():
                orig_dot = repl.replace('_DOT_ ', '. ')
                s = s.replace(repl.strip(), orig_dot.strip())
            s = s.strip()
            if s:
                sentences.append(s)

        return sentences if sentences else [clean_text]

    def synthesize_utterance(self, text: str, voice_id: str = "elia",
                             speed: float = 1.0, pitch: float = 0.0,
                             clone_audio_path: Optional[str] = None) -> np.ndarray:
        """
        Sintetitza una oració en català amb Matxa-TTS v2 de forma nítida i directa.
        """
        # 1. Normalització de text en català (xifres, percentatges, dates, sigles)
        norm_text = self.text_normalizer.normalize(text)
        if not norm_text:
            return np.zeros(0, dtype=np.float32)

        # Conversió a minúscules i col·lapse d'espais (norma de basic_cleaners de BSC-LT)
        norm_text = re.sub(r'\s+', ' ', norm_text.lower()).strip()
        if not norm_text:
            return np.zeros(0, dtype=np.float32)

        # Assegurar càrrega sota demanda
        if not self.is_loaded():
            loaded = self.ensure_loaded()
            if not loaded:
                print("No s'ha pogut carregar Matxa-TTS.")
                return np.zeros(0, dtype=np.float32)

        voice_key = voice_id.lower()
        spk_info = self.MATXA_SPEAKERS.get(voice_key, self.MATXA_SPEAKERS["elia"])
        spk_id = spk_info["id"]

        try:
            x, x_lengths = self.text_to_grapheme_sequence(norm_text)

            # Escala de durada (length_scale: menor = més ràpid)
            length_scale = float(np.clip(1.0 / max(0.5, speed), 0.6, 1.8))
            temperature = 0.667

            inputs = {
                "x": x,
                "x_lengths": x_lengths,
                "scales": np.array([temperature, length_scale], dtype=np.float32),
                "spks": np.array([spk_id], dtype=np.int64)
            }

            outputs = self.matxa_session.run(None, inputs)

            # L'arxiu ONNX conté el vocoder WaveNeXt integrat a outputs[1]
            wav_out = np.squeeze(outputs[1]).astype(np.float32)

            # 2. Retallar silenci mort inicial (~1s) i final del vocoder WaveNeXt
            wav_out = self.trim_silence_and_fade(wav_out, self.sample_rate)

            # Ajust de to (pitch) opcional mitjançant resample si s'ha especificat
            if abs(pitch) > 0.05 and len(wav_out) > 0:
                pitch_factor = float(2.0 ** (pitch / 12.0))
                orig_len = len(wav_out)
                resampled = scipy.signal.resample(wav_out, int(orig_len / pitch_factor))
                wav_out = scipy.signal.resample(resampled, orig_len).astype(np.float32)

            # Normalització de volum i protecció contra saturació
            max_val = np.max(np.abs(wav_out)) if len(wav_out) > 0 else 0
            if max_val > 0.01:
                wav_out = (wav_out / max_val) * 0.92

            return wav_out

        except Exception as e:
            print(f"Error durant la inferència de Matxa-TTS: {e}")
            return np.zeros(0, dtype=np.float32)

    def synthesize_podcast_stream(self, segments: List[Any],
                                  on_progress: Optional[Callable[[int, int, str], None]] = None,
                                  is_cancelled: Optional[Callable[[], bool]] = None) -> List[Tuple[np.ndarray, float, int]]:
        """
        Sintetitza tot el guió sense límit de durada, oració a oració, amb Matxa-TTS.
        """
        # Assegurar càrrega sota demanda abans d'iniciar el bucle de síntesi
        if not self.is_loaded():
            if on_progress:
                on_progress(0, len(segments), "Carregant model Matxa-TTS v2 a la memòria...")
            self.ensure_loaded()

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
                    preview = text[:40] + ("..." if len(text) > 40 else "")
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
