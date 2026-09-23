"""
Giny de Reproducció d'Àudio i Exportació (Audio Player Widget).
Disseny modern, elegant i minimalista en blanc pur i verd matxa.
Garanteix conformitat estricta amb el contrast de colors (WCAG AAA).
"""

import os
import time
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import pygame
import soundfile as sf
import numpy as np
from typing import Optional

from ui.theme import MatchaTheme
from ui.components import CleanButton

class AudioPlayerWidget(ctk.CTkFrame):
    """Component visual minimalista per reproduir i exportar el pòdcast generat."""

    def __init__(self, parent, audio_processor, **kwargs):
        super().__init__(
            parent,
            fg_color=MatchaTheme.BG_CARD,
            corner_radius=MatchaTheme.CARD_RADIUS,
            border_width=1,
            border_color=MatchaTheme.BORDER_CARD,
            **kwargs
        )
        self.audio_processor = audio_processor

        self.current_audio_stereo: Optional[np.ndarray] = None
        self.temp_wav_path: Optional[str] = None
        self.is_playing = False
        self.duration_seconds = 0.0
        self.current_position = 0.0
        self.stop_requested = False
        self.is_tracking = False

        self._init_mixer()
        self._build_ui()

    def _init_mixer(self):
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=1024)
        except Exception as e:
            print("Avís inicialitzant pygame.mixer:", e)

    def _build_ui(self):
        # Capçalera del reproductor
        title_row = ctk.CTkFrame(self, fg_color="transparent")
        title_row.pack(fill="x", padx=18, pady=(14, 4))

        title_lbl = ctk.CTkLabel(
            title_row,
            text="🎧 Reproductor del pòdcast",
            font=MatchaTheme.FONT_SUBTITLE,
            text_color=MatchaTheme.TEXT_MAIN
        )
        title_lbl.pack(side="left")

        self.status_badge = ctk.CTkLabel(
            title_row,
            text="Cap àudio carregat",
            font=MatchaTheme.FONT_SMALL,
            text_color=MatchaTheme.TEXT_MUTED,
            fg_color=MatchaTheme.BG_CARD_SUBTLE,
            corner_radius=10,
            padx=10,
            pady=3
        )
        self.status_badge.pack(side="right")

        # Barra de progrés temporal neta
        prog_row = ctk.CTkFrame(self, fg_color="transparent")
        prog_row.pack(fill="x", padx=18, pady=(4, 6))

        self.time_current_lbl = ctk.CTkLabel(
            prog_row,
            text="00:00",
            font=MatchaTheme.FONT_SMALL_BOLD,
            text_color=MatchaTheme.TEXT_SECONDARY
        )
        self.time_current_lbl.pack(side="left")

        self.progress_slider = ctk.CTkSlider(
            prog_row,
            from_=0.0,
            to=100.0,
            height=14,
            progress_color=MatchaTheme.PRIMARY,
            button_color=MatchaTheme.PRIMARY,
            button_hover_color=MatchaTheme.PRIMARY_HOVER,
            fg_color=MatchaTheme.PROGRESS_BG,
            command=self._on_seek
        )
        self.progress_slider.pack(side="left", fill="x", expand=True, padx=12)
        self.progress_slider.set(0.0)

        self.time_total_lbl = ctk.CTkLabel(
            prog_row,
            text="00:00",
            font=MatchaTheme.FONT_SMALL_BOLD,
            text_color=MatchaTheme.TEXT_SECONDARY
        )
        self.time_total_lbl.pack(side="right")

        # Fila de botons de control i exportació amb contrast impecable
        controls_row = ctk.CTkFrame(self, fg_color="transparent")
        controls_row.pack(fill="x", padx=18, pady=(4, 14))

        # Botons d'acció de reproducció
        btn_frame = ctk.CTkFrame(controls_row, fg_color="transparent")
        btn_frame.pack(side="left")

        # Botó Reproduir: Verd fosc amb TEXT BLANC PUR
        self.play_btn = CleanButton(
            btn_frame,
            style="primary",
            text="▶ Reproduir",
            width=115,
            height=32,
            state="disabled",
            command=self.toggle_play_pause
        )
        self.play_btn.pack(side="left", padx=(0, 8))

        # Botó Aturar: Blanc amb vora suau i TEXT FOSC
        self.stop_btn = CleanButton(
            btn_frame,
            style="ghost",
            text="■ Aturar",
            width=75,
            height=32,
            state="disabled",
            command=self.stop
        )
        self.stop_btn.pack(side="left")

        # Botó d'exportació a MP3: Daurat de bambú amb TEXT BLANC PUR
        self.export_btn = CleanButton(
            controls_row,
            style="accent",
            text="💾 Desar MP3 (160k)",
            height=32,
            state="disabled",
            command=self._export_mp3_dialog
        )
        self.export_btn.pack(side="right")

    def load_audio(self, stereo_audio: np.ndarray, title: str = "Pòdcast"):
        """Carrega l'àudio estèreo sintetitzat al reproductor."""
        self.stop()
        self.current_audio_stereo = stereo_audio
        num_samples = stereo_audio.shape[1]
        self.duration_seconds = float(num_samples) / float(self.audio_processor.sample_rate)

        try:
            pygame.mixer.music.unload()
        except Exception:
            pass

        tmp_dir = os.path.join(os.path.expanduser("~"), ".podcasts_matxa")
        os.makedirs(tmp_dir, exist_ok=True)
        self.temp_wav_path = os.path.join(tmp_dir, f"podcast_{int(time.time() * 1000)}.wav")

        audio_clipped = np.clip(stereo_audio.T, -1.0, 1.0)
        sf.write(self.temp_wav_path, audio_clipped, self.audio_processor.sample_rate, subtype='PCM_16')

        self.time_total_lbl.configure(text=self._format_time(self.duration_seconds))
        self.time_current_lbl.configure(text="00:00")
        self.progress_slider.configure(to=max(1.0, self.duration_seconds))
        self.progress_slider.set(0.0)

        mins = int(self.duration_seconds // 60)
        secs = int(self.duration_seconds % 60)
        self.status_badge.configure(
            text=f"Àudio llest ({mins:02d}:{secs:02d}) · Estèreo 160k",
            text_color=MatchaTheme.PRIMARY,
            fg_color=MatchaTheme.PRIMARY_LIGHT
        )

        self.play_btn.configure(state="normal", text="▶ Reproduir")
        self.stop_btn.configure(state="normal")
        self.export_btn.configure(state="normal")

    def toggle_play_pause(self):
        if not self.temp_wav_path or not os.path.exists(self.temp_wav_path):
            return

        if self.is_playing:
            try:
                pygame.mixer.music.pause()
            except Exception:
                pass
            self.is_playing = False
            self.play_btn.configure(text="▶ Reprendre")
        else:
            self._init_mixer()
            try:
                if not pygame.mixer.music.get_busy() and self.current_position == 0.0:
                    pygame.mixer.music.load(self.temp_wav_path)
                    pygame.mixer.music.play()
                elif not pygame.mixer.music.get_busy() and self.current_position > 0.0:
                    pygame.mixer.music.load(self.temp_wav_path)
                    try:
                        pygame.mixer.music.play(start=self.current_position)
                    except Exception:
                        pygame.mixer.music.play()
                else:
                    pygame.mixer.music.unpause()
            except Exception as e:
                print(f"Error reproduint amb pygame: {e}")
                try:
                    import winsound
                    threading.Thread(target=lambda: winsound.PlaySound(self.temp_wav_path, winsound.SND_FILENAME), daemon=True).start()
                except Exception:
                    pass

            self.is_playing = True
            self.stop_requested = False
            self.play_btn.configure(text="⏸ Pausar")
            if not self.is_tracking:
                self._start_progress_tracker()

    def stop(self):
        self.stop_requested = True
        self.is_playing = False
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        except Exception:
            pass
        self.current_position = 0.0
        self.progress_slider.set(0.0)
        self.time_current_lbl.configure(text="00:00")
        self.play_btn.configure(text="▶ Reproduir")

    def _on_seek(self, value):
        seek_time = float(value)
        self.current_position = seek_time
        self.time_current_lbl.configure(text=self._format_time(seek_time))
        if self.is_playing and self.temp_wav_path:
            try:
                pygame.mixer.music.load(self.temp_wav_path)
                pygame.mixer.music.play(start=seek_time)
            except Exception:
                pass

    def _start_progress_tracker(self):
        self.is_tracking = True
        self.stop_requested = False

        def track():
            start_wall_time = time.time() - self.current_position
            while self.is_playing and not self.stop_requested:
                time.sleep(0.1)
                elapsed = time.time() - start_wall_time

                if elapsed >= self.duration_seconds:
                    self.current_position = self.duration_seconds
                    self.after(0, lambda: self._update_ui_progress(self.duration_seconds))
                    break

                if elapsed > 0.5:
                    try:
                        if not pygame.mixer.music.get_busy() and self.is_playing:
                            break
                    except Exception:
                        pass

                self.current_position = min(elapsed, self.duration_seconds)
                self.after(0, lambda p=self.current_position: self._update_ui_progress(p))

            self.is_tracking = False
            if not self.stop_requested and self.is_playing:
                self.after(0, self.stop)

        threading.Thread(target=track, daemon=True).start()

    def _update_ui_progress(self, pos_s):
        self.progress_slider.set(pos_s)
        self.time_current_lbl.configure(text=self._format_time(pos_s))

    def _format_time(self, seconds: float) -> str:
        s = int(seconds)
        m = s // 60
        sec = s % 60
        return f"{m:02d}:{sec:02d}"

    def _export_mp3_dialog(self):
        if self.current_audio_stereo is None:
            return

        initial_name = "podcast_matxa_catala.mp3"
        file_path = filedialog.asksaveasfilename(
            title="Desar pòdcast com a MP3",
            defaultextension=".mp3",
            initialfile=initial_name,
            filetypes=[("Arxiu MP3 (160 kbps estèreo)", "*.mp3"), ("Tots els fitxers", "*.*")]
        )
        if file_path:
            try:
                self.audio_processor.export_mp3(
                    self.current_audio_stereo,
                    file_path,
                    title="Pòdcasts amb Estil i Matxa",
                    artist="Pòdcasts amb Estil i Matxa · BSC-LT & alVoCat"
                )
                messagebox.showinfo(
                    "Pòdcast desat amb èxit",
                    f"El fitxer s'ha exportat correctament:\n{file_path}\n\nFormat: MP3 Estèreo, 160 kbps CBR\nSonoritat: EBU R128 (-16 LUFS)"
                )
            except Exception as e:
                messagebox.showerror("Error d'exportació", f"No s'ha pogut desar el fitxer MP3: {e}")
