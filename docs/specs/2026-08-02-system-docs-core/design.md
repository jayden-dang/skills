# Design: System-docs core + Codebase Map

Feature code: SDOC
Status: Approved
Date: 2026-08-02
Requirements: ./requirements.md

## Context

Today the skill set has an optional project-docs layer (vision, architecture spine, guidelines) authored by `define-project`, a feature triad under `docs/specs/`, agent config under `docs/agents/`, glossary/ADRs/out-of-scope, and roadmap. There is **no** pack-local system-docs catalog, no `/define-system-doc` one-artifact authoring loop, no consumer `docs/codebase/map.md` contract, and no `plan-tasks` consult of a Codebase Map. Placement guidance is ad hoc in each plan's File Structure step.

The binding constraint is **ARCH-2 / ARCH-3**: every specialized system-doc layer stays optional (no-op when absent or non-authoritative), and consumer repos must not require vendored tooling to adopt the methodology. That rules out a generated graph service, a mandatory empty Hybrid 1A seed tree, and a consumer-side catalog mirror. Catalog and validators live **in the pack** beside the skill; consumer authority is derived at runtime from entry-specific predicates.

`plan-tasks` already owns File Structure and Global Constraints and is the locked first reader for `codebase/map`. Ephemera path SSOT already lives in `templates/skills-ephemera-paths.md` (SKNS pattern). Tests for skill contracts are Python `unittest` over skill markdown and fixture trees (see `tests/test_skills_namespace_contract.py`). Skills become installable only when listed in **both** `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` (plus AGENTS.md / architecture skill inventory for human and agent discovery).

**Fresh retrieval (advisory):** neighbors by surface/terms include SKNS (ephemera paths), DOSP (docs-only IDs, guidelines), RMAP/PFIND (program/project layer), FSUB/FSUBR (Files/OWNS — not a substitute for Codebase Map). No existing feature owns system-docs catalog or define-system-doc.

**Spine reliance:** ARCH-2 (optional layers no-op), ARCH-3 (zero mandatory consumer tooling — validators enforced by pack skill procedures + pack tests), ARCH-5 (user-invoked author never auto-run from model skills), ARCH-4 (frozen SDOC strings cited exactly; one primary Satisfies owner per ID).

## Decisions

1. **Pack-local catalog SSOT** under `skills/project/define-system-doc/catalog/` — not under `docs/architecture/`, not seeded into consumers.
2. **Hybrid 1A inventory is exactly 36 entry keys** (normative table in requirements); maturity only in `CATALOG.md`.
3. **Multi-writer:** `define-project` keeps product + architecture spine; `/define-system-doc` authors one non-owned-elsewhere artifact per run; ROAD-7 only fully First-classes `codebase/map`.
4. **Authority is entry-specific**; for `codebase/map`, Approved = `Status: Approved` + validator pass.
5. **Ephemera** only under `.skills/system-docs/<entry-key>/{state,evidence,proposal}.md`; never mediated Draft at canonical path.
6. **Targeted approved patches** for updates (add/modify/remove selected content); no silent whole-file clobber.
7. **Validators** are structural/deterministic pack markdown contracts plus pack tests (no consumer binary; no semantic prose judgment).
8. **First-class reader evidence** requires applicability / authoritative consult / no-op / suggestion tests — not entry-key string presence alone.
9. **Primary resource load** is skill-local under `define-system-doc/`; packaging baseline investigation is design-risk, not a product criterion.
10. No new greppable placement-rule IDs; map addressable by entry key, path, headings.
11. **Skill packaging is complete registration:** skill directory + both plugin manifests + AGENTS.md + architecture skill inventory + tests that the path appears in both JSON files and both files remain valid JSON.
12. **Placement-conflict precedence:** hard constraints (Approved requirements/design, ARCH-N, standing project constraints) outrank Codebase Map; map guides only within hard constraints; conflicts are surfaced, hard constraint wins, map update suggested via `/define-system-doc codebase/map`, never auto-invoked.
13. **Exactly one primary `Satisfies:` owner** per requirement ID; supporting modules use `Supports:` or `Verification for:`.

