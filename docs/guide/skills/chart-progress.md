# `chart-progress`

> The end-of-week page: what finished, what is building, what can start next and what can run beside it, drawn from the repo the same way every time.

|  |  |
|---|---|
| **Bucket** | track |
| **Invocation** | `/chart-progress` (user-invoked; `disable-model-invocation: true`) |
| **Reads** | `docs/roadmap/INDEX.md`, `docs/specs/INDEX.md` and `docs/specs/catalog/*.md`, each spec folder's `tasks.md` and `design.md`, `docs/adr/`, `docs/architecture/INDEX.md`, `.skills/<CODE>/progress.md`, `.skills/_pending-road*/`, and first-parent `git` history |
| **Writes** | `.skills/dashboard/<date>.notes.json` and `<date>.html`; through `refresh-lanes`, the snapshot `<date>.json` and `docs/roadmap/lanes.md`, left for you to commit |
| **Calls** | [`refresh-lanes`](refresh-lanes.md), for the snapshot and the lanes file. Names [`plan-milestones`](plan-milestones.md) and [`/assess-milestone`](assess-milestone.md) in its notes |
| **Called by** | nobody — it is user-invoked |

## Two scripts and one paragraph

`extract.py`, which lives in [`refresh-lanes`](refresh-lanes.md), turns the repo into one JSON snapshot; `scripts/render.py` turns the snapshot into one self-contained HTML page with inline SVG, light and dark. Both are deterministic: the same revision and date give the same bytes. The agent's only authored content is the notes — a summary and up to five recommendations — and every ID it names must appear in the snapshot.

The split exists because the baseline did not hold still. Two agents asked for this page on the same repo and the same day each wrote a generator of its own: one counted 7 features finished that week and the other 14, one listed 30 items ready to start and the other 16, and each took about seven minutes and 140k tokens. The scripts take a quarter of a second.

## What it shows

The page reads top to bottom like a weekly briefing. Things are named the way a person knows them — a feature by its catalog name, a roadmap item by its feature name or its slug read as words, a milestone by its name — with the ID as a small tag beside it. States are plain words (done, in build, ready, not started), and dates read "Sat 10 Oct".

| Section | What it answers |
|---|---|
| **The week in brief** | the agent's summary and suggestions, then four numbers: finished this week, in build, ready to start, milestones ready to close |
| **Next week** | what is still in build, how long it has been there and how many of its tasks are done; what is ready to start, grouped under each milestone's name and outcome, committed milestones first, with what each opens up and what it shares code with; milestones whose work is all done; the longest chain still ahead |
| **What happened** | features finished this week, day by day; a note when one commit marked several done at once; what went into build; new specs; roadmap changes; new decisions; finished per week over 8 weeks; the last 30 days behind a fold |
| **The roadmap** | unfinished milestones as a graph, columns in the order they can happen; each opens to its own items, with items it waits on elsewhere dashed and "order assumed" where the roadmap does not say |
| **By area** | each catalog area: its mix of states, what is open, what finished lately |
| **Architecture** | the latest decisions; the architecture rules and how many designs name each, behind a fold |
| **Housekeeping** | how many roadmap items record what they wait for, and gaps in the records — a broken `After:`, a milestone whose table and section disagree, a decision number used twice |

Every number comes from the snapshot. Finished and started are status changes in the catalog's first-parent history, dated when they landed; ready means every item the roadmap says it waits for is done.

## Item order is `After:`

The ready set is only as good as the edges. [`plan-milestones`](plan-milestones.md) 1.2.0 writes item order as an `After:` field (`ROAD-N`, `MILE-N`, or `none`); an item without one waits on the member above it, which turns each milestone into one chain and understates what can run in parallel. The health section reports the coverage, and the notes recommend a backfill while it is incomplete.

## Lanes, delivery proof and the migration slot

When the roadmap carries `## Focus` ([`plan-milestones`](plan-milestones.md) 1.4.0), [`refresh-lanes`](refresh-lanes.md) writes `docs/roadmap/lanes.md` — on every run of this page, and right after each skill that moves a roadmap item: one lane per Focus entry (a milestone's live members, or one item, plus the items they name directly in `After:`), who has claimed each item (an open, assigned issue whose title names the ROAD), and who waits for a serialized surface such as `migrations/`. It replaces a hand-kept lanes table; in klynt that table was refreshed five times in six days. The header records the integration ref, its SHA and when the tracker was read, because claims change without a commit.

With `Delivery proof: required` in `docs/agents/project.md`, "done" means merged: an Implemented feature, or a fully ticked `## ROAD-N amendment` group, counts only when its `Delivered-by:` (`PR #N` or a merge SHA) resolves to one commit on the integration ref. A squash subject ending `(#N)`, a "Merge pull request #N" commit, or ancestry all count. Anything else is *in review* and unlocks nothing downstream. The switch is opt-in because klynt's 99 finished features had no `Delivered-by:` yet, and only 13 had a single obvious candidate commit.

## Read-only by contract

Nothing outside `.skills/dashboard/` is written except `docs/roadmap/lanes.md`, which `refresh-lanes` generates. A number the agent doubts is noted beside it, never corrected on the page — the page shows what the record says. Repairs go to [`plan-milestones`](plan-milestones.md) (roadmap), [`realign-spec`](realign-spec.md) (a drifted `Status:`), or `/assess-milestone` (a milestone ready to close).

## See also

- [`refresh-roadmap-status`](refresh-roadmap-status.md) — the same inputs reduced to findings and one next action, in the terminal
- [`assess-milestone`](assess-milestone.md) — the verdict a "ready to close" milestone needs before `Closed`
