# `run-product-walkthrough`

> Execute an existing review-product-flow guide against the **product app** in a real browser. The deliverable is an evidence-backed **run ledger** (CLI) — every case ID accounted for with quoted screen evidence and, when needed, a server-side probe. Guide HTML localStorage ticks are never the agent progress path.

|  |  |
|---|---|
| **Bucket** | acceptance |
| **Invocation** | model-invocable |
| **Reads** | cases YAML or review-product-flow HTML; `docs/agents/project.md` (`## Run locally (dev)`); prior ledger under `.skills/` |
| **Writes** | `.skills/<slug>-review-product-flow.json` (verdicts via `review-product-flow mark`); end report via `review-product-flow report` |
| **Calls** | review-product-flow CLI (`list` / `show` / `init` / `mark` / `next` / `status` / `report`); [`root-cause`](root-cause.md) on deterministic product failures |
| **Called by** | user / agent when a guide already exists; hand-off after [`review-product-flow`](review-product-flow.md) |

## When it fires

When a review-product-flow catalog **already exists** and cases must be executed rather than handed to a human.

**Not for:** authoring ([`review-product-flow`](review-product-flow.md)) or committed e2e ([`validate-ui`](validate-ui.md)).

## The Iron Law

```
NO CASE IS TICKED ON THE SCREEN ALONE
PROGRESS LIVES IN THE LEDGER — NEVER IN GUIDE localStorage
```

State-touching cases need both `saw` and `server` before `pass`. Presentational cases use `server: none — presentational`.

Agents **must not** open the review-product-flow HTML in a browser to tick checkboxes. Use:

```bash
DF=python3 <review-product-flow-skill-root>/scripts/review-product-flow
$DF init .skills/<slug>-review-product-flow.json
$DF show <catalog> CASE-1
$DF mark <run> CASE-1 pass --saw '…' --server '…' --catalog <catalog>
$DF next <run>
$DF report <run> -o .skills/<slug>-review-product-flow-report.md
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

Earlier runs still burned browser tokens ticking guide checkboxes even though D1 already made the ledger authoritative. The CLI makes list/show/mark deterministic and keeps Chrome for the product under test only. RED/GREEN: `tests/run-product-walkthrough/`.

## See also

- [`review-product-flow`](review-product-flow.md) — author cases + render shell
- [`validate-ui`](validate-ui.md) — committed Playwright
- [`root-cause`](root-cause.md) — product defects mid-run
