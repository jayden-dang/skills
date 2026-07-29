# Trigger routing — `prepare-change` / `finish-branch` / neighbors

Description-routing evidence for `writing-skills`. Descriptions under test:

- `skills/ship/prepare-change/SKILL.md`
- `skills/ship/finish-branch/SKILL.md`
- Neighbors for should-not-fire traps: `execute-plan`, `release`, `record-decision`,
  `code-review`, `verify`, `sync-spec`

**Status:** query set locked before scoring. Live pass recorded below
(fresh context per query; model labelled per row).

## Disambiguators (expected)

| Skill | Observable predicate |
|---|---|
| `prepare-change` | Work is finished but commits and/or PR description still need **authoring** — nothing has crossed |
| `finish-branch` | Branch is reviewer-ready and an **integration decision** (merge / PR / keep / discard / block) is needed |
| `execute-plan` | An approved `tasks.md` still needs **executing** (implement + review loop), not ship authoring alone |
| `release` | Work is already **merged** to the release branch; version/tag/publish |

## Method

1. Write expected skill first; hold out from the tested agent.
2. Fresh context per query — one query per agent turn.
3. Prompt shape: "Which skill from this skill set do you invoke first? Name
   exactly one primary skill. This is live work."
4. Bar = weakest model on the roster.

Roster for this pass: record the harness model on each row.

## Should-fire → `prepare-change` (primary)

| # | Query | Expected primary |
|---|---|---|
| SF1 | I have a pile of uncommitted changes ready — group these into proper commits | `prepare-change` |
| SF2 | Branch work is done but I still need a real PR description written from the diff | `prepare-change` |
| SF3 | Author reviewer-readable commits before we hand this to finish-branch | `prepare-change` |
| SF4 | Open a PR for this branch — commits are a mess / unauthored, no package yet | `prepare-change` first (then `finish-branch`) |
| SF5 | Working tree is dirty after acceptance; make the commit set and PR package | `prepare-change` |
| SF6 | Don't push yet — just prepare the change and the PR body package | `prepare-change` |
| SF7 | Uncommitted residue after the plan tasks — group and commit it cleanly | `prepare-change` |
| SF8 | Resolve the PR base and write the pr-packages manifest for this branch | `prepare-change` |
| SF9 | Commits exist but the pull-request description still has to be written | `prepare-change` |
| SF10 | Turn this finished branch into commits a reviewer can actually read | `prepare-change` |

## Should-not-fire → neighbor wins

| # | Query | Expected primary | Trap |
|---|---|---|---|
| SN1 | Merge this into main — commits and PR content already authored and approved | `finish-branch` | "merge" alone |
| SN2 | Implementation complete, what should I do with the branch? | `finish-branch` | menu language |
| SN3 | Push and create the pull request — package already at `.skills/pr-packages/…` | `finish-branch` | "create PR" after package |
| SN4 | Approved tasks.md is ready — execute the plan | `execute-plan` | end-of-plan ship |
| SN5 | Cut a release, bump version, tag and publish | `release` | ship vocabulary |
| SN6 | Publish the decision record before we cross | `record-decision` | crossing adjacent |
| SN7 | Review this branch's diff for standards and spec | `code-review` | before ship |
| SN8 | Run verify and prove the suite is green before we claim done | `verify` | gate before finish |
| SN9 | Spec drifted from what we shipped — realign requirements/design/tasks | `sync-spec` | after ship |
| SN10 | Discard this work / block the branch at the boundary | `finish-branch` | terminal options |

## Live results

Pass date: 2026-07-29. Method: fresh-context subagents; descriptions only (no
skill bodies). Model: **grok-4.5** (harness default — bar = this model until a
weaker roster model is available).

| Query # | Expected | Model | Observed primary | Pass? | Notes |
|---|---|---|---|---|---|
| SF1 | prepare-change | grok-4.5 | prepare-change | yes | |
| SF2 | prepare-change | grok-4.5 | prepare-change | yes | |
| SF3 | prepare-change | grok-4.5 | prepare-change | yes | |
| SF4 | prepare-change | grok-4.5 | prepare-change | yes | primary authoring first |
| SF5 | prepare-change | grok-4.5 | prepare-change | yes | |
| SF6 | prepare-change | grok-4.5 | prepare-change | yes | |
| SF7 | prepare-change | grok-4.5 | prepare-change | yes | |
| SF8 | prepare-change | grok-4.5 | prepare-change | yes | |
| SF9 | prepare-change | grok-4.5 | prepare-change | yes | |
| SF10 | prepare-change | grok-4.5 | prepare-change | yes | |
| SN1 | finish-branch | grok-4.5 | finish-branch | yes | |
| SN2 | finish-branch | grok-4.5 | finish-branch | yes | |
| SN3 | finish-branch | grok-4.5 | finish-branch | yes | package already present |
| SN4 | execute-plan | grok-4.5 | execute-plan | yes | |
| SN5 | release | grok-4.5 | release | yes | |
| SN6 | record-decision | grok-4.5 | record-decision | yes | |
| SN7 | code-review | grok-4.5 | code-review | yes | |
| SN8 | verify | grok-4.5 | verify | yes | |
| SN9 | sync-spec | grok-4.5 | sync-spec | yes | |
| SN10 | finish-branch | grok-4.5 | finish-branch | yes | |

**Score: 20/20 pass on grok-4.5.**

**Pass criterion:** primary skill matches Expected. For SF4, naming
`prepare-change` first (with finish-branch as later) counts as pass; naming only
`finish-branch` is fail.

**Status:** live routing pass complete for the harness model. Re-run if the
description changes or the ship roster adds a weaker model.
