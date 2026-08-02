# Requirements: System-docs core + Codebase Map

Feature code: SDOC
Status: Approved
Date: 2026-08-02
Roadmap item: ROAD-7

<!--
ROAD-7 first shippable slice of MILE-3. Self-contained acceptance criteria.
IDs are immutable from this Approved status; retire only by strikethrough.
-->

## Normative Hybrid 1A inventory

THE SYSTEM SHALL use exactly the following entry keys in `CATALOG.md` for the Hybrid 1A model. No other key is a Hybrid 1A inventory member for pack tests that assert inventory completeness. Canonical consumer paths are defaults in consuming repositories; they are not pack implementation Surfaces.

| Entry key | Canonical consumer path (default) |
|---|---|
| `product/vision` | `docs/product/vision.md` |
| `product/personas` | `docs/product/personas.md` |
| `product/metrics` | `docs/product/metrics.md` |
| `product/principles` | `docs/product/principles.md` |
| `product/guidelines` | `docs/product/guidelines.md` |
| `architecture/INDEX` | `docs/architecture/INDEX.md` |
| `architecture/system` | `docs/architecture/system.md` |
| `architecture/data` | `docs/architecture/data.md` |
| `architecture/integrations` | `docs/architecture/integrations.md` |
| `architecture/runtime` | `docs/architecture/runtime.md` |
| `codebase/map` | `docs/codebase/map.md` |
| `codebase/modules` | `docs/codebase/modules.md` |
| `codebase/ownership` | `docs/codebase/ownership.md` |
| `codebase/dependencies` | `docs/codebase/dependencies.md` |
| `security/threat-model` | `docs/security/threat-model.md` |
| `security/posture` | `docs/security/posture.md` |
| `security/compliance` | `docs/security/compliance.md` |
| `standards/INDEX` | `docs/standards/INDEX.md` |
| `standards/testing` | `docs/standards/testing.md` |
| `standards/api` | `docs/standards/api.md` |
| `standards/ui` | `docs/standards/ui.md` |
| `standards/accessibility` | `docs/standards/accessibility.md` |
| `standards/security-coding` | `docs/standards/security-coding.md` |
| `standards/errors-logging` | `docs/standards/errors-logging.md` |
| `standards/observability` | `docs/standards/observability.md` |
| `ops/deployment` | `docs/ops/deployment.md` |
| `ops/reliability` | `docs/ops/reliability.md` |
| `ops/observability` | `docs/ops/observability.md` |
| `ops/disaster-recovery` | `docs/ops/disaster-recovery.md` |
| `ops/runbooks` | `docs/ops/runbooks/` |
| `roadmap/INDEX` | `docs/roadmap/INDEX.md` |
| `specs/INDEX` | `docs/specs/INDEX.md` |
| `adr` | `docs/adr/` |
| `agents/config` | `docs/agents/` |
| `glossary` | `CONTEXT.md` |
| `out-of-scope` | `.out-of-scope/` |

**Count:** 36 entry keys. Pack tests that assert inventory completeness SHALL compare `CATALOG.md` entry keys to this set (exact set equality).

## 1. Pack-local system-docs catalog

**Story:** As a skill-set author, I want a pack-local catalog of the Hybrid 1A inventory with maturity and entry packages, so that agents resolve one artifact's contract without loading the full documentation tree or a consumer-side registry.

- **SDOC-1.1** THE SYSTEM SHALL ship a pack-local catalog at `skills/project/define-system-doc/catalog/CATALOG.md` whose table columns are only: Entry key, Maturity, Entry-package pointer.
- **SDOC-1.2** THE SYSTEM SHALL list in `CATALOG.md` exactly the 36 Hybrid 1A entry keys from the Normative Hybrid 1A inventory table above, and no additional Hybrid 1A members.
- **SDOC-1.3** THE SYSTEM SHALL store each entry package at a filesystem path that mirrors the slash-delimited entry key under `skills/project/define-system-doc/catalog/entries/` (example: entry key `codebase/map` maps to `catalog/entries/codebase/map.md`).
- **SDOC-1.4** WHEN an entry package is present THE SYSTEM SHALL include in that package (and not in `CATALOG.md`) the fields: purpose and boundary; canonical consumer path; applicability (when it should exist); mediated writer; template/schema pointer; validator pointer; evidence sources; real readers and decision points; no-op behavior when absent or non-authoritative. THE SYSTEM SHALL NOT duplicate Maturity inside the entry package; maturity is authoritative only in the matching `CATALOG.md` row.
- **SDOC-1.5** THE SYSTEM SHALL assign each Hybrid 1A row a Maturity value of exactly one of: `First-class`, `Recognized`, `Deferred`.
- **SDOC-1.6** THE SYSTEM SHALL define pack-support maturity as follows:
  - **First-class** — stable canonical consumer path; template/schema and required slots; mediated writer (`/define-system-doc` or an existing owner skill); validator; legal authoring target; at least one real consult hook at a named decision point; conditional suggestion protocol where the entry package defines suggestion applicability; tests; synchronized guide coverage.
  - **Recognized** — official model includes purpose, boundary, applicability rule, and canonical path; the pack provides no template, no `/define-system-doc` target, no validator, no suggestion, no consult hook, and no claimed reader for that entry.
  - **Deferred** — possibility recorded only so it is not lost; no path contract, writer, template, validator, hook, or suggestion; non-applicable catalog fields explicitly `None — deferred`.
