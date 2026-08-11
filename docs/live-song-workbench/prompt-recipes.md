# 🤖 Prompt Recipes

> **Vliegbasis71 Live Song Workbench**
>
> Kleine, herbruikbare AI-prompts voor live songwriting, improvisatie,
> akkoordprogressies, woorden, mantra's en eenvoudige arrangementen.

---

## 1. Waarom Prompt Recipes?

Tijdens een live sessie wil je niet vijf minuten met een AI praten.

Je wilt dit:

```text
MENS VERTELT VERHAAL
        ↓
THEMA
        ↓
KORTE PROMPT
        ↓
LOCAL LLM
        ↓
BRUIKBARE SUGGESTIES
        ↓
MENS KIEST
        ↓
MUZIEK
```

De AI is geen songwriter die de sessie overneemt.

De AI is een **snelle ideeënmachine**.

De mens blijft beslissen.

---

# 2. Hoofdregel

Gebruik tijdens een live sessie liever:

```text
kleine prompt
     ↓
kleine output
     ↓
mens kiest
```

dan:

```text
enorme prompt
     ↓
enorm AI-antwoord
     ↓
iedereen wacht
     ↓
energie verdwijnt
```

!!! tip "Live-regel"
    Als de AI-output niet binnen enkele seconden begrijpelijk is,
    is de output waarschijnlijk te ingewikkeld voor de live sessie.

---

# 3. Recipe 01 — Thema → woorden

## Doel

Een deelnemer heeft een verhaal maar kan nog geen goede woorden bedenken.

## Prompt

```text
Theme: {THEME}

Generate 10 short uplifting keywords related to this theme.

Rules:
- simple language
- maximum 2 words per keyword
- emotionally useful
- suitable for songwriting
- no explanations

Return only the keywords.
```

## Voorbeeld

```text
Theme:

I left my job after 20 years for a new venture.
```

Mogelijke output:

```text
Freedom
Growth
Adventure
Courage
Opportunity
Confidence
New beginning
Vision
Discovery
Gratitude
```

De deelnemer kiest vervolgens bijvoorbeeld:

```text
Freedom
Adventure
Courage
Vision
```

---

# 4. Recipe 02 — Woorden → korte zinnen

## Prompt

```text
Use these keywords:

{KEYWORDS}

Create 12 short positive musical phrases.

Rules:
- 2 to 4 words per phrase
- one phrase per musical measure
- simple language
- easy to speak or sing
- no explanation
```

## Voorbeeld

```text
Freedom calls
New roads open
Courage grows
Adventure begins
```

---

# 5. Recipe 03 — Thema → 12-measure mantra

Dit is gebaseerd op een van de eerste lokale-LLM experimenten
voor de Workbench.

## Prompt

```text
I want to create a mantra song.

Theme:

"{THEME}"

First create 10 uplifting unique keywords related to the theme.

Then create minimalist positive phrases using those ideas.

Rules:

- total song length: 12 measures
- each phrase occupies one musical measure
- each phrase contains approximately 2 to 4 words
- simple language
- positive tone
- easy to repeat
- suitable for live looping

Output as a numbered 12-measure song.
```

---

# 6. Recipe 04 — Zeer snelle mantra

Voor live gebruik kan bovenstaande prompt nog kleiner.

```text
Theme: {THEME}

Create a 12-bar positive mantra.

2-4 words per bar.
Simple words.
Easy to sing.
No explanation.
```

Dit is waarschijnlijk beter wanneer snelheid belangrijk is.

---

# 7. Recipe 05 — 4-bar akkoordprogressie

## Prompt

```text
Create one simple 4-bar chord progression.

Key: {KEY}
Style: {STYLE}

Rules:
- one chord per bar
- beginner-friendly guitar chords
- musically coherent
- suitable for looping
- no explanation

Format:

1 | chord
2 | chord
3 | chord
4 | chord
```

## Voorbeeld

```text
Key: E minor
Style: acoustic campfire
```

Output kan bijvoorbeeld zijn:

```text
1 | Em
2 | C
3 | G
4 | D
```

---

# 8. Recipe 06 — 8-bar akkoordprogressie

```text
Create one 8-bar chord progression.

Key: A minor
Style: warm acoustic storytelling

Rules:
- beginner-friendly
- maximum one chord per bar
- strong loop back to bar 1
- avoid unusual jazz chords
- no explanation

Return bars 1-8 only.
```

---

# 9. Recipe 07 — Veilige gitaarprogressie

Kleine lokale modellen kunnen harmonisch vreemde antwoorden produceren.

Daarom kan de prompt strenger worden.

