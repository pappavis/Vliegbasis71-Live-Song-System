# 🧱 MVP — Minimum Viable Workbench

> **Bouw alleen wat nodig is om een verhaal snel in speelbare muziek te veranderen.**

De Vliegbasis71 Live Song Workbench kan uiteindelijk enorm uitgebreid worden.

Dat betekent niet dat dit verstandig is.

De eerste versie heeft één taak:

> Een facilitator en deelnemer helpen om binnen enkele minuten van een verhaal naar een eenvoudig speelbaar liedje te gaan.

---

# 🎯 MVP-doel

```text
VERHAAL
   ↓
WOORDEN
   ↓
12 REGELS
   ↓
MUZIEKRECEPT
   ↓
LIVE SPELEN
```

Als dit betrouwbaar werkt, bestaat het product.

Al het andere is uitbreiding.

---

# 👤 Gebruikers

## Facilitator

De facilitator:

- stelt vragen;
- luistert;
- speelt eventueel gitaar;
- bedient de Workbench;
- bewaakt het tempo van de sessie.

## Deelnemer

De deelnemer:

- vertelt;
- kiest woorden;
- accepteert of verandert regels;
- bepaalt wat persoonlijk mag blijven;
- kan spreken, neuriën, zingen of alleen luisteren.

## Nieuwsgierige beginner

Een derde belangrijke gebruiker is iemand die denkt:

> "Dit lijkt me gaaf, maar ik weet weinig van songwriting."

Daarom moet de documentatie ook uitleggen **waarom** iets gebeurt.

---

# 🧭 MVP-functionaliteit

| Capability | MVP |
|---|:---:|
| Verhaal invoeren | ✅ |
| Keywords invoeren | ✅ |
| Keywords laten voorstellen | ✅ |
| 12 regels maken | ✅ |
| Regel handmatig aanpassen | ✅ |
| Alternatieve regel vragen | ✅ |
| BPM kiezen | ✅ |
| Toonsoort kiezen | ✅ |
| Akkoordprogressie kiezen | ✅ |
| Strumming pattern tonen | ✅ |
| Eenvoudige stijl kiezen | ✅ |
| Mobiele weergave | ✅ |
| Printbare kaart | ✅ |
| Offline werken | ✅ |
| Lokale LLM optioneel | ✅ |
| MIDI-output | ❌ later |
| Audio genereren | ❌ later |
| DAW | ❌ |
| Accounts | ❌ |
| Cloud database | ❌ |
| Multi-agent AI | ❌ |
| Automatische mastering | ❌ |

---

# 🧠 De belangrijkste architectuurregel

```text
                 WORKBENCH

         ┌──────────┼──────────┐
         ▼          ▼          ▼

       HUMAN       LLM        CODE

      meaning     ideas     structure
      choice    variants    validation
      consent   keywords     12 = 12
```

Geen van deze drie moet de andere vervangen.

---

# 🤖 Waarom de LLM niet de structuur beheert

Tijdens vroege experimenten bleek al iets nuttigs:

Een model kan gevraagd worden:

> "Maak een liedje van exact twaalf maten."

en vervolgens minder dan twaalf regels produceren.

Dat betekent niet dat het model nutteloos is.

Het betekent dat we het gebruiken waar het sterk in is:

```text
LLM
 ↓
ideeën
woorden
alternatieven
herformuleringen
```

en gewone software waar die sterker in is:

```text
CODE
 ↓
exact 12 regels
geldige JSON
verplichte velden
BPM-bereik
akkoordvelden
```

---

# 📦 Conceptueel JSON-model

Een toekomstige kleine app kan bijvoorbeeld met een structuur werken zoals:

```json
{
  "title": "Nieuwe Weg",
  "theme": "Een nieuw begin",
  "key": "Am",
  "bpm": 80,
  "style": "acoustic",
  "progression": ["Am", "F", "C", "G"],
  "strumming": "D D U X U D U",
  "measures": [
    {"measure": 1, "text": "Ik laat los"},
    {"measure": 2, "text": "Een nieuwe weg"},
    {"measure": 3, "text": "Vandaag begint"},
    {"measure": 4, "text": "Ik kies vooruit"}
  ]
}
```

!!! note

    Dit is nog geen definitief JSON-contract.
    Het definitieve contract wordt beschreven in `ai/json-contract.md`.

---

# 🖥️ De kleinste technische implementatie

De MVP hoeft aanvankelijk niet meer te zijn dan:

```text
BROWSER
   │
   ▼
LOCAL HTML / JS
   │
   ├── song data
   ├── recipes
   └── display
          │
          ▼
      OPTIONAL API
          │
          ▼
        OLLAMA
          │
          ▼
      LOCAL MODEL
```

Dat heeft een paar voordelen:

- geen cloud nodig;
- geen account nodig;
- snel te bouwen;
- gemakkelijk op laptop te testen;
- HTML-interface kan later mobiel worden verbeterd;
- AI kan vervangen worden zonder de hele Workbench te herschrijven.

---

# 📴 Offline-first

Een belangrijk ontwerpprincipe:

> **Geen AI mag betekenen: minder functies, niet: systeem onbruikbaar.**

Dus:

```text
           INTERNET?
              │
         maakt niet uit
              │
              ▼
           WORKBENCH
              │
      ┌───────┴───────┐
      ▼               ▼
 MANUAL MODE       LOCAL AI
      │               │
      └───────┬───────┘
              ▼
             SONG
```

