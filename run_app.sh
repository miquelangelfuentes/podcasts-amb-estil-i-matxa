#!/usr/bin/env bash
# ==============================================================================
# Script de llançament per a Linux: Pòdcasts amb Estil i Matxa
# Configura automàticament l'entorn virtual i arrenca l'aplicació.
# ==============================================================================

set -e

# Directori base del script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "============================================================"
echo "  🎙️🍵 Pòdcasts amb Estil i Matxa (Linux)"
echo "============================================================"

# 1. Comprovació de Python 3
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 no està instal·lat al sistema."
    echo "Pots instal·lar-lo amb: sudo apt install python3 python3-pip python3-venv python3-tk libsndfile1"
    exit 1
fi

PYTHON_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Versió de Python detectada: $PYTHON_VER"

# 2. Creació i activació de l'entorn virtual .venv
if [ ! -d ".venv" ]; then
    echo "Creant l'entorn virtual de Python (.venv)..."
    python3 -m venv .venv || {
        echo "[ERROR] No s'ha pogut crear l'entorn virtual."
        echo "Si us plau, instal·la el paquet venv amb:"
        echo "  sudo apt install python3-venv python3-tk libsndfile1"
        exit 1
    }
fi

source .venv/bin/activate

# 3. Verificació de paquets del sistema (Tkinter)
python3 -c "import tkinter" 2>/dev/null || {
    echo "[AVÍS] Tkinter no està disponible a l'entorn de Python."
    echo "A distribucions basades en Debian/Ubuntu cal executar:"
    echo "  sudo apt update && sudo apt install -y python3-tk libsndfile1"
    echo "A Fedora:"
    echo "  sudo dnf install python3-tkinter libsndfile"
    echo "A Arch Linux:"
    echo "  sudo pacman -S tk libsndfile"
    exit 1
}

# 4. Instal·lació de dependències si cal
if [ ! -f ".venv/.deps_installed" ]; then
    echo "Instal·lant dependències de requirements.txt..."
    pip install --upgrade pip
    pip install -r requirements.txt
    touch .venv/.deps_installed
    echo "[OK] Dependències instal·lades amb èxit."
fi

# 5. Execució de l'aplicació
echo "Iniciant l'aplicació..."
exec python3 app.py "$@"
