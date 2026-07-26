---
name: drive-dogfood
description: >-
  Use when a dogfood test guide already exists and its cases must be executed
  rather than handed to a human — the agent-driven pass over every case in the
  guide against the running app in a real browser, judging both what the screen
  shows and what the backend actually stored. Produces an evidence-backed run
  ledger carrying a pass / fail / blocked verdict per case ID, and a guide left
  fully accounted for. Triggers on running or resuming a half-finished test
  guide, working a dogfood file end to end, or testing every case in the browser
  and fixing what breaks. Not for authoring the guide (`dogfood`) or writing
  committed e2e specs (`acceptance-ui`).
---

# Drive Dogfood

Execute an existing dogfood guide in a real browser. The deliverable is the
**run ledger** — every case ID accounted for with quoted screen evidence and,
when the case touches server-owned state, a server-side probe that actually ran.
A chat summary is not the deliverable.

## The Iron Law

```
NO CASE IS TICKED ON THE SCREEN ALONE
```

If the case's Expect (or `data-backend`) touches state the server owns, the
ledger row carries **both** `saw` (quoted UI) **and** `server` (probe command +
result) before `verdict: pass`. Pure presentation (layout, color, copy, empty
state with no write) records `server: none — presentational`.

"Dogfood judges product behavior on screen, not wire traffic" is false for any
case that claims create, update, delete, or persistence. The screen is necessary;
it is not sufficient.

Probe ladder (strongest first): the request/response the UI just made → read-back
through the app's own API → store peek (DB / file / cache) → reload or restart
for durability. A red console error or 5xx on the wire fails the case even when
the screen looks right. Do not invent probe results you did not run.

## 1. Preconditions — origin and app

Confirm the target origin **before the first guide click**:

- Default: local dev from `docs/agents/project.md` (`## Run locally (dev)`).
  Start the app if it is down.
- Non-local origin (staging, production, shared QA): **stop**. Ask for an
  explicit yes in this thread naming that origin. "Whatever is fastest", a demo
  deadline, or an already-open tab is **not** consent.
- Drive a dedicated tab. Do not hijack a tab the user is working in.
- Avoid controls that raise native `alert` / `confirm` (they freeze many browser
  bridges); warn the user first if a case requires one.

*Done when: origin is local, or non-local consent is on the record, and the app
loads.*

## 2. Build the ledger before any drive

Read the guide file (HTML path from `dogfood`, or the path the user gave). Parse
every case. Prefer `data-case`, `data-req`, `data-backend`, `data-setup` when
present; fall back to visible Try / Expect / requirement text when attributes
are missing (older guides).

Write `.skills/<slug>-dogfood-run.md` with **one row per case before driving any
case**. Create one todo per case. Resume: if the ledger exists, trust it — first
non-`pass` row is next; do not re-derive progress from memory.

| field | content |
|---|---|
| `case` | stable id (`data-case` or stable title) |
| `req` | requirement ID |
| `verdict` | `pending` \| `pass` \| `fail` \| `blocked` |
| `saw` | what was on screen — **quoted**, not paraphrased |
| `server` | probe + result, or `none — presentational` |
| `notes` | setup used, fix / `debug` hand-off, re-drive |

**No row, not run.** Skipping a case because it is "the same CRUD pattern",
because a lead said spot-check is fine, or to "save time for the demo" leaves
that row `pending` or `blocked` — never silent `pass`. A partial run reports
exactly which rows are unfinished.

*Done when: every case in the guide has a ledger row and a todo, all `pending`
(or restored from a prior ledger).*

## 3. Drive each pending case

In ledger order, for each non-`pass` row:

1. Apply `data-setup` (or the setup implied by Try) so the case can run
   independently.
2. Execute Try in the browser (Chrome extension tools when present; else headed
   Chromium/Playwright). Do not hard-depend on a package-external browser skill.
3. Fill `saw` from what is actually visible.
4. Run the backend probe when required by the Iron Law / `data-backend`; fill
   `server`.
5. Set `verdict`: `pass` only when Expect holds **and** evidence slots are full;
   else `fail`. Mark the todo done only on `pass`.

*Done when: the row is `pass`, or routed through §4.*

## 4. Failure routing

Re-drive the failed case once from a clean setup, then classify by observation:

| Observation | Action |
|---|---|
| Deterministic fail on a real Expect / backend assertion | Product defect. **REQUIRED SUB-SKILL: use `debug`.** Hand a red-capable loop (repro steps, request/response, console), not only a click path. |
| Flaky, or guide wrong (stale label, missing seed, bad Expect) | Fix the **guide** (or note the guide defect); re-drive. Do not send guide bugs to `debug`. |
| Shared precondition broken (login, server down, seed missing) | Stop the run. Leave remaining rows `pending`/`blocked`. Downstream is untested, not passing. |

After `debug` reports fixed: restart the app if needed, re-drive the failed case
from a clean setup, **and** re-drive every already-`pass` case whose `req`
appears in the fix's changed files (grep the diff for requirement IDs or the
modules those cases exercise).

**Caps (D2):** 3 distinct fix attempts on the same case → stop and escalate.
5 product-defect fix cycles in the whole run → stop with a partial ledger.
Do not mark untested cases `pass` to clear the board.

Durable asset for a product fix: the regression test `debug` already requires
under TDD — not a silent promotion of the whole guide into Playwright
(`acceptance-ui` is that path, only if the user asks).

## 5. Close the run

When every row is `pass`, or the run stops on a cap / precondition / escalate:

1. Ledger is authoritative (D1). Guide HTML checkboxes are optional niceties only.
2. Write an end-of-run report next to the guide path (or under `.skills/`) with
   each case's verdict + `saw` + `server`.
3. Hand the user: path to ledger, path to report, any `blocked`/`pending` rows
   and why.

*Done when: every case ID is accounted for in the ledger and the report matches
the ledger — no bare "all good."*

## Rationalizations

| Thought | Reality |
|---|---|
| "Dogfood judges the screen, not wire traffic" | State cases require a server probe. Screen-only is not a pass. |
| "Same CRUD pattern — spot-check is enough" | No row, not run. Every case gets its own evidence. |
| "User said whatever is fastest / demo in N minutes" | Speed is not consent for staging/prod. Ask, or run local. |
| "Happy paths on staging; skip edges to make the demo" | Partial run: unfinished rows stay pending/blocked, never pass. |
| "I'll tick pass and fill server evidence later" | Evidence slots are full before `pass`, or the verdict stays fail/pending. |
| "The other cases already passed before the fix" | Re-drive every already-pass case whose req the fix touched. |

## Red Flags

- Marking `pass` with `server` empty on a create/update/delete/persist case
- Spot-checking a subset while claiming the guide is done
- Driving a non-local origin without an explicit yes naming that origin
- Patching product on a dogfood fail without `debug` when the fail is deterministic
- Claiming completion from memory after compaction instead of reading the ledger
