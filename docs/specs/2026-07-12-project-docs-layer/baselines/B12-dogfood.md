# B12 — Dogfood spine + DESIGN/AGENTS/guide reconciliation

Covers: `[PROJDOC-6.2]`

**Scenario:** This repo has `docs/architecture/INDEX.md` with ARCH-1..5
(determinism-of-trace, optionality, zero-tooling, ID immutability, sub-skill
composition); DESIGN.md/AGENTS.md/guide agree on 35 skills and describe the project
layer; the feature adds no mandatory tooling or gate.

**Walk (verify):**
- `docs/architecture/INDEX.md` exists with ARCH-1..5, each a bold ID + one imperative
  rule. ✅
- The PROJDOC `design.md` cites all five (`Respects: ARCH-1..5`); trace's invariant
  passes run clean on the real repo — live={ARCH-1..5}, cited={ARCH-1..5}, E4/E5/W3 none
  (verified live). ✅
- DESIGN.md gains "The project layer (optional)" section; inventory lists
  `establish-project` (#35, project/) and `check-invariants` (#22); count reads 35;
  "not in v1" no longer lists planning maps. ✅
- AGENTS.md header + file-org read 35 skills / 10 categories, with project/ +
  check-invariants added; guide overview + skill-model + skills/README read 35 / ten
  buckets; new guide pages exist for both skills. ✅
- No mandatory tooling, no generated artifact requiring refresh, no new hard gate — the
  one deterministic addition (trace E4/E5/W3) extends an existing agent-run check
  `[PROJDOC-6.2]`. ✅

**Result:** PASS.
