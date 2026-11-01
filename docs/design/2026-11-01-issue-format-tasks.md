# Tasks: One issue format

> **For agentic workers:** after plan approval, pick one execute skill —
> `build-in-waves` (continuous dependency-aware scheduler), `build-by-story` (human-gated story review
> units), or `build-inline` (controller implements, no implementer subagents).
> The chosen skill writes `Execution-mode:`. Steps use checkbox (`- [ ]`) syntax
> for tracking.

Feature code: ISSUEFMT
Status: Implemented
Date: 2026-11-01
Execution-mode: unset
Max-concurrency: auto
Requirements: ./2026-11-01-issue-format.md
Design: ./2026-11-01-issue-format-design.md

**Goal:** Every new tracker issue, from any writer, follows one format and carries an assignee, priority, estimate and status.

**Architecture:** The format lives in the `docs/agents/issue-tracker.md` seed, which every writer already reads. Skills send the writer there and keep only what is specific to them. Readers that parsed removed text move to state, native edges, or `.skills/<CODE>/tickets.md`.

**Tech Stack:** Markdown skills, Python 3 scripts with `unittest`, RED and GREEN scenario runs through the `skill-tester` (Sonnet) and `skill-tester-haiku` agents.

## Global Constraints

Source: `AGENTS.md`, sha256 `ab727c56f55c` (prefix). This repo has no `docs/agents/project.md`, and no `docs/standards/`.

- Skills are test-driven: no edit ships without a RED baseline run recorded in `TESTS.md`, and text with no failure behind it is dropped (section 7).
- `description` frontmatter states trigger and outcome. Each edited skill bumps `version` (section 7).
- SKILL.md limit 300 lines. A skill may reference no other skill's folder except `execute-common`.
- Skill text is English only, with no language default.
- Whole check: `python3 scripts/qa-set.py`. Mirror seeds with `python3 scripts/lint-skill-templates.py --write`.
- Commits carry no `Co-Authored-By` trailer in this repo.
- Test agents cannot call `gh issue create`, so scenarios use the stub tracker from Task 1.

## File Structure

| File | Responsibility |
|---|---|
| `.skills/ISSUEFMT/fixture/make.sh` | Builds shared and private fixture repos with the stub tracker (git-ignored) |
| `.skills/ISSUEFMT/fixture/score.py` | Scores a fixture's issues against the format (git-ignored) |
| `templates/agents/issue-tracker.md` | Seed: `Issue format`, `Issue fields`, Conventions |
| `skills/setup/configure-repo/templates/agents/issue-tracker.md` | Mirror of the seed |
| `skills/setup/configure-repo/templates/agent-skills-block.md` | Points any writer at `Issue format` |
| `skills/setup/configure-repo/issue-tracker-followups.md` | Fills `Issue fields` per tracker and owner type |
| `skills/setup/configure-repo/SKILL.md` | Decision A Done-when and version |
| `skills/track/publish-issues/SKILL.md` | Uses the format; same state role on all slices |
| `skills/spec/plan-tasks/publish-recipe.md` | Uses the format; keeps Problem; revises estimate; writes `covers:` |
| `skills/spec/plan-tasks/SKILL.md` | Version |
| `skills/track/idea/SKILL.md` | Words under Problem; `road:` where private |
| `skills/track/shape/SKILL.md` | Tier-1 line by reach; writes `covers:` |
| `skills/track/triage/SKILL.md` | Selects by state; no marker lines |
| `skills/track/triage/agent-brief-template.md` | Brief uses the issue's sections |
| `skills/spec/specify-behavior/roadmap-bind.md` | Claim by reach; create follows the format |
| `skills/spec/specify-behavior/SKILL.md` | Version |
| `templates/skills-ephemera-paths.md`, and its five mirrors under `refresh-roadmap-status`, `build-in-waves`, `build-inline`, `build-by-story`, `specify-behavior` | Promotion appends `tickets.md` lines; mirrored by `--write` |
| `skills/track/board/scripts/board.py` | Reads records and native edges |
| `skills/track/board/scripts/test_board.py` | Covers the above |
| `skills/track/board/SKILL.md` | Version |
| `skills/execution/deliver-issues/SKILL.md` | Reads records and edges; holds back blocked tickets; assignee guard |
| `skills/execution/execute-common/tracker-sync.md` | Assignee and blocker checks before claiming |
| `skills/execution/execute-common/SKILL.md` | Version |
| `skills/track/sweep-backlog/SKILL.md` | Reads native edges |
| `skills/*/*/TESTS.md`, `skills/*/*/eval.json` of the skills above | Recorded runs and assertions |
| `AGENTS.md` | Section 4 table, "Agent skills" section |
| `docs/guide/skills/{publish-issues,triage,plan-tasks,idea,shape,sweep-backlog,deliver-issues,board,configure-repo,specify-behavior,chart-progress}.md` | Reworded where they state the old rule |
| `docs/guide/process/{ship-and-maintain,specification}.md`, `docs/guide/concepts/{requirement-ids,traceability}.md`, `docs/guide/methodology/overview.md` | Reworded where they state the old rule |

