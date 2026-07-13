# Design: A-to-Z Agentic Development Skill Set

**Date:** 2026-07-12
**Status:** Approved
**Repo:** `jayden-dang/skills`

## Vision

One skill set that carries a project from ideation to release, with **requirements
traceability as the spine**: hard process gates, disciplined execution loops, and
spec-driven development in which every task, test, and commit traces back to an
individually addressable requirement.

The set is **LLM-native and script-free**. Enforcement runs on **deterministic
primitives the agent already has** — `grep`, `git`, file reads — driven by a skill
that specifies the exact passes and the exact rules for reading them. Nothing is
installed into a consuming repo beyond the skills themselves: no Python, no
vendored linters, no CI or hook wiring.

### Principles

1. **Predictability is the root virtue**: a skill exists to wrangle determinism
   out of a stochastic system — the agent takes the same process every run.
2. **Traceability is the memory**: intent lives in persisted, individually
   addressable requirements — not chat history. Every task, test, and commit
   points at a requirement ID.
3. **Determinism comes from the primitives**: the trace check is `grep` +
   set-difference — operations that are exact no matter who runs them. A skill
   specifies the passes and the rules; the agent runs the passes and reads the
   output. The honesty lives in deterministic tools driven by a precise skill.
   (See "The trace check" below.)
4. **Gates, not vibes**: no code before an approved spec; no fix before a root
   cause; no completion claim without fresh evidence.
5. **Ceremony scales with the task**: a three-tier system prevents pages of spec
   for a trivial change.
6. **Zero mandatory tooling in the consuming repo**: adoption requires only the
   skills (plugin or npx) and markdown config. No Python, no vendored scripts, no
   CI or hook wiring is needed to get the full methodology. A hard headless gate is
   an *optional* add-on, documented separately, never the default path.
7. **Tracker-agnostic, configured once per repo**: skills read repo config from
   `docs/agents/*.md`; GitHub Issues, GitLab, or local markdown all work.
8. **Small skills that compose**: user-invoked skills orchestrate; model-invoked
   skills hold reusable discipline. A user-invoked skill may invoke model-invoked
   skills, never another user-invoked one.

## Repository architecture (this repo)

```
skills/
  meta/        using-skills, ask, writing-skills
  setup/       setup-repo, scaffold-project
  discovery/   brainstorm, grilling, research, prototype, domain-modeling
  spec/        write-requirements, write-design, write-plan
  execution/   execute-plan, tdd, debug, verify, trace, worktrees
  review/      code-review, receive-review, check-invariants
  acceptance/  acceptance-check, acceptance-api, acceptance-ui, dogfood
  ship/        finish-branch, release
  track/       amend, correct-course, triage, sync-spec, improve-architecture, handoff, file-issues
  project/     establish-project              (optional project-documentation layer)
templates/     requirements.md, design.md, tasks.md, docs/agents seeds, CONTEXT.md seed,
               product-vision.md, architecture-INDEX.md, product-guidelines.md seeds
hooks/         session-start (injects meta/using-skills)
docs/          per-skill human docs
.claude-plugin/plugin.json   (Claude Code plugin manifest)
```

The traceability discipline lives in the `trace` skill; feature-overlap detection
lives as inline grep-and-read steps inside `brainstorm` and `code-review`. Both run
on `grep`/`git` and file reads, so the whole set is `SKILL.md` and templates — a
consuming repo installs nothing executable beyond the session-start hook.

- **Installation:** `npx skills@latest add jayden-dang/skills` (skills.sh) or as a
  Claude Code plugin. Dev mode: clone the repo and either add it as a plugin, or
  symlink the skill folders into `~/.claude/skills` with a one-line shell loop
  documented in the README (no committed installer script).
- **Activation:** a `SessionStart` hook (matcher `startup|clear|compact`) injects
  the full text of `meta/using-skills` so the skill-check gate survives compaction.
  This is the one piece of scaffolding the design keeps. When installed via
  skills.sh (no plugin hook support), `setup-repo` offers to add the hook to the
  project's settings.
