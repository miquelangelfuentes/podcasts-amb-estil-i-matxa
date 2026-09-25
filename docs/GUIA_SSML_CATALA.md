# Guia d'opcions SSML, prosòdia i fonètica dialectal en català

Aquesta guia detalla les possibilitats del **Speech Synthesis Markup Language (SSML)**, el control prosòdic i el tractament fonètic de les diferents varietats dialectals catalanes a l'aplicació «Pòdcasts amb Matxa».

L'aplicació integra els models oficials desenvolupats pel **Barcelona Supercomputing Center (BSC-LT)**, la **Universitat Politècnica de Catalunya (UPC)** i el **Projecte AINA**:
- **BSC-LT/matxa-tts-v2-ca-multiaccent-graphemes**: model basat en *Optimal-Transport Conditional Flow Matching* (OT-CFM) i vocoder WaveNeXt, amb 16 veus autèntiques que cobreixen tots els dialectes catalans (100% offline, motor predeterminat).
- **UPC FestCat Ona i Pau (Piper Neural)**: models acústics neuronals d'alta definició a 22.050 Hz del corpus FestCat de la UPC (100% offline, Ona 63 MB i Pau 27 MB).
- **Microsoft Neural / Veus expressives ca-ES (Edge TTS)**: servei al núvol alternatiu amb veus Joana, Enric, Ona, Pau, Bet, etc.
- **projecte-aina/alvocat-vocos-22khz**: vocoder d'alta fidelitat acústica a 22.050 Hz i mòdul de normalització fonètica i ortogràfica del català.

---

## 1. Tractament de la prosòdia i la fonètica dialectal

### A. Riquesa fonètica i varietats territorials
El sistema no es limita al català central, sinó que reprodueix de forma genuïna els trets acústics de les cinc grans àrees dialectals:

1. **Català central (Barcelona, Girona, Tarragona)**:
   - **Vocalisme àton**: reducció de les vocals àtones *a* i *e* a vocal neutra [ə], i de *o* i *u* a [u].
   - **Consonantisme**: sonorització de les esses fricatives [z] davant de consonant sonora o entre vocals, i diferenciació nítida de les esses sordes [s].
   - **Veus de referència**: 'ona', 'pau', 'bet', 'jordi', 'teia', 'elia', 'grau'.

2. **Català balear (Mallorca, Menorca, Eivissa, Formentera)**:
   - **Vocalisme illenc**: realització genuïna de la vocal neutra tònica [ə] pròpia del mallorquí tradicional.
   - **Article salat i lèxic**: sintetització fluida de les combinacions amb l'article salat (*es*, *sa*, *ses*, *s'*), amb cadències entonatives pròpies de les Illes.
   - **Veus de referència**: 'olga' (femenina, Mallorca), 'quim' (masculina, Menorca), 'bm' (Bernat, Mallorca).

3. **Valencià (Comunitat Valenciana)**:
   - **Vocalisme occidental**: manteniment del sistema de 7 vocals tòniques sense vocal neutra, amb *e* i *o* àtones ben diferenciades d'*a* i *u*.
   - **Distinció consonàntica**: obertura de les *e* tòniques segons la norma valenciana i pronúncia genuïna de les terminacions verbals en *-e*.
   - **Veus de referència**: 'gina' (femenina), 'lluc' (masculina), 'arnau' (masculina), 'berta' (femenina), 'pere' (masculina).