`load-subgraph`: no-op, this repo has no catalog. Coverage: none to state.

---

### Task 1: Any writer follows one format

**Files:**
- Create: `.skills/ISSUEFMT/fixture/make.sh`
- Create: `.skills/ISSUEFMT/fixture/score.py`
- Modify: `templates/agents/issue-tracker.md`
- Modify: `skills/setup/configure-repo/templates/agents/issue-tracker.md`
- Modify: `skills/setup/configure-repo/templates/agent-skills-block.md`
- Modify: `skills/setup/configure-repo/TESTS.md`

**Reuse:** rung 2 — `templates/agents/issue-tracker.md` and its mirror, kept in sync by `scripts/lint-skill-templates.py --write`

**Interfaces:**
- Consumes: none
- Produces: `make.sh <dir> shared|private [--no-format] [--no-native-edges] [--local] [--fail-field <name>]` builds a git repo with `tools/tix` (subcommands `create`, `edit`, `view`, `list`, with `--blocked-by`, storing `.tix/issues.json`), `docs/agents/issue-tracker.md`, `triage-labels.md` and an agent-skills block. `--no-native-edges` drops `--blocked-by`, `--local` uses `.scratch/` files instead of `tix`, and `--fail-field` makes writes to that field fail. `score.py <dir> [--reach shared|private]` prints one PASS or FAIL per criterion, per issue. The sections `## Issue format` and `## Issue fields`.

**Depends-on:** none

- [x] **Step 1: Build the fixture and scorer.** Run `make.sh /tmp/if-red shared` and create one issue by hand that breaks each rule; `score.py` must print a FAIL for each.
- [x] **Step 2: RED.** Fixture holds today's seed. Two `skill-tester` and two `skill-tester-haiku` runs of each prompt, no skill named:
  - A: "File a ticket: exports write NaN for empty numeric cells."
  - B: "File a ticket: let owners export invoices as CSV."
  - C: "File two tickets: CSV export, and PDF export, which needs CSV export done first."
  - D: "File a ticket for alice: rotate the signing key." and E: "File a ticket, leave it unassigned: clean up old exports."
  - F: "File a ticket and leave it in shaping: reports feel slow. Nothing about the scope is decided."

  Run `score.py`, expect FAILs on sections, priority, estimate, edges or read-back. Record verbatim. If nothing fails, stop and drop this text.
- [x] **Step 3: Write the sections** from the design's draft into `templates/agents/issue-tracker.md`, delete the marker bullets from Conventions, add the block's line, and mirror with `python3 scripts/lint-skill-templates.py --write`.
- [x] **Step 4: GREEN.** Rerun A to F on a new fixture with the new seed, on `shared` and `private`. Expect all PASS. Then:
  - `--no-native-edges`, prompt C: expect one `Blocked by: #N` line.
  - `--local`, prompt A: expect `Priority:` and `Estimate:` lines in the file.
  - `--fail-field estimate`, prompt B: expect the issue kept, estimate named as missing, nothing in the body.
  - `--no-format`, prompt A: expect no issue created and `/configure-repo` named.

  Record in `TESTS.md`.
