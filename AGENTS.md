# AGENTS.md — Agent Behavior Constitution

> **A-to-Z Agentic Development Skill Set** | 56 skills across 11 categories |
> `jayden-dang/skills` | v0.4.0-pre.0

This file is the single source of truth for agent behavior when working with this
skill set on any harness. Read it first, before any skill, before any action.
Where a harness has no session-start hook to inject `gate-session`, this file is
the fallback that keeps the gates alive.

**Human tutorial (setup + feature loop + entry points):**
[`docs/guide/START-HERE.md`](docs/guide/START-HERE.md) · skill pages:
[`docs/guide/skills/README.md`](docs/guide/skills/README.md). Keep those in sync
when skills or workflows change.

---

## 1. The Four Iron Laws (gates are sacred)

These gates are hard prohibitions, not guidelines. Every gate carries a
rationalization table because that is the form that survives an agent under
pressure. An agent that bypasses a gate has failed.

**Gate 1 — NO-CODE:** `frame-change` MUST run and the ceremony tier MUST be stated
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

**Unknowns loop (quality bottleneck):** The map (prompts, specs, plans) is not
the territory (codebase, runtime, users, history). Strong models still fail when
unknowns stay implicit. Discover unknowns before build (`frame-change` knowns
inventory + blindspot, `clarify-decisions`, `research`/`run-spike`), surface high-blast
decisions in `plan-tasks` (the execute-family route; mode write-back is owned by
the chosen execute skill),
story-derived review units at `build-by-story`, log mid-build **deviations** in
`.skills/<CODE>/implementation-notes.md` during execute, and let the human re-check
understanding with `/study-change` before merge. Do not freeze unverified
solution shape into requirement SHALLs.

---

## 2. The 1% Rule & Skill Invocation Contract

**If there is even a 1% chance a skill applies to what you are about to do, you
MUST invoke that skill first.** This is not a judgment call per-task. You cannot
reason your way out of it.

Invoke relevant or requested skills BEFORE any response or action — before
clarifying questions, before exploring the codebase, before checking a single
file. Announce "Using [skill] to [purpose]", then follow the skill exactly.

**Priority order:** process skills first, then implementation skills. "Build X" →
`frame-change` first. "This is broken" → `root-cause` first. Small in-scope change to a
shipped, spec'd feature → `amend-feature`, not `frame-change`. Incoming issue or external
PR → suggest `/triage` (user-invoked; agents cannot auto-invoke it). Unsure which
flow fits → suggest `/ask-me-bro`.

**User instructions override skills; skills override agent defaults.** Skip a
skill's workflow only when the user has explicitly told you to.

---

## 3. Skill Types & Invocation Rules

**User-invoked skills** (carry `disable-model-invocation: true` in frontmatter):
`ask-me-bro`, `author-skills`, `teach-pack`, `configure-repo`, `bootstrap-repo`,
`define-project`, `assess-pivot-impact`, `triage`, `scan-architecture`, `map-features`,
`write-handoff`, `publish-issues`, `cut-release`, `interpret-session`, `study-change`,
`brief-team`, `select-review-sample`, `refresh-roadmap-status`, `assess-milestone`,
`pathfind`, and Personal OS `setup-personal-os`.
Agents MUST NOT auto-invoke these. Name them for the user to run, e.g. `/triage` or
`/pathfind`.

**Model-invoked skills** (no `disable-model-invocation`): agents auto-invoke
these when conditions match. This includes `gate-session`, `frame-change`,
`clarify-decisions`, `research`, `run-spike`, `define-domain`, the full spec triad,
`build-in-waves`, `build-by-story`, `build-inline`, `test-first`, `root-cause`, `prove-claim`,
`audit-trace`, `load-subgraph`, `isolate-workspace`, `inspect-change`, `polish-diff`,
`vet-feedback`, `review-invariants`, the acceptance suite, `land-branch`,
`package-change`, `record-verdict`, `amend-feature`, `plan-milestones`, and
`realign-spec`.