- **SDOC-1.7** WHEN a `CATALOG.md` row is marked `First-class` THE SYSTEM SHALL provide machine-checkable evidence that the complete First-class support package exists for that entry: entry package file; template path that exists when the writer is template-mediated; validator path that exists; mediated writer skill path that exists; at least one named reader skill with consult behavior described in the entry package; and pack tests for **every named First-class reader** of that entry that exercise all of the following (a string mention of the entry key alone is insufficient): (a) the reader's applicability predicate; (b) consult behavior when the artifact is authoritative under that entry's authority predicate; (c) no-op behavior when the artifact is absent or non-authoritative; (d) suggestion behavior when that reader declares a suggestion protocol for the entry (if the reader declares no suggestion protocol, (d) is not required for that reader). A pack test SHALL fail if any First-class row lacks any of these artifacts or if any named First-class reader lacks the required reader tests.
- **SDOC-1.8** WHILE this feature's delivery scope is ROAD-7 THE SYSTEM SHALL allow `codebase/map` to be marked `First-class` only when SDOC-1.7 holds for `codebase/map` including `plan-tasks` as a named reader with a real consult hook and the reader tests in SDOC-1.7; THE SYSTEM SHALL mark every other Hybrid 1A row at its actual pack-support maturity (not `First-class` without SDOC-1.7 evidence).
- **SDOC-1.9** THE SYSTEM SHALL NOT persist consumer-repository adoption state in the pack catalog. Consumer adoption is derived at runtime only as one of: `Absent`, `Non-authoritative`, or `Approved`. THE SYSTEM SHALL NOT use a single universal Status-header rule for all inventory entries. Each entry package and its validator SHALL define that entry's **authority predicate** (how a consumer path or directory is judged Absent, Non-authoritative, or Approved). For entry key `codebase/map` specifically, the authority predicate SHALL be: Approved means the canonical file has `Status: Approved` and the `codebase/map` validator returns pass; otherwise the map is Absent (no file) or Non-authoritative.
- **SDOC-1.10** THE SYSTEM SHALL NOT install or seed a catalog copy into consuming repositories. Consumers hold only Hybrid 1A artifacts they have adopted at the consumer paths.
- **SDOC-1.11** WHEN resolving `/define-system-doc <entry-key>` THE SYSTEM SHALL locate the `define-system-doc` skill directory, extract only that entry's `CATALOG.md` row, load only that entry package file, and load only the template, validator, and other resources named by that entry — not the full catalog body, every template, or the whole documentation tree by default.
- **SDOC-1.12** THE SYSTEM SHALL resolve `define-system-doc` catalog, templates, and validators from paths co-located under `skills/project/define-system-doc/` as the primary load path so a flat skill installation receives them with the skill folder.

## 2. Author one system-doc artifact (`/define-system-doc`)

**Story:** As a skill-mediated actor, I want to run a user-invoked one-artifact authoring workflow for `codebase/map`, so that I can produce a valid Approved consumer Codebase Map from bounded evidence without configuring the whole system-doc tree first.

