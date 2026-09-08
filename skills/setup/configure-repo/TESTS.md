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

## Length pass — SKILL.md 365 → 194 lines (v1.6.1, 2026-09-07)

**RED (repo-wide length ratchet, `scripts/lint-skill-length.py`):** SKILL.md
was 365 lines / 115 rule atoms — too rule-dense (3.2 lines/atom) to shrink by
prose-tightening alone; the file has two machine-checked eval anchors
(`§ 2. Decide, one section at a time`, `§ 4. Write`) that must survive intact.

**GREEN — extraction, following the existing `team-inference.md` pointer
pattern:**
- New siblings, each loaded via `**WHEN <condition>, read \`<file>.md\`... and
  follow it exactly**`: `issue-tracker-followups.md` (Decision A's option
  definitions, PR-surface/Publish-unit/Program-sync follow-ups, write-scope
  table, IC-default rule), `triage-label-mapping.md` (Decision B's canonical-
  roles table + mapping recipe), `project-docs-layer.md` (Decision I),
  `remote-environments.md` (Decision K, decision + Step 4 item 10 write step),
  `catalog-sync-choice.md` (Decision L's explainer/options + Step 4 item 11
  write step — the Thought/Reality gate table for L stays inline per the
  gate-block rule), `optional-offers.md` (Step 5's session-start-hook install
  and Context7 recommendation).
- `team-inference.md` gained the "why this decision matters" / user-explainer
  / recommend prose moved out of Decision H (its Thought/Reality gate table
  stayed inline, same gate rule).
- Two literal file-content blocks (the `## Agent skills` block and the
  `CLAUDE.md` pointer, both written verbatim into the target repo) moved to
  `templates/agent-skills-block.md` and `templates/claude-md-pointer.md`,
  following this file's own existing `templates/` seeding convention (Step 4
  item 7 now reads "seeded verbatim from `templates/...`").
- Decisions C, D, E, F, G, J (no skip predicate — reached by every run) were
  tightened by merging their Explainer / Confirm / Done-when paragraphs into
  one paragraph each (no bullet or fact dropped), per the universal-bucket
  rule ("tighten wording ... moving it behind a pointer buys nothing").
  Several hard-wrapped lines were reflowed to single lines (Decision K/L
  bullets before their move, the Step 1 "Seed files" bullet, Step 4 item 2,
  the Step 2 intro sentence) — pure whitespace, no wording change.
- Nothing was deleted as a no-op or duplicate in this pass; every relocated
  block was moved verbatim (`skill-rule-inventory.py --diff` confirms all 115
  atoms have a home across SKILL.md + the 8 new/extended siblings, and every
  sibling filename is named in SKILL.md so none is orphaned).
- Both eval anchors (`## 2. Decide, one section at a time`, `## 4. Write`)
  verified present verbatim; `lint-skill-evals.py` and the rest of the
  `scripts/lint-*.py` suite pass for this file.

**Numbers:** 365 → 194 lines (115 → 89 atoms in SKILL.md itself, 26 atoms
moved into siblings). Version bumped 1.6.0 → 1.6.1 (patch: wording/location
only, no behavior change). `scripts/skill-length-budget.json` entry for this
file removed (now under the 200-line limit).

### Reviewer note — two pointers are phase-scoped, not skip-scoped

`triage-label-mapping.md` and `optional-offers.md` sit behind "WHEN this decision
runs" and "WHEN this step runs", which are not skip predicates: every run reaches
both. Under the plain reading of the information-hierarchy rule that buys nothing
and adds a hop.

Kept, because this skill is a long interactive walk-through and the saving is real
in a different shape. Decision B's label tables are loaded while Decision B is
being worked and are not carried through Decision K; the body pays for the walk,
not for every branch of it at once. `team-inference.md`, shipped here well before
this pass, uses the same "WHEN Decision H runs" form, so this is the file's
existing convention rather than a new one.

The distinction matters for anyone repeating this: a pointer earns its place
either because some runs skip it, or because it is scoped to one phase of a long
run. A pointer that is neither is just an extra hop.
