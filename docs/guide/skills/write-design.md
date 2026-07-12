# `write-design`

> HOW the approved requirements get built. Every architecture section names the IDs it satisfies, and a seam table pre-agrees where the tests will live.

|  |  |
|---|---|
| **Bucket** | spec |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | `requirements.md` (the input contract), `templates/design.md`, a scan digest at `.skills/<slug>-scan.md` |
| **Writes** | `docs/specs/<date>-<feature>/design.md`, a scan digest and an independent review under `.skills/` (via subagents) |
| **Calls** | a scan subagent, design-it-twice subagents, an independent review subagent, [`domain-modeling`](domain-modeling.md) (ADR gate), then [`write-plan`](write-plan.md) |
| **Called by** | [`write-requirements`](write-requirements.md) |

## When it fires

After requirements are Approved and before the plan is written. It fires on tier-2 work — tier-1 fixes skip straight from [`write-requirements`](write-requirements.md) to [`tdd`](tdd.md). The requirements file is the input contract, read in full first; the output is the design that spells out how each Approved ID gets satisfied and, critically, where its tests are allowed to be written.

## The four steps

Starting from `templates/design.md`, the skill walks four steps. Two of them lean on dispatched subagents — a scan up front and a review at the end — so the design context stays clear of raw source and free of self-serving framing.

1. **Context and decisions** — what exists today and which constraint shapes the approach, learned through a scan subagent.
2. **Architecture with Satisfies lines** — one section per area, each naming the IDs it exists to meet, designing the hard parts twice.
3. **Seams for testing** — the table that is the contract with [`tdd`](tdd.md).
4. **Coverage self-check, independent review, upstream sync-back, then the approval gate.**

## Context via a scan subagent

To learn "what exists today" without flooding the design context with raw source, the skill dispatches a **scan subagent** to map the touched surface — current signatures, data shapes, save/load paths — and return a digest to `.skills/<slug>-scan.md`. You design against the digest and pull a specific file into context only when a decision hinges on its exact contents. Decisions locked during discovery are recorded as a numbered list. Any decision that is hard to reverse *and* surprising without context *and* a real trade-off also earns an ADR — and [`domain-modeling`](domain-modeling.md) owns that ADR gate. The step is done when a newcomer could state why this approach was chosen over the obvious alternative.

## Satisfies lines and designing it twice

Every `###` architecture section carries a `Satisfies: CODE-N.M, CODE-N.M` line naming the requirement IDs it exists to meet. This is a hard rule with a sharp consequence: a section with no Satisfies line is either infrastructure — and you say so explicitly — or it does not belong in this feature at all. The line is what lets the coverage check and [`trace`](trace.md) prove the design accounts for every requirement.

For the genuinely hard parts, the skill designs it twice. It dispatches two or three parallel subagents with **divergent constraints** — minimize the interface, maximize flexibility, optimize the common caller — compares their results on interface depth and seam placement, and commits to one with a stated reason. The user wants a strong recommendation, not a menu.

The comparison is concrete, not aesthetic. The two axes are **interface depth** — how much complexity the module hides behind how small a surface — and **seam placement** — whether the boundary falls somewhere tests can reach without prying into internals. The winning design is chosen and the reason recorded; the losing designs are discarded, not kept as alternatives.

The governing quality bar is **deep-module discipline**: a module's interface should be much simpler than what it hides. The skill applies the **deletion test** — if this module vanished, how much would callers need to know to rebuild it? If the answer is "everything it did", the interface is shallow and gets redesigned. A shallow module is one whose interface is nearly as complex as its implementation; it adds ceremony without hiding anything, and the deletion test is how you catch one before it ships into the plan.

## The seam table — the contract with `tdd`

Step 3 fills the "Seams for testing" table: the public boundaries tests will be written at, which requirement IDs each seam covers, and the test kind (unit, integration, or e2e). Two rules govern it:

- **Prefer existing seams.** The ideal number of *new* seams is zero or one — every new seam is new surface to maintain.
- **Cover every requirement.** Every requirement ID maps to at least one seam row; an ID with no seam has no place a test can verify it.

This table is a contract, not a suggestion. The [`tdd`](tdd.md) skill refuses to write a test at any seam this table does not list, and [`write-plan`](write-plan.md) must tag a test for every ID in every row or the coverage is dropped. Agreeing the seams here is how the design pre-commits where the testing budget gets spent, so it lands on critical paths instead of on every internal detail.

The step is done when every requirement ID maps to at least one seam row. See [artifacts](../concepts/artifacts.md) for how the seam table threads through the rest of the flow.

## Coverage check, independent review, and upstream sync-back

Step 4 has three parts before the gate.

The **coverage self-check** walks `requirements.md` top to bottom: every ID appears in exactly one Satisfies line, or is listed as deliberately unmapped with a reason. Then it scans for placeholders and internal contradictions — a name used two ways, a data flow that skips a component.

