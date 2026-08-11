# 🧱 Song Structure

> **Tijdens een live sessie wil je niet eerst een liedje ontwerpen. Je wilt een bruikbaar skelet kiezen en beginnen.**

De Live Song Workbench werkt daarom met vooraf gemaakte songstructuren.

De structuur is geen gevangenis.

Het is een startbaan.

---

# 🎯 Het probleem

Tijdens een live sessie heb je misschien:

- vijf minuten;
- een onbekende deelnemer;
- drie kernwoorden;
- een gitaar;
- een eenvoudig ritme;
- en geen idee wat het liedje gaat worden.

Dit is niet het juiste moment om te denken:

> "Welke innovatieve compositiestructuur zullen we ontwikkelen?"

Gebruik een recept.

```text
VERHAAL
   ↓
KERNWOORDEN
   ↓
KIES STRUCTUUR
   ↓
VUL REGELS
   ↓
SPEEL
```

---

# 🧰 Structure Menu

De eerste Workbench-versie krijgt een klein aantal kant-en-klare structuren.

| Recept | Maten | Gebruik |
|---|---:|---|
| Mini Mantra | 4 | ultrasnel |
| Happy Loop | 8 | eenvoudige jam |
| Story 12 | 12 | standaard collaborative song |
| Question / Answer | 12 | twee personen |
| Build & Release | 16 | iets uitgebreider |

Voor het MVP is **Story 12** de belangrijkste.

---

# 🎵 Story 12

```text
01 ─────────────
02 ─────────────
03 ─────────────
04 ─────────────
05 ─────────────
06 ─────────────
07 ─────────────
08 ─────────────
09 ─────────────
10 ─────────────
11 ─────────────
12 ─────────────
```

Iedere regel vertegenwoordigt in de eenvoudigste variant één maat.

Dat betekent niet dat iedere maat exact dezelfde hoeveelheid zang moet bevatten.

De maat is het creatieve vakje.

---

# 🧱 Vooraf ingevulde structuur

Een belangrijk Vliegbasis71-principe is:

> **Niet alles hoeft tijdens de sessie bedacht te worden.**

Een template kan bijvoorbeeld al regels bevatten.

```text
01  Vandaag begin ik
02  __________________
03  __________________
04  Ik ga
05  __________________
06  __________________
07  __________________
08  Nieuwe wegen
09  Ik kies
10  Vandaag
11  __________________
12  __________________
```

De lege plekken worden tijdens het gesprek gevuld.

Dit verlaagt de cognitieve belasting.

---

# 🧠 Waarom gedeeltelijk vooraf invullen?

Vergelijk:

```text
SCHRIJF EEN LIEDJE
```

met:

```text
01 Vandaag ______
02 Ik zie _______
03 _____________
04 Ik ga
```

De tweede opdracht is veel kleiner.

Dat is precies de bedoeling.

---

# 🎸 Harmonie en tekst zijn aparte lagen

De Workbench behandelt:

```text
TEKST
+
AKKOORDEN
+
RITME
+
STIJL
```

als afzonderlijke componenten.

Dus dezelfde tekst kan worden gespeeld als:

```text
80 BPM
Am - F - C - G
acoustic
```

maar daarna opnieuw als:

```text
120 BPM
Am - F - C - G
shoegaze / dance
```

of:

```text
56 BPM
Am - F - C - G
slow classical-inspired
```

Het verhaal blijft herkenbaar.

De muzikale interpretatie verandert.

---

# 🔄 Eén verhaal, meerdere uitvoeringen

```text
                 STORY
                   │
                   ▼
              12-LINE SONG
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
    ACOUSTIC     DANCE      SLOW
      80 BPM     120 BPM     56 BPM
        │          │          │
        └──────────┼──────────┘
                   ▼
              SAME STORY
           DIFFERENT EXPERIENCE
```

Dit is een kernfunctie van het toekomstige Workbench-concept.

---

# 🎼 Progression Slot

Een songstructuur bevat niet noodzakelijk vaste akkoordnamen.

Gebruik eerst graden:

```text
I
IV
V
vi
```

