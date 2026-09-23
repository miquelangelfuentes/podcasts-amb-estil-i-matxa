# Guia d'opcions SSML, prosòdia i fonètica dialectal en català

Aquesta guia detalla les possibilitats del **Speech Synthesis Markup Language (SSML)**, el control prosòdic i el tractament fonètic de les diferents varietats dialectals catalanes a l'aplicació «Pòdcasts amb Estil i Matxa».

L'aplicació integra els models oficials desenvolupats pel **Barcelona Supercomputing Center (BSC-LT)** i el **Projecte AINA**:
- **BSC-LT/styletts2-catalan-multispeaker**: Model basat en difusió d'estil neuronal, representacions WavLM i PL-BERT en català, i clonació de veu zero-shot.
- **BSC-LT/matxa-tts-v2-ca-multiaccent-graphemes**: Model basat en *Optimal-Transport Conditional Flow Matching* (OT-CFM) i vocoder WaveNeXt, amb 16 veus autèntiques que cobreixen tots els dialectes catalans.
- **projecte-aina/alvocat-vocos-22khz**: Vocoder d'alta fidelitat acústica a 22.050 Hz i mòdul de normalització fonètica i ortogràfica del català.

---

## 1. Tractament de la prosòdia i la fonètica dialectal

### A. Riquesa fonètica i varietats territorials
El sistema no es limita al català central, sinó que reprodueix de forma genuïna els trets acústics de les cinc grans àrees dialectals:

1. **Català central (Barcelona, Girona, Tarragona)**:
   - **Vocalisme àton**: Reducció de les vocals àtones *a* i *e* a vocal neutra [ə], i de *o* i *u* a [u].
   - **Consonantisme**: Sonorització de les esses fricatives [z] davant de consonant sonora o entre vocals, i diferenciació nítida de les esses sordes [s].
   - **Veus de referència**: 'ona', 'pau', 'bet', 'jordi', 'teia', 'elia', 'grau'.

2. **Català balear (Mallorca, Menorca, Eivissa, Formentera)**:
   - **Vocalisme illenc**: Realització genuïna de la vocal neutra tònica [ə] pròpia del mallorquí tradicional.
   - **Article salat i lèxic**: Sintetització fluida de les combinacions amb l'article salat (*es*, *sa*, *ses*, *s'*), amb cadències entonatives pròpies de les Illes.
   - **Veus de referència**: 'olga' (femenina, Mallorca), 'quim' (masculina, Menorca), 'bm' (Bernat, Mallorca), 'lluc' (StyleTTS 2).

3. **Valencià (Comunitat Valenciana)**:
   - **Vocalisme occidental**: Manteniment del sistema de 7 vocals tòniques sense vocal neutra, amb *e* i *o* àtones ben diferenciades d'*a* i *u*.
   - **Distinció consonàntica**: Obertura de les *e* tòniques segons la norma valenciana i pronúncia genuïna de les terminacions verbals en *-e*.
   - **Veus de referència**: 'gina' (femenina), 'lluc' (masculina), 'arnau' (masculina), 'berta' (femenina), 'pere' (StyleTTS 2).

