# AGENTS.md — Agent Behavior Constitution

> **A-to-Z Agentic Development Skill Set** | 37 skills across 10 categories |
> `jayden-dang/skills` | v1.0

This file is the single source of truth for agent behavior when working with this
skill set on any harness. Read it first, before any skill, before any action.
Where a harness has no session-start hook to inject `using-skills`, this file is
the fallback that keeps the gates alive.

---

## 1. The Four Iron Laws (gates are sacred)

These gates are hard prohibitions, not guidelines. Every gate carries a
rationalization table because that is the form that survives an agent under
pressure. An agent that bypasses a gate has failed.

**Gate 1 — NO-CODE:** `brainstorm` MUST run and the ceremony tier MUST be stated
out loud before any spec work begins. For tier ≥1, requirements MUST be written
and approved before design or code. No scaffolding, no generators, no "just
trying something" until the gate clears.

**Gate 2 — TEST-FIRST:** NO production code without a failing test first. Wrote
code before the test? Delete it — no exceptions, no "keep as reference", no
"adapt it while tests catch up". Verify RED (fails for the right reason) and
verify GREEN (pristine output, zero warnings) are mandatory, never skip.

**Gate 3 — ROOT-CAUSE:** NO fixes without root-cause investigation. A
red-capable command (fast, deterministic, agent-runnable pass/fail) MUST exist
and have been run before any theory-building. Three failed fix attempts = STOP
and question the architecture.

**Gate 4 — EVIDENCE:** NO completion claims without fresh verification evidence.
Identify the proving command → run it full and fresh → read the output → confirm
it supports the claim. "It passed earlier" is not evidence. "The agent said
success" is not evidence. Read the diff yourself.

---

## 2. The 1% Rule & Skill Invocation Contract

**If there is even a 1% chance a skill applies to what you are about to do, you
MUST invoke that skill first.** This is not a judgment call per-task. You cannot
reason your way out of it.

Invoke relevant or requested skills BEFORE any response or action — before
clarifying questions, before exploring the codebase, before checking a single
file. Announce "Using [skill] to [purpose]", then follow the skill exactly.

**Priority order:** process skills first, then implementation skills. "Build X" →
`brainstorm` first. "This is broken" → `debug` first. Small in-scope change to a
shipped, spec'd feature → `amend`, not `brainstorm`. Incoming issue or external
PR → suggest `/triage` (user-invoked; agents cannot auto-invoke it). Unsure which
flow fits → suggest `/ask`.

**User instructions override skills; skills override agent defaults.** Skip a
skill's workflow only when the user has explicitly told you to.

---

## 3. Skill Types & Invocation Rules

**User-invoked skills** (carry `disable-model-invocation: true` in frontmatter):
`ask`, `writing-skills`, `teach`, `setup-repo`, `scaffold-project`,
`establish-project`, `triage`, `improve-architecture`, `handoff`, `file-issues`,
`release`. Agents MUST NOT auto-invoke these. Name them for the user to run, e.g.
`/triage`.

**Model-invoked skills** (no `disable-model-invocation`): agents auto-invoke
these when conditions match. This includes `using-skills`, `brainstorm`,
`grilling`, `research`, `prototype`, `domain-modeling`, the full spec triad,
`execute-plan`, `tdd`, `debug`, `verify`, `worktrees`, `code-review`,
`receive-review`, `check-invariants`, the acceptance suite, `finish-branch`, `amend`, and
`sync-spec`.

**Session-injected skill:** `using-skills` is injected by the `SessionStart` hook
on every `startup|clear|compact` event. It is the gate that keeps the 1% rule
alive across compaction. On harnesses without hook support, this file carries
that role.

**Orchestration rule:** a user-invoked skill may invoke model-invoked skills; a
model-invoked skill must never invoke a user-invoked skill. A model-invoked skill
may invoke other model-invoked skills via `REQUIRED SUB-SKILL:` prose.

---

## 4. Requirements Traceability Spine (non-negotiable)

A requirement ID is a first-class runtime object. It flows through every artifact
in a deterministic chain:

```
requirements.md  →  design.md  →  tasks.md  →  tests  →  commits  →  changelog
**SHELL-1.2**      Satisfies:   _Requirements:_   tag/@ID    Implements:   derived
```

