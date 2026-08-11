# 🎛️ Style Transform

> **Verander het lichaam van het liedje zonder het verhaal weg te gooien.**

Dit is één van de centrale ideeën van de Live Song Workbench.

We hebben bijvoorbeeld:

```text
THEME
   ↓
KEYWORDS
   ↓
12 LINES
   ↓
CHORDS
```

Dat is de kern.

Daarna kan dezelfde kern verschillende muzikale interpretaties krijgen.

---

# 🧬 Song DNA

```text
              SONG DNA
                 │
     ┌───────────┼───────────┐
     │           │           │
   WORDS       STORY       CORE
                          HARMONY
     │           │           │
     └───────────┼───────────┘
                 ▼
             STYLE LAYER
```

De style layer mag veranderen.

Het persoonlijke verhaal blijft herkenbaar.

---

# 🎸 Style 01 — Acoustic Story

```text
BPM: 80
Meter: 4/4

Guitar:
warm acoustic

Rhythm:
↓ X ↓ ↑ X ↑ ↓ ↑

Dynamics:
medium / relaxed
```

Gebruik voor:

- eerste uitvoering;
- kampvuur;
- tafel;
- straat;
- kennismaking.

---

# 🌙 Style 02 — Slow Reflective

```text
BPM: 56

Guitar:
sparse chords
long sustain

Rhythm:
↓ X X X ↓ X X X

Voice:
spoken / soft
```

Veel ruimte.

---

# 🌊 Style 03 — Shoegaze

```text
BPM: 110–120

Guitar:
reverb
delay
sustained chords

Rhythm:
steady eighth-note feel

Texture:
wide / dreamy
```

De tekst kan identiek blijven.

---

# ⚙️ Style 04 — Techno-inspired

```text
BPM: 120

Kick:
four-on-the-floor

Bass:
root pulse

Guitar:
short rhythmic texture

Voice:
repetitive mantra
```

Bijvoorbeeld:

```text
Freedom calls
Freedom calls
I choose
Today
```

kan hier juist sterker worden door herhaling.

---

# 🎻 Style 05 — Classical-inspired

```text
BPM: 60–80

Harmony:
same functional progression

Guitar / keys:
arpeggiated

Dynamics:
controlled

Voice:
clear / spacious
```

Belangrijk:

`classical-inspired` betekent hier niet:

> "genereer Bach."

Het betekent:

> gebruik een eenvoudige interpretatie met kenmerken die voor deze sessie klassieker aanvoelen.

---

# 🥁 Style 06 — Industrial Pulse

```text
BPM: 100–120

Beat:
mechanical

Bass:
repetitive

Guitar:
short distorted accents

Voice:
spoken / rhythmic
```

Goed voor een dramatische remix.

---

# 🔄 De Remix Button

De toekomstige interface:

```text
┌───────────────────────────────┐
│ 🎵 OUR SONG                  │
├───────────────────────────────┤
│                               │
│ Lyrics: LOCKED 🔒             │
│ Story:  LOCKED 🔒             │
│                               │
│ Current Style                 │
│ 🎸 Acoustic Story             │
│                               │
│ [ 🎲 REMIX STYLE ]            │
└───────────────────────────────┘
```

Druk:

```text
🎲 REMIX STYLE
```

Dan:

```text
Acoustic
   ↓
Shoegaze
```

maar:

```text
WORDS
STORY
CORE STRUCTURE
```

blijven staan.

---

# 🧠 Waarom dit belangrijk is

De deelnemer hoort:

> "Dat zijn nog steeds mijn woorden."

Maar tegelijkertijd:

> "Wow — het is ineens een compleet ander lied."

Dat creëert een sterk co-creatiemoment.

---

# 🎭 Style als vraag

In plaats van technisch te vragen:

> "Welke production aesthetic prefereer je?"

vraag:

> "Hoe moet jouw verhaal voelen?"

Bijvoorbeeld:

```text
☀️ vrolijk
🌙 rustig
🌊 dromerig
⚙️ hard
🕺 dansbaar
🎻 klassiek
```

---

# 🗺️ Human Language Mapping

```text
"rustig"
     ↓
Slow Reflective

"dromerig"
     ↓
Shoegaze

"lekker dansen"
     ↓
Techno-inspired

"gewoon gitaar"
     ↓
Acoustic Story

"iets raars"
     ↓
Random Style
```

---

# 🎚️ Style Recipe Object

Conceptueel:

```json
{
  "id": "shoegaze_01",
  "name": "Dream Wall",
  "tempo": 116,
  "meter": "4/4",
  "guitar": {
    "character": "sustained",
    "effects": [
      "reverb",
      "delay"
    ]
  },
  "rhythm": "steady_eighths",
  "energy": "medium"
}
```

---

# 🧩 Belangrijke architectuurregel

Style recipes mogen geen songtekst genereren.

Dus:

```text
SONG CONTENT ENGINE
        │
        ▼
words / lines / story

MUSIC ENGINE
        │
        ▼
chords / rhythm

STYLE ENGINE
        │
        ▼
tempo / texture / interpretation
```

Drie aparte verantwoordelijkheden.

---

# 🔒 Preserve Decisions

Stel:

Aletta heeft regel 6 gekozen:

```text
Ik durf opnieuw
```

Die regel wordt:

```text
🔒 LOCKED
```

Een style transform mag hem niet veranderen in:

```text
I boldly embrace tomorrow
```

alleen omdat de LLM dat mooier vindt.

Dat is precies wat we niet willen.

---

# 🤖 AI Style Assist

Een lokale LLM kan later bijvoorbeeld krijgen:

```text
Current song:

Key: A minor
Progression: Am F C G
Tempo: 80
Style: acoustic

Transform the performance recipe into:
dreamy shoegaze.

Do not modify:
- lyrics
- key
- progression
- structure

Return only structured performance parameters.
```

---

# 📦 Structured Output

Bijvoorbeeld:

```json
{
  "style": "shoegaze",
  "tempo": 116,
  "guitar_character": "sustained",
  "rhythm": "steady_eighths",
  "effects": [
    "reverb",
    "delay"
  ],
  "vocal_character": "soft"
}
```

Dit is precies het soort taak waarvoor een lokaal model met schema-gebonden output later interessant wordt.

---

# 🛡️ Maar presets eerst

MVP:

```text
ACOUSTIC
SLOW
SHOEGAZE
TECHNO
CLASSICAL
INDUSTRIAL
```

zijn gewone vooraf gedefinieerde recepten.

Geen AI nodig.

Dat betekent:

```text
NO INTERNET
NO API
NO MODEL
```

en toch werkt de Workbench.

---

# 🧠 AI komt erbovenop

```text
             WORKBENCH
                 │
        ┌────────┴────────┐
        │                 │
    PRESETS              AI
        │                 │
 deterministic       suggestions
        │                 │
        └────────┬────────┘
                 ▼
               HUMAN
                CHOICE
```

---

# ⚡ Live Performance Flow

```text
STORY
  ↓
WORDS
  ↓
12 LINES
  ↓
Am F C G
  ↓
80 BPM
  ↓
ACOUSTIC
  ↓
▶ PLAY
  ↓
"Wil je horen hoe dit
als shoegaze klinkt?"
  ↓
🎲 REMIX
  ↓
116 BPM
  ↓
🌊 SHOEGAZE
```

Dit kan een natuurlijk onderdeel van de live ervaring worden.

---

# 🎤 Facilitation Moment

Het interessante is niet alleen de techniek.

De facilitator kan vragen:

> "Welke versie voelt het meest als jouw verhaal?"

Daarmee wordt de remix opnieuw onderdeel van het gesprek.

---

# 🧭 Style is Interpretation

```text
VERHAAL
   │
   ├── kan zacht klinken
   ├── kan hard klinken
   ├── kan dansbaar klinken
   ├── kan verdrietig klinken
   └── kan hoopvol klinken
```

De deelnemer ontdekt daardoor mogelijk iets nieuws over hetzelfde verhaal.

---

# 📱 Ultimate Style View

```text
┌───────────────────────────────┐
│ 🎛️ STYLE                    │
├───────────────────────────────┤
│                               │
│ CURRENT                       │
│ 🎸 Acoustic · 80 BPM          │
│                               │
│ TRY                           │
│                               │
│ 🌙 Slow        56             │
│ 🌊 Shoegaze   116             │
│ ⚙️ Industrial 108             │
│ 🕺 Techno     120             │
│ 🎻 Classical   70             │
│                               │
│ [ APPLY ]                     │
│                               │
├───────────────────────────────┤
│ 🔒 Story                      │
│ 🔒 Lyrics                     │
│ 🔒 Chords                     │
└───────────────────────────────┘
```

---

# ⭐ Kernregel

> **Remix de muziek. Respecteer het verhaal.**