No ADR this slice: pack-local catalog vs architecture path was discovery-locked and is consistent with ARCH-2; not surprising relative to other skill-local resources.

## Architecture

### Catalog index and entry packages

Satisfies: SDOC-1.1, SDOC-1.2, SDOC-1.3, SDOC-1.4, SDOC-1.5, SDOC-1.6, SDOC-1.7, SDOC-1.8, SDOC-1.9, SDOC-1.10, SDOC-1.11, SDOC-1.12, SDOC-9.2, SDOC-9.3
Reuse: none — new code (rung 7) — no existing catalog of system-doc entries; mirror SKNS “SSOT markdown + contract tests” pattern only
Respects: ARCH-2, ARCH-3, ARCH-4
Interface: `CATALOG.md` row (entry key, maturity, package pointer); entry package fields; resolve(entry_key) → {row, package, template_path, validator_path}; authority_predicate(entry) → Absent | Non-authoritative | Approved
Depth: Callers need only resolve(entry_key) and maturity/authority results — not the full inventory prose or guide.
Locality: create `skills/project/define-system-doc/catalog/**`; leave other skills until hooks; pack tests verify (do not own) inventory IDs

Layout:

```
skills/project/define-system-doc/
  SKILL.md
  catalog/CATALOG.md
  catalog/entries/<domain>/<name>.md   # slash key → nested path
  templates/<domain>/<name>.md
  validators/<domain>/<name>.md
```

`CATALOG.md` lists all 36 keys. For ROAD-7 ship: `codebase/map` may be First-class when SDOC-1.7 holds; other rows honest Recognized/First-class/Deferred per evidence. Entry packages for non-First-class rows still exist for Recognized (purpose/boundary/path/applicability, no template/validator/reader claims) or Deferred fields as `None — deferred` where required.

Resolution algorithm (skill procedure, not a runtime binary):

1. `SKILL_DIR` = directory containing `define-system-doc/SKILL.md`
2. Read `SKILL_DIR/catalog/CATALOG.md`; find row for entry key
3. Load only `SKILL_DIR/` + package pointer relative path
4. Load only named template/validator under `SKILL_DIR/`

### define-system-doc authoring skill

Satisfies: SDOC-2.1, SDOC-2.2, SDOC-2.3, SDOC-2.4, SDOC-2.5, SDOC-2.6, SDOC-2.7, SDOC-2.8, SDOC-2.9, SDOC-2.10, SDOC-2.11, SDOC-2.12, SDOC-2.13, SDOC-4.1, SDOC-4.2, SDOC-4.3, SDOC-4.4
Reuse: rung 2 — pattern of user-invoked skills with `disable-model-invocation: true` (`define-project`, `map-features` propose→confirm); no shared authoring engine exists
Respects: ARCH-5, ARCH-2
Interface: invoke with entry key; phases draft→evidence→propose→validate→approve→write; never auto-invoked
Depth: Callers (humans/harness) only need “one entry key in, optional Approved consumer file out.”
Locality: create `skills/project/define-system-doc/SKILL.md`; leave `define-project` ownership of vision/spine

Skill body (imperative checklist):

1. Parse entry key; refuse unknown keys not in CATALOG.
2. Bound-load package + template + validator (catalog module).
3. Resume from ephemera if present; else start empty state.
4. Fill required slots; grade evidence; never promote high-risk Inference without human confirm (factual correctness of placement content is human/evidence, not the structural validator).
5. Write `proposal.md` as full file or targeted patch.
6. Run structural validator; on fail, no approval offer.
7. On explicit approve: apply write to canonical path only; set Status Approved for single-file entries like map; mark digest complete.

For ROAD-7, only `codebase/map` is a legal full authoring target with template+validator shipped complete. Other keys may resolve for inventory honesty but authoring returns “not First-class / no template” unless later ROADs land packages.

