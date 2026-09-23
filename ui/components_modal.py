"""
Finestra Modal del Gestor de Models i Components (Components Manager Modal).
Permet comprovar l'estat dels models d'intel·ligència artificial (alVoCat, Matxa-TTS, StyleTTS),
la seva mida en disc i integritat, i descarregar-los per separat des d'Hugging Face.
"""

import os
import threading
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from typing import Dict, Any, Optional

from ui.theme import MatchaTheme
from core.model_downloader import ModelDownloader

class ComponentsManagerModal(ctk.CTkToplevel):
    """Diàleg modal d'instal·lació i verificació de components de síntesi de veu."""

    def __init__(self, parent, on_update_callback=None):
        super().__init__(parent)
        self.parent = parent
        self.on_update_callback = on_update_callback

        self.downloader = ModelDownloader()
        self.is_downloading = False
        self.active_key = None

        self.title("📦 Gestor de models i components")
        self.geometry("680x620")
        self.minsize(620, 520)
        self.configure(fg_color=MatchaTheme.BG_MAIN)

        # Assegurar que estigui en primer pla
        self.transient(parent)
        self.grab_set()

        # Icona del chawan verd
        self._set_modal_icon()

        self._cards: Dict[str, Dict[str, Any]] = {}
        self._build_ui()
        self._refresh_all_status()

    def _set_modal_icon(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ico_path = os.path.join(base_dir, "assets", "icon.ico")
        if os.path.exists(ico_path):
            try:
                self.iconbitmap(ico_path)
                self.after(200, lambda: self.iconbitmap(ico_path))
            except Exception:
                pass

    def _build_ui(self):
        # 1. Capçalera
        header = ctk.CTkFrame(self, fg_color=MatchaTheme.BG_CARD, corner_radius=12, border_width=1, border_color=MatchaTheme.BORDER_CARD)
        header.pack(fill="x", padx=20, pady=(18, 12))

        title_lbl = ctk.CTkLabel(
            header,
            text="📦 Gestor de models i components d'àudio",
            font=MatchaTheme.FONT_TITLE,
            text_color=MatchaTheme.TEXT_MAIN
        )
        title_lbl.pack(anchor="w", padx=16, pady=(12, 4))

        desc_lbl = ctk.CTkLabel(
            header,
            text="Comprova la instal·lació dels models neuronals del BSC-LT i el Projecte AINA.\nPots descarregar o reinstal·lar cada component per separat.",
            font=MatchaTheme.FONT_SMALL,
            text_color=MatchaTheme.TEXT_SECONDARY,
            justify="left"
        )
        desc_lbl.pack(anchor="w", padx=16, pady=(0, 12))

        # 2. Contenidor amb desplaçament per a les targetes de components
        scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=10
        )
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 12))
        self.scroll_frame = scroll_frame

        # Construir una targeta per a cada model
        models_info = self.downloader.MODEL_REPOSITORIES
        for key, info in models_info.items():
            self._create_component_card(scroll_frame, key, info)

        # 3. Barra inferior d'accions globals
        footer = ctk.CTkFrame(self, fg_color=MatchaTheme.BG_CARD, height=54, corner_radius=12, border_width=1, border_color=MatchaTheme.BORDER_CARD)
        footer.pack(fill="x", padx=20, pady=(0, 18))
        footer.pack_propagate(False)

        btn_refresh = ctk.CTkButton(
            footer,
            text="🔄 Actualitzar estat",
            font=MatchaTheme.FONT_SMALL,
            fg_color=MatchaTheme.BG_CARD_SUBTLE,
            text_color=MatchaTheme.TEXT_MAIN,
            hover_color=MatchaTheme.BG_CARD_HOVER,
            corner_radius=16,
            height=32,
            width=130,
            command=self._refresh_all_status
        )
        btn_refresh.pack(side="left", padx=12, pady=10)

        self.btn_download_all = ctk.CTkButton(
            footer,
            text="⬇ Descarregar pendents",
            font=MatchaTheme.FONT_SMALL_BOLD,
            fg_color=MatchaTheme.PRIMARY,
            text_color=MatchaTheme.TEXT_ON_PRIMARY,
            hover_color=MatchaTheme.PRIMARY_HOVER,
            corner_radius=16,
            height=32,
            width=170,
            command=self._download_all_pending
        )
        self.btn_download_all.pack(side="left", padx=(0, 12), pady=10)

        btn_close = ctk.CTkButton(
            footer,
            text="Tancar",
            font=MatchaTheme.FONT_SMALL,
            fg_color="transparent",
            text_color=MatchaTheme.TEXT_SECONDARY,
            hover_color=MatchaTheme.BG_CARD_HOVER,
            corner_radius=16,
            height=32,
            width=80,
            command=self.destroy
        )
        btn_close.pack(side="right", padx=12, pady=10)

    def _create_component_card(self, parent, key: str, info: Dict[str, Any]):
        card = ctk.CTkFrame(
            parent,
            fg_color=MatchaTheme.BG_CARD,
            corner_radius=MatchaTheme.CARD_RADIUS,
            border_width=1,
            border_color=MatchaTheme.BORDER_CARD
        )
        card.pack(fill="x", pady=6)

        # Fila superior de la targeta: Títol, categoria i estat
        top_row = ctk.CTkFrame(card, fg_color="transparent")
        top_row.pack(fill="x", padx=14, pady=(12, 4))

        title_box = ctk.CTkFrame(top_row, fg_color="transparent")
        title_box.pack(side="left", fill="x", expand=True)

        name_lbl = ctk.CTkLabel(
            title_box,
            text=f"{info['name']}",
            font=MatchaTheme.FONT_SUBTITLE,
            text_color=MatchaTheme.TEXT_MAIN
        )
        name_lbl.pack(anchor="w")

        meta_lbl = ctk.CTkLabel(
            title_box,
            text=f"{info['provider']} · {info['category']} · Repositori: {info['repo_id']}",
            font=MatchaTheme.FONT_TINY,
            text_color=MatchaTheme.TEXT_MUTED
        )
        meta_lbl.pack(anchor="w")

        badge_lbl = ctk.CTkLabel(
            top_row,
            text="Comprovant...",
            font=MatchaTheme.FONT_SMALL_BOLD,
            text_color=MatchaTheme.PRIMARY,
            fg_color=MatchaTheme.PRIMARY_LIGHT,
            corner_radius=10,
            padx=10,
            pady=4
        )
        badge_lbl.pack(side="right")

        # Descripció
        desc_lbl = ctk.CTkLabel(
            card,
            text=info["desc"],
            font=MatchaTheme.FONT_SMALL,
            text_color=MatchaTheme.TEXT_SECONDARY,
            justify="left",
            wraplength=580
        )
        desc_lbl.pack(anchor="w", padx=14, pady=(2, 8))

        # Contenidor de progrés (ocult per defecte)
        progress_box = ctk.CTkFrame(card, fg_color="transparent")
        progress_lbl = ctk.CTkLabel(
            progress_box,
            text="Descarregant fitxers...",
            font=MatchaTheme.FONT_TINY,
            text_color=MatchaTheme.TEXT_MUTED
        )
        progress_lbl.pack(anchor="w", pady=(0, 2))

        progress_bar = ctk.CTkProgressBar(
            progress_box,
            height=6,
            corner_radius=3,
            progress_color=MatchaTheme.PROGRESS_FILL,
            fg_color=MatchaTheme.PROGRESS_BG
        )
        progress_bar.pack(fill="x")
        progress_bar.set(0)

        # Fila d'accions de la targeta
        actions_row = ctk.CTkFrame(card, fg_color="transparent")
        actions_row.pack(fill="x", padx=14, pady=(4, 12))

        btn_action = ctk.CTkButton(
            actions_row,
            text="⬇ Descarregar",
            font=MatchaTheme.FONT_SMALL,
            height=28,
            corner_radius=14,
            command=lambda k=key: self._on_action_click(k)
        )
        btn_action.pack(side="left")

        btn_delete = ctk.CTkButton(
            actions_row,
            text="Alliberar espai",
            font=MatchaTheme.FONT_TINY,
            fg_color="transparent",
            text_color=MatchaTheme.TEXT_MUTED,
            hover_color=MatchaTheme.BG_CARD_HOVER,
            height=28,
            corner_radius=14,
            width=90,
            command=lambda k=key: self._on_delete_click(k)
        )
        btn_delete.pack(side="right")

        self._cards[key] = {
            "badge": badge_lbl,
            "desc": desc_lbl,
            "progress_box": progress_box,
            "progress_lbl": progress_lbl,
            "progress_bar": progress_bar,
            "btn_action": btn_action,
            "btn_delete": btn_delete
        }

    def _refresh_all_status(self):
        """Actualitza la informació visual de tots els components."""
        statuses = self.downloader.get_all_components_status()
        pending_count = 0

        for key, st in statuses.items():
            card_ui = self._cards.get(key)
            if not card_ui:
                continue

            badge = card_ui["badge"]
            btn_action = card_ui["btn_action"]
            btn_delete = card_ui["btn_delete"]

            if st["is_installed"]:
                badge.configure(
                    text=f"✓ Instal·lat ({st['installed_size_mb']} MB)",
                    text_color=MatchaTheme.PRIMARY,
                    fg_color=MatchaTheme.PRIMARY_LIGHT
                )
                btn_action.configure(
                    text="🔄 Reinstal·lar",
                    fg_color=MatchaTheme.BG_CARD_SUBTLE,
                    text_color=MatchaTheme.TEXT_MAIN,
                    hover_color=MatchaTheme.BG_CARD_HOVER
                )
                btn_delete.pack(side="right")
            else:
                pending_count += 1
                badge.configure(
                    text=f"⬇ Pendent (~{st['expected_size_mb']} MB)",
                    text_color="#8C5C00",
                    fg_color="#FFF8E7"
                )
                btn_action.configure(
                    text="⬇ Descarregar",
                    fg_color=MatchaTheme.PRIMARY,
                    text_color=MatchaTheme.TEXT_ON_PRIMARY,
                    hover_color=MatchaTheme.PRIMARY_HOVER
                )
                btn_delete.pack_forget()

        if pending_count > 0:
            self.btn_download_all.configure(
                text=f"⬇ Descarregar ({pending_count} pendents)",
                state="normal"
            )
        else:
            self.btn_download_all.configure(
                text="✓ Tots instal·lats",
                state="disabled"
            )

    def _on_action_click(self, key: str):
        if self.is_downloading:
            messagebox.showinfo("Descàrrega en curs", "Ja hi ha una descàrrega en marxa. Espera que acabi.")
            return
        self._start_download_component(key)

    def _on_delete_click(self, key: str):
        if self.is_downloading:
            return
        info = self.downloader.MODEL_REPOSITORIES.get(key, {})
        name = info.get("name", key)
        if messagebox.askyesno("Alliberar espai", f"Segur que vols eliminar els fitxers locals de «{name}»?"):
            self.downloader.delete_component(key)
            self._refresh_all_status()
            if self.on_update_callback:
                self.on_update_callback()

    def _start_download_component(self, key: str):
        self.is_downloading = True
        self.active_key = key
        card_ui = self._cards[key]

        progress_box = card_ui["progress_box"]
        progress_lbl = card_ui["progress_lbl"]
        progress_bar = card_ui["progress_bar"]
        btn_action = card_ui["btn_action"]

        progress_box.pack(fill="x", padx=14, pady=(0, 8))
        progress_bar.set(0)
        progress_lbl.configure(text="Connectant amb Hugging Face...")
        btn_action.configure(state="disabled", text="Descarregant...")

        def _progress(downloaded, total, filename, speed_mb_s):
            def _ui_update():
                if total > 0:
                    pct = max(0.0, min(1.0, downloaded / total))
                    progress_bar.set(pct)
                    cur_mb = downloaded / (1024 * 1024)
                    tot_mb = total / (1024 * 1024)
                    speed_str = f" · {speed_mb_s:.1f} MB/s" if speed_mb_s > 0 else ""
                    progress_lbl.configure(text=f"{filename}: {cur_mb:.1f} MB / {tot_mb:.1f} MB ({int(pct*100)}%){speed_str}")
                else:
                    progress_lbl.configure(text=f"{filename}: descarregant...")
            self.after(0, _ui_update)

        def _worker():
            try:
                success = self.downloader.download_model(key, progress_callback=_progress)
            except Exception as e:
                success = False
                print(f"Error descarregant model {key}: {e}")

            def _on_finish():
                self.is_downloading = False
                self.active_key = None
                progress_box.pack_forget()
                btn_action.configure(state="normal")
                self._refresh_all_status()
                if self.on_update_callback:
                    self.on_update_callback()

                if success:
                    messagebox.showinfo("Descàrrega completada", f"El component «{self.downloader.MODEL_REPOSITORIES[key]['name']}» s'ha instal·lat amb èxit.")
                else:
                    messagebox.showerror("Error", f"No s'ha pogut completar la descàrrega de «{self.downloader.MODEL_REPOSITORIES[key]['name']}». Comprova la connexió a Internet.")

            self.after(0, _on_finish)

        threading.Thread(target=_worker, daemon=True).start()

    def _download_all_pending(self):
        if self.is_downloading:
            return
        statuses = self.downloader.get_all_components_status()
        pending = [k for k, s in statuses.items() if not s["is_installed"]]
        if not pending:
            messagebox.showinfo("Gestor de models", "Tots els models ja estan instal·lats!")
            return

        def _queue_worker():
            for key in pending:
                self.is_downloading = True
                self.active_key = key
                card_ui = self._cards[key]

                def _start_card():
                    card_ui["progress_box"].pack(fill="x", padx=14, pady=(0, 8))
                    card_ui["btn_action"].configure(state="disabled", text="Descarregant...")
                self.after(0, _start_card)

                def _progress(downloaded, total, filename, speed_mb_s):
                    def _ui_update():
                        if total > 0:
                            pct = max(0.0, min(1.0, downloaded / total))
                            card_ui["progress_bar"].set(pct)
                            cur_mb = downloaded / (1024 * 1024)
                            tot_mb = total / (1024 * 1024)
                            speed_str = f" · {speed_mb_s:.1f} MB/s" if speed_mb_s > 0 else ""
                            card_ui["progress_lbl"].configure(text=f"{filename}: {cur_mb:.1f} MB / {tot_mb:.1f} MB ({int(pct*100)}%){speed_str}")
                    self.after(0, _ui_update)

                try:
                    self.downloader.download_model(key, progress_callback=_progress)
                except Exception as e:
                    print(f"Error a la cua per a {key}: {e}")

                def _finish_card():
                    card_ui["progress_box"].pack_forget()
                    card_ui["btn_action"].configure(state="normal")
                    self._refresh_all_status()
                self.after(0, _finish_card)

            def _all_done():
                self.is_downloading = False
                self.active_key = None
                self._refresh_all_status()
                if self.on_update_callback:
                    self.on_update_callback()
                messagebox.showinfo("Cua completada", "S'ha completat la descàrrega de tots els components pendents.")

            self.after(0, _all_done)

        threading.Thread(target=_queue_worker, daemon=True).start()
