---
type: capability-map
updated: {{date}}
counts: { R0: 0, R1: 0, R2: 0, R3: 0 }
---

# Capability map

| state | means |
| ----- | ----- |
| R0 | understands the rule |
| R1 | recognises it when listening or reading |
| R2 | produces it correctly with preparation |
| R3 | uses it automatically under pressure |

Built **complete** at setup for the configured target language. Later skills change state;
they do not build coverage incrementally — a map grown from errors alone can never contain
the structures the learner avoids.

**Movement rules — the single home. Every skill that changes a state reads them here.**

- **R1 → R2** — correct use *with preparation*, with a linked artifact.
- **R2 → R3** — correct use *unprompted*, twice, at least seven days apart.
- **Demotion** — any error on a row at R2 or R3 drops it one state and resets `next_due` to
  the first bucket.
- **No link, no move.** An empty `evidence` cell means the state did not change, and
  `lang-review-practice-week` reverts anything that moved without one.

The same ladder governs `lexicon.md` entries.

`next_due` follows `config.due_buckets`.

`band` records where a row sits on the framework in `config.cycle.benchmarks`, so the map can
be filtered by level without a second file. It describes the row, never the learner — the
learner's level lives in `profile.md` and only `lang-assess-level` writes it.

## Grammar

| id | capability | band | state | evidence | next_due |
| ---- | ---------- | ---- | ----- | -------- | -------- |
| G-01 | | | R0 | | |

## Functions

What the learner can *do* with the language, not what they know about it.

| id | function | band | state | evidence | next_due |
| ---- | -------- | ---- | ----- | -------- | -------- |
| F-01 | | | R0 | | |

## Phonology

| id | feature | intelligibility cost | band | state | evidence | next_due |
| ---- | ------- | -------------------- | ---- | ----- | -------- | -------- |
| P-01 | | | | R0 | | |
