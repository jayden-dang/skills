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

Execute an existing dogfood guide against the **product app** in a real browser.
The deliverable is the **run ledger** — every case ID accounted for with quoted
screen evidence and, when the case touches server-owned state, a server-side
probe that actually ran. A chat summary is not the deliverable.

## The Iron Law

```
NO CASE IS TICKED ON THE SCREEN ALONE
PROGRESS LIVES IN THE LEDGER — NEVER IN GUIDE localStorage
```

If the case's Expect (or `backend`) touches state the server owns, the ledger
row carries **both** `saw` (quoted UI) **and** `server` (probe command + result)
before `verdict: pass`. Pure presentation records
`server: none — presentational`.

"Dogfood judges product behavior on screen, not wire traffic" is false for any
case that claims create, update, delete, or persistence. The screen is necessary;
it is not sufficient.

Ticking checkboxes on the dogfood HTML guide (localStorage) is a **human nicety
only**. Agents **must not** open the guide in Chrome (or any browser) to mark
progress — that burns tokens and is never authoritative. Use the CLI ledger.

Probe ladder (strongest first): the request/response the UI just made → read-back
through the app's own API → store peek (DB / file / cache) → reload or restart
for durability. A red console error or 5xx on the wire fails the case even when
the screen looks right. Do not invent probe results you did not run.

## CLI (required for progress)

Resolve the dogfood skill root (this monorepo:
`skills/acceptance/dogfood`; when installed, the skill package path). Then:

```bash
DF=python3 <skill-root>/scripts/dogfood
# prefer cases YAML; HTML with data-* / embedded shell JSON also works
$DF list   .skills/<slug>-dogfood.cases.yaml
$DF show   .skills/<slug>-dogfood.cases.yaml CASE-1
$DF init   .skills/<slug>-dogfood.cases.yaml -o .skills/<slug>-dogfood-run.md
$DF next   .skills/<slug>-dogfood-run.md
$DF mark   .skills/<slug>-dogfood-run.md CASE-1 pass \
  --saw '…quoted UI…' --server '…probe…' \
  --catalog .skills/<slug>-dogfood.cases.yaml
$DF status .skills/<slug>-dogfood-run.md
$DF report .skills/<slug>-dogfood-run.md -o .skills/<slug>-dogfood-report.md
```

`mark pass` refuses empty `--saw` / `--server`. Presentational cases require
`--server 'none — presentational'`.

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

## 2. Build the ledger before any drive

Catalog path: cases YAML from `dogfood`, or the HTML path the user gave (CLI
reads both).

```bash
$DF init <catalog> -o .skills/<slug>-dogfood-run.md
```

If a ledger already exists, **trust it** — do not re-init without `--force`.
Create one todo per case. Resume: `$DF next` (first non-`pass`).

| field | content |
|---|---|
| `case` | stable id |
| `req` | requirement ID |
| `kind` | taxonomy kind |
| `verdict` | `pending` \| `pass` \| `fail` \| `blocked` |
| `saw` | what was on screen — **quoted**, not paraphrased |
| `server` | probe + result, or `none — presentational` |
| `notes` | setup used, fix / `debug` hand-off, re-drive |

**No row, not run.** Skipping a case because it is "the same CRUD pattern",
"only happy paths for the demo", because a lead said spot-check is fine, or to
"save time" leaves that row `pending` or `blocked` — never silent `pass`.

*Done when: every case has a ledger row and a todo, all `pending` (or restored).*

## 3. Drive each pending case

In ledger order (`$DF next` until empty):

1. `$DF show <catalog> <CASE-ID>` — load Try / Expect / setup / backend.
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
| Flaky, or guide wrong (stale label, missing seed, bad Expect) | Fix the **cases YAML** (re-`render` HTML if needed); re-drive. Do not send guide bugs to `debug`. |
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

1. Ledger is authoritative. Guide HTML checkboxes are never required.
2. `$DF report <run.md> -o .skills/<slug>-dogfood-report.md`
3. Hand the user: path to ledger, path to report, any `blocked`/`pending` rows
   and why.

*Done when: every case ID is accounted for in the ledger and the report matches
the ledger — no bare "all good."*

## Rationalizations

| Thought | Reality |
|---|---|
| "Dogfood judges the screen, not wire traffic" | State cases require a server probe. Screen-only is not a pass. |
| "Tick the guide so localStorage is the source of truth" | Ledger + `dogfood mark` is the only agent progress path. Guide ticks are human-only. |
| "I'll dual-write guide ticks and the ledger" | Dual-write is waste. Ledger only. |
| "Same CRUD pattern — spot-check is enough" | No row, not run. Every case gets its own evidence. |
| "User said whatever is fastest / demo in N minutes" | Speed is not consent for staging/prod. Ask, or run local. |
| "Happy paths on staging; skip edges to make the demo" | Partial run: unfinished rows stay pending/blocked, never pass. |
| "I'll tick pass and fill server evidence later" | Evidence slots are full before `pass`, or the verdict stays fail/pending. |
| "The other cases already passed before the fix" | Re-drive every already-pass case whose req the fix touched. |

## Red Flags

- Opening the dogfood HTML in a browser to tick checkboxes during the run
- Marking `pass` with `server` empty on a create/update/delete/persist case
- Spot-checking a subset while claiming the guide is done
- Driving a non-local origin without an explicit yes naming that origin
- Patching product on a dogfood fail without `debug` when the fail is deterministic
- Claiming completion from memory after compaction instead of reading the ledger
