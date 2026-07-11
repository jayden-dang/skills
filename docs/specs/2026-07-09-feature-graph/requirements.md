# Requirements: Horizontal feature-graph layer

Feature code: FGRAPH
Status: Implemented
Date: 2026-07-09

<!--
Origin: brainstorm on optimizing how the skill set links features. Today the feature
code (INDEX.md registry) drives only the VERTICAL trace spine — requirement → design →
task → test → commit, enforced by check-trace.mjs. Relationships BETWEEN features live
only as freeform prose in each requirements.md header: not machine-queryable, not
bidirectional, not loaded selectively. That is what lets an agent rebuild territory a
neighbor already owns (duplication) and forces it to read whole specs to learn context
(cost, no scaling).

This feature adds a HORIZONTAL layer on the same feature-code key: a surface manifest
(the files a feature owns/touches), a reverse index (file → features), and bounded
summary cards (owns / interfaces / Out-of-Scope) — all HARVESTED from the design.md and
tasks.md a feature already writes, so there is NO new authoring burden.

Spike (scratchpad/surface-spike.mjs, throwaway) validated the harvest on the bot repo's
three real specs: for a CHIPUI-shaped idea it surfaced 15 shared files with INLTASK vs 1
with SHELL — the known "CHIPUI extends INLTASK" relationship, computed with zero manual
declaration. The spike also exposed the real noise to handle: basename-vs-fullpath double
counting and non-path junk tokens (see FGRAPH-1.3/1.4/1.5).

Agreed shape (brainstorm decisions):
- Engine: ONE scripts/check-graph.mjs, sibling to check-trace.mjs, modes --harvest /
  --query / --verify; config reuses docs/agents/trace.json (specsDir).
- Artifact: docs/specs/GRAPH.md — generated, committed, diff-reviewable; INDEX.md stays
  hand-maintained.
- Consumers (v1): brainstorm (regenerate in-memory, dedup query at the step-1 gate),
  sync-spec (regenerate + commit), verify/CI (--verify freshness lint).
- v1 role classification is BEST-EFFORT (hotspot signal); the dedup use only needs
  presence of ≥2 features on a path, not authoritative ownership.

Deferred to a fast-follow (see Out of Scope): manually-declared typed edges
(extends/supersedes) and their auto-reversal; authoritative owns-vs-touches precision;
card-based context loading in write-design / execute-plan / code-review.

Vocabulary (new terms, to add to CONTEXT.md via domain-modeling): Surface, Surface
manifest, Reverse index, Shared surface, Summary card.
-->

## 1. Harvest a per-feature surface manifest

**Story:** As an agent, I want each feature's owned and touched files derived from the specs it already has, so feature relationships are computed from existing artifacts with no new authoring.

