# RED baselines — RMAP roadmap layer

Recorded per the `author-skills` Iron Law: no new skill and no edit to a skill ships
without a failing test first, and the failures must be **observed**, not guessed.

**IDs in this file are baseline records, not coverage.** It is Audit Trace-ignored.

## Method

Three baseline agents, each given a realistic user request and no roadmap skill.

**First run was contaminated and is discarded for two of three agents.** The spec triad
(`docs/specs/2026-07-25-roadmap/`) and `templates/roadmap-INDEX.md` had already been
committed, so agents A and C read them off disk and complied — agent C cited RMAP-1.11,
RMAP-1.17 and RMAP-1.19 by ID. That measures compliance, not baseline behavior. Only
agent B was usable, because it never consulted the spec.

**Re-run** against a sanitized copy of the repo with `docs/specs/`, `tests/`, and
`templates/roadmap-INDEX.md` removed. Verified by `grep -rl 'RMAP-\|MILE-\|ROAD-\|roadmap-INDEX'`
returning nothing before dispatch.

| Agent | Request | Environment |
|---|---|---|
| A | Author a roadmap for a note app from four work items plus two stated dependencies | sanitized |
| B | Review and finalize a hand-written draft roadmap containing a forward dependency and a surface repeated across three milestones | scratchpad, never read the spec |
| C | Apply three material changes to an already-approved roadmap | sanitized |

## Confirmed failures

### RMAP-1.1 — no durable, conventional home

B wrote the roadmap to a scratchpad temp directory. A invented
`docs/product/roadmap.md`, reasoning that the product-docs layer "holds only those two
files — a roadmap is an addition to that layer". Two agents, two different locations,
neither reproducible.

### RMAP-1.2 — no testable outcome; commitment conflated with progress

A's table columns were `ID | Milestone | Depends on | Status | Notes`. No milestone
carried an outcome sentence a reader could test it against, and there was no commitment
state distinct from progress.

### RMAP-1.7 — a dropped item is deleted, not deferred

C, asked to drop one item:

> "item-4: removed entirely. […] `item-4 search-ui` was deleted along with its
> separating comma; no other reference to item-4 existed in the file."

No date, no reason, no record that the item ever existed.

### RMAP-1.11 / RMAP-1.12 — renumbering under reorder

B, after moving a milestone earlier:

> "I renumbered so Storage rework runs second (right after Capture), pushing Search and
> Sharing to third and fourth"

C did **not** fail this — it kept `M1`/`M2`/`M3` and moved only row position, reasoning
from "AGENTS.md ID rule, applied here by analogy". One of two baselines failed, so the
rule is load-bearing but not universally missing.

### RMAP-1.17 — no approval gate

All three agents finalized without stopping. A's rationalization, verbatim:

> "nothing in this doc modifies shipped product behavior, code, or other files — it is a
> new, standalone planning artifact the user asked for directly, so none of this repo's
> approval gates (which govern requirements/code changes) apply."

### RMAP-1.19 — `Approved` survives a material change

C left `Status: Approved` untouched after dropping a member, reordering milestones, and
rewriting an outcome sentence. Verbatim rationalization:

> "you are the approving stakeholder and you are the one directing this exact edit right
> now, in real time — this isn't drift or a third party's unilateral change to an
> approved artifact, it's you exercising your own approval authority to amend-feature it."

This is the sharpest rationalization in the set and needs an explicit counter.

### RMAP-1.20 — no surface declaration

Neither A nor B recorded which components or paths a milestone's items would touch, so
nothing existed for a consolidation check to run against.

### Decision 1 (derive, never store) — the strongest failure

A invented **two** roadmap-level progress stores unprompted:

> "Status values — Reuses this repo's existing feature-status vocabulary (Draft →
> Approved → Implemented → Shipped) at milestone granularity"

and

> "Added a `Change log` section (dated bullet entries […]) as the mechanism for recording
> status changes over time"

Left alone, an agent rebuilds exactly the duplicated, drift-prone status store the design
rejects. This validates the derive-not-store decision empirically rather than by argument.

## No failure observed — candidate no-ops

### RMAP-1.5 — forward dependency

B caught it unprompted, first finding, correctly diagnosed:

> "Milestone 2 (Search) is scheduled before Milestone 3 (Storage rework) even though
> Search's own 'Needs' column names Storage rework as a prerequisite — a direct ordering
> violation."

