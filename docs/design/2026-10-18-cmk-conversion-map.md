# cmk conversion map

Date: 2026-10-18. Task T22 of `2026-10-18-survey-upgrade-plan.md`. Branch `feat/survey-upgrade`.

## 1. What this is

This is the input for porting the proven jdk changes into cmk (`~/Developer/work/ai-devkit`).
It maps each jdk task T1 to T23 to a cmk target, says what carries over, and says what
conflicts with cmk's tracker-first model.

How to read it:

- Section 2 is the map, one row per task.
- Section 3 lists the scripts jdk added and where cmk could keep them.
- Section 4 lists what must be re-tested on cmk before any no-op is trusted there.
- Section 5 lists open questions.

The evidence rule:

- Port behavior only where jdk has a RED that failed and a GREEN that passed. The proof is in
  that skill's `TESTS.md`.
- A jdk tested no-op is a claim to re-test on cmk. It is not something to port. cmk has a
  different model (tracker-first, Linear, unattended pipeline), so the same prompt may fail
  there.
- Where jdk shipped nothing, nothing is ported. Only a re-test is owed.

Facts about cmk used below (all read from the files named):

- cmk is tracker-first. The tracker is the delivery ledger (`skills/delivery-pipeline/SKILL.md`,
  `skills/delivery-workflow/SKILL.md`). Linear specifics sit in one `references/linear.md` per
  delivery skill.
- cmk runs with no human gates. "Human gates are suppressed ... decide and record"
  (`skills/delivery-pipeline/SKILL.md`, § Working with superpowers). Contestable items are
  brought to the operator only when asked up front (`skills/delivery-pipeline/references/engineering-principles.md`, § Dispositions).
- cmk specs and plans are git-ignored scratch. Durable docs live in `docs/design/` and
  `docs/requirements/` (`skills/delivery-spec-plan/SKILL.md`, `skills/delivery-pipeline/SKILL.md`).
- cmk keeps run state in `docs/plans/<issue>-run-notes.md` (fields only) and a phase 3 ledger
  keyed `Task <N>:`. jdk keeps `.skills/<CODE>/progress.md`. These are different shapes.
- jdk is already tracker-neutral in places. `land-branch/tickets.md` reads
  `docs/agents/issue-tracker.md` and handles local, GitHub and Linear. The `.scratch/` tickets
  and `docs/specs/catalog/` are jdk's consuming-repo layout, not Linear.
- cmk has no `docs/specs/catalog/` and no feature CODE. Its unit of work is a tracker issue.

## 2. The map

Legend for "jdk result": shipped (skill@version), tested no-op (record file), deferred, not done.
All jdk paths are under `~/Developer/skills/`. All cmk paths are under `~/Developer/work/ai-devkit/`.