SDOC-2.6 and SDOC-2.11 are owned here (authoring workflow runs validator and treats Approved+pass as authoritative for map writes/reads in this skill). The validator module **implements** the checks those criteria invoke (see Supports).

### Ephemeral working state

Satisfies: SDOC-3.1, SDOC-3.2, SDOC-3.3, SDOC-3.4, SDOC-3.5, SDOC-3.6, SDOC-3.7, SDOC-3.8, SDOC-9.1, SDOC-10.5
Reuse: rung 2 — extend `templates/skills-ephemera-paths.md` shared-roots table (SKNS pattern)
Respects: ARCH-3
Interface: paths `.skills/system-docs/<entry-key>/{state,evidence,proposal}.md`; readers of project facts never open proposal.md
Depth: Orchestration state schema only — not conversation history.
Locality: extend ephemera SSOT; create digests only at runtime in consumer checkouts

Entry-key path mirroring: `codebase/map` → `.skills/system-docs/codebase/map/`.

### Codebase Map template and validator

Satisfies: SDOC-7.1, SDOC-7.2, SDOC-7.3, SDOC-7.4
Supports: SDOC-2.6, SDOC-2.11 (structural checks invoked by authoring authority rules)
Reuse: none — new code (rung 7) — no existing codebase map template
Interface: fixed required headings/slots; `validate_codebase_map(text) -> pass|fail` + structured reason list (deterministic only)
Depth: Callers need pass/fail + machine reasons; not a semantic summary of placement prose.
Locality: create template + validator under skill dir; tests under `tests/`

**Template required headings/slots (exact names locked in template; validator checks presence):**

| Slot / heading | Structural completeness rule |
|---|---|
| Purpose and boundary | Non-empty section body, or exact line `None — <reason>` |
| Top-level layout | A markdown table with header row plus ≥1 data row of `path \| purpose`, **or** exact line `None — <reason>` |
| Placement rules | Non-empty section body with ≥1 rule bullet/paragraph, **or** exact line `None — <reason>` |
| Not spine / not feature registry | Fixed disclaimer paragraph present (template provides text; validator checks non-empty presence of the disclaimer heading+body) |
| Status (canonical-write readiness only) | When validating a proposed or on-disk canonical body for write readiness or authority: line matching `Status: Approved` (exact status token) |

**Deterministic fail conditions (structural only — no semantic judgment of whether placement is “correct”):**

1. Any required heading missing.
2. Any required slot fails its completeness rule above (empty body without valid `None — <reason>` form; layout table missing or zero data rows without `None — <reason>`).
3. Unresolved named blockers: lines matching a declared blocker marker (template uses `Blocker:` or `**Blocker:**` prefix) that are not marked resolved per template convention (`Resolved:` companion or strikethrough of the blocker line — exact convention fixed in validator doc).
4. Forbidden placeholders in required-slot bodies (case-insensitive whole-token / substring scan): `TBD`, `TODO`, `...`, `lorem`.
5. Canonical-write readiness check: required `Status: Approved` missing or Status token not exactly `Approved`.

**Explicit non-goals of the validator:** It does **not** judge whether paths exist on disk, whether placement rules are wise, or whether prose is accurate. Evidence grades and human confirmation own factual correctness (SDOC-4.x).

**Authority predicate (`codebase/map`):**  
- Absent: no file at `docs/codebase/map.md`  
- Non-authoritative: file exists but Status ≠ Approved or structural validator fail  
- Approved: Status Approved and structural validator pass  

### plan-tasks consult and suggestion hooks

Satisfies: SDOC-5.1, SDOC-5.2, SDOC-5.3, SDOC-5.4, SDOC-5.5, SDOC-6.1, SDOC-6.2, SDOC-6.3, SDOC-6.4, SDOC-6.5, SDOC-10.1, SDOC-10.2
Reuse: rung 2 — extend `skills/spec/plan-tasks/SKILL.md` File Structure + Global Constraints flow
Respects: ARCH-2, ARCH-5
Interface: after File Structure step starts: `map_authority()`; if Approved consult digest within hard-constraint envelope; if not and placement uncertain → suggest once; never invoke define-system-doc
Depth: plan-tasks needs only authority result + placement rules digest + conflict surface, not full authoring workflow.
Locality: extend plan-tasks only; leave other consumers out of ROAD-7

