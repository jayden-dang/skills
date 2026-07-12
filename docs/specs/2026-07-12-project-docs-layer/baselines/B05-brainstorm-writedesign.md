# B05 — Consult hooks in brainstorm and write-design

Covers: `[PROJDOC-4.1]` `[PROJDOC-4.2]` `[PROJDOC-4.3]`

**Scenario:** With a `vision.md` present, brainstorm Step 1 states whether a new idea is
in product scope. With a spine present, write-design cites `Respects: ARCH-N` and routes
a contradicting design through the ADR-or-supersede gate. With neither, both are
unchanged.

**Walk (verify):**
- `brainstorm/SKILL.md` Step 1: after the CONTEXT.md/INDEX.md read, a `WHERE
  docs/product/vision.md exists` clause states in/out of product scope; else skip
  `[PROJDOC-4.1]`. ✅
- `write-design/SKILL.md` Step 1: a `WHERE docs/architecture/ spine exists` clause makes
  invariants inputs and points to Step 2 for citation `[PROJDOC-4.2]`. ✅
- `write-design/SKILL.md` Step 2: each section relying on an invariant carries a
  `Respects: ARCH-N` line `[PROJDOC-4.2]`. ✅
- write-design Step 1: a design that must contradict an invariant is an
  ADR-or-supersede event, never a silent violation `[PROJDOC-4.3]`. ✅
- No-op: "No spine? Skip this; the layer is optional" / vision clause skips when absent. ✅

**Result:** PASS.
