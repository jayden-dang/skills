# Design: A-to-Z Agentic Development Skill Set

**Date:** 2026-07-07
**Status:** Approved
**Repo:** `jayden-dang/skills`

## Vision

One skill set that carries a project from ideation to release, with **requirements
traceability as the spine**: hard process gates, disciplined execution loops, and
spec-driven development in which every task, test, and commit traces back to an
individually addressable requirement.

### Principles

1. **Predictability is the root virtue**: a skill exists to wrangle determinism
   out of a stochastic system — the agent takes the same process every run.
2. **Traceability is the memory**: intent lives in persisted, individually
   addressable requirements — not chat history. Every task, test, and commit
   points at a requirement ID. A script, not diligence, keeps this honest.
3. **Gates, not vibes**: no code before an approved spec; no fix before a root
   cause; no completion claim without fresh evidence.
4. **Ceremony scales with the task**: a three-tier system prevents pages of spec
   for a trivial change.
5. **Tracker-agnostic, configured once per repo**: skills read repo config from
   `docs/agents/*.md`; GitHub Issues, GitLab, or local markdown all work.
6. **Small skills that compose**: user-invoked skills orchestrate; model-invoked
   skills hold reusable discipline. A user-invoked skill may invoke model-invoked
   skills, never another user-invoked one.

## Repository architecture (this repo)

```
skills/
  meta/        using-skills, ask, writing-skills
  setup/       setup-repo, scaffold-project
  discovery/   brainstorm, grilling, research, prototype, domain-modeling
  spec/        write-requirements, write-design, write-plan
  build/       execute-plan, tdd, debug, verify, worktrees
  review/      code-review, receive-review
  ship/        finish-branch, release
  track/       triage, sync-spec, improve-architecture, handoff
scripts/       check-trace.mjs, task-brief, review-package
templates/     requirements.md, design.md, tasks.md, docs/agents seeds, CONTEXT.md seed
hooks/         session-start (injects meta/using-skills)
docs/          per-skill human docs (optional, later)
.claude-plugin/plugin.json   (Claude Code plugin manifest)
```

- **Installation:** `npx skills@latest add jayden-dang/skills` (skills.sh) or as a
  Claude Code plugin. Dev mode: a `link-skills.sh` that symlinks into
  `~/.claude/skills` so `git pull` keeps skills current.
- **Activation:** a `SessionStart` hook (matcher `startup|clear|compact`) injects
  the full text of `meta/using-skills` so the skill-check gate survives
  compaction. When installed via skills.sh (no hook support), `setup-repo` offers
  to add the hook to the project's settings.
- **Conventions:** verb-first skill names; frontmatter descriptions state
  *triggering conditions only, never the workflow* (a description that summarizes
  the workflow tempts the agent to follow the summary and skip the skill body);
  cross-references as `REQUIRED SUB-SKILL:` prose, never `@`-links; user-invoked
  skills carry `disable-model-invocation: true`.

## The artifact model (in consuming repos)