### RMAP-1.6 — surface-overlap consolidation

B caught the repeated surface unprompted and consolidated it:

> "'rework note model' is repeated as a task line under three separate milestones […]
> even though it is the actual deliverable of Storage rework alone — redundant/duplicated
> work."

A independently did the same thing while authoring, elevating the shared storage rework
into its own milestone rather than duplicating it under two dependents.

Both behaviors appeared without any skill. Per `author-skills`, text with no failure
behind it is a no-op.

**Ruled 2026-07-25: both retired by strikethrough** in `requirements.md`, with this file
as the stated evidence. Neither rule is written into `plan-milestones`. What survives:
forward dependencies are still caught structurally by S4 in the template rule block, the
authoring gate (RMAP-1.18), and `status-roadmap`'s R11; the `Surfaces:` slot is retained by
RMAP-1.20 because it is the input that makes overlap visible — the retired part is the
instruction to reason about it, not the data.

## GREEN — `plan-milestones`

Same prompts, same sanitized repo, with the skill and template added and still no spec to
read. Three runs were needed; the two failures were both **discoverability**, not
body loopholes.

| Run | Outcome |
|---|---|
| GREEN A (author) | full compliance, first attempt. Cited the skill by name |
| GREEN C attempt 1 (update) | **failed** RMAP-1.7 and RMAP-1.19. Never mentioned the skill |
| GREEN C attempt 2 (update) | **failed** the same two. Reported "no AGENTS.md gate applies" |
| GREEN C attempt 3 (update) | full compliance. Cited `skills/project/plan-milestones/SKILL.md` by path |

**GREEN A** wrote to `docs/roadmap/INDEX.md`, filled every slot, kept `Status: Draft`,
preserved every pre-existing ID and continued past the highest in use (`ROAD-6`, `ROAD-7`),
left the `ROAD-4` gap alone rather than reusing it, and folded the storage rework into
Search because "a milestone whose outcome is only 'the storage layer is reworked' isn't a
testable user outcome". It invented no status column and no change log — the strongest
baseline failure, fixed.

**Why C failed twice.** Attempt 1's report never named the skill. Attempt 2 said it
outright:

> "the roadmap-edit skills in this repo's AGENTS.md (frame-change/specify-behavior/etc.)
> gate *feature/code* work, not roadmap-document edits — there's no gate here requiring a
> check-in"

`plan-milestones` was not yet registered in `AGENTS.md`. Skills in this repo are source, not
harness-installed, so **`AGENTS.md` §11 is the discovery surface** — an agent that trusts
the index and finds nothing listed correctly concludes nothing applies. Two fixes, both
kept:

1. The `description` had only create-shaped triggers. Added update-branch triggers —
   "update the roadmap", "drop this item", "reorder the milestones", "move sharing ahead of
   search", and any request that edits `docs/roadmap/INDEX.md`.
2. Registered the skill in `AGENTS.md` §3, §8, §11, the main-flow block, and the guide
   index.

**Lesson worth keeping:** for an in-repo product walking agent, registration in `AGENTS.md` is a
harder trigger than description keywords. A skill that exists on disk but not in the index
is invisible to an agent that reads the index first.

**Incidental catch.** The first description rewrite failed
`scripts/lint-skill-frontmatter.py` on an unquoted colon — the precise failure its
docstring says once silently dropped `audit-trace` from the catalog. Rephrased without colons.

**GREEN C attempt 3, verbatim on the two previously-failing behaviors:**

> "I did not delete it. Changed `Members: ROAD-3 search-index, ROAD-4 search-ui` to
> `Members: ROAD-3 search-index, ~~ROAD-4 search-ui~~ — dropped 2026-07-25: no custom
> search UI` — struck through in place, with a date and reason, so the record that it was
> considered and rejected survives."

> "`Status: Approved` → `Status: Draft`: I demoted it. […] a prior sign-off does not
> pre-approve a new edited version ('an amended plan is a different plan')."

No new rationalizations appeared in attempt 3, so REFACTOR closed with the description and
registration fixes above.

## RED — `frame-change` step-5 write-handoff

One agent, current `frame-change` (no write-handoff), `plan-milestones` present and registered, spec
removed. Request: a four-subsystem feature (roster, approval permissions, invitation flow,
spec-approval audit log).