```text
Create a guitar chord progression.

Key: {KEY}

Use ONLY diatonic chords belonging naturally to the key.

Requirements:
- beginner friendly
- open chords preferred
- no modulation
- no slash chords
- no altered chords
- no diminished chords unless explicitly requested
- suitable for live looping

Return 4 bars only.
```

Dit vermindert het risico op output zoals:

```text
Dm6/Eb
C#m
B♭6/E♯
```

wanneer je eigenlijk een eenvoudige kampvuurprogressie nodig hebt.

---

# 10. Recipe 08 — Verse + Chorus

```text
Create a simple song progression.

Key: {KEY}

Structure:

Verse: 8 bars
Chorus: 8 bars

Requirements:
- beginner guitar
- maximum 4 different chords
- verse should feel calm
- chorus should feel slightly more uplifting
- both sections must loop naturally

Output only:

VERSE
1 |
2 |
...

CHORUS
1 |
2 |
...
```

---

# 11. Recipe 09 — Zelfde verhaal, andere stijl

Een belangrijk Workbench-principe is:

> Het verhaal blijft hetzelfde.
> De muzikale interpretatie mag veranderen.

Prompt:

```text
Reinterpret this song structure.

Original:

{SONG}

New style:

{STYLE}

Keep:
- theme
- emotional meaning
- basic song structure

Change:
- tempo suggestion
- chord voicing suggestions
- rhythm feel
- arrangement feel

Keep the result simple enough for live looping.
```

---

# 12. Recipe 10 — Acoustic

```text
Reinterpret this song as:

minimal acoustic guitar storytelling

Tempo:
70-90 BPM

Use:
- simple guitar chords
- relaxed strumming
- lots of space
- warm repetitive rhythm

Keep it easy to perform live.
```

---

# 13. Recipe 11 — Shoegaze

```text
Reinterpret this song as:

90s inspired shoegaze

Tempo:
100-125 BPM

Use:
- repeating guitar progression
- spacious rhythm
- reverb-heavy guitar concept
- simple bass foundation
- hypnotic repetition

Do not make the harmony complicated.
```

---

# 14. Recipe 12 — Techno

```text
Reinterpret this song as minimalist techno.

Tempo:
120 BPM

Keep the original emotional theme.

Use:
- repetitive harmonic loop
- strong pulse
- minimal chord changes
- gradual layering
- loop-friendly structure

Output a simple performance plan.
```

---

# 15. Recipe 13 — Baroque-inspired

```text
Reinterpret this song in a slow baroque-inspired style.

Tempo:
56-80 BPM

Use:
- elegant harmonic movement
- simple repeating bass concept
- restrained arrangement
- clear melodic space

It must still be playable by a small live-looping setup.
```

---

# 16. Recipe 14 — Strumming generator

```text
Create 4 guitar strumming patterns.

Time signature:
4/4

Use:

↓ = downstroke
↑ = upstroke
X = muted/rest stroke

Requirements:
- beginner friendly
- one bar each
- patterns must be clearly different
- suitable for acoustic guitar

No explanation.
```

Example:

```text
Pattern 1
↓ ↓ ↑ ↑ ↓ ↑

Pattern 2
↓ X ↓ ↑ X ↑

Pattern 3
↓ ↓ X ↑ ↓ ↑

Pattern 4
↓ X ↑ ↑ X ↑
```

---

# 17. Recipe 15 — Story interview helper

De Workbench kan ook helpen wanneer iemand zegt:

> "Ik weet niet waarover ik moet vertellen."

Prompt:

```text
Theme:

{THEME}

Generate 5 friendly storytelling questions.

Rules:
- easy to answer
- non-judgmental
- conversational
- start with concrete memories
- avoid therapy language
- do not pressure the person into vulnerability

Return questions only.
```

---

# 18. Recipe 16 — Van verhaal naar kernzin

```text
Story:

{STORY}

Find the emotional core of this story.

Return:

Theme:
3 keywords:
1 short sentence:

The sentence must contain maximum 8 words.
Do not psychoanalyse the storyteller.
```

---

# 19. Recipe 17 — Positieve reframing

```text
Story:

{STORY}

Generate 5 possible positive forward-looking interpretations.

Rules:
- preserve what actually happened
- do not deny difficult emotions
- do not invent facts
- simple language
- maximum 8 words each
```

De mens kiest.

De AI bepaalt niet wat het verhaal "werkelijk betekent".

---

# 20. Recipe 18 — Chorus hook

```text
Theme:

{THEME}

Keywords:

{KEYWORDS}

Create 8 possible chorus hooks.

Rules:
- maximum 6 words
- easy to remember
- easy to repeat
- positive or emotionally open
- suitable for group singing

Return hooks only.
```

---

# 21. Recipe 19 — Call and response

