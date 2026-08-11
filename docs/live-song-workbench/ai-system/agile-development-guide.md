# 🏃 Agile Development Guide

The Live Song Workbench is developed in small, playable increments.

## Development loop

```text
FIELD EXPERIENCE
      ↓
OBSERVATION
      ↓
USER STORY
      ↓
SMALLEST VERTICAL SLICE
      ↓
IMPLEMENT
      ↓
TEST
      ↓
PLAY
      ↓
LEARN
      └───────────────↺
```

## Product hierarchy

```text
VISION
  │
  ▼
EPIC
  │
  ▼
USER STORY
  │
  ▼
ACCEPTANCE CRITERIA
  │
  ▼
CODE
  │
  ▼
TEST
  │
  ▼
FIELD VALIDATION
```

A feature is valuable only when it improves a real song-making session.

---

## Story template

```markdown
# LSW-US-XXX — Title

## User Story

As a ...
I want ...
so that ...

## Business Value

...

## Acceptance Criteria

- Given ...
  When ...
  Then ...

## Out of Scope

...

## Dependencies

...

## Test Evidence

...
```

---

## Engineering principles

```text
CLASS-BASED
+
NO MUTABLE GLOBAL VARIABLES
+
EXPLICIT DEPENDENCIES
+
SMALL CLASSES
+
CLEAR RESPONSIBILITIES
+
TESTABLE SERVICES
+
REPLACEABLE AI PROVIDERS
```

Prefer:

```text
SongService
   │
   ├── SongRepository
   ├── AIProvider
   └── MusicRuleEngine
```

over:

```text
main.py
  ↓
2,700 lines
  ↓
globals everywhere
```

---

## YAGNI rule

Before adding something:

```text
Does the current user story need it?
             │
        ┌────┴────┐
        │         │
       YES        NO
        │         │
       BUILD    BACKLOG
```

---

## AI rule

AI suggestions are proposals.

```text
AI
 ↓
SUGGEST
 ↓
HUMAN CHOOSES
```

For deterministic musical constraints:

```text
RULE ENGINE
 ↓
VALIDATE
```

---

## Field-test rule

After a meaningful increment:

**stop coding and use it.**

The primary laboratory is not the IDE.

It is:

```text
🎸 + 👤 + 👤
```

---

## Definition of Done

```text
☑ acceptance criteria satisfied
☑ tests passing
☑ no mutable global state
☑ class responsibilities remain clear
☑ offline/manual fallback works
☑ documentation consistent
☑ mkdocs build --strict passes
☑ feature usable during an actual session
```

## North Star

> Build less. Test sooner. Play more.