**It decomposed correctly and then destroyed two of the four pieces.** Verbatim:

> "**B. Per-person permission levels controlling who may approve a spec** — declined.
> Recorded at `docs/adr/0002-defer-enforced-approval-permissions-and-invitations.md` and in
> […] requirements.md, 'Out of Scope' section, first bullet."

> "**C. Invitation flow for adding a new person to a repo** — declined"

Two of four sub-features became *rejections* — an ADR and Out-of-Scope bullets — not
deferrals. No build order was persisted anywhere. Corroborating, unprompted, in the same
report:

> "There's no clean home for a 'flag a pre-existing repo inconsistency' note […] so it's
> only recorded here, in this report."

The agent then spent 176k tokens writing a full triad for the one surviving piece — correct
under the current skill, and the reason the other three had to be disposed of somehow.

## GREEN — `frame-change` step-5 write-handoff

**Attempt 1 failed on a harness error of mine.** The prompt said "Do not write any spec
triad", which the agent generalized: *"This was read-only discovery. No file in the repo was
created or edited."* I had forbidden the artifact under test. Re-ran with the stop boundary
named by the flow's own steps instead of by "don't write files".

**Attempt 2 complied.** Verbatim:

> "Created: […] `docs/roadmap/INDEX.md` — the program-layer roadmap (Status: Draft) […]
> S1–S7 structural validation was run against it and is clean"

> "**ROAD-2** and **ROAD-3** remain `Planned` (not yet committed) under the same `MILE-1`
> milestone in `docs/roadmap/INDEX.md`, each to get its own frame-change→spec cycle once
> ROAD-1 ships."

Three sub-features, three tracked items, zero rejections — against RED's four pieces with
two declined.

### A real gap the GREEN run found

> "The fine-grained dependency chain (ROAD-2 and ROAD-3 both depend on ROAD-1) has **no
> field in the roadmap template at ROAD-N granularity** (`Depends-on` exists only at the
> `MILE-N` level) — that ordering is only in this conversation."

`frame-change` step 5 mandates recording build order, but the template could only express
dependencies between milestones, so within-milestone ordering was unrepresentable. Fixed by
extending the existing positional convention to members — item order is list position and
carries build order; identity stays the ID. No new slot.

### Two findings routed elsewhere, not defects here

- The vision has no `**GOAL-N**` IDs, so `Goals:` citation is vacuous today. That is Task 5.
- `plan-milestones` is not a harness-registered tool in this repo, so the agent followed it by
  reading the file. Correct behavior; noted because it confirms `AGENTS.md` registration plus
  the on-disk body — not tool registration — is what makes an in-repo skill effective.

## Task 9 — no RED phase, by design

`tests/test_trace_scope.py` guards RMAP-2.10, a `SHALL CONTINUE TO` criterion. It protects a
boundary that already holds, so it passes on its first run. `test-first` lists "a new test passed on
its first run" as a red flag, and that flag is correct for a test meant to *drive* new
behaviour — this one engages no production change at all, and `specify-behavior` Step 3
mandates exactly this shape for guard criteria. The failure mode it exists for is a future
edit that grows `audit-trace` into planning-ID territory.

Recorded here so the absent RED phase is a stated decision rather than a gap someone finds
later and has to reconstruct.

## Task 7 — weak RED, and why

`tests/test_priority_ladder.py` had **6 of 7 tests pass on first run**. The cause is a
sequencing slip of mine, not a property of the work: the plan allocated the ten-row ladder to
Task 7, and I wrote it into `status-roadmap`'s body during Task 6. By the time the ladder test
existed, its subject already did.

Deleting a verified ladder to manufacture a red bar would have been theatre, so the content
stands and the slip is recorded here instead. The test keeps its value as a **regression
guard** on ordering, tie-breaks, the withholding branch, and the ARCH-5 boundary at row 7.

The one genuine failure it did catch: the standup card's phrase "the milestone in flight"
wraps across a newline in the source, so a plain substring check for `in flight` failed. The
fix belonged in the test — collapsing whitespace before prose assertions — because a test that
breaks whenever a paragraph reflows is coupled to formatting rather than behaviour. The
table-row assertions stay line-scoped, since markdown table rows are single lines by
construction.