```
docs/specs/<YYYY-MM-DD>-<feature>/
  requirements.md      # WHAT — EARS acceptance criteria with hierarchical IDs
  design.md            # HOW — architecture, each section cites the REQ IDs it satisfies
  tasks.md             # PLAN — checkbox tasks, each ending `_Requirements: CODE-N.M, ..._`
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

`scripts/check-trace.mjs` parses the spec inventory + test files/reports + task
footers and **fails** on: implemented requirements with zero covering tests; tests
or tasks citing nonexistent IDs; approved specs with uncovered requirements
(warning tier). Run by `verify`, `release`, and CI. Unchecked trace matrices rot —
so trace checking is automated lint, not a manual audit.

### Ceremony tiers

| Tier | When | Artifacts |
|---|---|---|
| **0 — trivial** | typo-level, no behavior change | none — tdd/verify only |
| **1 — bugfix / small change** | behavior change ≤ ~half a day | mini-spec: add a fix REQ + a SHALL-CONTINUE-TO guard to the owning feature's requirements.md (or `docs/specs/fixes.md`), tagged regression test; no design.md, task list optional |
| **2 — feature** | multi-task work | full triad + execute-plan |

`brainstorm` and `ask` decide the tier explicitly and say so. Never spec what you
don't understand yet — spike via `prototype`/`research` first (specs are an
execution tool, not a discovery tool).

## Skill inventory

Legend: (U) user-invoked, (m) model-invoked.

### meta/
1. **using-skills** (m, session-injected) — the gate. 1%-rule ("if there is even
   a 1% chance a skill applies, invoke it"), skill-check before ANY response,
   red-flags table, process-skills-before-implementation-skills priority, user
   instructions override skills.
2. **ask** (U) — router. Maps situations to flows; documents the main idea→ship
   chain, the bugfix on-ramp, the maintenance loop, and context hygiene (do
   discovery→spec in one unbroken context window; handoff near the smart zone).
3. **writing-skills** (U) — TDD for skills (no skill without a failing
   pressure-test first; RED/GREEN/REFACTOR with subagent pressure scenarios) +
   the authoring vocabulary (leading words, completion criteria, no-op test,
   negation, information hierarchy). The standard every skill here is written
   against.

### setup/
4. **setup-repo** (U) — run-once per repo. One-decision-at-a-time wizard: issue
   tracker (GitHub/GitLab/local markdown), triage-label mapping, docs layout,
   **verify commands** (typecheck/lint/unit/e2e — consumed by tdd, verify,
   execute-plan, release), **release steps**, feature-code registry location.
   Writes `docs/agents/*.md` + an `## Agent skills` block into CLAUDE.md. Offers
   to install the session-start hook and CI trace check.
5. **scaffold-project** (U) — greenfield bootstrap: grills stack/layout
   decisions, scaffolds repo (test harness, formatter/linter, pre-commit, CI
   stub, README, CONTEXT.md seed, docs/specs/INDEX.md), then runs setup-repo.
   Ends with a verified "hello world + one passing test" baseline.

### discovery/
6. **grilling** (m) — the interview primitive: relentless, one question at a
   time, recommended answer per question, walk every branch of the decision
   tree; **facts are looked up in the codebase, decisions belong to the human**;
   confirmation gate before enacting anything.
7. **brainstorm** (U) — HARD GATE: no code, no scaffolding until requirements
   are approved. Explore context → grilling with domain-modeling side effects →
   detours to research/prototype when a question needs evidence → 2–3 approaches
   with a recommendation → decide ceremony tier and decompose multi-subsystem
   work. Terminal state: invoke write-requirements (tier ≥1) — no other exit.
8. **research** (m) — background investigation against primary sources; every
   claim traced to the source that owns it; output = one cited markdown file
   where the repo keeps such notes. Optionally fans out multiple search angles +
   adversarial verification for high-stakes questions.
9. **prototype** (m) — throwaway code that answers a question. LOGIC branch
   (terminal UI over a pure logic module) / UI branch (3 structurally different
   variants on one route). The answer is the only thing worth keeping — capture
   it in an ADR/requirement/commit, then delete or absorb.
10. **domain-modeling** (m) — challenge terms against CONTEXT.md, stress-test
    with edge cases, cross-reference with code, update glossary inline (never
    batch); ADRs only when hard-to-reverse AND surprising AND a real trade-off;
    ADRs are 1–3 sentences.

### spec/
11. **write-requirements** (m) — produce `requirements.md`: feature code
    (registered in docs/specs/INDEX.md), numbered stories, EARS acceptance
    criteria (`WHEN/WHILE/IF-THEN/WHERE … THE SYSTEM SHALL …`) with hierarchical
    IDs, SHALL-CONTINUE-TO guards for touched existing behavior, explicit
    Out-of-Scope section. Self-review: ambiguity scan ("could any requirement be
    read two ways? pick one"), testability check (every criterion independently
    verifiable), placeholder scan. Then a **user approval gate** on the written
    file. IDs are immutable once approved — superseded requirements are struck
    through, never renumbered.
12. **write-design** (m) — `design.md`: architecture, file map, data flow; every
    section carries `Satisfies: <IDs>`; seams for testing pre-agreed here (the
    tdd skill will refuse tests at unconfirmed seams); design-it-twice (parallel
    divergent design subagents) for the hard parts; deep-module discipline
    (deletion test, interface-is-the-test-surface, one-adapter-means-a-
    hypothetical-seam). Coverage self-check: every requirement maps to a design
    section. Approval gate.
13. **write-plan** (m) — `tasks.md`: header with Goal/Architecture/Tech Stack,
    **Global Constraints** copied verbatim from the spec, File Structure first,
    per-task **Files/Interfaces** blocks, bite-sized TDD steps with exact
    commands and expected output, **no-placeholder rule** — plus each task is a
    **vertical slice** (demoable end-to-end, prefactoring first) and each task
    ends `_Requirements: CODE-N.M, ..._`. Machine-checkable coverage:
    check-trace verifies every requirement is cited by ≥1 task before execution
    starts. Optional final step: publish tasks as tracker issues (native
    sub-issues + blocking edges) with `Requirements covered` in each body.

### build/
14. **execute-plan** (m) — fresh subagent per task via file handoffs
    (`scripts/task-brief`, `scripts/review-package`; artifacts in `.skills/`);
    implementer contract with four statuses (DONE / DONE_WITH_CONCERNS /
    NEEDS_CONTEXT / BLOCKED) and TDD evidence in reports; two-verdict task
    review (spec compliance vs code quality — the spec verdict checks the
    task's cited requirement IDs); explicit model tiering per dispatch;
    **progress ledger** appended per task (compaction/crash recovery: trust the
    ledger and git log, never memory); continuous execution (no "should I
    continue?" prompts); final whole-branch review then ONE fix subagent for
    all findings. Inline fallback mode for harnesses without subagents.
15. **tdd** (m) — Iron Law: **NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST**
    (wrote code first? delete it — no exceptions), verify-RED and verify-GREEN
    mandatory, pristine output; **test only at pre-agreed seams** from
    design.md; tautological-test ban (expected values from an independent
    source of truth); mock only at system boundaries; every test carries its
    requirement ID (Playwright tag / Vitest annotate or name / Rust doc
    comment). Full rationalization table + red flags.
16. **debug** (m) — Iron Law: NO FIXES WITHOUT ROOT CAUSE. Phase 1 is the
    **red-capable command gate**: a fast, deterministic, agent-runnable
    pass/fail signal must exist and have been run before any theory-building
    ("build the right feedback loop and the bug is 90% fixed"), with ordered
    loop-construction tactics. Then: pattern analysis → single falsifiable
    hypothesis → one-variable fixes; **≥3 failed fixes = stop, question the
    architecture**. Exit: regression test at a correct seam + a
    SHALL-CONTINUE-TO guard requirement added to the owning spec (tier 1
    mini-spec), post-mortem hands to improve-architecture.
17. **verify** (m) — Iron Law: NO COMPLETION CLAIMS WITHOUT FRESH EVIDENCE. The
    Gate Function (IDENTIFY the proving command → RUN full and fresh → READ
    output → VERIFY it confirms → only then claim); claim→evidence table;
    "requirements met" claims require `check-trace` pass + per-ID checklist
    against acceptance criteria, not just green tests.
18. **worktrees** (m) — native-tool-first isolation, `.worktrees/` fallback with
    git-ignore check, dependency setup, clean-baseline test run before work
    starts.

### review/
19. **code-review** (m) — two parallel subagents so neither pollutes the other:
    **Standards** (repo standards + a code-smell baseline, skip what tooling
    enforces) and **Spec** (diff vs the requirements: missing/partial IDs,
    scope creep, wrong implementations — every finding quotes the requirement
    ID). Reviewer hygiene: read-only review, never pre-judge findings in the
    dispatch prompt, calibrated severities, "Ready to merge? Yes/No/With fixes"
    verdict.
20. **receive-review** (m) — anti-sycophancy: no "You're absolutely right!", no
    gratitude — verify each item against the codebase, push back with reasoning
    when the reviewer is wrong, clarify ALL items before implementing any,
    YAGNI-check "implement properly" suggestions.

### ship/
21. **finish-branch** (m) — verify tests → exactly four options (merge locally /
    push + PR / keep / discard, "discard" must be typed), provenance-checked
    worktree cleanup, re-run tests after merge.
22. **release** (U) — release-prep gate: full verify (all verify commands from
    docs/agents/project.md) + check-trace clean → changelog assembled from
    commit trailers (requirement IDs give requirement-level release notes for
    free) → version bump → tag → build → smoke-check → release notes.
    Per-project steps (e.g. desktop bundling) come from setup-repo config. No
    CI/CD authoring in v1.

### track/
23. **triage** (U) — issue state machine (needs-triage / needs-info /
    ready-for-agent / ready-for-human / wontfix + bug/enhancement); redundancy +
    prior-rejection checks; verify claims before recommending; **agent briefs**
    as the contract (durable: behavioral contracts and interfaces, never file
    paths; independently verifiable acceptance criteria — which cite
    requirement IDs when touching spec'd behavior); wontfix → `.out-of-scope/`
    KB. AI-generated comments labeled as such.
24. **sync-spec** (m) — realign the triad after requirements change or
    implementation drifts: diff requirements ↔ design ↔ tasks ↔ tests; create
    tasks for new requirements; flag orphaned tests/tasks citing dead IDs;
    update Status fields (Draft → Approved → Implemented → Shipped); print the
    trace report. The anti-spec-rot skill — run whenever a spec'd feature
    changes outside its plan.
25. **improve-architecture** (U) — periodic deepening scan (friction: shallow
    modules, poor locality, untested seams; deletion test), self-contained HTML
    report of candidates, grill through the chosen one; feeds back into
    brainstorm.
26. **handoff** (U) — compact the conversation into a handoff doc in OS tmp
    (reference artifacts by path, never duplicate; redact secrets;
    suggested-skills section); optional background-agent continuation.

**Deliberately not in v1:** multi-session planning maps, full CI/CD authoring,
teaching/writing skills.

## The workflow chains

### Main flow: idea → ship (tier 2)
```
using-skills (session gate)
→ brainstorm            grilling + domain-modeling; research/prototype detours;
                        tier decision; approach chosen           [HARD GATE: no code]
→ write-requirements    EARS + IDs; approval gate on the file
→ write-design          Satisfies: per section; seams agreed; approval gate
→ write-plan            tasks with _Requirements:_ footers; coverage check;
                        (optional) publish issues
→ worktrees             isolated workspace, clean baseline
→ execute-plan          per task: brief → implementer (tdd) → review-package →
                        two-verdict review → fixes → ledger
                        [debug on failures; verify before any claim]
→ code-review           whole-branch, two-axis (Standards + Spec-by-ID)
→ finish-branch         merge / PR / keep / discard
→ release               when shipping: verify + trace gate, changelog, tag, build
→ sync-spec             mark requirements Implemented/Shipped
```
Context hygiene: brainstorm → write-plan in one unbroken context window; handoff
if approaching the smart zone; execute-plan sessions are per-task context-isolated
by design.

### Bugfix flow (tier 1)
```
debug (red-capable command → root cause → fix via tdd)
→ mini-spec: fix REQ + SHALL-CONTINUE-TO guard in the owning requirements.md
→ tagged regression test → verify → code-review (spec axis) → finish-branch
```

### Maintenance loop
```
improve-architecture (periodic) → picked candidate → brainstorm → ...
triage (incoming issues) → ready-for-agent brief → execute or implement directly
```

## Build plan

1. **Foundation:** repo scaffolding, plugin manifest, session-start hook,
   templates/, scripts/ (check-trace.mjs first — it defines the ID grammar).
2. **Spec layer:** write-requirements, write-design, write-plan (+ INDEX.md
   registry convention).
3. **Meta + discovery:** using-skills, ask, grilling, brainstorm, domain-modeling,
   research, prototype.
4. **Build + review:** tdd, debug, verify, worktrees, execute-plan (+ task-brief /
   review-package scripts), code-review, receive-review.
5. **Setup + ship + track:** setup-repo, scaffold-project, finish-branch, release,
   triage, sync-spec, improve-architecture, handoff, writing-skills.
6. **Validation:** pressure-test the gate skills with subagents; dogfood on a real
   project.