Daarna kan de gekozen toonsoort deze vertalen.

Bijvoorbeeld in G majeur:

```text
I   = G
IV  = C
V   = D
vi  = Em
```

---

# 🎸 Beginner Mode

Voor beginners:

```text
Key: G

G | D | Em | C
```

Geen ingewikkelde inversies.

Geen jazz-extensies.

Geen modulaties.

De vraag is:

> Kan iemand dit live spelen?

---

# 🧪 Explorer Mode

Voor nieuwsgierige spelers kan later een variant ontstaan:

```text
G
Dsus4
Em7
Cadd9
```

Maar de Workbench moet nooit doen alsof complexer automatisch beter is.

---

# ⚠️ LLM-waarschuwing uit het experiment

Een lokale LLM kan harmonisch plausibel klinkende tekst produceren die muzikaal niet klopt.

Bijvoorbeeld een model kan zeggen:

```text
Key: E minor

Em
Am
Dm
C#m
```

en vervolgens beweren dat dit logisch binnen de toonsoort past.

Dat moet niet blind worden vertrouwd.

Daarom:

```text
LLM SUGGESTION
      ↓
MUSIC RULE VALIDATION
      ↓
PLAYABILITY CHECK
      ↓
HUMAN EAR
      ↓
ACCEPT
```

---

# 🧮 Deterministische harmonie

Voor het MVP hoeft de LLM daarom niet eens de basisakkoorden te bepalen.

De software kan een veilige bibliotheek hebben.

Bijvoorbeeld:

```text
MINOR POP 01
i - VI - III - VII

A minor:
Am - F - C - G
```

of:

```text
MAJOR POP 01
I - V - vi - IV

G major:
G - D - Em - C
```

Daarna kan AI varianten voorstellen.

---

# 🎚️ Structure + Style

Een recept kan uiteindelijk bestaan uit:

```yaml
name: story_12
bars: 12
key: A_minor
tempo: 80

progression:
  - Am
  - F
  - C
  - G

style:
  acoustic

lyrics:
  - Vandaag begin ik
  - ""
  - ""
  - Ik ga
  - ""
  - ""
  - ""
  - Nieuwe wegen
  - Ik kies
  - Vandaag
  - ""
  - ""
```

Dit is conceptueel.

De definitieve machine-schema's komen later.

---

# 🎵 12 maten is een Workbench-keuze

De 12-maatsstructuur is hier geen verplicht blues-schema.

Een klassieke 12-bar blues gebruikt wel degelijk twaalf maten en doorgaans een I-IV-V-patroon, maar Vliegbasis71 gebruikt het getal twaalf primair als **praktische creatieve container**.  [oai_citation:1‡guitaring.net](https://guitaring.net/learn/blues-guitar-101-twelve-bar?utm_source=chatgpt.com)

Dus:

```text
12-BAR BLUES
≠
VLIEGBASIS71 STORY 12
```

Ze kunnen elkaar wel ontmoeten.

---

# 🧭 De North Star

```text
STRUCTURE
moet sneller maken

niet

STRUCTURE
moet creativiteit voorschrijven
```

---

# 📱 Workbench View

Uiteindelijk moet een speler ongeveer dit kunnen zien:

```text
┌──────────────────────────────┐
│ 🎵 STORY 12                 │
│                              │
│ Key: Am        BPM: 80       │
│ Style: Acoustic              │
├──────────────────────────────┤
│ 01 Am  Vandaag begin ik      │
│ 02 F   Nieuwe lucht          │
│ 03 C   Ik kijk vooruit       │
│ 04 G   Ik ga                 │
│                              │
│ 05 Am  ...                   │
│ 06 F   ...                   │
│ 07 C   ...                   │
│ 08 G   Nieuwe wegen          │
│                              │
│ 09 Am  Ik kies               │
│ 10 F   Vandaag               │
│ 11 C   ...                   │
│ 12 G   ...                   │
└──────────────────────────────┘
```

Groot.

Leesbaar.

Speelbaar.

---

# ⭐ Kernregel

> **Kies eerst een bruikbaar skelet. Maak het daarna persoonlijk.**