- **SDOC-2.1** THE SYSTEM SHALL provide a user-invoked skill `define-system-doc` under `skills/project/define-system-doc/` that authors exactly one catalog entry per invocation and carries `disable-model-invocation: true`.
- **SDOC-2.2** WHEN the actor invokes `/define-system-doc codebase/map` (or equivalent harness invocation naming entry key `codebase/map`) THE SYSTEM SHALL start from that single concrete artifact need and SHALL NOT ask the actor to configure or create the entire Hybrid 1A tree.
- **SDOC-2.3** THE SYSTEM SHALL NOT create empty consumer directories or empty canonical consumer files as part of starting an authoring session.
- **SDOC-2.4** WHEN the actor authors `codebase/map` THE SYSTEM SHALL use the entry's template required slots; every required slot SHALL end as confirmed content, confirmed `None` / not applicable, or a named blocker before approval is allowed.
- **SDOC-2.5** IF a high-impact required slot is a named blocker THEN THE SYSTEM SHALL prevent approval of the canonical write until the blocker is resolved or the slot is explicitly set to confirmed content or confirmed `None` / not applicable.
- **SDOC-2.6** BEFORE presenting a proposal for approval THE SYSTEM SHALL run the entry validator and SHALL NOT offer canonical-write approval while the validator returns fail.
- **SDOC-2.7** WHEN the actor explicitly approves a validator-passing proposal for `codebase/map` THE SYSTEM SHALL write only the canonical consumer path `docs/codebase/map.md` with `Status: Approved` and SHALL NOT create sibling Hybrid 1A artifacts in the same write.
- **SDOC-2.8** WHEN updating an existing canonical `docs/codebase/map.md` THE SYSTEM SHALL keep the previously valid Approved content authoritative until a new explicitly approved patch is applied; the patch SHALL be a targeted, explicitly approved change set that may add, modify, or remove selected content while preserving unrelated content; THE SYSTEM SHALL NOT replace the whole file with an unreviewed full rewrite that discards unrelated content (whole-file clobber without a reviewed complete replacement proposal is prohibited).
- **SDOC-2.9** WHEN the actor intends a complete replacement of the canonical file THE SYSTEM SHALL present the complete proposed new file contents for approval (not a silent overwrite); after approval and validator pass the new file becomes the Approved SSOT.
- **SDOC-2.10** THE SYSTEM SHALL show the complete proposed new file or targeted patch (from `proposal.md`) and require explicit human approval before any canonical write.
- **SDOC-2.11** THE SYSTEM SHALL treat a canonical artifact as authoritative standing project documentation only when it has `Status: Approved` and its entry validator returns pass. Draft, missing file, missing Status, unknown Status, or validator fail SHALL be non-authoritative.
- **SDOC-2.12** THE SYSTEM SHALL NOT write a `Status: Draft` file at a canonical consumer path as part of the mediated workflow. IF an external contributor places a non-Approved file at a canonical path THEN readers SHALL treat it as non-authoritative.
- **SDOC-2.13** AFTER a successful approved canonical write THE SYSTEM SHALL treat that Approved validator-passing file as the only SSOT for that subject; ephemera digests SHALL NOT compete as standing project facts.

## 3. Ephemeral authoring state

**Story:** As a skill-mediated actor, I want unfinished authoring work stored only under a bounded ephemera digest, so that I can resume without replaying chat or treating proposals as project truth.

- **SDOC-3.1** THE SYSTEM SHALL store unfinished work for an entry only under `.skills/system-docs/<entry-key>/` with exactly these files when present: `state.md`, `evidence.md`, `proposal.md` (entry-key path mirroring, e.g. `.skills/system-docs/codebase/map/`).
- **SDOC-3.2** THE SYSTEM SHALL register `.skills/system-docs/` in the shared ephemera-path SSOT (`templates/skills-ephemera-paths.md` and any pack docs that enumerate shared `.skills/` roots).
- **SDOC-3.3** WHEN writing `state.md` THE SYSTEM SHALL include only bounded orchestration state: catalog entry and canonical target; phase; confirmed decisions; explicit None/not-applicable slots; open slots and named blockers; rejected assumptions; explicit defer condition when set; last verified revision.
- **SDOC-3.4** WHEN writing `evidence.md` THE SYSTEM SHALL record a bounded claim ledger where each claim has: claim text; grade exactly one of `Verified`, `Inference`, or `Open`; source (file:line, bounded command, or human confirmation); observed git revision or runtime environment/timestamp as applicable; affected template slot.
- **SDOC-3.5** WHEN writing `proposal.md` THE SYSTEM SHALL store only the preview of the proposed new file or targeted patch; THE SYSTEM SHALL treat `proposal.md` as never an SSOT; consumer skills SHALL NOT read `proposal.md` as a standing project fact.
- **SDOC-3.6** WHEN resuming an authoring session for an entry THE SYSTEM SHALL load only: the selected catalog entry package; `state.md`; the current canonical artifact if present; evidence relevant to open or stale slots; the entry template and validator — and SHALL NOT replay the full conversation, load the full catalog, or rescan the whole repository by default.
- **SDOC-3.7** WHEN revalidating evidence THE SYSTEM SHALL revalidate only claims affected by repository or runtime changes; repository claims SHALL carry the observed revision; runtime claims SHALL carry environment and timestamp.
- **SDOC-3.8** AFTER a successful approved canonical write THE SYSTEM SHALL mark the digest complete in `state.md` (or equivalent complete phase) so resume does not treat the session as an open authoring run.

