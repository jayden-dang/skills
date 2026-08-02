# Requirements: Docs-only spine

Feature code: DOSP
Status: Implemented
Date: 2026-08-02
Approved: 2026-08-02 (user)
Implemented: 2026-08-02 (build-inline on main)

Removes the requirement that feature / requirement IDs appear in application
source, tests, or commit trailers. Vertical integrity stays in `docs/specs/**`
(and optional architecture docs). Horizontal ownership stays path-based via
`load-subgraph` / `**Files:**`. Execute-family Spec reviews remain the judgment
that work matches requirements. Adds comment discipline so agents stop leaving
narrating / process trash comments in production-facing code.

**Locks from frame-change (2026-08-02):** reshape `audit-trace` (docs-only, drop
E2 + test greps); remove `Implements:` / `Guards:` trailers entirely; comment
rules ship in the same release via implementer + polish-diff (+ guidelines);
full pack rewrite (skills, AGENTS, guide, ARCH, templates, configure-repo).

**Consumer context that shaped the frame:** multi-skill teams (e.g. mailgate)
where only one participant uses this pack; `/// REQ:` and similar annotations
are unreadable process noise; shared docs must not depend on skill-set
glossary pollution.

## 1. Docs-only audit-trace

**Story:** As an agent running prove-claim or cut-release, I want a vertical
trace check that only reads `docs/specs/` (and optional architecture), so that
consumer codebases never need requirement IDs for the gate to pass.

- **DOSP-1.1** WHEN `audit-trace` runs THE SYSTEM SHALL gather requirement
  definitions only from bold `**CODE-N.M**` in `requirements.md` / `fixes.md`
  under the configured specs directory, and task citations only from
  `_Requirements:` lines in `tasks.md` — verified by the skill body and unit
  fixtures containing no test-file search roots for requirement coverage.
- **DOSP-1.2** WHEN `audit-trace` runs THE SYSTEM SHALL NOT search application
  source, test files, or any path outside the specs (and optional architecture /
  decision-record) trees for requirement-ID coverage — verified by absence of
  a test-coverage pass and by fixtures where IDs exist only in code and produce
  zero findings.
- **DOSP-1.3** THE SYSTEM SHALL retire finding code **E2** (Implemented/Shipped
  requirement lacks a covering test string) and SHALL NOT introduce a
  replacement finding that greps the codebase for requirement IDs — verified by
  skill finding table and unit fixtures that assert E2 is undefined / never
  emitted.
- **DOSP-1.4** THE SYSTEM SHALL CONTINUE TO emit **E1** only for task citations
  (and architecture / decision-record citations under their existing rules) that
  name undefined or retired IDs — not for strings found in code or tests —
  verified by a fixture where a test file cites a fake ID and E1 does not fire
  for that path, while a `_Requirements:` line with the same fake ID does.
- **DOSP-1.5** THE SYSTEM SHALL CONTINUE TO emit **E3**, **W1**, **W2**, and
  when `docs/architecture/` exists **E4**, **E5**, **W3**, with the same
  semantics as before this feature except where DOSP-1.3–1.4 change E1/E2 —
  verified by existing red/green fixtures updated only as needed for the
  retired E2 path.
- **DOSP-1.6** THE SYSTEM SHALL keep the skill name `audit-trace` (no rename
  required) and update its `description` frontmatter so agents invoke it for
  docs/spec integrity, not "covering tests" — verified by frontmatter text.

## 2. No requirement IDs in code or commits

**Story:** As a developer on a multi-skill team, I want production source,
tests, and commit messages free of skill-set requirement IDs, so that
reviewers who never adopted this pack see domain code only.

- **DOSP-2.1** THE SYSTEM SHALL NOT require, recommend, or gate on requirement
  IDs (`CODE-N.M`) or feature codes appearing in application source files, test
  source, doc comments on production code, or test titles/tags — verified by
  grepping skill bodies, templates, and guide for removed mandates (configure-repo
  test-annotation section, implementer prompts, plan-tasks "test annotation"
  coverage, AGENTS.md citation table rows for tests).
- **DOSP-2.2** THE SYSTEM SHALL forbid agents from choosing production
  identifiers (tables, modules, packages, API paths, exported type names) by
  copying a feature code or requirement ID — domain naming follows the
  consumer's architecture docs and existing patterns — verified by an explicit
  rule in AGENTS.md / guidelines / implementer prompts and a guide sentence.
