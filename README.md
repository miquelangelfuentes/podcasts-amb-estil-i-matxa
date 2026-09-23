# 🎙️ Pòdcasts amb Estil i Matxa

> **Aplicació d'escriptori autònoma per a Windows de creació de pòdcasts en català d'1, 2 o 3 veus en local i sense límit de durada.**  
> Dissenyada per a materials educatius, formatius i divulgatius.  
> Estètica moderna i elegant en tons verd pastel cerimonial inspirada en el **te matxa**.

---

## 🌟 Característiques principals

- **Estructura flexible d'1, 2 o 3 veus**:
  - **1 veu (monòleg)**: Càpsules didàctiques i explicacions amb la Veu presentadora al centre (`pan=0%`).
  - **2 veus (diàleg)**: Converses i entrevistes naturals entre dues veus interlocutores (`-25%` i `+25%`, sense presentador).
  - **3 veus (tertúlia)**: Taules rodones amb Veu presentadora al centre (`pan=0%`) i dues veus col·laboradores als laterals (`-25%` i `+25%`).
- **Sense límit de durada**: Genera des de càpsules breus de 2 minuts fins a lliçons o debats de 30-60 minuts gràcies a la síntesi per blocs oracionals.
- **100% local i privat**: No envia cap dada ni text a internet. Apte per a escoles, instituts i universitats (privadesa total per a docents i alumnat).
- **Models de llengua oberts de Catalunya**:
  - **`BSC-LT/StyleTTS2-Catalan`**: Model neuronal basat en difusió d'estil i alta expressivitat, amb suport per a clonació de veu zero-shot (motor per defecte).
  - **`BSC-LT/Matxa-TTS-v2-Multiaccent`**: Model acústic d'última generació basat en transport òptim i flow matching, amb 16 variants dialectals del català (central, balear, valencià, nord-occidental i septentrional).
  - **`projecte-aina/alvocat-vocos-22khz`**: Vocoder neuronal Vocos i normalitzador desenvolupat en el marc del Projecte AINA.
- **Clonació de veu zero-shot**: Clona la veu de qualsevol docent aportant una petita mostra d'àudio (5-15 segons).
- **Mostres instantànies de veu (0 ms)**: Escolta en directe qualsevol veu catalana amb el botó `▶ Escolta`.
- **Masterització d'estudi i exportació MP3**:
  - Espacialització estèreo (*panning*) per posicionar cada veu a l'estudi sonor.
  - Normalització de sonoritat d'emissió segons l'estàndard **EBU R128 (-16 LUFS)**.
  - Exportació directa a **MP3 estèreo a 160 kbps CBR** (màxima fidelitat per a 22,05 kHz).
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
│   └── 📄 audio_processor.py     # Panning estèreo, LUFS i exportació MP3 160k
├── 📁 ui/                        # Interfície d'usuari (CustomTkinter)
│   ├── 📄 theme.py               # Paleta de colors Te Matxa Pastel
│   ├── 📄 main_window.py         # Finestra principal amb editor i selecció d'1, 2 o 3 veus
│   ├── 📄 voice_clone_modal.py   # Modal per a clonació de veu zero-shot
│   └── 📄 player_widget.py       # Reproductor d'àudio i exportador MP3
├── 📁 docs/                      # Guies i documentació
│   ├── 📄 GUIA_PROMPT_LLM.md     # Indicació per a models de llenguatge (ChatGPT/Claude/Gemini)
│   └── 📄 GUIA_SSML_CATALA.md    # Manual d'opcions SSML i fonètica en català
├── 📁 examples/                  # Recursos didàctics
│   ├── 📄 guio_exemple_5min.txt  # Guió formatiu complet de 5 minuts
│   ├── 📄 plantilla_1veu.txt     # Plantilla d'1 veu (monòleg amb Veu presentadora)
│   ├── 📄 plantilla_2veus.txt    # Plantilla de 2 veus (diàleg sense presentador)
│   └── 📄 plantilla_3veus.txt    # Plantilla de 3 veus (tertúlia amb Veu presentadora)
├── 📁 assets/                    # Icona cerimonial de te matxa (ICO i PNG)
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

L'aplicació inclou un gestor visual integrat accessible des del botó **`📦 Models`** de la barra superior. Aquest mòdul permet a qualsevol usuari:
- **Comprovar l'estat**: Saber a l'instant quins models neuronals estan instal·lats localment i quant d'espai ocupen.
- **Descarregar per separat**: Obtenir directament des d'Hugging Face cadascun dels components:
  - **Vocoder alVoCat** (~51 MB)
  - **Matxa-TTS v2 multiaccent** (~260 MB)
  - **StyleTTS 2 Català**
- **Verificar la integritat o alliberar espai** amb un sol clic.

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