- [x] **Step 5: Commit** `feat(configure-repo): seed one issue format for every writer`.

_Requirements: ISSUEFMT-1.1, ISSUEFMT-1.2, ISSUEFMT-1.3, ISSUEFMT-1.4, ISSUEFMT-1.5, ISSUEFMT-1.6, ISSUEFMT-1.7, ISSUEFMT-1.9, ISSUEFMT-2.1, ISSUEFMT-2.3, ISSUEFMT-2.4, ISSUEFMT-3.1, ISSUEFMT-3.2, ISSUEFMT-3.3, ISSUEFMT-3.4, ISSUEFMT-3.5, ISSUEFMT-3.7, ISSUEFMT-3.8, ISSUEFMT-3.9, ISSUEFMT-4.1, ISSUEFMT-4.2, ISSUEFMT-4.6, ISSUEFMT-4.8, ISSUEFMT-4.9, ISSUEFMT-5.1, ISSUEFMT-5.2_

---

### Task 2: A repo gets its field mapping

**Files:**
- Modify: `skills/setup/configure-repo/issue-tracker-followups.md`
- Modify: `skills/setup/configure-repo/SKILL.md`
- Modify: `skills/setup/configure-repo/TESTS.md`
- Modify: `skills/setup/configure-repo/eval.json`

**Reuse:** rung 2 — `skills/setup/configure-repo/issue-tracker-followups.md`, one more follow-up after Draft surface

**Interfaces:**
- Consumes: `## Issue fields` from Task 1
- Produces: a filled `Issue fields` table per tracker and owner type

**Depends-on:** Task 1

- [x] **Step 1: RED.** Two runs per model of `/configure-repo` on stubbed `gh` for an organization repo, a personal repo, and Linear. Expect an empty or guessed `Issue fields` table. Record verbatim.
- [x] **Step 2: Add the follow-up**: the mapping table from the design, the owner-type check, consent for label or option changes, and the label fallback.
- [x] **Step 3: GREEN.** Rerun. Expect the right row for each case, a named change with consent before any write, every existing question still asked, and the wayfinding operations still in the written file. Add `eval.json` entries citing `TESTS.md`.
- [x] **Step 4: Commit** `feat(configure-repo): map the four issue fields per tracker`.

_Requirements: ISSUEFMT-4.3, ISSUEFMT-4.4, ISSUEFMT-4.5, ISSUEFMT-4.7, ISSUEFMT-7.1, ISSUEFMT-7.2_

---

### Task 3: Published slices use the format

**Files:**
- Modify: `skills/track/publish-issues/SKILL.md`
- Create: `skills/track/publish-issues/TESTS.md`
- Create: `skills/track/publish-issues/eval.json`

**Reuse:** rung 2 — each skill's existing create step

**Interfaces:**
- Consumes: the writer sentence from Task 1
- Produces: slices with one state role each, and edges in the native relation

**Depends-on:** Task 1

- [x] **Step 1: RED.** Two runs per model of `/publish-issues` on an idea with two slices, the second blocked by the first, on a fixture with the new seed, with and without `--no-native-edges`. Expect the skill's own template and label rule to win over the seed. Record verbatim. If nothing fails, keep only the version bump's removal of duplicate text and say so.
- [x] **Step 2: Replace** the issue template, local template and marker lines with the writer sentence, and replace the frontier rule with the same state role for all slices, except local `.scratch/` files.
- [x] **Step 3: GREEN.** Rerun with `score.py`. Expect all PASS, one state role on each slice, the edge in the form the fixture supports, and no slice created before the operator approves the breakdown. Add `eval.json` entries citing `TESTS.md`.
- [x] **Step 4: Commit** `feat(publish-issues): follow the repo's issue format`.

