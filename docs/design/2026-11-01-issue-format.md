# Requirements: One issue format

Feature code: ISSUEFMT
Status: Implemented
Date: 2026-11-01

This repo keeps no `docs/specs/` catalog or roadmap (AGENTS.md section 8), so the record lives
in `docs/design/` and the Step 1 catalog card and roadmap bind have no target. Research:
`.skills/research/2026-11-01-issue-template.md`.

Terms:

- **Reach.** An artifact is *shared* when `git check-ignore -q <path>` exits non-zero, and
  *private* when it exits 0. Specs are judged on a triad path such as
  `docs/specs/_probe/requirements.md`, never on `INDEX.md`, which an index-only gitignore keeps
  tracked. The roadmap is judged on `docs/roadmap/INDEX.md`.
- **Writer.** Anything that creates a tracker issue, with or without a skill loaded.
- **Four fields.** Assignee, priority, estimate, status.

## 1. A reader gets one format

**Story:** As a teammate holding only the tracker, I want to open any new issue and find the same sections, so that I understand the work without knowing how it was produced.

- **ISSUEFMT-1.1** WHEN a writer creates an enhancement issue THE SYSTEM SHALL write the body with the sections Problem, Outcome, Acceptance and Out of scope, in that order.
- **ISSUEFMT-1.2** WHEN a writer creates a bug issue THE SYSTEM SHALL write the body with the sections What happens, Expected, How to reproduce and Evidence, in that order.
- **ISSUEFMT-1.3** IF a bug has not been reproduced THEN THE SYSTEM SHALL say so under How to reproduce.
- **ISSUEFMT-1.4** WHEN a writer creates an issue THE SYSTEM SHALL title it with the outcome it delivers, with no `Task N`, no commit-style prefix such as `feat:`, and no internal prefix other than those ISSUEFMT-2.2 and ISSUEFMT-2.5 keep.
- **ISSUEFMT-1.5** THE SYSTEM SHALL keep source file paths, line numbers, `Task N` items and lists of implementation steps out of issue titles and bodies.
- **ISSUEFMT-1.6** WHERE an issue is a bug THE SYSTEM SHALL allow error text, versions, trace IDs and a minimal reproduction under How to reproduce and Evidence.
- **ISSUEFMT-1.7** THE SYSTEM SHALL write no line stating that AI or a skill drafted an issue body or a tracker comment.
- **ISSUEFMT-1.8** WHEN `/idea` files a ticket THE SYSTEM SHALL place the operator's words verbatim under Problem.
- **ISSUEFMT-1.9** WHILE a ticket is in `shaping` THE SYSTEM SHALL write `Not decided yet` under any format section that has no content yet.
- **ISSUEFMT-1.10** WHEN `plan-tasks` publishes onto an existing ticket THE SYSTEM SHALL keep the operator's words under Problem.
- **ISSUEFMT-1.11** WHEN `triage` posts an agent brief THE SYSTEM SHALL use the sections of the issue's kind and name no type or function.

## 2. Internal IDs follow reach

**Story:** As a project owner, I want an issue to show `CODE`, requirement IDs and `ROAD-N` only where my team can open them, so that a reader never meets a reference they cannot follow.

- **ISSUEFMT-2.1** WHERE specs are private THE SYSTEM SHALL keep feature codes, requirement IDs and spec paths out of issue titles, bodies and comments.
- **ISSUEFMT-2.2** (guard) WHERE specs are shared THE SYSTEM SHALL CONTINUE TO title a `plan-tasks` issue `[CODE] <outcome>` and to write `Requirements covered:` and `Plan:`.
- **ISSUEFMT-2.3** WHERE specs are shared THE SYSTEM SHALL place `Requirements covered:`, `Plan:` and `Roadmap:` as the last lines of the body.
- **ISSUEFMT-2.4** WHERE the roadmap is private THE SYSTEM SHALL keep `ROAD-N` and `MILE-N` out of issue titles, bodies and comments.
- **ISSUEFMT-2.5** (guard) WHERE the roadmap is shared THE SYSTEM SHALL CONTINUE TO treat an open, assigned issue whose title names a `ROAD-N` as its claim.
- **ISSUEFMT-2.6** WHERE the roadmap is private THE SYSTEM SHALL find the ticket of a `ROAD-N` from `.skills/<CODE>/tickets.md`, and SHALL NOT create a second ticket when that file holds one.
- **ISSUEFMT-2.7** WHERE specs are private THE SYSTEM SHALL record a ticket's covered IDs in `.skills/<CODE>/tickets.md`, whose directory gives the feature code.
- **ISSUEFMT-2.8** WHERE specs are private WHEN `/board` or `/go` judges a ready ticket THE SYSTEM SHALL resolve its feature and covered IDs from `.skills/<CODE>/tickets.md`.
- **ISSUEFMT-2.9** (guard) WHERE specs are shared WHEN `/board` or `/go` judges a ready ticket THE SYSTEM SHALL CONTINUE TO recognize a tier-1 fix from `Requirements covered:`.