The **independent design review** is dispatched, not self-run. A fresh context has no stake in your framing — it will not fall into the bias that reinterprets a stale requirement rather than catching it. The review subagent gets the design, `requirements.md`, and the repo, and verifies every code-facing claim: each named seam, signature, and data path exists as described, and each Satisfies mapping is actually achievable at that seam. It cites `file:line`, defaults to flagging, and writes to `.skills/<slug>-design-review.md`; you fix the findings without loading the code into the design context.

The **upstream sync-back** is the step the skill insists you never skip.

Designing routinely surfaces a fact that contradicts an *Approved* requirement — a premise that turned out false, a mechanism named wrong, a constraint that does not hold (the requirement says the stored body is ProseMirror-JSON but you discover it is Markdown). When that happens you MUST correct the requirement's own text and re-surface it for approval. You never satisfy a requirement by quietly reinterpreting words you now know are false: a Satisfies line pointing at wrong wording makes the trace spine cite a lie, and the error survives all the way to code. The same holds for an ADR that contradicts an existing one — supersede it explicitly by number. If you changed any requirement, you say exactly which and why when presenting for approval.

Then the file is presented — section by section for large designs — and the skill stops. On approval, `Status` becomes Approved.

## Exit

The skill hands off to [`write-plan`](write-plan.md) as a required sub-skill. The Approved design is the plan's second input contract alongside the requirements: the plan must cover every Satisfies mapping and tag a test for every ID in the seam table, so a design that leaves those two invariants clean is what lets the plan's coverage check pass without renumbering anything.

## The three subagent dispatches

The skill offloads three kinds of work to subagents, each for a specific reason. When no subagents are available, the skill does each pass itself — but the ordering and intent stay the same.

| Dispatch | Step | Why it is offloaded |
|---|---|---|
| Scan | 1 | Maps the touched surface to a digest so raw source never floods the design context |
| Design-it-twice | 2 | Explores divergent constraints in parallel so the chosen interface is compared, not defaulted into |
| Review | 4 | A fresh context has no stake in the framing, so it catches the stale-requirement reinterpretation self-review misses |

## Worked example

Continuing `SHELL` — the left icon rail — from the [`write-requirements`](write-requirements.md) page. A scan subagent reports that the app already has a `moduleStore` with a `hydrate()` path, so the design reuses it rather than inventing new persistence.

```md
## Decisions

1. Reuse the existing `moduleStore` for persistence; do not add a new store.
2. Restore after `hydrate()` resolves, never before — an async boundary.

## Architecture

### Rail and active-module state

Satisfies: SHELL-1.1, SHELL-1.2, SHELL-1.3

The rail renders one icon per registered module. Clicking an icon calls
`moduleStore.setActive(id)`, which updates state and renders the panel.
On boot, `restoreModule()` reads the persisted id after `hydrate()`
resolves; an unknown id falls back to `defaultModuleId`.

## Seams for testing

| Seam | Kind | Covers |
|---|---|---|
| `moduleStore` (setActive / restoreModule) | unit | SHELL-1.1, SHELL-1.2, SHELL-1.3 |
| Rail click → panel render | e2e | SHELL-1.1 |
```

Reading the excerpt against the four steps:

- **Step 1** learned from the scan digest that `moduleStore.hydrate()` already exists, and recorded the decision to reuse it rather than build new persistence.
- **Step 2** put a Satisfies line on the section naming all three IDs; there is no orphan section and no unlabelled one.
- **Step 3** filled the seam table using the *existing* `moduleStore` seam plus one e2e row, so the new-seam count is zero.
- **Step 4** walked the requirements top to bottom, confirmed every ID appears in exactly one Satisfies line and at least one seam row, and dispatched the review subagent to confirm `moduleStore.setActive` and `restoreModule` actually exist as named.

`moduleStore` is an existing seam, so no new seam is introduced. When a later bugfix reveals `restoreModule()` reads the key *before* hydration resolves, that becomes the tier-1 fix `SHELL-1.4` that [`tdd`](tdd.md) tests at this same `moduleStore` seam — the contract set here is what makes that test legal.

## Why it is written the way it is

The design document is the hinge between intent and implementation, and its two load-bearing inventions — the Satisfies line and the seam table — both exist to keep the trace spine honest across that hinge. Satisfies lines make coverage checkable at a glance; the seam table constrains where the testing budget can be spent so `tdd` cannot scatter tests into internals.

The two dispatch patterns — scan first, review last — keep the design context clean of raw source and free of self-serving framing. Design-it-twice sits between them because the hardest interfaces are exactly the ones a single pass tends to shape around the first idea rather than the best one.

And the upstream sync-back exists because the most expensive bug is a wrong requirement that everyone downstream faithfully implements; the moment design proves a premise false is the cheapest moment to fix it. Reinterpreting the words instead — satisfying the letter of a requirement you know is wrong — is the failure the dispatched review is specifically there to catch, since it is the one your own framing will rationalize.

## See also

- [Artifacts](../concepts/artifacts.md) — how the seam table threads into `tdd`
- [`write-requirements`](write-requirements.md) — the input contract this reads
- [`write-plan`](write-plan.md) — the next step, which the design hands off to
- [`domain-modeling`](domain-modeling.md) — owns the ADR gate this skill defers to