- **Conventions:** verb-first skill names; frontmatter descriptions state
  *triggering conditions only, never the workflow*; cross-references as
  `REQUIRED SUB-SKILL:` prose, never `@`-links; user-invoked skills carry
  `disable-model-invocation: true`.

## The artifact model (in consuming repos)

```
docs/specs/<YYYY-MM-DD>-<feature>/
  requirements.md      # WHAT — EARS acceptance criteria with hierarchical IDs
  design.md            # HOW — architecture, each section cites the REQ IDs it satisfies
  tasks.md             # PLAN — checkbox tasks, each ending `_Requirements: CODE-N.M, ..._`
docs/specs/INDEX.md    # the feature registry — feature codes, names, statuses (LLM-maintained)
CONTEXT.md             # domain glossary (terms + tight definitions + Avoid-lists)
docs/adr/NNNN-slug.md  # minimal ADRs (1–3 sentences; three-part gate)
docs/agents/           # per-repo config written by setup-repo:
  project.md           #   verify commands (typecheck/lint/test/e2e), release steps
  issue-tracker.md     #   tracker choice + wayfinding operations
  triage-labels.md     #   canonical role → repo label mapping
.out-of-scope/         # rejection knowledge base (one file per concept)
.skills/               # git-ignored ephemera: task briefs, reports, review diffs,
                       #   progress ledger (crash/compaction recovery)
```

`docs/specs/INDEX.md` is the sole feature registry. Feature overlap is discovered
on demand by searching `docs/specs/` — a live read of the specs themselves, not a
generated artifact that has to be kept fresh.

### Requirement IDs and the trace spine

`requirements.md` format — acceptance criteria use EARS (Easy Approach to
Requirements Syntax) with hierarchical IDs:

```markdown
# Requirements: <Feature Name>
Feature code: SHELL          ← short unique prefix, repo-wide registry in docs/specs/INDEX.md
Status: Draft | Approved | Implemented | Shipped

## 1. Module switching
**Story:** As a user, I want a left icon rail so I can switch modules.

- **SHELL-1.1** WHEN the app starts with no persisted module THE SYSTEM SHALL
  activate the Notes module.
- **SHELL-1.2** WHEN the user selects a module THE SYSTEM SHALL persist the
  selection and restore it on next launch.
- **SHELL-1.3** (guard) WHEN the user switches modules THE SYSTEM SHALL CONTINUE
  TO preserve unsaved editor state.
```

The ID then flows through everything:

| Artifact | Carries the ID as |
|---|---|
| `design.md` section | `Satisfies: SHELL-1.1, SHELL-1.2` line |
| `tasks.md` task | `_Requirements: SHELL-1.1, SHELL-1.2_` footer |
| Playwright test | `{ tag: ['@SHELL-1.2'] }` (grep-selectable, in JSON reporter) |
| Vitest test | `annotate('SHELL-1.2', 'requirement')` or ID in test name |
| Rust test | `/// REQ: SHELL-1.2` doc comment (greppable) |
| Commit message | `Implements: SHELL-1.2` / `Guards: SHELL-1.3` trailer |
| Issue (if tracker used) | `Requirements covered` section in issue body |

Every use is a **grep-selectable string**. That is what makes the ID a first-class
runtime object and what makes the trace check reproducible without a bundled
linter.

### The trace check

The `trace` skill (model-invoked, in `execution/`) is the vertical enforcement
layer. It does not eyeball specs — it drives a fixed sequence of deterministic
passes and applies fixed rules:

- **Define:** extract bold requirement IDs (`**CODE-N.M**`) from every
  `requirements.md`/`fixes.md` under `docs/specs/`, dropping any inside `~~…~~`
  strikethrough (retired). Read each file's `Status:` and `Feature code:` lines.
- **Cite (tasks):** extract IDs from `_Requirements:` lines in every `tasks.md`.
- **Cover (tests):** grep IDs across the repo's configured test globs. Coverage is
  **purely textual** — an ID string present in a test file counts. The skill does
  *not* judge whether the test "really" asserts the ID; that judgment would diverge
  from a deterministic check and is explicitly forbidden.
