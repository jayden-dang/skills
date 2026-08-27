---
name: plan-tasks
version: 1.2.1
description: Use when a design is approved and the tasks.md implementation plan
  (vertical-slice tasks with requirement footers and behavior tests) needs writing,
  after design-solution and before the execute family (build-in-waves /
  build-by-story / build-inline).
---

Produce `docs/specs/<YYYY-MM-DD>-<feature>/tasks.md` from the approved requirements
and design. Start from the skill set's `templates/tasks.md`. Resolve pack seeds
in this order, first path that exists: (1) `templates/` beside this SKILL.md,
(2) `${CLAUDE_PLUGIN_ROOT}/templates` when that variable is set, (3)
`../../../templates` relative to this SKILL.md. Every slot in a task block
(**Files**, **Interfaces**, **Depends-on**, **Steps**, `_Requirements:_`) is
REQUIRED. Do **not** author per-task risk labels, decision-surface flags, or a
Human-review-order section — risk is measured by select-sample risk globs
against the actual diff; review units are **derived** from user stories at
`build-by-story` time (see that skill).

Create a todo per step (1–4, plus 5 if the repo uses an issue tracker) before starting, and complete them in order — this skill owns its own list, distinct from `design-solution`'s upstream and the execute family's downstream. Check each off only when its **Done when:** is met.

Write for an implementer who is skilled but knows NOTHING about this codebase
or problem domain, and will see ONLY their own task plus the Global
Constraints. **Names, paths, types, and commands** the implementer must not
guess belong in **Files / Interfaces / Reuse / footer** (and Global Constraints
by reference) — not as novel-length prose inside Steps (see **Thin steps**).

## Step 1: Header and Global Constraints

Goal (one sentence), Architecture (2–3 sentences), Tech Stack. Header also
carries the bookkeeping field:

```
Execution-mode: <unset | continuous | story-unit>
```

Leave `Execution-mode: unset` while planning — never invent continuous/story-unit
from plan size, band, or habit. Route choice and mode write-back live only at
**Exit** (and in the chosen execute skill).

Then **Global Constraints**: project-wide rules recorded at their canonical
source path and content hash. Resolve the source from the design and
`docs/agents/project.md` — test/lint/typecheck commands, naming and i18n rules,
forbidden changes. Every task references this source; execution carries a
compact delta. When `## Team` is present with a
non-empty **roster** or band override, derive the **band** and apply
**packaging** from that section only: Solo tasks avoid fake multi-assignee
theater; Small/Multi may add optional freeform owner/review notes (never a new
required task field). Missing Team → pre-feature default.

When a `docs/architecture/` spine exists, also fold its hard `**ARCH-N**` invariants
into Global Constraints so every task inherits them; no spine, nothing to fold. And
source the human-facing engineering rules (naming, i18n, house rules, testing,
errors/logging) from **`docs/standards/`** when that tree exists (prefer
`docs/standards/INDEX.md` plus applicable domain files such as `testing.md` and
`errors-logging.md`). IF `docs/standards/` is absent and unmigrated content still
lives in `docs/product/guidelines.md`, use that as a **legacy fallback only**.
IF `docs/product/guidelines.md` is a pointer-only file (no parallel rule body), do
not treat it as SSOT. Otherwise fall back to `docs/agents/project.md` as above.
Never maintain or invent parallel SSOTs.

**Done when:** Goal, Architecture, Tech Stack, `Execution-mode:` (typically
`unset`), and Global Constraints source path/hash are written, and every
constraint source is identified without inventing a parallel SSOT.

## Step 2: File structure first

Map every file the plan creates or modifies, with one-line responsibilities,
BEFORE writing tasks. A file not in the map should not be touched by any task.

### System docs consult during File Structure (optional)

**Load:** `skills/project/define-system-doc/consult-recipe.md` (one home for authority,
hard-constraint precedence, no-op, once-per-entry suggest, never auto-invoke).

**Applicability:** this step writes or revises File Structure / path placement.

| Entry | Path | Use when Approved |
|---|---|---|
| `codebase/map` | `docs/codebase/map.md` | Layout and placement rules |
| `codebase/modules` | `docs/codebase/modules.md` | Module boundary placement |
| `codebase/ownership` | `docs/codebase/ownership.md` | Ownership notes (advisory, not authz) |
| `codebase/dependencies` | `docs/codebase/dependencies.md` | Forbidden dependency directions |
| `standards/INDEX` / `testing` / `errors-logging` | `docs/standards/…` | Global Constraints house rules (prefer standards over guidelines) |

