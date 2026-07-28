# Trigger routing — `prepare-change` / `finish-branch`

Description-routing baseline for the new skill. Descriptions under test live in:

- `skills/ship/prepare-change/SKILL.md`
- `skills/ship/finish-branch/SKILL.md`

**Status:** baseline rows written at scaffolding time (Task 1); a live multi-model
routing pass is scheduled once the skill's phases are filled in.

## Disambiguators (expected)

| Skill | Observable predicate |
|---|---|
| `prepare-change` | Work is finished but its commits and/or PR description still need **authoring** — nothing has crossed to a reviewer yet |
| `finish-branch` | The branch is already reviewer-ready and an **integration decision** (merge / PR / keep / discard / block) is needed |

## Routing baseline

- **PCHG-1.1** "I have a pile of uncommitted changes ready — group these into proper commits" → routes to `prepare-change`
- "Open a PR for this branch" on an already-committed, unauthored branch → routes to `prepare-change` first (to author commits and the PR package), then `finish-branch` (to approve and submit it)
- "Merge this into main" on a branch whose commits and PR content are already authored → routes to `finish-branch` only

## Recording results

| Query # | Expected | Observed model / choice | Pass? |
|---|---|---|---|
| (fill when a live routing pass runs) | | | |
