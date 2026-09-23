# Fitxa informativa i de divulgació: «Pòdcasts amb Estil i Matxa»

Aquest document és una **guia completa de context i indicacions de referència** dissenyada per a:
1. Proporcionar als docents i centres educatius una visió clara, rigorosa i pràctica de l'aplicació.
2. Servir com a **document de context per a models de llenguatge (LLM com ChatGPT, Claude, Gemini, Mistral o Llama)** per generar continguts de divulgació d'alta qualitat (fils de Twitter/X, publicacions de LinkedIn, carrusels d'Instagram, circulars docents o butlletins pedagògics).

---

## 1. Resum executiu i fitxa ràpida

| Paràmetre | Detall |
| :--- | :--- |
| **Nom de l'eina** | Pòdcasts amb Estil i Matxa |
| **Tipus de programari** | Aplicació d'escriptori autònoma per a Windows (sense dependències externes) |
| **Finalitat principal** | Creació àgil, intuïtiva i professional de pòdcasts educatius i institucionals en català mitjançant intel·ligència artificial neuronal |
| **Públic destinatari** | Docents de Primària, Secundària, Batxillerat, FP, Escoles Oficials d'Idiomes, Universitats, centres de formació d'adults (CFA) i creadors de contingut pedagògic |
| **Llengua i varietats** | Català en totes les seves variants territorials (central, balear, valencià, nord-occidental i septentrional/rossellonès) |
| **Motors de veu** | 1. **StyleTTS 2 Català** (BSC-LT, difusió neuronal amb veus d'estil i clonació zero-shot, motor predeterminat)<br>2. **Matxa-TTS v2 multiaccent** (BSC-LT, 16 veus territorials en format ONNX, 100% offline)<br>3. **alVoCat 22kHz** (Projecte AINA, vocoder d'alta fidelitat i normalitzador lingüístic)<br>4. **Microsoft Neural ca-ES** (servei al núvol alternatiu) |
| **Privadesa** | **100% local i confidencial** amb els models Matxa-TTS i StyleTTS 2 (cap text ni àudio surt de l'equip; apte per a la normativa RGPD) |
| **Cost i llicència** | Gratuït, lliure i de codi obert (fons públics del Projecte AINA i el BSC-LT) |
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

---

## 3. Catàleg de motors i veus disponibles

### Motor 1: 🎙️ StyleTTS 2 Català (motor predeterminat)
- **Model:** Checkpoint complet de pesos PyTorch de difusió neuronal del BSC-LT (`epoch_2nd_00070.pth`, ~2,05 GB descarregat a disc) condicionat amb alVoCat.
- **Característiques:** Gran expressivitat humana, modulació acústica de velocitat i to, i capacitat de clonació de veu zero-shot a partir d'arxius d'àudio de referència.
- **Veus integrades (9 veus d'estil):**
  - **Ona:** veu femenina central, to càlid, professional i corporatiu.
  - **Pau:** veu masculina central, to comunicatiu, dinàmic i proper.
  - **Bet:** veu femenina central, to didàctic, vivaç i expressiu.
  - **Jordi:** veu masculina central, to acadèmic, pausat i serè.
  - **Teia:** veu femenina central, to narratiu, calmat i reflexiu.
  - **Pere:** veu masculina valenciana, to natural i fluid.
  - **Lluc:** veu masculina balear, to genuí mallorquí.
  - **Joana:** veu femenina central estàndard.
  - **Enric:** veu masculina central estàndard.

### Motor 2: 🍵 Matxa-TTS v2 multiaccent (100% offline)
- **Model:** Model de síntesi autònoma en format ONNX Runtime (~260 MB) desenvolupat pel BSC-LT.
- **Característiques:** Ràpid, ultra-lleuger, d'execució directa per CPU sense necessitat de targeta gràfica dedicada.
- **16 veus catalanes genuïnes per a totes les variants dialectals:**
  - **Central:** Èlia (Fem, Barcelona), Grau (Masc, Girona), Ona (Fem), Pau (Masc).
  - **Balear:** Olga (Fem, Mallorca), Quim (Masc, Menorca), Bernat (Masc, Mallorca).
  - **Valencià:** Gina (Fem), Lluc (Masc), Arnau (Masc), Berta (Fem).
  - **Nord-occidental:** Emma (Fem, Lleida), Pere (Masc, Lleida), Estel (Fem, Pirineu).
  - **Septentrional / Rossellonès:** Laura (Fem, Rosselló), Jordi (Masc, Perpinyà).

### Motor 3: ☁️ Microsoft Neural ca-ES (Online)
- **Model:** Servei de connexió directa amb Microsoft Edge TTS al núvol.
- **Característiques:** No requereix espai al disc local (0 MB), però depèn d'internet constant i envia el text a servidors externs. Inclou les veus Joana i Enric.

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
   - L'alumnat esdevé guionista: redacta, revisa l'ortografia i la sintaxi, i l'eina genera el programa de ràdio sonoritzat i masteritzat sense complicacions tècniques.

---

## 5. Limitacions tècniques i recomanacions d'ús

- **Requisits de maquinari:** funciona en qualsevol ordinador amb Windows 10 o Windows 11. No requereix targeta gràfica dedicada (GPU); els models ONNX estan optimitzats per a processadors estàndard (Intel o AMD). Es recomanen 4 GB de memòria RAM (òptim 8 GB) i espai lliure al disc (mínim 500 MB per a Matxa-TTS; 2,5 GB si es descarrega el checkpoint complet de StyleTTS 2).
- **Format del guió:** l'eina processa els guions a partir de signes de puntuació (. ! ? ;). Per a una prosòdia excel·lent, es recomana redactar frases d'una extensió equilibrada (entre 10 i 25 paraules) evitant paràgrafs densos sense punts.
- **Mode núvol vs. mode offline:** per a ús amb menors d'edat i en entorns escolars, es recomana prioritzar sempre els motors offline (StyleTTS 2 o Matxa-TTS) per garantir la privadesa absoluta de les dades.

---

## 6. Usos ètics de l'eina a l'educació

1. **Transparència i reconeixement de la IA:**
   - Cal informar sempre l'alumnat i l'audiència que les veus han estat sintetitzades amb intel·ligència artificial neuronal del BSC-LT i el Projecte AINA.
2. **Protecció de dades de menors (RGPD):**
   - Els motors autònoms locals no guarden registres a servidors externs ni transfereixen dades a tercers, complint les normatives europees i departamentals de protecció de dades.
3. **Ús ètic i responsable de la clonació de veu:**
   - La funció de referència acústica (clonació zero-shot) s'ha d'utilitzar exclusivament amb el consentiment exprés de la persona titular de la veu.
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

### Prompt 1: Fil divulgatiu per a Twitter / X
```text
Actua com a especialista en comunicació educativa i tecnologia en català. A partir de la fitxa adjunta de «Pòdcasts amb Estil i Matxa», escriu un fil de Twitter/X de 5 a 6 piulades:
- Piulada 1 (Ganxo): Destaca la fita de tenir una eina d'estudi de ràdio en català, gratuïta, 100% offline i creada amb els models del BSC-LT i Projecte AINA.
- Piulada 2: Explica com ajuda els docents (creació de pòdcasts a 1, 2 o 3 veus en minuts, sense haver d'editar so).
- Piulada 3: Parla de la riquesa dialectal (16 veus: central, balear, valencià, lleidatà, rossellonès) i StyleTTS 2.
- Piulada 4: Emfatitza la privadesa (0% dades al núvol, ideal per a escoles i instituts, compleix el RGPD).
- Piulada 5: Usos pedagògics concrets (DUA, dislèxia, microlearning, ràdio escolar).
- Piulada 6 (Crida a l'acció): Enllaç al projecte a GitHub i invitació a provar-ho.
To: engrescador, divulgatiu, rigorós i proper. Fes servir icones i hashtags com #EducaCat #ProjecteAINA #BSCLT #IAenCatala. Recorda que en català no va majúscula després dels dos punts.
```

### Prompt 2: Publicació professional per a LinkedIn
```text
Actua com a docent innovador i assessor pedagògic en competència digital docent. Escriu una publicació per a LinkedIn sobre l'aplicació «Pòdcasts amb Estil i Matxa»:
- Enfocament: Innovació educativa, sobirania tecnològica i aplicació real a l'aula (DUA, comprensió oral, situacions d'aprenentatge).
- Explica per què és rellevant per a equips directius, coordinadors digitals i professorat de llengua o d'altres matèries.
- Destaca que no envia dades a cap servidor (privadesa dels centres) i que és una tecnologia d'accés obert creada pel BSC-LT i Projecte AINA.
- Estructura amb punts clau, to professional i reflexiu, i crida a la reflexió per als docents.
Recorda aplicar la normativa del català (minúscula després dels dos punts).
```

### Prompt 3: Guió visual per a carrusel d'Instagram
```text
Dissenya el contingut d'un carrusel d'Instagram de 6 diapositives per a docents sobre «Pòdcasts amb Estil i Matxa»:
- Diapositiva 1 (Portada): Títol impactant sobre com crear pòdcasts educatius en català amb IA en 1 minut.
- Diapositiva 2: El problema (la manca de temps dels docents per editar àudio i la manca de veus catalanes de qualitat).
- Diapositiva 3: La solució (com funciona l'eina: escrius el guió, tries les veus i generes l'episodi).
- Diapositiva 4: Característiques clau (100% offline, 16 accents territorials, privadesa per a menors).
- Diapositiva 5: 3 idees per a l'aula demà mateix (càpsules de repàs, entrevistes històriques, suport DUA a la lectura).
- Diapositiva 6: Com descarregar-la gratuïtament i crida a compartir amb el claustre.
Inclou indicacions de text visual i el text del peu de foto (caption) amb hashtags rellevants.
```

### Prompt 4: Circular o butlletí pedagògic per a claustres i coordinadors
```text
Redacta un text informatiu breu (300-400 paraules) per a un butlletí pedagògic escolar o correu de coordinació digital adreçat a tot el claustre de professors, presentant «Pòdcasts amb Estil i Matxa» com a eina recomanada per al nou curs:
- Explica què és, com s'instal·la (executable per a Windows), quins avantatges té per a l'atenció a la diversitat i com respecta la protecció de dades dels estudiants.
```