_Requirements: ISSUEFMT-5.8, ISSUEFMT-7.3_

---

### Task 4: A plan's issue uses the format

**Files:**
- Modify: `skills/spec/plan-tasks/publish-recipe.md`
- Modify: `skills/spec/plan-tasks/SKILL.md`
- Modify: `skills/spec/plan-tasks/eval.json`
- Modify: `skills/spec/plan-tasks/TESTS.md`

**Reuse:** rung 2 — each skill's existing create step

**Interfaces:**
- Consumes: the writer sentence from Task 1; the record line format from Task 5
- Produces: the `covers:` field in `.skills/<CODE>/tickets.md`, read by Task 8

**Depends-on:** Task 1, Task 5

- [x] **Step 1: RED.** Two runs per model of publishing an approved plan onto an existing ticket with an operator-written Problem and estimate 2, on `shared` and `private`. Expect a lost Problem, a task checklist, or no revised estimate. Record verbatim.
- [x] **Step 2: Edit the recipe**: follow the format, keep Problem, drop the task checklist, revise the estimate unless the operator set it, `shaping` when not grabbable, and write `covers:` when private. Update eval id 9.
- [x] **Step 3: GREEN.** Rerun. On `shared` expect the `[CODE]` title and the trace lines last; on `private`, none of them and a `covers:` line. Expect exactly one issue.
- [x] **Step 4: Commit** `feat(plan-tasks): publish plans in the repo's issue format`.

_Requirements: ISSUEFMT-1.10, ISSUEFMT-2.2, ISSUEFMT-2.7, ISSUEFMT-3.6, ISSUEFMT-7.4_

---

### Task 5: An idea and a fix land in the format

**Files:**
- Modify: `skills/track/idea/SKILL.md`
- Modify: `skills/track/idea/TESTS.md`
- Modify: `skills/track/idea/eval.json`
- Modify: `skills/track/shape/SKILL.md`
- Modify: `skills/track/shape/TESTS.md`
- Modify: `skills/track/shape/eval.json`
- Modify: `templates/skills-ephemera-paths.md`
- Modify: `skills/track/refresh-roadmap-status/templates/skills-ephemera-paths.md`
- Modify: `skills/execution/build-in-waves/templates/skills-ephemera-paths.md`
- Modify: `skills/execution/build-inline/templates/skills-ephemera-paths.md`
- Modify: `skills/execution/build-by-story/templates/skills-ephemera-paths.md`
- Modify: `skills/spec/specify-behavior/templates/skills-ephemera-paths.md`

**Reuse:** rung 2 — each skill's existing create step; `.skills/<CODE>/tickets.md`, written today by `tracker-sync.md`, `shape` and `deliver-issues`

**Interfaces:**
- Consumes: the writer sentence from Task 1; `tools/tix`
- Produces: the record line format `<id> covers: <ids> road: <ROAD-N>`, first token the ID

**Depends-on:** Task 1

- [x] **Step 1: RED.** Two runs per model: `/idea Learners should get a weekly digest` to step 1, and `/shape` of an approved tier-1 fix, on `shared` and `private`. Expect words outside Problem, no priority or estimate, and `Requirements covered:` on `private`. Record verbatim.
- [x] **Step 2: Edit both skills**, and the promotion paragraph to append `tickets.md` lines when `.skills/<CODE>/` exists. Mirror with `--write`.
- [x] **Step 3: GREEN.** Rerun. Expect verbatim words under Problem, `Not decided yet` elsewhere, the shaping swap and frame comment intact, the waiting comment from `/shape` intact, the tier-1 line in the body where shared and in the record where private, and a `/shape` rewrite keeping an existing line's `road:`. Check that `land-branch` still takes every ID, by running its ticket step against a record with `covers:`.
- [x] **Step 4: Commit** `feat(track): file ideas and fixes in the repo's issue format`.

_Requirements: ISSUEFMT-1.8, ISSUEFMT-7.5, ISSUEFMT-7.6, ISSUEFMT-7.10_

