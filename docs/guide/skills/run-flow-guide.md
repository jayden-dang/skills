# `run-flow-guide`

> Execute an existing guide from write-flow-guide against the **product app** in a real browser. The deliverable is an evidence-backed **run ledger** (CLI) — every case ID accounted for with quoted screen evidence and, when needed, a server-side probe. Guide HTML localStorage ticks are never the agent progress path.

|  |  |
|---|---|
| **Bucket** | acceptance |
| **Invocation** | model-invocable |
| **Reads** | cases YAML or write-flow-guide HTML; `docs/agents/project.md` (`## Run locally (dev)`); prior ledger under `.skills/` |
| **Writes** | `.skills/<slug>-flow-guide.json` (verdicts via `write-flow-guide mark`); end report via `write-flow-guide report` |
| **Calls** | write-flow-guide CLI (`list` / `show` / `init` / `mark` / `next` / `status` / `report`); [`root-cause`](root-cause.md) on deterministic product failures |
| **Called by** | user / agent when a guide already exists; hand-off after [`write-flow-guide`](write-flow-guide.md) |

## When it fires

When a write-flow-guide catalog **already exists** and cases must be executed rather than handed to a human.

**Not for:** authoring ([`write-flow-guide`](write-flow-guide.md)) or committed e2e ([`validate-ui`](validate-ui.md)).

## The Iron Law

```
NO CASE IS TICKED ON THE SCREEN ALONE
PROGRESS LIVES IN THE LEDGER — NEVER IN GUIDE localStorage
```

State-touching cases need both `saw` and `server` before `pass`. Presentational cases use `server: none — presentational`.

Agents **must not** open the write-flow-guide HTML in a browser to tick checkboxes. Use:

```bash
DF=python3 <write-flow-guide-skill-root>/scripts/flow-guide
$DF init .skills/<slug>-flow-guide.json
$DF show <catalog> CASE-1
$DF mark <run> CASE-1 pass --saw '…' --server '…' --catalog <catalog>
$DF next <run>
$DF report <run> -o .skills/<slug>-flow-guide-report.md
```

## The five steps

1. **Preconditions** — local origin by default; non-local needs explicit consent. Drive a dedicated **product** tab only.
2. **Ledger first** — `init` (or trust existing); one todo per case; **no row, not run**.
3. **Drive pending** — `show` → setup → Try on the product → evidence → `mark`. Never guide-HTML ticks.
4. **Failure routing** — product defect → `root-cause`; guide wrong → fix cases YAML (+ re-render); shared precondition → stop run. Caps: 3 fixes/case, 5 fix cycles/run.
5. **Close** — `report`; ledger authoritative.

## Decisions

| Decision | Choice |
|---|---|
| Where "done" is marked | CLI ledger only for agents; HTML ticks human-only |
| Fix-in-place vs batch | Fix-in-place with caps |
| Durable asset | Failures leave regressions via `root-cause`; passes do not auto-become e2e |

## Why it is written this way

Earlier runs still burned browser tokens ticking guide checkboxes even though D1 already made the ledger authoritative. The CLI makes list/show/mark deterministic and keeps Chrome for the product under test only. RED/GREEN: `tests/run-flow-guide/`.

## See also

- [`write-flow-guide`](write-flow-guide.md) — author cases + render shell
- [`validate-ui`](validate-ui.md) — committed Playwright
- [`root-cause`](root-cause.md) — product defects mid-run
