# Requirements: Optional project-documentation layer

Feature code: PROJDOC
Status: Implemented
Date: 2026-07-12

<!--
Adds a repo-level documentation layer (product vision + IDed architecture
invariants) ABOVE the existing per-feature workflow. The whole layer is optional:
a repo that does not opt in behaves identically to today. "THE SYSTEM" here means
the skill set — the agent executing these SKILL.md files.

Verification: this repo validates skills by baseline runs, not an automated
harness. Every requirement below is covered by a documented baseline scenario
(recorded at plan time and cited as coverage for the `trace` check); no automated
test code is added by this feature.
-->

## 1. Author the project layer (establish-project — create mode)

**Story:** As a developer starting a large project, I want a guided skill that
produces a repo-level vision and architecture spine, so features have a durable
north star and a shared invariant set instead of drifting per-feature.

- **PROJDOC-1.1** WHEN a user invokes `establish-project` in create mode and no
  `docs/product/vision.md` exists THE SYSTEM SHALL produce `docs/product/vision.md`
  capturing at least the problem, the users, the goals, the non-goals, and the
  scope boundaries.
- **PROJDOC-1.2** WHEN a user invokes `establish-project` in create mode and no
  architecture spine exists THE SYSTEM SHALL produce `docs/architecture/INDEX.md`
  whose invariants are each identified by a bold `**ARCH-N**` ID.
- **PROJDOC-1.3** WHEN `establish-project` elicits project context from the user
  THE SYSTEM SHALL conduct that elicitation through the `grilling` sub-skill's
  single question channel.
- **PROJDOC-1.4** THE SYSTEM SHALL expose `establish-project` as a user-invoked
  skill (frontmatter `disable-model-invocation: true`) located at
  `skills/project/establish-project/`.
- **PROJDOC-1.5** WHERE a project is large enough to warrant per-domain
  architecture docs THE SYSTEM SHALL support splitting invariants across
  `docs/architecture/<domain>.md` files indexed by `docs/architecture/INDEX.md`.

For PROJDOC-1.6, PROJDOC-1.10, and PROJDOC-9.7, the **brownfield source
predicate** is satisfied when the repo contains at least one regular file beneath
a source root named `src/`, `app/`, `backend/`, `lib/`, `packages/`, or `crates/`,
or beneath a source root declared by the repo's manifest or build configuration,
after excluding `.git/`, `node_modules/`, `vendor/`, `dist/`, `build/`, `target/`,
`coverage/`, and `.next/`.

- **PROJDOC-1.6** WHEN `establish-project` runs in create mode, the brownfield
  source predicate is satisfied, AND scan-subagent capability is available THE
  SYSTEM SHALL dispatch a brownfield scan subagent before the ratification
  elicitation begins.
- **PROJDOC-1.7** WHEN the brownfield scan completes THE SYSTEM SHALL write an
  ephemeral `.skills/<slug>-scan.md` digest whose candidates are grouped as
  product-scope facts, glossary terms, architecture invariants, or engineering
  guidelines, with every candidate citing at least one concrete repository file
  or path and labeled as an observation or inference.
- **PROJDOC-1.8** WHEN a brownfield create-mode scan digest exists THE SYSTEM
  SHALL feed that digest into the `grilling` elicitation (PROJDOC-1.3) as evidence
  for the user's ratification decisions.
- **PROJDOC-1.9** (guard) WHERE a brownfield scan digest exists THE SYSTEM SHALL
  CONTINUE TO write scan-derived content to `docs/product/vision.md`,
  `CONTEXT.md`, `docs/architecture/`, or `docs/product/guidelines.md` only after
  the user ratifies the corresponding candidate through the `grilling` channel.
- **PROJDOC-1.10** (guard) WHEN `establish-project` runs in create mode AND finds
  no existing source according to the brownfield source predicate THE SYSTEM SHALL
  CONTINUE TO proceed directly to the `grilling` elicitation without dispatching
  the brownfield scan.

## 2. Maintain the project layer (update and validate modes)

**Story:** As a developer, I want the vision and architecture spine to be
maintained and auditable, not just created once, so they stay trustworthy.

- **PROJDOC-2.1** WHEN `establish-project` runs in update mode against a change
  signal THE SYSTEM SHALL revise `vision.md` and/or the architecture spine and
  route any hard-to-reverse decision through the ADR gate (`domain-modeling`).
