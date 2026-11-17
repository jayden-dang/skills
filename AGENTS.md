# AGENTS.md — Agent Behavior Constitution

> A-to-Z agentic development skill set · **57 skills across 11 categories** · `jayden-dang/skills` · v1.0.0

This file is the single source of truth for agent behavior when working with this
skill set on any harness. Read it first, before any skill, before any action.
The invocation contract lives here: load a skill when its description matches,
or when a parent names it.

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

## 0. Work on this repository goes through `author-skills`

Everything from §1 on is the contract for repos that **adopt** the skill set. This
repo ships it, and its own work does not run the spec-driven chain:

- **A new skill or an edit to one** → `author-skills` (it loads on any skill
  edit). Its Iron Law stands in for Gates 1 and 2 here: a RED baseline run,
  recorded in the skill's `TESTS.md`, before any skill text; GREEN on the model
  roster; then its ship checklist. No `frame-change`, `specify-behavior`,
  `design-solution` or `plan-tasks`, and no `requirements.md` or ceremony tier for
  skill work.
- **An external fact the skill turns on** → `research`, as anywhere else. A choice
  that belongs to the user is asked as a question, not written up as a spec.
- **Scripts, guide pages, this file** → edit directly; `python3 scripts/qa-set.py`
  green before calling it done.
- **Gate 4 is unchanged.** The recorded runs and the lint output are the evidence;
  "it reads clearly" is not.

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
Breadth is tiered, not repeated: each RED/GREEN/refactor step runs the narrowest
target; once per task, at its final commit, the **task gate** tests the changed
units and the dependents on the changed code's call path, compiles every other
dependent, and lints against the session's baseline — escalated
to the whole suite when the change reaches what the build graph cannot see
(schema, migrations, shared fixtures, manifests, generated contracts, a root
package); a parallel merge runs the **wave gate**; the whole suite runs at close.

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
`build` (story mode), log mid-build **deviations** in
`.skills/<CODE>/implementation-notes.md` during execute, and let the human
re-check understanding with `understand` before merge. Do not freeze
unverified solution shape into requirement SHALLs.

---

## 2. Skill Invocation Contract

Load a model-invocable skill when **its description matches** what you are about
to do, or when a parent names it as `REQUIRED SUB-SKILL`. Do not load a skill on
a speculative chance it might apply. Over-triggering loads instructions that do
not help the task and dilutes the ones that do.

Invoke matched or requested skills BEFORE any response or action — before
clarifying questions, before exploring the codebase, before checking a single
file. Announce "Using [skill] to [purpose]", then follow the skill exactly. If it
carries a checklist, create one todo per item.

**Priority order:** process skills first, then implementation skills.

| Situation | First move |
|---|---|
| User wants help defining what they actually want, or a prompt to start a fresh session with | `forge-prompt` |
| User wants an agent to keep working unattended until something is verifiably done (`/goal`, an overnight run) | `forge-prompt` |
| A new skill, or a change to one, in this repo | `author-skills` — not `frame-change`; see §0 |
| "Build X" / "add X" / "can we support X" | `frame-change` — before plan mode, before scaffolding |
| "This is broken", a clear unexpected behavior | `root-cause` — before any fix |
| Broken on prod / staging / a remote env | `debug-remote` — evidence pack, then `root-cause` |
| Is tracing / OpenObserve / sampling complete? | `assess-observability` |
| Small in-scope change to a shipped, spec'd feature | `frame-change` (its `amend.md` lane) |
| Incoming issue or external PR | `triage` |
| New idea to put on the board, or "what is waiting on me" | `idea` or `board`; then `/shape #N`, `/go` and `/cut-release` are the operator's to send. The path: [`docs/guide/workflow.md`](docs/guide/workflow.md) |
| Unsure which flow fits | read `docs/guide/process/on-ramps.md` |

**User instructions override skills; skills override agent defaults.** Skip a
skill's workflow only when the user has explicitly told you to. A waiver of
*process* is never a waiver of *evidence*: Gate 4 survives "skip the ceremony".