- **Diff the sets** and report:
  - **ERROR** — a task/test cites an ID with no bold definition (E1); an
    `Implemented`/`Shipped` requirement with no covering test (E2); the same ID
    bold-defined in two files (E3).
  - **WARN** — an `Approved` requirement cited by no task (W1); a `requirements.md`
    missing its `Status:` or `Feature code:` line (W2).

`verify`, `release`, `sync-spec`, and `write-plan`'s coverage check invoke `trace`.
Because the passes are `grep`/read and the rules are set operations, two agents on
the same repo reach the same finding set. Exact message wording and ordering are
not contractual — the *finding set* is.

### Feature overlap (horizontal)

The previous design maintained a generated feature graph to answer "does this idea
already exist?" and "does this diff reimplement a neighbor?". This design answers
both by search, inline in the skills that ask:

- `brainstorm`: search `docs/specs/` for the idea's candidate feature codes and key
  terms, read any matching `requirements.md`, and report overlap as summary cards
  (owned paths + Out-of-Scope) — never blocking the gate on it.
- `code-review`: grep `docs/specs/` for features whose specs name the diff's
  changed paths, and surface those neighbors to the reviewer.

`docs/specs/INDEX.md` is the registry both consult first. There is no generated
artifact to keep fresh, so nothing can go stale.

### Ceremony tiers

| Tier | When | Artifacts |
|---|---|---|
| **0 — trivial** | typo-level, no behavior change | none — tdd/verify only |
| **1 — bugfix / small change** | behavior change ≤ ~half a day | mini-spec: add a fix REQ + a SHALL-CONTINUE-TO guard to the owning feature's requirements.md (or `docs/specs/fixes.md`), tagged regression test; no design.md, task list optional |
| **2 — feature** | multi-task work | full triad + execute-plan |

`brainstorm` and `ask` decide the tier explicitly and say so. Never spec what you
don't understand yet — spike via `prototype`/`research` first.

## The project layer (optional)

Above the per-feature workflow sits an **optional** repo-level documentation layer, for
large or long-lived projects. It is authored by one user-invoked skill,
`establish-project` (create/update/validate), and consists of three durable docs:

```
docs/product/vision.md      # the product north star — problem, users, goals, non-goals, scope
docs/architecture/INDEX.md  # the architecture spine: IDed **ARCH-N** invariants (+ per-domain files)
docs/product/guidelines.md  # human-facing engineering guidelines (write-plan sources these)
```

The load-bearing idea is the **architecture spine as invariants**: not a diagram doc, but
the small set of cross-cutting rules that keep independently-built features from
diverging — each a greppable `**ARCH-N**` ID, exactly like a requirement ID. A feature
`design.md` cites the ones it relies on as `Respects: ARCH-N`, and the `trace` check
extends **one level up**: it verifies each citation points at a *live* invariant
(referential integrity — codes E4/E5/W3), while the *semantic* judgment of whether a
design truly respects an invariant is a separate, advisory, LLM-judged check
(`check-invariants`), never folded into deterministic `trace`.

The layer is **optional by construction**. Feature skills consult it through
observable-predicate, no-op-if-absent hooks (`brainstorm` checks product scope;
`write-design` cites invariants; `write-plan` folds them into Global Constraints;
`execute-plan` surfaces them per task; `code-review` runs the advisory lane). A repo that
opts into nothing behaves exactly as before — `setup-repo` gates the whole layer behind a
default-**No** decision. This repo dogfoods it: `docs/architecture/INDEX.md` holds
`ARCH-1..5` (determinism-of-trace, optionality, zero-tooling, ID immutability, sub-skill
composition), and this feature's own `design.md` cites them.

## Skill inventory

Legend: (U) user-invoked, (m) model-invoked. **36 skills.**

### meta/
1. **using-skills** (m, session-injected) — the gate. 1%-rule, skill-check before
   ANY response, red-flags table, process-skills-before-implementation priority,
   user instructions override skills.
2. **ask** (U) — router. Maps situations to flows; the main idea→ship chain, the
   bugfix on-ramp, the maintenance loop, context hygiene.
3. **writing-skills** (U) — TDD for skills + the authoring vocabulary. The standard
   every skill here is written against. This revision updates its guidance so that
   a deterministic check driven by an LLM (grep/git under a precise skill) is a
   first-class form, not an anti-pattern.

