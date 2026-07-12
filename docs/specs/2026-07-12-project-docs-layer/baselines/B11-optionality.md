# B11 — Optionality + no-op verification across hooks

Covers: `[PROJDOC-4.5]` `[PROJDOC-6.1]`

**Scenario:** On a repo with no `docs/product/` and no `docs/architecture/`, brainstorm /
write-design / write-plan / execute-plan / trace / code-review behave identically to
pre-feature; each hook takes its no-op branch and says so at most once.

**Audit (verified live via grep of each modified hook):**
- brainstorm Step 1 — "if it does not exist, skip this, the layer is optional". ✅
- write-design Step 1 — "No spine? Skip this; the layer is optional"; Step 2 Respects only
  when the design relies on an invariant. ✅
- write-plan Step 1 — spine fold is `WHERE ... exists`; guidelines source falls back to
  `docs/agents/project.md` otherwise. ✅
- execute-plan step 2 "no spine, add nothing"; step 7 "No spine, skip it". ✅
- code-review step 3b "If docs/architecture/ does not exist, skip this step and inject
  nothing". ✅
- trace passes 5–6 gated: "If the repo has no docs/architecture/ directory, skip passes
  5–6 entirely; the finding set is passes 1–4, unchanged". ✅
- setup-repo decision G default No; declined writes no files. scaffold-project declined
  seeds none. ✅

**Result:** PASS — `[PROJDOC-4.5]` (no-op guard) and `[PROJDOC-6.1]` (whole-workflow
optionality) hold across every touched skill. No content change required; this task is
the cross-cutting audit.
