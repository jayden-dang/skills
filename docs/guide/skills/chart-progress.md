# `chart-progress`

> The end-of-week page: what finished, what is building, what can start next and what can run beside it, drawn from the repo the same way every time.

|  |  |
|---|---|
| **Bucket** | track |
| **Invocation** | `/chart-progress` (user-invoked; `disable-model-invocation: true`) |
| **Reads** | `docs/roadmap/INDEX.md`, `docs/specs/INDEX.md` and `docs/specs/catalog/*.md`, each spec folder's `tasks.md` and `design.md`, `docs/adr/`, `docs/architecture/INDEX.md`, `.skills/<CODE>/progress.md`, `.skills/_pending-road*/`, and first-parent `git` history |
| **Writes** | `.skills/dashboard/<date>.json`, `<date>.notes.json`, `<date>.html` — nothing else |
| **Calls** | nothing. Names [`plan-milestones`](plan-milestones.md) and [`/assess-milestone`](assess-milestone.md) in its notes |
| **Called by** | nobody — it is user-invoked |

## Two scripts and one paragraph

`scripts/extract.py` turns the repo into one JSON snapshot; `scripts/render.py` turns the snapshot into one self-contained HTML page with inline SVG, light and dark. Both are deterministic: the same revision and date give the same bytes. The agent's only authored content is the notes — a summary and up to five recommendations — and every ID it names must appear in the snapshot.

The split exists because the baseline did not hold still. Two agents asked for this page on the same repo and the same day each wrote a generator of its own: one counted 7 features finished that week and the other 14, one listed 30 items ready to start and the other 16, and each took about seven minutes and 140k tokens. The scripts take a quarter of a second.

## What it shows

| View | Derived from |
|---|---|
| **Plan next week** | the ready set (every open item whose `After:` is done), ranked committed-first, then milestone order, then how many items it unlocks; what is building, with task progress from the ledger; the critical path; milestones whose members are all done but are not `Closed`; paths that ready and building items share |
| **What happened** | status changes in the catalog's first-parent history for the last 7 and 30 days, dated when they landed; a commit that moves three or more features to done at once is flagged as a batch, since its date is when the record caught up; roadmap items that entered, came back from deferred, or left the plan; new ADRs; commits by conventional scope |
| **Roadmap** | the milestone graph, columns by dependency depth; each milestone opens to its own item graph, outside predecessors dashed, items without `After:` marked "implied order" |
| **Catalog** | per domain: status mix, open features, latest finished |
| **Architecture** | each `ARCH-N` with the number of designs whose `Respects:` line cites it; the latest ADRs |
| **Health** | `S8` (dangling or cyclic `After:`), a milestone whose table row and block disagree on commitment, duplicate ADR numbers, and `After:` coverage |

## Item order is `After:`

The ready set is only as good as the edges. [`plan-milestones`](plan-milestones.md) 1.2.0 writes item order as an `After:` field (`ROAD-N`, `MILE-N`, or `none`); an item without one waits on the member above it, which turns each milestone into one chain and understates what can run in parallel. The health section reports the coverage, and the notes recommend a backfill while it is incomplete.

## Read-only by contract

Nothing outside `.skills/dashboard/` is written. A number the agent doubts is noted beside it, never corrected on the page — the page shows what the record says. Repairs go to [`plan-milestones`](plan-milestones.md) (roadmap), [`realign-spec`](realign-spec.md) (a drifted `Status:`), or `/assess-milestone` (a milestone ready to close).

## See also

- [`refresh-roadmap-status`](refresh-roadmap-status.md) — the same inputs reduced to findings and one next action, in the terminal
- [`assess-milestone`](assess-milestone.md) — the verdict a "ready to close" milestone needs before `Closed`
