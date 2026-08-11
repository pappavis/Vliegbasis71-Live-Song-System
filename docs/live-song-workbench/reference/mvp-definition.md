# 🚀 MVP Definition

> **Het MVP moet binnen een korte bouwsessie bruikbaar worden — niet veranderen in een softwareproject dat gitaarspelen vervangt.**

---

# 🎯 Probleem

Tijdens een live sessie moet de facilitator snel van:

```text
VERHAAL
```

naar:

```text
SPEELBAAR LIEDJE
```

kunnen gaan.

Zonder:

- lange prompts;
- papierwerk;
- complexe DAW;
- internetdependency;
- muziektheorie tijdens de sessie.

---

# 👤 Primaire gebruiker

```text
HAPPY STRUMMER
```

Een gebruiker die:

- eenvoudige akkoorden kan spelen;
- ritme kan vasthouden;
- met mensen wil samenwerken;
- geen professionele producer hoeft te zijn.

---

# 🧪 MVP User Story

> Als live song facilitator wil ik een thema of klein verhaal kunnen invoeren, daar snel woorden en korte regels uit kiezen, een eenvoudige muzikale structuur selecteren en alles op één scherm zien zodat ik binnen enkele minuten samen met iemand een liedje kan spelen.

---

# 🖥️ MVP Screen

```text
┌─────────────────────────────────────────┐
│ 🎛️ VLIEGBASIS71 LIVE WORKBENCH        │
├─────────────────────────────────────────┤
│                                         │
│ THEME                                   │
│ [ New beginning________________ ]       │
│                                         │
│ KEYWORDS                                │
│ [freedom] [courage] [future] [+]        │
│                                         │
│ KEY     BPM       STYLE                 │
│ [Am]    [80]      [Acoustic ▼]          │
│                                         │
│ CHORDS                                  │
│ ┌────┬────┬────┬────┐                   │
│ │ Am │ F  │ C  │ G  │                   │
│ └────┴────┴────┴────┘                   │
│                                         │
│ STRUM                                   │
│ ↓  ↓  ↑  X  ↑  ↓  ↑                    │
│                                         │
│ LYRICS                                  │
│ 01 Freedom calls                        │
│ 02 I move forward                       │
│ 03 Courage grows                        │
│ 04 A new road                           │
│ ...                                     │
│ 12 Here I go                            │
│                                         │
│ [✨ WORDS] [🎲 CHORDS] [🔄 REMIX]       │
│                                         │
│ [ ▶ PERFORMANCE VIEW ]                  │
└─────────────────────────────────────────┘
```

---

# 🧱 MVP Functional Scope

## Must Have

```text
Theme input
Keywords
12 lines
Key
BPM
Chord progression
Strumming
Style
Save/load JSON
Performance view
```

---

# 🤖 AI

AI is:

```text
OPTIONAL
```

MVP moet handmatig bruikbaar zijn.

Wanneer Ollama beschikbaar is:

```text
[✨ WORDS]
```

kan keywords en regels voorstellen.

---

# 🎲 Chord Generator

Voor MVP:

```text
RULE BASED FIRST
```

Bijvoorbeeld:

```text
Am:
Am F C G
Am G F G
Am C G F
```

Random selection:

```text
🎲
```

is voldoende.

LLM chord generation kan eksperimenteel bly.

---

# 🎨 Style Presets

Begin klein:

```text
🔥 Campfire
🌫️ Shoegaze
🪩 Dance
🎹 Classical-ish
🖤 Dark
```

Elke preset kan bevatten:

```json
{
  "name": "Campfire",
  "bpm": 80,
  "strumming": ["D", "D", "U", "X", "U", "D", "U"]
}
```

---

# 🔄 Remix

Remix verandert bijvoorbeeld:

```text
STYLE
BPM
RHYTHM
```

maar behoudt:

```text
STORY
KEYWORDS
LYRICS
```

Dus:

```text
         SAME STORY
             │
       ┌─────┼─────┐
       ▼     ▼     ▼
    CAMP   DANCE  SHOEGAZE
```

---

# ▶ Performance View

Performance View verwijdert alle onnodige bediening.

```text
┌──────────────────────────────┐
│ 80 BPM       Am             │
│                              │
│ Am     F      C      G       │
│                              │
│ ↓ ↓ ↑ X ↑ ↓ ↑                │
│                              │
│ FREEDOM CALLS                │
│                              │
│ I MOVE FORWARD               │
│                              │
│ COURAGE GROWS                │
│                              │
└──────────────────────────────┘
```

Groot.

Leesbaar.

Geen instellingen.

---

# 📴 Offline

MVP moet kunnen draaien als:

```text
localhost
```

zonder internet.

---

# 💾 Persistence

Begin simpel:

```text
current-song.json
```

Later eventueel:

```text
songs/
session-001.json
session-002.json
...
```

Geen database in MVP.

---

# 🚫 Explicit Non-Goals

Niet in MVP:

```text
user accounts
cloud sync
payments
social network
complex DAW
audio synthesis engine
MIDI orchestration
multi-agent AI
vector database
enterprise architecture
mobile native app
```

Interessant?

Ja.

Nu nodig?

Nee.

---

# ⏱️ Bouwfilosofie

```text
2 UUR CODEREN
     ↓
BUITEN TESTEN
     ↓
LEREN
     ↓
AANPASSEN
```

Niet:

```text
2 WEKEN ARCHITECTUUR
      ↓
37 DOCUMENTEN
      ↓
NOG GEEN LIEDJE
```

---

# 🧪 MVP Acceptance Test

Het MVP slaagt wanneer:

```text
1. Open app

2. Enter:
   "new adventure"

3. Kies/generate keywords

4. Kies:
   Am
   80 BPM
   Campfire

5. Zie:
   chords
   rhythm
   12 lines

6. Open Performance View

7. Pak gitaar

8. Speel
```

Doel:

```text
IDEA → PLAY
< 5 MINUTES
```

---

# 🧭 North Star

```text
              STORY
                │
                ▼
             CHOICE
                │
                ▼
              MUSIC
                │
                ▼
             TOGETHER
```

---

# ⭐ Definition of Done

Het MVP is klaar wanneer het in een echte sessie bruikbaar is.

Niet wanneer:

```text
de code perfect is
```

maar wanneer:

```text
iemand een verhaal vertelt
        +
de Workbench helpt
        +
jullie daadwerkelijk spelen
```

---

# ⭐ Kernregel

> **Ship the smallest thing that gets the guitar playing.**

