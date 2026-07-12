# B08 — code-review advisory invariant lane

Covers: `[PROJDOC-8.2]` `[PROJDOC-8.5]`

**Scenario:** With a spine present, code-review runs check-invariants and reports verdicts
under `## Invariants (advisory)`, separate from Standards/Spec; with no spine, code-review
is unchanged.

**Walk (verify):**
- `code-review/SKILL.md` step 3b (Invariant conformance, advisory): `WHERE
  docs/architecture/ exists`, run `check-invariants`; hold verdicts for step 5
  `[PROJDOC-8.2]`. ✅
- Step 5 aggregate presents verdicts under a separate `## Invariants (advisory)` heading,
  never merged/reranked into the two hard axes, never a merge blocker `[PROJDOC-8.2]`. ✅
- step 3b "If docs/architecture/ does not exist, skip this step and inject nothing" →
  two-axis behavior unchanged `[PROJDOC-8.5]`. ✅

**Result:** PASS.
