# Requirements: Module Manifest & Boundary Linting

Feature code: MODMAP
Status: Approved
Date: 2026-07-11

Foundation slice (M1) of the enterprise context layer. Defines the **module
manifest** — the authored, linter-checked map of source folders to modules that
is the boundary source of truth — its loader, and a boundary-verification
extension to `check_graph`. Downstream slices (sharded graph, feature homing,
brownfield on-ramp, per-module standards, gate integration) all consume this
manifest; none are in scope here. Design context:
`scratchpad/ENTERPRISE-CONTEXT-DESIGN.md`.

Vocabulary (to be formalized in CONTEXT.md at design time): a **module** is a
first-class ownership grouping between the project and a feature; the **module
manifest** is the small authored map of folder-glob → module; a folder is
**owned** by a module when one of that module's glob patterns matches it.

## 1. Declare and load the module manifest

**Story:** As an engineer adopting the skillset on a large repo, I want to
declare my modules and which folders each owns in one small manifest, so that the
tooling has a single honest source of truth for architectural boundaries.

- **MODMAP-1.1** WHERE a `modules` key is present in `docs/agents/trace.json` THE
  SYSTEM SHALL load each entry as a module carrying a `code`, a `name`, and an
  `owns` list of folder-glob patterns.
- **MODMAP-1.2** THE SYSTEM SHALL accept optional `layer` and `owner` string
  fields on a module entry and preserve them for downstream consumers without
  otherwise acting on them.
- **MODMAP-1.3** IF a module entry omits its `code`, its `name`, or a non-empty
  `owns` list THEN THE SYSTEM SHALL report a manifest-validity error naming the
  offending entry and SHALL NOT run boundary verification.
- **MODMAP-1.4** IF two module entries share the same `code` THEN THE SYSTEM
  SHALL report a duplicate-code error naming that code.
- **MODMAP-1.5** IF a module `code` does not match the feature-code format (2–12
  chars, A–Z0–9, starting with a letter) THEN THE SYSTEM SHALL report a
  malformed-code error naming the entry.

## 2. Resolve a source path to its owning module

**Story:** As a downstream consumer (the sharded graph, feature homing), I want
to ask which module owns a given source path, so that ownership is computed one
way in one place rather than reinvented per consumer.

- **MODMAP-2.1** WHEN asked for the module owning a given repo-relative source
  path THE SYSTEM SHALL return the single module whose `owns` patterns match that
  path.
- **MODMAP-2.2** WHEN more than one module's `owns` patterns match the same path
  THE SYSTEM SHALL report a double-mapped-path error naming the path and every
  competing module code, and SHALL treat the path as unresolved rather than
  silently choosing one.
- **MODMAP-2.3** WHEN no module's `owns` patterns match a given path THE SYSTEM
  SHALL return "no owning module" for that path (an orphan), distinct from an
  error at resolution time.

## 3. Verify boundary coverage

**Story:** As a maintainer, I want a check that proves every part of the source
tree belongs to exactly one module, so that the manifest cannot silently drift
from the real folder layout the way a prose architecture doc would.

- **MODMAP-3.1** WHEN boundary verification runs with a manifest present THE
  SYSTEM SHALL enumerate every source folder under the effective graph
  `sourceRoots` configuration (the built-in defaults merged with any override in
  `trace.json`) and resolve each to its owning module.
- **MODMAP-3.2** IF a source folder resolves to no module THEN THE SYSTEM SHALL
  report an orphan-folder error naming the folder.
- **MODMAP-3.3** IF a source folder resolves to more than one module THEN THE
  SYSTEM SHALL report a double-mapped-folder error naming the folder and the
  competing module codes.
- **MODMAP-3.4** IF a module's `owns` pattern matches no folder in the repo THEN
  THE SYSTEM SHALL report a stale-glob warning naming the module and the pattern.
- **MODMAP-3.5** WHEN every source folder resolves to exactly one module and no
  manifest-validity, duplicate-code, malformed-code, orphan-folder, or
  double-mapped-folder finding exists THE SYSTEM SHALL report boundary
  verification as passing.
- **MODMAP-3.6** IF boundary verification produces any error-level finding THEN
  THE SYSTEM SHALL exit with a non-zero status.
- **MODMAP-3.7** WHEN boundary verification produces only warnings and no
  error-level finding THE SYSTEM SHALL exit with a zero status.

## 4. Degrade gracefully and preserve existing behavior

**Story:** As an owner of a repo that has not adopted modules, I want the
existing feature graph to behave exactly as before, so that this feature is
purely additive and never nags a repo that declined it.

- **MODMAP-4.1** WHERE no `modules` key is present in `docs/agents/trace.json`
  THE SYSTEM SHALL treat the module layer as disabled and SHALL NOT emit
  orphan-folder, double-mapped-folder, or stale-glob findings.
- **MODMAP-4.2** (guard) WHEN no manifest is present THE SYSTEM SHALL CONTINUE TO
  produce the existing `check_graph` harvest and query output unchanged.
- **MODMAP-4.3** (guard) WHEN a manifest is present THE SYSTEM SHALL CONTINUE TO
  perform the existing `--verify` checks — the committed `GRAPH.md` matching a
  fresh render, and every harvested feature code being registered in `INDEX.md` —
  in addition to boundary verification.
- **MODMAP-4.4** (guard) WHEN a `modules` key is added to `docs/agents/trace.json`
  THE SYSTEM SHALL CONTINUE TO resolve the existing `specsDir` value from that
  file and the `graph` configuration (built-in defaults merged with any override
  in the file), ignoring the new key for those purposes.
- **MODMAP-4.5** (guard) THE SYSTEM SHALL CONTINUE TO run with no top-level side
  effects on import — loading the manifest happens only when a mode is invoked,
  never at import time.

## Out of Scope

- **Seeding/drafting the manifest** from CODEOWNERS, workspace config, or
  top-level directories — that is the brownfield on-ramp (M4).
- **Sharding the graph or per-module rendering** — the module-scoped
  MODULES.md, per-module row indexes, and on-query cards are M2.
- **Feature-to-module homing and cross-cutting facets** — M3.
- **Per-module standards** and their consumption by review/briefs — M5.
- **Gate integration** — brainstorm dedup, code-review reuse-miss/boundary,
  sync-spec regeneration, and setup-repo installation reading the manifest — M6.
- **Enforcing layering rules** between modules (e.g., "UI must not import
  infra") — M1 preserves `layer` but attaches no semantics to it.
- **Any authoring UI or migration tool** — in M1 the manifest is hand-edited.
