# Trigger routing — `package-change` / `land-branch` / neighbors

Description-routing evidence for `author-skills`. Descriptions under test:

- `skills/ship/package-change/SKILL.md`
- `skills/ship/land-branch/SKILL.md`
- Neighbors for should-not-fire traps: `build-continuous`, `cut-release`, `record-verdict`,
  `inspect-change`, `prove-claim`, `realign-spec`

**Status:** query set locked before scoring. Live pass recorded below
(fresh context per query; model labelled per row).

## Disambiguators (expected)

| Skill | Observable predicate |
|---|---|
| `package-change` | Work is finished but commits and/or PR description still need **authoring** — nothing has crossed |
| `land-branch` | Branch is reviewer-ready and an **integration decision** (merge / PR / keep / discard / block) is needed |
| `build-continuous` | An approved `tasks.md` still needs **executing** (implement + review loop), not ship authoring alone |
| `cut-release` | Work is already **merged** to the release branch; version/tag/publish |

## Method

1. Write expected skill first; hold out from the tested agent.
2. Fresh context per query — one query per agent turn.
3. Prompt shape: "Which skill from this skill set do you invoke first? Name
   exactly one primary skill. This is live work."
4. Bar = weakest model on the roster.

Roster for this pass: record the harness model on each row.

## Should-fire → `package-change` (primary)

| # | Query | Expected primary |
|---|---|---|
| SF1 | I have a pile of uncommitted changes ready — group these into proper commits | `package-change` |
| SF2 | Branch work is done but I still need a real PR description written from the diff | `package-change` |
| SF3 | Author reviewer-readable commits before we hand this to land-branch | `package-change` |
| SF4 | Open a PR for this branch — commits are a mess / unauthored, no package yet | `package-change` first (then `land-branch`) |
| SF5 | Working tree is dirty after acceptance; make the commit set and PR package | `package-change` |
| SF6 | Don't push yet — just prepare the change and the PR body package | `package-change` |
| SF7 | Uncommitted residue after the plan tasks — group and commit it cleanly | `package-change` |
| SF8 | Resolve the PR base and write the pr-packages manifest for this branch | `package-change` |
| SF9 | Commits exist but the pull-request description still has to be written | `package-change` |
| SF10 | Turn this finished branch into commits a reviewer can actually read | `package-change` |

## Should-not-fire → neighbor wins

| # | Query | Expected primary | Trap |
|---|---|---|---|
| SN1 | Merge this into main — commits and PR content already authored and approved | `land-branch` | "merge" alone |
| SN2 | Implementation complete, what should I do with the branch? | `land-branch` | menu language |
| SN3 | Push and create the pull request — package already at `.skills/pr-packages/…` | `land-branch` | "create PR" after package |
| SN4 | Approved tasks.md is ready — execute the plan | `build-continuous` | end-of-plan ship |
| SN5 | Cut a release, bump version, tag and publish | `cut-release` | ship vocabulary |
| SN6 | Publish the decision record before we cross | `record-verdict` | crossing adjacent |
| SN7 | Review this branch's diff for standards and spec | `inspect-change` | before ship |
| SN8 | Run prove-claim and prove the suite is green before we claim done | `prove-claim` | gate before finish |
| SN9 | Spec drifted from what we shipped — realign requirements/design/tasks | `realign-spec` | after ship |
| SN10 | Discard this work / block the branch at the boundary | `land-branch` | terminal options |

## Live results

Pass date: 2026-07-29. Method: fresh-context subagents; descriptions only (no
skill bodies). Model: **grok-4.5** (harness default — bar = this model until a
weaker roster model is available).

| Query # | Expected | Model | Observed primary | Pass? | Notes |
|---|---|---|---|---|---|
| SF1 | package-change | grok-4.5 | package-change | yes | |
| SF2 | package-change | grok-4.5 | package-change | yes | |
| SF3 | package-change | grok-4.5 | package-change | yes | |
| SF4 | package-change | grok-4.5 | package-change | yes | primary authoring first |
| SF5 | package-change | grok-4.5 | package-change | yes | |
| SF6 | package-change | grok-4.5 | package-change | yes | |
| SF7 | package-change | grok-4.5 | package-change | yes | |
| SF8 | package-change | grok-4.5 | package-change | yes | |
| SF9 | package-change | grok-4.5 | package-change | yes | |
| SF10 | package-change | grok-4.5 | package-change | yes | |
| SN1 | land-branch | grok-4.5 | land-branch | yes | |
| SN2 | land-branch | grok-4.5 | land-branch | yes | |
| SN3 | land-branch | grok-4.5 | land-branch | yes | package already present |
| SN4 | build-continuous | grok-4.5 | build-continuous | yes | |
| SN5 | cut-release | grok-4.5 | cut-release | yes | |
| SN6 | record-verdict | grok-4.5 | record-verdict | yes | |
| SN7 | inspect-change | grok-4.5 | inspect-change | yes | |
| SN8 | prove-claim | grok-4.5 | prove-claim | yes | |
| SN9 | realign-spec | grok-4.5 | realign-spec | yes | |
| SN10 | land-branch | grok-4.5 | land-branch | yes | |

**Score: 20/20 pass on grok-4.5.**

**Pass criterion:** primary skill matches Expected. For SF4, naming
`package-change` first (with land-branch as later) counts as pass; naming only
`land-branch` is fail.

**Status:** live routing pass complete for the harness model. Re-run if the
description changes or the ship roster adds a weaker model.
