"""
Mòdul de Processament i Masterització d'Àudio (Audio Processor).
Gestiona l'encadenament per blocs, cross-fades, espacialització estèreo (panning),
normalització de sonoritat (estàndard EBU R128 per a pòdcasts) i
exportació a MP3 estèreo a 160 kbps mitjançant FFmpeg integrat.
"""

import os
import subprocess
import tempfile
import numpy as np
import soundfile as sf
from typing import List, Tuple, Optional
import imageio_ffmpeg

class AudioProcessor:
    """Motor de processament d'àudio i masterització de pòdcast."""

    def __init__(self, sample_rate: int = 22050):
        self.sample_rate = sample_rate
        self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    def generate_silence(self, duration_ms: int) -> np.ndarray:
        """
        Genera silenci digital pur (zeros absoluts) entre frases.
        """
        num_samples = int((duration_ms / 1000.0) * self.sample_rate)
        if num_samples <= 0:
            return np.zeros(0, dtype=np.float32)
        return np.zeros(num_samples, dtype=np.float32)

    def apply_pan(self, mono_audio: np.ndarray, pan: float = 0.0) -> np.ndarray:
        """
        Aplica llei de panoràmica d'energia constant (Constant Power Panning Law).
        pan: -1.0 (esquerra pura) a +1.0 (dreta pura). 0.0 és centre.
        Retorna array estèreo (2, num_samples).
        """
        if mono_audio.ndim > 1:
            mono_audio = np.mean(mono_audio, axis=0)

        pan = max(-1.0, min(1.0, float(pan)))
        angle = (pan + 1.0) * (np.pi / 4.0) # 0 a pi/2

        gain_left = float(np.cos(angle))
        gain_right = float(np.sin(angle))

        left_ch = mono_audio * gain_left
        right_ch = mono_audio * gain_right

        return np.vstack([left_ch, right_ch])

    def crossfade_segments(self, seg1: np.ndarray, seg2: np.ndarray, fade_ms: int = 15) -> np.ndarray:
        """
        Encadena dos segments estèreo (2, N) aplicant un cross-fade suau
        per eliminar espetecs de fase a les unions.
        """
        fade_samples = int((fade_ms / 1000.0) * self.sample_rate)
        if seg1.shape[1] < fade_samples or seg2.shape[1] < fade_samples or fade_samples <= 0:
            return np.concatenate([seg1, seg2], axis=1)

        fade_out = np.linspace(1.0, 0.0, fade_samples, dtype=np.float32)
        fade_in = np.linspace(0.0, 1.0, fade_samples, dtype=np.float32)

        # Aplicació del crossfade a la zona encavalcada
        overlap = seg1[:, -fade_samples:] * fade_out + seg2[:, :fade_samples] * fade_in

        stitched = np.concatenate([
            seg1[:, :-fade_samples],
            overlap,
            seg2[:, fade_samples:]
        ], axis=1)

        return stitched

    def normalize_loudness(self, stereo_audio: np.ndarray, target_lufs: float = -16.0, max_peak_db: float = -1.0) -> np.ndarray:
        """
        Normalitza la sonoritat aproximant l'estàndard EBU R128 (-16 LUFS per a pòdcasts)
        amb sostre de pic màxim (True Peak) a -1.0 dBTP per evitar distorsió en codificar a MP3.
        """
        if stereo_audio.size == 0:
            return stereo_audio

        # Càlcul de potència RMS ponderada
        rms = np.sqrt(np.mean(stereo_audio ** 2) + 1e-9)
        current_lufs = 20.0 * np.log10(rms + 1e-9) - 0.691

        gain_db = target_lufs - current_lufs
        # Limitem el guany màxim per evitar amplificar sorolls en audios molt fluixos
        gain_db = max(-18.0, min(18.0, gain_db))
        gain_linear = 10.0 ** (gain_db / 20.0)

        normalized = stereo_audio * gain_linear

        # Limitador de pic
        peak_limit = 10.0 ** (max_peak_db / 20.0)
        current_peak = np.max(np.abs(normalized))
        if current_peak > peak_limit:
            normalized = normalized * (peak_limit / current_peak)

        return normalized.astype(np.float32)

    def assemble_podcast(self, audio_segments: List[Tuple[np.ndarray, float, int]]) -> np.ndarray:
        """
        Acobla una seqüència de segments d'àudio (mono_audio, pan, pause_after_ms)
        en un únic senyal estèreo final sense cap soroll romanent inicial.
        """
        combined = np.zeros((2, 0), dtype=np.float32)

        for idx, (mono_chunk, pan, pause_ms) in enumerate(audio_segments):
            if mono_chunk is not None and len(mono_chunk) > 0:
                # 1. Eliminació de qualsevol component continu (DC offset) del model acústic
                mono_chunk = mono_chunk - np.mean(mono_chunk)

                # 2. Finestra d'esvaïment suau (micro fade-in / fade-out de 8ms) per evitar espetecs
                fade_len = int(0.008 * self.sample_rate)
                if len(mono_chunk) > 2 * fade_len:
                    fade_in = 0.5 * (1.0 - np.cos(np.pi * np.linspace(0, 1, fade_len, dtype=np.float32)))
                    fade_out = 0.5 * (1.0 + np.cos(np.pi * np.linspace(0, 1, fade_len, dtype=np.float32)))
                    mono_chunk[:fade_len] *= fade_in
                    mono_chunk[-fade_len:] *= fade_out

                stereo_chunk = self.apply_pan(mono_chunk, pan)

                if combined.shape[1] == 0:
                    # Afegim 60 ms de silenci net al començament absolut del podcast
                    initial_clean_silence = np.zeros((2, int(0.06 * self.sample_rate)), dtype=np.float32)
                    combined = np.concatenate([initial_clean_silence, stereo_chunk], axis=1)
                else:
                    combined = self.crossfade_segments(combined, stereo_chunk, fade_ms=10)

            # Inserció de pauses naturals (silenci pur, sense sorolls de sala artificials)
            if pause_ms > 0:
                silence_mono = self.generate_silence(pause_ms)
                silence_stereo = self.apply_pan(silence_mono, pan=0.0)
                if combined.shape[1] == 0:
                    combined = silence_stereo
                else:
                    combined = np.concatenate([combined, silence_stereo], axis=1)

        # Masterització final de sonoritat (-16 LUFS)
        final_mastered = self.normalize_loudness(combined, target_lufs=-16.0, max_peak_db=-1.0)
        return final_mastered

    def export_mp3(self, stereo_audio: np.ndarray, output_path: str, title: str = "Pòdcast amb StyleTTS",
                   artist: str = "StyleTTS 2 Catalan & alVoCat") -> str:
        """
        Exporta l'àudio estèreo a format MP3 a 160 kbps CBR mitjançant FFmpeg.
        (160 kbps és el màxim estàndard ISO MPEG-2 Layer 3 per a la freqüència de 22.05 kHz).
        Inclou metadades ID3 i conversió directa d'alta qualitat.
        """
        output_path = os.path.abspath(output_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Creem un fitxer temporal WAV per passar-lo a FFmpeg
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_wav:
            tmp_wav_path = tmp_wav.name

        try:
            # Transposem a (num_samples, 2) per a soundfile
            sf_audio = stereo_audio.T
            sf.write(tmp_wav_path, sf_audio, self.sample_rate, subtype="FLOAT")

            # Ordre FFmpeg per a MP3 160kbps estèreo constant bit-rate
            cmd = [
                self.ffmpeg_exe,
                "-y",
                "-i", tmp_wav_path,
                "-vn",
                "-ar", str(self.sample_rate if self.sample_rate in (44100, 48000, 22050) else 44100),
                "-ac", "2",
                "-b:a", "160k",
                "-c:a", "libmp3lame",
                "-metadata", f"title={title}",
                "-metadata", f"artist={artist}",
                "-metadata", "album=Pòdcasts Educatius en Català",
                "-metadata", "genre=Podcast / Educació",
                output_path
            ]

            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"Error a FFmpeg al codificar MP3: {result.stderr}")

            return output_path
        finally:
            if os.path.exists(tmp_wav_path):
                try:
                    os.remove(tmp_wav_path)
                except OSError:
                    pass