- **DOSP-2.3** THE SYSTEM SHALL remove the `Implements:` and `Guards:` commit
  trailer requirement from plan-tasks, execute-family implementer prompts,
  package-change, and cut-release — commits use conventional / domain subjects
  only — verified by absence of mandatory trailer steps in those skills.
- **DOSP-2.4** WHEN cut-release builds a changelog THE SYSTEM SHALL derive
  shipped-behavior entries from `docs/specs/**` (requirement text for features
  moving to or already at Implemented/Shipped in the release range, and/or
  task footers + subjects) WITHOUT requiring `Implements:` / `Guards:` trailers
  on commits — verified by skill procedure text and a unit or scenario fixture.
- **DOSP-2.5** WHERE this skill-set repository's own tests or scenario markdown
  embed `CODE-N.M` strings as **fixtures testing pack behavior** THE SYSTEM
  SHALL CONTINUE TO allow those embeddings — they are product tests of the
  skill set, not a consumer annotation convention — verified by an explicit
  exception in guide/AGENTS and unchanged ability to unit-test ID parsers.

## 3. Spec-side coverage and Implemented evidence

**Story:** As an agent finishing a feature, I want a clear non-code definition
of "requirements met" and `Status: Implemented`, so that dropping E2 does not
create a freeroll status flip.

- **DOSP-3.1** WHEN `plan-tasks` runs its coverage check THE SYSTEM SHALL require
  every live Approved requirement ID to appear in at least one task
  `_Requirements:` footer and SHALL NOT require the ID string inside planned
  test source snippets — verified by plan-tasks skill body.
- **DOSP-3.2** WHEN realign-spec or any skill transitions a feature to
  `Status: Implemented` THE SYSTEM SHALL require: (a) every task checkbox in
  that feature's `tasks.md` checked; (b) the docs-only `audit-trace` finding set
  has zero errors; (c) verify commands from `docs/agents/project.md` have been
  run green under prove-claim — and SHALL NOT require any requirement ID to
  appear in test files — verified by realign-spec / prove-claim skill text.
- **DOSP-3.3** THE SYSTEM SHALL treat execute-family dual-verdict **Spec**
  review (per-task and whole-branch inspect-change Spec axis) as the judgment
  that implementation matches requirement prose — not a greppable ID in code —
  verified by implementer and reviewer prompt updates that remove "test must
  carry requirement ID" and keep "walk requirement IDs against the diff".
- **DOSP-3.4** (guard) WHEN prove-claim evaluates "requirements met" THE SYSTEM
  SHALL CONTINUE TO require the `audit-trace` check (docs-only form) clean AND
  acceptance criteria checked against observed behavior — green tests alone
  still do not prove requirements met — verified by prove-claim claim table.

## 4. Comment discipline

**Story:** As a reviewer reading production code written by an agent, I want
comments only where a future editor would mis-change behavior without them, so
that the tree is not filled with narrating or process trash.

- **DOSP-4.1** WHEN an implementer (build-in-waves, build-by-story, or
  build-inline) writes or edits production source THE SYSTEM SHALL instruct
  that default is **zero new comments**, and a comment is allowed only when it
  records a non-obvious invariant, hazard, protocol constraint, or "why"
  that the code alone does not show — verified by implementer prompt text.
- **DOSP-4.2** THE SYSTEM SHALL forbid comments that: restate the next line of
  code; narrate control flow; cite requirement IDs or feature codes; say
  "as per the plan/spec"; or leave placeholder TODOs that only restate the
  task — verified by implementer + polish-diff rationalization tables.
- **DOSP-4.3** WHEN `polish-diff` runs on a diff THE SYSTEM SHALL delete or
  flag for deletion comments that match DOSP-4.2, and SHALL preserve hazard /
  invariant comments that meet DOSP-4.1 — verified by polish-diff skill steps.
- **DOSP-4.4** THE SYSTEM SHALL record the same comment rules in
  `docs/product/guidelines.md` (Coding standards or House rules) so plan-tasks
  Global Constraints pick them up for consumer work in this repo and the rule
  is visible outside skill bodies — verified by guidelines content.

## 5. Doctrine and pack surface rewrite

**Story:** As a pack maintainer, I want AGENTS, architecture invariants, guide
concepts, templates, and configure-repo aligned with docs-only IDs, so that a
fresh agent does not re-teach ID-in-code.

- **DOSP-5.1** WHEN this feature ships THE SYSTEM SHALL update `AGENTS.md`
  Requirements Traceability Spine so citation forms list requirements, design,
  tasks, and optional issue body — and do **not** list Playwright/Vitest/Rust
  test annotations or commit trailers as required carriers — verified by
  AGENTS.md content.
