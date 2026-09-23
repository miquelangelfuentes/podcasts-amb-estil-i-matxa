"""
Script de Compilació Automatitzada a Executable Windows (.exe).
Utilitza PyInstaller per crear un paquet independent i autònom
amb l'aplicació 'Pòdcasts amb Estil i Matxa'.
"""

import os
import sys
import shutil
import subprocess

import time

def build():
    print("=" * 60)
    print("  Iniciant compilació de 'Pòdcasts amb Estil i Matxa' (.exe)")
    print("=" * 60)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    dist_dir = os.path.join(base_dir, "dist")
    build_dir = os.path.join(base_dir, "build")
    icon_path = os.path.join(base_dir, "assets", "icon.ico")

    # Tancar instancies previes obertes a Windows per alliberar bloquejos de fitxers
    if sys.platform == "win32":
        for exe in ["PodcastsAmbEstilIMatxa.exe", "MatxaIEstil.exe", "PodcastsAmbStyleTTS.exe"]:
            try:
                subprocess.run(["taskkill", "/F", "/IM", exe], capture_output=True)
            except Exception:
                pass
        time.sleep(2)

    # Neteja preventiva del directori destí amb reintents
    target_dist = os.path.join(dist_dir, "PodcastsAmbEstilIMatxa")
    if os.path.exists(target_dist):
        for _ in range(5):
            try:
                shutil.rmtree(target_dist, ignore_errors=True)
                if not os.path.exists(target_dist):
                    break
            except Exception:
                pass
            time.sleep(1)

    staging_dist = os.path.join(os.environ.get("TEMP", "C:\\Temp"), "pm_stg")
    if os.path.exists(staging_dist):
        shutil.rmtree(staging_dist, ignore_errors=True)

    # Ordre PyInstaller amb el nou nom oficial i sortida a directori staging
    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--name=PodcastsAmbEstilIMatxa",
        "--noconsole",
        "--onedir",
        "--clean",
        "-y",
        f"--icon={icon_path}",
        f"--distpath={staging_dist}",
        # Dades i carpetes de recursos
        f"--add-data={os.path.join(base_dir, 'assets')};assets",
        f"--add-data={os.path.join(base_dir, 'docs')};docs",
        f"--add-data={os.path.join(base_dir, 'examples')};examples",
        f"--add-data={os.path.join(base_dir, 'models')};models",
        # Recollida de mòduls essencials amb binaris
        "--collect-all=customtkinter",
        "--collect-all=imageio_ffmpeg",
        "--collect-all=soundfile",
        "--collect-all=edge_tts",
        "--collect-all=pyttsx3",
        # Imports ocults per a àudio i xarxa
        "--hidden-import=scipy.signal",
        "--hidden-import=scipy.special",
        "--hidden-import=pygame",
        "--hidden-import=onnxruntime",
        "--hidden-import=yaml",
        "--hidden-import=pydub",
        "--hidden-import=requests",
        "--hidden-import=aiohttp",
        "--hidden-import=aiohappyeyeballs",
        "--hidden-import=tabulate",
        "--hidden-import=uuid",
        "--hidden-import=asyncio",
        "--hidden-import=edge_tts",
        "--hidden-import=pyttsx3",
        os.path.join(base_dir, "app.py")
    ]

    print("Executant PyInstaller amb la comanda:")
    print(" ".join(cmd))
    print("-" * 60)

    result = subprocess.run(cmd, cwd=base_dir)
    if result.returncode == 0:
        built_dir = os.path.join(staging_dist, "PodcastsAmbEstilIMatxa")
        new_dist = os.path.join(dist_dir, "PodcastsAmbEstilIMatxa")
        os.makedirs(new_dist, exist_ok=True)
        print(f"\nCopiant fitxers generats a {new_dist}...")
        shutil.copytree(built_dir, new_dist, dirs_exist_ok=True)

        exe_path = os.path.join(new_dist, "PodcastsAmbEstilIMatxa.exe")
        print("\n" + "=" * 60)
        print("  [OK] Compilació de PodcastsAmbEstilIMatxa COMPLETADA AMB ÈXIT!")
        print(f"  Executable generat a:")
        print(f"  {exe_path}")

        # Sincronitzar amb dist/MatxaIEstil i dist/PodcastsAmbStyleTTS per als accessos directes existents de l'usuari
        for alias_name, alias_exe in [
            ("MatxaIEstil", "MatxaIEstil.exe"),
            ("PodcastsAmbStyleTTS", "PodcastsAmbStyleTTS.exe")
        ]:
            alias_dist = os.path.join(dist_dir, alias_name)
            try:
                print(f"\n  Sincronitzant versió actualitzada a dist/{alias_name}...")
                os.makedirs(alias_dist, exist_ok=True)
                shutil.copytree(built_dir, alias_dist, dirs_exist_ok=True)
                dest_exe = os.path.join(alias_dist, alias_exe)
                orig_in_copy = os.path.join(alias_dist, "PodcastsAmbEstilIMatxa.exe")
                if os.path.exists(orig_in_copy):
                    shutil.copy2(orig_in_copy, dest_exe)
                print(f"  [OK] Executable de compatibilitat generat a:")
                print(f"  {dest_exe}")
            except Exception as e:
                print(f"  [AVÍS] Error sincronitzant dist/{alias_name}: {e}")

        # Neteja del directori staging temporal
        try:
            shutil.rmtree(staging_dist, ignore_errors=True)
        except Exception:
            pass

        print("=" * 60)
    else:
        print("\n[ERROR] La compilació ha fallat.")
        sys.exit(result.returncode)

if __name__ == "__main__":
    build()
