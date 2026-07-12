# B04 — trace referential-integrity extension

Covers: `[PROJDOC-3.1]` `[PROJDOC-3.2]` `[PROJDOC-3.3]` `[PROJDOC-3.4]` `[PROJDOC-3.5]`

**Scenario:** On a fixture with `docs/architecture/INDEX.md` (ARCH-1, ARCH-2 live;
ARCH-9 struck) and a `design.md` citing ARCH-1, ARCH-9, ARCH-5, `trace` reports W3 for
the uncited live ARCH-2, E5 for the retired ARCH-9, E4 for the undefined ARCH-5. On a
repo with no `docs/architecture/`, the finding set is byte-identical to today.

**Walk (verify):** — executed live in the Task 4 fixture run:
- retired set = `{ARCH-9}`, live set = `{ARCH-1, ARCH-2}`, cited = `{ARCH-1, ARCH-9, ARCH-5}`. ✅
- Rule E4 → ARCH-5 (cited, in neither set) `[PROJDOC-3.1]`. ✅
- Rule E5 → ARCH-9 (cited, retired) `[PROJDOC-3.2]`. ✅
- Rule W3 → ARCH-2 (live, uncited) `[PROJDOC-3.3]`. ✅
- `<NON-NEGOTIABLE>` extended: invariant passes check existence/liveness only; semantic
  respect is deferred to check-invariants/code-review `[PROJDOC-3.4]`. ✅
- Passes 5–6 gated on `docs/architecture/` existing; absent → E1–E3/W1–W2 unchanged
  `[PROJDOC-3.5]`. ✅

**Result:** PASS — grep passes verified live; rules and gating documented in
`skills/execution/trace/SKILL.md`.
