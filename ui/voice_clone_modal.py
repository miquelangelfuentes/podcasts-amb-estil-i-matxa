"""
Finestra Emergent de Clonació de Veu Zero-Shot (Voice Clone Modal).
Permet carregar una mostra d'àudio de referència en català (5-15 segons),
extreure el perfil tímbric i afegir-lo com a locutor al guió del pòdcast.
"""

import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import pygame

from ui.theme import MatchaTheme

class VoiceCloneModal(ctk.CTkToplevel):
    """Diàleg modal per a la clonació de veu zero-shot a partir d'un fitxer d'àudio."""

    def __init__(self, parent, tts_engine, on_clone_success_callback=None):
        super().__init__(parent)
        self.parent = parent
        self.tts_engine = tts_engine
        self.on_clone_success_callback = on_clone_success_callback

        self.title("🌿 Clonació de veu zero-shot en català")
        self.geometry("540x500")
        self.resizable(False, False)
        self.configure(fg_color=MatchaTheme.BG_MAIN)

        # Assegurar que estigui en primer pla
        self.transient(parent)
        self.grab_set()

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ico_path = os.path.join(base_dir, "assets", "icon.ico")
        if os.path.exists(ico_path):
            try:
                self.iconbitmap(ico_path)
                self.after(200, lambda: self.iconbitmap(ico_path))
            except Exception:
                pass

        self.selected_file_path = None
        self.test_audio_path = None

        self._build_ui()

    def _build_ui(self):
        # Capçalera
        header_frame = ctk.CTkFrame(self, fg_color=MatchaTheme.BG_CARD, corner_radius=10)
        header_frame.pack(fill="x", padx=20, pady=(20, 15))

        title_lbl = ctk.CTkLabel(
            header_frame,
            text="🌿 Clonació de veu zero-shot (StyleTTS 2)",
            font=MatchaTheme.FONT_SUBTITLE,
            text_color=MatchaTheme.TEXT_MAIN
        )
        title_lbl.pack(anchor="w", padx=15, pady=(12, 4))

        desc_lbl = ctk.CTkLabel(
            header_frame,
            text="Aporta una mostra d'àudio (5-15 segons) en català net per assignar\nel teu timbre a qualsevol personatge del guió.",
            font=MatchaTheme.FONT_SMALL,
            text_color=MatchaTheme.TEXT_SECONDARY,
            justify="left"
        )
        desc_lbl.pack(anchor="w", padx=15, pady=(0, 12))

        # Cos del formulari
        body_frame = ctk.CTkFrame(self, fg_color="transparent")
        body_frame.pack(fill="both", expand=True, padx=25)

        # 1. Nom de la veu
        name_lbl = ctk.CTkLabel(body_frame, text="Nom de la veu al guió:", font=MatchaTheme.FONT_BODY_BOLD, text_color=MatchaTheme.TEXT_MAIN)
        name_lbl.pack(anchor="w", pady=(5, 3))

        self.name_entry = ctk.CTkEntry(
            body_frame,
            placeholder_text="p. ex. LaMevaVeu o ProfJoan",
            fg_color=MatchaTheme.ENTRY_BG,
            border_color=MatchaTheme.ENTRY_BORDER,
            text_color=MatchaTheme.TEXT_MAIN,
            font=MatchaTheme.FONT_BODY,
            height=36
        )
        self.name_entry.pack(fill="x", pady=(0, 12))
        self.name_entry.insert(0, "LaMevaVeu")

        # 2. Fitxer d'àudio de referència
        file_lbl = ctk.CTkLabel(body_frame, text="Fitxer d'àudio de referència (WAV o MP3):", font=MatchaTheme.FONT_BODY_BOLD, text_color=MatchaTheme.TEXT_MAIN)
        file_lbl.pack(anchor="w", pady=(0, 3))

        file_row = ctk.CTkFrame(body_frame, fg_color="transparent")
        file_row.pack(fill="x", pady=(0, 12))

        self.path_entry = ctk.CTkEntry(
            file_row,
            placeholder_text="Cap fitxer seleccionat...",
            fg_color=MatchaTheme.ENTRY_BG,
            border_color=MatchaTheme.ENTRY_BORDER,
            text_color=MatchaTheme.TEXT_MUTED,
            font=MatchaTheme.FONT_SMALL,
            height=36
        )
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        browse_btn = ctk.CTkButton(
            file_row,
            text="Explorar...",
            width=90,
            height=36,
            fg_color=MatchaTheme.PRIMARY_MUTED,
            hover_color=MatchaTheme.PRIMARY,
            text_color=MatchaTheme.TEXT_ON_PRIMARY,
            font=MatchaTheme.FONT_BODY_BOLD,
            command=self._browse_audio_file
        )
        browse_btn.pack(side="right")

        # Estat de la mostra
        self.info_lbl = ctk.CTkLabel(
            body_frame,
            text="Recomanació: veu parlant sense música de fons ni ressò d'habitació.",
            font=MatchaTheme.FONT_SMALL,
            text_color=MatchaTheme.TEXT_SECONDARY
        )
        self.info_lbl.pack(anchor="w", pady=(0, 15))

        # Frase de prova
        test_frame = ctk.CTkFrame(body_frame, fg_color=MatchaTheme.BG_CARD, corner_radius=8)
        test_frame.pack(fill="x", pady=(0, 20), ipady=5)

        test_title = ctk.CTkLabel(test_frame, text="Text de prova de la veu clonada:", font=MatchaTheme.FONT_BODY_BOLD, text_color=MatchaTheme.TEXT_MAIN)
        test_title.pack(anchor="w", padx=12, pady=(8, 2))

        self.test_text_entry = ctk.CTkEntry(
            test_frame,
            fg_color=MatchaTheme.ENTRY_BG,
            border_color=MatchaTheme.ENTRY_BORDER,
            text_color=MatchaTheme.TEXT_MAIN,
            font=MatchaTheme.FONT_BODY,
            height=32
        )
        self.test_text_entry.pack(fill="x", padx=12, pady=(0, 8))
        self.test_text_entry.insert(0, "Aquesta és una prova de síntesi amb la meva veu clonada en català.")

        self.test_btn = ctk.CTkButton(
            test_frame,
            text="▶ Provar veu clonada",
            height=32,
            fg_color=MatchaTheme.ACCENT_BAMBOO,
            hover_color=MatchaTheme.ACCENT_BAMBOO_HOVER,
            text_color="#FFFFFF",
            font=MatchaTheme.FONT_BODY_BOLD,
            command=self._test_voice
        )
        self.test_btn.pack(anchor="e", padx=12, pady=(0, 6))

        # Botons d'acció inferiors
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(fill="x", side="bottom", padx=25, pady=(0, 20))

        cancel_btn = ctk.CTkButton(
            bottom_frame,
            text="Cancel·lar",
            width=110,
            height=38,
            fg_color="transparent",
            border_width=1,
            border_color=MatchaTheme.BORDER_CARD,
            text_color=MatchaTheme.TEXT_MAIN,
            font=MatchaTheme.FONT_BODY,
            command=self.destroy
        )
        cancel_btn.pack(side="left")

        apply_btn = ctk.CTkButton(
            bottom_frame,
            text="✓ Aplicar i afegir al guió",
            height=38,
            fg_color=MatchaTheme.PRIMARY,
            hover_color=MatchaTheme.PRIMARY_HOVER,
            text_color=MatchaTheme.TEXT_ON_PRIMARY,
            font=MatchaTheme.FONT_BODY_BOLD,
            command=self._apply_clone
        )
        apply_btn.pack(side="right", fill="x", expand=True, padx=(15, 0))

    def _browse_audio_file(self):
        filetypes = [
            ("Fitxers d'àudio", "*.wav;*.mp3;*.ogg;*.flac;*.m4a"),
            ("Format WAV", "*.wav"),
            ("Format MP3", "*.mp3"),
            ("Tots els fitxers", "*.*")
        ]
        chosen = filedialog.askopenfilename(title="Selecciona una mostra de veu", filetypes=filetypes)
        if chosen:
            self.selected_file_path = chosen
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, chosen)
            self.info_lbl.configure(
                text=f"Mostra seleccionada: {os.path.basename(chosen)} ({os.path.getsize(chosen)//1024} KB)",
                text_color=MatchaTheme.PRIMARY
            )

    def _test_voice(self):
        if not self.selected_file_path or not os.path.exists(self.selected_file_path):
            messagebox.showwarning("Atenció", "Si us plau, selecciona primer un fitxer d'àudio de referència.")
            return

        text = self.test_text_entry.get().strip()
        if not text:
            return

        self.test_btn.configure(state="disabled", text="Sintetitzant...")

        def run_test():
            try:
                # Extracció de perfil
                speaker_name = self.name_entry.get().strip() or "VeuClonada"
                self.tts_engine.clone_voice_from_audio(self.selected_file_path, speaker_name)
                audio = self.tts_engine.synthesize_utterance(text, clone_audio_path=self.selected_file_path)

                # Desar a fitxer temporal per reproduir
                import soundfile as sf
                tmp_dir = os.path.join(os.path.expanduser("~"), ".podcasts_styletts")
                import time
                import numpy as np
                tmp_file = os.path.join(tmp_dir, f"test_clon_{int(time.time()*1000)}.wav")
                try:
                    pygame.mixer.music.unload()
                except Exception:
                    pass
                sf.write(tmp_file, np.clip(audio, -1.0, 1.0), self.tts_engine.sample_rate, subtype='PCM_16')

                # Reproducció amb pygame
                if not pygame.mixer.get_init():
                    pygame.mixer.init(frequency=self.tts_engine.sample_rate)
                pygame.mixer.music.load(tmp_file)
                pygame.mixer.music.play()

            except Exception as e:
                messagebox.showerror("Error", f"No s'ha pogut provar la veu: {e}")
            finally:
                self.after(0, lambda: self.test_btn.configure(state="normal", text="▶ Provar veu clonada"))

        threading.Thread(target=run_test, daemon=True).start()

    def _apply_clone(self):
        speaker_name = self.name_entry.get().strip()
        if not speaker_name:
            messagebox.showwarning("Atenció", "Indica el nom de la veu.")
            return
        if not self.selected_file_path or not os.path.exists(self.selected_file_path):
            messagebox.showwarning("Atenció", "Selecciona un fitxer d'àudio de referència.")
            return

        # Notificar al pare
        if self.on_clone_success_callback:
            self.on_clone_success_callback(speaker_name, self.selected_file_path)

        self.destroy()
