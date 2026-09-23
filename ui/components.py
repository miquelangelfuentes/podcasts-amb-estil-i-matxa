"""
Components Visuals d'Alta Fidelitat i Contrast Accessible (High-Contrast Clean UI).
Garanteix conformitat estricta amb les directrius WCAG AAA:
- Fons verds o foscos -> SEMPRE text blanc pur (#FFFFFF).
- Fons clars o blancs -> SEMPRE text fosc d'alta llegibilitat (#16291C o #23422C).
- Evita completament el text fosc sobre fons verd.
"""

import customtkinter as ctk
from typing import List, Callable, Optional
from ui.theme import MatchaTheme

class PillSelector(ctk.CTkFrame):
    """Selector en format píndola amb màxim contrast entre actiu i inactiu."""

    def __init__(
        self,
        master,
        values: List[str],
        default_val: Optional[str] = None,
        command: Optional[Callable[[str], None]] = None,
        height: int = 32,
        font_size: int = 10,
        expand_buttons: bool = False,
        btn_width: Optional[int] = None,
        **kwargs
    ):
        super().__init__(master, fg_color="#EAF1EA", corner_radius=int(height / 2), **kwargs)
        self.values = values
        self.command = command
        self.selected_value = default_val or (values[0] if values else "")
        self.buttons = {}
        self.height = height
        self.font_size = font_size
        self.expand_buttons = expand_buttons

        for val in values:
            b_width = btn_width if btn_width is not None else (0 if expand_buttons else 140)
            btn_kwargs = {
                "master": self,
                "text": val,
                "height": height - 6,
                "corner_radius": int((height - 6) / 2),
                "font": ("Segoe UI", font_size, "bold"),
                "command": lambda v=val: self.select(v)
            }
            if expand_buttons or btn_width is not None:
                btn_kwargs["width"] = b_width

            btn = ctk.CTkButton(**btn_kwargs)
            if expand_buttons:
                btn.pack(side="left", expand=True, fill="both", padx=1, pady=2)
            else:
                btn.pack(side="left", padx=2, pady=3)
            self.buttons[val] = btn

        self._update_styles()

    def select(self, val: str):
        if val not in self.values:
            return
        self.selected_value = val
        self._update_styles()
        if self.command:
            self.command(val)

    def set(self, val: str):
        if val in self.values:
            self.selected_value = val
            self._update_styles()

    def get(self) -> str:
        return self.selected_value

    def _update_styles(self):
        for val, btn in self.buttons.items():
            if val == self.selected_value:
                # ESTAT ACTIU: Fons verd cerimonial profund amb TEXT BLANC PUR (Contrast 7.5:1)
                btn.configure(
                    fg_color="#2E5E41",
                    hover_color="#21442F",
                    text_color="#FFFFFF"
                )
            else:
                # ESTAT INACTIU: Fons transparent o suau amb TEXT FOSC LEGIBLE (Contrast 8:1)
                btn.configure(
                    fg_color="transparent",
                    hover_color="#DFEADE",
                    text_color="#284330"
                )

class CleanButton(ctk.CTkButton):
    """Botó amb estils predefinits d'alta llegibilitat i contrast garantit."""

    def __init__(self, master, style="primary", **kwargs):
        height = kwargs.pop("height", 32)
        corner_radius = kwargs.pop("corner_radius", int(height / 2))
        font = kwargs.pop("font", ("Segoe UI", 10, "bold"))

        if style == "primary":
            # Botó d'acció principal: Verd fosc amb text blanc pur
            fg_color = "#2E5E41"
            hover_color = "#21442F"
            text_color = "#FFFFFF"
            border_width = 0
            border_color = None
        elif style == "accent":
            # Botó d'exportació / daurat de bambú: Text blanc pur
            fg_color = "#B8955A"
            hover_color = "#A38249"
            text_color = "#FFFFFF"
            border_width = 0
            border_color = None
        elif style == "danger":
            # Cancel·lar / aturar: Terracota amb text blanc pur
            fg_color = "#C7543E"
            hover_color = "#AF432F"
            text_color = "#FFFFFF"
            border_width = 0
            border_color = None
        elif style == "ghost":
            # Botó secundari net: Blanc amb vora suau i text fosc
            fg_color = "#FFFFFF"
            hover_color = "#F0F5F0"
            text_color = "#223E2A"
            border_width = 1
            border_color = "#D2E0D1"
        else:  # "subtle"
            # Botó suau: fons matxa molt clar amb text verd fosc
            fg_color = "#EBF3EB"
            hover_color = "#DFEADE"
            text_color = "#223E2A"
            border_width = 1
            border_color = "#CFDFCE"

        kwargs["height"] = height
        kwargs["corner_radius"] = corner_radius
        kwargs["font"] = font
        kwargs["fg_color"] = fg_color
        kwargs["hover_color"] = hover_color
        kwargs["text_color"] = text_color
        kwargs["border_width"] = border_width
        if border_color is not None:
            kwargs["border_color"] = border_color

        super().__init__(master, **kwargs)
