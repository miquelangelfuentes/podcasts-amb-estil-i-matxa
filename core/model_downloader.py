"""
Gestor de Descàrrega de Models i Components (Model Downloader).
Gestiona la descàrrega autònoma, verificació d'integritat, estat local
i memòria cau dels models de Hugging Face:
- BSC-LT/matxa-tts-v2-ca-multiaccent-graphemes
- projecte-aina/alvocat-vocos-22khz
- BSC-LT/styletts2-catalan-multispeaker
"""

import os
import sys
import time
import requests
import shutil
from typing import Callable, Optional, Dict, Any, List

class ModelDownloader:
    """Descàrrega i gestió d'integritat per a models TTS en català."""

    HF_BASE_URL = "https://huggingface.co"

    MODEL_REPOSITORIES = {
        "matxa_tts": {
            "name": "Matxa-TTS v2 multiaccent (100% Offline)",
            "provider": "BSC-LT",
            "repo_id": "BSC-LT/matxa-tts-v2-ca-multiaccent-graphemes",
            "files": {
                "matxa_v2_multiaccent_graphemes_20_steps_wavenext.onnx": "matxa_v2_multiaccent_graphemes_20_steps_wavenext.onnx"
            },
            "desc": "Model neuronal autònom amb 16 veus per a totes les variants dialectals. No requereix internet.",
            "expected_size_mb": 260.17,
            "category": "Motor autònom principal (Offline)",
            "is_cloud": False
        },
        "alvocat_vocos": {
            "name": "Vocoder alVoCat 22kHz (100% Offline)",
            "provider": "Projecte AINA",
            "repo_id": "projecte-aina/alvocat-vocos-22khz",
            "files": {
                "mel_spec_22khz_cat.onnx": "mel_spec_22khz_cat.onnx"
            },
            "desc": "Vocoder neuronal d'alta fidelitat acústica a 22.050 Hz i normalització lingüística AINA.",
            "expected_size_mb": 51.2,
            "category": "Vocoder essencial (Offline)",
            "is_cloud": False
        },
        "styletts2_ca": {
            "name": "StyleTTS 2 Català (BSC-LT Checkpoint 2.05 GB)",
            "provider": "BSC-LT",
            "repo_id": "BSC-LT/styletts2-catalan-multispeaker",
            "files": {
                "epoch_2nd_00070.pth": "epoch_2nd_00070.pth",
                "config.yml": "config.yml"
            },
            "desc": "Checkpoint PyTorch complet de difusió neuronal del BSC-LT (~2,05 GB). Descarrega el model complet a disc.",
            "expected_size_mb": 2050.1,
            "category": "Model complet (PyTorch 2.05 GB)",
            "is_cloud": False
        },
        "edge_tts_cloud": {
            "name": "Microsoft Neural ca-ES (Online)",
            "provider": "Microsoft Edge Cloud",
            "repo_id": "microsoft/edge-tts-catalan",
            "files": {},
            "desc": "Servei de veus Joana i Enric al núvol. No requereix espai a disc; requereix connexió a internet.",
            "expected_size_mb": 0.0,
            "category": "Servei al núvol (Online)",
            "is_cloud": True
        }
    }

    def __init__(self, cache_dir: Optional[str] = None):
        if cache_dir:
            self.cache_dir = os.path.abspath(cache_dir)
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.cache_dir = os.path.join(base_dir, "models")
        os.makedirs(self.cache_dir, exist_ok=True)
        self._cancel_requested = False

    def cancel_download(self):
        """Sol·licita la cancel·lació de la descàrrega en curs."""
        self._cancel_requested = True

    def get_model_path(self, model_key: str, filename: str) -> str:
        """Retorna la ruta local on s'espera trobar el fitxer del model."""
        return os.path.join(self.cache_dir, model_key, filename)

    def is_model_downloaded(self, model_key: str) -> bool:
        """Comprova si tots els fitxers d'un model estan presents localment."""
        if model_key not in self.MODEL_REPOSITORIES:
            return False
        model_info = self.MODEL_REPOSITORIES[model_key]
        for local_file in model_info["files"].values():
            full_path = self.get_model_path(model_key, local_file)
            if not os.path.exists(full_path) or os.path.getsize(full_path) == 0:
                return False
        return True

    def get_component_status(self, model_key: str) -> Dict[str, Any]:
        """Obté l'estat detallat d'un component per a la interfície d'usuari."""
        if model_key not in self.MODEL_REPOSITORIES:
            raise ValueError(f"Model desconegut: {model_key}")

        info = self.MODEL_REPOSITORIES[model_key]
        total_installed_bytes = 0
        files_detail = []
        is_complete = True

        for remote_name, local_file in info["files"].items():
            path = self.get_model_path(model_key, local_file)
            exists = os.path.exists(path)
            size = os.path.getsize(path) if exists else 0
            total_installed_bytes += size
            if not exists or size == 0:
                is_complete = False
            files_detail.append({
                "remote_name": remote_name,
                "local_file": local_file,
                "path": path,
                "exists": exists,
                "size_bytes": size,
                "size_mb": round(size / (1024 * 1024), 2)
            })

        installed_mb = round(total_installed_bytes / (1024 * 1024), 2)
        return {
            "key": model_key,
            "name": info["name"],
            "provider": info["provider"],
            "desc": info["desc"],
            "category": info["category"],
            "repo_id": info["repo_id"],
            "expected_size_mb": info["expected_size_mb"],
            "installed_size_mb": installed_mb,
            "is_installed": is_complete,
            "is_cloud": info.get("is_cloud", False),
            "files": files_detail
        }

    def get_all_components_status(self) -> Dict[str, Dict[str, Any]]:
        """Retorna l'estat de tots els components registrats."""
        return {key: self.get_component_status(key) for key in self.MODEL_REPOSITORIES}

    def delete_component(self, model_key: str) -> bool:
        """Elimina els fitxers d'un model per alliberar espai de disc."""
        if model_key not in self.MODEL_REPOSITORIES:
            return False
        model_dir = os.path.join(self.cache_dir, model_key)
        if os.path.exists(model_dir):
            try:
                shutil.rmtree(model_dir, ignore_errors=True)
                return not os.path.exists(model_dir)
            except Exception as e:
                print(f"Error eliminant component {model_key}: {e}")
                return False
        return True

    def download_file(self, url: str, destination_path: str, progress_callback: Optional[Callable[[int, int, str, float], None]] = None) -> bool:
        """
        Descarrega un fitxer via HTTP amb suport de represa, velocitat i cancel·lació.
        Callback signature: progress_callback(downloaded_bytes, total_bytes, filename, speed_mb_s)
        """
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        temp_dest = destination_path + ".tmp"
        self._cancel_requested = False

        headers = {
            "User-Agent": "PodcastsAmbEstilIMatxa/1.0"
        }

        downloaded_bytes = 0
        if os.path.exists(temp_dest):
            downloaded_bytes = os.path.getsize(temp_dest)
            headers["Range"] = f"bytes={downloaded_bytes}-"

        start_time = time.time()
        last_time = start_time
        bytes_since_last = 0
        speed_mb_s = 0.0

        try:
            with requests.get(url, headers=headers, stream=True, timeout=30) as response:
                if response.status_code == 416: # Range not satisfiable
                    headers.pop("Range", None)
                    downloaded_bytes = 0
                    response = requests.get(url, headers=headers, stream=True, timeout=30)

                response.raise_for_status()

                total_size = int(response.headers.get("content-length", 0)) + downloaded_bytes
                mode = "ab" if downloaded_bytes > 0 else "wb"

                chunk_size = 512 * 1024 # 512 KB per bloc
                with open(temp_dest, mode) as f:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if self._cancel_requested:
                            return False
                        if chunk:
                            f.write(chunk)
                            downloaded_bytes += len(chunk)
                            bytes_since_last += len(chunk)

                            now = time.time()
                            if now - last_time >= 0.5:
                                speed_mb_s = (bytes_since_last / (now - last_time)) / (1024 * 1024)
                                bytes_since_last = 0
                                last_time = now

                                if progress_callback:
                                    progress_callback(downloaded_bytes, total_size, os.path.basename(destination_path), speed_mb_s)

            if self._cancel_requested:
                return False

            if os.path.exists(destination_path):
                os.remove(destination_path)
            os.rename(temp_dest, destination_path)

            if progress_callback:
                progress_callback(total_size, total_size, os.path.basename(destination_path), 0.0)
            return True

        except Exception as e:
            if progress_callback:
                progress_callback(-1, -1, f"Error: {e}", 0.0)
            return False

    def download_model(self, model_key: str, progress_callback: Optional[Callable[[int, int, str, float], None]] = None) -> bool:
        """Descarrega tots els fitxers d'un repositori de model."""
        if model_key not in self.MODEL_REPOSITORIES:
            raise ValueError(f"Model desconegut: {model_key}")

        model_info = self.MODEL_REPOSITORIES[model_key]
        repo_id = model_info["repo_id"]

        for hf_file, local_file in model_info["files"].items():
            dest_path = self.get_model_path(model_key, local_file)
            if os.path.exists(dest_path) and os.path.getsize(dest_path) > 0:
                continue

            url = f"{self.HF_BASE_URL}/{repo_id}/resolve/main/{hf_file}"
            success = self.download_file(url, dest_path, progress_callback=progress_callback)
            if not success:
                return False

        return True