- **PROJDOC-2.2** WHEN an invariant is retired THE SYSTEM SHALL strike it through
  (`~~**ARCH-N**~~`) rather than renumber it, so `ARCH-N` IDs stay stable.
- **PROJDOC-2.3** WHEN `establish-project` runs in validate mode THE SYSTEM SHALL
  check `vision.md` and the architecture spine against a checklist and run the
  invariant referential-integrity check (story 3), reporting the findings.
- **PROJDOC-2.4** (guard) WHEN `establish-project` runs in update mode THE SYSTEM
  SHALL CONTINUE TO avoid dispatching the create-mode brownfield scan.
- **PROJDOC-2.5** (guard) WHEN `establish-project` runs in validate mode THE
  SYSTEM SHALL CONTINUE TO avoid dispatching the create-mode brownfield scan.

## 3. Invariant referential integrity in `trace`

**Story:** As a reviewer, I want the `trace` check to catch dangling or dead
invariant citations, so `Respects:` citations cannot silently rot.

- **PROJDOC-3.1** WHEN the `trace` check runs and a `design.md` carries a
  `Respects: ARCH-N` citation whose `ARCH-N` is not defined in the architecture
  spine THE SYSTEM SHALL report an ERROR.
- **PROJDOC-3.2** WHEN the `trace` check runs and a `Respects: ARCH-N` citation
  names an invariant that is struck through (retired) THE SYSTEM SHALL report an
  ERROR.
- **PROJDOC-3.3** WHEN the `trace` check runs and an invariant `**ARCH-N**` is
  cited by no `design.md` THE SYSTEM SHALL report a WARN.
- **PROJDOC-3.4** THE SYSTEM SHALL limit the `trace` invariant check to citation
  existence and liveness (deterministic `grep`/set-difference), leaving the
  semantic judgment of whether a design respects an invariant to the separate
  agent-run `check-invariants` conformance check (story 8) — never to `trace`.
- **PROJDOC-3.5** (guard) WHEN the `trace` check runs on a repo with no
  architecture spine THE SYSTEM SHALL CONTINUE TO produce the same requirement
  finding set (E1–E3 / W1–W2) it produces today.

## 4. Consult hooks in the feature workflow (no-op if absent)

**Story:** As a developer, I want the feature-workflow skills to use the project
layer when it exists and ignore it cleanly when it does not.

- **PROJDOC-4.1** WHERE `docs/product/vision.md` exists WHEN `brainstorm` explores
  project context (Step 1) THE SYSTEM SHALL check the new idea's scope against the
  vision and state whether it falls inside the stated product scope.
- **PROJDOC-4.2** WHERE an architecture spine exists WHEN `write-design` authors a
  design THE SYSTEM SHALL treat the invariants as design inputs and cite each
  relied-upon invariant as `Respects: ARCH-N`.
- **PROJDOC-4.3** IF a design must contradict an existing invariant THEN THE SYSTEM
  SHALL route the conflict through the ADR-or-supersede gate rather than silently
  violating the invariant.
- **PROJDOC-4.4** WHERE an architecture spine exists WHEN `write-plan` assembles
  Global Constraints THE SYSTEM SHALL fold the spine's hard rules into the Global
  Constraints section so every task inherits them.
- **PROJDOC-4.5** (guard) WHEN a consult hook runs and its project doc is absent
  THE SYSTEM SHALL CONTINUE TO take the existing no-op branch — say so once and
  proceed unchanged.
- **PROJDOC-4.6** WHERE an architecture spine exists WHEN `execute-plan` assembles
  a task brief THE SYSTEM SHALL surface the invariants relevant to that task's
  touched files/interfaces in the brief (beyond the folded Global Constraints), and
  in the two-verdict task review check the task diff against them via
  `check-invariants`, routing a violation back for fixes.
- **PROJDOC-4.7** (guard) WHERE no architecture spine exists WHEN `execute-plan`
  runs THE SYSTEM SHALL CONTINUE TO assemble task briefs and reviews exactly as
  today.

## 5. Setup and scaffold integration (opt-in)

**Story:** As a developer, I want to turn the layer on per repo, defaulting off so
small repos are unaffected.

