# AGENTS.md — Agent Behavior Constitution

> A-to-Z agentic development skill set · **80 skills across 11 categories**
> (62 engineering + 18 Personal OS) · `jayden-dang/skills` · v1.0.0

This file is the single source of truth for agent behavior when working with this
skill set on any harness. Read it first, before any skill, before any action.
Where a harness has no session-start hook to inject `gate-session`, this file is
the fallback that keeps the gates alive — that is why Codex, opencode, and Cursor
are pointed here rather than at the hook.

**Human tutorial (setup + feature loop + entry points):**
[`docs/guide/START-HERE.md`](docs/guide/START-HERE.md) · skill pages:
[`docs/guide/skills/README.md`](docs/guide/skills/README.md). Keep those in sync
when skills or workflows change.

> **Restored, not reverted.** This file was deleted in `65126b7` ("chrone: clean
> docs"), a commit that removed this repo's own dogfooding artifacts and took the
> portable contract with them — the same accident that had already cost
> `lefthook.yml`, which carries its own note about it. Restored 2026-08-15 with
> corrections rather than a straight revert: the skill inventory, the invocation
> lists, and the frontmatter rules had all moved on, and the old §8 described a
> **consuming** repo's layout as though it were this one.

---

## 1. The Four Iron Laws (gates are sacred)

These gates are hard prohibitions, not guidelines. Every gate carries a
rationalization table because that is the form that survives an agent under
pressure. An agent that bypasses a gate has failed.

**Gate 1 — NO-CODE:** `frame-change` MUST run and the ceremony tier MUST be
stated out loud before any spec work begins. For tier ≥1, requirements MUST be
written and approved before design or code. No scaffolding, no generators, no
"just trying something" until the gate clears.

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
success" is not evidence. Read the diff yourself. **Full means the project's
whole suite command, not a path- or pattern-scoped subset**: a scoped run's
totals are that scope's, never the suite's, and quoting them as the suite's is a
false claim even though a real command really ran. When the claim is that a
record now *holds* a change — a ticket, a remote, a stored row — the proving
command is the **read**, never the write that made it.

**Unknowns loop (quality bottleneck):** The map (prompts, specs, plans) is not
the territory (codebase, runtime, users, history). Strong models still fail when
unknowns stay implicit. Discover unknowns before build (`frame-change` knowns
inventory + blindspot, `clarify-decisions`, `research` / `run-spike`), surface
high-blast decisions in `plan-tasks`, take story-derived review units at
`build-by-story`, log mid-build **deviations** in
`.skills/<CODE>/implementation-notes.md` during execute, and let the human
re-check understanding with `/study-change` before merge. Do not freeze
unverified solution shape into requirement SHALLs.

---

## 2. The 1% Rule & Skill Invocation Contract

**If there is even a 1% chance a skill applies to what you are about to do, you
MUST invoke that skill first.** This is not a judgment call per-task. You cannot
reason your way out of it.

Invoke relevant or requested skills BEFORE any response or action — before
clarifying questions, before exploring the codebase, before checking a single
file. Announce "Using [skill] to [purpose]", then follow the skill exactly. If it
carries a checklist, create one todo per item.

**Priority order:** process skills first, then implementation skills.

| Situation | First move |
|---|---|
| "Build X" / "add X" / "can we support X" | `frame-change` — before plan mode, before scaffolding |
| "This is broken", a clear unexpected behavior | `root-cause` — before any fix |
| Ambiguous problem, or a requested solution with no trustworthy gap | `solve-problem` — before guessing between the two above |
| Small in-scope change to a shipped, spec'd feature | `amend-feature`, not `frame-change` |
| Incoming issue or external PR | suggest `/triage` (user-run; agents cannot auto-invoke) |
| Capture this conversation into tracker issues | suggest `/publish-issues` (user-run) |
| Unsure which flow fits | suggest `/ask-me-bro` (user-run) |

**User instructions override skills; skills override agent defaults.** Skip a
skill's workflow only when the user has explicitly told you to. A waiver of
*process* is never a waiver of *evidence*: Gate 4 survives "skip the ceremony".

---

## 3. Skill Types & Invocation Rules

**User-invoked skills** carry `disable-model-invocation: true` in frontmatter.
Agents MUST NOT auto-invoke these — name them for the user to run (`/triage`,
`/pathfind`). All 25 of them:

`ask-me-bro`, `author-skills`, `teach-pack` · `bootstrap-repo`, `configure-repo` ·
`deepen-codebase`, `interpret-session`, `pathfind`, `work-the-problem` ·
`brief-team`, `select-review-sample`, `study-change` · `assess-pivot-impact`,
`define-project`, `define-system-doc` · `cut-release` · `assess-milestone`,
`map-features`, `publish-issues`, `record-debt`, `refresh-roadmap-status`,
`scan-architecture`, `triage`, `write-handoff` · Personal OS: `life-setup`.

**Model-invoked skills** (no `disable-model-invocation`) are auto-invoked when
the description matches the situation. Everything not listed above, including
`gate-session`, `frame-change`, `clarify-decisions`, `solve-problem`, `research`,
`run-spike`, `define-domain`, the full spec triad, the execute family,
`test-first`, `root-cause`, `prove-claim`, `audit-trace`, `load-subgraph`,
`isolate-workspace`, `inspect-change`, `polish-diff`, `vet-feedback`,
`review-invariants`, the acceptance suite, `package-change`, `land-branch`,
`record-verdict`, `amend-feature`, `reroute-plan`, `realign-spec`, and
`plan-milestones`.

**Session-injected skill:** `gate-session` is injected by the `SessionStart` hook
(`hooks/hooks.json`, matcher `startup|clear|compact`), so the 1% rule survives
`/clear` and compaction. On harnesses without hook support, this file carries
that role.

**Orchestration rule:** a user-invoked skill may invoke model-invoked skills; a
model-invoked skill must never invoke a user-invoked one. `REQUIRED SUB-SKILL:
use \`x\`` is for model-invocable targets only — pointing it at a
`disable-model-invocation` skill is a dead-end hand-off and a real bug, caught by
`scripts/lint-write-handoffs.py`.

**Two reachability paths, and one of them is fragile.** A skill is reached either
by a `REQUIRED SUB-SKILL` hand-off or by its description matching what the user
said. Five model-invocable skills have no `REQUIRED SUB-SKILL` caller —
`solve-problem`, `amend-feature`, `vet-feedback`, `run-product-walkthrough`
(plus hook-injected `gate-session`). `review-product-flow` is reached from
`prove-claim` (alternative to `validate-feature`) and from the execute-family
close sequence when a walk predicate holds. The remaining entry points fire
on what the user said, which makes their descriptions the only thing
standing between them and never running. An entry point that undertriggers
is invisible: it does not fail, it simply never appears.

**Participant boundary:** skills enforce and record only actions this skill set
mediates. Never infer skill-set membership from repository membership, roster,
CODEOWNERS, branch ownership, or PR authorship. External contributors are not
policed by a process they never adopted — missing decision records or requirement
IDs on unmediated work is not a methodology violation.

---

## 4. Requirements Traceability Spine (non-negotiable)

A requirement ID is a first-class object of the **spec triad**. It flows through
docs-side artifacts; it is **not** required in application source, tests, or
commit messages (docs-only spine).

```
requirements.md  →  design.md  →  tasks.md  →  (behavior tests + Spec review)
**SHELL-1.2**       Satisfies:    _Requirements:_    domain-language tests
        optional: issue body · changelog derived from specs
```

**ID format:** `CODE-N.M`, where `CODE` is a short feature prefix registered in
`docs/specs/INDEX.md`, `N` is the story number and `M` the criterion number. IDs
are immutable once approved — retire by striking through (`~~**CODE-1.2**~~`),
never renumber.

| Artifact | Citation form |
|---|---|
| `requirements.md` | `**CODE-N.M**` bold, opening an EARS statement |
| `design.md` | `Satisfies: CODE-N.M, …` per section |
| `tasks.md` | `_Requirements: CODE-N.M, …_` footer per task |
| Issue body (optional) | a `Requirements covered` section |
| Application source, tests, commits | **no IDs required** — domain language only |
| Changelog | derived from specs and commit subjects, not trailer parsing |

**Horizontal ownership** is path-based: `load-subgraph` and the `**Files:**`
grammar, neighbors schema 1.1 plus query-local `cluster(focus)`, advisory only.

**Trace checking:** `audit-trace` is the **docs-only** vertical check — fixed
`grep` / `git` passes over `docs/specs/` and optional architecture. It fails on
tasks citing unknown IDs and on duplicate ID definitions; it warns on approved
requirements no task cites. It never greps tests or source for IDs. Run by
`prove-claim`, `land-branch`, `cut-release`, and `realign-spec`.

**Coverage definition:** a requirement's *behavior* is covered when tests or
acceptance checks prove that behavior and Spec review walks the ID against the
diff. Greppable ID strings in test files are not required and are not coverage.
This repo's own pack tests may embed `CODE-N.M` tokens as product fixtures —
that is not a consumer convention.

---

## 5. Ceremony Tier Rules

Tiers are stated explicitly, with justification. Never let the agent decide
silently — deciding it is tier 0 **is** the design step, performed at the
smallest scale the change deserves.

| Tier | Trigger | Artifacts | Exit |
|---|---|---|---|
| **0 — Trivial** | Typo-level, zero behavior change | none — `test-first` + `prove-claim` only | `test-first` |
| **1 — Bugfix / small** | Behavior change ≤ ~half a day | mini-spec: fix requirement + `SHALL CONTINUE TO` guard in the owning `requirements.md`, plus a regression test | `specify-behavior` → `test-first` |
| **2 — Feature** | Multi-task work | the full triad, then the execute family | full chain |

Tier is decided by `frame-change` (new work) or `amend-feature` (changes to a
shipped, spec'd feature). Never spec what you do not understand yet — detour
through `research` or `run-spike` first. **The tier controls the artifacts; it
never softens the gates.**

---

## 6. Subagent Rules

**Why subagents:** each worker receives exactly the context its task needs and
nothing else. Subagents never inherit session history — you construct their
world. Bulk artifacts travel as file paths under `.skills/`, never as pasted text.

**Task hand-off protocol:**

1. Record `BASE=$(git rev-parse HEAD)` before dispatch.
2. Build the brief: Task N's block plus verbatim Global Constraints into
   `.skills/<CODE>/task-N-brief.md`.
3. Dispatch a fresh implementer with the brief path, interfaces from prior tasks,
   the report path, and an explicit model tier.
4. On DONE, package the diff into `.skills/<CODE>/review-<base7>..<head7>.diff`
   over `$BASE..HEAD` — never `HEAD~1`.
5. Two-verdict review: **Standards** (repo conventions + the code-smell baseline)
   and **Spec** (diff against requirement IDs).
6. Fix loop: ONE fix subagent for all findings, then re-review. Circuit breaker —
   a finding surviving 3 fix cycles, or a task not DONE after 2 redispatches,
   escalates to the user.
7. Ledger: append `Task N: complete (commits <base7>..<head7>, review clean)` to
   `.skills/<CODE>/progress.md`.

**Model tiering:** state the model explicitly on every dispatch. Cheap tier for
transcription and mechanical fixes; mid tier for reviewers and implementers
working from prose; top tier for design judgment, broad codebase understanding,
and the final whole-branch review.

**Progress ledger:** `.skills/<CODE>/progress.md` is the source of truth per
feature across compaction and crash. Trust the ledger and `git log`, never
memory. Never re-dispatch a task the ledger marks complete.

**Subagent-exempt:** a subagent dispatched for one specific task ignores
`gate-session` and follows its brief only.

---

## 7. Skill File Conventions

Every skill lives in `skills/<category>/<name>/SKILL.md`. Cross-references are
`REQUIRED SUB-SKILL:` prose, never `@`-links or markdown links into another
skill's folder.

**Frontmatter (all three fields mandatory; `scripts/lint-skill-frontmatter.py`
fails a missing or malformed `version`):**

```yaml
---
name: skill-name
version: 1.0.0
description: Use when <trigger> — produces <the outcome noun>
---
```

- `description` states **trigger + outcome, never the workflow.** Name the
  deliverable plus when it fires. A process summary hands the agent a shortcut it
  obeys instead of reading the body.
- User-invoked skills add `disable-model-invocation: true`. Their descriptions
  route nothing — the user types the name — so write one plain human-facing line,
  no keyword packing.
- `version`: patch for wording that changes no behavior, minor for a new rule or
  slot, major when existing usage breaks.

**Body rules:** imperative voice; hard gates in `<HARD-GATE>`,
`<NON-NEGOTIABLE>`, or `## The Iron Law` blocks; rationalization tables in
`| Thought | Reality |` form, verbatim from baseline runs; a `## Red Flags`
section for the anti-patterns; checklists whose steps end on a checkable
`Done when:` criterion; and a no-op path for when the conditions do not apply.

**Naming:** verb-first, kebab-case — `specify-behavior`, `inspect-change`.
Engineering skills carry no prefix; Personal OS skills are namespaced `life-`
because their bare verbs would collide once both packs are installed.

**Budget:** discipline skills keep the core body to ~500 words; the hard ceiling
for any SKILL.md is ~500 lines / 5k words. Past that, split detail behind a
well-worded pointer to a sibling file, one level deep.

**Evidence files beside the skill:** `TESTS.md` holds the recorded RED/GREEN
evidence — transcripts, the rationalizations the text had to counter, what
changed between iterations. `eval.json` holds the runnable assertions derived
from it. A `behavior` or `trigger` eval must cite `TESTS.md`; a `contract` eval
may only assert what SKILL.md's own text already states.
`scripts/lint-skill-evals.py` enforces the split, which is what stops the repo
filling with plausible assertions for failures nobody observed.

**Skills are test-driven.** No new skill and no edit to a skill ships without a
failing test first: run the scenario without the skill (for an edit, with the
current version), record the failures verbatim, then write the smallest text that
answers them. If the baseline does not fail, stop — text with no failure behind
it is a no-op, and it is paid for on every run.

---

## 8. File Organization

**This repository** ships the skill set. It deliberately does *not* carry the
per-repo artifacts the skills create — those belong to the repos that adopt it.

```
skills/
  meta/ setup/ discovery/ spec/ execution/ review/    # engineering (default plugin)
  acceptance/ craft/ ship/ track/ project/
  engineering/                                        # package index README only
  personal/                                           # Personal OS, opt-in, life-* prefix
templates/          # seeds the skills write into a consuming repo, + personal-os/
  agents/           # project.md, issue-tracker.md, triage-labels.md templates
hooks/              # hooks.json + session-start.sh (the gate-session injector)
scripts/            # the four lint passes lefthook runs
docs/
  guide/            # the human tutorial and per-skill pages
  design/           # design records, including tested no-ops
  releases/ personal-os/
.skills/            # git-ignored ephemera: .skills/<CODE>/ per feature;
                    # shared pathfind/, research/, decisions/, pr-packages/
```

**A consuming repo** is where `configure-repo` and the spec skills write:
`docs/agents/project.md` (verify commands, release steps, project posture, Team
roster), `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`,
`docs/specs/<feature>/` (the triad) with `docs/specs/INDEX.md`, `CONTEXT.md` (the
glossary), `docs/adr/`, `docs/architecture/` (the `ARCH-N` spine),
`docs/roadmap/INDEX.md`, and `docs/quality/debt.md`. Skills read these at runtime;
when one is missing, say so once per session and suggest `configure-repo` rather
than inventing the content.

**Packages:** engineering and Personal OS install independently. Personal skills
run on a **secretary default** — management only. The Iron Laws above govern
engineering sessions, not life-vault management.

---

## 9. Forbidden Patterns (agents MUST NEVER)

- Write production code before a failing test exists (Gate 2)
- Propose or apply a fix without root-cause investigation (Gate 3)
- Claim completion without fresh verification evidence (Gate 4)
- Quote a path-scoped test run's totals as the suite's
- Skip the tier-decision gate and start coding (Gate 1)
- Auto-invoke a user-invoked skill, or direct another skill to invoke one
- Run two implementers on the same plan in parallel
- Hand a subagent the whole plan file — the brief is its world
- Use `HEAD~1` as a review base instead of the recorded `BASE`
- Skip re-review after a fix, or accept a review missing either verdict
- Move to the next task with open Critical/Important findings
- Fix reviewer findings in the controller context — dispatch a fixer
- Pause for permission between tasks under continuous `build-in-waves` /
  `build-inline` (human stops belong to `build-by-story`)
- Re-dispatch a task the ledger marks complete
- Start implementation on main/master without explicit user consent
- Tell a reviewer what not to flag, or pre-rate a finding's severity
- Dispatch a reviewer without a diff package
- Keep untested code "as reference" while writing tests
- Write all tests up front, then all code — work one vertical slice at a time
- Mock internal collaborators, or assert on a mock's existence or call count
- Put workflow steps in a skill's `description` frontmatter
- Ship skill text for a failure no baseline run produced

---

## 10. Quality Standards — Definition of Done

A change is done ONLY when ALL of the following hold:

- Every new behavior has a test that was watched failing first, for the expected
  reason — error paths and boundary values count as behaviors
- The whole suite is green and the output pristine: zero warnings, zero errors
- Every new behavior maps to a requirement in the brief or report (IDs stay in
  docs)
- Mocks only at system boundaries, complete data structures, no assertions on
  mocks
- `audit-trace` clean — no task citing an unknown ID, no duplicate definitions
- The progress ledger carries a line for every completed task
- `inspect-change` clean on both axes (Standards and Spec)
- `validate-feature` has confirmed the user-facing behavior on the running system
- Feature status updated: Draft → Approved → Implemented → Shipped

Can't tick a box? The work is not done.

---

## 11. Quick Reference: Every Skill

**Legend:** (m) model-invoked · (U) user-invoked · (si) session-injected

| Category | Skills |
|---|---|
| **meta** (4) | `gate-session` (m, si), `ask-me-bro` (U), `author-skills` (U), `teach-pack` (U) |
| **setup** (2) | `configure-repo` (U), `bootstrap-repo` (U) |
| **discovery** (10) | `frame-change` (m), `clarify-decisions` (m), `solve-problem` (m), `research` (m), `run-spike` (m), `define-domain` (m), `pathfind` (U), `interpret-session` (U), `deepen-codebase` (U), `work-the-problem` (U) |
| **spec** (3) | `specify-behavior` (m), `design-solution` (m), `plan-tasks` (m) |
| **execution** (10) | `build-in-waves` (m), `build-by-story` (m), `build-inline` (m), `execute-common` (m), `test-first` (m), `root-cause` (m), `prove-claim` (m), `audit-trace` (m), `load-subgraph` (m), `isolate-workspace` (m) |
| **review** (7) | `inspect-change` (m), `polish-diff` (m), `vet-feedback` (m), `review-invariants` (m), `study-change` (U), `brief-team` (U), `select-review-sample` (U) |
| **acceptance** (6) | `validate-feature` (m), `validate-api` (m), `validate-ui` (m), `review-product-flow` (m), `vet-product-flow` (m), `run-product-walkthrough` (m) |
| **craft** (1) | `craft-page` (m) |
| **ship** (4) | `package-change` (m), `land-branch` (m), `record-verdict` (m), `cut-release` (U) |
| **track** (11) | `amend-feature` (m), `reroute-plan` (m), `realign-spec` (m), `triage` (U), `record-debt` (U), `refresh-roadmap-status` (U), `assess-milestone` (U), `scan-architecture` (U), `map-features` (U), `write-handoff` (U), `publish-issues` (U) |
| **project** (4) | `plan-milestones` (m), `define-project` (U), `define-system-doc` (U), `assess-pivot-impact` (U) |
| **personal** (18) | Personal OS, `life-` prefixed, opt-in — see `skills/personal/README.md` |

**Execute family — pick one after an approved `tasks.md`:**

| Skill | When |
|---|---|
| `build-in-waves` | Subagent waves (writes `Execution-mode: continuous`) |
| `build-by-story` | Human-gated review units (writes `Execution-mode: story-unit`) |
| `build-inline` | No implementer subagents; the user watches the controller implement |

**Main flow:** `frame-change` (+ `load-subgraph`) → `specify-behavior` →
`design-solution` → `plan-tasks` → `isolate-workspace` → execute family →
`inspect-change` (+ `load-subgraph`) → `polish-diff` → `validate-feature` →
`package-change` → `land-branch` → `/cut-release` → `realign-spec`.

**Bugfix flow:** `root-cause` → mini-spec → `test-first` → `prove-claim` →
`inspect-change` → `land-branch`.

**Program layer (optional):** `/define-project` (vision + the `ARCH-N` spine) →
`plan-milestones` (`MILE-N` / `ROAD-N` in `docs/roadmap/INDEX.md`) → the feature
flow above, one roadmap item at a time. Every edit to an existing roadmap — a
dropped item, a reorder, a commit or close — goes through `plan-milestones`,
never a direct file edit. A pivot that collides with shipped code goes through
`/assess-pivot-impact` first.

**Maintenance:** `amend-feature` (small in-scope changes), `/triage` (incoming
issues), `realign-spec` (spec drift), `/scan-architecture` (periodic deepening),
`/map-features` (brownfield ID and Files backfill), `/record-debt` (bank a
finding judged real and left unfixed).

**Human how-to:** [`docs/guide/START-HERE.md`](docs/guide/START-HERE.md).

---

*This constitution is enforced. Read it first. Follow it always. No exceptions.*

## Agent skills

This repo is configured for a spec-driven skill set.

- Feature flow: `frame-change` (+ `load-subgraph`) → `specify-behavior` →
  `design-solution` → `plan-tasks` → execute family → `inspect-change` →
  `validate-feature` → `land-branch`
- Bug on-ramp: `root-cause` (root cause first, then a guarded fix)
- Ambiguous problem, or a solution requested with no clear gap: `solve-problem`
- Capture a conversation, spec, or idea into tracker issues: `/publish-issues`
- Multi-session decision map (Layer 0 fog): `/pathfind`
- Incoming issues and PRs: `/triage`
- Brownfield feature-ID / Files backfill: `/map-features`
- Traceability check: `audit-trace` — run by `prove-claim` and `/cut-release`;
  keep it clean
- Horizontal neighbors: `load-subgraph` — advisory, live specs only
- Project docs: `/define-project` maintains `docs/product/vision.md`, the
  `docs/architecture/` invariant spine, and `docs/product/guidelines.md`
- Pivot against shipped code: `/assess-pivot-impact` produces the disposition
  ledger before any vision or architecture rewrite
- Tutorial: [`docs/guide/START-HERE.md`](docs/guide/START-HERE.md)

Repo config the skills read:

- Verify commands, release steps, posture, Team: `docs/agents/project.md`
- Issue tracker operations: `docs/agents/issue-tracker.md`
- Triage label mapping: `docs/agents/triage-labels.md`
