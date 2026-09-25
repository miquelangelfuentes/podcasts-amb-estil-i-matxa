"""
Finestra Modal del Gestor de Models i Components (Components Manager Modal).
Permet comprovar l'estat dels models d'intel·ligència artificial (alVoCat, Matxa-TTS, UPC Ona),
la seva mida en disc i integritat, i descarregar-los per separat des d'Hugging Face.
Inclou diagnòstic de compatibilitat del sistema i guia d'implicacions d'instal·lació offline.
"""

import os
import threading
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from typing import Dict, Any, Optional

from ui.theme import MatchaTheme
from core.model_downloader import ModelDownloader
from core.system_checker import SystemChecker


class SystemCheckModal(ctk.CTkToplevel):
    """Diàleg modal de diagnòstic automàtic de maquinari i requisits."""

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("🔍 Diagnòstic de l'equip — Requisits de Síntesi Offline")
        self.geometry("640x580")
        self.minsize(580, 480)
        self.configure(fg_color=MatchaTheme.BG_MAIN)
        self.transient(parent)
        self.grab_set()

        self._set_modal_icon()
        self._build_ui()
        self._run_diagnostic()

    def _set_modal_icon(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ico_path = os.path.join(base_dir, "assets", "icon.ico")
        if os.path.exists(ico_path):
            try:
                self.iconbitmap(ico_path)
            except Exception:
                pass

    def _build_ui(self):
        # 1. Capçalera
        header = ctk.CTkFrame(self, fg_color=MatchaTheme.BG_CARD, corner_radius=12, border_width=1, border_color=MatchaTheme.BORDER_CARD)
        header.pack(fill="x", padx=18, pady=(16, 10))

        title_lbl = ctk.CTkLabel(
            header,
            text="🔍 Comprovació de requisits de l'equip",
            font=MatchaTheme.FONT_TITLE,
            text_color=MatchaTheme.TEXT_MAIN
        )
        title_lbl.pack(anchor="w", padx=16, pady=(12, 2))

        desc_lbl = ctk.CTkLabel(
            header,
            text="Avalua el disc dur, memòria RAM, processador i GPU per verificar que l'ordinador\npot sintetitzar àudio en català de forma 100% autònoma i sense dependre d'internet.",
            font=MatchaTheme.FONT_SMALL,
            text_color=MatchaTheme.TEXT_SECONDARY,
            justify="left"
        )
        desc_lbl.pack(anchor="w", padx=16, pady=(0, 12))

        # Targeta de veredicte consolidat
        self.verdict_frame = ctk.CTkFrame(self, fg_color=MatchaTheme.BG_CARD, corner_radius=10, border_width=1, border_color=MatchaTheme.BORDER_CARD)
        self.verdict_frame.pack(fill="x", padx=18, pady=(0, 10))

        self.verdict_title = ctk.CTkLabel(
            self.verdict_frame,
            text="Analitzant l'equip...",
            font=MatchaTheme.FONT_SUBTITLE,
            text_color=MatchaTheme.TEXT_MAIN
        )
        self.verdict_title.pack(anchor="w", padx=16, pady=(10, 2))

        self.verdict_desc = ctk.CTkLabel(
            self.verdict_frame,
            text="Si us plau, espera mentre es consulten els paràmetres de maquinari.",
            font=MatchaTheme.FONT_SMALL,
            text_color=MatchaTheme.TEXT_SECONDARY,
            justify="left"
        )
        self.verdict_desc.pack(anchor="w", padx=16, pady=(0, 10))

        # 2. Contenidor de l'anàlisi detallada
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=10)
        self.scroll_frame.pack(fill="both", expand=True, padx=18, pady=(0, 10))

        # 3. Peu
        footer = ctk.CTkFrame(self, fg_color=MatchaTheme.BG_CARD, height=50, corner_radius=12, border_width=1, border_color=MatchaTheme.BORDER_CARD)
        footer.pack(fill="x", padx=18, pady=(0, 16))
        footer.pack_propagate(False)

        btn_recheck = ctk.CTkButton(
            footer,
            text="🔄 Tornar a comprovar",
            font=MatchaTheme.FONT_SMALL,
            fg_color=MatchaTheme.BG_CARD_SUBTLE,
            text_color=MatchaTheme.TEXT_MAIN,
            hover_color=MatchaTheme.BG_CARD_HOVER,
            corner_radius=14,
            height=30,
            command=self._run_diagnostic
        )
        btn_recheck.pack(side="left", padx=12, pady=10)

        btn_close = ctk.CTkButton(
            footer,
            text="Tancar",
            font=MatchaTheme.FONT_SMALL,
            fg_color=MatchaTheme.PRIMARY,
            text_color=MatchaTheme.TEXT_ON_PRIMARY,
            hover_color=MatchaTheme.PRIMARY_HOVER,
            corner_radius=14,
            height=30,
            width=80,
            command=self.destroy
        )
        btn_close.pack(side="right", padx=12, pady=10)

    def _run_diagnostic(self):
        # Netejar elements previs
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        diag = SystemChecker.run_full_diagnostic()

        # Actualitzar veredicte consolidat
        status = diag["overall_status"]
        if status == "ok":
            card_bg = "#EBF5EE"
            border_c = "#A3CFBB"
            text_c = "#1B5E20"
        elif status == "warning":
            card_bg = "#FFF9E6"
            border_c = "#FFE082"
            text_c = "#8C5C00"
        else:
            card_bg = "#FFEBEE"
            border_c = "#EF9A9A"
            text_c = "#B71C1C"

        self.verdict_frame.configure(fg_color=card_bg, border_color=border_c)
        self.verdict_title.configure(text=diag["overall_title"], text_color=text_c)
        self.verdict_desc.configure(text=diag["overall_summary"], text_color=text_c)

        # Icones segons paràmetre
        icons = {
            "Espai en disc": "💾",
            "Memòria RAM": "🧠",
            "Processador (CPU)": "⚡",
            "Acceleració gràfica (GPU)": "🎮",
            "Connexió a Hugging Face": "🌐"
        }

        # Generar targetes individuals
        for check in diag["checks"]:
            card = ctk.CTkFrame(self.scroll_frame, fg_color=MatchaTheme.BG_CARD, corner_radius=10, border_width=1, border_color=MatchaTheme.BORDER_CARD)
            card.pack(fill="x", pady=4)

            top = ctk.CTkFrame(card, fg_color="transparent")
            top.pack(fill="x", padx=14, pady=(8, 2))

            icon = icons.get(check["name"], "📌")
            lbl_name = ctk.CTkLabel(
                top,
                text=f"{icon}  {check['name']}",
                font=MatchaTheme.FONT_SUBTITLE,
                text_color=MatchaTheme.TEXT_MAIN
            )
            lbl_name.pack(side="left")

            st = check["status"]
            if st == "ok":
                badge_bg = "#EBF5EE"
                badge_fg = "#2E7D32"
                badge_text = "✓ Apte"
            elif st == "warning":
                badge_bg = "#FFF8E7"
                badge_fg = "#8C5C00"
                badge_text = "⚠️ Avís"
            else:
                badge_bg = "#FFEBEE"
                badge_fg = "#C62828"
                badge_text = "❌ Atenció"

            badge = ctk.CTkLabel(
                top,
                text=badge_text,
                font=MatchaTheme.FONT_TINY,
                fg_color=badge_bg,
                text_color=badge_fg,
                corner_radius=8,
                padx=8,
                pady=1
            )
            badge.pack(side="right")

            lbl_val = ctk.CTkLabel(
                card,
                text=f"Mesurat: {check['value']}",
                font=MatchaTheme.FONT_SMALL_BOLD,
                text_color=MatchaTheme.PRIMARY
            )
            lbl_val.pack(anchor="w", padx=14, pady=(0, 2))

            lbl_details = ctk.CTkLabel(
                card,
                text=check["details"],
                font=MatchaTheme.FONT_SMALL,
                text_color=MatchaTheme.TEXT_SECONDARY,
                justify="left",
                wraplength=540
            )
            lbl_details.pack(anchor="w", padx=14, pady=(0, 8))


