"""
Script de Compilació Automatitzada a Executable Windows (.exe).
Utilitza PyInstaller per crear un paquet independent i autònom
amb l'aplicació 'Pòdcasts amb Matxa'.
"""

import os
import sys
import shutil
import subprocess
import time
import zipfile

from ui.version_check_modal import APP_VERSION

def build():
    print("=" * 60)
    print("  Iniciant compilació de 'Pòdcasts amb Matxa' (.exe)")
    print("=" * 60)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    dist_dir = os.path.join(base_dir, "dist")
    build_dir = os.path.join(base_dir, "build")
    icon_path = os.path.join(base_dir, "assets", "icon.ico")

    # Tancar instancies previes obertes a Windows per alliberar bloquejos de fitxers
    if sys.platform == "win32":
        for exe in ["PodcastsAmbMatxa.exe", "PodcastsAmbEstilIMatxa.exe", "MatxaIEstil.exe", "PodcastsAmbStyleTTS.exe"]:
            try:
                subprocess.run(["taskkill", "/F", "/IM", exe], capture_output=True)
            except Exception:
                pass
        time.sleep(2)

    # Neteja preventiva del directori destí amb reintents
    target_dist = os.path.join(dist_dir, "PodcastsAmbMatxa")
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
        "--name=PodcastsAmbMatxa",
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
        f"--add-data={os.path.join(os.path.dirname(__import__('piper').__file__), 'espeak-ng-data')};piper/espeak-ng-data",
        # Recollida de mòduls essencials amb binaris
        "--collect-all=customtkinter",
        "--collect-all=imageio_ffmpeg",
        "--collect-all=soundfile",
        "--collect-all=edge_tts",
        "--collect-all=pyttsx3",
        "--collect-all=piper",
        "--collect-all=pathvalidate",
        "--exclude-module=piper.train",
        "--exclude-module=torch",
        # Imports ocults per a àudio i xarxa
        "--hidden-import=piper",
        "--hidden-import=piper.voice",
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

    def robust_copy(src, dst):
        """Còpia segura de directoris que gestiona rutes llargues a Windows (MAX_PATH)."""
        if sys.platform == "win32":
            subprocess.run(["robocopy", src, dst, "/MIR", "/R:2", "/W:1", "/NP"], check=False)
        else:
            shutil.copytree(src, dst, dirs_exist_ok=True)

    result = subprocess.run(cmd, cwd=base_dir)
    if result.returncode == 0:
        built_dir = os.path.join(staging_dist, "PodcastsAmbMatxa")
        new_dist = os.path.join(dist_dir, "PodcastsAmbMatxa")
        os.makedirs(new_dist, exist_ok=True)
        print(f"\nCopiant fitxers generats a {new_dist}...")
        robust_copy(built_dir, new_dist)

        exe_path = os.path.join(new_dist, "PodcastsAmbMatxa.exe")
        print("\n" + "=" * 60)
        print("  [OK] Compilació de PodcastsAmbMatxa COMPLETADA AMB ÈXIT!")
        print(f"  Executable generat a:")
        print(f"  {exe_path}")

        # Sincronitzar amb dist/PodcastsAmbEstilIMatxa, dist/MatxaIEstil i dist/PodcastsAmbStyleTTS per als accessos directes existents de l'usuari
        for alias_name, alias_exe in [
            ("PodcastsAmbEstilIMatxa", "PodcastsAmbEstilIMatxa.exe"),
            ("MatxaIEstil", "MatxaIEstil.exe"),
            ("PodcastsAmbStyleTTS", "PodcastsAmbStyleTTS.exe")
        ]:
            alias_dist = os.path.join(dist_dir, alias_name)
            try:
                print(f"\n  Sincronitzant versió actualitzada a dist/{alias_name}...")
                os.makedirs(alias_dist, exist_ok=True)
                robust_copy(built_dir, alias_dist)
                dest_exe = os.path.join(alias_dist, alias_exe)
                orig_in_copy = os.path.join(alias_dist, "PodcastsAmbMatxa.exe")
                if os.path.exists(orig_in_copy):
                    shutil.copy2(orig_in_copy, dest_exe)
                print(f"  [OK] Executable de compatibilitat generat a:")
                print(f"  {dest_exe}")
            except Exception as e:
                print(f"  [AVÍS] Error sincronitzant dist/{alias_name}: {e}")

        # Empaquetar a fitxer ZIP oficial amb el nom de la versió actual
        zip_name = f"PodcastsAmbMatxa-v{APP_VERSION}-Windows.zip"
        zip_path = os.path.join(dist_dir, zip_name)
        print(f"\n  Empaquetant a arxiu comprimit oficial: {zip_name}...")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(new_dist):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, dist_dir)
                    zipf.write(full_path, rel_path)
        zip_mb = os.path.getsize(zip_path) / (1024 * 1024)
        print(f"  [OK] Fitxer ZIP generat amb èxit ({zip_mb:.1f} MB):")
        print(f"  {zip_path}")

        # Generar còpia de compatibilitat de l'arxiu ZIP amb l'antic nom
        legacy_zip = os.path.join(dist_dir, f"PodcastsAmbEstilIMatxa-v{APP_VERSION}-Windows.zip")
        try:
            shutil.copy2(zip_path, legacy_zip)
        except Exception:
            pass

        # Sincronitzar còpia directa al directori Downloads de l'usuari si existeix
        user_downloads = os.path.join(os.path.expanduser("~"), "Downloads")
        if os.path.exists(user_downloads):
            try:
                dest_zip_downloads = os.path.join(user_downloads, zip_name)
                shutil.copy2(zip_path, dest_zip_downloads)
                print(f"  [OK] Còpia de descàrrega sincronitzada a: {dest_zip_downloads}")
                # Sincronitzar també la carpeta extreta per a execució immediata
                unzipped_target = os.path.join(user_downloads, f"PodcastsAmbMatxa-v{APP_VERSION}-Windows", "PodcastsAmbMatxa")
                if os.path.exists(os.path.dirname(unzipped_target)):
                    robust_copy(new_dist, unzipped_target)
                    print(f"  [OK] Carpeta d'execució extreta actualitzada a: {unzipped_target}")
            except Exception as e:
                print(f"  [AVÍS] No s'ha pogut copiar a Downloads: {e}")

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