**ID format:** `CODE-N.M` where `CODE` is a short feature prefix (registered in
`docs/specs/INDEX.md`), `N` is the story number, `M` is the criterion number. IDs
are immutable once approved — retire by striking through
(`~~**CODE-1.2**~~`), never renumber.

**Citation rules per artifact:**

| Artifact | Citation form | Example |
|---|---|---|
| `requirements.md` | `**CODE-N.M**` bold EARS statement | `**SHELL-1.2** WHEN ... THE SYSTEM SHALL ...` |
| `design.md` | `Satisfies: CODE-N.M, ...` per section | `Satisfies: SHELL-1.1, SHELL-1.2` |
| `tasks.md` | `_Requirements: CODE-N.M, ..._` footer per task | `_Requirements: SHELL-1.2_` |
| Playwright test | `{ tag: ['@CODE-N.M'] }` | grep-selectable, JSON reporter |
| Vitest test | `annotate('CODE-N.M', 'requirement')` or ID in test name | |
| Rust test | `/// REQ: CODE-N.M` doc comment | greppable |
| Commit message | `Implements: CODE-N.M` or `Guards: CODE-N.M` trailer | |
| Issue body | `Requirements covered` section | |

**Trace checking:** the `trace` skill is the traceability check — a fixed set of
`grep`/`git` passes with fixed rules, not a manual audit and not a bundled linter.
It fails on: tasks/tests citing unknown IDs; implemented/shipped requirements with
zero covering tests; duplicate ID definitions. It warns on approved requirements
not yet cited by any task. Run by `verify` and `release`, where an agent is present
to run it.

**Coverage definition:** a requirement is covered when ≥1 test citing its ID ran
and passed, as attested by a test runner's report. A skipped, failing, or
commented-out test is NOT coverage. A string in a file is NOT a test. Fixture IDs
(doc comments, example data) are NOT citations.

---

## 5. Ceremony Tier Rules

Tiers are stated explicitly, with justification. Never let the agent decide
silently.

| Tier | Trigger | Artifacts | Exit |
|---|---|---|---|
| **0 — Trivial** | Typo-level, zero behavior change | None — `tdd` + `verify` only | `tdd` |
| **1 — Bugfix/Small** | Behavior change ≤ ~half day | Mini-spec: fix REQ + SHALL-CONTINUE-TO guard in owning `requirements.md`, tagged regression test | `write-requirements` → `tdd` |
| **2 — Feature** | Multi-task work | Full triad: `requirements.md` → `design.md` → `tasks.md` + `execute-plan` | Full chain |

Tier is decided by `brainstorm` (new work) or `amend` (existing-feature changes).
Never spec what you do not understand — detour through `research` or `prototype`
first.

---

## 6. Subagent Rules

**Why subagents:** each worker receives exactly the context its task needs and
nothing else. Subagents never inherit session history — you construct their
world. Bulk artifacts travel as file paths under `.skills/`, never as pasted
text.

**Task handoff protocol:**
1. Record `BASE=$(git rev-parse HEAD)` before dispatch
2. Build brief: copy Task N's block + verbatim Global Constraints into
   `.skills/task-N-brief.md`
3. Dispatch fresh implementer with brief path, interfaces from prior tasks,
   report path (`.skills/task-N-report.md`), explicit model tier
4. On DONE: package the diff into `.skills/review-<base7>..<head7>.diff`
   (`git log`/`git diff --stat`/`git diff` over `$BASE..HEAD`) — never `HEAD~1`
5. Two-verdict review: **Standards** (repo standards + code-smell baseline) +
   **Spec** (diff vs requirement IDs)
6. Fix loop: ONE fix subagent for all findings, then re-review. Circuit breaker:
   a finding surviving 3 fix cycles, or a task not DONE after 2 redispatches,
   escalates to the user
7. Ledger: append `Task N: complete (commits <base7>..<head7>, review clean)` to
   `.skills/progress.md`

**Model tiering:** state the model explicitly on every dispatch. Cheap tier =
transcription/mechanical fixes. Mid tier = reviewers and implementers working
from prose. Top tier = design judgment, broad codebase understanding, final
whole-branch review.

