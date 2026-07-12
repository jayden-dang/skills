# B06 — execute-plan invariant awareness

Covers: `[PROJDOC-4.6]` `[PROJDOC-4.7]`

**Scenario:** With a spine present, an execute-plan task brief lists the invariants
relevant to the task's files, and the task review runs check-invariants, routing a
`violates` verdict back for fixes. With no spine, briefs and reviews are unchanged.

**Walk (verify):**
- Per-Task Loop step 2 (Build the brief): `WHERE a docs/architecture/ spine exists`, the
  brief lists the ARCH-N invariants relevant to the task's touched files `[PROJDOC-4.6]`. ✅
- Per-Task Loop step 7 (task reviewer): `WHERE a spine exists`, run `check-invariants` on
  the diff; a `violates` verdict routes through the fix loop (step 8) `[PROJDOC-4.6]`. ✅
- Both clauses end "no spine, add nothing / skip it" → unchanged behavior `[PROJDOC-4.7]`. ✅
- No new execute-plan mechanics beyond these two additive clauses; Global Constraints
  inheritance untouched. ✅

**Result:** PASS.
