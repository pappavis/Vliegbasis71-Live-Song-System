# 🧠 Local LLM

> **De lokale LLM is een snelle muzikale assistent, geen componist die de sessie overneemt.**

Voor de eerste experimenten kan de Workbench lokaal draaien met:

```text
Ollama
   +
phi4-mini
```

Het doel is niet maximale AI-intelligentie.

Het doel is:

```text
FAST
+
LOCAL
+
PREDICTABLE
+
GOOD ENOUGH
```

---

# 🎯 Eerste use cases

De lokale LLM hoeft aanvankelijk slechts vier dingen goed te kunnen.

```text
┌──────────────────────────┐
│ 1. KEYWORDS              │
├──────────────────────────┤
│ 2. SHORT LINES           │
├──────────────────────────┤
│ 3. CHORD PROGRESSIONS    │
├──────────────────────────┤
│ 4. STYLE VARIATIONS      │
└──────────────────────────┘
```

---

# 1. Keywords

Input:

```text
Theme:
I left my job after 20 years for a new venture.
```

Output bijvoorbeeld:

```text
freedom
growth
adventure
courage
future
change
confidence
possibility
journey
beginning
```

De gebruiker kiest.

AI beslist niet.

---

# 2. Short Lines

Van:

```text
freedom
courage
new beginning
```

naar bijvoorbeeld:

```text
Freedom calls

Courage grows

I step forward

Something begins
```

Doel:

```text
2–4 woorden
per muzikale maat
```

Niet automatisch poëzie van twintig regels.

---

# 3. Chord Progressions

Voorbeeldvraag:

```text
Create an easy 4-chord guitar progression.

Key: E minor
Bars: 8
Skill: beginner
Mood: uplifting
Open chords preferred.
```

Gewenste respons:

```text
Em | C | G | D
Em | C | G | D
```

---

# ⚠️ LLM Music Hallucination

Een taalmodel kan overtuigend klinkende muzikale onzin produceren.

Bijvoorbeeld:

```text
E minor progression

Em
Am
Dm
C#m
```

Dit moet niet automatisch als correct worden beschouwd.

De Workbench moet daarom uiteindelijk:

```text
LLM
 ↓
PROPOSAL
 ↓
VALIDATOR
 ↓
DISPLAY
```

gebruiken.

---

# 🎼 Safe Chord Library

Voor MVP is een deterministische bibliotheek vaak beter dan AI.

Bijvoorbeeld:

```json
{
  "E_minor": [
    ["Em", "C", "G", "D"],
    ["Em", "G", "D", "C"],
    ["Em", "D", "C", "D"]
  ]
}
```

Dan kan AI bijvoorbeeld zeggen:

```text
"use progression 2"
```

in plaats van zelf exotische akkoorden te verzinnen.

---

# 🧠 Hybrid Model

Dit geeft:

```text
             USER
               │
               ▼
             THEME
               │
       ┌───────┴───────┐
       ▼               ▼
     LLM            RULE ENGINE
       │               │
   keywords          chords
   phrases           rhythm
   style             safe notes
       │               │
       └───────┬───────┘
               ▼
             SONG
```

Dit is waarschijnlijk sterker dan alles door de LLM laten genereren.

---

# ⚡ Latency

Live gebruik verandert de eisen.

Een antwoord dat technisch correct is maar twintig seconden duurt voelt tijdens een sessie langzaam.

Daarom:

```text
0–2 sec     excellent
2–5 sec     usable
5–10 sec    noticeable
10+ sec     disrupts flow
```

Dit zijn UX-richtlijnen, geen harde technische garanties.

---

# ✂️ Kleine prompts

Niet:

```text
You are one of the greatest composers...
```

plus 900 woorden instructies.

Voor live gebruik:

```text
Theme: new beginning
Task: 10 positive keywords
Output: JSON only
```

---

# 🎛️ Prompt Recipes

## Keywords

```text
Generate 10 positive unique keywords.

Theme:
{{theme}}

Use simple language.

Return JSON only.
```

---

## Mantra Lines

```text
Create 12 short mantra lines.

Theme:
{{theme}}

Use these keywords:
{{keywords}}

Rules:
- 2 to 4 words per line
- positive
- easy to speak
- one line per musical measure

Return JSON only.
```

---

## Chords

```text
Select an easy chord progression.

Key:
{{key}}

Bars:
{{bars}}

Mood:
{{mood}}

Skill:
beginner

Prefer open guitar chords.

Return JSON only.
```

---

# 🔄 Variation Prompt

```text
Keep the story and words.

Create a new musical interpretation.

Current:
80 BPM
Acoustic
Am F C G

New style:
Shoegaze

Return JSON only.
```

---

# 🎹 Instrument Independence

Later kan die output meer as kitaar ondersteun:

```text
SONG MODEL
    │
    ├── guitar
    ├── piano
    ├── bass
    ├── synth
    ├── drums
    └── voice
```

Die verhaal bly dieselfde.

Die arrangement verander.

---

# 🚫 Geen chain-of-thought nodig

Die live app het nie die model se interne redenasie nodig nie.

Wat nuttig is:

```json
{
  "choice": "Em-C-G-D",
  "reason": "easy open chords, uplifting movement"
}
```

Kort verduideliking.

Nie bladsye interne redenasie nie.

---

# 🧪 Local Model Test

Voordat ’n model in die Workbench kom:

```text
TEST 1
keyword generation

TEST 2
12 short lines

TEST 3
valid chord progression

TEST 4
JSON compliance

TEST 5
response speed
```

---

# ⭐ Kernregel

> **Gebruik die LLM vir idees; gebruik reëls vir dinge wat musikale korrekheid vereis.**