## 4. Evidence grades and human confirmation

**Story:** As a skill-mediated actor, I want repository facts, inferences, and open questions separated, so that durable system docs do not silently invent compliance, ownership, topology, or operational procedure.

- **SDOC-4.1** THE SYSTEM SHALL separate verified repository/runtime facts, human decisions, inferences, and unresolved questions in the evidence ledger and authoring dialogue.
- **SDOC-4.2** WHEN recording a Verified repository claim THE SYSTEM SHALL cite file and line evidence where possible (or a bounded command result with revision).
- **SDOC-4.3** THE SYSTEM SHALL NOT promote Inference-graded claims about compliance obligations, SLO targets, trust boundaries, ownership, runtime topology, or operational procedures into durable project documentation without explicit human confirmation that regrades or replaces them as confirmed content.
- **SDOC-4.4** WHILE a claim remains grade `Inference` THE SYSTEM SHALL keep it explicitly labeled as inference in `evidence.md` and SHALL NOT silently promote it to Verified or to Approved canonical text.

## 5. Suggest authoring without auto-invoke

**Story:** As a skill-mediated actor running planning, I want at most one clear suggestion to author a missing Codebase Map when placement is uncertain, so that I discover the workflow without the agent auto-running a user-invoked skill.

- **SDOC-5.1** WHEN `plan-tasks` is producing or revising a plan and placement of new or changed production paths is materially uncertain because no valid Approved Codebase Map is available (file absent, non-authoritative Status, or validator fail) THE SYSTEM SHALL suggest exactly the action `/define-system-doc codebase/map` and SHALL explain why the Codebase Map would help at that planning decision point.
- **SDOC-5.2** THE SYSTEM SHALL present that suggestion at most once per artifact entry key (`codebase/map`) within a single parent `plan-tasks` workflow run.
- **SDOC-5.3** THE SYSTEM SHALL NEVER auto-invoke `define-system-doc` from `plan-tasks` or any other model-invoked skill.
- **SDOC-5.4** WHEN the actor declines the suggestion within that parent run THE SYSTEM SHALL suppress further suggestions for `codebase/map` for the remainder of that run.
- **SDOC-5.5** THE SYSTEM SHALL persist a deferment for `codebase/map` only when the actor explicitly supplies a defer condition; THE SYSTEM SHALL NOT invent fixed defer periods or claim cross-machine suppression from gitignored ephemera alone.

## 6. Plan-tasks consults valid Approved Codebase Map

**Story:** As a skill-mediated actor, I want `plan-tasks` to consult only a valid Approved Codebase Map when available, so that task File Structure and placement follow authoritative placement rules instead of inventing folder conventions.

- **SDOC-6.1** WHEN `docs/codebase/map.md` has `Status: Approved` and the `codebase/map` validator returns pass, and `plan-tasks` is writing or revising the plan's file map / placement guidance, THE SYSTEM SHALL read that map (or a bounded digest extracted for the decision) and SHALL align planned paths with the map's placement rules.
- **SDOC-6.2** WHERE no valid Approved Codebase Map is available (absent, Draft, missing/unknown Status, or validator fail) THE SYSTEM SHALL continue `plan-tasks` without failing the skill solely for that absence (no-op consult) and MAY apply SDOC-5.x suggestion rules when placement uncertainty is material.
- **SDOC-6.3** THE SYSTEM SHALL NOT consult a Codebase Map as authoritative standing guidance when the validator returns fail or Status is not `Approved`.
- **SDOC-6.4** THE SYSTEM SHALL list `plan-tasks` as a reader of `codebase/map` in the entry package only because this consult hook exists; THE SYSTEM SHALL NOT list any other skill as a reader of `codebase/map` in this feature unless that skill also gains a real consult hook and tests in this feature's scope.
- **SDOC-6.5** THE SYSTEM SHALL keep consumer canonical path `docs/codebase/map.md` documented in the entry package contract; pack implementation Surfaces remain under `skills/project/define-system-doc/` and related pack paths.