## 3. Every issue is filled in

**Story:** As an operator, I want every new issue to carry an assignee, priority, estimate and status, so that the board tells me who owns what, how much it matters and how big it is.

| Priority | When |
|---|---|
| Urgent | Production is down, data is being lost, or a security hole is open |
| High | It blocks users or other work, has a deadline this week, or is in `## Focus` |
| Medium | The default, when nothing else applies |
| Low | No time pressure; an improvement |

| Estimate | Complexity |
|---|---|
| 1 | One small change, approach known |
| 2 | A few places in one part of the system |
| 3 | Many places, with points to weigh |
| 5 | Several parts of the system, or open questions remain |
| 8 | Large with many unknowns; consider splitting |

- **ISSUEFMT-3.1** WHEN a writer creates an issue THE SYSTEM SHALL assign the person the operator named, else the operator.
- **ISSUEFMT-3.2** IF the operator said to leave an issue unassigned THEN THE SYSTEM SHALL leave it unassigned and say so in the reply.
- **ISSUEFMT-3.3** WHEN a writer creates an issue THE SYSTEM SHALL apply exactly one state role and one category role from `triage-labels.md`.
- **ISSUEFMT-3.4** WHEN a writer creates an issue THE SYSTEM SHALL set its priority from the operator's word, else the roadmap's `## Focus`, else the priority rubric.
- **ISSUEFMT-3.5** WHEN a writer creates an issue THE SYSTEM SHALL set its estimate on the scale 1, 2, 3, 5, 8 from the operator's word, else the estimate rubric.
- **ISSUEFMT-3.6** WHEN a plan is approved and published onto a ticket THE SYSTEM SHALL revise the ticket's estimate from the approved plan, unless the operator set it.
- **ISSUEFMT-3.7** WHEN a writer creates an issue THE SYSTEM SHALL name its ID, assignee, priority, estimate and status in the reply, or in the final report of an unattended run.
- **ISSUEFMT-3.8** WHEN a writer creates an issue THE SYSTEM SHALL read the issue back from the tracker before reporting the four fields.
- **ISSUEFMT-3.9** IF a field cannot be written THEN THE SYSTEM SHALL keep the issue, name the missing field in the reply and write no substitute value into the body.
- **ISSUEFMT-3.10** IF a build would claim a ticket assigned to someone else THEN THE SYSTEM SHALL ask the operator before reassigning it.
- **ISSUEFMT-3.11** IF nobody can answer during an unattended run THEN THE SYSTEM SHALL leave that ticket unbuilt, report it and carry on with the rest.

## 4. A repo declares the format once

**Story:** As a repo owner, I want to run `/configure-repo` and get one issue format with this repo's field mapping, so that every writer follows the same rule on this tracker.

- **ISSUEFMT-4.1** THE SYSTEM SHALL seed `docs/agents/issue-tracker.md` with an `Issue format` section holding both templates and both rubrics.
- **ISSUEFMT-4.2** THE SYSTEM SHALL seed `docs/agents/issue-tracker.md` with an `Issue fields` table naming how each of the four fields is written and read on this tracker.
- **ISSUEFMT-4.3** WHEN `/configure-repo` runs on a Linear tracker THE SYSTEM SHALL map priority and estimate to Linear's native fields.
- **ISSUEFMT-4.4** WHEN `/configure-repo` runs on a GitHub repo owned by an organization THE SYSTEM SHALL map priority and estimate to the organization's issue fields, unless the organization has no such fields or refuses the write, in which case it SHALL use ISSUEFMT-4.5's labels.
- **ISSUEFMT-4.5** WHEN `/configure-repo` runs on a GitHub repo owned by a person THE SYSTEM SHALL map priority and estimate to `priority:*` and `size:*` labels.
- **ISSUEFMT-4.6** WHERE the tracker is local THE SYSTEM SHALL write the four fields as lines in the issue file.
- **ISSUEFMT-4.7** IF `/configure-repo` would change a tracker's field options or labels THEN THE SYSTEM SHALL name the change and get the operator's consent first.
- **ISSUEFMT-4.8** THE SYSTEM SHALL seed the agent-skills block with one line sending any writer to the `Issue format` section before it creates an issue.
- **ISSUEFMT-4.9** IF `docs/agents/issue-tracker.md` has no `Issue format` section THEN THE SYSTEM SHALL name `/configure-repo`, show the drafted title and fields, and create no issue.

