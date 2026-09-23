"""
Punt d'entrada principal: Pòdcasts amb Estil i Matxa.
Síntesi de pòdcasts en català d'1, 2 o 3 veus sense límit de durada.
Desenvolupat per a materials educatius, formatius i divulgatius.
Models: BSC-LT StyleTTS 2, Matxa-TTS v2 multiaccent & alVoCat 22kHz (Projecte AINA).
"""

import os
import sys
import ctypes

# Assegurar que el directori arrel del projecte és al sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

def enable_windows_dpi_awareness():
    """Activa el suport per a pantalles d'alta densitat (High DPI) a Windows."""
    try:
        if sys.platform.startswith("win"):
            ctypes.windll.shcore.SetProcessDpiAwareness(2) # Per-Monitor DPI Aware
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

def main():
    enable_windows_dpi_awareness()
    from ui.main_window import MainWindow

    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()