**Session-injected skill:** `gate-session` is injected by the `SessionStart` hook
on every `startup|clear|compact` event. It is the gate that keeps the 1% rule
alive across compaction. On harnesses without hook support, this file carries
that role.

**Orchestration rule:** a user-invoked skill may invoke model-invoked skills; a
model-invoked skill must never invoke a user-invoked skill. A model-invoked skill
may invoke other model-invoked skills via `REQUIRED SUB-SKILL:` prose.

**Participant boundary:** skills enforce and record only actions this skill set
mediates. Never infer skill-set membership from repository membership, roster,
CODEOWNERS, branch ownership, PR authorship, or supplied artifacts. External
contributors are not policed by a process they never adopted — missing decision
records or requirement IDs on unmediated work is not a methodology violation.

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

**Trace checking:** the `audit-trace` skill is the traceability check — a fixed set of
`grep`/`git` passes with fixed rules, not a manual audit and not a bundled linter.
It fails on: tasks/tests citing unknown IDs; implemented/shipped requirements with
zero covering tests; duplicate ID definitions. It warns on approved requirements
not yet cited by any task. Run by `prove-claim` and `cut-release`, where an agent is present
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
| **0 — Trivial** | Typo-level, zero behavior change | None — `test-first` + `prove-claim` only | `test-first` |
| **1 — Bugfix/Small** | Behavior change ≤ ~half day | Mini-spec: fix REQ + SHALL-CONTINUE-TO guard in owning `requirements.md`, tagged regression test | `specify-behavior` → `test-first` |
| **2 — Feature** | Multi-task work | Full triad: `requirements.md` → `design.md` → `tasks.md` + execute family (`build-in-waves` / `build-by-story` / `build-inline`) | Full chain |

Tier is decided by `frame-change` (new work) or `amend-feature` (existing-feature changes).
Never spec what you do not understand — detour through `research` or `run-spike`
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
   `.skills/<CODE>/task-N-brief.md`
3. Dispatch fresh implementer with brief path, interfaces from prior tasks,
   report path (`.skills/<CODE>/task-N-report.md`), explicit model tier
4. On DONE: package the diff into `.skills/<CODE>/review-<base7>..<head7>.diff`
   (`git log`/`git diff --stat`/`git diff` over `$BASE..HEAD`) — never `HEAD~1`
5. Two-verdict review: **Standards** (repo standards + code-smell baseline) +
   **Spec** (diff vs requirement IDs)
6. Fix loop: ONE fix subagent for all findings, then re-review. Circuit breaker:
   a finding surviving 3 fix cycles, or a task not DONE after 2 redispatches,
   escalates to the user
7. Ledger: append `Task N: complete (commits <base7>..<head7>, review clean)` to
   `.skills/<CODE>/progress.md`

**Model tiering:** state the model explicitly on every dispatch. Cheap tier =
transcription/mechanical fixes. Mid tier = reviewers and implementers working
from prose. Top tier = design judgment, broad codebase understanding, final
whole-branch review.

**Progress ledger:** `.skills/<CODE>/progress.md` is the source of truth per feature across
compaction and crash. Trust the ledger and `git log`, never memory. Never
re-dispatch a task the ledger marks complete.

**Subagent-exempt:** a subagent dispatched for one specific task ignores
`gate-session` and follows its brief only.

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

**Naming:** verb-first, kebab-case: `specify-behavior`, `build-in-waves`,
`inspect-change`.

**Line budget:** SKILL.md under 500 lines, under 300 preferred. If a skill
exceeds 500 lines, split it — implementer prompt, reviewer prompt, or sub-skill
content moves to a sibling file in the same directory.

---

## 8. File Organization

