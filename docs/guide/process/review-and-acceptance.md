# Phase 4 — Review and acceptance

**Skills:** [`code-review`](../skills/code-review.md) · [`receive-review`](../skills/receive-review.md) · [`acceptance-check`](../skills/acceptance-check.md) → [`acceptance-api`](../skills/acceptance-api.md) / [`acceptance-ui`](../skills/acceptance-ui.md) · [`dogfood`](../skills/dogfood.md)

**Produces:** a two-axis merge verdict, and committed ID-tagged tests that prove the feature works against the running system.

## Why there are two separate phases here

A change can be **correct code that builds the wrong thing**, or **the right thing built badly**. And it can pass every unit test while being broken for a real user.

Those are three different failures, and the system checks them with three different mechanisms.

## `code-review` — two axes, deliberately unmerged

Two subagents, dispatched **in one message** so they run concurrently and neither pollutes the other's context:

- **Standards** — does the code follow this repo's documented conventions and avoid the baseline smells?
- **Spec** — does the code implement what the requirements asked for, ID by ID?

> The axes are deliberately separate because a change can pass one and fail the other: flawless code that builds the wrong thing (Standards pass, Spec fail), or a faithful implementation that tramples the repo's conventions (Spec pass, Standards fail). Merged reports let one axis mask the other.

At aggregation time this is enforced rather than merely suggested. The reports are presented under separate `## Standards` and `## Spec` headings, lightly cleaned at most. They are **not** merged, deduped across axes, or reranked against each other — *that reranking is exactly what the separation prevents.*

### The steps

**Pin the range — fail fast.** `git rev-parse <base>` must resolve, and `git diff <base>...HEAD` must be non-empty. A bad ref or an empty diff fails **here**, not inside two parallel subagents.

**Locate the spec**, in order: requirement-ID trailers in the commits (`Implements:`, `Guards:`), whose feature code maps to a spec folder via `docs/specs/INDEX.md`; then a `requirements.md` matching the branch or feature name; then a caller-supplied path; then ask. An explicit "no spec exists" means the Spec axis is skipped and the report says so.

**Gather standards sources.** Whatever documents how code here should be written — `CLAUDE.md`, lint and formatter configs, CONTRIBUTING-style docs — plus `CONTEXT.md` for the repo's canonical vocabulary, plus `standards-baseline.md`: twelve smells that apply even in a repo that documents nothing.

Two rules bind the baseline. **A documented repo standard always overrides it**, and **every baseline hit is a labeled judgment call**, never a hard violation. And: skip anything tooling already enforces. A reviewer repeating the linter is noise.

**Check for duplication.** `check-graph --query` against the diff's changed files returns overlapping features and their [summary cards](../concepts/feature-graph.md). When overlaps exist, the Spec subagent additionally receives those cards and is directed to flag — as a **reuse-miss** finding citing the neighbor's feature code — any place the diff reimplements behavior a shares-surface neighbor already owns.

**Dispatch.** Both subagents are **read-only**: no mutation of the working tree, index, HEAD, or branch state. To inspect another revision, use a temporary worktree — never move HEAD. Each brief stays under 400 words. Never pre-judge findings: no "do not flag", no pre-rated severities.

**Aggregate.** Every finding carries severity (Critical / Important / Minor), `file:line`, why it matters, and a suggested fix unless obvious. Then the verdict:

```
Ready to merge? Yes | No | With fixes
[1–2 sentences of technical reasoning]
```

## `receive-review` — the anti-sycophancy skill

Review feedback is a set of **technical claims to evaluate**, not orders to follow and not kindness to repay. Being correct matters more than being agreeable.

The sequence is strict, and step 2 is the one people violate:

1. **READ** every item to the end before reacting to any.
2. **UNDERSTAND** — restate each item in your own words. Any item you cannot restate is unclear: ask about **all** unclear items now, before implementing **any** item. *Items interact; partial understanding produces confidently wrong implementations.*
3. **VERIFY** each claim against the actual codebase. The reviewer says the function ignores errors? Open the function.
4. **EVALUATE** — is the suggestion right for *this* codebase? When a reviewer says "implement this properly", grep for real usage first. If nothing calls it, the correct fix is **removal**, and you propose that instead.
5. **RESPOND** with technical reasoning. Agreement cites evidence; pushback cites specifics.
6. **IMPLEMENT** one item at a time — blocking items, then simple corrections, then complex changes — each through `tdd`.

