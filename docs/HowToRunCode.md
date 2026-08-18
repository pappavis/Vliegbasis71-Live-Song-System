<!--
File     : HowToRunCode.md
Version  : 0.2.1
ChatID   : 2D7A4C91
Purpose  : Handleiding voor het uitvoeren van alle unit tests via commandline en VS Code.
-->

# How to run alle unit tests

Deze handleiding beschrijft hoe je alle unit tests van **Vliegbasis71 Live Song System / MuScriptor Batch Converter** in één keer uitvoert vanuit de commandline of vanuit VS Code.

## Release

- **Version:** 0.2.1
- **ChatID:** 2D7A4C91

## Projectstructuur

De relevante projectstructuur is:

```text
Vliegbasis71-Live-Song-System/
├── pyproject.toml
├── src/
│   └── muscriptor_batch.py
└── tests/
    ├── __init__.py
    ├── test_muscriptor_batch.py
    ├── test_muscriptor_batch_red_streaming.py
    ├── test_release_metadata_red.py
    └── test_source_traceability.py
```

## Alle tests uitvoeren vanaf de commandline

Ga eerst naar de project-root:

```bash
cd "/Volumes/data1/Yandex.Disk.localized/michiele/Programmering/Python/python_normaal/github_python_normaal/Vliegbasis71-Live-Song-System"
```

Controleer indien gewenst welke Python-interpreter actief is:

```bash
which python
```

Voor de huidige ontwikkelomgeving wordt verwacht:

```text
/Users/michiele/venv/venv3.12/bin/python
```

Voer vervolgens de volledige unittest-suite uit:

```bash
python -m unittest discover -s tests -t . -v
```

Betekenis:

- `python -m unittest` — start Python `unittest`.
- `discover` — zoekt automatisch naar tests.
- `-s tests` — gebruikt `tests/` als startdirectory.
- `-t .` — gebruikt de project-root als top-level directory.
- `-v` — verbose output; toont iedere test afzonderlijk.

Bij een volledig succesvolle run eindigt de uitvoer ongeveer met:

```text
----------------------------------------------------------------------
Ran 28 tests in ...

OK
```

> **Acceptance gate:** voordat een GREEN-phase als voltooid wordt beschouwd, moet de volledige regressiesuite groen zijn.

Omdat het project editable is geïnstalleerd:

```bash
python -m pip install -e .
```

is normaal gesproken geen `PYTHONPATH=src` meer nodig.

## Alle tests uitvoeren vanuit VS Code

VS Code heeft ingebouwde ondersteuning voor Python unit tests.

Open eerst de volledige projectdirectory **Vliegbasis71-Live-Song-System** in VS Code.

Open daarna de Command Palette:

```text
Shift + Command + P
```

Op macOS kan hiervoor ook `⇧⌘P` worden gebruikt.

Kies:

```text
Python: Configure Tests
```

Selecteer vervolgens:

```text
unittest
```

en kies als testdirectory:

```text
tests
```

VS Code ontdekt vervolgens de tests.

## Test Explorer

Open in de VS Code Activity Bar het **Testing**-icoon.

De structuur ziet er ongeveer als volgt uit:

```text
TEST EXPLORER

Vliegbasis71-Live-Song-System
└── tests
    ├── test_muscriptor_batch
    │   ├── CommandBuilderTests
    │   ├── ConfigurationManagerTests
    │   ├── ConverterTests
    │   └── JobResolverTests
    │
    ├── test_muscriptor_batch_red_streaming
    │   └── LiveCommandOutputRedPhaseTests
    │
    ├── test_release_metadata_red
    │   └── ReleaseMetadataRedPhaseTests
    │
    └── test_source_traceability
        └── SourceTraceabilityTests
```

Gebruik bovenaan **Run All Tests** om de volledige suite uit te voeren.

Vanuit Test Explorer kun je ook:

- één individuele test uitvoeren;
- één `TestCase` uitvoeren;
- één testbestand uitvoeren;
- alle tests uitvoeren;
- een test onder de debugger starten.

## Aanbevolen TDD-workflow

Voor iedere nieuwe feature gebruiken we:

```text
RED
 │
 ├─ Schrijf eerst de nieuwe test(s)
 ├─ Voer de relevante tests uit
 └─ Bewijs dat ze om de juiste reden falen
       │
       ▼
GREEN
 │
 ├─ Implementeer minimale productiecode
 ├─ Voer de nieuwe tests opnieuw uit
 └─ Maak de nieuwe tests groen
       │
       ▼
REFACTOR
 │
 ├─ Verbeter de implementatie
 └─ Houd alle tests groen
       │
       ▼
FULL REGRESSION / ACCEPTANCE GATE
 │
 └─ python -m unittest discover -s tests -t . -v
```

Tijdens de RED/GREEN-cyclus is VS Code Test Explorer handig om snel één test of testgroep te draaien.

Voor de uiteindelijke acceptance gate wordt altijd de volledige suite uitgevoerd:

```bash
python -m unittest discover -s tests -t . -v
```

Alle tests moeten eindigen met:

```text
OK
```

## Eén specifieke test uitvoeren

Een individuele test kan vanaf de commandline bijvoorbeeld zo worden gestart:

```bash
python -m unittest   tests.test_muscriptor_batch.ConverterTests.test_midi_conversion_calls_muscriptor_and_checks_output   -v
```

Dit is vooral handig tijdens de RED/GREEN-cyclus.

## Problemen met imports

Als je bijvoorbeeld krijgt:

```text
ModuleNotFoundError: No module named 'muscriptor_batch'
```

controleer eerst de actieve interpreter:

```bash
which python
```

en controleer vervolgens of het project editable is geïnstalleerd:

```bash
python -m pip show vliegbasis71-live-song-system
```

Zo nodig installeer je het project vanuit de project-root opnieuw:

```bash
python -m pip install -e .
```

Controleer daarna:

```bash
python -c "import muscriptor_batch; print(muscriptor_batch.__file__)"
```

Dit moet verwijzen naar:

```text
.../Vliegbasis71-Live-Song-System/src/muscriptor_batch.py
```

## Release-traceability

Alle sourcebestanden moeten in hun header minimaal bevatten:

```text
Version
ChatID
```

De regressietest:

```text
tests/test_source_traceability.py
```

controleert deze afspraak automatisch voor de Python-sourcebestanden onder `src/` en `tests/`.

De applicatie-UI toont eveneens de release-identiteit, bijvoorbeeld:

```text
Version 0.2.1 · ChatID 2D7A4C91
```

Hierdoor kan bij een testresultaat, screenshot of bugmelding worden vastgesteld tegen welke release van de code is getest.
