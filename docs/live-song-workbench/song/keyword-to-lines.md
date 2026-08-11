# 🔑 Keyword to Lines

> **Een heel verhaal is moeilijk te zingen. Drie goede woorden zijn veel makkelijker.**

Deze stap vertaalt gesprek naar compacte muzikale taal.

---

# 🧭 De pipeline

```text
VERHAAL
   ↓
10 MOGELIJKE WOORDEN
   ↓
3–5 GEKOZEN WOORDEN
   ↓
KORTE GEDACHTEN
   ↓
2–4 WOORDEN
   ↓
MUZIKALE REGELS
```

---

# 1. Begin bij het verhaal

Fictieve deelnemer **Aletta** vertelt:

> "Na twintig jaar bij hetzelfde bedrijf ben ik weggegaan. Ik vond het spannend, maar ik wilde eindelijk mijn eigen onderneming proberen."

Mogelijke woorden:

```text
vrijheid
groei
avontuur
kans
moed
ervaring
toekomst
keuze
vertrouwen
begin
```

---

# 2. De mens kiest

De AI kan tien woorden voorstellen.

Aletta kiest:

```text
vrijheid
moed
ervaring
begin
```

Waarom?

Omdat het haar verhaal is.

Niet omdat een taalmodel ze het hoogst rankt.

---

# 🧠 Human-in-the-loop

```text
          AI
          │
     suggesties
          │
          ▼
       MENS
   kiest / wijzigt
          │
          ▼
       LIEDJE
```

AI is hier brainstormpartner.

Niet auteur met vetorecht.

---

# 3. Van keyword naar gedachte

Keyword:

```text
vrijheid
```

Te abstract:

> "Vrijheid vertegenwoordigt de mogelijkheid om nieuwe levenskeuzes te omarmen."

Niet bruikbaar live.

Maak klein:

```text
Vrijheid roept
```

of:

```text
Ik kies vrijheid
```

---

# 4. De 2–4 woorden-regel

Voor het mantra-recept gebruiken we als sterke default:

```text
MINIMUM: 2 woorden
TARGET:  2–4 woorden
```

Voorbeelden:

```text
Moed groeit

Nieuwe deuren openen

Ik kies vandaag

Ervaring draagt mij

Avontuur begint nu
```

---

# 🥁 Waarom kort?

Omdat korte regels ruimte laten voor:

- adem;
- herhaling;
- ritme;
- publiek;
- call-and-response;
- improvisatie;
- instrumentale ruimte.

Vergelijk:

```text
Ik heb na twintig jaar eindelijk besloten
dat ik een nieuwe richting wil inslaan
```

met:

```text
Twintig jaar

Nieuwe richting

Ik kies

Ik ga
```

De tweede versie laat muziek binnen.

---

# 🎵 Eén gedachte per maat

Default:

```text
1 maat
=
1 compacte gedachte
```

Bijvoorbeeld:

| Maat | Regel |
|---:|---|
| 1 | Twintig jaar |
| 2 | Ervaring blijft |
| 3 | Nieuwe deuren |
| 4 | Ik kies |
| 5 | Vrijheid roept |
| 6 | Moed groeit |
| 7 | Stap vooruit |
| 8 | Ik vertrouw |
| 9 | Avontuur wacht |
| 10 | Vandaag begin ik |
| 11 | Mijn eigen weg |
| 12 | Ik ga |

---

# 🧩 Geen rijmdwang

Vliegbasis71 vereist niet:

```text
AABB
ABAB
AAAA
```

Een mantra kan krachtiger zijn zonder rijm.

Het eerste doel is:

```text
BETEKENIS
+
RITME
+
ZINGBAARHEID
```

Rijm is optioneel.

---

# 👄 Spreektest

Lees iedere regel hardop.

Bijvoorbeeld:

```text
Nieuwe mogelijkheden ontvouwen
```

Mogelijk te formeel.

Vergelijk:

```text
Nieuwe deuren
```

of:

```text
Iets nieuws begint
```

Gebruik gewone spreektaal.

---

# 🥁 Klaptest

Klap een eenvoudige vierkwartsmaat.

