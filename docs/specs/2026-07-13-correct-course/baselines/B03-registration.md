# B03 — registration

Baseline for Task 3: registering `correct-course` across every roster surface — the plugin
manifest, `AGENTS.md`, `DESIGN.md`, the guide, and the `ask` router — bumping the skill count
35 → 36 everywhere. Each scenario is walked by hand against the edited files (this repo
verifies skills by baseline scenario, not an automated harness — see Global Constraints). RED
= walked before the edits (`correct-course` is absent from every surface and every count reads
35, "Thirty-five"); GREEN = walked after the edits, confirmed to hold.

## S1 — Every roster surface registers correct-course at count 36

**Walk:**
- `.claude-plugin/plugin.json` `skills[]` contains `"./skills/track/correct-course",` inside
  the track cluster.
- `AGENTS.md` line 3 header reads `36 skills across 10 categories`.
- `AGENTS.md` §8 file-org tree (`skills/ # skill definitions (...)` comment) reads `36 skills,
  10 categories`, and the `track/` tree line lists `correct-course` alongside `amend, triage,
  sync-spec, improve-architecture, handoff, file-issues`.
- `AGENTS.md` §11 heading reads `## 11. Quick Reference: The 36 Skills`, and the **track** row
  of the quick-reference table includes `` `correct-course` (m) ``.
- `DESIGN.md` skill-inventory legend line reads `**36 skills.**`.
- `DESIGN.md` compact tree `track/` line lists `correct-course`.
- `DESIGN.md` numbered inventory: `### track/` group gains a new item **35 — correct-course
  (m)**, appended after item 34 (`file-issues`); `### project/`'s `establish-project` is
  renumbered from 35 to **36**.
- `docs/guide/skills/correct-course.md` exists as a new guide page, mirroring `amend.md`'s
  structure (title, blurb, metadata table, `## When it fires`, numbered workflow sections,
  red flags, worked example, "why it is written the way it is", `## See also`), factual to
  `skills/track/correct-course/SKILL.md`.
- `docs/guide/skills/README.md` line 3 reads `Thirty-six skills in ten buckets.`, and the
  `## track` table gains a `` [`correct-course`](correct-course.md) `` row with Invocation
  `model`.

Every count surface (AGENTS.md ×3, DESIGN.md ×1, README word form) reads 36 or "Thirty-six";
none still reads 35 or "Thirty-five".

RED (before edit): `correct-course` is absent from `plugin.json`, both `AGENTS.md` spots,
both `DESIGN.md` inventories, and the README track table; no `docs/guide/skills/correct-course.md`
exists; every count surface reads 35 / "Thirty-five".
GREEN (after edit): all of the above holds as described.

`[CCOURSE-7.1]`

## S2 — ask on-ramp

`skills/meta/ask/SKILL.md`'s `## On-ramps` section routes "a mid-execution discovery
invalidated my approved plan" to `correct-course`.

**Walk:** Read the `## On-ramps` list. Confirm a new bullet, near the `amend`/`debug`
bullets, reads to the effect of: "A mid-execution discovery invalidated your already-approved
plan (the plan is wrong, scope changed mid-flight, the design no longer holds) →
**`correct-course`**", noting it classifies the lowest invalidated artifact and routes the
re-entry, and that `execute-plan` also hands off to it.

RED (before edit): no on-ramp bullet mentions `correct-course`; the mid-execution
plan-invalidation scenario has no named entry point in `ask`.
GREEN (after edit): the bullet exists as described, and `correct-course` is reachable from the
router.

`[CCOURSE-7.2]`

## Coverage self-check

Both of Task 3's IDs appear in at least one tag above: 7.1, 7.2 — 2 of 2, none missing, none
double-defined.