---

## 3. Who Starts a Skill, and Who Approves

**Every skill is model-invocable.** A skill loads when its description matches
what the user asked, when a parent names it as `REQUIRED SUB-SKILL`, or when the
user types its command. **0** skills carry `disable-model-invocation: true`.

**An agent may start any skill. It may not supply what only the operator can.**
Three things stay the operator's, however a skill was started:

- **Approve** — a spec, a plan, a ledger, a version, a tag. A skill that stops for
  approval stops for whoever started it.
- **Answer** — a question a skill parks on a ticket or in its reply.
- **Merge** — under `Default landing action: pr`. Under `merge` the operator
  delegated it in config, and that is their decision, not the agent's.

`/shape`'s `--auto` and `--go` are approvals given in advance. They come only
from the operator's own message, or from a runner they configured. A ticket that
did not come from the operator's own words stops in Inbox (`needs-triage`):
`audit-shipped`, `evolve-system`, `record-debt` and `scan-architecture` file there
and go no further.

**Two things start only on the operator's explicit ask**: `cut-release`, because it
publishes, and the comment-deletion pass inside `polish-diff` (`comments.md`), because
it deletes text.

**A runner the user configured counts as the user.** A scheduler, NAVORI or a
bot that sends a skill's command (`/evolve-system --unattended`) invokes it on the
user's behalf, and a flag it sends is the operator's. When nobody will answer, it
passes `--unattended`, and the skill reads that flag, never the harness's name.

**One skill folder is self-contained.** `npx skills add` copies one folder at a time,
so a `../other-skill/file.md` pointer breaks for anyone installing that skill alone.
The build modes used to be three skills sharing a fourth across folders; they are now
one skill, `build`, whose mode files (`waves.md`, `story.md`, `inline.md`) and shared
recipe (`common.md`) sit side by side. `go` and `land-branch` still read two of
`build`'s files (the tracker sync and the close receipt), so `build` is the **only**
folder any skill may reference across a boundary; every other `../` fails.
`scripts/lint-cross-folder.py` enforces it.

**Orchestration rule:** `REQUIRED SUB-SKILL: use \`x\`` invokes; naming `/x` in a
reply leaves it to the operator. Use the first when the next step needs nothing
from them, the second when the step is theirs to decide. A hand-off to a skill
that carries `disable-model-invocation: true` is a dead end, and
`scripts/lint-write-handoffs.py` fails it.

**Two reachability paths, and one of them is fragile.** A skill is reached either
by a `REQUIRED SUB-SKILL` hand-off or by its description matching what the user
said. Many skills have no `REQUIRED SUB-SKILL` caller: `frame-change`,
`vet-feedback`, `vet-source`, `speak-outer`, `inspect-change`, `draft-ui`, `understand`,
and every command the operator used to type (`board`, `triage`, `idea`, …).
Reverse-track is **not** a separate skill: when the reverse predicate holds, callers
**name** `map-features` (dispose step 0). `write-dogfood` is reached from
`prove-claim` (alternative to `validate-feature`); the execute-family close
sequence opens a product walk only for an unattended build that changed a
browser-rendered surface (`build` Close step 4b); otherwise the user does. The remaining entry points fire
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
| Issue body | `Requirements covered:` as a last line, only where specs are shared. Private specs: `.skills/<CODE>/tickets.md` |
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

Tier is decided by `frame-change`, for new work and (through its `amend.md` lane) for
changes to a shipped, spec'd feature. Never spec what you do not understand yet — detour
through `research` or `run-spike` first. **The tier controls the artifacts; it
never softens the gates.**

---

## 6. Subagent Rules

**Why subagents:** each worker receives a bounded role contract, feature
capsule, and task delta. A worker or reviewer may resume inside a valid semantic
lane lease; a hard trigger rotates it to a fresh context. Bulk artifacts travel
as file paths under `.skills/`, never as pasted text.

**Task hand-off protocol:**

