# Design: One issue format

Feature code: ISSUEFMT
Status: Approved
Date: 2026-11-01
Requirements: ./2026-11-01-issue-format.md

## Context

Five skills write issues in five shapes, and "never file paths" is repeated in four places. In
klynt, 28 of 65 issues carry source paths and only 1 of those has a skill marker. In zroute, 25
of the latest 40 issues name no skill as their writer. So most of the drift happens outside the
skills, and another paragraph inside a skill would not reach it.

The binding constraint is that a skill folder must stand alone: `scripts/lint-cross-folder.py`
fails any `../` reference except `execute-common`. That rules out a shared template file inside
one skill. It also rules out a new shared skill: `publish-issues` and `idea` could name it, but an
agent writing with no skill loaded would never reach it.

Every writer already reads one runtime file, `docs/agents/issue-tracker.md`, and the agent-skills
block in the consuming repo already points at it. So the format lives there. Skills keep only
what is specific to them and send the writer to that section. The cost is that an adopting repo
needs its config regenerated, which ISSUEFMT-4.9 makes explicit.

Parsers shape the rest. `board.py`, `deliver-issues` and `triage` read body text, so removing a
line means giving each reader another source. That source is the ticket's state for `triage`,
`.skills/<CODE>/tickets.md` for private feature joins, and native edges for blocking.

No catalog exists in this repo, so `load-subgraph` has nothing to retrieve: no overlap, and no
OWNS coverage to report. No `docs/architecture/` spine and no standing system docs apply.

## Decisions

1. The format lives in `docs/agents/issue-tracker.md`, seeded from `templates/agents/issue-tracker.md`. Skills do not restate it.
2. Reach is `git check-ignore -q`, on `docs/specs/_probe/requirements.md` for specs and `docs/roadmap/INDEX.md` for the roadmap, judged separately. `INDEX.md` is no test for specs: `skills/setup/configure-repo/templates/gitignore-index-only.snippet` ignores the spec directories and keeps it tracked. `git check-ignore` needs no existing file.
3. Assignee defaults to the operator; blank only on the operator's word. Taking over someone else's ticket needs a yes.
4. The agent sets priority and estimate at create from written rubrics. The estimate is revised when a plan is approved.
5. GitHub organizations use issue fields. Personal repos use `priority:*` and `size:*` labels. Linear uses native fields. Local trackers use lines in the file.
6. `.skills/<CODE>/tickets.md` keeps the ticket ID as each line's first token and adds optional `covers:` and `road:` fields.
7. No line in any issue or comment states who or what wrote it.
8. `triage` selects by state alone.
9. `lanes.py` stays as it is. In a repo with a private roadmap it reports items as unclaimed, because only that machine reads the file and title claims no longer exist there.

## Architecture

Vocabulary for every section below: **module**, **interface**, **implementation**, **seam**.

### Issue format section

Satisfies: ISSUEFMT-1.1, ISSUEFMT-1.2, ISSUEFMT-1.3, ISSUEFMT-1.4, ISSUEFMT-1.5, ISSUEFMT-1.6, ISSUEFMT-1.7, ISSUEFMT-1.9, ISSUEFMT-2.1, ISSUEFMT-2.3, ISSUEFMT-2.4, ISSUEFMT-3.1, ISSUEFMT-3.2, ISSUEFMT-3.3, ISSUEFMT-3.4, ISSUEFMT-3.5, ISSUEFMT-3.7, ISSUEFMT-3.8, ISSUEFMT-3.9, ISSUEFMT-4.1, ISSUEFMT-4.2, ISSUEFMT-4.6, ISSUEFMT-4.8, ISSUEFMT-4.9, ISSUEFMT-5.1, ISSUEFMT-5.2
Reuse: rung 2 — `templates/agents/issue-tracker.md` and its mirror, kept in sync by `scripts/lint-skill-templates.py --write`
Surface:
- `issue-tracker.md` Conventions, the AI marker rules: **replace**, deleted.
- Every skill reading that file: **replace**, each gets the sentence below.
- `templates/agents/issue-tracker.md` in klynt, zroute and raki, already generated: **compat**, unaffected until each repo re-runs `/configure-repo`. The follow-up is the adoption step, which ISSUEFMT-4.9 forces.
Interface: two new sections, `## Issue format` and `## Issue fields`. A writer knows one sentence: "Write it as `docs/agents/issue-tracker.md` **Issue format** says. No such section: name `/configure-repo`, show the draft, create nothing."
Depth: n/a — extends `templates/agents/issue-tracker.md`
Locality: extend the template. Writers shrink.

Draft of the seeded text:

```markdown
## Issue format

Any writer follows this, with or without a skill loaded.

**Title:** the outcome it delivers. No `Task N`, no `feat:`.

**Feature:** ## Problem · ## Outcome · ## Acceptance (checkable items) · ## Out of scope
**Bug:** ## What happens · ## Expected · ## How to reproduce · ## Evidence
Not reproduced: say so under How to reproduce. In `shaping`, an empty section reads `Not decided yet`.

**Keep out:** source paths, line numbers, `Task N` items, implementation steps, and any line
saying who or what wrote it. Bugs may quote errors, versions, trace IDs and a minimal reproduction.

**Internal IDs follow reach.** `git check-ignore -q docs/specs/_probe/requirements.md` exit 0 means specs are
private: no feature code, requirement ID or spec path anywhere on the tracker. Same check on
`docs/roadmap/INDEX.md` for `ROAD-N` and `MILE-N`. Shared specs: `[CODE]` title for a plan's issue,
with `Requirements covered:`, `Plan:` and `Roadmap:` as the last lines. Shared roadmap: `ROAD-N`
leads the title of its claim.

**Fill all four, using the `Issue fields` table:**
- Assignee: whom the operator named, else the operator. Blank only on the operator's word; say so.
- Status: one state role and one category role from `triage-labels.md`.
- Priority: the operator's word, else `## Focus`, else the rubric.
- Estimate: the operator's word, else the rubric.

| Priority | When | | Estimate | Complexity |
<both rubrics from ISSUEFMT story 3>

**Blocking:** the tracker's native relation when `Issue fields` names one, else one line: `Blocked by: #N, #M`.

**After creating:** read the issue back. Reply with its ID, assignee, priority, estimate and status.
A field that would not write: keep the issue, name the field, put nothing in the body.

## Issue fields

| Field | Write | Read |
|---|---|---|
| Assignee | … | … |
| Status | … | … |
| Priority | … | … |
| Estimate | … | … |
| Blocking | … | … |
```

The agent-skills block gains one line: "Creating an issue, with or without a skill: read `docs/agents/issue-tracker.md` **Issue format** first."

### configure-repo mapping

Satisfies: ISSUEFMT-4.3, ISSUEFMT-4.4, ISSUEFMT-4.5, ISSUEFMT-4.7, ISSUEFMT-7.1, ISSUEFMT-7.2
Reuse: rung 2 — `skills/setup/configure-repo/issue-tracker-followups.md`, one more follow-up after Draft surface
Interface: `/configure-repo` fills the `Issue fields` table for the chosen tracker.
Depth: n/a — extends `issue-tracker-followups.md`
Locality: extend the followups file. `SKILL.md` Done-when gains one word.

| Tracker | Priority and estimate | Blocking | Read |
|---|---|---|---|
| Linear | `save_issue` `priority`, `estimate` | `save_issue` `blockedBy` | `get_issue` |
| GitHub, organization | `createIssue` `issueFields`, global IDs from GraphQL `organization.issueFields` (the REST list gives only numeric option IDs, which the mutation rejects) | `gh issue create --blocked-by` | `issue_field_values` on the REST issue |
| GitHub, personal | `--label priority:<p> --label size:<n>` | `gh issue create --blocked-by` | `gh issue view --json labels,blockedBy` |
| GitLab | Labels, as GitHub personal | Unverified, `Blocked by:` line until checked | `glab issue view` |
| Local | `Priority:`, `Estimate:` lines | `Blocked by:` line | The file |

Owner type comes from `gh repo view --json isInOrganization`. An organization whose `Effort`
options are not 1, 2, 3, 5, 8 gets the change named for the operator, because it reaches every repo
in that organization. Without consent, the estimate maps to `size:*` labels on that repo.

The `createIssue` shape is proven: a run on `KlyntLabs/klynt` set `Priority` at create with `fieldId` and the option's global ID, using a token holding only `repo` and `read:org`. REST `issue_field_values` read back `{"issue_field_name":"Priority","single_select_option":{"name":"Medium"}}`.

### Writers

Satisfies: ISSUEFMT-1.8, ISSUEFMT-1.10, ISSUEFMT-1.11, ISSUEFMT-2.2, ISSUEFMT-3.6, ISSUEFMT-5.8, ISSUEFMT-7.3, ISSUEFMT-7.4, ISSUEFMT-7.5, ISSUEFMT-7.6, ISSUEFMT-7.12
Reuse: rung 2 — each skill's existing create step
Surface:
- `publish-issues` issue and local templates, marker line: **replace**.
- `publish-recipe.md` body list and marker: **replace**, the optional task checklist is deleted.
- `agent-brief-template.md` marker and `Key interfaces`: **replace**.
- `plan-tasks/eval.json` id 9, "first line is still the drafted-by-AI marker", and `triage/eval.json` scope assertions: **replace**.
- `notion-draft.md` ticket list: **frozen**, built around. It is a sign-off list on a Notion page, not a tracker body, and the tickets it lists follow the format when published.
Interface: the writer sentence from the first section, plus what is specific to that skill.
Depth: n/a — extends each skill
Locality: extend, with net shrink in `publish-issues`.

- `idea`: operator's words under `## Problem`; other sections `Not decided yet`; priority and estimate at create.
- `plan-tasks`: updates in place keeping `## Problem`; revises estimate from the plan; `Requirements covered:`, `Plan:`, `Roadmap:` only where shared. An issue not yet grabbable gets `shaping`, never no state role.
- `publish-issues`: every slice gets the same state role, and the edge gates it. The frontier rule goes, except on local `.scratch/` files, whose `Status:` keeps `blocked`.
- `triage`: the brief uses the sections of the issue's kind, as a comment.
- `shape`: the tier-1 line goes in the body where shared, in the ticket record where private.

