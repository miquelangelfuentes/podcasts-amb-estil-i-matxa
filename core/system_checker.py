"""
Mòdul de Comprovació de Requisits del Sistema (System Checker).
Analitza el maquinari local (disc dur, memòria RAM, processador, GPU i connectivitat)
per validar la idoneïtat de l'ordinador per a la síntesi de veu neuronal 100% offline.
"""

import os
import sys
import shutil
import platform
from typing import Dict, Any, List

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    import onnxruntime as ort
    HAS_ONNX = True
except ImportError:
    HAS_ONNX = False


class SystemChecker:
    """Diagnòstic de compatibilitat del maquinari per a síntesi de veu local."""

    @staticmethod
    def check_disk(target_path: str = ".") -> Dict[str, Any]:
        """Comprova l'espai lliure a la unitat de disc de l'aplicació."""
        try:
            abs_path = os.path.abspath(target_path)
            # A Windows, cercar l'arrel de la unitat si no existeix
            while not os.path.exists(abs_path) and os.path.dirname(abs_path) != abs_path:
                abs_path = os.path.dirname(abs_path)

            usage = shutil.disk_usage(abs_path)
            free_gb = round(usage.free / (1024 ** 3), 2)
            total_gb = round(usage.total / (1024 ** 3), 2)

            # Requisits: Matxa-TTS, alVoCat i UPC Ona ocupen ~370 MB en total
            if free_gb >= 2.0:
                status = "ok"
                msg = f"{free_gb} GB lliures de {total_gb} GB (Més que suficient per instal·lar tots els models autònoms)"
            elif free_gb >= 1.0:
                status = "ok"
                msg = f"{free_gb} GB lliures de {total_gb} GB (Suficient per a la síntesi autònoma Matxa-TTS v2 i alVoCat)"
            elif free_gb >= 0.5:
                status = "warning"
                msg = f"{free_gb} GB lliures de {total_gb} GB (Espai ajustat per als models bàsics; es recomana alliberar espai)"
            else:
                status = "error"
                msg = f"{free_gb} GB lliures de {total_gb} GB (Molt poc espai, cal un mínim de 500 MB lliures)"

            return {
                "name": "Espai en disc",
                "status": status,
                "value": f"{free_gb} GB lliures",
                "details": msg,
                "free_gb": free_gb
            }
        except Exception as e:
            return {
                "name": "Espai en disc",
                "status": "warning",
                "value": "Desconegut",
                "details": f"No s'ha pogut calcular l'espai: {e}",
                "free_gb": 0.0
            }

    @staticmethod
    def check_ram() -> Dict[str, Any]:
        """Mesura la memòria RAM física total i disponible mitjançant l'API de Windows o psutil."""
        total_gb = 0.0
        avail_gb = 0.0

        if sys.platform == "win32":
            try:
                import ctypes
                class MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [
                        ('dwLength', ctypes.c_ulong),
                        ('dwMemoryLoad', ctypes.c_ulong),
                        ('ullTotalPhys', ctypes.c_ulonglong),
                        ('ullAvailPhys', ctypes.c_ulonglong),
                        ('ullTotalPageFile', ctypes.c_ulonglong),
                        ('ullAvailPageFile', ctypes.c_ulonglong),
                        ('ullTotalVirtual', ctypes.c_ulonglong),
                        ('ullAvailVirtual', ctypes.c_ulonglong),
                        ('ullAvailExtendedVirtual', ctypes.c_ulonglong),
                    ]

                stat = MEMORYSTATUSEX()
                stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
                if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
                    total_gb = round(stat.ullTotalPhys / (1024 ** 3), 2)
                    avail_gb = round(stat.ullAvailPhys / (1024 ** 3), 2)
            except Exception:
                pass
        elif os.path.exists("/proc/meminfo"):
            try:
                meminfo = {}
                with open("/proc/meminfo", "r", encoding="utf-8") as f:
                    for line in f:
                        parts = line.split(":")
                        if len(parts) == 2:
                            meminfo[parts[0].strip()] = parts[1].strip()
                if "MemTotal" in meminfo:
                    kb_total = float(meminfo["MemTotal"].split()[0])
                    total_gb = round(kb_total / (1024 ** 2), 2)
                if "MemAvailable" in meminfo:
                    kb_avail = float(meminfo["MemAvailable"].split()[0])
                    avail_gb = round(kb_avail / (1024 ** 2), 2)
            except Exception:
                pass

        if total_gb == 0.0:
            try:
                import psutil
                mem = psutil.virtual_memory()
                total_gb = round(mem.total / (1024 ** 3), 2)
                avail_gb = round(mem.available / (1024 ** 3), 2)
            except Exception:
                pass

        if total_gb > 0:
            if total_gb >= 7.5 and avail_gb >= 1.5:
                status = "ok"
                msg = f"{total_gb} GB totals ({avail_gb} GB disponibles). Excel·lent per carregar el model a memòria."
            elif total_gb >= 3.5 and avail_gb >= 0.8:
                status = "ok"
                msg = f"{total_gb} GB totals ({avail_gb} GB disponibles). Apte per a síntesi per CPU."
            elif avail_gb >= 0.4:
                status = "warning"
                msg = f"{total_gb} GB totals ({avail_gb} GB disponibles). Memòria justa; es recomana tancar altres programes."
            else:
                status = "error"
                msg = f"{total_gb} GB totals ({avail_gb} GB disponibles). Memòria disponible molt baixa per a inferència."
            val_str = f"{total_gb} GB ({avail_gb} GB lliures)"
        else:
            status = "ok"
            val_str = "No determinable"
            msg = "No s'ha pogut llegir la memòria física directament, es continuarà igualment."

        return {
            "name": "Memòria RAM",
            "status": status,
            "value": val_str,
            "details": msg,
            "total_gb": total_gb,
            "avail_gb": avail_gb
        }

    @staticmethod
    def check_cpu() -> Dict[str, Any]:
        """Comprova el processador i el nombre de nuclis de càlcul."""
        cores = os.cpu_count() or 2
        arch = platform.machine()
        proc_name = platform.processor() or "Processador compatible"

        # Neteja de cadenes llargues de nom del processador
        if len(proc_name) > 40:
            proc_name = proc_name[:37] + "..."

        if cores >= 4:
            status = "ok"
            msg = f"{cores} nuclis lògics ({arch}). Molt bona velocitat de síntesi per blocs."
        elif cores >= 2:
            status = "ok"
            msg = f"{cores} nuclis lògics ({arch}). Velocitat adequada per a generació de podcasts."
        else:
            status = "warning"
            msg = f"{cores} sol nucli. La síntesi pot ser més pausada."

        return {
            "name": "Processador (CPU)",
            "status": status,
            "value": f"{cores} nuclis ({arch})",
            "details": f"{proc_name} — {msg}",
            "cores": cores
        }

    @staticmethod
    def check_gpu() -> Dict[str, Any]:
        """Detecta si hi ha targeta gràfica dedicada o acceleració per maquinari."""
        gpu_name = "Inferència per CPU (Ràpida i universal)"
        has_accel = False
        providers = []

        if HAS_ONNX:
            try:
                avail = ort.get_available_providers()
                if "CUDAExecutionProvider" in avail:
                    gpu_name = "NVIDIA CUDA (Acceleració màxima per GPU)"
                    has_accel = True
                elif "DmlExecutionProvider" in avail:
                    gpu_name = "DirectML (Acceleració gràfica de Windows)"
                    has_accel = True
                providers = avail
            except Exception:
                pass

        return {
            "name": "Acceleració gràfica (GPU)",
            "status": "ok",
            "value": "GPU activa" if has_accel else "CPU estàndard",
            "details": f"{gpu_name}. Els models Matxa i alVoCat estan optimitzats tant per a CPU moderna com per a GPU.",
            "has_acceleration": has_accel,
            "providers": providers
        }

    @staticmethod
    def check_internet() -> Dict[str, Any]:
        """Comprova si hi ha connexió activa a Hugging Face per a la descàrrega inicial."""
        if not HAS_REQUESTS:
            return {
                "name": "Connexió (Hugging Face)",
                "status": "warning",
                "value": "No comprovat",
                "details": "Mòdul de xarxa no disponible.",
                "online": False
            }

        try:
            try:
                resp = requests.head("https://huggingface.co", timeout=2.5, verify=True)
            except requests.exceptions.SSLError:
                import urllib3
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                resp = requests.head("https://huggingface.co", timeout=2.5, verify=False)
            if resp.status_code < 400:
                return {
                    "name": "Connexió a Hugging Face",
                    "status": "ok",
                    "value": "Connexió operativa",
                    "details": "Pots descarregar o reinstal·lar models oficials amb un sol clic.",
                    "online": True
                }
            else:
                return {
                    "name": "Connexió a Hugging Face",
                    "status": "warning",
                    "value": f"Codi {resp.status_code}",
                    "details": "El servidor respon amb avís. Si ja tens els models instal·lats, pots treballar 100% offline.",
                    "online": False
                }
        except Exception:
            return {
                "name": "Connexió a Hugging Face",
                "status": "warning",
                "value": "Sense connexió",
                "details": "Mode fora de línia. Si els models ja estan instal·lats, funcionarà al 100% de manera autònoma.",
                "online": False
            }

    @classmethod
    def run_full_diagnostic(cls, target_path: str = ".") -> Dict[str, Any]:
        """Executa l'anàlisi completa del sistema i retorna un veredicte consolidat."""
        disk = cls.check_disk(target_path)
        ram = cls.check_ram()
        cpu = cls.check_cpu()
        gpu = cls.check_gpu()
        net = cls.check_internet()

        checks = [disk, ram, cpu, gpu, net]

        # Càlcul del veredicte general
        has_error = any(c["status"] == "error" for c in checks)
        has_warning = any(c["status"] == "warning" for c in checks)

        if has_error:
            overall = "error"
            title = "⚠️ L'equip presenta limitacions que poden afectar el rendiment"
            summary = "Revisa l'espai a disc o allibera memòria RAM abans de generar pòdcasts llargs."
        elif has_warning:
            overall = "warning"
            title = "👍 L'equip és apte per a síntesi de veu local"
            summary = "El teu ordinador pot sintetitzar pòdcasts en català de forma autònoma i sense problemes."
        else:
            overall = "ok"
            title = "✨ L'equip compleix de forma excel·lent tots els requisits"
            summary = "Maquinari òptim per a síntesi de veu neuronal d'alta fidelitat 100% offline."

        return {
            "overall_status": overall,
            "overall_title": title,
            "overall_summary": summary,
            "checks": checks
        }