| Task | jdk result | cmk target | What carries over | What conflicts with cmk |
|---|---|---|---|---|
| T0.1 Roster and fixture | done (harness, not a skill). Fixture at `~/Developer/skill-fixtures/`, headless runner `run-headless.sh` | none | The method: weakest model plus sonnet, fresh fixture per run, scored by artifact diff. cmk needs its own fixture on Linear. | The jdk fixture (`harbor-ledger`, `.scratch/` tracker) is not a Linear fixture. cmk has `eval.json` in 8 non-delivery skills and none in delivery (`docs/ai/skills/conventions.md`, § Where). |
| T1 Autonomy policy block | closed, not shipped. Plan: "T1 does not ship as a block". Only one field survived: optional `Language` line in `templates/agents/project.md` (with T5) | re-test only | Nothing as a block. The idea of a per-repo policy slot only returns field by field (T4, T5, T6). | cmk has no `docs/agents/project.md` template that I found. Where cmk keeps per-repo policy is unclear. Check `skills/agent-instructions/SKILL.md` and `skills/repo-setup/SKILL.md`. |
| T2 Propose mode at the issue creator | tested no-op, 6/6. `docs/design/2026-10-18-tracker-writes-no-op.md` | re-test only, on `skills/delivery-intake/` and `skills/discover-efforts/` | Nothing. | The jdk RED used a local `.scratch/` tracker. The record says to re-run on a Linear fixture (see § 4). cmk intake creates and edits issues as part of the pipeline, so cmk may fail where jdk complied. |
| T3a Pending ticket sign-off | tested no-op, 12/12 (same record, follow-up section) | re-test only | Nothing. | Same Linear caveat. cmk's `references/linear.md` files govern Linear writes. A sign-off role has no cmk home yet. |
| T3b Milestone sign-off | tested no-op, 6/6 (same record) | re-test only | Nothing. | jdk tested MILE-2 in `docs/roadmap/INDEX.md`. cmk has no roadmap file. Linear milestones or projects would be the surface. unclear, check `skills/discover-efforts/SKILL.md`. |
| T3c Notion draft surface | deferred, not tested | none | Nothing. | Needs a Notion MCP server and open decision 3 in the plan. Skip. |
| T4 Batched decisions | tested no-op, 6/6 on `build-inline` only. `docs/design/2026-10-18-batched-decisions-no-op.md` | re-test only, on `skills/delivery-pipeline/` and `skills/delivery-pipeline/references/engineering-principles.md` | Nothing. | cmk default is already "decide, record, tell the operator in one PR line" with no stop. That is the opposite pole from jdk's one-decision-per-message. `build-in-waves` and an interactive session were not tested in jdk. |
| T5 Language policy | shipped: `skills/review/speak-outer/SKILL.md` @1.3.0, § Language. Evidence: `skills/review/speak-outer/TESTS.md`. | no `speak-outer` in cmk. Nearest homes: `skills/delivery-ship/` (PR text, `references/linear.md`) and `skills/delivery-workflow/references/pr-traceability.md`. Or a new small cmk skill. Decide in § 5. | The rule: chat in the operator's language, PR bodies, commits and tracker comments in English. The failure that was real: a ticket comment followed the thread into Vietnamese (5/5 RED). Port the ticket-comment case first. | cmk has no language rule anywhere (grep of `skills/delivery-*` found none). cmk's tracker writes go through Linear MCP comments, so test that surface, not a `.scratch/` file. The optional `Language` line in jdk's `project.md` has no cmk home. |
| T6 Host-level concurrency | tested no-op on jdk, 12/12. `docs/design/2026-10-18-host-concurrency-no-op.md`. Plan note: "The cap belongs in the cmk port." | `skills/delivery-pipeline/references/worktree-wave-execution.md` (already says "wave width is chosen against host capacity", line ~109) and `skills/delivery-pipeline/references/cluster-mode.md` | Nothing proven. The record says jdk lacks parallel dispatch in the tested runner, so the test did not exercise the cap. Side finding is jdk-only: haiku builds inline instead of dispatching (fixed in `build-in-waves` 2.3.0 and 2.4.0, T8). | cmk does dispatch waves in parallel worktrees, so the RED may fail on cmk. This is a real RED to run, not a port. The jdk design (slot directory `~/.cache/jdk/slots/`) was never built. |
| T7 Run status | shipped: `skills/track/show-run-status/SKILL.md` @1.0.0 plus `scripts/collect.sh`. Evidence: `skills/track/show-run-status/TESTS.md` (RED parked decision missed 2/6, unpushed commit 2/6, stale ticket 5/6; GREEN 6/6). | new cmk skill (user-invoked) or a section in `skills/delivery-pipeline/` | The recipe: one fixed collector pass over every source, sections always print so a missing source shows as missing, then the six facts. Rewrite the collector's source list for cmk. | `collect.sh` reads `.skills/<CODE>/progress.md`, `docs/specs/catalog/*.md` and `tasks.md`. None exist in cmk. cmk sources are `docs/plans/<issue>-run-notes.md`, the phase 3 ledger, Linear issue and relations, `gh pr view` and `gh pr checks`. The tracker read becomes a Linear MCP call, which a bash script cannot make. unclear how a cmk script would reach Linear. See § 3. |
| T8 Operator amendment | shipped: `skills/track/reroute-plan/SKILL.md` @1.1.0 (§ Operator amendment, REQUIRED "Check this wording" block) and `skills/execution/build-in-waves/SKILL.md` @2.4.0 (pointer). Evidence: `skills/track/reroute-plan/TESTS.md`, `skills/execution/build-in-waves/TESTS.md`. | no `reroute-plan` in cmk. Nearest: `skills/delivery-review/` (plan conflict owner, per `skills/delivery-pipeline/SKILL.md` line ~44) and `skills/delivery-pipeline/` phase 3. Likely a new cmk skill or a pipeline reference. | The rule: the operator's message is both approvals, so the stops do not fire. Before rewriting an `Approved` spec, quote the wording to change (the "Check this wording" block). Keep every untouched task's commits by adding new commits. | cmk has no `Approved` spec status in git (specs are git-ignored scratch). The "wording to check" lands in the Linear issue's acceptance criteria and the scratch spec. How an operator amends mid-run in cmk (a Linear comment? a chat message?) is unclear, check `skills/delivery-pipeline/references/cluster-mode.md`. |
| T9 Token and cost in close receipt | not done | none | Nothing. | jdk has not built it. Do not port. |
| T10 Ship-time guard | shipped: `skills/ship/land-branch/SKILL.md` @4.3.0, `prepare.md` § Ship guard, `scripts/ship-guard.sh`; fixed in @4.3.1. Evidence: `skills/ship/land-branch/TESTS.md` (RED 3 of 4 pushed files they had named as not belonging; GREEN 0 of 4). | `skills/delivery-ship/SKILL.md` (and a new `scripts/` or `references/` home, see § 3) | The script and the rule: stop on any flag and require literal confirmation per flag. Flags: `lockfile` (no manifest change), `generated`, `out-of-plan`, `behind-base`. | `out-of-plan` reads jdk's `tasks.md` File Structure and `**Files:**` blocks. cmk plans are scratch with `File scope:` per task (`skills/delivery-pipeline/SKILL.md`, phase 2 row). Re-point the parser at `File scope:`. cmk ship already checks traceability and gates (`skills/delivery-ship/SKILL.md`), so the guard slots in before PR open. |
| T11 Verified RED | tested no-op, 10/10. `docs/design/2026-10-18-verified-red-no-op.md` | re-test only, on the review step in `skills/delivery-pipeline/references/phase-3-execution.md` | Nothing. | The record says a vacuous test behind I/O, a clock, or a long call chain was not covered. See § 4. |
| T12 Security by blast radius | tested no-op, 5/5 review and 5/5 design. `docs/design/2026-10-18-security-blast-radius-no-op.md` | re-test only, on `skills/delivery-review/` (security lens in `references/lenses.md`) and `skills/delivery-spec-plan/` (invariant check, step 4) | Nothing. | cmk already has an invariant check (spec-plan step 4) and a defaulting-to-targeted depth rule for security-touching diffs (`skills/delivery-review/SKILL.md` line ~40). Different prose, so re-test. Not covered: no auth code in repo, a scanner in verify commands, a large diff. |
| T13 Spike pipeline | tested no-op, 8/8. `docs/design/2026-10-18-spike-pipeline-no-op.md` | re-test only. cmk has no spike skill. Nearest: `skills/delivery-intake/` (it captures "reproduction and suspected cause", line ~76) | Nothing. | Not covered: GitHub or Linear tickets (comment durability differs), a spike with no ticket, the UI branch, an investigation needing `research`. Open decision 6 (may a spike start the build) is unanswered. |
| T14 Incident lifecycle | tested no-op, 0/8 patched from the theory. `docs/design/2026-10-18-incident-no-op.md` | re-test only. cmk mentions incidents in `skills/delivery-workflow/SKILL.md` line ~97 ("mitigate first, create the issue once it ...") | Nothing. | Not covered: live telemetry, an agent that can reach the VM, the postmortem. cmk's "mitigate first" rule may change the result. |
| T15 Visualize planned changes | shipped: `skills/spec/plan-tasks/SKILL.md` @1.8.0, a conditional change map through `craft-page`. Evidence: `skills/spec/plan-tasks/TESTS.md` (asked: 3 inline ASCII and 1 none, collision on 0; GREEN 10/10 with 3/3 after a haiku counter). | `skills/delivery-spec-plan/SKILL.md` (150 lines, at the lint budget) | The rule: when the operator asks to see a change map, produce a page through a figure skill with four parts and a `grep` for other plans on the same files. Unasked: no map. | cmk has no `craft-page`. The roadmap lists `cmk:visualize` (`docs/research/skill-ecosystem-and-kit-improvements.md`, item 14). Port after that exists, or point at it. cmk plans are scratch, so a change map would also be scratch unless the operator asks. `skills/delivery-spec-plan/SKILL.md` is at 150 lines; `scripts/skill-lint.sh` fails above 150, so the text must live in a new `references/` file. |
| T16 Backlog sweep | shipped: `skills/track/sweep-backlog/SKILL.md` @1.0.0 plus `scripts/landed.sh`. Evidence: `skills/track/sweep-backlog/TESTS.md` (RED 6/6 missed a fix already on dev, 5/6 edited the tracker before asking; GREEN and REFACTOR 6/6). | closest: `skills/discover-efforts/` (reconcile obligations to the tracker). A new cmk skill is likely, since `discover-efforts` starts from sources, not from the backlog. | The rule: nothing is written first. One list, one question. `landed.sh` finds work already on the default branch by ticket ID. | The jdk skill reads local, GitHub and Linear IDs (`SKILL.md` line 42). cmk is Linear-only in practice. The "four status vocabularies" problem is jdk-specific. Linear status types may be one vocabulary. |
| T17 Workspace housekeeping | tested no-op for the git part, 6/6. `docs/design/2026-10-18-housekeeping-no-op.md` | re-test only. cmk phase 5 retires scratch workspace once evidence is durable (`skills/delivery-pipeline/SKILL.md`) | Nothing. | Containers were excluded on purpose. PR state on a real forge was untested. cmk uses per-issue worktrees that "nobody removes" until phase 5, so the cmk case differs. |
| T18 Post-ship audit | shipped: `skills/review/audit-shipped/SKILL.md` @1.0.0. Evidence: `skills/review/audit-shipped/TESTS.md` (RED: cross-feature state between features 3/8, UTC against marina day 2/8; GREEN 4/4 on all five, held-out 4/4). | new cmk skill (user-invoked), or a mode in `skills/delivery-review/` | The two REQUIRED tables: a reader pass (who reads state each merged change writes) and a glossary pass (terms against the glossary). | The glossary pass needs a glossary: cmk has `skills/glossary/`. The "merged window" is a Linear query plus merged PRs, not `.skills/`. Follow-ups: jdk sends them to the proposal file, cmk would file Linear issues. See § 5. |
| T19 deliver-issues | shipped: `skills/execution/deliver-issues/SKILL.md` @1.0.0 (with `land-branch` @4.3.1). Evidence: `skills/execution/deliver-issues/TESTS.md` (RED 4/4 built all ten tasks in the controller; GREEN: three PRs through review and landing). | already covered by `skills/delivery-pipeline/` (cluster mode, `references/cluster-mode.md`). Port only the failure fixes. | The three fixes: an Iron Law that tasks are not written in the controller, the chain as REQUIRED sub-skills, and "build the contract-keeping option, ask in the PR, carry on". | cmk's pipeline is the thing jdk copied, so the skill itself does not port. The failure modes might: controller writes tasks itself, tickets parked on a question. cmk uses superpowers for execution (`skills/delivery-pipeline/SKILL.md`, "Working with superpowers"). Re-test whether those failures occur there. |
| T20 Real-repo dogfood | not done | none | Nothing. | Not done on jdk, so no proof for cmk. |
| T21 Docs and inventory sync | not done | `docs/ai/skills/*.md` and `docs/ai/skills/conventions.md` in cmk | The idea of one writer for shared ledgers. | cmk's version table in `conventions.md` lists versions per skill, so every port bumps it. |
| T22 This map | this file | none | none | none |
| T23 Cross-owner change notice | shipped: `skills/ship/land-branch/SKILL.md` @4.4.0, `prepare.md` § Owner notice, `scripts/owner-notice.py`; catalog `Owner` column in `templates/specs-catalog-domain.md`. Evidence: `skills/ship/land-branch/TESTS.md` (RED 0/5 named the other owner; GREEN 7/7 section and reviewer, 0/3 on own-only). `skills/spec/plan-tasks` early warning not written (no RED). | `skills/delivery-ship/SKILL.md` and `skills/delivery-workflow/references/pr-traceability.md` (PR body contents) | The behavior: a conditional section `## Changes outside this feature's ownership`, one bullet per owner, present only when a cross-owner path exists, and `gh pr create --reviewer`. No change, no heading, no "none" line. | Biggest conflict. `owner-notice.py` resolves owner through the catalog `Owner` column, then a shard `Owner:` line, then `project.md` Ownership notes, via feature CODEs and `Surface roots`. cmk has none of these. cmk's ownership is the Linear assignee and issue ownership (`skills/delivery-intake/SKILL.md` line ~21). A path-to-owner source for cmk is unclear, check for `CODEOWNERS` in a target repo. Open decision 5 (also comment the PR link on the foreign feature's issue) is a Linear ledger write and is natural in cmk. |

