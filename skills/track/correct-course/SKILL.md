---
name: correct-course
description: Use when a mid-execution discovery invalidates an already-approved plan —
  "the plan is wrong," a re-plan is needed, scope changed mid-flight, or a
  divergence surfaces during execute-plan or tdd that the current task can't
  absorb. Produces a blast-radius classification of the lowest invalidated
  artifact plus a re-entry decision or change proposal, never a silent
  rewrite. Not for a post-ship in-scope tweak (amend), broken code against a
  still-valid spec (debug), or the mechanical reconciliation that runs after
  the decision (sync-spec).
---

# Correct Course

The mid-flight rewind decision for when a discovery falsifies an approved plan. It is a **thin router**: it decides *which artifact is now false and how far back to rewind*, then delegates — it never rewrites a requirement, a design, a plan, or trace metadata itself. `execute-plan` hands off here when it hits "the plan itself is wrong" or a circuit breaker whose root cause sits above the current task; a user may also invoke it directly the moment something feels off.

Three phases, in order: diagnose, classify, route. Two hard stops, never an auto-rewrite.

## Phase 1 — Diagnose (hard stop for the user)

Author a structured diagnosis notice with five labelled parts:

- **What** is wrong or changed
- **Where** the deviation surfaced
- **Why** the current plan is no longer valid
- **How** it impacts the remaining execution
- Any other **context** needed to decide

Present the notice and **STOP**. Do not classify, do not touch any artifact, do not proceed until the user has ruled explicitly.

**Done when:** the user has ruled go or no-go.

If the user declines: make no spec or code change and return control without a rewind. This is a clean no-op, not a partial rewind — nothing on disk moves.

## Phase 2 — Classify the lowest invalidated artifact

Only after the diagnosis go-ahead. Identify the **lowest** level in the chain genuinely invalidated, and cite the evidence for it:

| Level | The discovery falsified… | Re-entry (Phase 3) |
|---|---|---|
| **Task-local** | only the current task's approach; the spec still holds | back to `execute-plan`/`tdd` |
| **Plan** | task breakdown / sequencing / coverage; design holds | `write-plan` |
| **Design** | an architecture/design decision; requirements hold | `write-design` → `write-plan` |
| **Requirements** | what was promised — a criterion is wrong or missing | `write-requirements` → design → plan |
| **Vision** | the feature's premise conflicts with product scope | vision layer, else escalate to a human |

**The classification law:** pick the *lowest* level with evidence. Rewinding to a higher level "to be safe," without evidence for that higher level, is **prohibited**. A discovery that only breaks the current task's approach does not earn a trip to `write-requirements` just because the rewind feels safer big.

Present a **change proposal** — the chosen level, its evidence, and the proposed re-entry — and **STOP** for the user's approval before routing.

**Done when:** the user approves the proposal.

The proposal is **ephemeral**: it lives in the conversation for the go/no-go and is **never** written as a standalone artifact on disk. Nothing under `docs/specs/` records "a change was proposed" — only the eventual re-entry skill's own edits, and the ledger below, leave a trace.

## Idempotency — the evidence ledger

Every rewind must be driven by **newly discovered evidence** — not a second look at the same fact. Before classifying, read `.skills/corrections.md` (ephemeral, git-ignored scratch, parallel to `.skills/progress.md`, scoped to the in-flight plan). It carries one line per acted-on correction: an **evidence fingerprint**, the **chosen level**, and the **outcome**.

IF the current divergence would re-classify the **same already-acted-on evidence to the same lowest invalidated artifact**, with no new evidence, do **NOT** re-enter that level again. Escalate to the user instead — this breaks the `execute-plan → correct-course → write-* → sync-spec → execute-plan` loop before it spins. A genuinely new discovery is not blocked by this: record its fingerprint, its level, and its outcome as a new ledger line, and classify normally.

**Done when:** the ledger has been read before classifying, and either escalation fired (repeat, no new evidence) or a new line was recorded (genuinely new evidence).

Note the ledger is scratch, not a durable spec artifact — recording to it does not conflict with the ephemeral-proposal rule above, which concerns the change *proposal*, not this correction log.

## Phase 3 — Route and re-enter