## 5. Blocking uses the tracker

**Story:** As an operator, I want a blocked issue to show as blocked on the board, so that nobody starts work that cannot finish.

- **ISSUEFMT-5.1** WHERE the tracker has a native blocking relation THE SYSTEM SHALL write the edge with that relation and add no `Blocked by:` line.
- **ISSUEFMT-5.2** WHERE the tracker has no native blocking relation THE SYSTEM SHALL write one line in the exact form `Blocked by: #N, #M`.
- **ISSUEFMT-5.3** WHEN `/board` lists a ready ticket THE SYSTEM SHALL show it as blocked if a native edge or a `Blocked by:` line names an open issue.
- **ISSUEFMT-5.4** WHEN `/go` orders tickets THE SYSTEM SHALL take edges from the native relation and the `Blocked by:` line.
- **ISSUEFMT-5.5** WHEN `/sweep-backlog` classifies a ticket THE SYSTEM SHALL take edges from the native relation and the `Blocked by:` line.
- ~~**ISSUEFMT-5.6**~~ superseded by ISSUEFMT-5.8: it left blocked slices on text-only trackers with no state role, against ISSUEFMT-3.3.
- **ISSUEFMT-5.7** IF a build would start a ticket with an open blocker that the same run does not also deliver THEN THE SYSTEM SHALL leave it unbuilt and report the blocker.
- **ISSUEFMT-5.8** WHEN `publish-issues` files a blocked slice on a tracker with labels or states THE SYSTEM SHALL apply the same state role as the slices around it.

## 6. Triage selects by state

**Story:** As a maintainer, I want `/triage` to pick issues by their state, so that planned work is skipped and a reporter's issue is never missed.

- ~~**ISSUEFMT-6.1**~~ superseded by ISSUEFMT-6.6: "unlabeled" read a category-only issue as out of scope.
- **ISSUEFMT-6.2** WHEN `/triage` meets an issue in any other state THE SYSTEM SHALL skip it and say why.
- **ISSUEFMT-6.3** (guard) WHEN a person outside this skill set files an issue THE SYSTEM SHALL CONTINUE TO place it in the triage queue.
- **ISSUEFMT-6.4** (guard) WHEN the operator names an issue and its target state THE SYSTEM SHALL CONTINUE TO treat it as a direct state change.
- **ISSUEFMT-6.6** WHEN `/triage` selects issues THE SYSTEM SHALL take only issues with no state role, `needs-triage` issues and `needs-info` issues with reporter activity.
- **ISSUEFMT-6.5** THE SYSTEM SHALL decide whether to triage an issue from its state and SHALL NOT read its body text to decide.

## 7. Existing behavior stays

**Story:** As a skill-set user, I want my existing commands to keep working after this change, so that the new format costs me no other workflow.

Files the change touches, with what each must keep:

| File | Guard |
|---|---|
| `templates/agents/issue-tracker.md`, `skills/setup/configure-repo/templates/agents/issue-tracker.md` | ISSUEFMT-7.1 |
| `skills/setup/configure-repo/SKILL.md`, `issue-tracker-followups.md` | ISSUEFMT-7.2 |
| `skills/setup/configure-repo/templates/agent-skills-block.md` | no behavior to guard |
| `skills/ship/land-branch/tickets.md` | ISSUEFMT-7.10 |
| `skills/track/show-run-status/scripts/collect.sh` | ISSUEFMT-7.11 |
| `skills/project/plan-milestones/notion-draft.md` | ISSUEFMT-7.12 |
| `skills/ship/land-branch/` other files reading `tickets.md`, `skills-ephemera-paths.md` | ISSUEFMT-7.10 |
| `skills/track/publish-issues/SKILL.md` | ISSUEFMT-7.3 |
| `skills/spec/plan-tasks/publish-recipe.md` | ISSUEFMT-7.4 |
| `skills/track/idea/SKILL.md` | ISSUEFMT-2.5, ISSUEFMT-7.5 |
| `skills/track/shape/SKILL.md` | ISSUEFMT-2.9, ISSUEFMT-7.6 |
| `skills/track/triage/SKILL.md`, `agent-brief-template.md` | ISSUEFMT-6.3, ISSUEFMT-6.4 |
| `skills/spec/specify-behavior/roadmap-bind.md` | ISSUEFMT-2.5, with ISSUEFMT-2.4 and ISSUEFMT-2.6 as its private path |
| `skills/execution/execute-common/tracker-sync.md` | ISSUEFMT-7.7 |
| `skills/execution/deliver-issues/SKILL.md` | ISSUEFMT-2.9 |
| `skills/track/sweep-backlog/SKILL.md` | ISSUEFMT-7.8 |
| `skills/track/board/scripts/board.py`, `test_board.py` | ISSUEFMT-2.9, ISSUEFMT-7.9 |
| `skills/track/chart-progress/scripts/lanes.py` | ISSUEFMT-2.5 |
| `docs/guide/` pages for the skills above, plus `process/ship-and-maintain.md`, `concepts/requirement-ids.md`, `concepts/traceability.md`, `process/specification.md`, `methodology/overview.md` | no behavior to guard |
| `AGENTS.md` section 4, `eval.json` and `TESTS.md` of the skills above | no behavior to guard |

