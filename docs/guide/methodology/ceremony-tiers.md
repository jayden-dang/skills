# Ceremony tiers

The standard objection to spec-driven development is that it buries a two-line change under paperwork. The three-tier system is the answer, and it is load-bearing enough to deserve its own page.

## The tiers

| Tier | When | Artifacts produced |
|---|---|---|
| **0 — trivial** | typo-level; no behavior change | none — [`tdd`](../skills/tdd.md) and [`verify`](../skills/verify.md) only |
| **1 — bugfix / small change** | a behavior change taking ≤ ~half a day | a mini-spec: one fix requirement plus a `SHALL CONTINUE TO` guard appended to the owning feature's `requirements.md` (or `docs/specs/fixes.md`), and a tagged regression test. No `design.md`; task list optional |
| **2 — feature** | multi-task work | the full triad — `requirements.md`, `design.md`, `tasks.md` — then [`execute-plan`](../skills/execute-plan.md) |

## The tier decision *is* the design step

This is the part that gets missed.

Naming the tier is not a way to get out of designing. It is the design, performed at the smallest scale the change deserves. `brainstorm` requires the tier to be **stated out loud** — its completion criterion is literally "you have said *This is tier N because…*" — and `amend` requires the same classification against the existing spec.

An agent that silently concludes "this is too small for process" has not made the decision. It has skipped it. From `brainstorm`'s rationalization table:

| Thought | Reality |
|---|---|
| "This is a one-liner, designing it is overhead" | Deciding it is tier 0 **is** the design step — say so explicitly and move on. Skipping the decision is the overhead. |
| "The user already told me exactly what to build" | They told you a solution. You have not confirmed the problem, the constraints, or what must keep working. |
| "We talked enough, I basically know the answer" | If it is not in an approved `requirements.md`, it lives only in this chat and dies with it. |

The output of a tier-0 pass can be three sentences. The *process* runs every time.

## Who decides

Two skills own the tier decision, and they cover different ground:

- [`brainstorm`](../skills/brainstorm.md) decides the tier for **new** work — a feature or component nothing has spec'd. Step 5 of its checklist is "Decide the ceremony tier — out loud."
- [`amend`](../skills/amend.md) decides it for a small change to an **already-shipped, spec'd** feature. Step 2 is "Classify the change — out loud," against the existing requirements.

Two other skills feed into the decision rather than making it. [`debug`](../skills/debug.md) exits into the tier-1 mini-spec flow by construction: a fix requirement plus a guard. [`improve-architecture`](../skills/improve-architecture.md) ends by assigning its chosen candidate a tier, and explicitly denies architecture work any exemption — anything tier 1 or above goes to `brainstorm` like everything else.

## Tier 1 in detail: the mini-spec

Tier 1 is where most maintenance work lives, so its shape is worth spelling out. Two requirements get appended to the owning feature's `requirements.md`:

```markdown
- **SHELL-1.4** WHEN the app starts with a persisted module THE SYSTEM SHALL
  activate that module after the store has hydrated.
- **SHELL-1.5** (guard) WHEN the store hydrates THE SYSTEM SHALL CONTINUE TO
  preserve unsaved editor state.
```

The first is the fix. The second is the **guard** — a `SHALL CONTINUE TO` criterion protecting behavior the fix might trample. Guards are what stop an agent from breaking load-bearing behavior nobody thought to mention.

`write-requirements` is explicit that finding nothing to guard is not a valid default. Its completion criterion for that step: *"you have actively searched the touched surface for behaviors to guard — not merely found none by default."*

Then one regression test, tagged with the new ID, and the commit carries the trailers:

```
fix(shell): restore persisted module after store hydration

Implements: SHELL-1.4
Guards: SHELL-1.5
```

If no existing feature owns the behavior, the mini-spec lands in `docs/specs/fixes.md` instead — a shared home the trace check reads for ID definitions like any other requirements file.

## What escalation looks like

The tier is a claim about the work, and claims get falsified. Both `brainstorm` and `amend` are built to escalate mid-flight.

`brainstorm` decomposes when the request spans multiple independent subsystems: it names the sub-features, their relationships, and the build order, then continues with the first one only. Each sub-feature gets its own full spec cycle.

`amend` escalates when the change turns out to be genuinely new scope. Its red flags are precise about what that means:

- You are inventing behavior the spec never described.
- The "small" change grew a design decision with real alternatives.
- You are splitting one request into a trivial part and a new-behavior part — route each half separately.

And the honest test: **does the existing spec's intent already cover this behavior?** If you are inventing what it should do, hand it up.

## What never scales down

The tier controls the *artifacts*. It does not soften the gates.

Tier 0 has no requirements file, no design, no plan. It still goes through `tdd` — a failing test first, at a seam agreed with the user since there is no `design.md` to name one — and it still goes through `verify` before anyone says the word "done".

There is no tier at which an agent may write production code without a failing test, apply a fix without a root cause, or claim completion without fresh evidence. The three-tier system exists so that those four gates stay affordable, not so they can be traded away.

## See also

- [The gates](../concepts/gates.md) — what stays constant across all three tiers
- [`brainstorm`](../skills/brainstorm.md) — decides the tier for new work
- [`amend`](../skills/amend.md) — decides it for changes to shipped features
- [Tier 1 bugfix walkthrough](../examples/tier-1-bugfix.md) — the mini-spec, end to end
