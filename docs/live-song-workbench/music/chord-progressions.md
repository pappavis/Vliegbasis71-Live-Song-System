# 🎸 Chord Progressions

> **Tijdens een live sessie is een eenvoudige progressie die je direct kunt spelen waardevoller dan een briljante progressie waar je drie minuten over moet nadenken.**

De Live Song Workbench gebruikt daarom eerst een bibliotheek van veilige, speelbare akkoordprogressies.

AI mag later variaties voorstellen.

De basis hoeft niet door AI bedacht te worden.

---

# 🎯 Ontwerpprincipe

```text
THEMA
   ↓
SONG STRUCTURE
   ↓
KEY
   ↓
SAFE PROGRESSION
   ↓
PLAY
```

Niet:

```text
THEMA
   ↓
LLM
   ↓
12 exotische akkoorden
   ↓
"Eh..."
   ↓
sessie staat stil
```

---

# 🧱 Progressies als graden

De Workbench bewaart progressies bij voorkeur eerst als akkoordgraden.

Bijvoorbeeld:

```text
I - V - vi - IV
```

In G majeur:

```text
G - D - Em - C
```

In C majeur:

```text
C - G - Am - F
```

In D majeur:

```text
D - A - Bm - G
```

Hierdoor kan één recept eenvoudig worden getransponeerd.

---

# 🟢 Beginner Library

## Major 01 — Open Road

```text
I - V - vi - IV
```

Voorbeeld G:

```text
G | D | Em | C
```

Karakter:

- vertrouwd;
- open;
- uplifting;
- geschikt voor verhalen;
- gemakkelijk te loopen.

---

## Major 02 — Home

```text
I - IV - V - IV
```

G:

```text
G | C | D | C
```

Goed voor:

- kampvuur;
- eenvoudige mantra;
- call-and-response.

---

## Major 03 — Forward

```text
I - vi - IV - V
```

G:

```text
G | Em | C | D
```

Geeft iets meer beweging.

---

# 🌙 Minor Library

## Minor 01 — Journey

```text
i - VI - III - VII
```

A minor:

```text
Am | F | C | G
```

Dit is een belangrijke Workbench-default.

---

## Minor 02 — Reflect

```text
i - VII - VI - VII
```

A minor:

```text
Am | G | F | G
```

Goed voor:

- reflectieve verhalen;
- rustige loops;
- spoken word.

---

## Minor 03 — Rise

```text
i - VI - VII - i
```

A minor:

```text
Am | F | G | Am
```

Heel eenvoudig.

Sterke terugkeer naar thuis.

---

# 🎸 Happy Strummer Keys

Voor de eerste versie geven we voorkeur aan gitaristische toonsoorten zoals:

```text
G major
C major
D major
A minor
E minor
```

Niet omdat andere toonsoorten verkeerd zijn.

Maar omdat open akkoorden hier vaak praktisch bruikbaar zijn.

---

# 🎛️ Workbench Selector

De gebruiker hoeft muziektheorie niet te kennen.

```text
┌──────────────────────────┐
│ 🎸 CHORDS               │
├──────────────────────────┤
│ Mood                     │
│                          │
│ [ Happy ]                │
│ [ Reflective ]           │
│ [ Adventure ]            │
│ [ Dark ]                 │
│                          │
│ Key                      │
│ [ A minor ▼ ]            │
│                          │
│ Progression              │
│ Am · F · C · G           │
│                          │
│ [🎲 OTHER] [✓ USE]       │
└──────────────────────────┘
```

---

# 🔁 12-bar mapping

Voor een vier-akkoordenprogressie:

```text
Am F C G
```

over twaalf maten:

```text
01 Am
02 F
03 C
04 G

05 Am
06 F
07 C
08 G

09 Am
10 F
11 C
12 G
```

Extreem voorspelbaar.

Dat is tijdens live co-creatie juist een voordeel.

---

# 🧩 Andere mapping

Niet ieder akkoord hoeft één maat te duren.

Later kan bijvoorbeeld:

```text
| Am     | F      |
| C      | G      |
```

of:

```text
| Am  F  | C  G   |
```

Maar MVP:

> één akkoord per maat.

---

# 🧠 Beginner versus Explorer

## 🟢 Beginner

```text
Am
F
C
G
```

## 🟡 Explorer

```text
Am7
Fmaj7
Cadd9
Gsus4
```

## 🔴 Advanced — later

```text
inversions
secondary dominants
borrowed chords
voice leading
modal interchange
```

Niet nodig voor MVP.

---

# 🤖 Rol van de lokale LLM

De LLM kan bijvoorbeeld ontvangen:

```text
Theme:
starting a new adventure

Key:
A minor

Base progression:
Am F C G

Give 3 stylistic variations.
Keep every chord easily playable on guitar.
```

Maar de Workbench valideert de uitkomst.

---

# 🛡️ Harmonic Guardrail

```text
              LLM
               │
        chord suggestion
               │
               ▼
        ┌──────────────┐
        │ VALIDATOR    │
        └──────────────┘
          │          │
        VALID      INVALID
          │          │
          ▼          ▼
        SHOW       REJECT
```

Voor MVP hoeft dit nog geen complexe muziektheorie-engine te zijn.

Een whitelist is voldoende.

---

# 📦 Progression Object

Conceptueel:

```json
{
  "id": "minor_01",
  "name": "Journey",
  "mode": "minor",
  "degrees": ["i", "VI", "III", "VII"],
  "key": "A minor",
  "chords": ["Am", "F", "C", "G"],
  "difficulty": "beginner"
}
```

---

# 🎤 Facilitator Shortcut

Tijdens een live sessie:

> "Wil je dat het vrolijk, rustig, donker of avontuurlijk klinkt?"

De deelnemer hoeft niet te antwoorden:

> "Ik verkies een i–VI–III–VII-progressie."

😛

Menselijke taal aan de voorkant.

Muziektheorie achter de schermen.

---

# 🧭 Mood Mapping

```text
VROLIJK
   ↓
G / C major

REFLECTIEF
   ↓
Am / Em

AVONTUUR
   ↓
major progression + hoger tempo

INTIEM
   ↓
minor + lager tempo
```

Dit zijn defaults.

Geen natuurwetten.

---

# ⭐ Kernregel

> **De beste live progressie is degene die de speler niet meer hoeft te bedenken.**