**When Approved:** align the plan **within** hard constraints from consult-recipe;
note which docs were consulted. **Conflict** with a hard constraint → surface, keep
hard constraint, suggest `/define-system-doc <entry-key>`.

**When absent / non-authoritative:** CONTINUE (no-op). Suggest only when the gap is
material. Standards fallback chain stays: `docs/standards/` → legacy guidelines →
`docs/agents/project.md`.

**Done when:** every file the plan will create or modify appears in the map
with a one-line responsibility.

## Step 2b: Retrieval after the file map

After Step 2's map is complete and **before writing task bodies** (Step 3), run
retrieval **once** over the complete candidate path set:

1. REQUIRED SUB-SKILL: use `load-subgraph` query **`blast_radius`** on the mapped
   paths (blast-radius context for neighboring ownership).
2. REQUIRED SUB-SKILL: use `load-subgraph` query **`cluster`** with the feature
   **CODE** as the single focus (`cluster(feature CODE)`).

Hold the retrieval package while authoring Files/Reuse. **Grounded claims** (one
home): follow `skills/execution/load-subgraph/references/grounded-claims.md` —
empty/thin is not a plan gate; still state coverage/emptiness before absence claims.

**Done when:** blast_radius and cluster(feature CODE) have run once (or explicit
no-op if `docs/specs/` / seeds missing).

## Step 3: Tasks as vertical slices

**Contract — a task is a vertical slice:** the smallest unit that carries its own
test cycle and deserves its own review verdict. Split only where a reviewer could
reject one task while approving its neighbor.

**Shape:** one demoable end-to-end outcome per task when the work is one user
story. Prefactoring that only enables a later slice is its **own earlier task**
("make the change easy, then make the easy change") with `Depends-on` edges —
not a license to bury horizontal layers inside a story task.

Each task:
- **Files:** Create / Modify / Test with **hardened** path tokens: each path in
  backticks (e.g. `` `src/foo/bar.ts` ``). Line numbers or ranges, when stated,
  MUST NOT be glued into the path token (`path:86-103` is forbidden); put ranges
  in surrounding prose or a separate annotation. P1 ownership extraction still
  accepts legacy glued forms in already-written tasks.md — this grammar is for
  **new** plans only.
- **Reuse:** the concrete existing code, library, or pattern this task builds on — carried down
  verbatim from the design section's `Reuse:` line, same `<rung> — <concrete target>` grammar,
  so the implementer is told to build on it, not reimplement it (e.g. `Reuse: existing —
  src/util/dates:parseISO (rung 2)`, copied verbatim from the design section's `Reuse:` line).
  Step 4 checks it against the design's `Reuse:` line, so copy rather than reinterpret.
- **Interfaces:** Consumes / Produces — the names and types neighboring tasks
  share. This block is how an isolated implementer learns what to call things.
- **Depends-on:** the earlier tasks this one truly needs — those whose
  interface it Consumes or whose files it builds on — as `Depends-on: Task 2,
  Task 4`, or `Depends-on: none` when it has no prerequisite. This is the
  parallelism signal: two tasks that share no files and no interface declare no
  edge, so the continuous `build-in-waves` scheduler may place them in one ready
  set when surfaces are disjoint and worktree isolation is safe. Omit the
  line and the task falls back to depending on every prior task — safe but fully
  serial. Over-declaring needlessly serializes; under-declaring is caught by the
  executor's file-disjoint check before it can collide.
- **Steps:** bite-sized checkboxes (2–5 min each) following the TDD cycle:
  failing test (complete code describing **behavior**, not embedding requirement
  IDs in application/test source) → run, expect the stated failure → implement
  (complete code) → run, expect pass → commit with a conventional subject that
  explains the change (no `Implements:` / `Guards:` trailer required or taught).
- **Footer:** `_Requirements: CODE-N.M, CODE-N.M_` — the IDs this task
  implements or guards. Every task has one. **Default: one story's IDs** (same
  story number N). Multi-story footers **merge** those stories into one review
  unit under `build-by-story` (plan-quality signal — not a ban, not a reason to
  lie about Depends-on). IDs live in this footer (and in requirements/design),
  not in production source or test titles.