Plan note on T11 and T12: both are tested no-ops, so they belong in § 4.

## 3. Bundled scripts jdk added

Found with `git -C ~/Developer/skills diff --stat main..HEAD`: four scripts.

| Script | Purpose | Reads | jdk-specific parts to replace |
|---|---|---|---|
| `skills/ship/land-branch/scripts/ship-guard.sh <base> [tasks.md]` | One tab-separated row per finding (`lockfile`, `generated`, `out-of-plan`, `behind-base`), then `# clean` or `# findings: N`. Read-only. | `git diff --name-only base...HEAD` and the plan file | The plan parser (`tasks.md` File Structure and `**Files:**`). Pure git otherwise. |
| `skills/ship/land-branch/scripts/owner-notice.py <base> <tasks.md or CODE>` | Rows `cross-owner CODE owner path IDs`, then `# clean` or `# cross-owner: N`. | git diff, `docs/specs/catalog/*.md`, `docs/agents/project.md` Ownership notes, foreign `requirements.md` | Almost everything. The catalog, CODE, `Surface roots` and `Owner` cell are jdk's. Only the git-diff and requirement-ID diff logic carry over. |
| `skills/track/show-run-status/scripts/collect.sh <CODE>` | One fixed pass over every status source. Sections always print. | `docs/specs/catalog/*.md`, `.skills/<CODE>/progress.md`, `git`, project test command | Plan, ledger and tracker sections. Git section carries over. Note it also runs the project's unit-test command. |
| `skills/track/sweep-backlog/scripts/landed.sh <pattern>...` | Where does work naming each ticket ID already live (commit or branch, on the default branch or not). Read-only. | git only | Nothing. It takes a ticket ID pattern, so `ENG-123` works as is. Closest to a drop-in. |

