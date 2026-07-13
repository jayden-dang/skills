# Design: Correct-course — mid-flight plan-invalidation router

Feature code: CCOURSE
Status: Approved
Date: 2026-07-13
Requirements: ./requirements.md

## Context

The skill set drives an approved plan forward through `execute-plan`: waves of
fresh implementer subagents, a two-verdict task review, a whole-branch review at
the end. The loop is built to *not* pause — "the only legitimate stops: a BLOCKED
status you cannot resolve, ambiguity that genuinely prevents progress, or all tasks
complete" (`execute-plan/SKILL.md:14`). When a mid-execution discovery falsifies the
*approved plan itself* (not the code, not the current task), the loop has exactly one
move: the BLOCKED diagnose row "the plan itself is wrong → escalate to the user"
(`execute-plan/SKILL.md:60`), which dead-ends — it hands the mess to the user with no
classification and no route back into the chain. The circuit breaker
(`execute-plan/SKILL.md:38`) has the same shape: three failed fix cycles → "the task
is mis-scoped … escalate to the user." Nothing owns the *rewind decision*.

Three neighbours sit next to this gap but none fills it. `amend` (`track/amend`)
evolves an **already-shipped** feature with a small **forward** tweak — it picks a
lane *down* (tier 0/1/escalate). `sync-spec` (`track/sync-spec`) is the mechanical
reconciler that runs *after* a decision — it realigns the triad and the trace but
never *makes* the decision. `debug` fixes **broken code against a still-valid spec**.
`correct-course` is the missing router for the opposite case: valid code, a discovery
that falsifies the *spec's* premise mid-flight, any size, a **backward** rewind.

The governing constraint is that `correct-course` must be a **thin router**, not a
second copy of the spec skills. Its whole value is one decision — *which artifact is
now false, and how far back do we rewind* — made once, with the user in control at two
gates (diagnose, then propose). Everything downstream is delegation: content to the
`write-*` skills (each with its own approval gate), reconciliation to `sync-spec`, the
decision record to `domain-modeling`. If `correct-course` ever edits a
`requirements.md`/`design.md`/`tasks.md` itself, it has drifted into territory another
skill owns and will rot against it. The second constraint is **user control**: no plan
is ever rewritten silently — the diagnosis and the change proposal are both hard stops.

This repo has no `docs/architecture/` spine, so there are no `**ARCH-N**` invariants
to cite via `Respects:`; the sections below carry `Satisfies:` lines only. None of the
parts puts a new *interface* in question — a new model-invoked SKILL.md, a guarded prose
edit to one existing skill, and delegation to skills that already exist — so this is
single-design work, not a multi-variant interface bake-off.

## Decisions

1. **`correct-course` is a three-phase model-invoked skill** — diagnose → classify →
   route — in the `track/` bucket beside `amend` and `sync-spec`. Model-invoked (no
   `disable-model-invocation`) so `execute-plan` can hand off to it as a REQUIRED
   SUB-SKILL; also directly user-invokable.
2. **Two hard user gates, never an auto-rewrite.** Phase 1 ends by presenting the
   diagnosis and *stopping* for go/no-go; Phase 2 ends by presenting the change
   proposal and *stopping* for approval. Declining either is a clean no-op.
3. **The classifier is keyed on the lowest genuinely-invalidated artifact, with
   evidence** — one of Task-local / Plan / Design / Requirements / Vision. The decision
   rules live **inline** in the SKILL.md as a compact table (the way `amend` embeds its
   tier ladder), not in a separate reference file — the interface is a 5-row decision,
   too small to warrant its own file.
4. **The change proposal is ephemeral**; the durable trace is the re-entry skills'
   new/retired IDs, `sync-spec`'s strikethrough-with-reason, the commit, and the
   conditional ADR. No new persisted document class.
5. **Idempotency via an ephemeral evidence ledger** (`.skills/corrections.md`,
   git-ignored scratch parallel to `.skills/progress.md`): each acted-on correction is
   fingerprinted (evidence + chosen level); a divergence that would re-classify the same
   already-acted evidence to the same level without new evidence halts and escalates
   instead of looping.
6. **The only edit to an existing skill is a guarded two-point change to
   `execute-plan`**: the line-60 BLOCKED "plan is wrong" branch hands off unconditionally;
   the line-38 circuit breaker gains a root-cause step that hands off only when the
   lowest invalidated artifact is above the current task. The pre-flight review (line 24)
   and every other stop are untouched. No ADR is warranted — every decision here follows
   an existing idiom (a new SKILL.md, a REQUIRED SUB-SKILL hand-off, delegation) rather
   than overturning a principle.