### setup/
4. **setup-repo** (U) — run-once per repo. One-decision-at-a-time wizard: issue
   tracker, triage-label mapping, docs layout, **verify commands**, **release
   steps**, feature-code registry location. Writes `docs/agents/*.md` + an
   `## Agent skills` block into CLAUDE.md. Offers to install the session-start
   hook. Writes only markdown and settings — it vendors nothing and installs no
   linter, CI step, or git hook by default. (An optional hard CI gate is documented
   for teams that want one.)
5. **scaffold-project** (U) — greenfield bootstrap: grills stack/layout decisions,
   scaffolds repo (test harness, formatter/linter, pre-commit, CI stub, README,
   CONTEXT.md seed, docs/specs/INDEX.md), then runs setup-repo. Ends with a
   verified "hello world + one passing test" baseline.

### discovery/
6. **grilling** (m) — the interview primitive.
7. **brainstorm** (U) — HARD GATE: no code until requirements are approved. Explore
   context → search `docs/specs/` for overlapping features → grilling → detours to
   research/prototype → approaches with a recommendation → tier decision.
8. **research** (m) — background investigation against primary sources.
9. **prototype** (m) — throwaway code that answers a question.
10. **domain-modeling** (m) — glossary + ADR upkeep.

### spec/
11. **write-requirements** (m) — produce `requirements.md`: EARS + hierarchical
    IDs, SHALL-CONTINUE-TO guards, Out-of-Scope. Approval gate. IDs immutable once
    approved.
12. **write-design** (m) — `design.md`: architecture, `Satisfies:` per section,
    seams agreed. Approval gate.
13. **write-plan** (m) — `tasks.md`: Global Constraints verbatim, per-task
    Files/Interfaces, TDD steps, `_Requirements:` footers. Coverage self-check via
    the `trace` skill: every requirement cited by ≥1 task before execution starts.

### execution/
14. **execute-plan** (m) — fresh subagent per task via file handoffs in `.skills/`.
    The task brief and review package are assembled by the agent directly (copy the
    task block + Global Constraints; `git log`/`git diff` into a bundle) — no helper
    scripts. Implementer contract, two-verdict task review, progress ledger.
15. **tdd** (m) — Iron Law: NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST. Test
    only at pre-agreed seams; every test carries its requirement ID.
16. **debug** (m) — Iron Law: NO FIXES WITHOUT ROOT CAUSE.
17. **verify** (m) — Iron Law: NO COMPLETION CLAIMS WITHOUT FRESH EVIDENCE.
    "Requirements met" claims require the `trace` skill clean + a per-ID checklist
    against acceptance criteria, not just green tests.
18. **trace** (m) — the traceability check (see "The trace check" above). Driven by
    `grep`/`git`/reads under fixed rules; reports E1–E3 / W1–W2 finding sets.
    Invoked by verify, release, sync-spec, and write-plan.
19. **worktrees** (m) — isolation with a clean-baseline test run before work starts.