Does cmk have an equivalent place for scripts?

- Per skill: no. The scan of `~/Developer/work/ai-devkit/skills/*` found no `scripts/` folder. Skills hold `SKILL.md`, `references/`, `agents/` (in `skills/delivery-simplify/`), `eval.json` and `TESTS.md`.
- Repo level: `scripts/skill-lint.sh` is the only script. It lints `skills/*/SKILL.md`, `skills/*/references/*.md` and `skills/*/eval.json`. It does not lint a `scripts/` folder, so a `skills/<name>/scripts/` folder would not fail the lint. Whether it would be copied by `cmk:sync` or the plugin build is unclear, check `skills/sync/SKILL.md` and `.claude-plugin/`.
- Rule to respect: "No skill file references outside its own package by relative path" (`docs/ai/skills/conventions.md`). A script must live inside the skill that calls it. `ship-guard.sh` belongs under `skills/delivery-ship/scripts/`.
- Size: cmk caps `SKILL.md` at 150 lines (`scripts/skill-lint.sh`, line 80), so the recipe text goes into `references/`.
- Alternative if scripts are unwelcome: write the passes as shell steps inside a `references/*.md` file. This loses the "never misjudged" property that was the reason jdk used scripts (plan § 2, "Form follows failure").

## 4. Re-test on cmk before porting