### Triage selection

Satisfies: ISSUEFMT-6.2, ISSUEFMT-6.3, ISSUEFMT-6.4, ISSUEFMT-6.5, ISSUEFMT-6.6
Reuse: rung 2 — the queue buckets already at `skills/track/triage/SKILL.md` "Showing the queue"
Surface: `triage` Scope rule, reading `Requirements covered:` and the marker: **replace**.
Interface: an issue is in scope when it has no state role, or is `needs-triage`, or `needs-info` with reporter activity. This holds because every skill-written issue now carries a state role from birth (ISSUEFMT-3.3).
Depth: n/a — extends `triage`
Locality: replace one paragraph.

### Ticket record

Satisfies: ISSUEFMT-2.7, ISSUEFMT-7.10
Reuse: rung 2 — `.skills/<CODE>/tickets.md`, written today by `tracker-sync.md`, `shape` and `deliver-issues`
Surface:
- `land-branch/tickets.md` reading "every ID": **compat**, reads the first token, and old bare-ID files stay valid. No removal needed, since the new fields are optional.
- `tracker-sync.md`, `shape`, `deliver-issues` writing it: **replace**, they keep a line's fields when they rewrite it.
- `skills-ephemera-paths.md` promotion: **replace**, when `.skills/<CODE>/` already exists, `tickets.md` lines from `_pending-<slug>` are appended instead of lost.
Interface: one line per ticket. The first token is the ID in the tracker's own form (`#12`, `ZR-221`), compared with any leading `#` stripped; `covers:` and `road:` are optional. Written by `plan-tasks` and `shape` for `covers:`, and by `idea` and `roadmap-bind` for `road:`.
```
ZR-221 covers: CCGPT-1.1, CCGPT-1.2 road: ROAD-6
```
Depth: n/a — extends `.skills/<CODE>/tickets.md`
Locality: extend. `.skills/_pending-<slug>/tickets.md` serves a ticket filed before a code exists, and promotion carries it. Readers take a feature code only from a directory that is not `_pending-*`.

### Roadmap claim by reach

Satisfies: ISSUEFMT-2.5, ISSUEFMT-2.6
Reuse: rung 2 — `skills/spec/specify-behavior/roadmap-bind.md` claim check
Surface:
- `idea` step 3, `ROAD-N` in the title: **replace**, only where the roadmap is shared. Private: `road:` goes in `.skills/_pending-<slug>/tickets.md`.
- `roadmap-bind.md` create step as a writer: **replace**.
- `lanes.py` `claims_from_issues`: **compat**, no edit. It reads titles on shared roadmaps. Private roadmaps show unclaimed, per Decision 9, with no follow-up because no shared reader exists.
- `test_lanes.py`: no edit.
Interface: shared roadmap, as today. Private roadmap, `grep -l "road: ROAD-N" .skills/*/tickets.md`. Found: read that ticket's assignee from the tracker, and the same three assignee branches apply. None: create and record. Either way the create follows **Issue format**, with state `shaping` and `Not decided yet` in open sections. A repo with no such section stops here with the ISSUEFMT-4.9 message, naming `/configure-repo`, which is why adoption ships with the release.
Depth: n/a — extends `roadmap-bind.md`
Locality: extend, one branch at the top of the claim check.

### Board and delivery readers