## 7. Codebase Map template and validator

**Story:** As a skill-mediated actor, I want a Codebase Map template and a pass/fail validator, so that Approved maps are complete enough for planning and invalid maps are never treated as authoritative.

- **SDOC-7.1** THE SYSTEM SHALL ship template `skills/project/define-system-doc/templates/codebase/map.md` and validator `skills/project/define-system-doc/validators/codebase/map.md` for entry key `codebase/map`.
- **SDOC-7.2** THE SYSTEM SHALL require the Codebase Map template to include required slots covering at least: purpose and boundary of the map; top-level layout (path → purpose); placement rules for where new code of named kinds belongs; explicit `None` allowed per slot when not applicable; and a statement that the map is not the architecture invariant spine and not a feature registry.
- **SDOC-7.3** WHEN the `codebase/map` validator runs THE SYSTEM SHALL return pass or fail (no soft maybe) and SHALL fail when any required slot is missing or incomplete, when any named blocker remains unresolved, when forbidden placeholders (including `TBD`, `TODO`, `...`, or `lorem`) appear in required slot content, or when the document is not ready for canonical write (including missing or non-`Approved` Status in a proposed canonical body).
- **SDOC-7.4** THE SYSTEM SHALL document that Codebase Map content is addressable by catalog entry key, canonical path, and headings — without introducing greppable placement-rule IDs in this feature.

## 8. Guide and architecture narrative sync

**Story:** As a human adopter, I want a human guide page for system docs that stays synchronized with catalog entry keys, so that I can learn the model without a second SSOT.

- **SDOC-8.1** THE SYSTEM SHALL provide `docs/guide/concepts/system-docs.md` explaining the system-docs model, Hybrid 1A overview (referencing the normative inventory), maturity meanings, authoring via `/define-system-doc`, ephemera rules, authoritative Status/validator rules, and the Codebase Map loop, with links into the pack catalog (not a duplicated maturity table that becomes a second SSOT).
- **SDOC-8.2** WHEN the catalog's set of entry keys changes THE SYSTEM SHALL keep guide references to entry keys synchronized, verified by pack tests that fail on guide entry-key references that are missing from `CATALOG.md` or on First-class claims in the guide for rows that are not First-class in `CATALOG.md`.
- **SDOC-8.3** THE SYSTEM SHALL update `docs/architecture/artifacts.md` to link to the pack catalog / system-docs guide for the system-docs model and SHALL NOT restate full catalog rows there.
- **SDOC-8.4** THE SYSTEM SHALL document duplication rules: `CATALOG.md` owns identity, maturity, package pointer; entry package owns remaining contract fields; templates own consumer document shape only; validators own pass/fail checks; reader skills own minimal executable applicability and consult behavior; human guide owns explanation, examples, and links only.

## 9. Quality attributes

**Section-kind:** nfr

**Story:** As a stakeholder, I want measurable quality targets for this feature, so that how-well is not left implicit.

- **Performance:** None — pack documentation and skill orchestration; no runtime latency budget for an interactive app surface.
- **Security:** **SDOC-9.1** WHEN authoring or consulting system docs THE SYSTEM SHALL NOT treat ephemera under `.skills/system-docs/` or `proposal.md` as standing security or compliance truth — verified by skill text and tests asserting proposal/ephemera non-SSOT rules.
- **Reliability:** **SDOC-9.2** WHEN the catalog index and an entry package disagree on maturity THE SYSTEM SHALL treat `CATALOG.md` as authoritative for maturity — verified by pack test or skill rule that maturity is read only from the index row.
- **Reliability:** **SDOC-9.3** WHEN a First-class maturity claim is made in `CATALOG.md` THE SYSTEM SHALL fail pack tests if SDOC-1.7 machine-checkable evidence is incomplete — verified by the First-class package completeness test.
- **Accessibility:** None — no end-user interactive UI in this feature; human guide is static markdown.

## 10. Guards for existing behavior

Files this feature is expected to touch (pack), with guards:

| Path / area | Guard |
|---|---|
| `skills/spec/plan-tasks/SKILL.md` | **SDOC-10.1** (guard) WHEN `plan-tasks` runs and no valid Approved Codebase Map is available THE SYSTEM SHALL CONTINUE TO produce a tasks plan without requiring system-docs authoring to complete. |
| `skills/spec/plan-tasks/SKILL.md` | **SDOC-10.2** (guard) WHEN `plan-tasks` folds architecture invariants and guidelines/project constraints into Global Constraints THE SYSTEM SHALL CONTINUE TO do so under existing rules (Codebase Map consult is additive when a valid Approved map exists). |
| `skills/project/define-project/SKILL.md` | **SDOC-10.3** (guard) WHEN `define-project` is used THE SYSTEM SHALL CONTINUE TO own vision, architecture spine, and guidelines authoring paths already specified; this feature SHALL NOT remove those entry points. |
| `docs/architecture/artifacts.md` | **SDOC-10.4** (guard) WHEN artifacts narrative is updated THE SYSTEM SHALL CONTINUE TO describe the feature triad, agents config, glossary, ADRs, out-of-scope, and ephemera model; system-docs content is link/extension, not a wipe of that narrative. |
| `templates/skills-ephemera-paths.md` | **SDOC-10.5** (guard) WHEN `.skills/system-docs/` is registered THE SYSTEM SHALL CONTINUE TO document existing shared roots (pathfind, research, decisions, pr-packages) without removing them. |
| `skills/execution/audit-trace/` | **SDOC-10.6** (guard) WHEN this feature lands THE SYSTEM SHALL CONTINUE TO leave audit-trace system-ID families (`TB-N`, `THR-N`, `CMP-N`, `SLO-N`) unimplemented until ROAD-13/ROAD-14; ROAD-7 SHALL NOT claim those audit passes as delivered. |
| New `define-system-doc` skill tree | no prior behavior to guard |
| New catalog/templates/validators for `codebase/map` | no prior behavior to guard |
| New `docs/guide/concepts/system-docs.md` | no prior behavior to guard |
| Pack tests under `tests/` (new modules) | no prior behavior to guard |

## Out of Scope

- Completing First-class for Hybrid 1A rows other than those that honestly satisfy SDOC-1.7 after ROAD-7 (expected: `codebase/map` plus any pre-existing rows that already meet First-class evidence) — remaining rows are ROAD-8…ROAD-14.
- Implementing `TB-N` / `THR-N` / `CMP-N` / `SLO-N` minting or audit-trace passes for them (ROAD-13 / ROAD-14).
- `Security:` / `Reliability:` design citation fields (ROAD-13 / ROAD-14).
- Authoring product personas/metrics/principles, architecture shape files, standards tree, security docs, or ops docs as First-class packages beyond catalog inventory and honest maturity (later ROADs).
- Expanding `define-project` to author the full standards tree (ROAD-11).
- Making `docs/agents/project.md` `## Paths` an operational path remapper.
- Seeding empty Hybrid 1A trees in consumer repos via bootstrap/configure.
- Consumer-side catalog mirror (generated or hand-maintained).
- Auto-invoking user-invoked author skills from model-invoked skills.
- Cross-machine deferral memory based on gitignored state.
- Feature registry / OWNS changes via `map-features` (unchanged charter).
- Durable writes from `scan-architecture` (remains propose-only).
- Behavioral acceptance of packaging-baseline investigation outcomes (see Design risks).

## Design risks and implementation notes (non-normative)

These items are **not** acceptance criteria. They guide `design-solution` / `plan-tasks` / replan:

1. **Packaging baseline (verified fact):** flat installation carries skill-local sibling resources but does not provide root templates at some skills' documented fallback path. **Primary mitigation for this feature:** SDOC-1.12 skill-local resolution for `define-system-doc`. During implementation, investigate whether other owner skills' documented fallbacks need a small in-scope fix; if material, stop and run the formal replan workflow rather than expanding ROAD-7 silently.
2. **Existing-row honesty:** setting `CATALOG.md` maturity for pre-existing Hybrid 1A rows may reveal gaps against SDOC-1.6/1.7. Catalog honesty (do not mark First-class without evidence) is required by SDOC-1.7–1.8. Repairing missing hooks/templates for non-`codebase/map` rows is out of ROAD-7 scope unless a tiny documentation-only fix; material defects → replan.
3. **Guidelines migration:** `product/guidelines` remains in the inventory; legacy fallback only until content migrates to `docs/standards/`; pointer only afterward; never parallel SSOT — detailed migration behavior is ROAD-11.

## Open Questions

None for product behavior. Packaging materiality remains an implementation judgment under Design risks.