Every jdk no-op depended on a condition that may not hold on cmk. None of these should be written into cmk skills until a cmk RED fails.

| Task | Record | jdk-specific condition | Re-test on cmk |
|---|---|---|---|
| T1, T2 | `docs/design/2026-10-18-tracker-writes-no-op.md` | Local `.scratch/` tracker. The record's own Limits section: "Linear MCP server creation is one tool call. Re-run this scenario on a Linear fixture before claiming the result for Linear." The plan repeats it: "Re-run on a Linear fixture before claiming this for Linear." | Run `skills/delivery-intake/` and `skills/discover-efforts/` on a Linear workspace with the team rule "no new tickets without TPM approval" only as prose. Count Linear issues created. |
| T3a, T3b | same record, follow-up | Approver finds the pending ticket from a committed triad (cmk plans are git-ignored scratch). MILE-2 lived in `docs/roadmap/INDEX.md`. | Re-run with the plan in scratch and the milestone as a Linear project or milestone. |
| T4 | `docs/design/2026-10-18-batched-decisions-no-op.md` | Run on `build-inline` only. `build-in-waves` and an interactive session were untested (Limits section). | Run on cmk phase 3 with parallel dispatch. Count stops. cmk's default is already no stops, so the likely fail is silent decisions, not too many questions. |
| T6 | `docs/design/2026-10-18-host-concurrency-no-op.md` | 12/12 sessions ran one subagent at a time. "Untested where safe worktree isolation lets `build-in-waves` open several lanes." The plan says the cap belongs in the cmk port. | Highest value re-test. cmk does open parallel worktrees (`skills/delivery-pipeline/references/worktree-wave-execution.md`). Start two cluster runs on one machine and count agents in flight. |
| T11 | `docs/design/2026-10-18-verified-red-no-op.md` | Not covered: a vacuous test whose pass on the base cannot be worked out by reading (I/O, a clock, a long call chain). | Re-test with such a test in cmk phase 3 task review. |
| T12 | `docs/design/2026-10-18-security-blast-radius-no-op.md` | Not covered: no auth code in the repo, a scanner in the verify commands, a diff too large to read at once. | Re-test with auth buried in a large diff, and with a scanner listed in verify commands. cmk's security lens is in `skills/delivery-review/references/lenses.md`. |
| T13 | `docs/design/2026-10-18-spike-pipeline-no-op.md` | Not covered: GitHub or Linear tickets, a spike with no ticket, the UI branch, a spike needing `research`. Local ticket comments are durable files; Linear comments are not the same. | Run on a Linear issue, and with no issue. |
| T14 | `docs/design/2026-10-18-incident-no-op.md` | Not covered: live telemetry backend, an agent that can reach the VM, the postmortem. Fixture production had no telemetry. | Run with the manager's wrong theory and a Linear incident issue. cmk's "mitigate first" line (`skills/delivery-workflow/SKILL.md` ~97) is a variable. |
| T17 | `docs/design/2026-10-18-housekeeping-no-op.md` | Containers excluded on purpose. PR state on a real forge untested. | Run on a repo with a real forge and cmk's retained per-issue worktrees. |

