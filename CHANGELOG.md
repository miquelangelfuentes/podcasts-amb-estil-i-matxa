# Registre de canvis (Changelog)

Tots els canvis rellevants, correccions (*fixes*) i novetats del projecte **Pòdcasts amb Estil i Matxa** es documenten en aquest arxiu seguint el format estàndard de [Keep a Changelog](https://keepachangelog.com/ca/1.0.0/) i la numeració de versions [Semantic Versioning](https://semver.org/).

---

## [1.1.0] - 2026-09-25

### ✨ Novetats
* **Integració de la veu neural UPC Ona FestCat (100% offline):**
  * S'ha afegit un nou motor autònom basat en `piper-tts` i el model ONNX (`ca_ES-upc_ona-medium.onnx`, 63,2 MB) procedent de les gravacions del corpus FestCat de la **Universitat Politècnica de Catalunya (UPC)**.
  * Veu femenina central d'extraordinària calidesa, naturalitat i fidelitat acústica a 22.050 Hz, ideal per a continguts docents i institucionals.
  * Funciona de forma 100% local, autònoma i sense dependència de connexió a internet.
* **Comprovador d'actualitzacions integrat («🔄 Comprova versió»):**
  * S'ha afegit un botó d'accés directe a la barra superior que obre el diàleg `VersionCheckModal`.
  * Consulta l'API oficial de GitHub (`miquelangelfuentes/podcasts-amb-estil-i-matxa`) per contrastar la versió local amb l'últim commit o release disponible.
  * Mostra el resum dels darrers canvis introduïts al projecte.
  * Permet descarregar l'actualització i reiniciar automàticament l'aplicació amb el botó **«Actualitza l'aplicació»**.
* **Integració de suport oficial per a Linux:**
  * S'ha creat l'script llançador autònom `run_app.sh` que crea l'entorn virtual `.venv`, instal·la dependències i inicia l'aplicació en un sol pas.
  * S'ha afegit el script de compilació `build_linux.py` per generar paquets binaris autònoms en arxiu comprimit (`PodcastsAmbEstilIMatxa-v1.1.0-Linux-x86_64.tar.gz`).
  * S'ha integrat un flux de treball automatitzat de CI/CD amb GitHub Actions (`.github/workflows/build-linux.yml`) que compila la versió per a Linux sobre servidors Ubuntu a cada release.
  * Lectura nativa de memòria RAM des de `/proc/meminfo` al mòdul de comprovació de maquinari (`SystemChecker`).
* **Visualitzador de novetats millorat i identificació de versió:**
  * S'ha substituït l'etiqueta d'una sola línia del modal de versions per un component `CTkTextbox` amb ajust automàtic de paraules (`wrap="word"`), evitant que cap missatge de commit o actualització surti retallat.
  * S'ha incorporat el distintiu visual `v1.1.0` a la capçalera de l'aplicació i s'ha actualitzat el títol de la finestra amb la versió instal·lada.
  * Nomenclatura oficial del paquet comprimit per a Windows amb el número de versió corresponent: `PodcastsAmbEstilIMatxa-v1.1.0-Windows.zip`.
* **Previsualitzacions d'àudio integrades per a la veu UPC Ona:**
  * S'han generat i empaquetat mostres d'àudio WAV (`preview_upc_ona.wav`) a `assets/previews/` per permetre l'escolta instantània (0 ms) de la nova veu de la UPC.
* **Gestor de descàrrega de models actualitzat:**
  * S'ha incorporat `upc_ona` a `ModelDownloader` i a la finestra de gestió de models (`ComponentsManagerModal`), permetent comprovar el seu estat d'instal·lació, mida a disc (60,3 MB) i descarregar-la o suprimir-la fàcilment.

### 🐛 Correccions i transparència tècnica
* **Clarificació i transparència dels motors de veu:**
  * S'ha anomenat i identificat obertament el motor **`Microsoft Neural ca-ES (Online)`** com a servei al núvol (veus Joana i Enric mitjançant Edge TTS), evitant qualsevol confusió sobre la necessitat de connexió a internet i privadesa.
  * S'ha eliminat la descàrrega del checkpoint de 2,05 GB de StyleTTS 2 del gestor de models: en tractar-se d'un model de recerca en PyTorch que requereix entorns d'investigació amb GPU, l'aplicació autònoma per a CPU no el podia carregar a disc i malbaratava espai. S'ha unificat i clarificat el catàleg: els dos motors 100% autònoms i offline són **Matxa-TTS v2 (16 veus)** i **UPC Ona (63 MB)**, mentre que les 9 veus d'estil queden identificades obertament com a servei Online.
* **Correcció d'estil lingüístic:**
  * S'ha revisat i aplicat la norma gramatical catalana de mantenir minúscula després dels dos punts (`:`) a tots els textos informatius i etiquetes de la interfície.
* **Motor predeterminat per defecte:**
  * S'ha establert **Matxa-TTS v2 multiaccent (100% offline)** com a selecció predeterminada en obrir l'aplicació.
* **Empaquetat PyInstaller per a Windows:**
  * S'ha configurat la compilació de l'executable perquè inclogui automàticament la llibreria `piper-tts`, el seu binari `espeakbridge.pyd` i les taules de dades fonètiques d'`espeak-ng` per al català i totes les seves variants territorials (`ca`, `ca-ba`, `ca-nw`, `ca-va`).
* **Verificació de qualitat:**
  * Ampliació de la suite de proves unitàries i d'integració a 10 bateries de tests (`test_features.py`), totes validades amb èxit (10/10).

---

## [1.0.1] - 2026-09-24

### ✨ Novetats
* **Pista de música o so de fons avançada:**
  * Suport per a fitxers MP3, WAV, OGG i FLAC d'acompanyament sonora.
  * Bucle automàtic continu (*loop*) amb transició suau (*cross-fade* de 20 ms) per evitar salts sobtats.
  * Control de volum dinàmic regulable de l'1% al 100% (calibrat per defecte al 15% per garantir la màxima claredat vocal).
  * Botó de prova d'escolta ràpida de la sintonia (`▶ Prova` / `■ Atura`).
  * Mescla professional amb esvaïment d'entrada (*fade-in* d'1 s) i sortida (*fade-out* de 2 s), combinada amb un limitador suau de pic per evitar saturació.