class InstallGuideModal(ctk.CTkToplevel):
    """Diàleg modal informatiu sobre les implicacions d'instal·lar els models locals."""

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("ℹ️ Què implica instal·lar-ho tot? — Guia de Síntesi Offline")
        self.geometry("660x600")
        self.minsize(600, 500)
        self.configure(fg_color=MatchaTheme.BG_MAIN)
        self.transient(parent)
        self.grab_set()

        self._set_modal_icon()
        self._build_ui()

    def _set_modal_icon(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ico_path = os.path.join(base_dir, "assets", "icon.ico")
        if os.path.exists(ico_path):
            try:
                self.iconbitmap(ico_path)
            except Exception:
                pass

    def _build_ui(self):
        header = ctk.CTkFrame(self, fg_color=MatchaTheme.BG_CARD, corner_radius=12, border_width=1, border_color=MatchaTheme.BORDER_CARD)
        header.pack(fill="x", padx=18, pady=(16, 10))

        title_lbl = ctk.CTkLabel(
            header,
            text="ℹ️ Guia d'implicacions: síntesi 100% offline",
            font=MatchaTheme.FONT_TITLE,
            text_color=MatchaTheme.TEXT_MAIN
        )
        title_lbl.pack(anchor="w", padx=16, pady=(12, 2))

        desc_lbl = ctk.CTkLabel(
            header,
            text="Informació clara sobre com funcionen els models neuronals catalans a l'equip,\nquè ocupa cadascun i quines garanties de privadesa ofereixen.",
            font=MatchaTheme.FONT_SMALL,
            text_color=MatchaTheme.TEXT_SECONDARY,
            justify="left"
        )
        desc_lbl.pack(anchor="w", padx=16, pady=(0, 12))

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=10)
        scroll.pack(fill="both", expand=True, padx=18, pady=(0, 10))

        sections = [
            (
                "📦 Espai total necessari (311 MB a 371 MB)",
                "• Configuració 100% Offline recomanada (~311 MB a 371 MB):\n"
                "  - Matxa-TTS v2 multiaccent (BSC-LT): ~260 MB (16 veus catalanes autònomes).\n"
                "  - Vocoder alVoCat 22kHz (Projecte AINA): ~51 MB (reconstrucció acústica i normalitzador d'ortografia).\n"
                "  - Veu UPC Ona FestCat (UPC): ~60 MB (veu neuronal d'alta fidelitat 100% offline).\n\n"
                "• Veus neuronals expressives (Online — 0 MB):\n"
                "  - No ocupen espai a disc; requereixen connexió activa a internet."
            ),
            (
                "⚡ Cal ONNX també? Per a què serveix?",
                "• Sí! El format ONNX (Open Neural Network Exchange) és la clau de la rapidesa i eficiència de l'aplicació.\n"
                "• Permet que Matxa-TTS, alVoCat i UPC Ona s'executin directament sobre la CPU de qualsevol PC o portàtil (Intel o AMD) sense necessitat d'instal·lar paquets feixucs de PyTorch ni entorns gegants de CUDA.\n"
                "• L'aplicació ja porta el motor d'execució ONNX Runtime integrat; només cal que descarreguis els fitxers .onnx dels models per començar a parlar."
            ),
            (
                "✈️ Descàrrega única vs. Ús permanent sense connexió",
                "• Connexió puntual: la connexió a internet només cal una sola vegada per descarregar els arxius oficials des d'Hugging Face (a la pestanya de Models).\n"
                "• Funcionament permanent offline: un cop descarregats, l'ordinador pot funcionar en mode avió, sense connexió Wi-Fi o en aules d'escoles i instituts sense cap accés a la xarxa."
            ),
            (
                "🔒 Privadesa total (0% dades al núvol)",
                "Quan generes un podcast amb Matxa-TTS, alVoCat o UPC Ona:\n"
                "• Cap fragment de text, guió o nom s'envia a servidors externs.\n"
                "• Cap mostra de veu o àudio enregistrat surt mai de l'ordinador.\n"
                "• Compleix estrictament les normatives de protecció de dades (RGPD) en entorns educatius i corporatius."
            ),
            (
                "⏱️ Rendiment i temps de generació",
                "• Síntesi per CPU: els models funcionen a qualsevol ordinador estàndard amb Windows (Intel o AMD) sense necessitat de targeta gràfica dedicada.\n"
                "• Temps estimat: en un processador típic de 4 a 8 nuclis, 1 minut de conversa o lliçó es genera en aproximadament 15-30 segons (més ràpid que en temps real).\n"
                "• Si l'equip disposa de GPU NVIDIA amb suport CUDA o DirectML, la generació és encara més ràpida."
            ),
            (
                "🗣️ Diferència entre els motors disponibles",
                "• Matxa-TTS v2 multiaccent (100% Offline — Recomanat per defecte):\n"
                "  model autònom en ONNX del Barcelona Supercomputing Center amb 16 veus catalanes (central, balear, valencià, nord-occidental i rossellonès). Ràpid i sense dependre de la xarxa.\n\n"
                "• UPC Ona FestCat (100% Offline — Veu neuronal 63 MB):\n"
                "  veu femenina d'alta fidelitat de la UPC basada en el corpus FestCat. 100% privada i autònoma.\n\n"
                "• Veus neuronals ca-ES (Online):\n"
                "  9 veus expressives (Joana, Enric, Ona, Pau, Bet, etc.) connectades al servei de veus al núvol. Ocupa 0 MB al disc, però requereix connexió constant a internet."
            ),
            (
                "☁️ Limitacions d'ús del servei al núvol (Online)",
                "Tot i que és una alternativa ràpida que no requereix espai de disc (0 MB locals), presenta limitacions clau:\n\n"
                "• Connexió permanent requerida: si cau la xarxa Wi-Fi o no hi ha internet, la síntesi no funcionarà.\n"
                "• Privadesa de les dades: el guió s'envia a servidors al núvol; no és apte per a dades personals o privades protegides pel RGPD.\n"
                "• Límits de peticions (Rate Limiting): sessions consecutives molt intenses poden retornar errors de bloqueig temporal (HTTP 429 Too Many Requests).\n"
                "• Sense garantia de servei (SLA): l'endpoint gratuït pot patir canvis d'accés o talls sobtats sense previ avís.\n"
                "• Per a total privadesa i independència, es recomana prioritzar sempre els motors offline (Matxa-TTS v2 o UPC Ona)."
            ),
            (
                "📜 Llicències i suport institucional",
                "Tots els models integrats han estat desenvolupats amb fons públics pel Barcelona Supercomputing Center (BSC-LT), la Universitat Politècnica de Catalunya (UPC) i la Generalitat de Catalunya a través del Projecte AINA, amb llicències obertes aptes per a docència, divulgació i ús institucional."
            )
        ]

        for title, content in sections:
            card = ctk.CTkFrame(scroll, fg_color=MatchaTheme.BG_CARD, corner_radius=10, border_width=1, border_color=MatchaTheme.BORDER_CARD)
            card.pack(fill="x", pady=4)

            t_lbl = ctk.CTkLabel(card, text=title, font=MatchaTheme.FONT_SUBTITLE, text_color=MatchaTheme.PRIMARY)
            t_lbl.pack(anchor="w", padx=14, pady=(10, 4))

            c_lbl = ctk.CTkLabel(card, text=content, font=MatchaTheme.FONT_SMALL, text_color=MatchaTheme.TEXT_SECONDARY, justify="left", wraplength=560)
            c_lbl.pack(anchor="w", padx=14, pady=(0, 10))

        footer = ctk.CTkFrame(self, fg_color=MatchaTheme.BG_CARD, height=50, corner_radius=12, border_width=1, border_color=MatchaTheme.BORDER_CARD)
        footer.pack(fill="x", padx=18, pady=(0, 16))
        footer.pack_propagate(False)

        btn_ok = ctk.CTkButton(
            footer,
            text="D'acord, entès",
            font=MatchaTheme.FONT_SMALL_BOLD,
            fg_color=MatchaTheme.PRIMARY,
            text_color=MatchaTheme.TEXT_ON_PRIMARY,
            hover_color=MatchaTheme.PRIMARY_HOVER,
            corner_radius=14,
            height=30,
            command=self.destroy
        )
        btn_ok.pack(side="right", padx=12, pady=10)


