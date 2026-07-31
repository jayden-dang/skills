# `design-solution`

> HOW the approved requirements get built. Every architecture section names the IDs it satisfies, records interface depth and locality, and a seam table pre-agrees where the tests will live.

|  |  |
|---|---|
| **Bucket** | spec |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | `requirements.md` (the input contract), `templates/design.md`, a scan digest at `.skills/<slug>-scan.md` |
| **Writes** | `docs/specs/<date>-<feature>/design.md`, a scan digest and an independent review under `.skills/` (via subagents) |
| **Calls** | a scan subagent, design-it-twice subagents, an independent review subagent, [`define-domain`](define-domain.md) (ADR gate), then [`plan-tasks`](plan-tasks.md) |
| **Called by** | [`specify-behavior`](specify-behavior.md) |

## When it fires

After requirements are Approved and before the plan is written. It fires on tier-2 work — tier-1 fixes skip straight from [`specify-behavior`](specify-behavior.md) to [`test-first`](test-first.md). The requirements file is the input contract, read in full first; the output is the design that spells out how each Approved ID gets satisfied and, critically, where its tests are allowed to be written.

## The four steps

Starting from `templates/design.md`, the skill walks four steps. Two of them lean on dispatched subagents — a scan up front and a review at the end — so the design context stays clear of raw source and free of self-serving framing.

1. **Context and decisions** — what exists today and which constraint shapes the approach, learned through a scan subagent.
2. **Architecture** — one section per module: `Satisfies:`, `Reuse:`, `Interface:`, `Depth:` (deletion test for new modules), `Locality:`; hard parts designed twice.
3. **Seams for testing** — the table that is the contract with [`test-first`](test-first.md).
4. **Coverage + structure self-check, independent review, upstream sync-back, then the approval gate.**

## Context via a scan subagent

To learn "what exists today" without flooding the design context with raw source, the skill dispatches a **scan subagent** to map the touched surface — current signatures, data shapes, save/load paths — and return a digest to `.skills/<slug>-scan.md`. You design against the digest and pull a specific file into context only when a decision hinges on its exact contents. Decisions locked during discovery are recorded as a numbered list. Any decision that is hard to reverse *and* surprising without context *and* a real trade-off also earns an ADR — and [`define-domain`](define-domain.md) owns that ADR gate. The step is done when a newcomer could state why this approach was chosen over the obvious alternative.

## Satisfies, depth, locality, and designing it twice

Every `###` architecture section is a **module** (or named area) with a fixed slot list from `templates/design.md`:

| Slot | Job |
|---|---|
| `Satisfies:` | Trace — which requirement IDs this module exists to meet |
| `Reuse:` | Ladder rung + concrete target (or new code at rung 7) |
| `Interface:` | What callers know — kept smaller than the implementation |
| `Depth:` | Written **deletion test** for new modules; `n/a — extends …` when reusing |
| `Locality:` | Where the change lands; neighbor impact (`leave` / `extend` / `extract`) |

Vocabulary matches [`scan-architecture`](scan-architecture.md): **module, interface, implementation, seam**. Trace coverage and structure quality are separate Done-when axes — every ID can have a Satisfies line and still need a redesign if Depth restates the whole implementation.

For the genuinely hard parts, the skill designs it twice. It dispatches two or three parallel subagents with **divergent constraints** — minimize the interface, maximize flexibility, optimize the common caller — compares on interface depth and seam placement, and commits to one with a stated reason. A strong recommendation, not a menu.

`scan-architecture` still owns **brownfield debt** across an existing codebase (user-invoked, after friction accumulates). `design-solution` owns **feature-local structure** before code — so a greenfield or feature design does not wait for a later debt scan to ask whether modules are deep.

## The seam table — the contract with `test-first`

Step 3 fills the "Seams for testing" table: the public boundaries tests will be written at, which requirement IDs each seam covers, and the test kind (unit, integration, or e2e). Two rules govern it:

- **Prefer existing seams.** The ideal number of *new* seams is zero or one — every new seam is new surface to maintain.
- **Cover every requirement.** Every requirement ID maps to at least one seam row; an ID with no seam has no place a test can prove-claim it.

This table is a contract, not a suggestion. The [`test-first`](test-first.md) skill refuses to write a test at any seam this table does not list, and [`plan-tasks`](plan-tasks.md) must tag a test for every ID in every row or the coverage is dropped. Agreeing the seams here is how the design pre-commits where the testing budget gets spent, so it lands on critical paths instead of on every internal detail.

The step is done when every requirement ID maps to at least one seam row. See [artifacts](../concepts/artifacts.md) for how the seam table threads through the rest of the flow.

## Coverage check, independent review, and upstream sync-back

Step 4 has three parts before the gate.

The **coverage self-check** walks `requirements.md` top to bottom: every ID appears in exactly one Satisfies line, or is listed as deliberately unmapped with a reason. Then it scans for placeholders and internal contradictions — a name used two ways, a data flow that skips a component. **Structure coverage** runs in the same pass: every section has Interface / Depth / Locality filled; rung-7 Depth answers are non-vacuous.