- **ISSUEFMT-7.1** (guard) WHEN a skill reads `docs/agents/issue-tracker.md` THE SYSTEM SHALL CONTINUE TO find the wayfinding operations of the configured tracker.
- **ISSUEFMT-7.2** (guard) WHEN `/configure-repo` runs THE SYSTEM SHALL CONTINUE TO ask the existing tracker, publish unit, program sync and draft surface questions.
- **ISSUEFMT-7.3** (guard) WHEN `/publish-issues` drafts work THE SYSTEM SHALL CONTINUE TO get the operator's approval of the slices before it creates any.
- **ISSUEFMT-7.4** (guard) WHILE Publish unit is `feature` THE SYSTEM SHALL CONTINUE TO open one issue per approved plan and leave tasks in `tasks.md`.
- **ISSUEFMT-7.5** (guard) WHEN `/idea` files a ticket THE SYSTEM SHALL CONTINUE TO swap `needs-triage` for `shaping` after the frame and comment the tier and open questions.
- **ISSUEFMT-7.6** (guard) WHEN `/shape` stops at a gate THE SYSTEM SHALL CONTINUE TO comment what is waiting and on whom.
- **ISSUEFMT-7.7** (guard) WHEN a build claims an unassigned ticket THE SYSTEM SHALL CONTINUE TO assign it and move it to `building` without asking.
- **ISSUEFMT-7.8** (guard) WHEN `/sweep-backlog` runs THE SYSTEM SHALL CONTINUE TO write nothing to the tracker until the operator answers.
- **ISSUEFMT-7.9** (guard) WHEN `/board` runs on an issues file with no native edges THE SYSTEM SHALL CONTINUE TO print every section.
- **ISSUEFMT-7.10** (guard) WHEN `land-branch` resolves a branch's tickets THE SYSTEM SHALL CONTINUE TO take every ticket ID in `.skills/<CODE>/tickets.md`.
- **ISSUEFMT-7.11** (guard) WHERE specs are shared WHEN `/show-run-status` collects a feature's issue THE SYSTEM SHALL CONTINUE TO find it by searching the tracker for the feature code.
- **ISSUEFMT-7.12** (guard) WHEN a milestone draft is signed off in Notion THE SYSTEM SHALL CONTINUE TO publish only the tickets its page lists.

## 8. Quality attributes

**Section-kind:** nfr

**Story:** As a stakeholder, I want measurable quality targets for this feature, so that how-well is not left implicit.

- **Performance:** None. Each issue adds at most one read-back call and one field call, with no target worth setting.
- **Security:** None. Issue fields carry no secrets, and the tracker's existing credential handling does not change.
- **Reliability:** **ISSUEFMT-8.1** THE SYSTEM SHALL pass `scripts/qa-set.py`, `test_board.py` and `test_lanes.py` with zero failures, verified by running all three, with a `TESTS.md` entry for every skill edited.
- **Accessibility:** None. The output is tracker text with no new interface.

Consult: no `docs/` system doc exists in this repo for these attributes, so none was used.

## Out of Scope

- Rewriting or backfilling issues that already exist.
- Creating GitHub Projects, milestones, Linear Initiatives or any other program object.
- Showing priority or estimate on `/board`.
- Changing the config of klynt, zroute, raki or any other adopting repo. Adoption is a separate step, with consent for each repo.
- Changing the org-level `Effort` options on KlyntLabs without the owner's separate consent.
- A ticket record that follows the operator to another machine. `.skills/` is git-ignored, so on another clone a private ticket's feature cannot be resolved; its specs are absent there too.
- The conflict between `publish-issues` calling a slice agent-ready and `/go` sending a slice with no spec back to `shaping`. It is recorded here and decided separately.

## Open Questions

None. Resolved 2026-11-01: `createIssue(issueFields:)` wrote `Priority` on `KlyntLabs/klynt` #285 with the current token, using the option's global ID. REST `issue_field_values` read it back, and the issue was deleted.
