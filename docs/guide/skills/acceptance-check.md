# `acceptance-check`

> Green unit tests prove the assertions someone wrote pass. They do not prove the feature works. This skill drives the running system through every spec'd behavior and closes that gap.

|  |  |
|---|---|
| **Bucket** | acceptance |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | the spec triad — `requirements.md`, `design.md`, `tasks.md`; the working ledger `.skills/<feature>-acceptance.md` |
| **Writes** | `.skills/<feature>-acceptance.md` (a git-ignored acceptance ledger, one todo per item); committed ID-tagged tests for non-API/non-UI surfaces |
| **Calls** | [`acceptance-api`](acceptance-api.md), [`acceptance-ui`](acceptance-ui.md), [`dogfood`](dogfood.md), [`debug`](debug.md) (through its children) |
| **Called by** | [`execute-plan`](execute-plan.md), [`finish-branch`](finish-branch.md), [`verify`](verify.md) |

## When it fires

Before merging or finishing a branch, when a feature's unit tests are green but its user-facing behavior has not been driven through the running system as a real client. It also fires when the repo has no documented way to run the app locally, because you cannot accept behavior you cannot boot.

Its place in the chain is fixed: it runs **after [`code-review`](code-review.md), before [`finish-branch`](finish-branch.md)**. Code review judges the diff; acceptance judges the running feature. The gap it exists to catch is the one a green suite hides:

- an API that returns `201` where the client reads `200`,
- a checkbox that flips in memory but never reaches the store,
- a form that clears on a failed submit.

Each of those passes every assertion someone wrote and still ships broken. The unit tests are green because they assert what the code does; none of them drove the feature as a real client, which is the only thing that surfaces the mismatch.

This is an orchestrator. It does little validation itself; it derives the work, splits it by surface, hands each slice to a child skill, and closes the loop. What sets it apart from a manual [`dogfood`](dogfood.md) pass is what it leaves behind: committed, ID-tagged tests, not a one-time walkthrough.

## The three steps

The skill is three steps and no more — derive, dispatch, close. Each ends on an explicit *done-when* condition, and the skill will not advance past one until that condition is met.

The pattern is the same one the whole set uses at its gates: name the observable outcome that ends the step, then refuse to call the step finished on anything weaker. Here the weakest tempting shortcut is "the tests are green, so the feature is accepted" — which is exactly the claim these three steps replace with driven-and-observed evidence.

## 1. Derive the acceptance checklist from the spec

Read the feature's `requirements.md`, `design.md`, and `tasks.md`. For every requirement describing user-observable behavior, list its concrete checks — the happy path AND each edge or error criterion — keyed to the requirement ID.

The spec is the source, and that has two teeth. A behavior nobody hand-fed you is still on the hook: if the requirements describe it, it belongs on the checklist whether or not anyone mentioned it. And an untraced behavior — one in the running system that no requirement covers — is a gap to **raise**, not to skip.

Write the checklist to `.skills/<feature>-acceptance.md`, a git-ignored working ledger, and create one todo per item. When the reading is heavy, dispatch a scan subagent to map the touched surface and digest it into the ledger so this context stays lean. The step is done when every user-facing requirement ID has at least one concrete, observable check with an expected result.

The ledger is the spine of the whole run. It is git-ignored because it is scaffolding, not a deliverable — the deliverables are the tests the children commit. But while the run is live it is the single shared record: the orchestrator writes the checklist into it, each child writes its observed results back into it by path, and the closing report reads out of it.

## 2. Dispatch by surface

The checklist splits by where each behavior lives, and most features need more than one child — a create-note feature has both an endpoint and a form, so its items fan out to two children at once. Run whichever surfaces apply:

| Surface | Handler |
|---|---|
| HTTP/RPC API a client calls | **required sub-skill** [`acceptance-api`](acceptance-api.md) |
| A frontend a user drives | **required sub-skill** [`acceptance-ui`](acceptance-ui.md) |
| Neither — a CLI, a library, a batch/cron job | drive it directly against the running system yourself, record each observed result in the ledger, and promote the passing checks into committed, ID-tagged tests |
| Human-eyeball qualities — visuals, feel | hand off to [`dogfood`](dogfood.md) |

Each child locates and persists how to run its surface, exercises its slice of the checklist against the live system, fixes failures through [`debug`](debug.md), and promotes the passing checks into committed, ID-tagged tests. Hand each child its slice of the ledger **by path** — it writes its results back into the same file, so the ledger stays the single record of what was observed.

