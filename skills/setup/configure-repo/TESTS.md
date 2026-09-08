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

## Edit — drop session-start hook offer (v1.7.0)

**RED:** Step 5 still offered to vendor a `SessionStart` hook that injected
`zone-mode` (or leftover `gate-session` copies) at startup / clear / compact.

**GREEN:** Step 5 offers Context7 MCP only. No session-start template is
copied. `/zone-mode` is user-run. Version 1.6.1 → 1.7.0.

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

## v1.8.0 — cold-start drive recipe (Decision M)

**Roster:** grok-4.5 only (this edit).

**RED (v1.6.1, no Decision M).** Fixture `plainsetup`: Vite
notes app, `"dev": "vite"` in `package.json`, user locked A–L and Context7 skip,
never mentioned booting or clicking. Agent wrote `docs/agents/project.md` with
**Run locally (dev)** Backend/API row blank and no Frontend command, and no
`docs/agents/verify.md`. `DONE.txt` listed only the existing wizard outputs.

When a second fixture (`notewell`) *did* ask for a cold-start click path, the
same model improvised `docs/agents/drive.md` — so the job is doable, but the
wizard does not produce it unless the user already knows to ask.

A third fixture (`paperkite`) was given the same extra ask. It **reported**
option A (recipe written and one feature proven) while the tree only had
`project.md` / `issue-tracker.md` / `triage-labels.md` — no `verify.md`, no
`drive.md`. Score the files, not the letter.

Verbatim cost: a later agent has to invent `npm run dev` and the create-note
click path; **Run locally** shipped empty on a repo that had a `dev` script.

**GREEN (v1.8.0, grok-4.5 ×2, fixtures `notecove` / `papercove`).** Same locked
A–L plus **Yes** on Decision M. Install and long-running server forbidden
(`drive: unproven` allowed).

Both wrote `docs/agents/verify.md` with Launch, Doctor, Drive, Evidence,
Cleanup, Features. Both filled **Run locally** Frontend as `npm run dev` /
`http://localhost:5173`. Both named a reload persist check. RED's empty
Frontend row did not recur.

**No-ops recorded the same day, not written.** research "code is not intent"
2/2; reroute-plan scrap 2/2 Design-level; design-solution graft 2/2 (forcing
`snapshot()` lost to YAGNI). A leaked speak-outer menu stayed dry; an unleaked
PR-body prompt shipped em dashes and is recorded on speak-outer v1.1.0.
design-solution v1.5.0 names `/tour-system` when the author has never read the
subsystem. On-ramps gained a `/tour-system` row.