## Architecture

### The correct-course skill — placement, frontmatter, boundaries

Satisfies: CCOURSE-1.3, CCOURSE-6.1, CCOURSE-6.2, CCOURSE-7.3

New **model-invoked** skill at `skills/track/correct-course/SKILL.md` (no
`disable-model-invocation`), so `execute-plan` may invoke it as a REQUIRED SUB-SKILL and
a user may invoke it directly. Body follows house style (imperative voice, per-step
**Done when:**, a `## Red Flags` block, a `| Thought | Reality |` rationalization table)
and stays under 500 lines. The frontmatter `description` is written trigger-plus-outcome
with **no unquoted colon-space** (`": "`) so the frontmatter linter passes (CCOURSE-7.3);
keywords packed for discovery: "discovery invalidates plan", "the plan is wrong",
"mid-execution", "re-plan", "scope changed".

Boundaries are enforced by a `## Red Flags — wrong skill` block that names the three
neighbours (CCOURSE-6.1, CCOURSE-6.2): a **post-ship in-scope tweak** hands to `amend`;
**broken code against a valid spec** hands to `debug`; and `sync-spec` is named as one of
`correct-course`'s *exits* (the mechanical reconciler that runs after the decision), never
the decision-maker — `correct-course` makes the rewind call, then delegates reconciliation.

### Phase 1 — the diagnosis gate

Satisfies: CCOURSE-2.1, CCOURSE-2.2, CCOURSE-2.3

The skill opens by authoring a **structured diagnosis notice** with five labelled parts —
**What** is wrong or changed, **Where** the deviation surfaced, **Why** the current plan
is no longer valid, **How** it impacts the remaining execution, and any other **context**
needed to decide (CCOURSE-2.1). It presents the notice and **hard-stops** for the user's
explicit go/no-go before any classification or artifact touch — the step's **Done when:**
is "the user has ruled go or no-go" (CCOURSE-2.2). A no-go is a clean exit: no spec or code
change, control returns without a rewind (CCOURSE-2.3). This is the same notice
`execute-plan` promised its user when it paused (What/Where/Why/How), authored here so the
diagnosis logic lives in one place rather than split across two skills.

### Phase 2 — the lowest-invalidated-artifact classifier

Satisfies: CCOURSE-3.1, CCOURSE-3.2, CCOURSE-3.3, CCOURSE-3.4

Only after the diagnosis go-ahead, the classifier identifies the **lowest** level in the
chain that is genuinely invalidated and cites the evidence for that determination
(CCOURSE-3.1). The decision rules are an inline table:

| Level | The discovery falsified… | Re-entry (see routing) |
|---|---|---|
| **Task-local** | only the current task's approach; the spec still holds | back to `execute-plan`/`tdd` |
| **Plan** | task breakdown / sequencing / coverage; design holds | `write-plan` |
| **Design** | an architecture/design decision; requirements hold | `write-design` → `write-plan` |
| **Requirements** | what was promised — a criterion is wrong or missing | `write-requirements` → design → plan |
| **Vision** | the feature's premise conflicts with product scope | vision layer, else escalate to a human |

The classification **law** is explicit and enforced in the body: pick the *lowest* level
with evidence; rewinding to a higher level "to be safe" without evidence for that higher
level is prohibited (CCOURSE-3.2). The classifier then presents a **change proposal** —
the chosen level, its evidence, and the proposed re-entry — and **hard-stops** for the
user's approval before routing (CCOURSE-3.3). The proposal is **ephemeral**: it lives in
the conversation for the go/no-go and is never written as a standalone artifact on disk
(CCOURSE-3.4).

### Idempotency — the evidence ledger

Satisfies: CCOURSE-3.5, CCOURSE-3.6

To keep the `execute-plan → correct-course → write-* → sync-spec → execute-plan` cycle from
looping on unchanged evidence, every rewind is treated as driven by **newly discovered
evidence** and recorded (CCOURSE-3.5). The record is an ephemeral ledger
`.skills/corrections.md` — git-ignored scratch parallel to `.skills/progress.md`, scoped to
the in-flight plan — with one line per acted-on correction carrying an evidence fingerprint,
the chosen level, and the outcome. Before classifying, `correct-course` reads the ledger:
IF the current divergence would re-classify the **same already-acted-on evidence to the same
lowest invalidated artifact** with no new evidence, it does **not** re-enter that level again
and instead escalates to the user, breaking the loop (CCOURSE-3.6). The ledger is scratch,
not a durable artifact — it does not conflict with the "no new persisted artifact" decision,
which concerns the *change proposal*.