- **FGRAPH-1.1** WHEN `--harvest` runs over a specs directory, THE SYSTEM SHALL produce, for every feature whose `requirements.md` declares a feature code, a surface manifest listing the source-file paths referenced in that feature's `design.md` and `tasks.md`.
- **FGRAPH-1.2** THE SYSTEM SHALL derive surface entries only from existing `design.md` and `tasks.md` content, requiring no new fields or annotations in those files.
- **FGRAPH-1.3** WHEN a referenced token carries a line or position locator (e.g. `Editor.tsx:208`, `App.tsx:127,172`, or a trailing `(~208-221)`), THE SYSTEM SHALL normalize it to the bare file path before recording it.
- **FGRAPH-1.4** WHEN the same file is referenced within one feature both by bare basename and by a fuller path, THE SYSTEM SHALL record it as a single surface entry under the fullest path seen.
- **FGRAPH-1.5** IF a candidate token is not a source path — it has no recognized code file extension and does not sit under a recognized source root, or it lacks a real path segment (e.g. a bare `src-tauri/` or a bare `.spec.ts`) — THEN THE SYSTEM SHALL exclude it from the manifest.
- **FGRAPH-1.6** THE SYSTEM SHALL classify each surface entry's role as `owns` or `touches` on a best-effort basis: a create/new-file signal in the feature's `tasks.md` yields `owns`; a modify/reference signal yields `touches`.
- **FGRAPH-1.7** IF a candidate token contains a glob wildcard character (`*`), THEN THE SYSTEM SHALL exclude it from the manifest (e.g. `e2e/*.spec.ts`, `noteListHelpers.*.test.ts` are not concrete surface paths). _(amend — dogfooding)_
- **FGRAPH-1.8** IF a source path appears in a spec only within a command-invocation context — a line invoking a CLI, recognized by a leading `node`/`npm`/`pnpm`/`npx`/`yarn`/`git`/`bash`/`sh`/`deno`/`bun` command word or a `Run:`-style step — THEN THE SYSTEM SHALL exclude that path from the manifest, since running a tool is neither owning nor touching feature surface. _(amend — dogfooding: every feature's `tasks.md` runs `node scripts/check-trace.mjs`, forging a false shared-surface edge across all features.)_
- **FGRAPH-1.9** (guard) WHEN the FGRAPH-1.7/1.8 exclusions run, THE SYSTEM SHALL CONTINUE TO harvest concrete source paths declared in unfenced `Files:` / `- Create:` / `- Modify:` bullets and in prose backticks — real surface must not be over-filtered. _(amend — dogfooding)_

## 2. Reverse index and shared-surface detection

**Story:** As an agent deciding whether new work duplicates existing work, I want a file→features index that flags overlapping territory, so duplication is visible before I build.

- **FGRAPH-2.1** WHEN `--harvest` runs, THE SYSTEM SHALL produce a reverse index mapping each surface path to the list of features that reference it, each paired with its role.
- **FGRAPH-2.2** WHEN a surface path is referenced by two or more distinct features, THE SYSTEM SHALL mark that path as a shared surface.
- **FGRAPH-2.3** THE SYSTEM SHALL determine shared-surface status from the presence of ≥2 referencing features alone, independent of role-classification accuracy.
- **FGRAPH-2.4** WHEN building the reverse index, THE SYSTEM SHALL treat a bare basename and a fuller path to the same file as a single surface path ACROSS features (not only within one feature, as FGRAPH-1.4 does), so a file referenced as `mathInputExtension.ts` in one spec and `src/components/mathInputExtension.ts` in another is counted as one shared surface, not two. _(amend — dogfooding)_
- **FGRAPH-2.5** (guard) WHEN cross-feature dedup runs, THE SYSTEM SHALL CONTINUE TO detect the already-validated shared surface between features that extend one another (e.g. CHIPUI↔INLTASK sharing the inline-task files). _(amend — dogfooding)_

## 3. Summary cards

**Story:** As an agent, I want a bounded per-feature card, so I can load a neighbor feature's essence without pulling its whole spec into context.

- **FGRAPH-3.1** WHEN `--harvest` runs, THE SYSTEM SHALL produce, per feature, a summary card containing the feature code, the feature name, its owned surface paths, its public interfaces (best-effort), and its Out-of-Scope items.
- **FGRAPH-3.2** THE SYSTEM SHALL populate a card's Out-of-Scope items from the feature's `requirements.md` `## Out of Scope` section.
- **FGRAPH-3.3** THE SYSTEM SHALL populate a card's public interfaces on a best-effort basis from the `Interfaces:` blocks present in the feature's `design.md` and `tasks.md`.
- **FGRAPH-3.4** THE SYSTEM SHALL cap each enumerated list in a card (owned paths, interfaces, Out-of-Scope items) at a configurable maximum, default 12 entries, so a card stays materially smaller than the feature's `requirements.md`.
- **FGRAPH-3.5** THE SYSTEM SHALL populate a card's interfaces as short, single-line entries — the signature or first line of each top-level `Interfaces:` bullet — excluding nested sub-bullets, multi-line prose continuations, and bare section-lead labels (e.g. a lone `Produces:` / `Consumes:`), so the interfaces field stays a bounded card summary rather than a verbatim dump. This refines the best-effort extraction of FGRAPH-3.3. _(amend — dogfooding)_

## 4. The GRAPH.md artifact

**Story:** As a maintainer and reviewer, I want the harvested graph committed and diff-reviewable, so relationships are visible in code review and survive fresh sessions.

- **FGRAPH-4.1** WHEN `--harvest` runs, THE SYSTEM SHALL write the reverse index and all summary cards to `GRAPH.md` in the specs directory (a sibling of `INDEX.md`).
- **FGRAPH-4.2** THE SYSTEM SHALL write `GRAPH.md` deterministically, with stable ordering, so re-running `--harvest` without any spec change produces a byte-identical file.
- **FGRAPH-4.3** WHEN generating `GRAPH.md`, THE SYSTEM SHALL leave `INDEX.md` unmodified.
- **FGRAPH-4.4** (guard) WHEN the FGRAPH-1.7/1.8/2.4/3.5 harvest changes are applied, THE SYSTEM SHALL CONTINUE TO produce a deterministic, byte-stable `GRAPH.md` (total ordering preserved). _(amend — dogfooding)_

## 5. Query mode

**Story:** As a skill, I want to ask which features overlap a set of candidate files or keywords and get a machine-readable answer, so I can act on overlaps programmatically.

- **FGRAPH-5.1** WHEN `--query` runs with one or more candidate file paths, THE SYSTEM SHALL return the features that own or touch any of those paths, each accompanied by its summary card.
- **FGRAPH-5.2** WHEN `--query` runs with one or more keywords, THE SYSTEM SHALL return the features whose card feature-name or Out-of-Scope items match a keyword, each accompanied by its summary card.
- **FGRAPH-5.3** THE SYSTEM SHALL rank query results by the number of overlapping surface paths, most-overlapping first.
- **FGRAPH-5.4** WHEN `--query` computes results, THE SYSTEM SHALL harvest current spec state rather than reading a previously written `GRAPH.md`.
- **FGRAPH-5.5** THE SYSTEM SHALL emit query results as JSON on stdout.
- **FGRAPH-5.6** THE SYSTEM SHALL compute query results by reading only spec markdown files — no code compilation, no build, and no network access.

## 6. Verify mode and the verify/CI gate

**Story:** As CI and the verify gate, I want a stale or broken graph to fail, so the committed graph never silently rots (the same discipline check-trace enforces for the trace spine).

- **FGRAPH-6.1** WHEN `--verify` runs and the committed `GRAPH.md` differs from a freshly harvested graph, THE SYSTEM SHALL report the staleness and exit non-zero.
- **FGRAPH-6.2** WHEN `--verify` runs and `GRAPH.md` is byte-identical to a freshly harvested graph, THE SYSTEM SHALL exit zero.
- **FGRAPH-6.3** IF a harvested feature declares a feature code that is absent from `INDEX.md`, THEN `--verify` SHALL report the unregistered code and exit non-zero.
- **FGRAPH-6.4** WHEN the `verify` skill runs its check suite, THE SYSTEM SHALL run `check-graph --verify` alongside `check-trace`.

## 7. Brainstorm dedup at the gate

**Story:** As an agent starting brainstorm, I want existing overlapping features surfaced during context exploration, so I extend rather than rebuild.

- **FGRAPH-7.1** WHEN brainstorm explores project context (step 1), THE SYSTEM SHALL query the feature graph using both the candidate files named by the context scan and the idea's key terms.
- **FGRAPH-7.2** WHEN the query returns overlapping features, THE SYSTEM SHALL present them to the user as summary cards, not as full specs.
- **FGRAPH-7.3** WHEN brainstorm completes step 1, THE SYSTEM SHALL state which existing features share the idea's surface and how the new idea differs, citing feature codes.
- **FGRAPH-7.4** IF the query returns no overlapping features, THEN THE SYSTEM SHALL state that no existing feature shares the idea's surface and continue.
- **FGRAPH-7.5** IF the graph query fails or `check-graph` is unavailable, THEN THE SYSTEM SHALL note that the automated overlap check was unavailable and continue brainstorm's manual context exploration.

## 8. Sync-spec keeps GRAPH.md fresh

**Story:** As the anti-rot skill, I want GRAPH.md regenerated whenever a triad changes, so the committed graph tracks reality.

- **FGRAPH-8.1** WHEN sync-spec realigns a feature's triad, THE SYSTEM SHALL regenerate `GRAPH.md` via `--harvest`.
- **FGRAPH-8.2** WHEN sync-spec regenerates `GRAPH.md` and the file changed, THE SYSTEM SHALL include the updated `GRAPH.md` in the sync-spec commit.

## 9. Graceful degradation and guards

**Story:** As a maintainer of an existing repo, I want the new layer to add value without breaking existing skills or demanding new spec conventions.

- **FGRAPH-9.1** IF a feature has a `requirements.md` but no `design.md` or `tasks.md`, THEN THE SYSTEM SHALL produce a card for it from available data (code, name, Out-of-Scope) with an empty surface manifest, without error.
- **FGRAPH-9.2** IF the specs directory contains no feature specs, THEN THE SYSTEM SHALL produce a well-formed empty `GRAPH.md` and exit zero.
- **FGRAPH-9.3** IF `docs/agents/trace.json` is absent, THEN THE SYSTEM SHALL resolve the specs directory using the same default as check-trace (`docs/specs`).
- **FGRAPH-9.4** (guard) WHEN `check-graph` runs, THE SYSTEM SHALL CONTINUE TO leave `check-trace`'s behavior, outputs, and exit codes unchanged.
- **FGRAPH-9.5** (guard) WHEN the feature-graph layer is present, THE SYSTEM SHALL CONTINUE TO require no new fields or annotations in `requirements.md`, `design.md`, or `tasks.md` for any existing skill to function.
- **FGRAPH-9.6** (guard) WHEN brainstorm runs in a harness without subagents, THE SYSTEM SHALL CONTINUE TO complete step 1, degrading the graph query to a direct in-context invocation.

## 10. Code-review duplication check (advisory)

**Story:** As a reviewer, I want code-review to surface which existing features share the diff's surface, so I catch a change that rebuilds behavior a neighbor already owns — a second dedup net after brainstorm's step-1 check. _(amend — reclaims the deferred Out-of-Scope item; advisory: the graph gives surface overlap, the reviewer judges semantic duplication.)_

- **FGRAPH-10.1** WHEN code-review runs, THE SYSTEM SHALL query the feature graph (`check-graph --query`) with the diff's changed source files and obtain the overlapping features and their summary cards.
- **FGRAPH-10.2** WHEN the Spec axis runs and the query returns overlapping features, THE SYSTEM SHALL include those features' summary cards (owned paths + Out-of-Scope) in the Spec subagent's brief as context.
- **FGRAPH-10.3** THE Spec review brief SHALL direct the reviewer to flag, as a reuse-miss finding citing the neighbor's feature code, any place the diff reimplements behavior a shares-surface neighbor already owns.
- **FGRAPH-10.4** IF no changed file overlaps any feature, THEN THE SYSTEM SHALL state that no existing feature shares the diff's surface and inject no cards.
- **FGRAPH-10.5** IF the graph query fails or `check-graph` is unavailable, THEN code-review SHALL note the automated overlap check was unavailable and continue the two-axis review.
- **FGRAPH-10.6** (guard) WHEN this check is added, THE SYSTEM SHALL CONTINUE TO run the Standards + Spec two-axis review unchanged when the graph query yields nothing, is unavailable, or when no requirements spec exists (Spec axis skipped).

## 11. Distribution — the graph runs where it is consumed

**Story:** As the maintainer of a repo that installed this skill set, I want `setup-repo` to install and wire the graph linter, so the dedup gates actually run in my repo instead of failing open silently forever. _(amend — reclaims the deferred Out-of-Scope item; dogfooding found `check-graph.mjs` absent from every consuming repo, so FGRAPH-7.5 and FGRAPH-10.5 fire on every query and the feature is inert outside the repo that authored it.)_

- **FGRAPH-11.1** WHEN `setup-repo` writes a repo's configuration, THE SYSTEM SHALL vendor each linter script the skill set ships (`check-trace.mjs`, `check-graph.mjs`) into that repo's configured scripts location.
- **FGRAPH-11.2** WHEN `setup-repo` vendors a linter script, THE SYSTEM SHALL write into the vendored copy a version stamp identifying the skill-set revision it was copied from.
- **FGRAPH-11.3** IF a repo's vendored linter carries a version stamp differing from the skill set's current copy, THEN `setup-repo` SHALL report the drift and offer to update the vendored copy.
- **FGRAPH-11.4** WHEN `setup-repo` writes `docs/agents/project.md`, THE SYSTEM SHALL include a `Graph` row whose command runs `check-graph.mjs --verify`, beside the existing `Trace` row.
- **FGRAPH-11.5** WHERE the user accepts the git-verify-hooks opt-in, THE SYSTEM SHALL include `check-graph.mjs --verify` in the vendored `pre-push` hook alongside the trace lint.
- **FGRAPH-11.6** WHERE the user accepts the CI opt-in, THE SYSTEM SHALL append a `check-graph.mjs --verify` step to the repo's existing CI workflow.
- **FGRAPH-11.7** (guard) WHEN the CI opt-in appends the graph step, THE SYSTEM SHALL CONTINUE TO edit the existing workflow additively, authoring no new pipeline.
- **FGRAPH-11.8** WHEN `setup-repo` reaches its configuration-proving gate, THE SYSTEM SHALL run `check-graph.mjs --harvest` once to seed the repo's `GRAPH.md`.
- **FGRAPH-11.9** IF `check-graph.mjs` cannot execute at `setup-repo`'s proving gate, THEN THE SYSTEM SHALL classify it as a wiring failure and fix it before setup completes.
- **FGRAPH-11.10** IF a consumer skill's graph query finds `check-graph.mjs` absent, THEN THE SYSTEM SHALL state that the feature graph is not installed and name `setup-repo` as the remedy. _(amends the bare "overlap check unavailable" note of FGRAPH-7.5 and FGRAPH-10.5.)_
- **FGRAPH-11.11** WHILE a consumer skill has already reported the graph as not installed in the current session, THE SYSTEM SHALL omit the remedy from subsequent queries in that session.
- **FGRAPH-11.12** (guard) IF `check-graph.mjs` is absent or errors, THEN THE SYSTEM SHALL CONTINUE TO complete `brainstorm` step 1 and `code-review`'s two-axis review without blocking.
- **FGRAPH-11.13** (guard) WHEN the distribution wiring is added, THE SYSTEM SHALL CONTINUE TO require no new fields or annotations in `requirements.md`, `design.md`, or `tasks.md`.
- **FGRAPH-11.14** (guard) WHEN `setup-repo` vendors the graph linter, THE SYSTEM SHALL CONTINUE TO leave `check-trace`'s behavior, outputs, and exit codes unchanged.

## Out of Scope

- **Manually-declared typed edges** (`extends`, `depends-on`, `supersedes`) and their automatic reversal — the fast-follow. v1 derives only the untyped `shares-surface` relationship, which is free from the harvest.
- **Authoritative owns-vs-touches precision.** v1 role classification is best-effort; the dedup signal depends only on shared-surface presence (FGRAPH-2.3).
- **Card-based context loading in write-design / execute-plan** — **evaluated 2026-07-09 and DECLINED.** write-design already bounds context via its scan-subagent digest; execute-plan's task-briefs already carry exact per-task neighbor `file:line` references (write-plan bakes them in). A throwaway A/B prototype on a real cross-feature task (bot CONVMK Task 3, which modifies CHIPUI's files) confirmed a best-effort card is redundant-to-noise: two cold planners made identical reuse decisions with and without the card, and the card's interfaces field omitted the interfaces the task needed while including irrelevant ones. Neighbor-awareness is already delivered at the gates that matter — `brainstorm` step-1 and `code-review` step-3a (Story 10, which DOES consume cards). Not a fast-follow; closed.
- ~~**A code-review "reimplements a neighbor?" check.**~~ Reclaimed — now specified as Story 10 (advisory).
- **Harvesting surface from committed code or import graphs.** The source of truth is specs only; the spike proved specs carry enough signal.
- **Semantic or embedding-based matching.** Keyword matching only (FGRAPH-5.2).
- ~~**setup-repo / scaffold-project auto-wiring** check-graph into CI and seeding an initial `GRAPH.md` — manual for v1.~~ Reclaimed — now specified as Story 11 (distribution). `scaffold-project` is covered transitively: it hands `docs/agents/` to `setup-repo` and writes none of it itself.
- **Dogfooding the graph across the skills repo's own future features** beyond bootstrapping this one spec and its `docs/specs/INDEX.md`.
- **Graph scale rework** — the committed-manifest / on-demand-card split, IDF-weighted ranking with a hub-degree cutoff, query result caps, and byte-bounded card fields. Measured 2026-07-10 on the `bot` repo: 4 features render a 15.7 KB `GRAPH.md` with per-card Out-of-Scope prose at 35–53% of card bytes; a 52-feature simulation renders 140.6 KB (~36k tokens), one hub path returns 38 full cards (97.3 KB), and FGRAPH-5.3's raw-overlap ranking degenerates to alphabetical order when every candidate overlaps on the same hub file. Fixing this **supersedes approved criteria** (FGRAPH-2.2/2.3, 3.4, 4.1, 5.3) and has live design alternatives, so it escalated to `brainstorm` rather than being decided inside this amendment.
- **Authoring a CI pipeline where none exists.** FGRAPH-11.6 appends to an existing workflow only; full CI/CD authoring is excluded from the skill set's v1 (`DESIGN.md`).
- **Silently auto-updating a drifted vendored linter.** FGRAPH-11.3 reports drift and offers; it never rewrites a repo's script without consent.
- **A package-manager distribution channel** (e.g. an npm `bin`) for the linters. Vendoring into the consuming repo keeps them dependency-free and offline, as `check-trace` already is.