**Progress ledger:** `.skills/progress.md` is the source of truth across
compaction and crash. Trust the ledger and `git log`, never memory. Never
re-dispatch a task the ledger marks complete.

**Subagent-exempt:** a subagent dispatched for one specific task ignores
`using-skills` and follows its brief only.

---

## 7. Skill File Conventions

Every skill lives in `skills/<category>/<name>/SKILL.md`. Cross-references use
`REQUIRED SUB-SKILL:` prose, never `@`-links.

**SKILL.md frontmatter (mandatory):**
```yaml
---
name: skill-name
description: Use when <triggering conditions only, never the workflow>
---
```
- `description` states triggering conditions only — a description that summarizes
  the workflow tempts the agent to follow the summary and skip the skill body.
- User-invoked skills add `disable-model-invocation: true`.

**SKILL.md body rules:**
- Imperative voice throughout
- Hard gates in `<HARD-GATE>` or `## The Iron Law` blocks with fenced text
- Rationalization tables: `| Thought | Reality |` format — verbatim from baseline
  runs
- Red-flags sections for anti-patterns the agent must watch for
- Checklists with explicit "Done when:" criteria
- A no-op path: what happens when the skill's conditions don't apply
- Completion criteria: what "done" means

**Naming:** verb-first, kebab-case: `write-requirements`, `execute-plan`,
`code-review`.

**Line budget:** SKILL.md under 500 lines, under 300 preferred. If a skill
exceeds 500 lines, split it — implementer prompt, reviewer prompt, or sub-skill
content moves to a sibling file in the same directory.

---

## 8. File Organization

```
skills/                  # skill definitions (40 skills, 11 categories)
  meta/                  # using-skills, ask, writing-skills
  setup/                 # setup-repo, scaffold-project
  discovery/             # brainstorm, grilling, research, prototype, domain-modeling
  spec/                  # write-requirements, write-design, write-plan
  execution/             # execute-plan, tdd, debug, verify, trace, worktrees
  review/                # code-review, receive-review, check-invariants
  acceptance/            # acceptance-check, acceptance-api, acceptance-ui, dogfood
  craft/                 # design-page
  ship/                  # finish-branch, release
  track/                 # amend, correct-course, triage, sync-spec, improve-architecture, handoff, file-issues
  project/               # establish-project (optional project-documentation layer)
templates/               # requirements.md, design.md, tasks.md, CONTEXT.md seeds
hooks/                   # session-start.sh + hooks.json (injection on startup/clear/compact)
docs/
  agents/                # per-repo config (project.md, issue-tracker.md, triage-labels.md)
  adr/                   # architecture decision records (1–3 sentences, three-part gate)
  architecture/          # SSOT: INDEX.md ARCH-N spine + system design domains
  product/               # vision.md + guidelines.md (optional project-docs layer)
  specs/                 # spec triads per feature + INDEX.md (feature-code registry)
  guide/                 # human documentation (concepts, methodology, process, skills)
.skills/                 # git-ignored ephemera: task briefs, reports, review diffs, ledger
.out-of-scope/           # rejection knowledge base (one file per concept)
```

**Per-repo config** (`docs/agents/`, written by `setup-repo`): `project.md`
(verify commands, release steps, **Project posture**, and **Team** roster/band),
`issue-tracker.md` (tracker choice + wayfinding), `triage-labels.md` (role →
label mapping). Skills read these at runtime; if missing, say so once per session
and suggest `setup-repo`.

---

## 9. Forbidden Patterns (agents MUST NEVER)

- Write production code before a failing test exists (Gate 2)
- Propose or apply a fix without root-cause investigation (Gate 3)
- Claim completion without fresh verification evidence (Gate 4)
- Skip the tier-decision gate and start coding (Gate 1)
- Auto-invoke a user-invoked skill (`disable-model-invocation: true`)
- Run two implementers on the same plan in parallel (collision guaranteed)
- Hand a subagent the whole plan file — the brief in `.skills/task-N-brief.md` is its world
- Use `HEAD~1` as a review base — use `git rev-parse HEAD` recorded before dispatch
- Skip re-review after a fix, or accept a review missing either verdict
- Move to the next task with open Critical/Important findings
- Fix reviewer findings in the controller context — dispatch a fixer
- Pause between tasks to ask permission to continue
- Re-dispatch a task the ledger marks complete
- Start implementation on main/master without explicit user consent
- Tell a reviewer what not to flag, or pre-rate a finding's severity
- Dispatch a reviewer without a diff package
- Keep untested code "as reference" while writing tests
- Write all tests up front, then all code — work one vertical slice at a time
- Mock internal collaborators — mock only at system boundaries
- Assert on mock existence or call count
- Put implementation details in skill `description` frontmatter
- Use `@`-links for cross-skill references