### Phase 3 — routing and re-entry

Satisfies: CCOURSE-4.1, CCOURSE-4.2, CCOURSE-4.3, CCOURSE-4.4, CCOURSE-4.5, CCOURSE-4.6

On proposal approval, `correct-course` routes to the matching re-entry, invoking each as a
REQUIRED SUB-SKILL **directly** (never merely suggesting the user run it) and letting that
skill run its **own** approval gate (CCOURSE-4.6):

- **Task-local** → return to `execute-plan`/`tdd`; no upstream artifact is rewound
  (CCOURSE-4.1).
- **Plan** → `write-plan` (CCOURSE-4.2).
- **Design** → `write-design`, which flows forward into `write-plan` (CCOURSE-4.3).
- **Requirements** → `write-requirements`, which flows forward into design and plan
  (CCOURSE-4.4).
- **Vision** → WHERE `docs/product/vision.md` exists, route the premise conflict to the
  vision layer; WHERE it does not exist (this repo), **escalate to the user** for a human
  decision and re-enter `brainstorm` only if the user agrees the premise is in question
  (CCOURSE-4.5). This mirrors the optional-doc idiom used across the project layer — the
  level is never silently dropped; with no vision doc it routes to a human instead of a file.

All five re-entry targets (`write-plan`, `write-design`, `write-requirements`, `brainstorm`,
`execute-plan`/`tdd`) are model-invoked, so `correct-course` — itself model-invoked — may
compose them as sub-skills.

### Thin router — delegation, reconciliation, ADR, resume

Satisfies: CCOURSE-5.1, CCOURSE-5.2, CCOURSE-5.3, CCOURSE-5.4, CCOURSE-5.5

`correct-course` holds **no** requirement/design/plan/tasks/trace editing logic of its own:
all spec-content generation is delegated to the `write-*` skills and all triad
reconciliation to `sync-spec` (CCOURSE-5.1) — enforced by a Red-Flags line and by the fact
that its only file writes are the ephemeral diagnosis/proposal (conversation) and the
`.skills/corrections.md` ledger. The exit sequence after the re-entry skill's approval gate
passes:

1. **Reconcile** — WHEN the re-entry changed already-approved artifacts or their trace
   links, invoke `sync-spec` to realign `Status` and the trace (CCOURSE-5.2). `sync-spec`
   owns the strikethrough-with-reason retirement and INDEX.md update; `correct-course` does
   not reimplement it.
2. **Record** — WHEN the final approved change carries an **architectural consequence**,
   record it as an ADR via `domain-modeling` (CCOURSE-5.3). Design-level rewinds usually
   qualify; Requirements/Vision only when architecturally weighty; Task-local and Plan-level
   **never** get an ADR. An ADR is **never** persisted for a proposal the user did not
   approve (CCOURSE-5.4).
3. **Resume** — WHEN routing, reconciliation, and any ADR are complete, return control to
   `execute-plan`, which resumes **automatically** against the corrected plan off its ledger
   (CCOURSE-5.5). For a **Task-local** rewind the `.skills/progress.md` ledger is untouched
   and resume is unchanged. For a **Plan/Design/Requirements** rewind that rewrote
   `tasks.md`, the ledger's task-numbered "complete" lines no longer map onto the new task
   set, so before handing back `correct-course` **re-baselines the ledger**: it keeps the
   entries whose committed work survives the rewrite and drops the entries the rewrite
   superseded, so `execute-plan` resumes after the last *still-valid* completed task rather
   than a stale number. The ledger is git-ignored scratch, so re-baselining it touches no
   spec artifact and CCOURSE-5.1 still holds. No manual restart.

### execute-plan hand-off edit (guarded)

Satisfies: CCOURSE-1.1, CCOURSE-1.2, CCOURSE-1.4, CCOURSE-1.5

Two edits to `skills/execution/execute-plan/SKILL.md`, both guarded so no other behaviour
shifts:

- **BLOCKED table, line 60** — the diagnose branch "the plan itself is wrong → escalate to
  the user" becomes "the plan itself is wrong → pause and REQUIRED SUB-SKILL: use
  `correct-course`" (CCOURSE-1.1). The other three BLOCKED diagnose branches (missing
  context, reasoning ceiling, task too large) and the redispatch cap are unchanged.