## 3. Close the loop

The orchestrator's own job at this point is bookkeeping, not driving: the children have already exercised their slices and written results into the ledger. Report the checklist with each item's observed result, then hand back to [`finish-branch`](finish-branch.md). Any item you could not exercise is an **open risk** — name it explicitly; do not let it pass silently. Silent gaps are exactly how the untested edge case reaches the user.

The step — and the skill — is done when every checklist item is observed green against the running system, each failure is fixed with a regression test, and the durable tests are committed and tagged so `finish-branch`'s verify gate keeps enforcing them.

The distinction between the two exit states is the whole discipline. "Observed green" means the behavior was driven through the running system and watched. "Open risk" means it was not, and says so out loud. There is no third state — no item quietly assumed to work because its unit test passes.

## Worked example

A note-taking app is adding a create-note feature under code `NOTE`. Two requirements describe user-observable behavior:

- `NOTE-1.1` — a submitted note appears in the list and persists across a reload.
- `NOTE-1.2` — an empty note is rejected with a visible error, and the input is not cleared.

The unit suite is green and `code-review` has passed, so acceptance is the next gate.

Deriving the checklist writes `.skills/note-acceptance.md`:

```markdown
- [ ] NOTE-1.1 (api) POST /notes with a body creates the note; GET /notes reads it back after reload
- [ ] NOTE-1.1 (ui) typing a note and clicking Add shows it in the list; survives page.reload()
- [ ] NOTE-1.2 (api) POST /notes with an empty body returns 422, not 201
- [ ] NOTE-1.2 (ui) submitting empty shows an error and leaves the typed text in the input
```

The API rows dispatch to [`acceptance-api`](acceptance-api.md); the UI rows to [`acceptance-ui`](acceptance-ui.md). Both receive `.skills/note-acceptance.md` by path and write their observed results back. Suppose `acceptance-api` finds `NOTE-1.2` returns `201` with a blank title instead of `422` — a real defect the unit tests missed because they asserted the handler's return value, not the wire status. It fixes the root cause through `debug`, leaves a committed `@NOTE-1.2` regression test, and marks the ledger row green.

Closing the loop reports the ledger back with each observed result:

```
NOTE acceptance — 4/4 observed green
  NOTE-1.1 (api)  green — POST 201, GET reads it back after restart
  NOTE-1.1 (ui)   green — note visible, survives reload
  NOTE-1.2 (api)  green — now 422 (was 201, fixed via debug; @NOTE-1.2 committed)
  NOTE-1.2 (ui)   green — error shown, input retained
Open risks: none
```

Had the browser refused to boot, that UI row would appear under **Open risks** by name — "NOTE-1.1 (ui): could not launch Chromium against the dev server" — rather than being quietly checked off. Only then does it hand back to [`finish-branch`](finish-branch.md).

## Why it is written the way it is

`acceptance-check` is a **coordination skill**, and its structure follows from the failure it was written against: an agent that reports "tests pass, done" when the feature has never once been driven through the running system. The three steps map onto that failure directly. Deriving the checklist from the spec — not from what was mentioned in chat — blocks the agent from accepting only the behaviors it happened to think of. Dispatching by surface routes each behavior to a child that can actually exercise it live, rather than reasoning about it. And the closing loop forces every item to end in one of two states, observed-green or named-risk, so nothing exits in the ambiguous middle where broken features hide.

The git-ignored ledger is the connective tissue: it lets a fan-out of children share one record without polluting the committed tree, and it is what makes the final report a single honest accounting rather than a scatter of subagent messages.

It is also why the skill is an orchestrator rather than a monolith. API validation, browser validation, and human-eyeball judgment are genuinely different disciplines with different tools — `curl` and a fresh `GET`, a Playwright session on Chromium, a hand-checked artifact. Rather than fold all three into one skill, `acceptance-check` keeps its own job small — decide what to check and where each check lives — and delegates the exercising to a child built for that surface. The orchestrator owns the accounting; the children own the driving.

## See also

- [The gates](../concepts/gates.md) — where acceptance sits relative to the verify and trace gates
- [`acceptance-api`](acceptance-api.md) and [`acceptance-ui`](acceptance-ui.md) — the two automated children
- [`dogfood`](dogfood.md) — the manual child, for judgment a test cannot make
- [`finish-branch`](finish-branch.md) — the skill that runs it before offering Merge or PR