**Applicability predicate:** plan-tasks is writing/revising File Structure or path placement guidance for production paths.

**Hard constraints (outrank the map):**

1. Approved feature `requirements.md` / `design.md` path and behavior constraints for the plan under construction.
2. Live `ARCH-N` invariants folded into Global Constraints.
3. Standing project constraints from `docs/product/guidelines.md` (or `docs/agents/project.md` fallback) and other standing config already sourced by plan-tasks.

**Codebase Map role:** When authoritative, the map **guides** placement of files **only within** those hard constraints. It is advisory relative to hard constraints, not a license to violate them.

**Placement-conflict procedure:**

1. Compute planned paths from hard constraints first.
2. If map is authoritative, attempt to align File Structure with map placement rules **without** violating hard constraints.
3. IF a map placement rule conflicts with a hard constraint THEN plan-tasks SHALL:
   - **surface** the conflict explicitly in the plan (or planner dialogue) naming the hard constraint and the map rule;
   - **preserve** the hard constraint in the planned File Structure;
   - **suggest** updating the map via exactly `/define-system-doc codebase/map` (counts toward the once-per-run suggestion budget for that entry when emitted);
   - **never** auto-invoke `define-system-doc`;
   - **never** silently follow the map over the hard constraint;
   - **never** silently drop the map without surfacing when a concrete conflict was detected.

**Consult when authoritative and no conflict:** read map (or extract layout + placement rules section); align File Structure with placement rules; record that Codebase Map was consulted.

**No-op when absent/non-authoritative:** continue plan without failure; optional suggestion when placement uncertainty is material (SDOC-5.x).

**Suggestion protocol:** at most once per `codebase/map` per plan-tasks run; exact string `/define-system-doc codebase/map` + why; suppress after decline for rest of run; persist defer only if user supplies condition; never auto-invoke.

**Reader tests (verification for SDOC-1.7 on plan-tasks):** fixture trees with (a) no map, (b) Draft/invalid map, (c) Approved valid map, (d) Approved map that conflicts with a fixture hard constraint — assert no-op / suggestion / consult / conflict surface + hard constraint wins + no auto-invoke.

### Guide and architecture narrative

Satisfies: SDOC-8.1, SDOC-8.2, SDOC-8.3, SDOC-8.4, SDOC-10.4
Reuse: rung 2 — extend `docs/guide/concepts/artifacts.md` link pattern; new page mirrors other concept guides
Interface: human-readable guide; tests sync entry-key mentions to CATALOG
Depth: Guide explains; does not redefine maturity SSOT.
Locality: create `docs/guide/concepts/system-docs.md`; patch `docs/architecture/artifacts.md`; leave full architecture domains

### Registration and packaging surfaces

Satisfies: SDOC-10.3
Supports: SDOC-2.1 (installability and discovery of the user-invoked skill)
Reuse: rung 2 — existing dual-manifest + AGENTS.md + architecture skills inventory pattern
Respects: ARCH-5 (registered as user-invoked with `disable-model-invocation: true`)
Interface: skill path `./skills/project/define-system-doc` listed for install and inventory
Depth: Registration is path presence + valid manifests + inventory lines — not skill body logic.
Locality: extend manifests and inventories; leave define-project behavior

**Must update all of:**

| Surface | Change |
|---|---|
| `.claude-plugin/plugin.json` | Add `"./skills/project/define-system-doc"` to `skills` array; keep JSON valid |
| `.claude-plugin/marketplace.json` | Add the same path in the marketplace skills list; keep JSON valid |
| `AGENTS.md` | Project category skill list + any count/table that enumerates skills |
| `docs/architecture/skills.md` | Skill inventory entry for define-system-doc (user-invoked, purpose) |
| Human guide skill index if present | `docs/guide/skills/` registration / README link as pack convention requires for new skills |

