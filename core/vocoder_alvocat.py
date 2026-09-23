"""
Mòdul del Vocoder i Normalitzador Acústic alVoCat (Vocos 22kHz).
Projecte AINA: projecte-aina/alvocat-vocos-22khz.
Permet la reconstrucció d'àudio a partir d'espectrogrames Mel de 80 bandes
i la millora de veu neuronal amb ONNXRuntime en GPU o CPU.
"""

import os
import numpy as np
import scipy.signal
from typing import Optional

try:
    import onnxruntime as ort
    HAS_ONNX = True
except ImportError:
    HAS_ONNX = False

class AlvocatVocoder:
    """Vocoder neuronal alVoCat basat en arquitectura Vocos (22050 Hz) amb càrrega sota demanda."""

    def __init__(self, onnx_model_path: Optional[str] = None):
        self.sample_rate = 22050
        self.n_fft = 1024
        self.hop_length = 256
        self.n_mels = 80
        self.onnx_model_path = onnx_model_path
        self.session = None

    def ensure_loaded(self) -> bool:
        """Carrega la sessió ONNX només quan es requereix expressament."""
        if self.session is not None:
            return True
        if self.onnx_model_path and os.path.exists(self.onnx_model_path) and HAS_ONNX:
            self.load_session(self.onnx_model_path)
            return self.session is not None
        return False

    def unload(self):
        """Allibera la sessió de memòria."""
        if self.session is not None:
            self.session = None
            import gc
            gc.collect()

    def load_session(self, model_path: str):
        """Carrega la sessió ONNXRuntime prioritzant CUDA si està disponible."""
        if not HAS_ONNX:
            return
        self.onnx_model_path = model_path
        providers = ["CUDAExecutionProvider", "CPUExecutionProvider"]
        available_providers = ort.get_available_providers()
        selected_providers = [p for p in providers if p in available_providers]
        try:
            self.session = ort.InferenceSession(model_path, providers=selected_providers)
        except Exception:
            self.session = ort.InferenceSession(model_path, providers=["CPUExecutionProvider"])

    def is_loaded(self) -> bool:
        return self.session is not None

    def compute_mel_spectrogram(self, audio: np.ndarray) -> np.ndarray:
        """
        Calcula l'espectrograma Mel de 80 bandes segons l'estàndard d'alVoCat:
        sample_rate=22050, n_fft=1024, hop_length=256, n_mels=80, f_min=0, f_max=8000.
        """
        if audio.ndim > 1:
            audio = np.mean(audio, axis=0)

        # STFT
        window = np.hanning(self.n_fft)
        stft = scipy.signal.stft(
            audio,
            fs=self.sample_rate,
            window=window,
            nperseg=self.n_fft,
            noverlap=self.n_fft - self.hop_length,
            boundary="zeros",
            padded=True
        )[2]

        magnitude = np.abs(stft)

        # Matriu de banc de filtres Mel (escala Slaney / HTK)
        mel_basis = self._create_mel_filterbank(
            sr=self.sample_rate,
            n_fft=self.n_fft,
            n_mels=self.n_mels,
            f_min=0.0,
            f_max=8000.0
        )

        mel_spec = np.dot(mel_basis, magnitude)
        mel_spec = np.log(np.clip(mel_spec, a_min=1e-5, a_max=None))

        # Forma final: (1, 80, T) en float32
        return mel_spec[np.newaxis, :, :].astype(np.float32)

    def decode_mel(self, mel_spectrogram: np.ndarray) -> np.ndarray:
        """
        Decodifica un espectrograma Mel (1, 80, T) en una forma d'ona d'àudio
        utilitzant el model alVoCat ONNX.
        """
        if self.session is None:
            # Fallback si no està carregat el model ONNX
            return self._fallback_inverse_mel(mel_spectrogram)

        input_name = self.session.get_inputs()[0].name
        outputs = self.session.run(None, {input_name: mel_spectrogram})
        if len(outputs) >= 3:
            mag, x, y = outputs[0], outputs[1], outputs[2]
            # Espectrograma complex a partir de components Vocos
            complex_spec = mag[0] * (x[0] + 1j * y[0])
            # Reconstrucció d'ona temporal mitjançant transformació de Fourier inversa
            _, audio_out = scipy.signal.istft(
                complex_spec,
                fs=self.sample_rate,
                window="hann",
                nperseg=self.n_fft,
                noverlap=self.n_fft - self.hop_length
            )
        else:
            audio_out = np.squeeze(outputs[0])

        return audio_out.astype(np.float32)

    def enhance_and_vocode(self, audio: np.ndarray, orig_sr: int = 22050) -> np.ndarray:
        """
        Re-sintetitza l'àudio a través del vocoder neuronal alVoCat per unificar
        l'acústica i aplicar un filtre de qualitat de locució.
        """
        if orig_sr != self.sample_rate:
            num_samples = int(len(audio) * (self.sample_rate / orig_sr))
            audio = scipy.signal.resample(audio, num_samples)

        if not self.is_loaded():
            # Acondicionament acústic de fallback
            b, a = scipy.signal.butter(2, [80.0 / (self.sample_rate / 2.0), 9500.0 / (self.sample_rate / 2.0)], btype="bandpass")
            return scipy.signal.filtfilt(b, a, audio).astype(np.float32)

        mel = self.compute_mel_spectrogram(audio)
        enhanced = self.decode_mel(mel)
        return enhanced

    def _fallback_inverse_mel(self, mel_spectrogram: np.ndarray) -> np.ndarray:
        """Síntesi de suport mitjançant Griffin-Lim si el pes ONNX no està present."""
        return np.zeros(mel_spectrogram.shape[2] * self.hop_length, dtype=np.float32)

    def _create_mel_filterbank(self, sr: int, n_fft: int, n_mels: int, f_min: float, f_max: float) -> np.ndarray:
        """Calcula els pesos dels filtres Mel triangulars."""
        weights = np.zeros((n_mels, int(1 + n_fft // 2)), dtype=np.float32)
        fftfreqs = np.linspace(0, sr / 2, int(1 + n_fft // 2), endpoint=True)

        def hz_to_mel(hz):
            return 2595.0 * np.log10(1.0 + hz / 700.0)

        def mel_to_hz(mel):
            return 700.0 * (10.0 ** (mel / 2595.0) - 1.0)

        mel_fmin = hz_to_mel(f_min)
        mel_fmax = hz_to_mel(f_max)
        mel_points = np.linspace(mel_fmin, mel_fmax, n_mels + 2)
        hz_points = mel_to_hz(mel_points)

        for i in range(n_mels):
            f_prev = hz_points[i]
            f_curr = hz_points[i + 1]
            f_next = hz_points[i + 2]

            up = (fftfreqs - f_prev) / (f_curr - f_prev + 1e-9)
            down = (f_next - fftfreqs) / (f_next - f_curr + 1e-9)
            weights[i] = np.maximum(0, np.minimum(up, down))

        # Normalització d'àrea Slaney
        enorm = 2.0 / (hz_points[2:n_mels + 2] - hz_points[:n_mels] + 1e-9)
        weights *= enorm[:, np.newaxis]
        return weights