Satisfies: ISSUEFMT-2.8, ISSUEFMT-2.9, ISSUEFMT-5.3, ISSUEFMT-5.4, ISSUEFMT-5.5, ISSUEFMT-5.7, ISSUEFMT-7.8, ISSUEFMT-7.9
Reuse: rung 2 — `covered()`, `code_of()` and the blocked calculation in `skills/track/board/scripts/board.py`
Surface:
- `board.py` `covered`, `code_of`: **replace**, body first, then the record.
- `board.py:205` blocking: **replace**, the union of `blockedBy.nodes[].number` and `Blocked by:` text, still filtered through `open_nums` because `nodes` includes closed issues.
- `gh issue list --json` in `board.py`'s docstring and `load` call: **replace**, adds `blockedBy`, and retries without it when an older `gh` rejects the field.
- Issue files with no `blockedBy` key from other trackers: **compat**, treated as no native edges. A tracker's ops may add the key, so nothing to remove.
- `test_board.py`: **replace**, extended.
- `deliver-issues` and `sweep-backlog` `Blocked by:` reads: **replace**, native edge or text line.
- `deliver-issues` eligibility: **replace**. Private: feature, covered IDs and tier-1 come from `.skills/<CODE>/tickets.md`. A ticket with an open blocker outside this run stays unbuilt with a row in the final table.
- `tracker-sync.md` claim of a named ticket: **replace**, reads blockers first and reports an open one.
- `show-run-status/scripts/collect.sh`: **frozen**, built around. It searches for the code and finds nothing in a private repo, which is what private means.
Interface: `board.py` flags and output are unchanged.
Depth: n/a — extends `board.py`
Locality: extend. One new function `records()` globs `.skills/*/tickets.md`.

### Claim guard

Satisfies: ISSUEFMT-3.10, ISSUEFMT-3.11, ISSUEFMT-7.7
Reuse: rung 2 — `skills/execution/execute-common/tracker-sync.md`, `skills/execution/deliver-issues/SKILL.md`
Surface: `tracker-sync.md` "Assign it to the session's tracker user": **replace**, with a check first.
Interface: a ticket assigned to someone else gets a question. In `deliver-issues`, it stays untouched and gets a row in the final table.
Depth: n/a — extends `tracker-sync.md`
Locality: one sentence in each.

### Verification and docs

Infrastructure for the requirements above, plus:

Satisfies: ISSUEFMT-7.11, ISSUEFMT-8.1
Reuse: rung 2 — `scripts/qa-set.py`, `test_board.py`, `test_lanes.py`, `TESTS.md` per skill
Surface: `AGENTS.md` section 4 table and "Agent skills" section; `docs/guide/skills/{publish-issues,triage,plan-tasks,idea,shape,sweep-backlog,deliver-issues,board,configure-repo}.md`; `docs/guide/process/ship-and-maintain.md`; `docs/guide/process/specification.md`; the title-claim wording in `docs/guide/skills/{specify-behavior,chart-progress}.md`; `docs/guide/concepts/{requirement-ids,traceability}.md`; `docs/guide/methodology/overview.md`: **replace**, reworded where they state the old rule.
Interface: no new script.
Depth: n/a — extends the existing checks
Locality: docs only, plus version bumps and `TESTS.md` entries per edited skill.

## Seams for testing

No new seams. Skill text is proven by RED and GREEN scenario runs on Sonnet and Haiku, per AGENTS.md section 7, on a stub tracker, since the harness denies `gh issue create` to test agents.

| Seam | Kind | Covers |
|---|---|---|
| `board.py --issues --prs` through `test_board.py` | unit | ISSUEFMT-2.8, 2.9, 5.3, 7.9 |
| `test_lanes.py` unchanged and passing | unit | ISSUEFMT-2.5 |
| Scenario: an agent with no skill is asked to file a bug and a feature | integration | ISSUEFMT-1.1–1.7, 3.1–3.5, 3.7–3.9, 4.8, 4.9, 5.1, 5.2 |
| Scenario: `/idea`, `/publish-issues`, `plan-tasks` publish, `/shape` tier 1, on a shared and a private fixture | integration | ISSUEFMT-1.8–1.10, 2.1–2.7, 3.6, 5.8, 7.3–7.6, 7.10, 7.12 |
| Scenario: `/triage` on a mixed queue | integration | ISSUEFMT-1.11, 6.2–6.6 |
| Scenario: `/configure-repo` per owner type and tracker | integration | ISSUEFMT-4.1–4.7, 7.1, 7.2 |
| Scenario: a build and `/go` on a ticket assigned to someone else | integration | ISSUEFMT-3.10, 3.11, 7.7 |
| Scenario: `/go` order and `/sweep-backlog` with native edges | integration | ISSUEFMT-5.4, 5.5, 5.7, 7.8 |
| `collect.sh` run on a shared fixture | integration | ISSUEFMT-7.11 |
| `scripts/qa-set.py` | integration | ISSUEFMT-8.1 |

## Coverage check

Every live ID in the requirements appears in exactly one `Satisfies:` line. ISSUEFMT-5.6 and ISSUEFMT-6.1 are struck and unmapped, superseded by ISSUEFMT-5.8 and ISSUEFMT-6.6.
