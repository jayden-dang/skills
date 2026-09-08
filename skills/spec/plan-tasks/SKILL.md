---
name: plan-tasks
version: 1.2.2
description: Use when a design is approved and the tasks.md implementation plan
  (vertical-slice tasks with requirement footers and behavior tests) needs writing,
  after design-solution and before the execute family (build-in-waves /
  build-by-story / build-inline).
---

Produce `docs/specs/<YYYY-MM-DD>-<feature>/tasks.md` from the approved
requirements and design, from the skill set's `templates/tasks.md` (first path
that exists: `templates/` beside this SKILL.md, `${CLAUDE_PLUGIN_ROOT}/templates`,
else `../../../templates`). Every task-block slot (**Files**, **Interfaces**,
**Depends-on**, **Steps**, `_Requirements:_`) is REQUIRED — no per-task risk
labels, decision-surface flags, or Human-review-order (see Step 3's gate table
for why). Write for a skilled implementer with NO context on this codebase,
seeing ONLY their task plus Global Constraints: **names, paths, types,
commands** they must not guess go in **Files / Interfaces / Reuse / footer**,
never as prose inside Steps (see **Thin steps**). Create a todo per step (1–4,
plus 5 if there's a tracker) — this skill's own list, separate from
`design-solution`'s and the execute family's — checked off only when its
**Done when:** is met.

## Step 1: Header and Global Constraints

Goal (one sentence), Architecture (2–3 sentences), Tech Stack, and
`Execution-mode: <unset|continuous|story-unit>` (leave **unset**; never invent
it from size/band/habit — mode write-back happens only at **Exit**). Then
**Global Constraints**: project-wide rules at a canonical source path + hash,
referenced (not copied) by every task. `## Team` with a roster/band override →
derive band + packaging from it alone (Solo: no fake multi-assignee theater;
Small/Multi: optional freeform notes, never a new required field); no Team →
pre-feature default. `docs/architecture/` spine, if any → fold its hard
`**ARCH-N**` invariants in too, so every task inherits them. Resolve the
source below — first hit is SSOT; never invent a parallel one:

| Order | Source | Covers |
|---|---|---|
| 1 | `docs/standards/`, when it exists (`INDEX.md` + domain files like `testing.md`, `errors-logging.md`) | naming, i18n, house rules, testing, errors/logging |
| 2, then 3 | Else `docs/product/guidelines.md` (**legacy fallback only**, and only if it has a parallel rule body — not pointer-only) when `docs/standards/` is absent; else `docs/agents/project.md` | test/lint/typecheck commands, naming/i18n rules, forbidden changes |

**Done when:** Goal, Architecture, Tech Stack, `Execution-mode:` (typically
`unset`), and Global Constraints source path/hash are written, with the
constraint source identified and no parallel SSOT invented.

## Step 2: File structure and retrieval

Map every file the plan creates or modifies, with one-line responsibilities,
BEFORE writing tasks. A file not in the map should not be touched by any task.

### System docs consult during File Structure (optional)

WHEN this step writes or revises File Structure / path placement, read
`system-docs-consult.md` beside this file and follow it exactly — it resolves
codebase/standards authority, conflict handling, and the no-op path when those
docs are absent or non-authoritative.

Once the map is complete and **before writing task bodies** (Step 3), run
retrieval once: REQUIRED SUB-SKILL: use `load-subgraph` for **`blast_radius`**
on the mapped paths, then for **`cluster(feature CODE)`** as sole focus. Hold
the package while authoring Files/Reuse; for **grounded claims** (one home)
follow `skills/execution/load-subgraph/references/grounded-claims.md` —
empty/thin isn't a gate, but state coverage before absence claims.

**Done when:** every file to create/modify is mapped with a one-line responsibility,
and blast_radius/cluster(feature CODE) ran once (or no-op if specs/seeds are missing).

## Step 3: Tasks as vertical slices

**Contract:** a task is a vertical slice — the smallest unit with its own test
cycle and review verdict; split only where a reviewer could reject one task
while approving its neighbor. **Shape:** one demoable end-to-end outcome per
task per user story; prefactoring that only enables a later slice is its own
**earlier task** ("make the change easy, then make the easy change") via
`Depends-on` edges — never buried horizontal layers inside a story task.

Each task carries these slots:

| Slot | Rule |
|---|---|
| **Files, Reuse, Interfaces, Depends-on** | Files: Create / Modify / Test, each path **hardened** in backticks (e.g. `` `src/foo/bar.ts` ``); never glue a line number/range into the path token (`path:86-103` is forbidden) — ranges go in surrounding prose or a separate annotation (new plans only; P1 ownership extraction still accepts legacy glued forms in already-written `tasks.md`). Reuse: the concrete existing code/library/pattern this task builds on, copied **verbatim** from the design section's `Reuse:` line — same `<rung> — <concrete target>` grammar (e.g. `Reuse: existing — src/util/dates:parseISO (rung 2)`); copy, don't reinterpret — Step 4 checks it against the design's line. Interfaces: Consumes / Produces — the names and types neighboring tasks share, so an isolated implementer learns what to call things. Depends-on: the earlier tasks this one truly needs — those whose interface it Consumes or whose files it builds on — as `Depends-on: Task 2, Task 4`, or `Depends-on: none`. Parallelism signal: two tasks sharing no files and no interface declare no edge, so the continuous `build-in-waves` scheduler may place them in one ready set when surfaces are disjoint and worktree isolation is safe; omitting the line falls back to depending on every prior task (safe but fully serial) — over-declaring needlessly serializes, under-declaring is caught by the executor's file-disjoint check before it can collide. Governs build waves — never reorder or narrow dependencies solely to tidy review units if that would lie about what the task needs. |
| **Steps (thin, 3–8 checkboxes)** | Bite-sized checkboxes (2–5 min each, prefer **3–8** per task), TDD cycle: failing test (complete code describing **behavior**, not embedding requirement IDs in application/test source) → run, expect the stated failure → implement (complete code) → run, expect pass → commit with a conventional subject explaining the change (no `Implements:` / `Guards:` trailer required or taught). No novel-length essays here — that bloats `line_count` and review surface; long how-to narration for one worker goes in the execute brief (`.skills/<CODE>/task-N-brief.md`) at execute time, while the shared plan keeps **identifiers** (paths, type names, commands) in Files / Interfaces / Reuse so the brief cannot invent APIs. |
| **Footer** | `` `_Requirements: CODE-N.M, CODE-N.M_` `` — the IDs this task implements or guards; every task has one. **Default: one story's IDs** (same story number N); multi-story footers **merge** those stories into one review unit under `build-by-story` (plan-quality signal — not a ban, not a reason to lie about Depends-on). IDs live in this footer (and in requirements/design), not in production source or test titles. No placeholders anywhere in a slot — "TBD", "add appropriate error handling", "similar to Task 3", or a type referenced but defined in no task — each is a plan bug; fix it before the plan ships. |

| Thought | Reality |
|---|---|
| "Prefactor first is always right — make the change easy" | Prefactor via Depends-on is fine; review units still follow story citations at build-by-story |
| "I'll add Risk: high so reviewers notice" | No such field. Risk globs on the actual diff replace agent labels |
| "I'll write Human review order so the human knows what to read first" | Superseded: story-derived units are the review order; an authored second list dies without a consumer |

**Done when:** every file in Step 2's map is covered by ≥1 task, each written
as a vertical slice with its own test cycle — slot/placeholder cleanliness is
Step 4's check, not this one.

## Plan size budget (hard gate)

**Home for this rule** — count in Step 4 and again at Exit before Approve;
other sections only point here.

| Metric | How to count | Hard ceiling |
|---|---|---|
| **task_count** | Count headings whose text matches `Task <integer>` at level `##` or `###` only (e.g. `### Task 3` or `## Task 12: Activate rail`). Not `####`, not `Task 3a`, not prose “task 3”, not checkbox count. | **12** |
| **line_count** | **Whole-file** line count of this `tasks.md` (header + Global Constraints + map + tasks). Checkbox count is irrelevant. “Fluff / ignore lines” does **not** waive. | **400** |

**WHEN** `task_count > 12` **OR** `line_count > 400` (either metric alone blocks):

- **MUST NOT** set `Status: Approved`.
- Surface both counts vs ceilings and that the plan is over budget.
- Offer only size remedies (user picks; no silent cut):
  1. **Decompose** — this plan keeps only the first ship slice. IF the leftover is new feature shape → hand back to `frame-change`. IF the roadmap already exists and you only need later slots → REQUIRED SUB-SKILL: use `plan-milestones` to add `ROAD-N` items. Then delete tasks that belong to later ROAD items from *this* file.
  2. **Cut scope** — strike or Out-of-Scope requirements, then delete the matching tasks (and shrink Steps if `line_count` alone is high).
  3. **Merge slices** — fewer tasks, still vertical (one demoable outcome each); do not hide horizontal layers inside one mega-task.

"Don't split / just approve / standup / only N tasks / line count is fluff / CFND-size is normal" **does not waive**. A megaplan is not made shippable by urgency.

**WHEN** both metrics are at or under ceiling → budget clear; continue Exit.

## Step 4: Coverage and consistency check

| Check | Rule |
|---|---|
| **Coverage: audit-trace, behavior steps, seam-table** | REQUIRED SUB-SKILL: use `audit-trace` — every Approved requirement cited by ≥1 task footer (uncited IDs mean incomplete, or strike with a reason); docs-only, no IDs in test source. Each footer ID needs a TDD step (or manual/acceptance step) asserting **behavior** in domain language — never `[CODE-N.M]`, `/// REQ:`, or `@CODE-N.M` in test source; map IDs to tests in the task report / Spec review, not production trees. If `design.md` has a "Seams for testing" table, every ID in every row needs a planned test/acceptance step at that seam — an ID promised but left uncovered is *dropped coverage*: add the step, don't renumber. |
| **Type/name + Reuse consistency + reuse-miss** | The same function must have the same name and signature in every task that mentions it. Flag any task whose `Reuse:` line disagrees with the design section's `Reuse:` line. Also flag any task whose Files **Create** something the scan digest or an already-installed dependency already provides — build on it instead (task-granularity sibling of `inspect-change`'s `reuse-miss`; advisory, not a hard block). |
| **Spec alignment + upstream sync-back** | Re-read requirements.md once, checking each criterion against the task that claims it. If a requirement proves *wrong or infeasible as written* — not merely uncovered — correct it in requirements.md and re-surface for approval; do not bury a workaround in a task that leaves the requirement lying — a plan that satisfies a false requirement ships the falsehood. |
| **Independent plan review (dispatch, don't self-review) + Plan size** | The checks above are doc-only and stay here; the codebase comparison does not. Dispatch a review subagent with the plan, requirements.md, design.md, and the repo; have it prove-claim against real code every symbol, signature, path, import, and **hardcoded test value** the plan asserts — a fabricated golden or a guessed API is the classic plan defect — citing `file:line` and defaulting to flag. Findings to `.skills/<CODE>/plan-review.md`; fix before offering execution (no subagents? do the comparison yourself). Also run the **Plan size budget** counts here (one home); over ceiling → shrink before Exit, don't present for Approve yet. |

**Done when:** every requirement ID has a task footer and a planned behavior
test at an agreed seam; audit-trace, the seam-table reconcile, and the
placeholder scan are clean, **and** the **Plan size budget** is clear (or shrunk).

## Step 5 (optional): Publish to the issue tracker

If the repo has no tracker (`docs/agents/issue-tracker.md` absent, or
**Tracker:** empty / none) → **skip** this step (not pending). Otherwise, read
`publish-recipe.md` beside this file and follow it exactly: resolve **Publish
unit**, author the issue body, and record ids under `.skills/<CODE>/`. Default
and only tracker-visible unit: **one feature issue** per plan, closed by the
feature PR.

| Thought | Reality |
|---|---|
| "Four tasks → four issues so agents can grab in parallel" | Waves read `tasks.md` + Depends-on. Tracker noise is not parallelism |
| "Sub-issues keep hierarchy without noise" | Under unit `feature`, tasks are not tracker tickets |
| "publish-issues always means one issue per slice" | Non-triad path only. This step follows Publish unit |
| "I'll publish tasks; the user can close extras" | Extras are the defect under unit `feature` |
| "Many tasks — config must mean tasks" | Size never sets Publish unit; only the file line or explicit user order |

### Red Flags — Step 5

- Under unit `feature`: more than one triad issue, or any issue titled like a plan task (`Task N:`)
- Setting or assuming `Publish unit: tasks` from plan size alone
- Falling back to task issues after a permission error

**Done when:** skipped (no tracker / cannot publish), **or** unit `feature` with
exactly one feature issue (union IDs, plan path, id under `.skills/<CODE>/`),
**or** unit `tasks` with one issue per plan task and ids recorded.

## Exit

| Step | Rule |
|---|---|
| **1–2. Present, budget gate** | Present the FILE and STOP — conversational agreement is not approval; the written plan is what gets approved, and the execute family runs only on an approved `tasks.md`. Follow **Plan size budget** (one home) before Approve: over ceiling → do **not** set Approved, run those remedies; under ceiling → continue. |
| **3. On approval** | Set `Status: Approved`. Leave `Execution-mode:` as `unset` (or untouched); do **not** write `continuous` or `story-unit` yourself. |
| **4. Offer three routes** | Exactly three, one question — do **not** first ask continuous vs story-unit (that interview is dead); mode write-back owned by the picked skill. `build-by-story`: subagent path, human-gated review units derived from stories (writes `story-unit`). `build-in-waves`: subagent waves, no human pause between tasks (writes `continuous`). `build-inline`: controller implements sequentially with `test-first`, no implementer subagents (writes `continuous` as bookkeeping; **does not** run unit barriers). **Recommend (label only, not invent mode):** mark **`build-by-story` (Recommended)** first WHEN user-facing UI/UX, Team Solo/Small, or `requirements.md` has **≥2** behavioral stories — still offer all three, still wait for the pick; no triggers → leave unmarked (not invent mode, not a size default — see gate table below). |
| **5–6. On pick, INDEX** | Name the skill and hand off — REQUIRED SUB-SKILL: use `build-in-waves`, `build-by-story`, or `build-inline` as chosen (for the two subagent routes, prefer REQUIRED SUB-SKILL: use `isolate-workspace` first when none exists yet). Then confirm the feature's row in `docs/specs/INDEX.md` carries the same `Status:` as its `requirements.md`. |

| Thought | Reality |
|---|---|
| "PM said just mark Approved — continuous is obvious" | Approval is the written plan **under budget**. Offer the three skills; do not invent mode |
| "Standup in five — skip asking which execute skill" | Time changes *when* you ask, not whether a route is named |
| "Four tasks → default build-in-waves" | No silent waves default. Prefer recommending `build-by-story` when the Recommend predicate holds; user still picks |
| "I'll ask continuous vs story-unit, then offer routes" | Redundant. One question: which of the three skills |
| "User said approve and start building — write continuous and go" | Budget clear + Approve + offer three routes. "Start building" is not a route pick |
| "I'll write Execution-mode now so the plan looks complete" | Completeness is Status + route name. Mode is written by the execute skill |
| "28 tasks / 900 lines — just approve, splitting is ceremony" | Plan size budget blocks Approve. Decompose, cut, or merge first |
| "Only 10 tasks — ignore line_count, it's fluff" | Either ceiling blocks. Whole-file `line_count` counts; thin Steps / cut prose |
| "Recommend story-unit is inventing Execution-mode / banned by no size-based default" | Recommend is an offer label; mode stays unset until the execute skill runs after pick |
| "Waves are faster — skip story stops on UI work" | Faster continuous often means one huge PR. Recommend still `build-by-story` when the predicate holds |
| "Thin steps — drop paths/types from the task into the brief only" | Identifiers stay in Files/Interfaces/Reuse; only narration moves to the brief |

### Red Flags — Exit

- Asking continuous vs story-unit before (or instead of) the three-skill offer
- Setting `Status: Approved` while inventing `Execution-mode: continuous`
- Setting `Status: Approved` while `task_count > 12` or `line_count > 400`
- Offering only one route, or skipping the offer after approval
- Writing `Execution-mode:` in plan-tasks instead of letting the execute skill do it
- Treating "LGTM, build it" as a silent default to `build-in-waves`
- Omitting the `(Recommended)` mark on `build-by-story` when the Recommend predicate holds
- Approving while over `line_count` because `task_count` alone is ≤ 12
- Dropping path/type/command identifiers from Files/Interfaces/Reuse while “thinning” Steps

**Done when:** `tasks.md` is **under the Plan size budget**, `Status: Approved`,
one of the three execute skills named (and handed off on pick),
`Execution-mode:` not invented here, and the INDEX.md row agrees.