```text
Theme:

{THEME}

Create 6 simple call-and-response pairs.

Format:

CALL:
RESPONSE:

Rules:
- maximum 5 words per line
- easy for strangers to repeat
- no complicated melody required
- suitable for a live group
```

---

# 22. Recipe 20 — Instrumentrollen

De toekomstige Workbench hoeft niet alleen gitaar te ondersteunen.

```text
Song:

{SONG}

Available instruments:

{INSTRUMENTS}

Create a minimalist live-looping arrangement.

Rules:
- give every instrument one clear role
- avoid frequency clutter
- start small
- add layers gradually
- maximum 6 layers

Output:

Layer 1:
Layer 2:
...
```

Voorbeeld:

```text
Available instruments:

acoustic guitar
voice
bass synth
drum machine
```

---

# 23. Recipe 21 — Performance card

```text
Convert this song into a live performance card.

Song:

{SONG}

Output only:

TITLE
KEY
BPM
TIME SIGNATURE

INTRO
VERSE
CHORUS
OUTRO

CHORDS

STRUM

LOOP LAYERS

LYRICS

Keep everything readable on one screen.
```

Dit is belangrijk voor die toekomstige iPhone/MacBook-view.

---

# 24. Recipe 22 — JSON output

Wanneer die Workbench later deur software aangestuur word,
wil ons nie prose parse nie.

Ons wil gestruktureerde data hê.

```text
Create a simple live-looping song.

Theme:
{THEME}

Key:
{KEY}

Style:
{STYLE}

Return VALID JSON ONLY.

Schema:

{
  "title": "",
  "theme": "",
  "key": "",
  "bpm": 0,
  "time_signature": "4/4",
  "style": "",
  "sections": {
    "verse": [],
    "chorus": []
  },
  "lyrics": [],
  "keywords": [],
  "strumming_pattern": "",
  "loop_layers": []
}

Do not use Markdown.
Do not explain anything.
Return JSON only.
```

---

# 25. Waarom JSON?

De toekomstige architectuur kan dan heel eenvoudig zijn:

```text
┌─────────────────┐
│ STORY / THEME   │
└────────┬────────┘
         ↓
┌─────────────────┐
│ LOCAL LLM       │
│ phi4-mini etc.  │
└────────┬────────┘
         ↓
┌─────────────────┐
│ song.json       │
└────────┬────────┘
         ↓
┌─────────────────┐
│ LOCAL WEB APP   │
└────────┬────────┘
         ↓
┌─────────────────┐
│ PERFORMANCE UI  │
│                 │
│ Em  C  G  D     │
│ 80 BPM          │
│ ↓ ↓↑ ↑↓↑        │
│                 │
│ Freedom calls   │
│ New roads open  │
└─────────────────┘
```

De webinterface hoeft dan niet te begrijpen waarom de AI iets koos.

Hij hoeft alleen het JSON-contract te begrijpen.

---

# 26. Local LLM waarschuwing

Een lokaal taalmodel is geen muziektheorie-engine.

Een model kan overtuigend klinkende maar muzikaal verkeerde informatie produceren.

Bijvoorbeeld:

```text
Key: E minor

AI:
Em
Am
Dm
C#m
```

Dat moet niet automatisch als correct worden beschouwd.

Daarom:

```text
LLM
 │
 ▼
SUGGESTIE
 │
 ▼
VALIDATIE
 │
 ▼
MENS
 │
 ▼
PLAY
```

---

# 27. Twee AI-modi

De Workbench moet uiteindelijk onderscheid kunnen maken tussen:

## Creative Mode

```text
meer vrijheid
meer onverwachte ideeën
meer harmonische variatie
```

Gebruik voor:

- brainstorming;
- alternatieve stijlen;
- hooks;
- woorden;
- arrangementideeën.

## Safe Live Mode

```text
beperkte akkoorden
bekende progressies
eenvoudige ritmes
voorspelbare output
```

Gebruik wanneer iemand voor je zit en het lied binnen minuten gespeeld moet worden.

---

# 28. Safe Live Mode prompt

```text
You are assisting a live musician.

Speed and playability are more important than originality.

Generate the simplest musically valid answer.

Rules:

- beginner guitar
- maximum 4 chords
- no modulation
- no unusual chord names
- no jazz substitutions
- no theoretical explanation
- loop friendly
- concise output

Request:

{REQUEST}
```

---

# 29. Beginner Mode

```text
You are helping a beginner guitarist.

Use only common open guitar chords where possible.

Avoid:
- barre chords
- altered chords
- extended jazz chords
- difficult chord changes

Make the result playable immediately.

Request:

{REQUEST}
```

---

# 30. Facilitator Mode