```text
1   2   3   4
👏  👏  👏  👏
```

Zeg:

```text
VRIJ-HEID ROEPT
```

Voelt het bruikbaar?

Prima.

De exacte melodie komt later.

---

# 🗣️ Preserve the Speaker

Als Aletta zelf zegt:

> "Ik ben nog niet klaar."

en dat blijkt een belangrijke zin:

Gebruik niet automatisch AI om daarvan te maken:

> "Mijn reis blijft zich ontvouwen."

De eerste zin klinkt misschien veel meer als Aletta.

---

# 🔄 Drie transformatieniveaus

## Level 1 — letterlijk

Verhaal:

> "Ik ga gewoon proberen."

Regel:

```text
Ik ga proberen
```

## Level 2 — compact

```text
Gewoon proberen
```

## Level 3 — poëtisch

```text
De deur staat open
```

De deelnemer kiest.

---

# 🤖 Local LLM Prompt

Een eenvoudige offline prompt:

```text
You are helping with a live collaborative mantra song.

Theme:
"I left my job after 20 years for a new venture."

Generate exactly 10 unique uplifting keywords.

Then generate 12 minimalist positive song lines.

Rules:
- each line is 2 to 4 words
- each line represents one musical measure
- use simple everyday language
- use the keywords naturally
- avoid long explanations
- do not force rhyme
- keep the tone hopeful
```

---

# ⚡ Live Prompt

Tijdens een echte sessie moet de prompt veel korter kunnen.

```text
Theme:
new venture after 20 years

10 positive keywords.
Then 12 lines.
2-4 words each.
Simple.
Uplifting.
```

---

# 🎛️ Workbench Interaction

Ideaal:

```text
THEME
[ New venture after 20 years ]

        [ GENERATE WORDS ]

              ↓

☐ freedom
☐ growth
☑ courage
☐ potential
☑ adventure
☑ experience
☐ opportunity
☐ confidence
☑ beginning
☐ vision

        [ MAKE LINES ]
```

Daarna:

```text
01  Courage grows       [✓] [↻]
02  Adventure calls     [✓] [↻]
03  Experience stays    [✓] [↻]
04  New beginning       [✓] [↻]
```

`↻` betekent:

> geef alleen voor deze regel alternatieven.

Niet:

> genereer het hele lied opnieuw.

---

# 💡 Dit is belangrijk

Tijdens samenwerking wil je niet:

```text
GENEREER
↓
niet goed
↓
GENEREER ALLES OPNIEUW
↓
bijna goed
↓
GENEREER ALLES OPNIEUW
```

Je wilt:

```text
GOEDE REGELS
    🔒 LOCK

SLECHTE REGEL
    ↻ REGENERATE
```

Zo blijft menselijke voortgang behouden.

---

# 🧠 AI Rescue Mode

Als de deelnemer niets kan bedenken:

```text
AI → 10 woorden
```

Als woorden er wel zijn maar geen regels:

```text
AI → regelvoorstellen
```

Als er al goede regels zijn:

```text
AI → niets
```

Dit is bewust.

---

# 🧪 Quality Check

Iedere regel kan vier simpele checks krijgen:

| Check | Vraag |
|---|---|
| Kort | 2–4 woorden? |
| Eigen | past het bij de verteller? |
| Spreekbaar | klinkt het natuurlijk? |
| Speelbaar | past het ongeveer in één maat? |

Vier keer ja?

Gebruik hem.

---

# 📱 Ultra-korte kaart

```text
┌────────────────────────────┐
│ 🔑 WORD → LINE            │
├────────────────────────────┤
│                            │
│ STORY                      │
│   ↓                        │
│ WORDS                      │
│   ↓                        │
│ CHOOSE 3–5                 │
│   ↓                        │
│ 2–4 WORD LINES             │
│   ↓                        │
│ SAY IT                     │
│   ↓                        │
│ PLAY IT                    │
│                            │
│ AI suggests.               │
│ Human chooses.             │
└────────────────────────────┘
```

---

# ⭐ Kernregel

> **Laat AI meer mogelijkheden maken. Laat de mens bepalen welke woorden betekenis hebben.**