- **DOSP-5.2** WHEN this feature ships THE SYSTEM SHALL revise **ARCH-4** so
  immutability and greppable citation apply to definitions and **docs-side**
  citations (`Satisfies:`, `_Requirements:`, `Respects:`) — not to tests or
  commit trailers — verified by `docs/architecture/INDEX.md`.
- **DOSP-5.3** WHEN this feature ships THE SYSTEM SHALL revise
  `docs/architecture/artifacts.md`, `CONTEXT.md` glossary for Requirement ID,
  and guide pages `concepts/requirement-ids.md` and `concepts/traceability.md`
  to describe docs-only vertical trace and path-based horizontal ownership —
  verified by those files.
- **DOSP-5.4** WHEN this feature ships THE SYSTEM SHALL update
  `configure-repo` / `templates/agents/project.md` to remove or replace the
  mandatory "Test annotation conventions" block that exists only to feed
  code-side audit-trace — verified by those files (a note that legacy
  annotations are ignored is allowed).
- **DOSP-5.5** WHEN this feature ships THE SYSTEM SHALL update guide examples
  (tier-0/1/2), process pages, skill guide stubs, and `docs/guide/resources/scripts.md`
  so they do not teach Implements trailers or REQ test tags as current practice —
  verified by grep of `docs/guide` for retired patterns after the rewrite.
- **DOSP-5.6** (guard) WHEN doctrine is rewritten THE SYSTEM SHALL CONTINUE TO
  treat requirement IDs as immutable once Approved (strikethrough retire only)
  inside `docs/specs/**` — verified by ARCH-4 / realign-spec iron rules retained.

## 6. Horizontal graph and execute Spec unchanged in purpose

**Story:** As an agent discovering neighbors or reviewing a task, I want
load-subgraph and Spec-axis review to keep working without code-side IDs.

- **DOSP-6.1** (guard) WHEN `load-subgraph` or `/map-features` runs THE SYSTEM
  SHALL CONTINUE TO derive OWNS/OVERLAPS from `**Files:**` and INDEX without
  requiring requirement IDs in source — verified by FSUB skill bodies
  untouched except cross-links if needed.
- **DOSP-6.2** (guard) WHEN build-in-waves / build-by-story / build-inline Spec
  review runs THE SYSTEM SHALL CONTINUE TO walk brief `_Requirements:` IDs
  against the diff for missing / extra / misunderstood behavior — verified by
  Spec Compliance sections remaining in reviewer prompts.
- **DOSP-6.3** (guard) WHEN `audit-trace` decision-record passes run THE SYSTEM
  SHALL CONTINUE TO invoke the record validator when `.skills/decisions/`
  exists, unchanged by docs-only reshape — verified by audit-trace skill
  section retained.

## 7. Quality attributes

**Section-kind:** nfr

**Story:** As a pack consumer, I want the reshaped check cheap and deterministic,
so that prove-claim stays harness-portable.

- **Performance:** **DOSP-7.1** WHEN `audit-trace` runs on a fixture of ≥20
  requirements files THE SYSTEM SHALL complete without grepping application
  trees — verified by skill passes listing only specs/architecture/decisions
  roots.
- **Security:** None — pure documentation/skill artifacts; no new trust
  boundary.
- **Reliability:** **DOSP-7.2** WHEN `docs/specs/` is absent THE SYSTEM SHALL
  CONTINUE TO no-op cleanly (nothing to check) rather than erroring — verified
  by audit-trace existing no-specs behavior retained.
- **Accessibility:** None — no interactive product UI; pack is markdown skills.

## Out of Scope

- Automatic mass-deletion of existing `/// REQ:` / `[CODE-N.M]` annotations in
  consumer repos (e.g. mailgate) — consumers clean on their own schedule; this
  feature only stops *requiring* and *teaching* them.
- A new user-invoked skill dedicated solely to comment cleanup of whole repos.
- Renaming `audit-trace` or inventing a parallel skill ID namespace.
- Materialized feature graphs or restoring E2 under another name.
- Changing Iron Laws NO-CODE / TEST-FIRST / ROOT-CAUSE / EVIDENCE (tests still
  required for behavior; they just need not embed IDs).
- Forcing Conventional Commit toolchains or changelog formats beyond
  cut-release procedure text.
- Personal OS package skills.

## Open Questions

- (none — residual defaults locked in frame-change: keep name `audit-trace`;
  Implemented evidence = DOSP-3.2; changelog without trailers = DOSP-2.4;
  skill-set fixture exception = DOSP-2.5)
