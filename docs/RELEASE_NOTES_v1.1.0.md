# Pòdcasts amb Matxa v1.1.0 🎙️🍵

Versió oficial actualitzada de **Pòdcasts amb Matxa**, l'estudi d'escriptori autònom per a la creació i locució de guions de pòdcast en català amb intel·ligència artificial. Aquesta compilació incorpora les noves funcionalitats de veu neural, ambientació sonora, suport per a Linux i comprovació integrada de versions.

### ✨ Novetats destacades de la versió 1.1.0
- **Nou motor de veu neural UPC FestCat — Ona i Pau (100% offline)**:
  - Síntesi local d'alta fidelitat acústica a 22.050 Hz basada en els models ONNX de la Universitat Politècnica de Catalunya: Ona (`ca_ES-upc_ona-medium.onnx`, 63,2 MB) i Pau (`ca_ES-upc_pau-x_low.onnx`, 26,8 MB).
  - Veus femenina (Ona) i masculina (Pau) de registre central, naturals, clares i ideals per a l'àmbit docent i divulgatiu.
  - Escolta prèvia instantània (0 ms) integrada al panell de locutors (`preview_upc_ona.wav` i `preview_upc_pau.wav`).
- **Pista de música i ambientació sonora de fons**:
  - Suport per a fitxers MP3, WAV, OGG i FLAC per a sintonia o música d'acompanyament.
  - Reproducció automàtica en bucle continu (*loop*) amb transició suau (*cross-fade* de 20 ms).
  - Control de volum dinàmic de l'1% al 100% (ajustat per defecte al 15% per a màxima claredat de veu).
  - Botó d'escolta de prova en temps real (`▶ Prova` / `■ Atura`).
  - Mescla professional amb esvaïment d'entrada (*fade-in* d'1 s) i sortida (*fade-out* de 2 s), combinada amb limitador suau de pic i masterització EBU R128 (-16 LUFS).
- **Comprovador d'actualitzacions i identificació de versió**:
  - Número de versió `v1.1.0` visible tant a la barra de títol de la finestra com al distintiu de la capçalera principal.
  - Botó d'accés ràpid **`🔄 Comprova versió`** a la capçalera per verificar actualitzacions contra el repositori de GitHub (`miquelangelfuentes/podcasts-amb-estil-i-matxa`).
  - Visualitzador de novetats amb `CTkTextbox` i ajust automàtic de línia (`wrap="word"`), evitant caràcters retallats a les descripcions de commits.
  - Diàleg informatiu amb historial de canvis i botó per descarregar i reiniciar automàticament.
- **Suport unificat per a Linux**:
  - Script llançador directe `run_app.sh` que crea l'entorn virtual `.venv`, instal·la dependències i inicia l'aplicació en un sol clic a distribucions com Ubuntu, Debian, Linkat, Fedora, Arch o Linux Mint.
  - Script de compilació `build_linux.py` per empaquetar binaris autònoms en fitxers `.tar.gz`.
  - Flux de treball CI/CD amb GitHub Actions (`.github/workflows/build-linux.yml`) per a compilació automàtica sobre servidors Ubuntu.
  - Diagnòstic de memòria RAM natiu mitjançant `/proc/meminfo`.
- **Distribució oficial amb nom de versió**:
  - El paquet binari autònom per a Windows es distribueix amb el nom de fitxer corresponent a la versió: `PodcastsAmbMatxa-v1.1.0-Windows.zip`.
- **Motors de veu integrats**:
  - **Matxa-TTS v2 multiaccent (100% offline)**: 16 veus per a totes les variants dialectals del català (balear, central, nord-occidental, septentrional i valencià) combinades amb el vocoder neuronal **alVoCat 22kHz**.
  - **UPC FestCat Ona i Pau (100% offline)**: veus femenina (63 MB) i masculina (27 MB) d'alta fidelitat de la Universitat Politècnica de Catalunya.
  - **Veus neuronals ca-ES (Online)**: servei al núvol amb 9 veus expressives (Joana, Enric, Ona, Pau, etc.).
- **Gestor integrat de components i models (📦 Models)**:
  - Descàrrega autònoma i modular des d'Hugging Face per a Matxa-TTS v2, alVoCat, UPC Ona i UPC Pau.
  - Eina **«Comprovar el meu equip»** amb diagnòstic automàtic de maquinari (CPU, GPU, RAM, disc i AVX2).
- **Control de qualitat**:
  - Bateria completa de proves automatitzades (`test_features.py`) amb 10/10 tests superats.
  - Correcció lingüística estricta en català (minúscula després dels dos punts `:`).
- **Dreceres de teclat globals (accessibilitat VCER Punt 5)**:
  - `Ctrl+G` o `Ctrl+Intro`: generar el pòdcast complet sense tocar el ratolí.
  - `Ctrl+S`: desar el guió; `Ctrl+O`: obrir un guió existent; `F1`: obrir la guia SSML.
  - `Escape`: cancel·lar la generació en curs.
- **Mode escola 100% offline (VCER Punts 2 i 4)**:
  - Botó **🏫 Mode escola** a la capçalera: activa un interruptor que elimina el motor al núvol del desplegable, mostra la insígnia **🛡️ Mode escola: 0% dades a internet (RGPD protegit)** i garanteix que cap text de l'alumnat surti de l'ordinador.
  - Ideal per a aules sense Wi-Fi, en entorns RGPD estrictes o amb menors d'edat.
- **Declaració d'ús de IA i verificació humana (VCER Punt 8)**:
  - Nova secció al README i a la Fitxa docent que documenta les quatre comprovacions manuals de contingut generat per IA: verificació fonètica, lingüística, de contingut i de privadesa.

---
*Creat mitjançant codificació per intencions amb Google Antigravity per Miquel Àngel Fuentes.*