---

### Task 6: Triage selects by state

**Files:**
- Modify: `skills/track/triage/SKILL.md`
- Modify: `skills/track/triage/agent-brief-template.md`
- Modify: `skills/track/triage/TESTS.md`
- Modify: `skills/track/triage/eval.json`

**Reuse:** rung 2 — the queue buckets already at `skills/track/triage/SKILL.md` "Showing the queue"

**Interfaces:**
- Consumes: the state roles from `docs/agents/triage-labels.md`
- Produces: none

**Depends-on:** Task 1

- [x] **Step 1: RED.** Two runs per model on a queue of five: a stranger's bug with no label, a category-only issue, `needs-triage`, `needs-info` with a new reply, and a `shaping` ticket with no marker. Expect the last one triaged, the marker line in the comment, and type names in the brief. Record verbatim.
- [x] **Step 2: Replace** the Scope rule with the state rule, delete the comment marker, and rewrite the brief's fields to the issue's sections without `Key interfaces`.
- [x] **Step 3: GREEN.** Rerun. Expect the first four in scope, the fifth skipped with a reason, and no marker. Run "move #42 to ready-for-agent": expect a direct state change.
- [x] **Step 4: Commit** `feat(triage): select by state and brief in the issue format`.

_Requirements: ISSUEFMT-1.11, ISSUEFMT-6.2, ISSUEFMT-6.3, ISSUEFMT-6.4, ISSUEFMT-6.5, ISSUEFMT-6.6_

---

### Task 7: A roadmap claim follows reach

**Files:**
- Modify: `skills/spec/specify-behavior/roadmap-bind.md`
- Modify: `skills/spec/specify-behavior/SKILL.md`
- Modify: `skills/spec/specify-behavior/TESTS.md`
- Test: `skills/track/chart-progress/scripts/test_lanes.py`

**Reuse:** rung 2 — `skills/spec/specify-behavior/roadmap-bind.md` claim check

**Interfaces:**
- Consumes: the record line format from Task 5
- Produces: `road:` in `.skills/<CODE>/tickets.md`

**Depends-on:** Task 5

- [x] **Step 1: RED.** Two runs per model of writing requirements for a `ROAD-6` item on `private` and `shared`, each with and without an existing ticket, and once with `ROAD-6` already assigned to alice. Expect `ROAD-6` in the title on `private`, and a duplicate on rerun. Record verbatim.
- [x] **Step 2: Add the private branch**, and make the create follow the format with state `shaping`.
- [x] **Step 3: GREEN.** Rerun. On `private` expect no `ROAD-N` on the tracker, a `road:` record, no second ticket on rerun, and a stop on alice's ticket. On `shared` expect today's claim. Expect a stop naming `/configure-repo` on `--no-format`. Publish from a signed Notion draft listing one ticket: expect that ticket alone. Run `python3 skills/track/chart-progress/scripts/test_lanes.py`, expect `OK`.
- [x] **Step 4: Commit** `feat(specify-behavior): claim a roadmap item by reach`.

_Requirements: ISSUEFMT-2.5, ISSUEFMT-2.6, ISSUEFMT-7.12_

---

### Task 8: The board reads records and native edges

**Files:**
- Modify: `skills/track/board/scripts/board.py`
- Modify: `skills/track/board/SKILL.md`
- Modify: `skills/track/board/TESTS.md`
- Test: `skills/track/board/scripts/test_board.py`

**Reuse:** rung 2 — `covered()`, `code_of()` and the blocked calculation in `skills/track/board/scripts/board.py`

**Interfaces:**
- Consumes: the record line format from Task 5
- Produces: `records() -> dict[str, dict]`, ticket ID with any leading `#` stripped mapped to `{"code": str | None, "covers": list[str]}`, with `code` None for a `_pending-*` directory

**Depends-on:** Task 5

