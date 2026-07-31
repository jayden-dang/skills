# `reroute-plan`

> The mid-flight rewind decision — classifies a discovery that invalidates an approved plan to the lowest invalidated artifact and routes to the right re-entry, delegating content to `write-*` and reconciliation to `realign-spec`.

|  |  |
|---|---|
| **Bucket** | track |
| **Invocation** | model-invocable (the agent calls it on its own); also user-invocable |
| **Reads** | `.skills/progress.md` and `.skills/corrections.md` (the evidence ledger); the spec triad it may route into |
| **Writes** | nothing durable — an ephemeral diagnosis/change-proposal that lives only in the conversation, plus a new line in the git-ignored `.skills/corrections.md` ledger |
| **Calls** | [`specify-behavior`](specify-behavior.md), [`design-solution`](design-solution.md), [`plan-tasks`](plan-tasks.md), [`frame-change`](frame-change.md) (vision-level only, with user agreement), [`realign-spec`](realign-spec.md) (reconcile after re-entry), [`define-domain`](define-domain.md) (ADR when the change is architecturally weighty), [`build-continuous`](build-continuous.md) / [`test-first`](test-first.md) (task-local re-entry and resume) |
| **Called by** | [`build-continuous`](build-continuous.md) when the plan itself is wrong or a circuit breaker's root cause sits above the current task; or the user directly the moment something feels off |

## When it fires

A mid-execution discovery invalidates an already-approved plan — "the plan is wrong," scope
changed mid-flight, or a divergence surfaces during [`build-continuous`](build-continuous.md) or
[`test-first`](test-first.md) that the current task can't absorb. It is a **thin router**: it decides which
artifact is now false and how far back to rewind, then delegates — it never rewrites a
requirement, a design, a plan, or audit-trace metadata itself.

Three phases, in order: diagnose, classify, route. Two hard stops, never an auto-rewrite.

## 1. Diagnose (hard stop for the user)

Author a structured diagnosis notice with five labelled parts — **what** is wrong or changed,
**where** it surfaced, **why** the current plan no longer holds, **how** it impacts the
remaining execution, and any other **context** needed to decide. Present the notice and
**STOP**. Do not classify, do not touch any artifact, do not proceed until the user has ruled
explicitly.

If the user declines, this is a clean no-op — no spec or code change, nothing on disk moves.

**Done when:** the user has ruled go or no-go.

## 2. Classify the lowest invalidated artifact

Only after the diagnosis go-ahead. Identify the **lowest** level in the chain genuinely
invalidated, with evidence:

| Level | The discovery falsified… | Re-entry |
|---|---|---|
| **Task-local** | only the current task's approach; the spec still holds | back to `build-continuous`/`test-first` |
| **Plan** | task breakdown / sequencing / coverage; design holds | `plan-tasks` |
| **Design** | an architecture/design decision; requirements hold | `design-solution` → `plan-tasks` |
| **Requirements** | what was promised — a criterion is wrong or missing | `specify-behavior` → design → plan |
| **Vision** | the feature's premise conflicts with product scope | vision layer, else escalate to a human |

**The classification law:** pick the *lowest* level with evidence. Rewinding higher "to be
safe," without evidence for that higher level, is prohibited.

Present a **change proposal** — the chosen level, its evidence, and the proposed re-entry —
and **STOP** for the user's approval before routing. The proposal is ephemeral: it lives in
the conversation for the go/no-go and is never written as a standalone artifact on disk.

**Done when:** the user approves the proposal.

## 3. Route and re-enter

On proposal approval, route to the matching re-entry, invoking it as a REQUIRED SUB-SKILL
directly — never merely suggesting the user run it — and letting that skill run its own
approval gate: Task-local returns to `build-continuous`/`test-first`; Plan uses
[`plan-tasks`](plan-tasks.md); Design uses [`design-solution`](design-solution.md) (which flows
forward into `plan-tasks`); Requirements uses
[`specify-behavior`](specify-behavior.md) (which flows forward into design and plan);
Vision routes to the vision layer where `docs/product/vision.md` exists, otherwise escalates
to the user and re-enters [`frame-change`](frame-change.md) only if the user agrees the premise is
genuinely in question.

After the re-entry skill's own gate passes: reconcile via
[`realign-spec`](realign-spec.md) when already-approved artifacts or trace links changed; record an
ADR via [`define-domain`](define-domain.md) when the approved change carries an
architectural consequence (Design-level rewinds usually qualify; Task-local and Plan-level
never do); then resume `build-continuous` automatically off its own ledger — re-baselining
`.skills/progress.md` first if `tasks.md` was rewritten, so execution resumes after the last
still-valid completed task.