### review/
20. **code-review** (m) — two parallel subagents: **Standards** (repo standards +
    code-smell baseline) and **Spec** (diff vs requirements, every finding quotes
    the ID). Includes an inline feature-overlap search (grep `docs/specs/` for the
    diff's paths) so a diff reimplementing a neighbor is caught. Runs the advisory
    `check-invariants` lane when an architecture spine exists.
21. **receive-review** (m) — anti-sycophancy; verify each item before implementing.
22. **check-invariants** (m) — advisory, LLM-judged invariant conformance: per
    `Respects: ARCH-N` citation, a respects/violates/unclear verdict. The semantic
    counterpart to `trace`; never a hard gate.

### acceptance/
23. **acceptance-check** (m) — pre-merge validation from the user's seat; ID-keyed
    checklist dispatched by surface.
24. **acceptance-api** (m) — drive the running backend as a real client.
25. **acceptance-ui** (m) — drive the frontend in a real browser.
26. **dogfood** (m) — the manual sibling; checkable HTML artifact.

### ship/
27. **finish-branch** (m) — verify → merge/PR/keep/discard → worktree cleanup.
28. **release** (U) — full verify + `trace` clean → changelog from commit trailers
    → version bump → tag → build → smoke-check → release notes.

### track/
29. **amend** (m) — the iteration lane for a shipped feature; routes to the lightest
    tier, always exits through `tdd`, `sync-spec` keeps the trace honest.
30. **triage** (U) — issue state machine; agent briefs as the contract.
31. **sync-spec** (m) — realign the triad after drift: diff requirements ↔ design ↔
    tasks ↔ tests via the `trace` skill; update Status fields; update INDEX.md.
32. **improve-architecture** (U) — periodic deepening scan; the natural home for
    promoting a recurring cross-cutting pattern into an architecture invariant.
33. **handoff** (U) — compact the conversation into a handoff doc.
34. **file-issues** (U) — capture a conversation, spec, or idea into tracker issues.
35. **correct-course** (m) — the mid-flight rewind decision: classifies a discovery that
    invalidates an approved plan to the lowest invalidated artifact and routes to the right
    re-entry, delegating content to `write-*` and reconciliation to `sync-spec`.

### project/
36. **establish-project** (U) — the optional project-documentation layer: authors and
    maintains `docs/product/vision.md`, the `docs/architecture/` invariant spine, and
    `docs/product/guidelines.md` (create/update/validate modes). Consulted by
    `brainstorm`, `write-design`, `write-plan`, `execute-plan`, and `code-review`;
    entirely optional — absent, the feature workflow is unchanged.

**Deliberately not in v1:** full CI/CD authoring. (The project-documentation layer —
repo-level vision + IDed architecture invariants — is now the `project/` bucket; see
"The project layer" above.)

## The workflow chains

### Main flow: idea → ship (tier 2)
```
using-skills (session gate)
→ brainstorm            grilling + domain-modeling; docs/specs/ overlap search;
                        research/prototype detours; tier decision  [HARD GATE: no code]
→ write-requirements    EARS + IDs; approval gate on the file
→ write-design          Satisfies: per section; seams agreed; approval gate
→ write-plan            tasks with _Requirements:_ footers; trace coverage check
→ worktrees             isolated workspace, clean baseline
→ execute-plan          per task: brief → implementer (tdd) → review bundle →
                        two-verdict review → fixes → ledger
                        [debug on failures; verify before any claim]
→ code-review           whole-branch, two-axis (Standards + Spec-by-ID) + overlap search
→ acceptance-check      drive the running system through the spec's user-facing
                        behaviors (API + UI); promote to tagged tests (+ dogfood)
→ finish-branch         merge / PR / keep / discard
→ release               when shipping: verify + trace gate, changelog, tag, build
→ sync-spec             mark requirements Implemented/Shipped
```

### Bugfix flow (tier 1)
```
debug (red-capable command → root cause → fix via tdd)
→ mini-spec: fix REQ + SHALL-CONTINUE-TO guard in the owning requirements.md
→ tagged regression test → verify → code-review (spec axis) → finish-branch
```

### Maintenance loop
```
amend → tier 0: tdd / tier 1: mini-spec → tdd / new scope: escalate to brainstorm
improve-architecture (periodic) → picked candidate → brainstorm → ...
triage (incoming issues) → ready-for-agent brief → execute or implement directly
```

## Boundaries

Known limits of the model, stated plainly so adopters can judge them:

- **Feature overlap is best-effort search, not a registry.** `brainstorm` and
  `code-review` find neighbors by searching `docs/specs/`; two runs may surface them
  in a different order or miss a subtly shared path. Overlap detection is advisory
  and never blocks a gate, so this is an acceptable bound.
- **There is no mandatory headless gate.** CI and git hooks run without an agent and
  cannot invoke a skill, so the trace discipline depends on the agent running
  `verify`/`release`, not on a build that fails on its own. Teams that want a hard
  gate opt into a documented CI job, outside the default path.
- **Skill-authoring QA is agent-run.** Frontmatter shape, naming, and trigger
  should-fire/should-not-fire checks live in the `writing-skills` deployment
  checklist as steps the agent performs, not a separate harness.