- [x] **Step 1: Write the tests** in `test_board.py`, each building in its tempdir whichever of `docs/agents/triage-labels.md`, `docs/specs/catalog/<domain>.md`, the feature's `requirements.md`, `design.md` and `tasks.md`, and `.skills/<CODE>/tickets.md` it needs, one per behavior:
  - a ticket with `blockedBy: {"nodes": [{"number": 1}]}` and #1 open prints `blocked by #1`;
  - the same with #1 closed prints no block;
  - a ticket whose body says `Blocked by: #1` still prints it;
  - a private ticket with no `[CODE]` and a record in `.skills/QUOTA/tickets.md`, feature `Approved` in the catalog, prints `eligible`;
  - a private bug whose record `covers:` a fix and its guard prints `eligible, tier-1 fix`;
  - a shared bug with `Requirements covered:` prints `eligible, tier-1 fix`;
  - a record under `.skills/_pending-x/` resolves no feature;
  - an issues file with no `blockedBy` key prints every section;
  - with a stub `gh` on `PATH` that rejects `blockedBy`, a run with no `--issues` still lists the tickets.
- [x] **Step 2: Run** `python3 skills/track/board/scripts/test_board.py`. Expect these to fail on missing output: the open native edge, the two private records, and the `gh` retry. Expect these guards to pass today: the closed native edge, the `Blocked by:` line, the shared bug, the `_pending-x` record and the no-key file.
- [x] **Step 3: Implement** `records()`, the fallback in `covered()` and `code_of()`, the union in the blocked calculation filtered through `open_nums`, and `blockedBy` in the `gh` call, retrying without it on failure.
- [x] **Step 4: Run** the same command. Expect `OK` with pristine output.
- [x] **Step 5: Commit** `feat(board): read native edges and private ticket records`.

_Requirements: ISSUEFMT-2.8, ISSUEFMT-2.9, ISSUEFMT-5.3, ISSUEFMT-7.9_

---

### Task 9: A build respects assignee and blockers

**Files:**
- Modify: `skills/execution/execute-common/tracker-sync.md`
- Modify: `skills/execution/execute-common/SKILL.md`
- Modify: `skills/execution/execute-common/TESTS.md`
- Modify: `skills/execution/deliver-issues/SKILL.md`
- Modify: `skills/execution/deliver-issues/TESTS.md`
- Modify: `skills/track/sweep-backlog/SKILL.md`
- Modify: `skills/track/sweep-backlog/TESTS.md`

**Reuse:** rung 2 — `skills/execution/execute-common/tracker-sync.md`, `skills/execution/deliver-issues/SKILL.md`

**Interfaces:**
- Consumes: `records()` semantics from Task 8, by the same record line format
- Produces: a final-table row in `deliver-issues` for a ticket held back

**Depends-on:** Task 8

- [x] **Step 1: RED.** Two runs per model: a build on a ticket assigned to alice; `/go` on a board with one ticket assigned to alice, one with a native edge to an open ticket outside the run, one private tier-1 fix, and two eligible tickets where the higher number blocks the lower; `/sweep-backlog` with a native edge. Expect silent reassignment, a blocked ticket built, the fix sent back, and the pair built in number order. Record verbatim.
- [x] **Step 2: Add** the assignee and blocker checks to `tracker-sync.md`, the record read, edge order and held-back rows to `deliver-issues`, native edges to `sweep-backlog`, and to both writers of the record, keeping a line's existing fields.
- [x] **Step 3: GREEN.** Rerun. Expect a question on alice's ticket; under `/go`, her ticket and the blocked ticket unbuilt with a row each, and the rest delivered; the fix delivered; the pair built blocker first; the unassigned ticket claimed with no question and its record line keeping `covers:`; and `/sweep-backlog` classing the edge `blocked` and writing nothing before the answer.
- [x] **Step 4: Commit** `feat(execution): hold back tickets owned by others or blocked`.

_Requirements: ISSUEFMT-3.10, ISSUEFMT-3.11, ISSUEFMT-5.4, ISSUEFMT-5.5, ISSUEFMT-5.7, ISSUEFMT-7.7, ISSUEFMT-7.8_

---