**Done when:** the matching sub-skill has been invoked directly and its own gate is running;
reconciliation has run if artifacts changed; an ADR exists only if warranted and approved; and
`build-continuous` is resuming against a ledger that matches the (possibly rewritten) `tasks.md`.

## Idempotency — the evidence ledger

Every rewind must be driven by newly discovered evidence, not a second look at the same fact.
Before classifying, read `.skills/corrections.md` (ephemeral, git-ignored scratch, scoped to
the in-flight plan) — one line per acted-on correction: an evidence fingerprint, the chosen
level, and the outcome. If the current divergence would re-classify the same already-acted-on
evidence to the same lowest invalidated artifact, with no new evidence, do **not** re-enter
that level again — escalate to the user instead. A genuinely new discovery is not blocked:
record its fingerprint, level, and outcome as a new ledger line, and classify normally.

## Red flags — you are in the wrong lane

- **A post-ship, in-scope tweak** to a shipped feature (a recolor, a copy edit, a small
  follow-on) → that is [`amend-feature`](amend-feature.md), not reroute-plan. Nothing was "approved and then
  invalidated" here — the feature already shipped.
- **Broken code against a still-valid spec** → that is [`root-cause`](root-cause.md), not reroute-plan.
  The spec is still true; only the implementation is wrong.
- **[`realign-spec`](realign-spec.md) is an exit, not a decision-maker.** It is the mechanical
  reconciler that runs *after* the rewind decision; reroute-plan makes the call about which
  artifact is false, and realign-spec does not make the rewind call.
- The pre-flight plan review inside [`build-continuous`](build-continuous.md) (its pre-dispatch
  consistency scan) is pre-execution, not a mid-flight discovery — it is not this skill's
  trigger.

## Worked example

Mid-execution, an implementer discovers the design's chosen caching strategy cannot satisfy a
requirement it was meant to serve — the design decision itself, not just the current task, is
wrong.

**Diagnose.** The notice: **what** — the design's cache invalidation strategy cannot meet the
requirement's staleness bound; **where** — surfaced while implementing the read-path task;
**why** — the design assumed a property the underlying store does not provide; **how** — every
remaining task built on this design is now suspect; **context** — one alternative strategy is
already known to work. Presented and **STOP**. The user rules go.

**Classify.** The requirement itself still holds — only the design's approach to satisfying it
is wrong. That is **Design-level**, not Requirements-level: rewinding to requirements would be
over-rewinding without evidence the promise itself is wrong. Proposal: Design-level, re-enter
`design-solution`. **STOP** for approval; the user approves.

**Route and reconcile.** REQUIRED SUB-SKILL: use `design-solution` to revise the caching
decision, which flows forward into `plan-tasks` to re-sequence the remaining tasks. Because an
already-approved design artifact changed, REQUIRED SUB-SKILL: use `realign-spec` to realign
`Status:` and the trace. The design change is architecturally weighty, so REQUIRED SUB-SKILL:
use `define-domain` to record an ADR. `.skills/progress.md` is re-baselined to drop the
tasks the rewrite superseded, and `build-continuous` resumes automatically against the corrected
plan.

## Why it is written the way it is

`reroute-plan` is a **thin router**, not an editor: all spec-content generation delegates to
the `write-*` skills and all triad reconciliation delegates to `realign-spec`, so the skill never
duplicates their logic or their approval gates. The **lowest-invalidated-artifact law** exists
because an agent under pressure will over-rewind "to be safe" — burning approvals a discovery
never earned — so the classification must cite evidence for the level it picks, not a feeling.
The **two hard stops** (diagnose go/no-go, then change-proposal approval) are separate because
agreeing something is wrong is not the same as approving a specific re-entry — collapsing them
would let a rewind happen without the user ever seeing the proposed blast radius. The
**evidence ledger** exists to break the `build-continuous → reroute-plan → write-* → realign-spec →
build-continuous` loop before it spins on the same fact twice.

## See also

- [`amend-feature`](amend-feature.md) — the lane for a post-ship, in-scope tweak; nothing here was "approved
  then invalidated"
- [`realign-spec`](realign-spec.md) — the mechanical reconciler this skill delegates to after a
  re-entry changes approved artifacts
- [`build-continuous`](build-continuous.md) — the caller this skill hands control back to once the
  rewind is resolved
