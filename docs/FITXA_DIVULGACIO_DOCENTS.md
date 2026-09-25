# Fitxa informativa i de divulgació: «Pòdcasts amb Matxa»

Aquest document és una **guia completa de context i indicacions de referència** dissenyada per a:
1. Proporcionar als docents i centres educatius una visió clara, rigorosa i pràctica de l'aplicació.
2. Servir com a **document de context per a models de llenguatge (LLM com ChatGPT, Claude, Gemini, Mistral o Llama)** per generar continguts de divulgació d'alta qualitat (fils de Twitter/X, publicacions de LinkedIn, carrusels d'Instagram, circulars docents o butlletins pedagògics).

---

## 1. Resum executiu i fitxa ràpida

| Paràmetre | Detall |
| :--- | :--- |
| **Nom de l'eina** | Pòdcasts amb Matxa |
| **Tipus de programari** | Aplicació d'escriptori autònoma per a Windows i Linux (sense dependències externes) |
| **Finalitat principal** | Creació àgil, intuïtiva i professional de pòdcasts educatius i institucionals en català mitjançant intel·ligència artificial neuronal |
| **Públic destinatari** | Docents de Primària, Secundària, Batxillerat, FP, Escoles Oficials d'Idiomes, Universitats, centres de formació d'adults (CFA) i creadors de contingut pedagògic |
| **Llengua i varietats** | Català en totes les seves variants territorials (central, balear, valencià, nord-occidental i septentrional/rossellonès) |
| **Motors de veu** | 1. **Matxa-TTS v2 multiaccent** (BSC-LT, 16 veus territorials en format ONNX, 100% offline, motor predeterminat)<br>2. **UPC FestCat — Ona i Pau** (UPC / Piper Neural, veus femenina de 63 MB i masculina de 27 MB, 100% offline d'alta definició)<br>3. **Microsoft Neural ca-ES** (servei al núvol alternatiu amb connexió a internet)<br>4. **alVoCat 22kHz** (Projecte AINA, vocoder i normalitzador lingüístic) |
| **Privadesa** | **100% local i confidencial** amb els models Matxa-TTS v2 i UPC FestCat (cap text ni àudio surt de l'equip; apte per a la normativa RGPD) |
| **Actualitzacions** | Botó integrat «Comprova versió» que contrasta directament amb el repositori GitHub i permet actualitzar l'aplicació en un clic |
| **Música i ambient de fons** | Pista d'acompanyament (MP3, WAV, OGG, FLAC) en bucle continu (*loop*), control de volum dinàmic, prova instantània i transicions suaus (*fade-in*/*fade-out*) |
| **Cost i llicència** | Gratuït, lliure i de codi obert (fons públics del Projecte AINA, la UPC i el BSC-LT) |
| **Repositori oficial** | [GitHub: miquelangelfuentes/podcasts-amb-estil-i-matxa](https://github.com/miquelangelfuentes/podcasts-amb-estil-i-matxa) |

---

## 2. Què fa que aquesta eina sigui única?

1. **Sobirania lingüística i tecnològica catalana:**
   - La majoria d'eines comercials de síntesi de veu (TTS) ofereixen poques veus en català, sovint amb accents forçats, errors de prosòdia o absència total de varietats com el balear o el valencià.
   - Aquesta eina utilitza la tecnologia de parla desenvolupada pel **Barcelona Supercomputing Center (BSC-LT)** amb el suport del **Projecte AINA** (Generalitat de Catalunya), situant la llengua catalana al capdavant de la recerca en intel·ligència artificial.

2. **Funcionament autònom (100% offline):**
   - No requereix connexió a internet ni dependència de serveis al núvol després de la descàrrega inicial.
   - Es pot utilitzar a les aules, en ordinadors portàtils sense Wi-Fi o en zones sense cobertura amb total seguretat.

3. **Arquitectura multilocutor integrada (1, 2 o 3 veus):**
   - Permet crear des d'un monòleg o càpsula formativa breu (1 veu) fins a entrevistes simulades (2 veus) o tertúlies radiofòniques amb presentador i convitats (3 veus).
   - Espacialització estèreo automàtica (veus a l'esquerra, al centre i a la dreta) per aconseguir una experiència acústica d'estudi de ràdio real.

4. **Masterització de so automàtica amb estàndard professional:**
   - Integra el normalitzador lingüístic alVoCat per pronunciar correctament xifres, sigles, ordinals i dates en català.
   - Masteritza l'episodi final d'acord amb la normativa internacional de radiodifusió **EBU R128 (-16 LUFS)**, garantint un volum homogeni i exportació directa a MP3 a 160 kbps.

5. **Música i ambientació sonora de fons (MP3, WAV, OGG, FLAC):**
   - Permet incorporar fàcilment una sintonia d'obertura, melodia o ambient acústic d'acompanyament (pluja, bosc, cafeteria, sintetitzadors, piano).
   - Reproducció automàtica en **bucle continu (*loop*)** amb transició suau (*cross-fade* de 20 ms) per evitar salts sobtats o clics entre repeticions.
   - **Control de volum dinàmic** ajustable de l'1% al 100% (calibrat per defecte al 15% per preservar la màxima claredat de la parla) i botó de reproducció de prova instantània (`▶ Prova` / `■ Atura`).
   - Mescla d'estudi amb esvaïment progressiu d'entrada (*fade-in* d'1 s) i sortida (*fade-out* de 2 s), combinada amb un limitador suau de pic per garantir zero distorsió abans de la normalització final.

---

## 3. Catàleg de motors i veus disponibles

### Motor 1: 🍵 Matxa-TTS v2 multiaccent (100% offline — motor predeterminat)
- **Model:** Model de síntesi autònoma en format ONNX Runtime (~260 MB) desenvolupat pel **Barcelona Supercomputing Center (BSC-LT)**.
- **Característiques:** Ràpid, ultra-lleuger, d'execució directa per CPU sense necessitat de targeta gràfica dedicada ni connexió a internet.
- **16 veus catalanes genuïnes per a totes les variants dialectals:**
  - **Central:** Èlia (Fem, Barcelona), Grau (Masc, Girona), Ona (Fem), Pau (Masc).
  - **Balear:** Olga (Fem, Mallorca), Quim (Masc, Menorca), Bernat (Masc, Mallorca).
  - **Valencià:** Gina (Fem), Lluc (Masc), Arnau (Masc), Berta (Fem).
  - **Nord-occidental:** Emma (Fem, Lleida), Pere (Masc, Lleida), Estel (Fem, Pirineu).
  - **Septentrional / Rossellonès:** Laura (Fem, Rosselló), Jordi (Masc, Perpinyà).

### Motor 2: 🎙️ UPC FestCat — Ona i Pau (100% offline)
- **Model:** Models neuronals en format Piper ONNX (Ona: ~63 MB, Pau: ~27 MB) basats en les gravacions del corpus **FestCat** de la **Universitat Politècnica de Catalunya (UPC)**.
- **Característiques:** Qualitat i calidesa de locució humana excepcionals, pes molt reduït, funcionament 100% autònom sense internet i gran naturalitat pedagògica.
- **Veus integrades:**
  - **Ona (UPC FestCat):** veu femenina central, càlida, didàctica i institucional.
  - **Pau (UPC FestCat):** veu masculina central, naturalesa divulgativa, propera i clara.

### Motor 3: ☁️ Microsoft Neural ca-ES (Online)
- **Model:** Servei de connexió al núvol mitjançant Edge TTS.
- **Característiques:** Útil com a alternativa ràpida; no requereix espai al disc local (0 MB), però requereix connexió constant a internet i transmet el text als servidors de Microsoft.
- **Veus integrades:** Joana (veu femenina) i Enric (veu masculina).

---

## 4. Usos educatius per a docents i aules

1. **Càpsules d'aprenentatge i microlearning:**
   - Explicacions sintètiques de conceptes clau (3 a 5 minuts) per a classes invertides (*Flipped Classroom*), repassos abans d'avaluacions o introducció de nous temes.

2. **Entrevistes i debats simulats:**
   - Recreació de diàlegs històrics (per exemple: un diàleg entre personatges d'època), debats ètics sobre ciència o debats literaris entre autors amb rols de veu ben diferenciats.

3. **Atenció a la diversitat i Disseny Universal per a l'Aprenentatge (DUA):**
   - **Suport a la lectura:** recurs imprescindible per a alumnat amb dislèxia, baixa visió o dificultats de descodificació lectora.
   - **Comprensió multimodal:** l'alumnat pot seguir el text escrit mentre escolta una locució impecable en català amb pauses naturals.

4. **Treball de dialectologia i sensibilització lingüística:**
   - Permet escoltar i comparar com sona un mateix text en català central, valencià, mallorquí, lleidatà o rossellonès, fomentant la riquesa dialectal a classe de llengua.

5. **Acollida lingüística i aprenentatge del català com a L2:**
   - Eina idònia per a aules d'acollida, escoles d'adults (CFA) i centres de normalització lingüística (CPNL), amb velocitat ajustable per a exercicis de comprensió oral.

6. **Projectes de ràdio escolar i comunicació audiovisual:**
   - L'alumnat esdevé guionista: redacta, revisa l'ortografia i la sintaxi, tria la sintonia musical o ambientació sonora de fons en bucle i l'eina genera el programa de ràdio sonoritzat i masteritzat sense complicacions tècniques ni necessitat d'editors externs.

7. **Narració sonora immersiva, audiocontes i teatre llegit:**
   - La combinació de diàlegs expressius a 2 o 3 veus amb música de fons (paisatges sonors de natura, melodies d'època o ambients de ciència-ficció) permet crear audiocontes, reconstruccions històriques o representacions literàries amb un alt grau d'immersió emocional i motivadora.

---

## 5. Limitacions tècniques i recomanacions d'ús

- **Requisits de maquinari:** funciona en qualsevol ordinador amb Windows 10 o Windows 11 i en distribucions Linux (Ubuntu, Debian, Linkat, Fedora, Arch o Linux Mint). No requereix targeta gràfica dedicada (GPU); els models ONNX estan optimitzats per a processadors estàndard (Intel o AMD). Es recomanen 4 GB de memòria RAM (òptim 8 GB) i espai lliure al disc (mínim 400-500 MB per als models ONNX offline).
- **Format del guió:** l'eina processa els guions a partir de signes de puntuació (. ! ? ;). Per a una prosòdia excel·lent, es recomana redactar frases d'una extensió equilibrada (entre 10 i 25 paraules) evitant paràgrafs densos sense punts.
- **Mode núvol vs. mode offline:** per a ús amb menors d'edat i en entorns escolars, es recomana prioritzar sempre els motors offline (Matxa-TTS v2 o UPC FestCat) per garantir la privadesa absoluta de les dades.

---

## 6. Usos ètics de l'eina a l'educació

1. **Transparència i reconeixement de la IA:**
   - Cal informar sempre l'alumnat i l'audiència que les veus han estat sintetitzades amb intel·ligència artificial neuronal del BSC-LT i el Projecte AINA.
2. **Protecció de dades de menors (RGPD):**
   - Els motors autònoms locals no guarden registres a servidors externs ni transfereixen dades a tercers, complint les normatives europees i departamentals de protecció de dades.
3. **Ús ètic i responsable de la síntesi de veu:**
   - La síntesi de veu s'ha d'utilitzar amb finalitats formatives, pedagògiques o divulgatives legítimes.
   - Està estrictament prohibit utilitzar l'eina per a suplantació d'identitat, generació de falsedats (*deepfakes*) o continguts difamatoris.
4. **Equitat dialectal i respecte lingüístic:**
   - Cap variant territorial no s'ha de considerar inferior o subordinada; l'eina promou la dignitat i presència de totes les parles catalanes.

---

## 7. Llicències i autoria

- **Models lingüístics i xarxes neuronals:** desenvolupats pel **Barcelona Supercomputing Center (BSC-LT)** en el marc del **Projecte AINA**, finançats pel Departament de Polítiques Digitals de la Generalitat de Catalunya.
- **Codi font de l'aplicació:** distribuït com a programari lliure sota llicència oberta a GitHub per a la comunitat educativa i la societat civil.
- **Llicència de documentació i exemples:** Creative Commons Reconeixement-CompartirIgual 4.0 Internacional (CC BY-SA 4.0).

---

## 8. Guia de prompts per a altres LLM (Creació de posts a xarxes socials)

A continuació es detallen plantilles d'instrucció que pots copiar i enganxar directament a un model de llenguatge (com ara ChatGPT, Claude o Gemini) juntament amb aquesta fitxa per crear continguts divulgatius:

### Prompt 1: fil divulgatiu per a Twitter / X
```text
Actua com a especialista en comunicació educativa i tecnologia en català. A partir de la fitxa adjunta de «Pòdcasts amb Matxa», escriu un fil de Twitter/X de 5 a 6 piulades:
- Piulada 1 (Ganxo): destaca la fita de tenir una eina d'estudi de ràdio en català, gratuïta, 100% offline i creada amb els models del BSC-LT i Projecte AINA.
- Piulada 2: explica com ajuda els docents (creació de pòdcasts a 1, 2 o 3 veus en minuts, música de fons en bucle amb volum regulable i sense haver d'editar so externament).
- Piulada 3: parla de la riquesa dialectal (16 veus: central, balear, valencià, lleidatà, rossellonès) i la claredat d'UPC FestCat (Ona i Pau).
- Piulada 4: emfatitza la privadesa (0% dades al núvol, ideal per a escoles i instituts, compleix el RGPD).
- Piulada 5: usos pedagògics concrets (DUA, dislèxia, microlearning, ràdio escolar, audiocontes immersius).
- Piulada 6 (Crida a l'acció): enllaç al projecte a GitHub i invitació a provar-ho.
To: engrescador, divulgatiu, rigorós i proper. Fes servir icones i hashtags com #EducaCat #ProjecteAINA #BSCLT #IAenCatala. Recorda que en català no va majúscula després dels dos punts.
```

### Prompt 2: publicació professional per a LinkedIn
```text
Actua com a docent innovador i assessor pedagògic en competència digital docent. Escriu una publicació per a LinkedIn sobre l'aplicació «Pòdcasts amb Matxa»:
- Enfocament: innovació educativa, sobirania tecnològica i aplicació real a l'aula (DUA, comprensió oral, situacions d'aprenentatge, expressió radiofònica).
- Explica per què és rellevant per a equips directius, coordinadors digitals i professorat de llengua o d'altres matèries.
- Destaca que no envia dades a cap servidor (privadesa dels centres), que incorpora música i ambientació de fons automàtica i que és una tecnologia d'accés obert creada pel BSC-LT i Projecte AINA.
- Estructura amb punts clau, to professional i reflexiu, i crida a la reflexió per als docents.
Recorda aplicar la normativa del català (minúscula després dels dos punts).
```

### Prompt 3: guió visual per a carrusel d'Instagram
```text
Dissenya el contingut d'un carrusel d'Instagram de 6 diapositives per a docents sobre «Pòdcasts amb Matxa»:
- Diapositiva 1 (Portada): títol impactant sobre com crear pòdcasts educatius en català amb IA en 1 minut.
- Diapositiva 2: el problema (la manca de temps dels docents per editar àudio i la manca de veus catalanes de qualitat).
- Diapositiva 3: la solució (com funciona l'eina: escrius el guió, tries les veus, afegeixes música de fons i generes l'episodi).
- Diapositiva 4: característiques clau (100% offline, 16 accents territorials, música de fons en bucle amb volum calibrat, privadesa per a menors).
- Diapositiva 5: 3 idees per a l'aula demà mateix (càpsules de repàs, entrevistes històriques, audiocontes sonoritzats, suport DUA a la lectura).
- Diapositiva 6: com descarregar-la gratuïtament i crida a compartir amb el claustre.
Inclou indicacions de text visual i el text del peu de foto (caption) amb hashtags rellevants.
```

### Prompt 4: circular o butlletí pedagògic per a claustres i coordinadors
```text
Redacta un text informatiu breu (300-400 paraules) per a un butlletí pedagògic escolar o correu de coordinació digital adreçat a tot el claustre de professors, presentant «Pòdcasts amb Matxa» com a eina recomanada per al nou curs:
- Explica què és, com s'instal·la (executable autònom per a Windows o paquet per a Linux), quins avantatges té per a l'atenció a la diversitat, com permet ambientar sonors amb música de fons i com respecta la protecció de dades dels estudiants.
```