Creating `skills/project/define-system-doc/` alone is **insufficient** for reliable install.

**Verification for registration:** pack tests assert (1) both JSON files parse as valid JSON; (2) both contain the exact skills path string `./skills/project/define-system-doc` (or the pack’s established relative form used by neighboring project skills); (3) AGENTS.md and `docs/architecture/skills.md` mention the skill.

### Pack test suite (SDOC contracts)

Satisfies: SDOC-10.6
Verification for: SDOC-1.2, SDOC-1.7, SDOC-1.8, SDOC-8.2, SDOC-9.3, SDOC-5.x, SDOC-6.x, SDOC-10.3, registration packaging
Reuse: rung 2 — `tests/test_*_contract.py` + optional `tests/<feature>/scenarios.md` pattern (SKNS, FSUB)
Interface: unittest modules fail CI on inventory set mismatch, First-class package holes, reader contract holes, guide drift, invalid/missing manifest registration; assert no TB/THR/CMP/SLO audit-trace delivery claims in this feature
Depth: Tests observe files + skill text + fixtures only.
Locality: create `tests/test_sdoc_system_docs_contract.py` (and fixtures under `tests/system-docs/` if needed)

Primary ownership of SDOC-1.2 / 1.7 / 1.8 / 9.3 remains **Catalog index**; of SDOC-8.2 **Guide**; of SDOC-5/6 **plan-tasks**; of SDOC-10.3 **Registration**. This suite verifies those plus owns the SDOC-10.6 absence guard.

## Seams for testing

| Seam | Kind | Covers (primary IDs) | Notes |
|---|---|---|---|
| `catalog/CATALOG.md` + inventory set equality | unit | SDOC-1.1, SDOC-1.2 | |
| entry package path layout + required fields | unit | SDOC-1.3–1.6, SDOC-1.9–1.12 | |
| First-class package + full reader tests (a–d) | unit | SDOC-1.7, SDOC-1.8, SDOC-9.3 | |
| maturity authority in CATALOG only | unit | SDOC-9.2 | |
| structural validator fixtures | unit | SDOC-7.1–7.4 | Supports 2.6/2.11 |
| `define-system-doc/SKILL.md` contracts | unit + scenario | SDOC-2.1–2.13, SDOC-4.1–4.4 | |
| ephemera SSOT + skill ephemera roles | unit | SDOC-3.1–3.8, SDOC-9.1, SDOC-10.5 | |
| `plan-tasks` hooks + conflict precedence | unit + scenario | SDOC-5.1–5.5, SDOC-6.1–6.5, SDOC-10.1–10.2 | |
| guide + artifacts sync | unit | SDOC-8.1–8.4, SDOC-10.4 | |
| plugin.json + marketplace.json registration + valid JSON | unit | SDOC-10.3 | Supports 2.1 installability |
| AGENTS.md + docs/architecture/skills.md inventory | unit | SDOC-10.3 | |
| audit-trace not claiming TB/SLO in this feature | unit | SDOC-10.6 | |

## Coverage check

Exactly-one primary `Satisfies:` owner. Supporting modules listed under Supports / Verification for only.

