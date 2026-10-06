# `run-dogfood`

> Execute an existing guide from write-dogfood against the **product app** in a real browser, and keep going until every case passes. Product defects are fixed and blockers are cleared inside the same unattended run. The deliverable is an evidence-backed **run ledger** (CLI) — every case ID accounted for with quoted screen evidence and, when needed, a server-side probe — plus one report at the end. Guide HTML localStorage ticks are never the agent progress path.

|  |  |
|---|---|
| **Bucket** | acceptance |
| **Invocation** | model-invocable |
| **Reads** | `.skills/<CODE>/dogfood.json`; `.skills/<CODE>/dogfood-review.md` (the gate); `docs/agents/project.md` (`## Run locally (dev)`) |
| **Writes** | `.skills/<CODE>/dogfood.json` (verdicts via `dogfood mark`); fix commits on the run's branch; local fixtures and env to unblock cases; end report via `dogfood report` plus four appended sections |
| **Calls** | the `dogfood` CLI (`list` / `show` / `init` / `mark` / `next` / `status` / `report`); [`root-cause`](root-cause.md) fix subagents on product failures, one at a time; `write-dogfood`'s review fix loop after a guide edit |
| **Called by** | user / agent when a guide already exists; hand-off after [`write-dogfood`](write-dogfood.md) |

## When it fires

When a write-dogfood catalog **already exists** and cases must be executed rather than handed to a human.

**Not for:** authoring ([`write-dogfood`](write-dogfood.md)) or committed e2e ([`validate-ui`](validate-ui.md)).

## The Iron Law

```
NO CASE IS TICKED ON THE SCREEN ALONE
PROGRESS LIVES IN THE LEDGER — NEVER IN GUIDE localStorage
THE RUN ENDS ONLY WHEN EVERY CASE IS PASS OR PARKED — NO REPORT BEFORE THAT
```

A case is **parked** in two situations only: it still fails after 3 fix attempts (Gate 3), or it is blocked on something only a person can supply (a credential, a non-local origin, a real payment, a missing browser driver).

State-touching cases need both `saw` and `server` before `pass`. Presentational cases use `server: none — presentational`.

Agents **must not** open the write-dogfood HTML in a browser to tick checkboxes. Use:

```bash
DF="python3 <write-dogfood-skill-root>/scripts/dogfood"
RUN=.skills/<CODE>/dogfood.json
$DF init $RUN
$DF show $RUN CASE-1
$DF mark $RUN CASE-1 pass --saw '…' --server '…'
$DF next $RUN
$DF report $RUN -o .skills/<CODE>/dogfood-report.md
```

## The five steps

1. **Preconditions** — a fresh clean `dogfood-review.md` (or a named override of each open `VFG-N`); local origin by default; non-local needs explicit consent. Drive a dedicated **product** tab only. On `main`/`master`, ask once here or branch first — the drive never stops later to ask.
2. **Ledger first** — `init` (or trust existing); record `RUN_BASE`; one todo per case; **no row, not run**.
3. **Round one** — drive every case once: `show` → setup → Try on the product → evidence → `mark`. Never guide-HTML ticks.
4. **Fix and unblock, in a loop** — `blocked` → build the precondition locally (start the app, run the migration, create the record or the test account, set local env with a dev stand-in). `fail` → one isolated `root-cause` fix subagent at a time, which commits on the branch as `pending disposition`. Then re-drive the case and the passes the fix touched. A guide edit needs a spec line behind it and re-enters `write-dogfood`'s review fix loop. Park a case after 3 failed attempts; there is no run-wide cap.
5. **Close** — whole suite once if a fix landed; `report` plus four sections: Why it failed, Why it was blocked, Notable changes, Awaiting your accept. This is the first report the user gets.

## Decisions

| Decision | Choice |
|---|---|
| Where "done" is marked | CLI ledger only for agents; HTML ticks human-only |
| Fix-in-place vs batch | Fix-in-place, unattended; a case is parked after 3 failed attempts, and the run itself never stops on a cap |
| When the user hears | Once, at close — never between rounds |
| Who accepts a fix's cause | The user, at close: `root-cause` disposition is deferred to the report, and the fix does not merge before the accept |
| Durable asset | Failures leave regressions via `root-cause`; passes do not auto-become e2e |

## Why it is written this way

Earlier runs still burned browser tokens ticking guide checkboxes even though D1 already made the ledger authoritative. The CLI makes list/show/mark deterministic and keeps Chrome for the product under test only. RED/GREEN: `tests/run-dogfood/`.

## See also

- [`write-dogfood`](write-dogfood.md) — author cases + render shell
- [`validate-ui`](validate-ui.md) — the kimi-webbridge acceptance drive
- [`root-cause`](root-cause.md) — product defects mid-run (deferred accept)