---

## 10. Quality Standards — Definition of Done

A change is done ONLY when ALL of the following are true:

- Every new behavior has a test that was watched failing first, for the expected
  reason
- Full test suite green, output pristine (zero warnings, zero errors)
- Every test tagged with its requirement ID per `docs/agents/project.md`
- Mocks only at system boundaries, complete data structures, no assertions on
  mocks
- Edge cases and error paths covered
- `trace` check clean (no orphaned IDs, no uncovered requirements, no duplicate
  definitions)
- Progress ledger appended for every completed task
- Code-review two-verdict clean (Standards + Spec axes)
- `acceptance-check` confirms user-facing behaviors on the running system
- Feature status updated (Draft → Approved → Implemented → Shipped)

Can't tick a box? The work is not done.

---

## 11. Quick Reference: The 40 Skills

**Legend:** (m) model-invoked · (U) user-invoked · (si) session-injected

| Category | Skills |
|---|---|
| **meta** | `using-skills` (m, si), `ask` (U), `writing-skills` (U), `teach` (U) |
| **setup** | `setup-repo` (U), `scaffold-project` (U) |
| **discovery** | `brainstorm` (m), `grilling` (m), `research` (m), `prototype` (m), `domain-modeling` (m) |
| **spec** | `write-requirements` (m), `write-design` (m), `write-plan` (m) |
| **execution** | `execute-plan` (m), `tdd` (m), `debug` (m), `verify` (m), `trace` (m), `worktrees` (m) |
| **review** | `code-review` (m), `receive-review` (m), `check-invariants` (m) |
| **acceptance** | `acceptance-check` (m), `acceptance-api` (m), `acceptance-ui` (m), `dogfood` (m) |
| **craft** | `design-page` (m) |
| **ship** | `finish-branch` (m), `release` (U) |
| **track** | `amend` (m), `correct-course` (m), `triage` (U), `sync-spec` (m), `improve-architecture` (U), `handoff` (U), `file-issues` (U) |
| **project** | `establish-project` (U) |

**Main flow:** `brainstorm` → `write-requirements` → `write-design` →
`write-plan` → `worktrees` → `execute-plan` → `code-review` → `acceptance-check`
→ `finish-branch` → `release` → `sync-spec`.

**Bugfix flow:** `debug` → mini-spec → `tdd` → `verify` → `code-review` →
`finish-branch`.

**Maintenance:** `amend` (small changes), `triage` (incoming issues), `sync-spec`
(spec drift), `improve-architecture` (periodic deepening).

---

*This constitution is enforced. Read it first. Follow it always. No exceptions.*

## Agent skills

This repo is configured for a spec-driven skill set.

- Feature flow: `brainstorm` → `write-requirements` → `write-design` →
  `write-plan` → `execute-plan`
- Bug on-ramp: `debug` (root cause first, then a guarded fix)
- Capture a conversation/spec/idea into tracker issues: `/file-issues` (user-run)
- Incoming issues and PRs: `/triage` (user-run)
- Traceability check: the `trace` skill — run by `verify` and `release`;
  keep it clean
- Project docs (layer enabled): `/establish-project` maintains
  `docs/product/vision.md`, the `docs/architecture/` invariant spine, and
  `docs/product/guidelines.md`; the feature skills consult them

Repo config the skills read:

- Verify commands, test annotations, release steps: `docs/agents/project.md`
- Team composition (roster, ownership notes, workflow band): `docs/agents/project.md` (`## Team`)
- Issue tracker operations: `docs/agents/issue-tracker.md`
- Triage label mapping: `docs/agents/triage-labels.md`
