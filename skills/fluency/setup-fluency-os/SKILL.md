---
name: setup-fluency-os
description: Install or remap a fluency practice vault — config, profile, capability map, lexicon, error log, and dashboard.
disable-model-invocation: true
---

# Setup Fluency OS

## Role

REQUIRED: read sibling `ROLE.md` (coach default, produce-first, evidence gate, config paths).

## Contract

Setup leaves six files and six directories, in this order: `config.md` from the learner's
answers, a complete `capability-map.md`, three empty-but-valid ledgers, a dashboard, and the
event directories. Every path in it was confirmed by the learner before it was written.

## Recipe

1. Confirm the vault root with the learner. Existing folder of notes → map their folders to roles; greenfield → propose the shape below and get consent before creating anything.
2. Interview for `config.md`. REQUIRED before any other file: `languages.target`, `languages.support`, `schedule.*`, `pronunciation.accent_anchor`, `themes` (totalling 100), `materials_blend`, `language_policy`, `ai_policy`, `cycle.weeks`, `limits.*`. Every value comes from the learner or from the template default — the target language, the accent, and the level framework are read from answers, never inferred from who the learner appears to be.
3. Seed `capability-map.md` **complete for `languages.target`**: grammar `G-*`, communicative functions `F-*`, and phonology `P-*` covering everything the learner needs up to the ceiling in `cycle.benchmarks` (or, with no benchmark named, up to advanced everyday plus their professional domain). Every row opens at R0 (understands the rule) with an empty evidence cell. Completeness here is what makes the avoidance set visible later; a map grown from errors alone can only ever contain what already went wrong.
4. Seed the remaining ledgers empty but valid: `profile.md`, `errors.md`, `lexicon.md`.
5. Write `README.md` as the dashboard: current state, live focus, links to every ledger and the newest event notes.
6. Create the event directories: `cycles/`, `sessions/`, `reviews/`, `assessments/`, `sources/`, `artifacts/`, `lexicon/` (word study notes).
7. REQUIRED SUB-SKILL: use `plan-cycle` to open cycle 1.

## Vault shape (proposal, not a mandate)

```text
<vault>/
  README.md            config.md    profile.md
  capability-map.md    lexicon.md   errors.md
  cycles/  sessions/  reviews/  assessments/  sources/  artifacts/  lexicon/
```

Templates for every note live in `templates/fluency-os/` at the repository root.

## Red flags

- A capability map seeded with a handful of example rows instead of full coverage
- A target language, accent, or framework filled in without the learner saying it
- A folder created or renamed before the learner agreed to the mapping
- Ledgers written before `config.md` exists

## Done when

`config.md` valid; four ledgers exist; `capability-map.md` complete for the target language; dashboard links resolve; no folder created without consent; cycle 1 opened.