`Depends-on` governs build waves. Never reorder or narrow dependencies solely to
tidy review units if that would lie about what the task needs.

| Thought | Reality |
|---|---|
| "Prefactor first is always right — make the change easy" | Prefactor via Depends-on is fine; review units still follow story citations at build-by-story |
| "I'll add Risk: high so reviewers notice" | No such field. Risk globs on the actual diff replace agent labels |
| "I'll write Human review order so the human knows what to read first" | Superseded: story-derived units are the review order; an authored second list dies without a consumer |

**No placeholders.** "TBD", "add appropriate error handling", "similar to
Task 3", or a type referenced but defined in no task — each of these is a plan
bug. Fix it before the plan ships.

**Thin steps.** Prefer **3–8** checkboxes per task (TDD beats: fail → implement →
pass → commit). Do not paste novel-length essays into Steps — that bloats
`line_count` and review surface. Long how-to narration for one worker goes in
the execute brief (`.skills/<CODE>/task-N-brief.md`) at execute time; the shared
plan still carries the **identifiers** (paths, type names, commands) in Files /
Interfaces / Reuse so the brief cannot invent APIs.

**Done when:** every file in Step 2's map is covered by at least one task, and
each task is written as a vertical slice carrying its own test cycle. Whether
the slots and placeholders are clean is Step 4's check, not this one.

## Plan size budget (hard gate)

**Home for this rule.** Count in Step 4 and again at Exit before Approve. Other
sections only point here.

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

- Run the audit-trace check (REQUIRED SUB-SKILL: use `audit-trace`): every Approved
  requirement must be cited by ≥1 task footer. Uncited IDs mean the plan is
  incomplete (or the requirement should be struck through with a reason).
  audit-trace is **docs-only** — it does not require IDs in test source.
- **Behavior coverage via steps, not ID strings in code:** every requirement ID
  in a footer must have a corresponding TDD step (or explicit manual/acceptance
  step) that asserts the **behavior** in domain language. Do **not** require
  `[CODE-N.M]`, `/// REQ:`, or `@CODE-N.M` inside planned test source. Map IDs
  to tests in the task report / Spec review, not in production trees.
- **Reconcile against the design's seam table:** if `design.md` has a "Seams
  for testing" table, every ID in every row must have a planned test or
  acceptance step at that seam. An ID the design promised to cover but the plan
  left without a behavior test is *dropped coverage* — add the step, don't renumber.
- Type/name consistency across tasks: the same function must have the same
  name and signature in every task that mentions it.
- **Component-level reuse-miss:** flag any task whose Files **Create** something the scan digest
  or an already-installed dependency already provides — build on it instead of rebuilding it.
  This is the task-granularity sibling of the `reuse-miss` `inspect-change` raises for feature
  overlap; it is an advisory finding, not a hard block.
- **Reuse consistency:** flag any task whose `Reuse:` line disagrees with the `Reuse:` line of
  the design section it implements.
- Spec alignment: re-read requirements.md once, checking each criterion
  against the task that claims it.
- Upstream sync-back: if planning reveals a requirement is *wrong or infeasible
  as written* — not merely uncovered — correct it in requirements.md and
  re-surface for approval. Do not bury a workaround in a task that leaves the
  requirement lying; a plan that satisfies a false requirement ships the falsehood.

**Independent plan review — dispatch, don't self-review.** The checks above are
doc-only and stay here; the codebase comparison does not. Dispatch a review
subagent with the plan, requirements.md, design.md, and the repo; have it prove-claim
against real code every symbol, signature, path, import, and **hardcoded test
value** the plan asserts — a fabricated golden or a guessed API is the classic
plan defect — citing `file:line` and defaulting to flag. Findings to
`.skills/<CODE>/plan-review.md`; fix before offering execution. (No subagents? Do the
comparison yourself against the code.)

**Plan size:** run the **Plan size budget** counts here. Over ceiling → shrink
before Exit (do not present for Approve yet).

**Done when:** every requirement ID has a task footer and a planned behavior
test/acceptance step at an agreed seam, the docs-only audit-trace check is clean,
the design's seam-table IDs are all covered, the placeholder scan is clean, **and**
the **Plan size budget** is clear (or the plan was shrunk until it is).

## Step 5 (optional): Publish to the issue tracker

If the repo has no tracker (`docs/agents/issue-tracker.md` absent, or
**Tracker:** empty / none) → **skip** this step; not pending.