On proposal approval, route to the matching re-entry. Invoke each as a REQUIRED SUB-SKILL **directly** — never merely suggest the user run it — and let that skill run its **own** approval gate:

- **Task-local** → return to `execute-plan`/`tdd`; no upstream artifact is rewound.
- **Plan** → REQUIRED SUB-SKILL: use `write-plan`.
- **Design** → REQUIRED SUB-SKILL: use `write-design`, which flows forward into `write-plan`.
- **Requirements** → REQUIRED SUB-SKILL: use `write-requirements`, which flows forward into design and plan.
- **Vision** → WHERE `docs/product/vision.md` exists, route the premise conflict to the vision layer. WHERE it does not exist, **escalate to the user** for a human decision, and re-enter REQUIRED SUB-SKILL: use `brainstorm` **only if** the user agrees the premise is genuinely in question.

**Done when:** the matching sub-skill has been invoked directly and its own gate is running — `correct-course` does not fabricate a second approval step on top of it.

## Thin-router exit — delegate, reconcile, record, resume

`correct-course` **never** rewrites requirements, design, plan, tasks, or trace metadata itself. All spec-content generation delegates to the `write-*` skills; all triad reconciliation delegates to `sync-spec`.

After the re-entry skill's approval gate passes:

1. **Reconcile.** WHEN the re-entry changed already-approved artifacts or their trace links, REQUIRED SUB-SKILL: use `sync-spec` to realign `Status` and the trace — it owns the strikethrough-with-reason retirement and the INDEX update; `correct-course` does not reimplement any of it.
2. **Record.** WHEN the final approved change carries an **architectural consequence**, record it as an ADR via REQUIRED SUB-SKILL: use `domain-modeling`. Design-level rewinds usually qualify; Requirements or Vision rewinds only when architecturally weighty. **Task-local and Plan-level never** get an ADR. **Never** persist an ADR for a proposal the user did not approve.
3. **Resume.** Return control to `execute-plan`, which resumes **automatically** against the corrected plan off its own ledger — no manual restart. For a **Task-local** rewind, `.skills/progress.md` is untouched. For a **Plan / Design / Requirements** rewind that rewrote `tasks.md`, **re-baseline the ledger** first: keep the entries whose committed work survives the rewrite, drop the entries the rewrite superseded, so `execute-plan` resumes after the last *still-valid* completed task rather than a stale task number. The ledger is git-ignored scratch, so this touches no spec artifact.

**Done when:** reconciliation has run if artifacts changed, an ADR exists only if warranted and approved, and `execute-plan` is resuming against a ledger that matches the (possibly rewritten) `tasks.md`.

## Red Flags — wrong skill

- **A post-ship, in-scope tweak** to a shipped feature (a recolor, a copy edit, a small follow-on) → that is `amend`, not correct-course. Nothing was "approved and then invalidated" here — the feature already shipped.
- **Broken code against a still-valid spec** → that is `debug`, not correct-course. The spec is still true; only the implementation is wrong.
- **`sync-spec` is an exit, not a decision-maker.** It is the mechanical reconciler that runs *after* the rewind decision, realigning `Status` and the trace. correct-course makes the call about which artifact is false; it does not do sync-spec's bookkeeping, and sync-spec does not make the rewind call.
- The pre-flight plan review inside `execute-plan` (its pre-dispatch consistency scan) is pre-execution, not a mid-flight discovery — it is not this skill's trigger.

| Thought | Reality |
|---|---|
| "This discovery smells big, I'll just rewind to requirements to be safe" | Classify the LOWEST invalidated artifact with evidence. Over-rewinding without evidence for the higher level is prohibited — it burns approvals the discovery never earned. |
| "The user already agreed something's wrong, I can skip straight to routing" | The diagnosis go/no-go and the change-proposal approval are two separate stops. Agreeing something is wrong is not the same as approving a specific re-entry. |
| "I'll just fix the plan file directly, it's faster" | correct-course holds no editing logic. Route to `write-plan`/`write-design`/`write-requirements` — they own the content and their own gate. |
| "Same bug came up again, let me rewind again" | Read `.skills/corrections.md` first. Same evidence, same level, no new discovery → escalate to the user instead of looping. |
