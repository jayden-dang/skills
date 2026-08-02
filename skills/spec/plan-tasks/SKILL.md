---
name: plan-tasks
description: Use when a design is approved and the tasks.md implementation plan
  (vertical-slice tasks with requirement footers and behavior tests) needs writing,
  after design-solution and before the execute family (build-in-waves /
  build-by-story / build-inline).
---

Produce `docs/specs/<YYYY-MM-DD>-<feature>/tasks.md` from the approved requirements
and design. Start from the skill set's `templates/tasks.md` — resolve `templates/`
as `${CLAUDE_PLUGIN_ROOT}/templates` when installed as a plugin, otherwise
`../../../templates` relative to this SKILL.md. Every slot in a task block
(**Files**, **Interfaces**, **Depends-on**, **Steps**, `_Requirements:_`) is
REQUIRED. Do **not** author per-task risk labels, decision-surface flags, or a
Human-review-order section — risk is measured by select-review-sample risk globs
against the actual diff; review units are **derived** from user stories at
`build-by-story` time (see that skill).

Create a todo per step (1–4, plus 5 if the repo uses an issue tracker) before starting, and complete them in order — this skill owns its own list, distinct from `design-solution`'s upstream and the execute family's downstream. Check each off only when its **Done when:** is met.

Write for an implementer who is skilled but knows NOTHING about this codebase
or problem domain, and will see ONLY their own task plus the Global
Constraints. Every name, path, command, and type they need must be in the task.

## Step 1: Header and Global Constraints

Goal (one sentence), Architecture (2–3 sentences), Tech Stack. Header also
carries the bookkeeping field:

```
Execution-mode: <unset | continuous | story-unit>
```

Leave `Execution-mode: unset` while planning — never invent continuous/story-unit
from plan size, band, or habit. Route choice and mode write-back live only at
**Exit** (and in the chosen execute skill).

Then **Global Constraints**: project-wide rules copied verbatim from the design
and `docs/agents/project.md` — test/lint/typecheck commands, naming and i18n
rules, forbidden changes. Every task's requirements implicitly include this
section; it travels with each task brief. When `## Team` is present with a
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
`unset`), and Global Constraints are written, and every command, naming/i18n
rule, and `ARCH-N` invariant in that section is copied verbatim from its source
file rather than paraphrased.

## Step 2: File structure first

Map every file the plan creates or modifies, with one-line responsibilities,
BEFORE writing tasks. A file not in the map should not be touched by any task.

### Codebase Map consult (optional system-doc)

**Applicability:** this step is writing or revising File Structure / path placement
for production paths.

**Hard constraints (outrank any Codebase Map):**

1. Approved feature `requirements.md` / `design.md` for the plan under construction
2. Live `ARCH-N` invariants in Global Constraints
3. Standing project constraints already sourced (`docs/standards/` when present,
   else legacy `docs/product/guidelines.md` fallback, else `docs/agents/project.md`,
   and other standing config this skill reads)

**Authority (`docs/codebase/map.md`):**

- **Absent** — no file
- **Non-authoritative** — file present but `Status` is not `Approved`, or the
  structural validator in `skills/project/define-system-doc/validators/codebase/map.md`
  fails (including external Draft)
- **Approved** — `Status: Approved` and structural validator pass

**When Approved:** extract layout + placement rules; align the File Structure map
**within** hard constraints; note that the Codebase Map was consulted.

**When absent or non-authoritative:** CONTINUE without failing the skill solely for
map absence (no-op consult). IF placement of new or changed production paths is
materially uncertain THEN suggest **at most once per plan-tasks run** the exact
action `/define-system-doc codebase/map` and explain why the map would help now.
Suppress further suggestions for that entry for the rest of the run after decline.
Persist defer only if the user supplies an explicit condition. **NEVER** auto-invoke
`define-system-doc` (user-invoked; ARCH-5).

**Placement conflict:** IF an Approved map rule conflicts with a hard constraint
THEN surface the conflict (name hard constraint + map rule), **preserve the hard
constraint** in File Structure, suggest `/define-system-doc codebase/map` to update
the map (counts toward the once-per-run budget when emitted), and never silently
follow the map over the hard constraint or silently ignore a detected conflict.

### Engineering standards docs (optional)

**Applicability:** Global Constraints need testing or errors/logging house rules
beyond ARCH-N and machine config.

**Authority:** `docs/standards/INDEX.md`, `testing.md`, `errors-logging.md` — each
**Approved** only when `Status: Approved` and the structural validator under
`skills/project/define-system-doc/validators/standards/` passes (for consumer files
authored via define-system-doc). Pack-maintained standards already in-repo are
treated as present standing rules when the file exists and is the SSOT path.

**When present:** fold applicable rules into Global Constraints (verbatim where
practical). Prefer `docs/standards/` over guidelines.

**When absent:** use legacy guidelines fallback or project.md as above; CONTINUE
without failing solely for missing standards files. IF standards would materially
improve Global Constraints, suggest **at most once per entry key per plan-tasks run**
`/define-system-doc standards/INDEX|testing|errors-logging`; **NEVER** auto-invoke.