4. **Català nord-occidental (Lleida, Alt Pirineu, Terres de Ponent i de l'Ebre)**:
   - **Vocalisme de Ponent**: Oposició clara entre [a] i [e] en posició àtona inicial o interior.
   - **Prosòdia pirinenca**: Entonació declarativa característica de les comarques de Lleida i de l'Alt Pirineu.
   - **Veus de referència**: 'emma' (femenina, Lleida), 'pere' (masculina, Lleida), 'estel' (femenina, Alt Pirineu).

5. **Català septentrional / Rossellonès (Catalunya del Nord)**:
   - **Vocalisme rossellonès**: Manteniment de les característiques entonatives i fonètiques septentrionals, amb obertures i tancaments vocàlics particulars.
   - **Veus de referència**: 'laura' (femenina, Rosselló), 'jordi' (masculina, Perpinyà).

---

## 2. La puntuació escrita com a prosòdia natural

Tant StyleTTS 2 com Matxa-TTS v2 extreuen la intenció prosòdica directament dels signes de puntuació:
- **La coma `,`**: Introdueix una corba melòdica ascendent suau i una pausa respiratòria d'entre 150 i 250 ms.
- **El punt i seguit `.`**: Aplica una cadència descendent declarativa conclusiva.
- **L'interrogant `?`**: Genera una elevació melòdica final característica de la pregunta en català.
- **Els punts suspensius `...`**: Allarguen la vocal anterior i transmeten dubte, reflexió o transició pedagògica.
- **L'ela geminada `l·l`**: Sempre amb punt volat central; es pronuncia com a consonant lateral allargada [lː].

---

## 3. Etiquetes SSML admeses al guió

Pots incorporar etiquetes SSML directament a les frases que pronuncia cada veu. El sistema les processa i les trasllada als motors neuronals:

### A. Pauses i silencis precisos (`<break>`)
Permet determinar la durada exacta del silenci d'una veu abans de continuar el discurs:
```xml
Veu 1: En primer lloc, analitzarem les dades. <break time="400ms"/> En segon lloc, veurem la hipòtesi.
Veu 2: Deixeu-me pensar un instant... <break time="1s"/> Ara ho veig molt més clar!
```
- **Atribut `time`**: Admet mil·lisegons (`250ms`, `500ms`) o segons (`1s`, `1.5s`).
- **Pautes recomanades**:
  - `150ms - 300ms`: Petita pausa respiratòria dins d'una frase llarga.
  - `400ms - 700ms`: Canvi de subtema o transició entre conceptes.
  - `800ms - 1.5s`: Silenci dramàtic o espai perquè l'oient assimili una pregunta clau.

---

### B. Velocitat i to emocional (`<prosody>`)
Modula la rapidesa de la locució (`rate`) i l'alçada tonal (`pitch`):
```xml
Veu 1: <prosody rate="0.9">Aquesta definició és fonamental per comprendre la teoria.</prosody>
Veu 2: <prosody rate="1.15" pitch="+1st">Molt bé! Hem resolt el problema en temps rècord!</prosody>
```
- **`rate` (Velocitat)**:
  - `rate="slow"` o `rate="0.85"`: To acadèmic reposat i pausat.
  - `rate="fast"` o `rate="1.15"`: To dinàmic, enèrgic o col·loquial.
- **`pitch` (To)**:
  - `pitch="+1st"` / `pitch="+2st"`: Eleva 1 o 2 semitons (expressa entusiasme, sorpresa o alegria).
  - `pitch="-1st"` / `pitch="-2st"`: Abaixa semitons (to solemne, greu o conclusiu).

---

### C. Èmfasi pedagògic (`<emphasis>`)
Incrementa l'energia acústica i dilata lleugerament la durada de les paraules destacades:
```xml
Veu presentadora: No es tracta d'una simple anècdota, és un <emphasis level="strong">canvi estructural</emphasis> del nostre model.
```
- **Nivells**:
  - `level="strong"`: Gran relleu a la frase (concepte clau).
  - `level="moderate"`: Relleu intermedi estàndard.
  - `level="reduced"`: To secundari o matís subordinat.

---

### D. Lletrejat i sigles (`<say-as>`)
Indica al normalitzador com ha d'articular sigles, nombres o caràcters:
```xml
Veu 1: Podeu consultar el text oficial al <say-as interpret-as="characters">DOGC</say-as>.
Veu 2: Som a la pàgina <say-as interpret-as="cardinal">24</say-as>, capítol <say-as interpret-as="ordinal">3</say-as>.
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

## 5. Clonació de veu zero-shot (StyleTTS 2)

StyleTTS 2 permet reproduir qualsevol timbre de veu català sense necessitat d'entrenament previ:
1. **Mostra de referència òptima**:
   - Durada recomanada: entre **5 i 15 segons**.
   - Àudio en format WAV o MP3 net, sense música de fons, reverberació ni sorolls.
   - Veu en català expressant el to i la intenció desitjats (el model transfereix tant la resposta en freqüència com l'estil d'articulació).
2. **Assignació**:
   - Mitjançant el botó **`🌿 Clonar veu...`** de la interfície o afegint `veu=clon=ruta_audio.wav` a la configuració de la veu.

---

## 6. Masterització EBU R128 i exportació

En finalitzar la síntesi de totes les intervencions, l'aplicació aplica un procés de masterització professional:
- **Normalització de sonoria EBU R128**: Ajusta el volum integrat a **-16 LUFS** (l'estàndard internacional per a pòdcasts i plataformes digitals) amb un sostre de pic màxim de **-1 dBTP**.
- **Respiració entre intervencions**: Intercala un respir natural de 650 ms (`PAUSA_INTERLOCUCIO`) entre canvis de veu per evitar talls sobtats.
- **Format d'exportació**: **MP3 a 160 kbps CBR estèreo**, que garanteix la màxima claredat en freqüències vocals mantenint fitxers lleugers i àgils per distribuir.
