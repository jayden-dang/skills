# `configure-repo` — tests

## author-skills wording pass — Catalog sync Decision L (v1.3.1)

**RED (open-code-review + catalog-sync design):** brownfield reconcile/map ran
without setup; teams wanting INDEX-only sync had no posture field. Description
had drifted into a packed feature list.

**GREEN:**
- User-invoked description is one plain human line (deliverable = docs/agents
  config), no keyword packing
- Decision L explains INDEX-only opt-in, points at `catalog-sync.md`, defaults
  **unset**, never force index-only; rationalization table for silent gitignore
- Write step 11 appends gitignore snippet only when L=`index-only`

## Edit — gitignore `.worktrees/` not `.isolate-workspace/` (v1.4.0)

**RED (v1.3.1):** Step 1 markers and Write step 8 added `.isolate-workspace/` to
`.gitignore`, a second isolation parent beside the conventional `.worktrees/`.

**GREEN:** local working-dir ignore is `.skills/` and `.worktrees/`. An existing
`.isolate-workspace/` line is left in place (additive); a new one is not written.
