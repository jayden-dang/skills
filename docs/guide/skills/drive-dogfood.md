# `drive-dogfood`

> Execute an existing dogfood guide in a real browser. The deliverable is an evidence-backed run ledger — every case ID accounted for with quoted screen evidence and, when the case touches server-owned state, a server-side probe that actually ran.

|  |  |
|---|---|
| **Bucket** | acceptance |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | a dogfood HTML guide on disk (path from `dogfood` or the user); `docs/agents/project.md` (`## Run locally (dev)`); optional prior ledger under `.skills/` |
| **Writes** | `.skills/<slug>-dogfood-run.md` (git-ignored run ledger); end-of-run report; optional guide checkbox ticks (never authoritative) |
| **Calls** | [`debug`](debug.md) on deterministic product failures |
| **Called by** | user / agent when a guide already exists; hand-off after [`dogfood`](dogfood.md) |

## When it fires

When a dogfood test guide **already exists** and its cases must be executed rather than handed to a human — the agent-driven pass over every case against the running app in a real browser, judging both what the screen shows and what the backend actually stored.

Triggers: run or resume a half-finished guide, work a dogfood file end to end, test every case in the browser and fix what breaks.

**Not for:** authoring the guide ([`dogfood`](dogfood.md)) or writing committed e2e specs ([`acceptance-ui`](acceptance-ui.md)).

The disambiguating predicate is observable: **does a guide file already exist?** If you need the guide written first, that is `dogfood`. If you need durable Playwright assets, that is `acceptance-ui`.

## The Iron Law

```
NO CASE IS TICKED ON THE SCREEN ALONE
```

State-touching cases (create, update, delete, persist) require both `saw` (quoted UI) and `server` (probe that actually ran) before `pass`. Pure presentation records `server: none — presentational`. Invented probe results are forbidden.

Counter recorded on RED: *"Dogfood judges product behavior on screen, not wire traffic."*

## The five steps

### 1. Preconditions — origin and app

Local dev from `project.md` by default. Non-local (staging/prod/shared QA): **stop** until the user explicitly consents in-thread, naming that origin. "Whatever is fastest", a demo deadline, or an already-open tab is not consent.

Drive a dedicated tab. Avoid native `alert`/`confirm` when possible (browser bridges freeze).

### 2. Build the ledger before any drive

Parse every case from the guide (`data-case`, `data-req`, `data-backend`, `data-setup` when present; visible Try/Expect otherwise). Write one ledger row **and** one todo per case **before** driving any case. Resume from the first non-`pass` row if a ledger already exists.

**No row, not run.** Spot-checking "the same CRUD pattern" leaves unfinished rows `pending`/`blocked` — never silent `pass`.

### 3. Drive each pending case

Apply setup → execute Try in the browser (Chrome extension tools when present; else headed Chromium) → fill `saw` → run backend probe when required → set verdict. Mark the todo done only on `pass`.

### 4. Failure routing

| Observation | Action |
|---|---|
| Deterministic product fail | **required sub-skill** [`debug`](debug.md); re-drive failed case + already-pass cases whose req the fix touched |
| Guide wrong / flaky | Fix the guide; re-drive |
| Shared precondition broken | Stop the run; remaining rows stay unfinished |

**Caps:** 3 distinct fixes per case; 5 product-defect fix cycles per run. Then stop with a partial ledger.

Durable asset for a product fix: the regression test `debug` already requires — not a silent promotion of the whole guide into Playwright.

### 5. Close the run

Ledger is authoritative. Write an end-of-run report with every case's verdict + `saw` + `server`. Hand paths to ledger and report; name any unfinished rows.

## Decisions baked into the skill

| Decision | Choice |
|---|---|
| Where "done" is marked | Ledger + todos; end report; guide checkboxes optional only |
| Fix-in-place vs batch | Fix-in-place with the caps above |
| Durable asset | Failures leave regressions via `debug`; passes do not auto-become e2e |

## Worked sketch

Guide path `.skills/note-dogfood.html` with six cases. Agent builds `.skills/note-dogfood-run.md` with six `pending` rows, starts local app, drives CASE-1 create: list shows "Alpha" **and** `GET /api/notes` includes Alpha → `pass`. On CASE-5 delete fail, hands `debug` a red curl loop, re-drives delete plus create/rename/persist that share the store module, continues. Ends with a report matching the ledger.

## Why it is written the way it is

`dogfood` produces a guide for a human. Nothing in the set used to *drive* it. `acceptance-ui` writes durable specs; this skill executes a checklist and self-heals. The shape is closer to `execute-plan` (ledger, resume, circuit breaker) over cases.

RED baselines (grok-4.5) forced the load-bearing rules: screen-only ticks, spot-checks under time pressure, and staging under "whatever is fastest." GREEN re-runs with the skill present flipped those choices. Full transcripts: `tests/drive-dogfood/red-baselines.md`.

## See also

- [`dogfood`](dogfood.md) — author the guide (including machine-drivable `data-*` slots)
- [`acceptance-ui`](acceptance-ui.md) — committed Playwright e2e, not a one-shot run
- [`acceptance-check`](acceptance-check.md) — orchestrator for durable acceptance
- [`debug`](debug.md) — product defects found mid-run
- [Review and acceptance](../process/review-and-acceptance.md) — where this sits in the phase
