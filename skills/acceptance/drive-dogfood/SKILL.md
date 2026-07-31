---
name: drive-dogfood
description: >-
  Use when a dogfood test guide already exists and its cases must be executed
  rather than handed to a human — the agent-driven pass over every case in the
  guide against the running app in a real browser, judging both what the screen
  shows and what the backend actually stored. Produces an evidence-backed run
  file carrying a pass / fail / blocked verdict per case ID, and a guide left
  fully accounted for. Triggers on running or resuming a half-finished test
  guide, working a dogfood file end to end, or testing every case in the browser
  and fixing what breaks. Not for authoring the guide (`dogfood`) or writing
  committed e2e specs (`acceptance-ui`).
---

# Drive Dogfood

Execute an existing dogfood guide against the **product app** in a real browser.
The deliverable is the **run file** — every case ID accounted for with quoted
screen evidence and, when the case touches server-owned state, a server-side
probe that actually ran. A chat summary is not the deliverable.

## The Iron Law

```
NO CASE IS TICKED ON THE SCREEN ALONE
A HUMAN TICK IS RECORDED, NEVER A VERDICT
```

If the case's Expect (or `backend`) touches state the server owns, the case's
`run` block carries **both** `saw` (quoted UI) **and** `server` (probe command +
result) before `verdict: pass`. Pure presentation records
`server: none — presentational`.

"Dogfood judges product behavior on screen, not wire traffic" is false for any
case that claims create, update, delete, or persistence. The screen is necessary;
it is not sufficient.

A person's tick in the guide lands in that case's `human` block, which the agent
can read and must never promote: it says someone looked, not that the thing
works. Agents **must not** open the guide in Chrome (or any browser) to mark
progress — that burns tokens and writes to the wrong field space. Use `dogfood
mark`.

Probe ladder (strongest first): the request/response the UI just made → read-back
through the app's own API → store peek (DB / file / cache) → reload or restart
for durability. A red console error or 5xx on the wire fails the case even when
the screen looks right. Do not invent probe results you did not run.

## CLI (required for progress)

Resolve the dogfood skill root (this monorepo:
`skills/acceptance/dogfood`; when installed, the skill package path). Every
subcommand takes the **one** run file — cases and verdicts live in it together:

```bash
DF="python3 <skill-root>/scripts/dogfood"
RUN=.skills/<slug>-dogfood.json

$DF list   $RUN
$DF show   $RUN CASE-1
$DF init   $RUN                       # seed pending in place
$DF next   $RUN                       # first case still to prove
$DF mark   $RUN CASE-1 pass --saw '…quoted UI…' --server '…probe…'
$DF status $RUN
$DF report $RUN -o .skills/<slug>-dogfood-report.md
```

`mark pass` refuses empty `--saw` / `--server`. Presentational cases require
`--server 'none — presentational'`, and a case with a real `backend` is refused
that string — the rules cannot be skipped, because `backend` now travels in the
same file as the verdict.

**Optional live guide.** `$DF serve $RUN` binds `127.0.0.1:8787` and serves a
page that follows the run and accepts the person's ticks. It is optional by
construction: `render` bakes current verdicts into the HTML, so a guide opened
by double-click is correct with nothing running. Do not drive the guide; it is
for the human beside you.

## 1. Preconditions — origin and app

Confirm the target origin **before the first product click**:

- Default: local dev from `docs/agents/project.md` (`## Run locally (dev)`).
  Start the app if it is down.
- Non-local origin (staging, production, shared QA): **stop**. Ask for an
  explicit yes in this thread naming that origin. "Whatever is fastest", a demo
  deadline, or an already-open tab is **not** consent.
- Drive a **dedicated product tab**. Do not hijack a tab the user is working in.
- Do **not** open the dogfood guide HTML as a drive target.
- Avoid controls that raise native `alert` / `confirm` (they freeze many browser
  bridges); warn the user first if a case requires one.

*Done when: origin is local, or non-local consent is on the record, and the app
loads.*

## 2. Seed the run file before any drive

The run file is the one `dogfood` wrote: `.skills/<slug>-dogfood.json`.

```bash
$DF init $RUN
```

If it already holds verdicts, **trust them** — `init` refuses to reset without
`--force`, and that refusal is the resume path, not an obstacle. Create one todo
per case. Resume: `$DF next` (first non-`pass`).

Each case's `run` block:

| field | content |
|---|---|
| `verdict` | `pending` \| `pass` \| `fail` \| `blocked` |
| `saw` | what was on screen — **quoted**, not paraphrased |
| `server` | probe + result, or `none — presentational` |
| `notes` | setup used, fix / `debug` hand-off, re-drive |

