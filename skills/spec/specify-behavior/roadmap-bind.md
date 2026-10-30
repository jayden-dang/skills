# Bind the roadmap item

Loaded from Step 1's `WHERE` pointer, when `docs/roadmap/INDEX.md` exists.

Slot vs CODE definitions live in `plan-milestones` (**ROAD-N is a slot, not a
feature**). This step only writes the join.

**Claim first.** WHERE `docs/agents/issue-tracker.md` exists and this work implements or
amends a `ROAD-N`, read the tracker live before writing anything — never a generated lanes
file. With GitHub: `gh issue list --state open --json number,title,assignees` and
`gh api user --jq .login`. An open issue whose **title** names the `ROAD-N` is its claim:

- assigned to someone else → stop; write nothing, and name the issue and its assignee;
- assigned to you → continue, and cite the issue number in your reply;
- unassigned → assign it to yourself (the file's Assign operation), then continue;
- no such issue → create one titled `ROAD-N <slug>` and assign it to yourself, then continue.

Continue means the issue now exists and is assigned to you. When the create or the assign
fails — a permission denial, no `gh` login — stop as on someone else's claim and name the
command for the user to run. A run whose `gh issue create` was denied wrote the card and the
requirements anyway and reported "the claim is missing": the unclaimed spec this check exists
to prevent.

Two baseline runs wrote a Draft card and requirements for ROAD-6 without calling the tracker
once, while #301 "ROAD-6 desktop foundation" was assigned to alice in shaping.

WHERE `docs/roadmap/INDEX.md` exists and this work implements one of its items, put that
item's `ROAD-N` in the shard row's **Roadmap item** column. WHERE there is no roadmap, or the work
was never a roadmap item, write `—`.

WHEN a tier-1 mini-spec delivers a roadmap item by changing this feature — the hand-off
names a `ROAD-N` that has no feature of its own — keep the cell's own `ROAD-N` and append
the delivered item after `amends`: `ROAD-2` becomes `ROAD-2 amends ROAD-5` (comma-separated
when there are several). `R5` and `R6` judge the part before `amends`; the amended item is
bound, not unspecced. Then open its task group in the feature's `tasks.md` — a
`## ROAD-5 amendment: <title>` heading with the tasks under it, written before any code, so
the item reads as in build while it is built. Two baseline runs kept the cell at `ROAD-2`
because "a two-valued cell would break R5", and left the item to show as unspecced
indefinitely with the link only in prose.

This column is the only plan↔spec join, and this step is its only writer — never invent a
`ROAD-N` here. IF the chosen ROAD is already bound to another CODE (`R6` in
`templates/roadmap-findings.md`) → stop and surface the collision; do not rebind or mint
another ROAD.