class ComponentsManagerModal(ctk.CTkToplevel):
    """Diàleg modal d'instal·lació i verificació de components de síntesi de veu."""

    def __init__(self, parent, on_update_callback=None):
        super().__init__(parent)
        self.parent = parent
        self.on_update_callback = on_update_callback

        self.downloader = ModelDownloader()
        self.is_downloading = False
        self.active_key = None

        self.title("📦 Gestor de models i components d'àudio")
        self.geometry("690x640")
        self.minsize(620, 530)
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

    def _open_system_check(self):
        """Obre la finestra de diagnòstic de requisits de maquinari."""
        SystemCheckModal(self)

    def _open_install_guide(self):
        """Obre la guia d'implicacions de la instal·lació offline."""
        InstallGuideModal(self)

    def _build_ui(self):
        # 1. Capçalera
        header = ctk.CTkFrame(self, fg_color=MatchaTheme.BG_CARD, corner_radius=12, border_width=1, border_color=MatchaTheme.BORDER_CARD)
        header.pack(fill="x", padx=20, pady=(18, 10))

        title_lbl = ctk.CTkLabel(
            header,
            text="📦 Gestor de models i components d'àudio",
            font=MatchaTheme.FONT_TITLE,
            text_color=MatchaTheme.TEXT_MAIN
        )
        title_lbl.pack(anchor="w", padx=16, pady=(12, 2))

        desc_lbl = ctk.CTkLabel(
            header,
            text="Comprova la instal·lació dels models neuronals de parla del BSC-LT i el Projecte AINA.\nPots descarregar o reinstal·lar cada component per separat.",
            font=MatchaTheme.FONT_SMALL,
            text_color=MatchaTheme.TEXT_SECONDARY,
            justify="left"
        )
        desc_lbl.pack(anchor="w", padx=16, pady=(0, 8))

        # Botons d'acció ràpida a la capçalera
        tools_row = ctk.CTkFrame(header, fg_color="transparent")
        tools_row.pack(fill="x", padx=16, pady=(0, 12))

        btn_check = ctk.CTkButton(
            tools_row,
            text="🔍 Comprovar el meu equip",
            font=MatchaTheme.FONT_SMALL_BOLD,
            fg_color=MatchaTheme.PRIMARY_LIGHT,
            text_color=MatchaTheme.PRIMARY,
            hover_color=MatchaTheme.BG_CARD_HOVER,
            corner_radius=14,
            height=30,
            command=self._open_system_check
        )
        btn_check.pack(side="left", padx=(0, 10))

        btn_guide = ctk.CTkButton(
            tools_row,
            text="ℹ️ Què implica instal·lar-ho tot?",
            font=MatchaTheme.FONT_SMALL_BOLD,
            fg_color=MatchaTheme.BG_CARD_SUBTLE,
            text_color=MatchaTheme.TEXT_MAIN,
            hover_color=MatchaTheme.BG_CARD_HOVER,
            corner_radius=14,
            height=30,
            command=self._open_install_guide
        )
        btn_guide.pack(side="left")

        # 2. Contenidor amb desplaçament per a les targetes de components
        scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=10
        )
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
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

        repo_lbl = ctk.CTkLabel(
            title_box,
            text=f"{info['provider']} · {info['category']} · Repositori: {info['repo_id']}",
            font=MatchaTheme.FONT_TINY,
            text_color=MatchaTheme.TEXT_MUTED
        )
        repo_lbl.pack(anchor="w", pady=(1, 0))

        # Distintiu d'estat
        badge_lbl = ctk.CTkLabel(
            top_row,
            text="Comprovant...",
            font=MatchaTheme.FONT_TINY,
            corner_radius=10,
            padx=10,
            pady=3
        )
        badge_lbl.pack(side="right")

        # Descripció del model
        desc_lbl = ctk.CTkLabel(
            card,
            text=info["desc"],
            font=MatchaTheme.FONT_SMALL,
            text_color=MatchaTheme.TEXT_SECONDARY,
            justify="left",
            wraplength=610
        )
        desc_lbl.pack(anchor="w", padx=14, pady=(2, 6))

        # Barra de progrés de descàrrega (inicialment oculta)
        progress_box = ctk.CTkFrame(card, fg_color="transparent")
        progress_lbl = ctk.CTkLabel(
            progress_box,
            text="",
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

    @staticmethod
    def _format_size_mb(mb: float) -> str:
        """Formata una mida en MB o GB per a una lectura clara a la interfície."""
        if mb >= 1024.0:
            return f"{mb / 1024.0:.2f} GB"
        return f"{mb:.1f} MB"

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

            if st.get("is_cloud", False):
                # Component que funciona per xarxa / núvol (com Edge TTS)
                badge.configure(
                    text="☁️ Servei al núvol (0 MB locals)",
                    text_color="#1565C0",
                    fg_color="#E3F2FD"
                )
                btn_action.configure(
                    text="🌐 Provar connexió al núvol",
                    fg_color=MatchaTheme.BG_CARD_SUBTLE,
                    text_color="#1565C0",
                    hover_color=MatchaTheme.BG_CARD_HOVER,
                    state="normal"
                )
                btn_delete.pack_forget()
            elif st["is_installed"]:
                inst_str = self._format_size_mb(st["installed_size_mb"])
                badge.configure(
                    text=f"✓ Instal·lat ({inst_str})",
                    text_color=MatchaTheme.PRIMARY,
                    fg_color=MatchaTheme.PRIMARY_LIGHT
                )
                btn_action.configure(
                    text="🔄 Reinstal·lar",
                    fg_color=MatchaTheme.BG_CARD_SUBTLE,
                    text_color=MatchaTheme.TEXT_MAIN,
                    hover_color=MatchaTheme.BG_CARD_HOVER,
                    state="normal"
                )
                btn_delete.pack(side="right")
            else:
                pending_count += 1
                exp_str = self._format_size_mb(st["expected_size_mb"])
                badge.configure(
                    text=f"⬇ Pendent (~{exp_str})",
                    text_color="#8C5C00",
                    fg_color="#FFF8E7"
                )
                btn_action.configure(
                    text="⬇ Descarregar",
                    fg_color=MatchaTheme.PRIMARY,
                    text_color=MatchaTheme.TEXT_ON_PRIMARY,
                    hover_color=MatchaTheme.PRIMARY_HOVER,
                    state="normal"
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

        info = self.downloader.MODEL_REPOSITORIES.get(key, {})
        if info.get("is_cloud", False):
            self._test_cloud_connection(key)
            return

        self._start_download_component(key)

    def _test_cloud_connection(self, key: str):
        try:
            import requests
            requests.head("https://azure.microsoft.com", timeout=3)
            messagebox.showinfo(
                "Estat del servei al núvol — Limitacions d'ús",
                "✅ Connexió amb el servei Microsoft Neural ca-ES establerta amb èxit.\n\n"
                "ℹ️ LIMITACIONS D'ÚS GRATUÏT I CONDICIONS:\n"
                "• Connexió requerida: cal internet permanent (no funciona offline).\n"
                "• Privadesa: el contingut del text s'envia als servidors de Microsoft.\n"
                "• Límits de peticions (Rate Limiting): sessions amb centenars de frases seguides a gran velocitat poden ser blocades temporalment per IP (error HTTP 429 Too Many Requests).\n"
                "• Sense garantia de servei (SLA): és un endpoint públic d'accés lliure; Microsoft pot canviar els paràmetres o la disponibilitat sense previ avís.\n"
                "• Varietats dialectals: només inclou 2 veus (Joana i Enric) en català central estàndard.\n\n"
                "💡 Recomanació: per a total privadesa, ús sense internet i 16 varietats dialectals, utilitza Matxa-TTS v2 multiaccent (100% Offline)."
            )
        except Exception as e:
            messagebox.showwarning(
                "Sense connexió al núvol",
                f"No s'ha pogut connectar amb el servei al núvol: {e}\n\n"
                "Pots continuar treballant amb normalitat utilitzant Matxa-TTS v2 multiaccent, que funciona 100% offline sense connexió ni límits externs."
            )

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
                    cur_str = f"{downloaded / (1024*1024*1024):.2f} GB" if total >= 1024*1024*1024 else f"{downloaded / (1024*1024):.1f} MB"
                    tot_str = f"{total / (1024*1024*1024):.2f} GB" if total >= 1024*1024*1024 else f"{total / (1024*1024):.1f} MB"
                    speed_str = f" · {speed_mb_s:.1f} MB/s" if speed_mb_s > 0 else ""
                    progress_lbl.configure(text=f"{filename}: {cur_str} / {tot_str} ({int(pct*100)}%){speed_str}")
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
                    err_msg = getattr(self.downloader, "last_error", "")
                    detail = f"\n\nDetall tècnic: {err_msg}" if err_msg else ""
                    messagebox.showerror("Error", f"No s'ha pogut completar la descàrrega de «{self.downloader.MODEL_REPOSITORIES[key]['name']}».{detail}")

            self.after(0, _on_finish)

        threading.Thread(target=_worker, daemon=True).start()

    def _download_all_pending(self):
        if self.is_downloading:
            return
        statuses = self.downloader.get_all_components_status()
        pending = [k for k, s in statuses.items() if not s["is_installed"] and not s.get("is_cloud", False)]
        if not pending:
            messagebox.showinfo("Gestor de models", "Tots els models locals ja estan instal·lats!")
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
                            cur_str = f"{downloaded / (1024*1024*1024):.2f} GB" if total >= 1024*1024*1024 else f"{downloaded / (1024*1024):.1f} MB"
                            tot_str = f"{total / (1024*1024*1024):.2f} GB" if total >= 1024*1024*1024 else f"{total / (1024*1024):.1f} MB"
                            speed_str = f" · {speed_mb_s:.1f} MB/s" if speed_mb_s > 0 else ""
                            card_ui["progress_lbl"].configure(text=f"{filename}: {cur_str} / {tot_str} ({int(pct*100)}%){speed_str}")
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
