# 📦 JSON Contract

> **De JSON-laag maakt de AI vervangbaar en de interface stabiel.**

De Workbench mag niet afhankelijk zijn van de precieze tekst die een LLM produceert.

Daarom:

```text
LLM
 ↓
JSON
 ↓
WORKBENCH
```

---

# 🎯 MVP Song Object

```json
{
  "version": "1.0",
  "theme": "new beginning",
  "mode": "5-minute",
  "key": "Am",
  "bpm": 80,
  "time_signature": "4/4",
  "style": "acoustic",
  "progression": [
    "Am",
    "F",
    "C",
    "G"
  ],
  "strumming": "D D U X U D U",
  "keywords": [
    "freedom",
    "courage",
    "future"
  ],
  "lines": [
    "Freedom calls",
    "I move forward",
    "Courage grows",
    "A new road",
    "Future opens",
    "I keep moving",
    "Something changes",
    "I choose today",
    "Freedom calls",
    "Courage grows",
    "I step forward",
    "Here I go"
  ]
}
```

---

# 🧱 Waarom een contract?

Zonder contract:

```text
MODEL A
"Here is your beautiful song..."

MODEL B
| Bar | Chord |

MODEL C
Sure! 🎸

MODEL D
```json ...
```
```

De UI moet dan alles proberen te begrijpen.

Dat is fragiel.

Met contract:

```text
MODEL
   ↓
KNOWN STRUCTURE
   ↓
VALIDATION
   ↓
UI
```

---

# 📐 Minimum Required Fields

Voor MVP:

```text
version
theme
key
bpm
progression
lines
```

Andere velden mogen defaults hebben.

---

# 🎚️ BPM

```json
"bpm": 80
```

Validatie bijvoorbeeld:

```text
30 ≤ BPM ≤ 330
```

---

# 🎼 Key

```json
"key": "Am"
```

Gebruik eenvoudige canonieke namen.

Bijvoorbeeld:

```text
C
G
D
A
E
F

Am
Em
Dm
Bm
```

MVP hoeft nog geen theoretisch complete enharmonische engine te zijn.

---

# 🎸 Progression

```json
"progression": [
  "Am",
  "F",
  "C",
  "G"
]
```

De UI kan dit visualiseren als:

```text
┌──────┬──────┬──────┬──────┐
│  Am  │  F   │  C   │  G   │
└──────┴──────┴──────┴──────┘
```

---

# 🥁 Strumming

Machine representation:

```json
"strumming": [
  "D",
  "D",
  "U",
  "X",
  "U",
  "D",
  "U"
]
```

Display:

```text
↓  ↓  ↑  X  ↑  ↓  ↑
```

---

# ✍️ Lines

Elke regel correspondeert in de eenvoudige MVP met één measure:

```text
BAR 01 → Freedom calls
BAR 02 → I move forward
BAR 03 → Courage grows
...
BAR 12 → Here I go
```

---

# 🧩 Uitgebreidere toekomstige structuur

Later:

```json
{
  "sections": [
    {
      "name": "verse",
      "bars": 8
    },
    {
      "name": "chorus",
      "bars": 8
    }
  ]
}
```

Maar dit hoeft niet in MVP.

---

# 🤖 AI Response

De LLM moet geen Markdown teruggeven.

Niet:

```text
Sure! Here's your JSON:
```

Gewenst:

```json
{
  "keywords": [
    "freedom",
    "growth",
    "courage"
  ]
}
```

---

# 🛡️ Validator

Pseudo-flow:

```text
receive JSON
     ↓
parse
     ↓
valid JSON?
 ├── NO → reject
 └── YES
       ↓
required fields?
 ├── NO → fallback
 └── YES
       ↓
music values valid?
 ├── NO → repair/default
 └── YES
       ↓
display
```

---

# 🎨 UI Independence

Dezelfde JSON kan later worden weergegeven als:

```text
📱 MOBILE CARD
💻 WEB WORKBENCH
🖨️ PRINT SHEET
🎸 PERFORMANCE VIEW
🎹 KEYBOARD VIEW
```

zonder de LLM te veranderen.

---

# 📂 Bestand

Bijvoorbeeld:

```text
data/current-song.json
```

De lokale website leest:

```text
current-song.json
```

en rendert de huidige sessie.

---

# 🔄 Eerste simpele architectuur

```text
       OLLAMA
          │
          ▼
      Python
          │
          ▼
current-song.json
          │
          ▼
      browser
          │
          ▼
┌───────────────────────┐
│  Am  F  C  G          │
│                       │
│  ↓ ↓ ↑ X ↑ ↓ ↑        │
│                       │
│  Freedom calls        │
│  Courage grows        │
└───────────────────────┘
```

Geen database nodig.

Geen cloud nodig.

Geen framework nodig.

---

# ⭐ Kernregel

> **De UI praat met een datastructuur, niet rechtstreeks met de persoonlijkheid van een taalmodel.**

