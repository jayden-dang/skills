# Assessments: MILE-2 — Faithful history

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

**Outcome verdict:** withheld — all three member bindings unresolved (ROAD-4, ROAD-5, ROAD-6) and mechanical baseline unresolved (`Commitment: Planned`)

**Delivery evidence (for human disposition; not a terminal achieved/not-achieved under skill rules):**

Outcome sentence promises: a reviewer reads a history and an explainer that match how the work will integrate — gated history rewriting on request, explainers against the integration base (not default branch guesswork), and bidirectional supersede linkage on decision records.

| Member | Binding | Delivery evidence at candidate `c8e5f73` |
|---|---|---|
| ROAD-4 gated-history-rewriting | **unbound** | **Not delivered.** `package-change` **NEVER** rewrites pre-existing history; only an **advisory** commit map. PCHG Out of Scope explicitly defers rewrite to ROAD-4. Blockers: conditional on demonstrated demand. |
| ROAD-5 shared-base-resolution-for-explainers | **unbound** | **Not delivered as ROAD-5.** `brief-team` / XPLN Implemented for explainers, but skill body has no shared PR-base / integration-base resolver aligned with package-change; PCHG Out of Scope defers base alignment to ROAD-5. XPLN INDEX `Roadmap item: —` (not bound to ROAD-5). Blockers: requires realign-spec on shipped XPLN. |
| ROAD-6 supersede-linkage-for-decision-records | **unbound** | **Partial at best, not complete.** `RECORD.md` defines `Supersedes:` / `Superseded-by:`; validator enforces bidirectional linkage. `record-verdict` **SKILL.md** does not teach writing both directions in one publish (blocker text). PCHG-8.10 defers mechanical supersede write path to ROAD-6. |

**Member bindings:**

| ROAD | Feature | INDEX Status | Spec Status | Binding |
|---|---|---|---|---|
| ROAD-4 | — | — | — | **unresolved (zero codes)** |
| ROAD-5 | — | — | — | **unresolved (zero codes)** |
| ROAD-6 | — | — | — | **unresolved (zero codes)** |

Deferred membership: None.  
**Depends-on:** MILE-1 (still `Commitment: Planned` / not Closed) — dependency milestone not closed.  
**Blockers (roadmap intent, still open):** ROAD-4 demand-gated; ROAD-5 realign-spec on shipped brief-team; ROAD-6 teach-pack bidirectional Supersedes write.

**Goal coverage:** cited GOAL-1, GOAL-3 resolve live. Formal goal-coverage **withheld** with outcome (no bound members). Informal: neither goal advanced by complete MILE-2 members.

**Deferrals:** None in `Deferred:` slot — honest empty (blockers are not deferrals).

**Attention:** range unsampled. Name `/select-review-sample` for the user if desired.

**Plan accuracy (descriptive only — not a schedule estimate):**

Committed baseline unresolvable → no baseline..candidate roadmap diff under plan-accuracy rules. Membership at assessment: ROAD-4, ROAD-5, ROAD-6 under MILE-2; none deferred or moved out in current INDEX.

No velocity or projected date derived.

**Findings:**

| Finding | Destination |
|---|---|
| ROAD-4/5/6 all unbound | `specify-behavior` when building each item, or bind after delivery |
| Outcome surface largely **not** met — advisory history only; no shared base for explainers; incomplete supersede publish teaching | implement MILE-2 members (or replan scope via `plan-milestones`) |
| ROAD-4 still demand-gated per Blockers | user decision: demand demonstrated → build; else defer with date/reason |
| ROAD-5 needs realign-spec on XPLN if amending shipped brief-team | `realign-spec` / `amend-feature` when scoped |
| ROAD-6 needs record-verdict write path for both Supersedes directions | feature work on `record-verdict` |
| MILE-1 dependency not Closed | finish/close MILE-1 before treating MILE-2 as closeable in program order |
| MILE-2 `Commitment: Planned` | `plan-milestones` when committing |

**Withholding preconditions relevant to MILE-2:** all three bindings unresolved; baseline unresolvable. R9 N/A. R2/R4/R11 not raised for this milestone parse.

**Rationale:** Unlike MILE-3 (delivered and closed) or even MILE-1 (partial informal surfaces), MILE-2's Outcome is **not** supported by complete member delivery. Formal verdict is **withheld** (bindings + Planned commitment). Informal reading: **not achieved** if judged on evidence alone — history remains advisory-only, explainer base resolution is not shared with package-change, and supersede linkage is validator-ready but not skill-taught as a full publish path. Close is not eligible.

### Human disposition

**Current:** Pending  
**Close decision:** None — required only once Current is terminal  
**History:**  
- 2026-08-02 Pending

## Close eligibility (this invocation)

1. **Mechanical eligibility:** **FAIL** — Committed baseline unresolved; ROAD-4, ROAD-5, ROAD-6 bindings unresolved. Non-overridable.  
2. **Permitting disposition:** **FAIL** — disposition is Pending (non-terminal).

→ **Not close-eligible.** No handoff to `plan-milestones` for close.

## What the human can do next

1. **Do not close** MILE-2 — members are unbound and outcome surfaces incomplete, or  
2. Sequence work after MILE-1: implement ROAD-4 (if demand), ROAD-5 (realign brief-team base), ROAD-6 (record-verdict bidirectional write), each via feature flow + INDEX bind, or  
3. **`plan-milestones`** to defer ROAD-4 (or others) with date/reason if demand never appears, or reorder intent, or  
4. Re-run **`/assess-milestone`** only after bindings exist and (for close) Commitment is Committed.