Otherwise run the publish recipe. Plan tasks stay in `tasks.md` and the execute
ledger. The default shipping unit on the tracker is the **feature**, closed by
the feature PR (close syntax from issue-tracker.md).

### Publish recipe

1. Read `docs/agents/issue-tracker.md`. Resolve **Publish unit** with this
   order (first match wins):
   - **`tasks`** only if the file sets `**Publish unit:** tasks`, **or** the
     user in this session explicitly orders per-task issues;
   - else **`feature`** (default when the field is absent or set to `feature`).
   Do not derive `tasks` from plan size, wave count, or “agents need tickets”.
2. IF create/publish is blocked (no auth, permission denied, role cannot open
   issues) → report the failure, leave the plan intact, **skip** remote create;
   do not open N task issues as a fallback.
3. **WHEN unit is `feature`:** create **exactly one** issue:
   - **Title:** `[CODE] <feature outcome>` (same sense as the plan Goal).
   - **Body** (behavior and interfaces, never file paths):
     - first line: `> *This issue was drafted by AI with \`plan-tasks\`.*`
     - What ships (end-to-end), high-level acceptance
     - `Requirements covered:` — **union** of every task footer ID
     - `Plan:` path to this `tasks.md`
     - `Roadmap:` `ROAD-N` / `MILE-N` when INDEX binds them; else omit
     - Optional: task checklist as plain markdown (not tracker issues)
   - Label only this issue with the frontier role (`ready-for-agent` mapped
     string) when it is grabbable.
   - Record the issue id under `.skills/<CODE>/` for execute / `land-branch`.
4. **WHEN unit is `tasks` (legacy only):** one issue per plan task in dependency
   order, each with its own `Requirements covered:` from that task’s footer;
   record all ids under `.skills/<CODE>/`. Still no silent invent of this unit.

Work that never went through the triad uses `/publish-issues` (multi-slice) —
do not re-file this plan there, and do not re-split a triad plan into
publish-issues slices under unit `feature`.

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

1. **Present the FILE and STOP.** Conversational agreement is not approval; the
   written plan is what gets approved. The execute family runs only on an
   approved `tasks.md`.
2. **Budget gate before Approve.** Follow **Plan size budget** (one home). Over
   ceiling → do **not** set Approved; run those remedies. Under ceiling → continue.
3. **On approval (budget clear):** set `Status: Approved`. Leave `Execution-mode:`
   as `unset` (or untouched). Do **not** write `continuous` or `story-unit` yourself.
4. **Offer exactly three execute routes** — one question, three skills. Do **not**
   first ask continuous vs story-unit; that interview is dead. Mode write-back is
   owned by the skill the user picks.

| Route | Meaning |
|---|---|
| **`build-by-story`** | Subagent path with human-gated review units derived from stories (writes `Execution-mode: story-unit`). Prefer `isolate-workspace` first. |
| **`build-in-waves`** | Subagent waves, no human pause between tasks (writes `Execution-mode: continuous`). Prefer `isolate-workspace` first. |
| **`build-inline`** | Controller implements sequentially with `test-first`, no implementer subagents (writes `Execution-mode: continuous` as bookkeeping; **does not** run unit barriers). |

**Recommend (offer label only — not invent mode):** mark **`build-by-story`
(Recommended)** first WHEN any of: user-facing UI/UX; Team band Solo or Small; or
`requirements.md` has **≥2** behavioral stories. Still offer all three; still wait
for an explicit pick. **No size-based default** means: never invent `Execution-mode`
and never silently start waves from task count — it does **not** forbid the
`(Recommended)` mark. Infra-only / no-UI with none of those triggers → leave the
offer unmarked.

5. **On pick:** name the skill and hand off — REQUIRED SUB-SKILL: use
   `build-in-waves`, `build-by-story`, or `build-inline` as chosen. For the two
   subagent routes, prefer REQUIRED SUB-SKILL: use `isolate-workspace` first when
   no isolated workspace exists yet.
6. **INDEX:** confirm the feature's row in `docs/specs/INDEX.md` carries the same
   `Status:` as its `requirements.md`.

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

**Done when:** the written `tasks.md` is **under the Plan size budget**, approved,
`Status:` reads `Approved`, one of the three execute skills is named (and handed
off when the user picks), `Execution-mode:` was not invented here, and the
INDEX.md row agrees.