* **Pre-escalfament en segon pla (*pre-warming*):**
  * Càrrega asíncrona dels models neuronals en memòria en arrencar l'aplicació per a una resposta immediata en la primera petició de síntesi.
* **Mostres d'àudio preempaquetades (0 ms):**
  * S'han emmagatzemat arxius WAV d'escolta prèvia a `assets/previews/` per a totes les veus catalanes de Matxa-TTS, evitant càrregues innecessàries dels models pesats per provar les veus.
* **Documentació divulgativa per a docents:**
  * Creació del document `docs/FITXA_DIVULGACIO_DOCENTS.md` amb context pedagògic, aplicacions a l'aula (DUA, diversitat, varietats dialectals) i directrius ètiques per alimentar altres models de llenguatge (LLM) a xarxes socials.

---

## [1.0.0] - 2026-09-23

### 🚀 Llançament inicial
* **Estructura adaptable de locutors:**
  * Suport per a formats d'**1 veu (monòleg)**, **2 veus (diàleg)** i **3 veus (amb presentador)**.
  * Espacialització estèreo automàtica (*panning*: esquerra, centre i dreta).
* **Motor Matxa-TTS v2 multiaccent (BSC-LT):**
  * 16 veus catalanes autèntiques que cobreixen totes les grans variants territorials:
    * **Central:** Èlia, Grau, Ona, Pau.
    * **Balear:** Olga, Quim, Bernat.
    * **Valencià:** Gina, Lluc, Arnau, Berta.
    * **Nord-occidental:** Emma, Pere, Estel.
    * **Septentrional / Rossellonès:** Laura, Jordi.
* **Normalització lingüística alVoCat (Projecte AINA):**
  * Expansió automàtica de números, dates, hores, símbols, sigles i abreviatures en català.
* **Masterització d'estudi:**
  * Normalització de sonoritat d'emissió segons l'estàndard internacional **EBU R128 (-16 LUFS)**.
  * Exportació directa a fitxer **MP3 estèreo a 160 kbps CBR**.
* **Interfície d'usuari accessible:**
  * Dissenyada amb CustomTkinter seguint la paleta verda te matxa pastel (`#2E5E41`).
  * Suport per a escalat d'alta resolució DPI a Windows (100%, 125%, 150%, 175%, 200%).
  * Reproductor d'àudio integrat ancorat a la part inferior amb control de temps, volum i descàrrega.
* **Gestor de models i diagnòstic de l'equip:**
  * Diàleg visual per verificar l'espai en disc, memòria RAM, processador i GPU, i gestionar la descàrrega de components des d'Hugging Face.
* **Executable independent per a Windows:**
  * Distribució autònoma portable (`PodcastsAmbEstilIMatxa.exe`) sense necessitat d'instal·lar Python.