Beside it sits `human` — `checked`, `at`, `comment` — written only by a person
through the served guide. Read it as a signal about where to look. Never copy it
into `verdict`, and never let it stand in for evidence you did not gather.

**No case, not run.** Skipping a case because it is "the same CRUD pattern",
"only happy paths for the demo", because a lead said spot-check is fine, or to
"save time" leaves it `pending` or `blocked` — never silent `pass`.

*Done when: every case has run state and a todo, all `pending` (or restored).*

## 3. Drive each pending case

In file order (`$DF next` until empty):

1. `$DF show $RUN <CASE-ID>` — load Try / Expect / setup / backend.
2. Apply setup so the case can run independently.
3. Execute Try against the **product app** only (Chrome extension tools when
   present; else headed Chromium/Playwright). Do not hard-depend on a
   package-external browser skill. Do **not** open the guide HTML to tick boxes.
4. Fill `saw` from what is actually visible on the product.
5. Run the backend probe when required; fill `server`.
6. `$DF mark … pass|fail|blocked --saw … --server …` only when evidence slots
   match the Iron Law. Mark the todo done only on `pass`.

*Done when: the row is `pass`, or routed through §4.*

## 4. Failure routing

Re-drive the failed case once from a clean setup, then classify by observation:

| Observation | Action |
|---|---|
| Deterministic fail on a real Expect / backend assertion | Product defect. **REQUIRED SUB-SKILL: use `debug`.** Hand a red-capable loop (repro steps, request/response, console), not only a click path. |
| Flaky, or guide wrong (stale label, missing seed, bad Expect) | Fix the case's authored slots in the **run file** (re-`render` the HTML if the human has it open); re-drive. Do not send guide bugs to `debug`. |
| Shared precondition broken (login, server down, seed missing) | Stop the run. Leave remaining cases `pending`/`blocked`. Downstream is untested, not passing. |

After `debug` reports fixed: restart the app if needed, re-drive the failed case
from a clean setup, **and** re-drive every already-`pass` case whose `req`
appears in the fix's changed files (grep the diff for requirement IDs or the
modules those cases exercise).

**Caps (D2):** 3 distinct fix attempts on the same case → stop and escalate.
5 product-defect fix cycles in the whole run → stop with a partial run file.
Do not mark untested cases `pass` to clear the board.

Durable asset for a product fix: the regression test `debug` already requires
under TDD — not a silent promotion of the whole guide into Playwright
(`acceptance-ui` is that path, only if the user asks).

## 5. Close the run

When every case is `pass`, or the run stops on a cap / precondition / escalate:

1. The run file is authoritative. A person's ticks are never required, and never
   substitute for a verdict you did not earn.
2. `$DF report $RUN -o .skills/<slug>-dogfood-report.md`
3. **If you started `$DF serve`, ask the user whether to stop it.** Do not stop
   it silently — they may still be reading the guide — and do not walk away
   leaving a process holding a port. On yes: `$DF serve $RUN --stop`. On no:
   hand them that exact command.
4. Hand the user: path to the run file, path to the report, any
   `blocked`/`pending` cases and why.

*Done when: every case ID is accounted for in the run file, the report matches
it, and any server this run started has been stopped or explicitly left up at
the user's word — no bare "all good."*

## Rationalizations

| Thought | Reality |
|---|---|
| "Dogfood judges the screen, not wire traffic" | State cases require a server probe. Screen-only is not a pass. |
| "The human ticked it, so the case is done" | A tick says someone looked. `pass` needs `saw` and `server`. The two never merge. |
| "I'll tick the guide too so the human sees progress" | `mark` already writes the file the guide reads. Opening a browser to tick is waste and writes to the wrong field space. |
| "Same CRUD pattern — spot-check is enough" | No case, not run. Every case gets its own evidence. |
| "User said whatever is fastest / demo in N minutes" | Speed is not consent for staging/prod. Ask, or run local. |
| "Happy paths on staging; skip edges to make the demo" | Partial run: unfinished rows stay pending/blocked, never pass. |
| "I'll tick pass and fill server evidence later" | Evidence slots are full before `pass`, or the verdict stays fail/pending. |
| "The other cases already passed before the fix" | Re-drive every already-pass case whose req the fix touched. |

## Red Flags

- Opening the dogfood HTML in a browser to tick checkboxes during the run
- Copying a `human` tick into `verdict`, or citing one as evidence
- Ending a run without asking about a server this run started
- Marking `pass` with `server` empty on a create/update/delete/persist case
- Spot-checking a subset while claiming the guide is done
- Driving a non-local origin without an explicit yes naming that origin
- Patching product on a dogfood fail without `debug` when the fail is deterministic
- Claiming completion from memory after compaction instead of reading the run file