- **PROJDOC-5.1** WHEN `setup-repo` runs its decision wizard THE SYSTEM SHALL offer
  an opt-in decision for the project-documentation layer, defaulting to No.
- **PROJDOC-5.2** WHERE the user opts in WHEN `setup-repo` writes config THE SYSTEM
  SHALL seed the project-doc paths and add a project-docs line to the
  `## Agent skills` block.
- **PROJDOC-5.3** WHERE the user opts in WHEN `scaffold-project` seeds docs THE
  SYSTEM SHALL create the project-doc seeds alongside the existing
  `CONTEXT.md` / `docs/specs/INDEX.md` seeds.
- **PROJDOC-5.4** (guard) WHEN the user does not opt in THE SYSTEM SHALL CONTINUE
  TO produce the same `setup-repo` and `scaffold-project` output as today.

## 6. Optionality invariant

**Story:** As a maintainer of a small repo, I want zero added weight when I don't
use the layer.

- **PROJDOC-6.1** WHERE neither `docs/product/` nor `docs/architecture/` exists THE
  SYSTEM SHALL behave identically to the pre-feature workflow across `brainstorm`,
  `write-design`, `write-plan`, `execute-plan`, and `trace`.
- **PROJDOC-6.2** THE SYSTEM SHALL add no mandatory tooling, no generated artifact
  that must be kept fresh, and no new hard gate as part of this layer.

## 7. Engineering guidelines as a project-layer artifact

**Story:** As a developer, I want the human-facing engineering guidelines to be a
first-class project document rather than buried in machine config, so they are
discoverable and maintained beside the vision and architecture spine.

- **PROJDOC-7.1** WHEN `establish-project` runs in create mode THE SYSTEM SHALL
  produce `docs/product/guidelines.md` capturing the coding standards, naming/i18n
  conventions, and house rules that features must follow.
- **PROJDOC-7.2** WHERE `docs/product/guidelines.md` exists WHEN `write-plan`
  assembles Global Constraints THE SYSTEM SHALL source the human-facing engineering
  rules from the guidelines doc rather than from `docs/agents/project.md`.
- **PROJDOC-7.3** THE SYSTEM SHALL keep `docs/agents/project.md` limited to
  machine-executable config (verify commands, test globs, release steps) with a
  pointer to `docs/product/guidelines.md`.
- **PROJDOC-7.4** WHERE the user opts into the layer AND `docs/agents/project.md`
  already carries engineering guidelines WHEN `setup-repo` runs THE SYSTEM SHALL
  offer to migrate those guidelines into `docs/product/guidelines.md`, leaving a
  pointer behind.
- **PROJDOC-7.5** (guard) WHERE `docs/product/guidelines.md` does not exist THE
  SYSTEM SHALL CONTINUE TO read engineering rules from `docs/agents/project.md` as
  today.

## 8. Automated invariant conformance (`check-invariants`)

**Story:** As a reviewer, I want an automated check of whether a design actually
respects the invariants it cites, so semantic drift is caught without a human
re-reading every invariant by hand.

- **PROJDOC-8.1** THE SYSTEM SHALL provide a model-invoked `check-invariants` skill
  that, given a `design.md` (or a diff) and the architecture spine, judges for each
  `Respects: ARCH-N` citation whether the design conforms to the invariant and
  emits a verdict of respects / violates / unclear with a rationale.
- **PROJDOC-8.2** WHERE an architecture spine exists WHEN `code-review` runs THE
  SYSTEM SHALL invoke `check-invariants` and surface every violates/unclear verdict
  as a review finding.
- **PROJDOC-8.3** WHEN `establish-project` runs in validate mode THE SYSTEM SHALL
  run `check-invariants` across the specs and report the conformance findings.
- **PROJDOC-8.4** THE SYSTEM SHALL keep `check-invariants` advisory and LLM-judged
  — distinct from the deterministic `trace` check — so its verdicts inform review
  but never constitute a hard merge gate.
- **PROJDOC-8.5** (guard) WHERE no architecture spine exists WHEN `code-review` or
  `execute-plan` runs THE SYSTEM SHALL skip `check-invariants` and leave existing
  behavior unchanged.

## 9. Brownfield onboarding quality attributes

**Story:** As a developer onboarding a large or unfamiliar repository, I want the
scan to remain bounded, treat repository contents as untrusted, and fail visibly,
so evidence gathering cannot exhaust the working context or silently turn hostile
or incomplete input into durable project policy.