```text
You assist a facilitator who is creating a song together with another person.

Important:

The participant owns the story.

You may:
- suggest words
- suggest questions
- suggest musical options

You may NOT:
- decide what the participant feels
- psychoanalyse the participant
- rewrite the story without permission
- turn the session into therapy

Offer small choices.

Request:

{REQUEST}
```

---

# 31. Eén belangrijk UX-principe

De gebruiker hoeft deze prompts later niet allemaal te zien.

De uiteindelijke interface kan gewoon knoppen hebben:

```text
┌─────────────────────────────────────┐
│          LIVE SONG WORKBENCH        │
├─────────────────────────────────────┤
│                                     │
│ Theme                               │
│ [ nieuwe start________________ ]    │
│                                     │
│ [ 💡 WOORDEN ]                      │
│ [ ✍️ 12 REGELS ]                    │
│ [ 🎸 AKKOORDEN ]                    │
│ [ 🥁 RITME ]                        │
│                                     │
│ Style                               │
│ [ Acoustic ▼ ]                      │
│                                     │
│ [ 🎵 MAAK LIED ]                    │
│                                     │
└─────────────────────────────────────┘
```

Achter:

```text
[ 🎸 AKKOORDEN ]
       ↓
prompt template
       ↓
local LLM
       ↓
JSON
       ↓
UI
```

De prompt recipes worden daarmee de interne taal tussen de Workbench en het model.

---

# 32. Human-first beslisboom

```text
Kan de persoon zelf iets bedenken?
        │
   ┌────┴────┐
   │         │
  JA        NEE
   │         │
   ▼         ▼
GEBRUIK    AI geeft
HUN IDEE   3-10 opties
             │
             ▼
        MENS KIEST
             │
             ▼
          VERDER
```

AI vult dus een stilte op.

AI vervangt niet de deelnemer.

---

# 33. Performance-first regel

Iedere AI-output moet uiteindelijk door deze vraag:

> **Kan ik dit binnen ongeveer tien seconden begrijpen en spelen?**

Zo niet:

```text
vereenvoudig
     ↓
vereenvoudig
     ↓
vereenvoudig
```

Een muzikaal theoretisch indrukwekkende output die live onbruikbaar is,
is voor deze Workbench een slechte output.

---

# 34. Prompt design checklist

Voor een nieuwe recipe:

```text
[ ] Heeft de prompt één duidelijke taak?
[ ] Is de gewenste output klein?
[ ] Is het formaat expliciet?
[ ] Zijn muzikale beperkingen expliciet?
[ ] Kan een klein lokaal model dit begrijpen?
[ ] Kan output eenvoudig gevalideerd worden?
[ ] Kan de facilitator binnen seconden kiezen?
[ ] Blijft de deelnemer eigenaar van het verhaal?
```

---

# 35. Phi4-mini experiment

De vroege experimenten tonen precies waarom de Workbench zowel interessant
als voorzichtig ontworpen moet worden.

Het model kan snel:

```text
thema
  ↓
keywords
  ↓
phrases
```

genereren.

Dat is uitstekend bruikbaar.

Maar bij muziektheorie kan het bijvoorbeeld ingewikkelde of foutieve
progressies produceren.

Daarom is de gewenste taakverdeling:

| Functie | LLM | Software | Mens |
|---|---:|---:|---:|
| Keywords bedenken | ★★★ | ★ | ★★★ |
| Korte zinnen voorstellen | ★★★ | ★ | ★★★ |
| Verhaalvragen | ★★★ | ★ | ★★★ |
| Akkoorden voorstellen | ★★ | ★★★ | ★★★ |
| Key-validatie | ★ | ★★★ | ★★ |
| BPM kiezen | ★★ | ★★ | ★★★ |
| Muzikale smaak | ★★ | ★ | ★★★ |
| Betekenis verhaal | ★ | ★ | ★★★ |
| Eindkeuze | — | — | ★★★ |

---

# 36. Het uiteindelijke principe

De Workbench probeert niet:

> AI maakt binnen twintig seconden een perfect lied.

De bedoeling is:

> Twee mensen kunnen binnen enkele minuten iets maken
> dat daarvoor nog niet bestond.

AI kan helpen wanneer het gesprek vastloopt.

De gitaar kan helpen wanneer woorden tekortschieten.

Een ritme kan helpen wanneer iemand niet wil zingen.

En soms is één regel al genoeg.

```text
VERHAAL
   ↓
WOORD
   ↓
RITME
   ↓
AKKOORD
   ↓
STEM
   ↓
SAMEN SPELEN
```

Dat is de kern van de Prompt Recipes.

---

## Volgende documenten

Zie ook:

- `quick-start.md`
- `local-llm.md`
- `keyword-generator.md`
- `phrase-generator.md`
- `chord-progressions.md`
- `json-contract.md`
- `performance-view.md`
- `ai-system/app-builder-master-prompt.md`