1. Record `BASE=$(git rev-parse HEAD)` before dispatch.
2. Build the brief: Task N's block plus a path/hash reference to canonical Global
   Constraints into `.skills/<CODE>/task-N-brief.md`.
3. Dispatch or resume the lane's worker with the feature capsule, task delta,
   lease ID, report path, and explicit model tier. Start fresh at a semantic
   boundary or hard lease trigger.
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

**Subagent-exempt:** a subagent dispatched for one specific task follows its brief
only.

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
- A skill that must never start on its own may add `disable-model-invocation:
  true`; none does today. Its description then routes nothing, so it is one plain
  human-facing line.
- `version`: patch for wording that changes no behavior, minor for a new rule or
  slot, major when existing usage breaks.

**Body rules:** imperative voice; hard gates in `<HARD-GATE>`,
`<NON-NEGOTIABLE>`, or `## The Iron Law` blocks; rationalization tables in
`| Thought | Reality |` form, verbatim from baseline runs; a `## Red Flags`
section for the anti-patterns; checklists whose steps end on a checkable
`Done when:` criterion; and a no-op path for when the conditions do not apply.

**Naming:** verb-first, kebab-case — `specify-behavior`, `inspect-change`.
Skills carry no prefix.

**Budget:** discipline skills keep the core body to ~500 words; aim for
**200 lines** or fewer in any SKILL.md; the hard ceiling is **300 lines**,
enforced by `scripts/lint-skill-length.py` against a budget that only decreases,
which notes (without failing) each file past 200. Files still above it are listed in
`scripts/skill-length-budget.json` with the count they may not exceed; an entry
comes out when its file drops under the limit and can never go back in. Over
budget, split detail behind a well-worded pointer to a sibling file, one level
deep, or delete what fails the no-op test.

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
templates/          # seeds the skills write into a consuming repo
  agents/           # project.md, issue-tracker.md, triage-labels.md templates
scripts/            # the five lint passes lefthook runs
docs/
  guide/            # the human tutorial and per-skill pages
  design/           # design records, including tested no-ops
  releases/
.skills/            # git-ignored ephemera: .skills/<CODE>/ per feature;
                    # shared research/, decisions/