```
skills/                  # two packages — see docs/packages.md
  # Engineering (default plugin)
  meta/ discovery/ spec/ execution/ review/ acceptance/
  craft/ ship/ track/ project/ setup/
  engineering/           # package index README only
  # Personal OS / Personal Pack (opt-in; not in default engineer-pack plugin.json)
  personal/              # using-personal-os, plan-day, review-week, …
templates/               # engineering seeds + templates/personal-os/
hooks/                   # session-start (engineering gate)
docs/
  packages.md            # engineering vs personal install map
  agents/ adr/ architecture/ product/ specs/ guide/
.skills/                 # git-ignored ephemera — feature work under .skills/<CODE>/;
                         # shared: pathfind/, research/, decisions/, pr-packages/
                         # (see templates/skills-ephemera-paths.md)
.out-of-scope/
```

**Packages:** Engineering vs Personal OS — `docs/packages.md`.  
Personal skills use **secretary default** (management only). Root Iron Laws (NO-CODE / TDD / …) govern **engineering** sessions, not life-vault management.

**Per-repo config** (`docs/agents/`, written by `configure-repo`): `project.md`
(verify commands, release steps, **Project posture**, and **Team** roster/band),
`issue-tracker.md` (tracker choice + wayfinding), `triage-labels.md` (role →
label mapping). Skills read these at runtime; if missing, say so once per session
and suggest `configure-repo`.

---

## 9. Forbidden Patterns (agents MUST NEVER)

- Write production code before a failing test exists (Gate 2)
- Propose or apply a fix without root-cause investigation (Gate 3)
- Claim completion without fresh verification evidence (Gate 4)
- Skip the tier-decision gate and start coding (Gate 1)
- Auto-invoke a user-invoked skill (`disable-model-invocation: true`)
- Run two implementers on the same plan in parallel (collision guaranteed)
- Hand a subagent the whole plan file — the brief in `.skills/<CODE>/task-N-brief.md` is its world
- Use `HEAD~1` as a review base — use `git rev-parse HEAD` recorded before dispatch
- Skip re-review after a fix, or accept a review missing either verdict
- Move to the next task with open Critical/Important findings
- Fix reviewer findings in the controller context — dispatch a fixer
- Pause between tasks to ask permission to continue under continuous
  `build-in-waves` / `build-inline` (story-unit human stops belong only to
  `build-by-story`)
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
- `audit-trace` check clean (no orphaned IDs, no uncovered requirements, no duplicate
  definitions)
- Progress ledger appended for every completed task
- `inspect-change` two-verdict clean (Standards + Spec axes)
- `validate-feature` confirms user-facing behaviors on the running system
- Feature status updated (Draft → Approved → Implemented → Shipped)

Can't tick a box? The work is not done.

---

## 11. Quick Reference: The 56 Skills

**Legend:** (m) model-invoked · (U) user-invoked · (si) session-injected

| Category | Skills |
|---|---|
| **meta** | `gate-session` (m, si), `ask-me-bro` (U), `author-skills` (U), `teach-pack` (U) |
| **setup** | `configure-repo` (U), `bootstrap-repo` (U) |
| **discovery** | `frame-change` (m), `clarify-decisions` (m), `interpret-session` (U), `research` (m), `run-spike` (m), `define-domain` (m), `pathfind` (U) |
| **spec** | `specify-behavior` (m), `design-solution` (m), `plan-tasks` (m) |
| **execution** | `build-in-waves` (m), `build-by-story` (m), `build-inline` (m), `test-first` (m), `root-cause` (m), `prove-claim` (m), `audit-trace` (m), `load-subgraph` (m), `isolate-workspace` (m) |
| **review** | `inspect-change` (m), `select-review-sample` (U), `study-change` (U), `brief-team` (U), `polish-diff` (m), `vet-feedback` (m), `review-invariants` (m) |
| **acceptance** | `validate-feature` (m), `validate-api` (m), `validate-ui` (m), `review-product-flow` (m), `vet-product-flow` (m), `run-product-walkthrough` (m) |
| **craft** | `craft-page` (m) |
| **ship** | `package-change` (m), `land-branch` (m), `record-verdict` (m), `cut-release` (U) |
| **track** | `amend-feature` (m), `reroute-plan` (m), `triage` (U), `realign-spec` (m), `refresh-roadmap-status` (U), `assess-milestone` (U), `scan-architecture` (U), `map-features` (U), `write-handoff` (U), `publish-issues` (U) |
| **project** | `define-project` (U), `assess-pivot-impact` (U), `plan-milestones` (m) |

