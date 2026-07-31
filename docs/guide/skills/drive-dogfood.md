# `drive-dogfood`

> Execute an existing dogfood guide against the **product app** in a real browser. The deliverable is an evidence-backed **run ledger** (CLI) — every case ID accounted for with quoted screen evidence and, when needed, a server-side probe. Guide HTML localStorage ticks are never the agent progress path.

|  |  |
|---|---|
| **Bucket** | acceptance |
| **Invocation** | model-invocable |
| **Reads** | cases YAML or dogfood HTML; `docs/agents/project.md` (`## Run locally (dev)`); prior ledger under `.skills/` |
| **Writes** | `.skills/<slug>-dogfood.json` (verdicts via `dogfood mark`); end report via `dogfood report` |
| **Calls** | dogfood CLI (`list` / `show` / `init` / `mark` / `next` / `status` / `report`); [`debug`](debug.md) on deterministic product failures |
| **Called by** | user / agent when a guide already exists; hand-off after [`dogfood`](dogfood.md) |

## When it fires

When a dogfood catalog **already exists** and cases must be executed rather than handed to a human.

**Not for:** authoring ([`dogfood`](dogfood.md)) or committed e2e ([`acceptance-ui`](acceptance-ui.md)).

## The Iron Law

```
NO CASE IS TICKED ON THE SCREEN ALONE
PROGRESS LIVES IN THE LEDGER — NEVER IN GUIDE localStorage
```

State-touching cases need both `saw` and `server` before `pass`. Presentational cases use `server: none — presentational`.

Agents **must not** open the dogfood HTML in a browser to tick checkboxes. Use:

```bash
DF=python3 <dogfood-skill-root>/scripts/dogfood
$DF init .skills/<slug>-dogfood.json
$DF show <catalog> CASE-1
$DF mark <run> CASE-1 pass --saw '…' --server '…' --catalog <catalog>
$DF next <run>
$DF report <run> -o .skills/<slug>-dogfood-report.md
```

## The five steps

1. **Preconditions** — local origin by default; non-local needs explicit consent. Drive a dedicated **product** tab only.
2. **Ledger first** — `init` (or trust existing); one todo per case; **no row, not run**.
3. **Drive pending** — `show` → setup → Try on the product → evidence → `mark`. Never guide-HTML ticks.
4. **Failure routing** — product defect → `debug`; guide wrong → fix cases YAML (+ re-render); shared precondition → stop run. Caps: 3 fixes/case, 5 fix cycles/run.
5. **Close** — `report`; ledger authoritative.

## Decisions

| Decision | Choice |
|---|---|
| Where "done" is marked | CLI ledger only for agents; HTML ticks human-only |
| Fix-in-place vs batch | Fix-in-place with caps |
| Durable asset | Failures leave regressions via `debug`; passes do not auto-become e2e |

## Why it is written this way

Earlier runs still burned browser tokens ticking guide checkboxes even though D1 already made the ledger authoritative. The CLI makes list/show/mark deterministic and keeps Chrome for the product under test only. RED/GREEN: `tests/drive-dogfood/`.

## See also

- [`dogfood`](dogfood.md) — author cases + render shell
- [`acceptance-ui`](acceptance-ui.md) — committed Playwright
- [`debug`](debug.md) — product defects mid-run