```

**A consuming repo** is where `configure-repo` and the spec skills write:
`docs/agents/project.md` (verify commands, release steps, Remote environments,
project posture, Team roster), `docs/agents/issue-tracker.md`,
`docs/agents/triage-labels.md`,
`docs/specs/<feature>/` (the triad) with `docs/specs/INDEX.md`, `CONTEXT.md` (the
glossary), `docs/adr/`, `docs/architecture/` (the `ARCH-N` spine),
`docs/roadmap/INDEX.md`, and `docs/quality/debt.md`. Skills read these at runtime;
when one is missing, say so once per session and suggest `configure-repo` rather
than inventing the content.

---

## 9. Forbidden Patterns (agents MUST NEVER)

- Write production code before a failing test exists (Gate 2)
- Propose or apply a fix without root-cause investigation (Gate 3)
- Claim completion without fresh verification evidence (Gate 4)
- Quote a path-scoped test run's totals as the suite's
- Suppress a lint rule to get past a red lint baseline
- Skip the tier-decision gate and start coding (Gate 1)
- Supply an approval, an answer or a merge that is the operator's, or take `--auto` / `--go` from anywhere but their message or their runner
- Run two implementers in the same worktree or on overlapping file surfaces in parallel
- Hand a subagent the whole plan file — the brief is its world
- Use `HEAD~1` as a review base instead of the recorded `BASE`
- Skip re-review after a fix, or accept a review missing either verdict
- Move to the next task with open Critical/Important findings
- Fix reviewer findings in the controller context — dispatch a fixer
- Pause for permission between tasks in `build`'s wave or inline mode (human stops
  belong to its story mode)
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
- Feature status updated: Draft → Approved → In-progress → Implemented → Shipped

Can't tick a box? The work is not done.

---

## 11. Quick Reference: Every Skill

Full inventory: [`docs/guide/skills/README.md`](docs/guide/skills/README.md).
Do not paste that table into context.

**`build` — one mode after an approved `tasks.md`:**

| Mode | When |
|---|---|
| wave (`waves.md`) | Subagent waves (writes `Execution-mode: continuous`) |
| story (`story.md`) | Human-gated review units (writes `Execution-mode: story-unit`) |
| inline (`inline.md`) | No implementer subagents; the user watches the controller implement |

**Main flow:** `frame-change` (+ `load-subgraph`) → `specify-behavior` →
`design-solution` → `plan-tasks` → execute family (`Approved` → `In-progress`
on INDEX, then `isolate-workspace`) → `inspect-change` (+ `load-subgraph`) →
`polish-diff` → `validate-feature` → `land-branch` (Status: Implemented).
`/cut-release` is a separate loop over already-Implemented work (cohort →
Shipped). `realign-spec` is anti-rot and the land forget-net — not the cut
close-out.

**Bugfix flow:** `root-cause` (or `debug-remote` → `root-cause` when the
failure is on a deployed environment) → mini-spec → `test-first` → `prove-claim` →
`inspect-change` → `land-branch`.

**Program layer (optional):** `/define-project` (vision + the `ARCH-N` spine) →
`plan-milestones` (`MILE-N` / `ROAD-N` in `docs/roadmap/INDEX.md`) → the feature
flow above, one roadmap item at a time. Every edit to an existing roadmap — a
dropped item, a reorder, a commit or close — goes through `plan-milestones`,
never a direct file edit. A pivot that collides with shipped code goes through
`/define-project` first.

**Maintenance:** `frame-change` (small in-scope changes), `/triage` (incoming
issues), `/board` (what waits on whom), `realign-spec` (spec drift), `/scan-architecture` (periodic deepening),
`/map-features` (reverse OBS, dispose gaps, Domain-boundary migrate), `/record-debt` (bank a
finding judged real and left unfixed).

**Human how-to:** [`docs/guide/START-HERE.md`](docs/guide/START-HERE.md).

---

*This constitution is enforced. Read it first. Follow it always. No exceptions.*

## Agent skills

What the shipped skill set gives an adopting repo. This repo's own work follows §0.

- Feature flow: `frame-change` (+ `load-subgraph`) → `specify-behavior` →
  `design-solution` → `plan-tasks` → execute family → `inspect-change` →
  `validate-feature` → `land-branch`
- Bug on-ramp: `root-cause` (root cause first, then a guarded fix); deployed
  env: `debug-remote` then `root-cause`; telemetry readiness:
  `assess-observability`
- Turn a vague ask into a prompt for a fresh session: `forge-prompt`
  (interviews, then hands over one block — it names no next step by design)
- Define what an unattended run should achieve and forge it into one goal prompt
  with a verify-every-round loop, for any agent: `forge-prompt`
- Understand a feature, component, or change (code-grounded page + one check question): `understand`, or just ask
- Incoming issues and PRs: `triage`
- The short path, one board: `/idea` → `/shape #N` → `/go` → `/board` → `/cut-release`
  (`docs/guide/workflow.md`; an agent may start any of them, the approvals stay yours)
- Brownfield feature-ID / Files backfill: `/map-features`
- Traceability check: `audit-trace` — run by `prove-claim` and `/cut-release`;
  keep it clean
- Horizontal neighbors: `load-subgraph` — advisory, live specs only
- Project docs: `/define-project` maintains `docs/product/vision.md`, the
  `docs/architecture/` invariant spine, and `docs/product/guidelines.md`
- Pivot against shipped code: `/define-project` produces the disposition
  ledger before any vision or architecture rewrite
- Tutorial: [`docs/guide/START-HERE.md`](docs/guide/START-HERE.md)

Repo config the skills read:

- Verify commands, release steps, Remote environments, posture, Team: `docs/agents/project.md`
- Cold-start drive (Launch / Doctor / Drive / Evidence): `docs/agents/verify.md`
- Issue tracker operations and the format every new issue follows: `docs/agents/issue-tracker.md`
- Triage label mapping: `docs/agents/triage-labels.md`