The **independent design review** is dispatched, not self-run. A fresh context has no stake in your framing — it will not fall into the bias that reinterprets a stale requirement rather than catching it. The review subagent gets the design, `requirements.md`, the scan digest when present, and the repo. It verifies **code-facing** claims (seams, signatures, paths, Satisfies achievable at that seam) and **structure** claims (Interface smaller than implementation, Depth non-vacuous, Locality consistent with the digest). It cites `file:line`, defaults to flagging, and writes to `.skills/<slug>-design-review.md`; you fix the findings without loading the code into the design context.

The **upstream sync-back** is the step the skill insists you never skip.

Designing routinely surfaces a fact that contradicts an *Approved* requirement — a premise that turned out false, a mechanism named wrong, a constraint that does not hold (the requirement says the stored body is ProseMirror-JSON but you discover it is Markdown). When that happens you MUST correct the requirement's own text and re-surface it for approval. You never satisfy a requirement by quietly reinterpreting words you now know are false: a Satisfies line pointing at wrong wording makes the trace spine cite a lie, and the error survives all the way to code. The same holds for an ADR that contradicts an existing one — supersede it explicitly by number. If you changed any requirement, you say exactly which and why when presenting for approval.

Then the file is presented — section by section for large designs — and the skill stops. On approval, `Status` becomes Approved.

## Exit

The skill hands off to [`plan-tasks`](plan-tasks.md) as a required sub-skill. The Approved design is the plan's second input contract alongside the requirements: the plan must cover every Satisfies mapping and tag a test for every ID in the seam table, so a design that leaves those two invariants clean is what lets the plan's coverage check pass without renumbering anything.

## The three subagent dispatches

The skill offloads three kinds of work to subagents, each for a specific reason. When no subagents are available, the skill does each pass itself — but the ordering and intent stay the same.

| Dispatch | Step | Why it is offloaded |
|---|---|---|
| Scan | 1 | Maps the touched surface to a digest so raw source never floods the design context |
| Design-it-twice | 2 | Explores divergent constraints in parallel so the chosen interface is compared, not defaulted into |
| Review | 4 | A fresh context has no stake in the framing — catches stale-requirement reinterpretation and vacuous Depth / Locality claims |

## Worked example

Continuing `SHELL` — the left icon rail — from the [`specify-behavior`](specify-behavior.md) page. A scan subagent reports that the app already has a `moduleStore` with a `hydrate()` path, so the design reuses it rather than inventing new persistence.

```md
## Decisions

1. Reuse the existing `moduleStore` for persistence; do not add a new store.
2. Restore after `hydrate()` resolves, never before — an async boundary.

## Architecture

### Rail and active-module state

Satisfies: SHELL-1.1, SHELL-1.2, SHELL-1.3
Reuse: existing — extends moduleStore (rung 2)
Interface: setActive(id), restoreModule() after hydrate; rail only knows active id
Depth: n/a — extends moduleStore
Locality: change lands in rail + moduleStore restore path; neighbors leave

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
- **Step 2** filled Satisfies, Reuse, Interface, Depth, and Locality; reuse path uses Depth `n/a` and Locality leave on neighbors.
- **Step 3** filled the seam table using the *existing* `moduleStore` seam plus one e2e row, so the new-seam count is zero.
- **Step 4** walked coverage and structure slots, then dispatched the review subagent on code-facing and structure claims.

`moduleStore` is an existing seam, so no new seam is introduced. When a later bugfix reveals `restoreModule()` reads the key *before* hydration resolves, that becomes the tier-1 fix `SHELL-1.4` that [`test-first`](test-first.md) tests at this same `moduleStore` seam — the contract set here is what makes that test legal.

## Why it is written the way it is

The design document is the hinge between intent and implementation. **Satisfies** keeps the trace spine honest; **Interface / Depth / Locality** keep structure quality honest at design time; the **seam table** constrains where the testing budget gets spent so `test-first` cannot scatter tests into internals.

The two dispatch patterns — scan first, review last — keep the design context clean of raw source and free of self-serving framing. Design-it-twice sits between them because the hardest interfaces are exactly the ones a single pass tends to shape around the first idea rather than the best one.

And the upstream sync-back exists because the most expensive bug is a wrong requirement that everyone downstream faithfully implements; the moment design proves a premise false is the cheapest moment to fix it. Reinterpreting the words instead — satisfying the letter of a requirement you know is wrong — is the failure the dispatched review is specifically there to catch, since it is the one your own framing will rationalize.

## See also

- [Artifacts](../concepts/artifacts.md) — how the seam table threads into `test-first`
- [`specify-behavior`](specify-behavior.md) — the input contract this reads
- [`plan-tasks`](plan-tasks.md) — the next step, which the design hands off to
- [`define-domain`](define-domain.md) — owns the ADR gate this skill defers to
- [`scan-architecture`](scan-architecture.md) — brownfield structure debt across an existing codebase