- **Circuit breaker, line 38** — after "if the same finding survives 3 fix→re-review
  cycles, stop looping," add a **root-cause step**: determine the lowest invalidated
  artifact; IF it is **above the current task**, hand off to `correct-course`; ELSE continue
  the existing "escalate to the user with the finding and the three attempts" flow
  (CCOURSE-1.2). The breaker itself still trips at three cycles exactly as today.

Guards, verified against the current file: the pre-flight plan review (step 5, line 24)
batches its findings into one pre-dispatch question and is **untouched** (CCOURSE-1.5); every
BLOCKED status the loop cannot resolve for a reason *other* than "plan is wrong", plus genuine
ambiguity and all-tasks-complete (line 14), **continue to** stop/handle as today without
routing to `correct-course` (CCOURSE-1.4). Both edits are prose changes in the idiom of the
existing REQUIRED SUB-SKILL hand-offs already in this file (e.g. `worktrees`, `code-review`).

### Roster registration

Satisfies: CCOURSE-7.1, CCOURSE-7.2

`correct-course` is appended to `.claude-plugin/plugin.json`'s `skills` array (so it groups
under the plugin in the picker) and registered across every roster surface, moving each
skill-count from **35 to 36** (CCOURSE-7.1):

- **AGENTS.md** — the §8 file-org tree (`track/` line), the §11 "The 35 Skills" quick-ref
  table (new `track` row), and the count in the header (line 3) and §8 comment (→36).
- **DESIGN.md** — the skill inventory `track/` list and the "35 skills" count (→36).
- **docs/guide/skills/** — a new page `correct-course.md`, the `track` table row and the
  "Thirty-five skills" opening count in `README.md` (→36), and any phase/overview table.
- **`skills/meta/ask/SKILL.md`** — an on-ramp line routing "a mid-execution discovery
  invalidated my approved plan" → `correct-course` (CCOURSE-7.2).

## Seams for testing

Per the approved verification approach (baseline scenarios, no automated test code), each
"seam" is the skill invocation that exercises the requirement; evidence is a documented
baseline scenario under `baselines/`, tagged with the covered IDs and cited as coverage for
`trace` (whose E2 is documented-exempt here). No new automated test seam is added.

| Seam | Kind | Covers |
|---|---|---|
| `correct-course` skill file — placement, frontmatter, boundary Red Flags | baseline | CCOURSE-1.3, 6.1, 6.2, 7.3 |
| Phase 1 diagnosis run → notice presented, stop, no-go is a no-op | baseline | CCOURSE-2.1, 2.2, 2.3 |
| Phase 2 classify run → lowest-artifact + evidence, ephemeral proposal, stop | baseline | CCOURSE-3.1, 3.2, 3.3, 3.4 |
| Idempotency run → repeated evidence halts and escalates | baseline | CCOURSE-3.5, 3.6 |
| Routing run per level (Task-local / Plan / Design / Requirements / Vision) | baseline | CCOURSE-4.1, 4.2, 4.3, 4.4, 4.5, 4.6 |
| Thin-router run → delegate, sync-spec, conditional ADR, resume | baseline | CCOURSE-5.1, 5.2, 5.3, 5.4, 5.5 |
| `execute-plan` edit — line 60 handoff, line 38 root-cause, guards intact | baseline | CCOURSE-1.1, 1.2, 1.4, 1.5 |
| Roster registration review of the diff → 36 across surfaces, ask on-ramp | baseline | CCOURSE-7.1, 7.2 |

## Coverage check

Every CCOURSE ID appears in exactly one Satisfies line:

- Story 1: 1.1,1.2,1.4,1.5 (execute-plan edit) · 1.3 (skill placement)
- Story 2: 2.1,2.2,2.3 (Phase 1)
- Story 3: 3.1,3.2,3.3,3.4 (Phase 2) · 3.5,3.6 (idempotency ledger)
- Story 4: 4.1,4.2,4.3,4.4,4.5,4.6 (Phase 3 routing)
- Story 5: 5.1,5.2,5.3,5.4,5.5 (thin router)
- Story 6: 6.1,6.2 (skill placement / boundaries)
- Story 7: 7.1 (roster) · 7.2 (roster / ask) · 7.3 (skill placement / frontmatter)

All 30 criteria mapped; none deliberately unmapped.