4. **Català nord-occidental (Lleida, Alt Pirineu, Terres de Ponent i de l'Ebre)**:
   - **Vocalisme de Ponent**: oposició clara entre [a] i [e] en posició àtona inicial o interior.
   - **Prosòdia pirinenca**: entonació declarativa característica de les comarques de Lleida i de l'Alt Pirineu.
   - **Veus de referència**: 'emma' (femenina, Lleida), 'pere' (masculina, Lleida), 'estel' (femenina, Alt Pirineu).

5. **Català septentrional / Rossellonès (Catalunya del Nord)**:
   - **Vocalisme rossellonès**: manteniment de les característiques entonatives i fonètiques septentrionals, amb obertures i tancaments vocàlics particulars.
   - **Veus de referència**: 'laura' (femenina, Rosselló), 'jordi' (masculina, Perpinyà).

---

## 2. La puntuació escrita com a prosòdia natural

Els motors neuronals de l'aplicació (Matxa-TTS v2, UPC FestCat i les veus expressives) extreuen la intenció prosòdica directament dels signes de puntuació:
- **La coma `,`**: introdueix una corba melòdica ascendent suau i una pausa respiratòria d'entre 150 i 250 ms.
- **El punt i seguit `.`**: aplica una cadència descendent declarativa conclusiva.
- **L'interrogant `?`**: genera una elevació melòdica final característica de la pregunta en català.
- **Els punts suspensius `...`**: allarguen la vocal anterior i transmeten dubte, reflexió o transició pedagògica.
- **L'ela geminada `l·l`**: sempre amb punt volat central; es pronuncia com a consonant lateral allargada [lː].

---

## 3. Etiquetes SSML admeses al guió

Pots incorporar etiquetes SSML directament a les frases que pronuncia cada veu. El sistema les processa i les trasllada als motors neuronals:

### A. Pauses i silencis precisos (`<break>`)
Permet determinar la durada exacta del silenci d'una veu abans de continuar el discurs:
```xml
Veu 1: en primer lloc, analitzarem les dades. <break time="400ms"/> En segon lloc, veurem la hipòtesi.
Veu 2: deixeu-me pensar un instant... <break time="1s"/> Ara ho veig molt més clar!
```
- **Atribut `time`**: admet mil·lisegons (`250ms`, `500ms`) o segons (`1s`, `1.5s`).
- **Pautes recomanades**:
  - `150ms - 300ms`: petita pausa respiratòria dins d'una frase llarga.
  - `400ms - 700ms`: canvi de subtema o transició entre conceptes.
  - `800ms - 1.5s`: silenci dramàtic o espai perquè l'oient assimili una pregunta clau.

---

### B. Velocitat i to emocional (`<prosody>`)
Modula la rapidesa de la locució (`rate`) i l'alçada tonal (`pitch`):
```xml
Veu 1: <prosody rate="0.9">Aquesta definició és fonamental per comprendre la teoria.</prosody>
Veu 2: <prosody rate="1.15" pitch="+1st">Molt bé! Hem resolt el problema en temps rècord!</prosody>
```
- **`rate` (Velocitat)**:
  - `rate="slow"` o `rate="0.85"`: to acadèmic reposat i pausat.
  - `rate="fast"` o `rate="1.15"`: to dinàmic, enèrgic o col·loquial.
- **`pitch` (To)**:
  - `pitch="+1st"` / `pitch="+2st"`: eleva 1 o 2 semitons (expressa entusiasme, sorpresa o alegria).
  - `pitch="-1st"` / `pitch="-2st"`: abaixa semitons (to solemne, greu o conclusiu).

---

### C. Èmfasi pedagògic (`<emphasis>`)
Incrementa l'energia acústica i dilata lleugerament la durada de les paraules destacades:
```xml
Veu presentadora: no es tracta d'una simple anècdota, és un <emphasis level="strong">canvi estructural</emphasis> del nostre model.
```
- **Nivells**:
  - `level="strong"`: gran relleu a la frase (concepte clau).
  - `level="moderate"`: relleu intermedi estàndard.
  - `level="reduced"`: to secundari o matís subordinat.

---

### D. Lletrejat i sigles (`<say-as>`)
Indica al normalitzador com ha d'articular sigles, nombres o caràcters:
```xml
Veu 1: podeu consultar el text oficial al <say-as interpret-as="characters">DOGC</say-as>.
Veu 2: som a la pàgina <say-as interpret-as="cardinal">24</say-as>, capítol <say-as interpret-as="ordinal">3</say-as>.
```

---

## 4. Espacialització estèreo i entorn sonor

L'aplicació recrea un estudi de ràdio mitjançant el posicionament de cada veu a l'espai estèreo:

| Posició | Valor tècnic | Ús recomanat | Sensació acústica |
| :--- | :--- | :--- | :--- |
| **Centre** | `pan=0%` | Veu presentadora o monòleg | Situada just al davant de l'oient |
| **Esquerra suau** | `pan=-25%` | Veu 1 (diàlegs i tertúlies) | A la banda esquerra de la taula de gravació |
| **Dreta suau** | `pan=+25%` | Veu 2 (diàlegs i tertúlies) | A la banda dreta de la taula de gravació |
| **Esquerra ampla** | `pan=-50%` | Veus convidades secundàries | Més separada per evitar solapaments |
| **Dreta ampla** | `pan=+50%` | Veus convidades secundàries | Més separada a l'extrem dret |

---

## 5. Masterització EBU R128 i exportació

En finalitzar la síntesi de totes les intervencions, l'aplicació aplica un procés de masterització professional:
- **Integració de música o ambient de fons**: si s'ha seleccionat una pista d'àudio (MP3, WAV, OGG, FLAC), es mescla automàticament amb la locució en bucle continu (*loop*) amb *cross-fade* de 20 ms, esvaïment d'entrada (*fade-in* d'1 s) i sortida (*fade-out* de 2 s), i un limitador suau de pic abans de la normalització.
- **Normalització de sonoritat EBU R128**: ajusta el volum integrat a **-16 LUFS** (l'estàndard internacional per a pòdcasts i plataformes digitals) amb un sostre de pic màxim de **-1 dBTP**.
- **Respiració entre intervencions**: intercala un respir natural de 650 ms (`PAUSA_INTERLOCUCIO`) entre canvis de veu per evitar talls sobtats.
- **Format d'exportació**: **MP3 a 160 kbps CBR estèreo**, que garanteix la màxima claredat en freqüències vocals mantenint fitxers lleugers i àgils per distribuir.