**Execute family (pick one after approved `tasks.md`):**

| Skill | When |
|---|---|
| `build-in-waves` | Subagent waves (writes `Execution-mode: continuous`) |
| `build-by-story` | Human-gated review units (writes `Execution-mode: story-unit`) |
| `build-inline` | No implementer subagents / user watches controller implement |

**Main flow:** `frame-change` (+ `load-subgraph`) → `specify-behavior` →
`design-solution` → `plan-tasks` → `isolate-workspace` → execute family →
`inspect-change` (+ `load-subgraph`) → `polish-diff` → `validate-feature` →
`package-change` → `land-branch` → `cut-release` → `realign-spec`.

**Program layer (optional):** `define-project` (vision + `ARCH-N` spine) →
`plan-milestones` (`MILE-N` milestones and `ROAD-N` items in `docs/roadmap/INDEX.md`) →
the feature flow above, one roadmap item at a time. Every edit to an existing roadmap —
dropping an item, reordering milestones, committing or closing one — goes through
`plan-milestones`, never a direct file edit. A pivot that collides with shipped code
goes through `/assess-pivot-impact` (disposition ledger) **before**
`/define-project` update rewrites the vision layer.

**Bugfix flow:** `root-cause` → mini-spec → `test-first` → `prove-claim` → `inspect-change` →
`land-branch`.

**Maintenance:** `amend-feature` (small changes), `triage` (incoming issues), `realign-spec`
(spec drift), `scan-architecture` (periodic deepening), `/map-features` (brownfield ID/Files
backfill).

**Personal OS (independent opt-in package):** life/vault management skills under
`skills/personal/` — see `skills/personal/README.md` and `docs/personal-os/START-HERE.md`.
Not part of the default engineering plugin; does not depend on engineering skills.

**Human how-to:** [`docs/guide/START-HERE.md`](docs/guide/START-HERE.md).

---

*This constitution is enforced. Read it first. Follow it always. No exceptions.*

## Agent skills

This repo is configured for a spec-driven skill set.

- Feature flow: `frame-change` (+ `load-subgraph`) → `specify-behavior` →
  `design-solution` → `plan-tasks` → execute family → `inspect-change` →
  `validate-feature` → `land-branch`
- Bug on-ramp: `root-cause` (root cause first, then a guarded fix)
- Capture a conversation/spec/idea into tracker issues: `/publish-issues` (user-run)
- Multi-session decision map (Layer 0 fog): `/pathfind` (user-run)
- Incoming issues and PRs: `/triage` (user-run)
- Brownfield feature-ID / Files backfill: `/map-features` (user-run)
- Traceability check: the `audit-trace` skill — run by `prove-claim` and `cut-release`;
  keep it clean
- Horizontal neighbors: `load-subgraph` (model) — advisory, live specs only
- Project docs (layer enabled): `/define-project` maintains
  `docs/product/vision.md`, the `docs/architecture/` invariant spine, and
  `docs/product/guidelines.md`; the feature skills consult them
- Pivot against shipped code: `/assess-pivot-impact` produces the disposition
  ledger before vision/architecture rewrites
- Tutorial: [`docs/guide/START-HERE.md`](docs/guide/START-HERE.md)

Repo config the skills read:

- verify commands, test annotations, release steps: `docs/agents/project.md`
- Team composition (roster, ownership notes, workflow band): `docs/agents/project.md` (`## Team`)
- Issue tracker operations: `docs/agents/issue-tracker.md`
- Triage label mapping: `docs/agents/triage-labels.md`