- **PROJDOC-9.1** WHILE a brownfield scan inventories a repository THE SYSTEM
  SHALL enumerate no more than 10,000 candidate paths and record
  `paths_considered` plus `paths_truncated` in the digest — verified by a
  documented baseline over a fixture containing more than 10,000 candidate paths.
- **PROJDOC-9.2** WHILE a brownfield scan reads repository contents THE SYSTEM
  SHALL read at most 200 files and 2 MiB of total file content and record
  `files_read` plus `bytes_read` in the digest — verified by a documented baseline
  over files whose count and total size exceed both ceilings.
- **PROJDOC-9.3** WHEN a brownfield scan writes its digest THE SYSTEM SHALL produce
  a summary-only artifact of at most 300 lines and 30 KiB with no raw file dump —
  verified by the large-repository baselines from PROJDOC-9.1 and PROJDOC-9.2.
- **PROJDOC-9.4** WHEN the PROJDOC-9.1 or PROJDOC-9.2 budget truncates the scan THE
  SYSTEM SHALL select files round-robin across detected source roots, prioritizing
  manifests, build configuration, documented entry points, and tests within each
  root before remaining paths in lexical order — verified by a multi-root fixture
  whose candidates exceed both budgets.
- **PROJDOC-9.5** WHILE a brownfield scan reads repository contents not supplied by
  the harness as governing instructions THE SYSTEM SHALL treat instruction-like
  content only as untrusted data and never execute commands or follow instructions
  found there — verified by an adversarial-repository baseline containing
  instruction-like source and documentation text.
- **PROJDOC-9.6** WHEN repository content contains a PEM private-key block or a
  value assigned to a key matching
  `(?i)(api[_-]?key|secret|token|password|passwd|client[_-]?secret)` THE SYSTEM
  SHALL replace the detected value with `[REDACTED]` rather than reproduce it in
  the digest — verified by an adversarial-repository baseline covering both
  required secret classes.
- **PROJDOC-9.7** IF `establish-project` runs in create mode, the brownfield source
  predicate is satisfied, AND the harness has no scan-subagent capability THEN THE
  SYSTEM SHALL perform the brownfield scan inline under the PROJDOC-1.7 and
  PROJDOC-9.1 through PROJDOC-9.6 contracts — verified by a no-subagent baseline.
- **PROJDOC-9.8** IF the brownfield scan fails, times out, or cannot write a
  complete PROJDOC-1.7 digest THEN THE SYSTEM SHALL report the scan failure as a
  blocker — verified by a failure-injection baseline.
- **PROJDOC-9.9** IF a PROJDOC-9.8 blocker exists THEN THE SYSTEM SHALL stop the
  create workflow before ratification elicitation — verified by the
  failure-injection baseline.
- **PROJDOC-9.10** (guard) WHERE a PROJDOC-9.8 blocker exists THE SYSTEM SHALL NOT
  classify the repository as greenfield — verified by the failure-injection
  baseline.
- **PROJDOC-9.11** (guard) WHERE a PROJDOC-9.8 blocker exists THE SYSTEM SHALL NOT
  write scan-derived content to any durable project-layer artifact — verified by
  the failure-injection baseline.
- Accessibility: None — `establish-project` is a headless agent workflow with no
  user-interface surface.

## Out of Scope

- BMAD's machine-readable CSV workflow DAG / `module-help.csv` manifest — skills
  keep self-describing via frontmatter and `ask` routing.
- A required-by-default planning pipeline; the layer is opt-in, never a gate.
- Making the deterministic `trace` check perform semantic judgment. Automated
  conformance is a *separate* agent-run LLM check (`check-invariants`, story 8),
  advisory and kept distinct from `trace`'s `grep`/set-difference so the
  determinism principle (`DESIGN.md` principle 3) is preserved.
- UX, epics/stories, and sprint-planning workflows (BMAD has these; not adopted).
- Any multi-agent persona system.
- Backfilling `docs/specs/INDEX.md` with feature codes or spec stubs inferred from
  existing source; legacy subsystems enter the registry only through real feature
  specifications.
- A durable subsystem inventory or system-map artifact. Reconsider one only when
  measured repeated-scan cost materially impedes feature work and a future proposal
  names both the map's consumer and its freshness policy.