Also owed: T19. The jdk failures (tasks written in the controller, tickets parked on a question) were fixed in a jdk skill. Check whether cmk's pipeline shows them before adding any text.

## 5. Open questions for the porter

1. Where does a per-repo policy live in cmk? jdk uses `docs/agents/project.md`. Candidates: `skills/agent-instructions/`, `skills/repo-setup/`, or `docs/ai/`. Needed for `Language` (T5) and any later policy field. unclear, check `skills/repo-setup/SKILL.md`.
2. Ownership source for T23. Linear assignee, a `CODEOWNERS` file, or a new field? Without one, `owner-notice.py` has nothing to resolve. Check how a target repo is expected to record ownership.
3. How does a script reach Linear? Bash cannot call the Linear MCP. Does the skill pass Linear data to the script on stdin, or does the script stay git-only and the skill add the Linear step after? `landed.sh` and `ship-guard.sh` are git-only, so they are safe either way.
4. Does cmk want a `scripts/` folder per skill? It is not forbidden by `scripts/skill-lint.sh`, but nothing uses it. Check `cmk:sync` and the plugin manifests for what ships.
5. cmk is "no human gates". jdk's gates are stops (ship guard asks for literal confirmation per flag; operator amendment relies on a hard stop being skipped). How does a confirmation stop fit an unattended run? Likely answer: record the flag as a blocker (`engineering-principles.md` § Autonomy). Decide per script.
6. T5 and T15 depend on skills cmk lacks (`speak-outer`, `craft-page`). Port the rule into an existing cmk skill, or add the dependency? `cmk:visualize` is on the roadmap for T15.
7. Follow-up filing. jdk's `audit-shipped` and `sweep-backlog` route follow-ups through a proposal file. In cmk, follow-ups are Linear issues. Is a new Linear issue created directly, or proposed first? cmk's rule so far: reconcile the tracker, create issues that lack an owner (`skills/discover-efforts/SKILL.md` line ~79).
8. Versions and docs. cmk records versions in `docs/ai/skills/conventions.md` and one page per skill under `docs/ai/skills/`. Each port needs both updated, and cmk's `CLAUDE.md` says `docs/` is the source of truth.
9. Evidence in cmk. Only four delivery skills have a `TESTS.md` and none has `eval.json`. The jdk rule (RED, then GREEN, in `TESTS.md`) needs a cmk fixture on Linear first. T0.1 does not port.
10. T9, T20 and T3c are not done in jdk. Decide whether cmk waits for them or drops them.