Forbidden, verbatim: *"You're absolutely right"*, *"Great point"*, *"Good catch, thanks"*, *"Thanks for"* anything. State the fix, not the feelings:

> "Fixed — `parseRange` now rejects reversed bounds (parser.ts:88)."

**The diff is the acknowledgment.**

Source calibration matters: the user is trusted (verify scope, then act). Reviewer subagents produce claims like any other. External reviewers get extra skepticism *because they lack full context* — but **check before dismissing**. Skepticism is verification, not a reflex "no".

## Acceptance — the gap green tests do not close

> Green unit tests prove that the assertions someone wrote pass. They do not prove the feature works.

The gap is concrete: an API that returns `201` where the client reads `200`. A checkbox that flips in memory but never reaches the store. A form that clears on a failed submit. This is where features ship broken.

`acceptance-check` runs **after `code-review`, before `finish-branch`**.

### 1. Derive the checklist from the spec

Read `requirements.md`, `design.md`, and `tasks.md`. For every requirement describing user-observable behavior, list its concrete checks — the happy path **and** each edge/error criterion — keyed to the requirement ID.

The spec is the source: *a behavior nobody hand-fed you is still on the hook, and an untraced one is a gap to raise, not to skip.* The checklist becomes `.skills/<slug>-acceptance.md`, a git-ignored working ledger, plus one todo per item.

### 2. Dispatch by surface

| Surface | Skill |
|---|---|
| An HTTP/RPC API a client calls | `acceptance-api` |
| A frontend a user drives | `acceptance-ui` |
| Neither — a CLI, a library, a batch job | drive it directly, record results, promote to ID-tagged tests |
| Human-eyeball qualities (visuals, feel) | `dogfood` |

Most features need both of the first two. Each child gets its slice of the ledger **by path** and writes results back to the same file.

**`acceptance-api`** starts the server — and if `docs/agents/project.md` has no `## Run locally (dev)` entry, it discovers the command, confirms the server answers, and *writes the command back into project.md* so the next run is cheap. Then each checklist item becomes a real request, and the assertion is the **full expectation**: status, body shape (names, casing, id type), and — where the criterion says "persists" — a fresh `GET` reading it back; where it says "across restart", a restart and another read.

**`acceptance-ui`** does the same for the frontend, ensuring a Playwright/Chromium harness exists (setting one up if not — done when the Playwright command runs against Chromium *even with zero specs*). Each flow becomes a spec that acts as a user: locate by role or label, type and click, and assert on **visible outcomes** — text on screen, the input cleared, list order, an error shown. Where the criterion says "persists", `page.reload()` and assert the state survives.

Both fix what breaks through `debug` — *the failing request or the failing spec is already your red-capable loop* — and both **promote the passing checks into committed, ID-tagged tests**, so they join the verify suite and guard the behavior forever after.

### 3. Close the loop

Report the checklist with each item's observed result. **Any item you could not exercise is an open risk — name it.** Do not let it pass silently.

## `dogfood` — the manual sibling

For the judgment an automated test cannot make: visuals, feel, and the edge cases a human must eyeball.

The deliverable is not a chat message. It is a **persistent, checkable HTML artifact** — one row per user-facing ability, each tagged with its requirement ID, each row a copy-pasteable **Try** and an **Expect** shown in the app's *real rendering* (badge colors, chip styles, icons pulled from theme tokens and CSS, never guessed). Interactive checkboxes persist to localStorage with a progress counter, so the user closes the page and resumes.

It scopes the happy path, the edge cases, **and the deliberate non-behaviors** — what should *not* happen, taken from the spec's Out-of-Scope decisions. And a behavior with no UI surface still gets a case, with a real way to observe it (a devtools `invoke(...)`, a read-only DB peek), never a pretend screen.

> "A markdown checklist in chat is enough" → It saves no tick, cannot show the real badge being checked against, and scrolls away.

## Next

→ [Phase 5 — Ship and maintain](ship-and-maintain.md)

## See also

- [Traceability](../concepts/traceability.md) — what "covered" means, and what it does not prove
- [`code-review`](../skills/code-review.md) — the twelve baseline smells
- [`acceptance-check`](../skills/acceptance-check.md) — the orchestrator
- [The feature graph](../concepts/feature-graph.md) — the reuse-miss check
