# Assessments: MILE-1 — Reviewable delivery

<!--
Outcome truth for one milestone, written only by `assess-milestone` to
docs/roadmap/assessments/<MILE-N>.md. One file per milestone.
Structural rules A1–A7: see templates/milestone-assessment.md.
-->

## Assessment 1

**Supersedes:** None — first assessment of this milestone
**Committed baseline:** None — unresolvable: milestone `**Commitment:**` is `Planned`, not `Committed` (pickaxe baseline requires the exact Committed line at the candidate revision)
**Candidate closing revision:** `c8e5f73c9853c83112335ad2412461447c1bdda7`
**Roadmap revision assessed:** `c8e5f73c9853c83112335ad2412461447c1bdda7` (working tree: clean)
**Assessed:** 2026-08-02

### Agent assessment

**Outcome verdict:** withheld — unresolved member bindings (ROAD-1, ROAD-2) and mechanical baseline unresolved (`Commitment: Planned`)

**Delivery evidence (for human disposition; not a terminal achieved/not-achieved under skill rules):**

Outcome sentence promises: a multi-person team can review skill-set changes as risk-aware, story-sized PRs — risk-glob review prompts, story-derived review units, and reviewer-facing commits/PR description that explain the change itself.

| Member | Binding | Delivery evidence at candidate `c8e5f73` |
|---|---|---|
| ROAD-1 risk-glob-review-prompts | **unbound** (0 feature codes) | Surface present: `land-branch` risk-glob finish prompts + `select-review-sample` risk signals; `plan-tasks` no longer authors per-task Risk labels. **No feature triad / INDEX row binds ROAD-1.** |
| ROAD-2 story-derived-review-units | **unbound** (0 feature codes) | Surface present: `build-by-story`, `Execution-mode: story-unit` / continuous write-back, plan-tasks three-route exit. **No feature triad / INDEX row binds ROAD-2.** |
| ROAD-3 reviewer-facing-change-authoring | **PCHG** (exactly one) | `docs/specs/2026-07-28-package-change/` **Implemented**; INDEX Status Implemented; package-change + land-branch handoff live |

**Member bindings:**

| ROAD | Feature | INDEX Status | Spec Status | Binding |
|---|---|---|---|---|
| ROAD-1 | — | — | — | **unresolved (zero codes)** |
| ROAD-2 | — | — | — | **unresolved (zero codes)** |
| ROAD-3 | PCHG | Implemented | Implemented | OK |

Deferred membership: None.  
Blockers slot: None.

**Goal coverage:** cited GOAL-1…5 all resolve live in `docs/product/vision.md`. Informal advancement only (partial surfaces + PCHG); **goal-coverage formal verdict withheld** with outcome (bindings incomplete).

| Goal | Informal note |
|---|---|
| GOAL-1 | partial — review/package path exists for ROAD-3; ROAD-1/2 unbound |
| GOAL-2 | partial — gates preserved in package-change/land-branch guards |
| GOAL-3 | partial — pack markdown skills only |
| GOAL-4 | partial — configure-repo Default PR base slot for PCHG |
| GOAL-5 | partial — optional brief-team naming; ceremony tiers unchanged |

**Deferrals:** None in `Deferred:` slot — honest empty.

**Attention:** range unsampled (no `/select-review-sample` allocation supplied). Name `/select-review-sample` for the user if a human sample set is desired.

**Plan accuracy (descriptive only — not a schedule estimate):**

Committed baseline unresolvable → no baseline..candidate roadmap diff under assess-milestone plan-accuracy rules. Membership at assessment: ROAD-1, ROAD-2, ROAD-3 under MILE-1; none deferred or moved out of this milestone in current INDEX.

No velocity or projected date derived.

**Findings:**

| Finding | Destination |
|---|---|
| ROAD-1 and ROAD-2 unbound (R7-class for those items) — surfaces appear shipped in skills without a feature code / INDEX binding | `specify-behavior` + INDEX bind, or `/map-features` backfill, then re-assess |
| MILE-1 `Commitment: Planned` — close baseline cannot resolve | `plan-milestones` when the team commits |
| ROAD-3 (PCHG) Implemented and bound — only complete formal member | none |
| Related work XPLN (brief-team) Implemented but INDEX `Roadmap item: —` (unplanned relative to ROAD-1 naming of brief-team) | optional bind or leave as unplanned (R8) |

**Withholding preconditions relevant to MILE-1:** binding failures withhold the outcome verdict (assess-milestone pass 3). R2/R4/R10/R11 not raised for this milestone's parse. R9 N/A (`Commitment` not Closed). R10 clean for PCHG.

**Rationale:** Formal Outcome cannot be **achieved** or **not achieved** while two of three members lack a 1:1 feature binding and Commitment remains Planned. Informally, large parts of the outcome surface exist (risk globs, story-unit execute path, PCHG packaging), but the milestone is not close-ready until bindings are complete, Commitment is advanced, and a re-assessment issues a terminal verdict.

### Human disposition

**Current:** Pending  
**Close decision:** None — required only once Current is terminal  
**History:**  
- 2026-08-02 Pending

## Close eligibility (this invocation)

1. **Mechanical eligibility:** **FAIL** — Committed baseline unresolved (`Commitment: Planned`); ROAD-1 and ROAD-2 bindings unresolved. Non-overridable.  
2. **Permitting disposition:** **FAIL** — disposition is Pending (non-terminal).

→ **Not close-eligible.** No handoff to `plan-milestones` for close.

## What the human can do next

1. Bind ROAD-1 and ROAD-2 (new specs or `/map-features` / INDEX write-back to existing skill delivery), or  
2. Run **`plan-milestones`** to set MILE-1 `Commitment: Committed` when committing to finish remaining members, then re-run **`/assess-milestone`**, or  
3. Supply a **`/select-review-sample`** allocation if a sampled review of the delivery range is desired, or  
4. Leave Pending until ROAD-1/2 are formalized — do not close on informal surface presence alone.
