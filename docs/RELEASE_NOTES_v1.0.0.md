# Pòdcasts amb Matxa (versió 1.0.0) 🎙️🍵

Versió inicial de **Pòdcasts amb Matxa**, l'estudi d'escriptori autònom per a la creació i locució de guions de pòdcast en català amb intel·ligència artificial. Aquesta compilació substitueix la versió 1.0.0 inicial i incorpora totes les darreres millores.

### ✨ Novetats i funcionalitats destacades
- **Motors de síntesi de veu catalana d'última generació**:
  - **Matxa-TTS v2 multiaccent (100% Offline)**: suport complet per a totes les variants dialectals (balear, central, nord-occidental, septentrional i valencià) combinat amb el vocoder neuronal **alVoCat**.
  - **Veus neuronals expressives (Online)**: locució natural amb 9 veus catalanes (`ona`, `pau`, `bet`, `jordi`, `teia`, `pere`, `lluc`, `joana`, `enric`).
  - **Microsoft Neural ca-ES (Online)**: integració al núvol per a síntesi ràpida amb les veus Joana i Enric.
- **Gestor integrat de components i models (📦 Models)**:
  - Descàrrega autònoma i modular dels pesos dels models des d'Hugging Face directament des de l'aplicació.
  - Comprovació automàtica de la instal·lació, velocitat de descàrrega en temps real (MB/s), represa automàtica de descàrregues i alliberament d'espai en disc.
  - Eina **«Comprovar el meu equip»** amb diagnòstic automàtic de maquinari (CPU, GPU, RAM, disc i suport AVX2).
  - Guia pedagògica **«Què implica instal·lar-ho tot?»** per resoldre dubtes d'independència tecnològica i privadesa.
- **Estudi de guió interactiu**:
  - Reproductor d'àudio integrat amb forma d'ona (*waveform*), controls de navegació i exportació a MP3 (160 kbps CBR).
  - Suport per a 1 veu (monòleg), 2 veus (diàleg) i 3 veus (tertúlia amb presentador) amb espacialització estèreo (*panning*) i masterització EBU R128 (-16 LUFS).
  - Guia de síntesi de veu i fonètica en català, i plantilla d'indicacions per a models de llenguatge (LLM).
- **Pista de música o ambientació sonora de fons**:
  - Selector de fitxers d'àudio compatibles (MP3, WAV, OGG, FLAC) per a sintonia d'obertura o ambientació general.
  - Reproducció automàtica en bucle continu (*loop*) amb transició suau (*cross-fade* de 20 ms) per evitar salts sobtats.
  - Regulador de volum en percentatge (predeterminat al 15% per no emmascarar la veu) amb botó d'escolta de prova instantània (`▶ Prova` / `■ Atura`).
  - Mescla final amb esvaïment d'entrada (*fade-in* d'1 s) i de sortida (*fade-out* de 2 s), combinat amb limitador de pic i masterització EBU R128 (-16 LUFS).
- **Interfície responsiva**:
  - Resolució adaptativa optimitzada per a escalat DPI de Windows (125% - 150%) amb panell d'àudio permanentment ancorat a la base.
- **Paquet binari autònom per a Windows**:
  - Aplicació d'escriptori directa en fitxer ZIP (`PodcastsAmbEstilIMatxa-v1.0.0-Windows.zip`) sense necessitat de configurar entorns de Python.

---
*Creat mitjançant codificació per intencions amb Google Antigravity per Miquel Àngel Fuentes.*
