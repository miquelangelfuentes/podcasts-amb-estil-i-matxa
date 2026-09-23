<p align="center">
  <img src="assets/banner.png" alt="Pòdcasts amb Estil i Matxa" width="100%">
</p>

# 🎙️ Pòdcasts amb Estil i Matxa

> **Aplicació d'escriptori autònoma per a Windows de creació de pòdcasts en català d'una, dues o tres veus, en local i sense límit de durada.**  
> Dissenyada per a materials educatius, formatius i divulgatius.  

---

## 📥 Descarrega directa per a Windows (.exe)

Per utilitzar l'aplicació a Windows **sense necessitat d'instal·lar Python ni compilar**:
1. Descarrega el paquet complet de la darrera versió:
   👉 **[Descarregar PodcastsAmbEstilIMatxa-v1.0.0-Windows.zip](https://github.com/miquelangelfuentes/podcasts-amb-estil-i-matxa/releases/download/v1.0.0/PodcastsAmbEstilIMatxa-v1.0.0-Windows.zip)** (~397 MB)
2. Descomprimeix el fitxer ZIP en una carpeta del teu ordinador.
3. Executa directament `PodcastsAmbEstilIMatxa.exe`.
4. A la barra superior, fes clic a **`📦 Models`** per descarregar els models de síntesi de veu des d'Hugging Face amb un sol clic.

---

## 🌟 Característiques principals

- **Estructura flexible d'1, 2 o 3 veus**:
  - **1 veu (monòleg)**: Càpsules didàctiques i explicacions amb la Veu presentadora al centre (`pan=0%`).
  - **2 veus (diàleg)**: Converses i entrevistes naturals entre dues veus interlocutores (`-25%` i `+25%`, sense presentador).
  - **3 veus (tertúlia)**: Taules rodones amb Veu presentadora al centre (`pan=0%`) i dues veus col·laboradores als laterals (`-25%` i `+25%`).
- **Sense límit de durada**: Genera des de càpsules breus de 2 minuts fins a lliçons o debats de 30-60 minuts gràcies a la síntesi per blocs oracionals.
- **100% local i privat**: No envia cap dada ni text a internet. Apte per a escoles, instituts i universitats (privadesa total per a docents i alumnat).
- **Models de llengua oberts de Catalunya**:
  - **`BSC-LT/Matxa-TTS-v2-Multiaccent`**: Model acústic d'última generació basat en transport òptim i flow matching (100% offline), amb 16 variants dialectals del català (central, balear, valencià, nord-occidental i septentrional).
  - **`BSC-LT/StyleTTS2-Catalan`**: Model neuronal basat en difusió d'estil i alta expressivitat, amb 9 veus i suport per a clonació de veu zero-shot.
  - **`projecte-aina/alvocat-vocos-22khz`**: Vocoder neuronal Vocos i normalitzador desenvolupat en el marc del Projecte AINA (100% offline).
  - **`Microsoft Neural ca-ES (Online)`**: Servei al núvol integrat opcionalment per a síntesi ràpida (veus Joana i Enric).
- **Selector directe de motor**: Canvi immediat entre Matxa-TTS v2 (offline), StyleTTS 2 (offline) i Microsoft Neural (online) des de la capçalera del panell de locutors.
- **Clonació de veu zero-shot**: Clona la veu de qualsevol persona aportant una petita mostra d'àudio en format WAV (5-15 segons).
- **Mostres instantànies de veu (0 ms)**: Escolta en directe qualsevol veu catalana amb el botó `▶ Escolta`.
- **Masterització d'estudi i exportació MP3**:
  - Espacialització estèreo (*panning*) per posicionar cada veu a l'estudi sonor.
  - Normalització de sonoritat d'emissió segons l'estàndard **EBU R128 (-16 LUFS)**.
  - Exportació directa a **MP3 estèreo a 160 kbps CBR** (màxima fidelitat per a 22,05 kHz).
- **Interfície responsiva i adaptativa**: Suport complet per a escalat DPI a Windows (125% i 150%) amb reproductor d'àudio ancorat a la base i controls desplaçables.
- **Executable independent per a Windows**: Distribució autònoma en fitxer `.exe`.

---

## 📂 Estructura del projecte

```
📁 Antigravity/
├── 📄 app.py                     # Punt d'entrada de l'aplicació
├── 📁 core/                      # Motors de processament
│   ├── 📄 script_parser.py       # Analitzador sintàctic del guió .txt
│   ├── 📄 text_normalizer.py     # Normalitzador lingüístic en català (alVoCat)
│   ├── 📄 matxa_tts_engine.py    # Motor Matxa-TTS v2 multiaccent (BSC-LT)
│   ├── 📄 tts_engine.py          # Motor StyleTTS 2 i clonació de veu
│   ├── 📄 vocoder_alvocat.py     # Vocoder neural Vocos 22kHz (AINA)
│   ├── 📄 voice_preview.py       # Gestor de mostres i memòria cau d'àudio
│   ├── 📄 audio_processor.py     # Panning estèreo, LUFS i exportació MP3 160k
│   ├── 📄 model_downloader.py    # Gestor de descàrrega asíncrona des d'Hugging Face
│   └── 📄 system_checker.py      # Diagnòstic automàtic de maquinari (CPU, GPU, RAM, disc)
├── 📁 ui/                        # Interfície d'usuari (CustomTkinter)
│   ├── 📄 theme.py               # Paleta de colors Te Matxa Pastel
│   ├── 📄 main_window.py         # Finestra principal amb editor i selecció d'1, 2 o 3 veus
│   ├── 📄 components_modal.py    # Gestor visual de models i comprovació del sistema
│   ├── 📄 voice_clone_modal.py   # Modal per a clonació de veu zero-shot
│   └── 📄 player_widget.py       # Reproductor d'àudio i exportador MP3
├── 📁 docs/                      # Guies i documentació
│   ├── 📄 GUIA_PROMPT_LLM.md     # Indicació per a models de llenguatge (ChatGPT/Claude/Gemini)
│   ├── 📄 GUIA_SSML_CATALA.md    # Manual d'opcions SSML i fonètica en català
│   └── 📄 FITXA_DIVULGACIO_DOCENTS.md # Fitxa pedagògica per a docents i comunitat educativa
├── 📁 examples/                  # Recursos didàctics
│   ├── 📄 guio_exemple_5min.txt  # Guió formatiu complet de 5 minuts
│   ├── 📄 plantilla_1veu.txt     # Plantilla d'1 veu (monòleg amb Veu presentadora)
│   ├── 📄 plantilla_2veus.txt    # Plantilla de 2 veus (diàleg sense presentador)
│   └── 📄 plantilla_3veus.txt    # Plantilla de 3 veus (tertúlia amb Veu presentadora)
├── 📁 assets/                    # Icona cerimonial de te matxa i bàner oficial
├── 📄 build_exe.py               # Script de compilació a .exe amb PyInstaller
├── 📄 build_exe.bat              # Fitxer per compilar amb un sol clic a Windows
├── 📄 run_app.bat                # Llançador directe de l'aplicació
└── 📄 requirements.txt           # Dependències de Python
```

---

## 🚀 Com executar l'aplicació

### Opció 1: Llançament directe (Python)
Fes doble clic a `run_app.bat` o obre una consola PowerShell i executa:
```powershell
py app.py
```

### Opció 2: Compilació a executable Windows (.exe)
Fes doble clic a `build_exe.bat` o executa:
```powershell
py build_exe.py
```
L'executable autònom es generarà a la carpeta `dist/PodcastsAmbEstilIMatxa/PodcastsAmbEstilIMatxa.exe`.

---

## 📦 Gestor de models i components

L'aplicació inclou un centre de control integrat accessible des del botó **`📦 Models`** de la barra superior. Aquest mòdul permet a qualsevol persona usuària:

- **Comprovar l'estat en temps real**: Saber a l'instant quins models neuronals estan instal·lats localment, quant d'espai ocupen en disc i la seva integritat.
- **Descarregar per separat de forma modular**: Obtenir directament des d'Hugging Face cadascun dels components amb suport per a represa automàtica i negociació de certificats SSL:
  - **Vocoder alVoCat 22kHz (100% Offline)** (~51,2 MB): Vocoder neuronal del Projecte AINA d'alta fidelitat acústica a 22.050 Hz i normalització lingüística.
  - **Matxa-TTS v2 multiaccent (100% Offline)** (~260,2 MB): Model acústic autònom en format ONNX amb 16 veus per a totes les variants dialectals del català (balear, central, nord-occidental, septentrional i valencià).
  - **StyleTTS 2 Català (BSC-LT Checkpoint complet)** (~2,05 GB): Checkpoint PyTorch oficial de difusió neuronal del BSC-LT per a locució expressiva d'alta fidelitat i clonació de veu zero-shot.
- **Gestió del servei al núvol (Microsoft Neural ca-ES)**:
  - Permet utilitzar les veus Joana i Enric ocupant 0 MB locals, amb informació transparent sobre la necessitat de connexió a internet, límits de peticions per IP (*rate limiting*) i absència de SLA.
- **Diagnòstic de maquinari («Comprovar el meu equip»)**:
  - Analitza automàticament la CPU, memòria RAM, GPU (DirectML/CUDA), emmagatzematge disponible i compatibilitat amb instruccions AVX2 per determinar amb precisió quins models pot executar el teu ordinador amb fluïdesa.
- **Guia pedagògica («Què implica instal·lar-ho tot?»)**:
  - Resol els dubtes més freqüents sobre l'ús de models locals en format ONNX (independència tecnològica, privadesa absoluta de les dades docents i funcionament sense xarxa).
- **Alliberament d'espai en disc**: Elimina els fitxers d'un model amb un sol clic si necessites recuperar espai.

---

## 🎙️ Com escriure o demanar guions a un model de llenguatge

Pots generar guions en 1 minut copiant la indicació que trobaràs a [`docs/GUIA_PROMPT_LLM.md`](file:///c:/Users/mique/Documents/Antigravity/docs/GUIA_PROMPT_LLM.md) i demanant a la teva eina d'IA preferida (ChatGPT, Gemini, Claude, etc.):

> *«Crea un guió de pòdcast de 5 minuts sobre com funciona l'aplicació utilitzant el format de la guia.»*

---

## 🌐 Publicació a GitHub i distribució

Per distribuir l'aplicació a altres usuaris:
1. **Codi font**: El repositori conté el codi font, la documentació i les plantilles didàctiques. El fitxer `.gitignore` exclou automàticament els fitxers de models binaris pesants (`.onnx`, `.pth`) per mantenir el repositori lleuger i per sota del límit de 100 MB de GitHub.
2. **Releases**: A la secció *Releases* de GitHub, es pot adjuntar l'arxiu ZIP amb l'executable compilat.
3. **Instal·lació de models**: Quan l'usuari final arrenca l'aplicació, el gestor de components (`📦 Models`) li permet descarregar els models neuronals amb facilitat.

---

## 📜 Llicència i crèdits

- **Autoria**: Aplicació creada mitjançant codificació per intencions amb Google Antigravity per Miquel Àngel Fuentes.
- **Llicència de codi**: [AGPL v3](https://www.gnu.org/licenses/agpl-3.0.en.html)
- **Llicència de continguts i materials didàctics**: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.es)
- **Models de veu**: **Barcelona Supercomputing Center (BSC-LT)** i **Projecte AINA**.