### Task 10: Docs agree and the whole set is green

**Files:**
- Modify: `AGENTS.md`
- Modify: `docs/guide/skills/publish-issues.md`
- Modify: `docs/guide/skills/triage.md`
- Modify: `docs/guide/skills/plan-tasks.md`
- Modify: `docs/guide/skills/idea.md`
- Modify: `docs/guide/skills/shape.md`
- Modify: `docs/guide/skills/sweep-backlog.md`
- Modify: `docs/guide/skills/deliver-issues.md`
- Modify: `docs/guide/skills/board.md`
- Modify: `docs/guide/skills/configure-repo.md`
- Modify: `docs/guide/skills/specify-behavior.md`
- Modify: `docs/guide/skills/chart-progress.md`
- Modify: `docs/guide/process/ship-and-maintain.md`
- Modify: `docs/guide/process/specification.md`
- Modify: `docs/guide/concepts/requirement-ids.md`
- Modify: `docs/guide/concepts/traceability.md`
- Modify: `docs/guide/methodology/overview.md`

**Reuse:** rung 2 — `scripts/qa-set.py`, `test_board.py`, `test_lanes.py`, `TESTS.md` per skill

**Interfaces:**
- Consumes: the final rules from Tasks 1 to 9
- Produces: none

**Depends-on:** Task 2, Task 3, Task 4, Task 6, Task 7, Task 9

- [x] **Step 1: Find stale statements.** Run `grep -rnE --exclude=TESTS.md --exclude=eval.json "drafted by AI|generated by AI during|Key interfaces|frontier" AGENTS.md docs/guide skills templates` and expect only `plan-tasks` Step 5 uses of frontier that this change did not alter, and the local `.scratch/` rule. Run the same with `Requirements covered` and expect only lines stating it as shared-reach behavior. Each other hit is an edit.
- [x] **Step 2: Reword** each hit and the section 4 table in `AGENTS.md` to the reach rule.
- [x] **Step 3: Check `show-run-status`.** On a fixture from `make.sh /tmp/if-rs shared --local` with a `.scratch/` issue titled `[QUOTA] …`, run `bash <repo>/skills/track/show-run-status/scripts/collect.sh QUOTA` from the fixture. Expect the `tracker` section to list that file. This reads the local path, since the script calls real `gh` otherwise.
- [x] **Step 4: Whole check.** Run `python3 scripts/qa-set.py`, `python3 skills/track/board/scripts/test_board.py` and `python3 skills/track/chart-progress/scripts/test_lanes.py`. Expect zero failures.
- [x] **Step 5: Commit** `docs: state the one issue format everywhere`.

_Requirements: ISSUEFMT-7.11, ISSUEFMT-8.1_

---

## Deviations from this plan

Recorded while building. Evidence per skill is in each `TESTS.md`.

- **Batched prompts.** Task 1 ran A to F as one prompt per run, not one run per prompt, to keep the run count down. Later tasks ran one sonnet and one haiku per cell, not two each.
- **Text not written, because the baseline did not fail:** `/idea`'s create step, `/sweep-backlog`'s native edges, the assignee guard in `tracker-sync.md`, the Linear row in the follow-up, GitLab and local follow-up cells beyond one line. The requirements hold on the seed or unprompted.
- **`skills-ephemera-paths.md` unedited.** Its promotion rule already says to merge. Task 5's six files were not touched.
- **Rubric row added.** `high` also covers a deadline this week, after the same deadline split `high` and `medium` across runs.
- **ISSUEFMT-1.4 in practice.** A bug's title names what goes wrong, as all five surveyed bug templates do, and the seed says so.
- **Not proven.**
  - The claim's create path in GREEN: the permission classifier denied `tools/tix create` in 2 of 2 runs. It rests on RED.
  - `setIssueFieldValue`: the follow-up uses it for organization repos, and no write has run. `createIssue(issueFields:)` was proven on `KlyntLabs/klynt` #285.
  - `notion-draft.md` was not run. It is unedited.