### Codebase navigation docs (modules / ownership / dependencies)

Same authority pattern as Codebase Map (`Status: Approved` + structural validator
pass under `skills/project/define-system-doc/validators/codebase/<entry>.md`).
Hard constraints still outrank these docs; conflict procedure matches Codebase Map
(surface, preserve hard constraint, suggest `/define-system-doc <entry-key>`, never
auto-invoke). Suggestion budget is **at most once per entry key per plan-tasks run**.

| Entry | Canonical path | When to consult if Approved |
|---|---|---|
| `codebase/modules` | `docs/codebase/modules.md` | Module boundary placement in File Structure |
| `codebase/ownership` | `docs/codebase/ownership.md` | Ownership notes (advisory; not access control) |
| `codebase/dependencies` | `docs/codebase/dependencies.md` | Avoid planning paths that imply forbidden dependency directions |

**When absent or non-authoritative:** CONTINUE (no-op) for that entry; may suggest
`/define-system-doc codebase/modules|ownership|dependencies` when that gap makes
placement or dependency direction materially uncertain.

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
  edge, so `build-in-waves` can run them together in one parallel wave. Omit the
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

**Done when:** every file in Step 2's map is covered by at least one task, and
each task is written as a vertical slice carrying its own test cycle. Whether
the slots and placeholders are clean is Step 4's check, not this one.

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

**Done when:** every requirement ID has a task footer and a planned behavior
test/acceptance step at an agreed seam, the docs-only audit-trace check is clean,
the design's seam-table IDs are all covered, and the placeholder scan is clean.

## Step 5 (optional): Publish to the issue tracker

If the repo uses one (`docs/agents/issue-tracker.md`), publish each task as an
issue in dependency order — native sub-issues and blocking links where
supported; body describes behavior and interfaces (never file paths), includes
acceptance criteria and a `Requirements covered:` list.

This is the heavyweight, traceable publish path — each issue carries its
requirement IDs. For capturing work that never went through the spec triad (a
raw conversation or idea), the user runs `publish-issues` instead; do not duplicate
these tasks there.

**Done when:** every task in `tasks.md` has an issue, each issue carries its
`Requirements covered:` list, and the blocking links match the plan's
dependency order. No tracker configured → this step is skipped, not pending.

## Exit

1. **Present the FILE and STOP.** Conversational agreement is not approval; the
   written plan is what gets approved. The execute family runs only on an
   approved `tasks.md`.
2. **On approval:** set `Status: Approved`. Leave `Execution-mode:` as `unset`
   (or untouched). Do **not** write `continuous` or `story-unit` yourself.
3. **Offer exactly three execute routes** — one question, three skills. Do **not**
   first ask continuous vs story-unit; that interview is dead. Mode write-back is
   owned by the skill the user picks.

| Route | Meaning |
|---|---|
| **`build-in-waves`** | Subagent waves, no human pause between tasks (writes `Execution-mode: continuous`). Prefer `isolate-workspace` first. |
| **`build-by-story`** | Subagent path with human-gated review units derived from stories (writes `Execution-mode: story-unit`). Prefer `isolate-workspace` first. |
| **`build-inline`** | Controller implements sequentially with `test-first`, no implementer subagents (writes `Execution-mode: continuous` as bookkeeping; **does not** run unit barriers). |

4. **On pick:** name the skill and hand off — REQUIRED SUB-SKILL: use
   `build-in-waves`, `build-by-story`, or `build-inline` as chosen. For the two
   subagent routes, prefer REQUIRED SUB-SKILL: use `isolate-workspace` first when
   no isolated workspace exists yet.
5. **INDEX:** confirm the feature's row in `docs/specs/INDEX.md` carries the same
   `Status:` as its `requirements.md`.

| Thought | Reality |
|---|---|
| "PM said just mark Approved — continuous is obvious" | Approval is the written plan. Offer the three skills; do not invent mode |
| "Standup in five — skip asking which execute skill" | Time changes *when* you ask, not whether a route is named |
| "Four tasks → default build-in-waves" | No size-based default. User picks one of the three |
| "I'll ask continuous vs story-unit, then offer routes" | Redundant. One question: which of the three skills |
| "User said approve and start building — write continuous and go" | Approve + offer three routes. "Start building" is not a route pick |
| "I'll write Execution-mode now so the plan looks complete" | Completeness is Status + route name. Mode is written by the execute skill |

### Red Flags — Exit

- Asking continuous vs story-unit before (or instead of) the three-skill offer
- Setting `Status: Approved` while inventing `Execution-mode: continuous`
- Offering only one route, or skipping the offer after approval
- Writing `Execution-mode:` in plan-tasks instead of letting the execute skill do it
- Treating "LGTM, build it" as a silent default to `build-in-waves`

**Done when:** the written `tasks.md` is approved, `Status:` reads `Approved`,
one of the three execute skills is named (and handed off when the user picks),
`Execution-mode:` was not invented here, and the INDEX.md row agrees.
