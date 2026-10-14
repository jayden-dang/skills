---
name: chart-progress
version: 1.0.0
description: Generates a weekly progress dashboard (one HTML page) of what finished, what is building, what is ready to start, and the roadmap graph. Run it with /chart-progress.
disable-model-invocation: true
---

# Chart Progress

One self-contained HTML page for the end-of-week review: what finished in the last 7 and 30
days, what is building, what is ready to start next, the roadmap as a dependency graph, each
catalog domain, the architecture invariants and latest decisions, and structural health.

Every number on the page comes from `scripts/extract.py`, a fixed parse of the repo's
markdown and git history. The agent writes one thing: the notes — a short summary and the
recommendations for next week, read off that snapshot.

## The Iron Law

```
EVERY NUMBER ON THE PAGE COMES FROM THE SNAPSHOT. THE AGENT NEVER RE-DERIVES ONE.
```

Two baseline agents, given this repo on the same day without this skill, each wrote its own
generator and its own rules. One counted 7 features finished that week, the other 14; one
listed 30 items ready to start, the other 16 — "this is my own rule, not a roadmap field",
plus readings "hand-applied" from `Blockers:` prose. Each run took about seven minutes and
140k tokens, and its generator was left in `/tmp`. A dashboard whose numbers move with the
reader cannot be compared week to week, which is the only thing a weekly dashboard is for.

## Run it

From the root of the repo under review, `<skill>` being this skill's folder:

```bash
d=.skills/dashboard; today=$(date +%F)
python3 <skill>/scripts/extract.py . --today "$today" --out "$d/$today.json"
```

*Done when: the snapshot JSON exists. A missing `docs/roadmap/INDEX.md` is not an error — the
page then says there is no roadmap, and the rest still renders.*

## Write the notes

Read the snapshot, then write `.skills/dashboard/<today>.notes.json`:

```json
{"summary": "two or three sentences on the week",
 "recommendations": ["…", "…", "…"]}
```

- **summary** — what finished, what is building, and the one thing that changed the plan.
  Quote counts and IDs from the snapshot as they are.
- **recommendations** — at most five, each naming the IDs it acts on, drawn from these
  snapshot fields: `graph.ready` (ranked by commitment, milestone order, then `graph.unlocks`),
  features with `status: In-progress`, `graph.closable` (name `/assess-milestone`),
  `graph.conflicts` (which ready items must not run together), and `findings`.
- When `coverage.with_after` is below `coverage.live_items`, the ready set and critical path
  are built from list order for the items without `After:`. Say so once in the summary and
  recommend backfilling `After:` through `plan-milestones` before trusting the lanes.

A number you believe is wrong is written as a note beside it ("FTRASH is in the 10-10 batch —
the record caught up that day"), never corrected on the page. The page shows what the record
says; the notes say what you think of it.

*Done when: every ID in the notes appears in the snapshot.*

## Render and hand over

```bash
python3 <skill>/scripts/render.py "$d/$today.json" --notes "$d/$today.notes.json" --out "$d/$today.html"
```

Open it (`open` / `xdg-open` / `start`) and reply with the absolute path, the summary, and the
recommendations — nothing else. The page is local and read-only: no file outside
`.skills/dashboard/` is written, and no status, roadmap line, or spec is touched. Repairs the
page points at belong to `plan-milestones`, `realign-spec`, or `/assess-milestone`.

*Done when: the HTML opens and the reply names its path.*

## What the page derives, and from where

| View | Source |
|---|---|
| Finished / started / new specs | catalog `Status` changes in first-parent git history, dated when they landed on the branch; one commit moving 3+ features to done is flagged as a batch |
| Building, task progress | catalog `In-progress`; `### Task N:` in `tasks.md` against `Task N: complete` in `.skills/<CODE>/progress.md` |
| Ready, blocked, critical path, unlocks | roadmap `After:` (an item without it waits on the member above it) joined to catalog status |
| Shared paths | backtick paths in `Surfaces:` of ready and building items, ignoring container directories |
| Milestones ready to close | every live member done, milestone not `Closed` |
| Architecture | `- **ARCH-N**` lines; `Respects:` lines in each feature's `design.md`; `docs/adr/NNNN-*.md` |
| Health | `S8` (dangling or cyclic `After:`), table/block commitment disagreement, duplicate ADR numbers, `After:` coverage |

## Red Flags

- Writing a generator, a query, or a `git log` pass of your own to fill in a number
- A count in the notes that differs from the snapshot field it names
- Reading `Blockers:` prose to decide what is ready
- Editing the HTML after `render.py` wrote it
- Writing anywhere outside `.skills/dashboard/`

## No-op

No `docs/specs/INDEX.md` and no `docs/roadmap/INDEX.md`: there is nothing to chart. Say the
repo carries neither and stop.
