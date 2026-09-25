# Pòdcasts amb Estil i Matxa v1.1.0 🎙️🍵

Versió oficial actualitzada de **Pòdcasts amb Estil i Matxa**, l'estudi d'escriptori autònom per a la creació i locució de guions de pòdcast en català amb intel·ligència artificial. Aquesta compilació incorpora les noves funcionalitats de veu neural, ambientació sonora i comprovació de versions.

### ✨ Novetats destacades de la versió 1.1.0
- **Nou motor de veu neural UPC Ona FestCat (100% offline)**:
  - Síntesi local d'alta fidelitat acústica a 22.050 Hz basada en el model ONNX de la Universitat Politècnica de Catalunya (`ca_ES-upc_ona-medium.onnx`, 63,2 MB).
  - Veu femenina central natural, clara i càlida, ideal per a l'àmbit docent i divulgatiu.
  - Escolta prèvia instantània (0 ms) integrada al panell de locutors (`preview_upc_ona.wav`).
- **Pista de música i ambientació sonora de fons**:
  - Suport per a fitxers MP3, WAV, OGG i FLAC per a sintonia o música d'acompanyament.
  - Reproducció automàtica en bucle continu (*loop*) amb transició suau (*cross-fade* de 20 ms).
  - Control de volum dinàmic de l'1% al 100% (ajustat per defecte al 15% per a màxima claredat de veu).
  - Botó d'escolta de prova en temps real (`▶ Prova` / `■ Atura`).
  - Mescla professional amb esvaïment d'entrada (*fade-in* d'1 s) i sortida (*fade-out* de 2 s), combinada amb limitador suau de pic i masterització EBU R128 (-16 LUFS).
- **Comprovador d'actualitzacions i identificació de versió**:
  - Número de versió `v1.1.0` visible tant a la barra de títol de la finestra com al distintiu de la capçalera principal.
  - Botó d'accés ràpid **`🔄 Comprova versió`** a la capçalera per verificar actualitzacions contra el repositori de GitHub (`miquelangelfuentes/podcasts-amb-estil-i-matxa`).
  - Diàleg informatiu amb historial de canvis i botó per descarregar i reiniciar automàticament.
- **Distribució oficial amb nom de versió**:
  - El paquet binari autònom per a Windows es distribueix amb el nom de fitxer corresponent a la versió: `PodcastsAmbEstilIMatxa-v1.1.0-Windows.zip`.
- **Motors de veu integrats**:
  - **Matxa-TTS v2 multiaccent (100% offline)**: 16 veus per a totes les variants dialectals del català (balear, central, nord-occidental, septentrional i valencià) combinades amb el vocoder neuronal **alVoCat 22kHz**.
  - **UPC Ona FestCat (100% offline)**: veu de la Universitat Politècnica de Catalunya d'alta claredat docent.
  - **Microsoft Neural ca-ES (Online)**: servei al núvol ràpid amb les veus Joana i Enric.
  - **StyleTTS 2 Català (Offline)**: checkpoint experimental de recerca del BSC-LT.
- **Gestor integrat de components i models (📦 Models)**:
  - Descàrrega autònoma i modular des d'Hugging Face.
  - Eina **«Comprovar el meu equip»** amb diagnòstic automàtic de maquinari (CPU, GPU, RAM, disc i AVX2).
- **Control de qualitat**:
  - Bateria completa de proves automatitzades (`test_features.py`) amb 10/10 tests superats.
  - Correcció lingüística estricta en català (minúscula després dels dos punts `:`).

---
*Creat mitjançant codificació per intencions amb Google Antigravity per Miquel Àngel Fuentes.*