| ID | Primary Satisfies section |
|---|---|
| SDOC-1.1 | Catalog index and entry packages |
| SDOC-1.2 | Catalog index and entry packages |
| SDOC-1.3 | Catalog index and entry packages |
| SDOC-1.4 | Catalog index and entry packages |
| SDOC-1.5 | Catalog index and entry packages |
| SDOC-1.6 | Catalog index and entry packages |
| SDOC-1.7 | Catalog index and entry packages |
| SDOC-1.8 | Catalog index and entry packages |
| SDOC-1.9 | Catalog index and entry packages |
| SDOC-1.10 | Catalog index and entry packages |
| SDOC-1.11 | Catalog index and entry packages |
| SDOC-1.12 | Catalog index and entry packages |
| SDOC-2.1 | define-system-doc authoring skill |
| SDOC-2.2 | define-system-doc authoring skill |
| SDOC-2.3 | define-system-doc authoring skill |
| SDOC-2.4 | define-system-doc authoring skill |
| SDOC-2.5 | define-system-doc authoring skill |
| SDOC-2.6 | define-system-doc authoring skill |
| SDOC-2.7 | define-system-doc authoring skill |
| SDOC-2.8 | define-system-doc authoring skill |
| SDOC-2.9 | define-system-doc authoring skill |
| SDOC-2.10 | define-system-doc authoring skill |
| SDOC-2.11 | define-system-doc authoring skill |
| SDOC-2.12 | define-system-doc authoring skill |
| SDOC-2.13 | define-system-doc authoring skill |
| SDOC-3.1 | Ephemeral working state |
| SDOC-3.2 | Ephemeral working state |
| SDOC-3.3 | Ephemeral working state |
| SDOC-3.4 | Ephemeral working state |
| SDOC-3.5 | Ephemeral working state |
| SDOC-3.6 | Ephemeral working state |
| SDOC-3.7 | Ephemeral working state |
| SDOC-3.8 | Ephemeral working state |
| SDOC-4.1 | define-system-doc authoring skill |
| SDOC-4.2 | define-system-doc authoring skill |
| SDOC-4.3 | define-system-doc authoring skill |
| SDOC-4.4 | define-system-doc authoring skill |
| SDOC-5.1 | plan-tasks consult and suggestion hooks |
| SDOC-5.2 | plan-tasks consult and suggestion hooks |
| SDOC-5.3 | plan-tasks consult and suggestion hooks |
| SDOC-5.4 | plan-tasks consult and suggestion hooks |
| SDOC-5.5 | plan-tasks consult and suggestion hooks |
| SDOC-6.1 | plan-tasks consult and suggestion hooks |
| SDOC-6.2 | plan-tasks consult and suggestion hooks |
| SDOC-6.3 | plan-tasks consult and suggestion hooks |
| SDOC-6.4 | plan-tasks consult and suggestion hooks |
| SDOC-6.5 | plan-tasks consult and suggestion hooks |
| SDOC-7.1 | Codebase Map template and validator |
| SDOC-7.2 | Codebase Map template and validator |
| SDOC-7.3 | Codebase Map template and validator |
| SDOC-7.4 | Codebase Map template and validator |
| SDOC-8.1 | Guide and architecture narrative |
| SDOC-8.2 | Guide and architecture narrative |
| SDOC-8.3 | Guide and architecture narrative |
| SDOC-8.4 | Guide and architecture narrative |
| SDOC-9.1 | Ephemeral working state |
| SDOC-9.2 | Catalog index and entry packages |
| SDOC-9.3 | Catalog index and entry packages |
| SDOC-10.1 | plan-tasks consult and suggestion hooks |
| SDOC-10.2 | plan-tasks consult and suggestion hooks |
| SDOC-10.3 | Registration and packaging surfaces |
| SDOC-10.4 | Guide and architecture narrative |
| SDOC-10.5 | Ephemeral working state |
| SDOC-10.6 | Pack test suite (assert non-delivery of TB/SLO audit) — **primary Satisfies for guard only** |

**Coverage integrity:** every Approved SDOC-N.M ID appears exactly once in a primary `Satisfies:` line above; none missing; none duplicated across primary lines; no extra IDs invented.

**Note on SDOC-10.6:** Guard criterion “do not deliver TB/SLO audit-trace in ROAD-7” is verified by pack tests and owned as Satisfies on the Pack test suite section (sole behavior is an absence assertion).

Deliberately unmapped: none.

## Design risks (from requirements, non-normative)

1. Packaging baseline: prefer skill-local load (SDOC-1.12); investigate other skills’ root-template fallback only if touched; replan if material.  
2. Existing Hybrid 1A rows: mark First-class only with SDOC-1.7 evidence; do not invent repairs for non-map rows in ROAD-7.  
3. Guidelines migration remains ROAD-11; inventory includes `product/guidelines`.