---

# 📱 Mobiel eerst denken

In een park wil niemand een spreadsheet met 47 velden bedienen.

De belangrijkste informatie moet groot zichtbaar zijn:

```text
┌──────────────────────────┐
│ NIEUWE WEG               │
│                          │
│ Am · 80 BPM              │
│ Am  F  C  G              │
├──────────────────────────┤
│                          │
│ 01  Ik laat los          │
│ 02  Een nieuwe weg       │
│ 03  Vandaag begint       │
│ 04  Ik kies vooruit      │
│                          │
│       ...                │
│                          │
├──────────────────────────┤
│ [WORDS] [LINES] [MUSIC]  │
└──────────────────────────┘
```

Tijdens spelen is leesbaarheid belangrijker dan configuratiemogelijkheden.

---

# 🎼 Recipe-first

Een beginner hoeft niet iedere keer een liedje vanaf nul te ontwerpen.

Daarom gebruikt de MVP kant-en-klare recepten.

Bijvoorbeeld:

## Happy Strummer

```text
Key: G
BPM: 86
Chords: G - D - Em - C
Rhythm: ↓ ↓↑ X ↑↓↑
```

## Reflective

```text
Key: Am
BPM: 68
Chords: Am - F - C - G
Rhythm: ↓ X ↓ ↑
```

## Slow Story

```text
Key: Em
BPM: 56
Chords: Em - C - G - D
Rhythm: ↓ . . .
```

Klik.

Speel.

Pas later aan.

---

# 🎨 Style is geen nieuw lied

Een belangrijk concept:

```text
STORY DATA
   │
   ├── words
   ├── lines
   └── meaning
        │
        ▼
   MUSIC ENGINE
        │
 ┌──────┼───────┐
 ▼      ▼       ▼
folk  techno  classical
```

Daarom moeten verhaal en muzikale presentatie technisch gescheiden blijven.

Dat maakt latere remix-functionaliteit veel eenvoudiger.

---

# ✋ KEEP / EDIT / OTHER

AI-output mag nooit voelen alsof de gebruiker het moet accepteren.

Voor iedere voorgestelde regel:

```text
"Vrijheid roept"

[ KEEP ]
[ EDIT ]
[ OTHER ]
```

### KEEP

Gebruik de regel.

### EDIT

De mens verandert hem.

### OTHER

Vraag nieuwe alternatieven.

Dit kleine patroon is belangrijker dan een ingewikkelde AI-chatinterface.

---

# 🧪 Definition of Done voor MVP v0.1

Een eerste versie is bruikbaar wanneer dit scenario werkt:

```text
1. Facilitator opent Workbench.

2. Deelnemer vertelt kort verhaal.

3. Facilitator voert thema/woorden in.

4. Workbench toont twaalf regels.

5. Iedere regel kan gewijzigd worden.

6. Gebruiker kiest muziekrecipe.

7. Workbench toont:
      key
      BPM
      chords
      rhythm
      twaalf regels

8. Interface is leesbaar tijdens gitaar spelen.

9. Sessie kan zonder internet doorgaan.

10. Eindresultaat kan eenvoudig
    opnieuw bekeken worden.
```

Dat is voldoende voor v0.1.

---

# 🚫 Anti-scope-creep

Wanneer tijdens ontwikkeling iemand zegt:

> "We kunnen ook meteen MIDI..."

of:

> "Wat als we hier een database..."

of:

> "Eigenlijk kunnen vijf agents..."

stel dan eerst:

> **Helpt dit Johan en Aletta om binnen vijf minuten hun verhaal te spelen?**

Zo niet:

```text
IDEA
  ↓
BACKLOG
```

Niet:

```text
IDEA
  ↓
DRIE DAGEN CODEREN
  ↓
WAAROM SPEEL IK GEEN GITAAR MEER?
```

---

# 🌱 Progressive Enhancement

De Workbench mag groeien in lagen.

```text
LEVEL 0
papier + gitaar

    ↓

LEVEL 1
telefoon + recepten

    ↓

LEVEL 2
interactive web Workbench

    ↓

LEVEL 3
lokale LLM

    ↓

LEVEL 4
MIDI / looper integration

    ↓

LEVEL 5
meer instrumenten / arrangement
```

Iedere laag moet zelfstandig nuttig blijven.

---

# 🧪 Wat testen we in het veld?

Niet alleen softwarebugs.

Observeer:

| Vraag | Waarom |
|---|---|
| Begrijpt iemand de eerste vraag? | conversation UX |
| Hoe snel komen woorden? | workflow |
| Zijn 12 regels te veel/weinig? | song structure |
| Kan facilitator tegelijk bedienen en spelen? | live UX |
| Is tekst groot genoeg? | mobile UX |
| Helpt AI werkelijk? | AI value |
| Wanneer wordt AI irritant? | AI boundary |
| Wanneer voelt het lied als "van ons"? | North Star |

---

# ⭐ De echte succesmaat

Niet:

> "Heeft het model perfecte poëzie geproduceerd?"

Niet:

> "Was de akkoordprogressie harmonisch innovatief?"

Maar:

```text
VERTELLER
   ↓
hoort resultaat
   ↓
glimlacht
   ↓
"Ha!
Dat is mijn verhaal."
```

Daar begint Vliegbasis71.

