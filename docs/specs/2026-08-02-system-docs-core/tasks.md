# Tasks: System-docs core + Codebase Map

> **For agentic workers:** after plan approval, pick one execute skill —
> `build-in-waves` (subagent waves), `build-by-story` (human-gated story review
> units), or `build-inline` (controller implements, no implementer subagents).
> The chosen skill writes `Execution-mode:`. Steps use checkbox (`- [ ]`) syntax
> for tracking.

Feature code: SDOC
Status: Approved
Date: 2026-08-02
Execution-mode: continuous
Requirements: ./requirements.md
Design: ./design.md

**Goal:** Ship pack-local Hybrid 1A catalog, `/define-system-doc` one-artifact authoring for Codebase Map, and `plan-tasks` consult/suggestion/conflict hooks so planning uses a valid Approved map without empty-forest setup or fake readers.

**Architecture:** Catalog and validators live under `skills/project/define-system-doc/`; ephemera under `.skills/system-docs/`; structural map validator only; plan-tasks hard constraints outrank the map; dual plugin manifests + inventories register the skill; pack unittest contracts prove inventory, First-class package, reader tests, and registration.

**Tech Stack:** Markdown skill procedures; Python 3 `unittest`; existing pack lint scripts; no new consumer runtime dependency.

## Global Constraints

Copied from `docs/agents/project.md` and spine / design:

- **Verify order (all must pass before completion claims):**
  - Lint: `python3 scripts/lint-skill-frontmatter.py && python3 scripts/lint-write-handoffs.py && python3 scripts/lint-context7.py`
  - Unit tests: `python3 -m unittest discover -s tests`
  - Single test module pattern: `python3 -m unittest tests.<module>`
- **ARCH-1:** Audit Trace and other vertical checks MUST be exact `grep`/`git`/file-read passes with fixed extraction rules — never LLM judgment of coverage.
- **ARCH-2:** Optional project layers and config sections MUST no-op when absent; skills MUST NOT invent standing facts that were never written.
- **ARCH-3:** Consumer-repo adoption MUST require only the skills and markdown config — never mandate Python/vendored linters/CI for the methodology default path. Pack-repo Python tests are allowed for *this* skill set only.
- **ARCH-4:** Requirement IDs and architecture IDs are immutable once defined; docs-side citations use the same greppable string; application source/tests MUST NOT be required to embed these IDs (pack fixture tests may still embed them when testing this skill set).
- **ARCH-5:** User-invoked skills may invoke model-invoked skills only; model-invoked skills must never invoke user-invoked skills; agents must never auto-invoke `disable-model-invocation: true` skills.
- **ARCH-6:** Skills enforce/record only skill-mediated actions; membership is never inferred from roster/CODEOWNERS/PR authorship alone.
- **Docs-only spine:** Do not require SDOC IDs in application consumer code; IDs live in docs/specs and task footers.
- **Solo band:** No fake multi-assignee theater.
- **Codebase Map vs hard constraints:** Approved requirements/design, ARCH-N, and standing project constraints outrank map guidance; conflicts surface; never auto-invoke `/define-system-doc`.
- **Forbidden:** Seed empty Hybrid 1A trees; write mediated Draft at canonical paths; whole-file clobber without reviewed complete replacement; claim TB/THR/CMP/SLO audit-trace in this feature; list fake readers without full reader tests.

## File Structure

| Path | Responsibility |
|---|---|
| `skills/project/define-system-doc/SKILL.md` | User-invoked one-artifact authoring procedure |
| `skills/project/define-system-doc/catalog/CATALOG.md` | Entry key \| Maturity \| package pointer (36 rows) |
| `skills/project/define-system-doc/catalog/entries/**` | Per-entry packages (all 36 keys; depth varies by maturity) |
| `skills/project/define-system-doc/templates/codebase/map.md` | Codebase Map consumer template |
| `skills/project/define-system-doc/validators/codebase/map.md` | Structural validator contract + fail rules |
| `templates/skills-ephemera-paths.md` | Register `.skills/system-docs/` shared root |
| `skills/spec/plan-tasks/SKILL.md` | Consult / suggest / conflict / no auto-invoke hooks |
| `.claude-plugin/plugin.json` | Register skill path |
| `.claude-plugin/marketplace.json` | Register skill path |
| `AGENTS.md` | Inventory / project table / skill count as needed |
| `docs/architecture/skills.md` | Architecture skill inventory entry |
| `docs/architecture/artifacts.md` | Link to system-docs guide/catalog (no row restatement) |
| `docs/guide/concepts/system-docs.md` | Human guide |
| `docs/guide/skills/README.md` (and/or `define-system-doc.md` if pack convention) | Skill index link |
| `tests/test_sdoc_system_docs_contract.py` | Contract tests |
| `tests/system-docs/` | Fixtures (maps, inventory expected set, scenarios) |

---

### Task 1: Catalog skeleton, 36-key inventory, entry packages, skill-local layout

**Files:**
- Create: `skills/project/define-system-doc/catalog/CATALOG.md`
- Create: `skills/project/define-system-doc/catalog/entries/**` (one package file per Hybrid 1A key; `codebase/map` full First-class fields; others honest Recognized/Deferred fields per design)
- Create: `tests/system-docs/expected_inventory.txt` (or embed set in test)
- Create: `tests/test_sdoc_system_docs_contract.py` (inventory section)
- Modify: none yet for plan-tasks

**Reuse:** rung 7 new catalog; pattern from SKNS SSOT + contract tests

**Interfaces:**
- Consumes: Normative 36 keys from `requirements.md` inventory table
- Produces: `CATALOG.md` rows; entry package paths; test `EXPECTED_KEYS` set equality

**Depends-on:** none

- [ ] **Step 1: Write the failing tests**

Add tests that:
1. Fail if `catalog/CATALOG.md` missing or columns ≠ Entry key | Maturity | Entry-package pointer
2. Fail if entry-key set ≠ exact 36-key normative set
3. Fail if any listed package pointer path is missing under the skill directory
4. Fail if maturity not in {First-class, Recognized, Deferred}
5. Fail if skill-local resolve paths for catalog are outside `skills/project/define-system-doc/`

Run: `python3 -m unittest tests.test_sdoc_system_docs_contract` — expect: FAIL (missing files / inventory)

- [ ] **Step 2: Implement catalog + packages**

Create CATALOG with all 36 keys. Maturity: `codebase/map` may be First-class only after later tasks complete SDOC-1.7 package — for this task mark non-map rows honestly (Recognized with purpose/boundary/path/applicability and no template/validator/reader claims, or Deferred with `None — deferred` where required). For `codebase/map` start as Recognized or leave First-class only after Task 5–6 complete; **recommended:** mark `codebase/map` Recognized until Task 6 then flip to First-class when tests pass.

Create entry packages with mirrored paths. Include authority predicate field: for `codebase/map` document Status Approved + structural validator pass.

Run: same unittest — expect: inventory tests PASS (First-class completeness tests may still skip or fail until later tasks — structure inventory tests pass).

- [ ] **Step 3: Commit**

`git commit -m "feat(sdoc): add Hybrid 1A catalog and entry packages"`

_Requirements: SDOC-1.1, SDOC-1.2, SDOC-1.3, SDOC-1.4, SDOC-1.5, SDOC-1.6, SDOC-1.9, SDOC-1.10, SDOC-1.11, SDOC-1.12, SDOC-9.2_

---

### Task 2: Ephemera root registration

**Files:**
- Modify: `templates/skills-ephemera-paths.md`
- Modify: `tests/test_sdoc_system_docs_contract.py` (ephemera assertions)
- Modify: `tests/test_skills_namespace_contract.py` only if shared-root table is grepped there and must include the new root (prefer extend SDOC tests; touch SKNS tests only if required for consistency)

**Reuse:** rung 2 — SKNS ephemera SSOT table

**Interfaces:**
- Consumes: shared-roots table format
- Produces: `.skills/system-docs/` documented with state/evidence/proposal basenames in define-system-doc skill (skill body Task 4) and SSOT row here

**Depends-on:** Task 1

- [ ] **Step 1: Failing test**

Assert `templates/skills-ephemera-paths.md` Shared roots table includes `.skills/system-docs/` with contents description for per-entry digests.

Run: `python3 -m unittest tests.test_sdoc_system_docs_contract` — expect: FAIL until row exists

- [ ] **Step 2: Implement**

Add shared root row; do not remove pathfind/research/decisions/pr-packages.

Run: unittest — expect: pass for ephemera checks

- [ ] **Step 3: Commit**

`git commit -m "feat(sdoc): register system-docs ephemera root"`

_Requirements: SDOC-3.1, SDOC-3.2, SDOC-10.5_

---

### Task 3: Codebase Map template + structural validator

**Files:**
- Create: `skills/project/define-system-doc/templates/codebase/map.md`
- Create: `skills/project/define-system-doc/validators/codebase/map.md`
- Create: `tests/system-docs/fixtures/` (pass map, fail missing slot, fail placeholder, fail no status, fail empty table)
- Modify: `tests/test_sdoc_system_docs_contract.py` (validator structural cases)
- Optional Create: `tests/system-docs/validate_map.py` helper imported by tests if parsing is non-trivial (pack-only)

**Reuse:** rung 7 new template/validator; design structural rules

**Interfaces:**
- Consumes: design slot names and fail conditions
- Produces: `validate_codebase_map(text) -> (ok: bool, reasons: list[str])` behavior in tests/helper; validator.md is the agent-facing contract

**Depends-on:** Task 1

- [ ] **Step 1: Failing tests**

Fixtures must fail/pass per design: required headings; layout table ≥1 data row or `None — reason`; placement rules or None; disclaimer; no TBD/TODO/.../lorem; blockers unresolved; Status Approved for write-readiness. Assert validator does not require path-exists checks (semantic non-goal).

Run: unittest — expect: FAIL until template/validator exist

- [ ] **Step 2: Implement template + validator contract + test harness**

Implement deterministic checks only.

Run: unittest — expect: pass

- [ ] **Step 3: Commit**

`git commit -m "feat(sdoc): add codebase map template and structural validator"`

_Requirements: SDOC-7.1, SDOC-7.2, SDOC-7.3, SDOC-7.4_

---

### Task 4: define-system-doc authoring skill body

**Files:**
- Create: `skills/project/define-system-doc/SKILL.md`
- Modify: `tests/test_sdoc_system_docs_contract.py` (frontmatter + procedure contracts)
- Modify: entry package `catalog/entries/codebase/map.md` writer field → define-system-doc

**Reuse:** rung 2 — define-project / map-features user-invoked pattern

**Interfaces:**
- Consumes: catalog resolve, template, validator, ephemera paths
- Produces: agent procedure for one-entry authoring; `disable-model-invocation: true`

**Depends-on:** Task 1, Task 2, Task 3

- [ ] **Step 1: Failing tests**

Assert SKILL.md exists; frontmatter name `define-system-doc`; `disable-model-invocation: true`; body requires: one entry per invocation; no empty-forest seed; skill-local load; ephemera state/evidence/proposal; evidence grades; no Inference promotion for high-risk classes without human confirm; validator before approve; no approve on fail; targeted patch / full replacement rules; no mediated Draft write; proposal non-SSOT; digest complete after write; resume bounds.

Run: unittest — expect: FAIL

- [ ] **Step 2: Implement SKILL.md**

Write imperative procedure matching design; description = triggering conditions only.

Run: frontmatter lint + unittest — expect: pass for skill contracts

- [ ] **Step 3: Commit**

`git commit -m "feat(sdoc): add define-system-doc authoring skill"`

_Requirements: SDOC-2.1, SDOC-2.2, SDOC-2.3, SDOC-2.4, SDOC-2.5, SDOC-2.6, SDOC-2.7, SDOC-2.8, SDOC-2.9, SDOC-2.10, SDOC-2.11, SDOC-2.12, SDOC-2.13, SDOC-3.3, SDOC-3.4, SDOC-3.5, SDOC-3.6, SDOC-3.7, SDOC-3.8, SDOC-4.1, SDOC-4.2, SDOC-4.3, SDOC-4.4, SDOC-9.1_

---

### Task 5: plan-tasks Codebase Map consult, suggestion, conflict precedence

**Files:**
- Modify: `skills/spec/plan-tasks/SKILL.md`
- Modify: `catalog/entries/codebase/map.md` readers + suggestion protocol
- Create: `tests/system-docs/plan_tasks_scenarios.md` (or embed in test)
- Modify: `tests/test_sdoc_system_docs_contract.py`

**Reuse:** rung 2 — extend plan-tasks File Structure step

**Interfaces:**
- Consumes: map authority predicate; hard constraints list from design
- Produces: consult/no-op/suggest/conflict procedure text; never auto-invoke

**Depends-on:** Task 3, Task 4

- [ ] **Step 1: Failing tests**

Assert plan-tasks skill text includes: applicability at File Structure; authority check; no-op when absent/non-authoritative; consult when Approved+pass; hard constraints outrank map; conflict surface + preserve hard constraint + suggest `/define-system-doc codebase/map`; once-per-run suggestion; suppress after decline; never auto-invoke; continue without map (guard).

Reader tests for First-class: applicability, authoritative consult, no-op, suggestion — string mention alone insufficient (require dedicated test methods or scenario sections covering a–d + conflict case).

Run: unittest — expect: FAIL

- [ ] **Step 2: Implement plan-tasks hooks**

Insert design procedure into plan-tasks (File Structure / Global Constraints adjacency as design specifies). Update entry package readers.

Run: unittest — expect: pass for plan-tasks reader contracts

- [ ] **Step 3: Commit**

`git commit -m "feat(sdoc): plan-tasks consults Codebase Map with conflict precedence"`

_Requirements: SDOC-5.1, SDOC-5.2, SDOC-5.3, SDOC-5.4, SDOC-5.5, SDOC-6.1, SDOC-6.2, SDOC-6.3, SDOC-6.4, SDOC-6.5, SDOC-10.1, SDOC-10.2_

---

### Task 6: Registration packaging + First-class maturity for codebase/map

**Files:**
- Modify: `.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json`
- Modify: `AGENTS.md`
- Modify: `docs/architecture/skills.md`
- Modify: `docs/guide/skills/README.md` (and create `docs/guide/skills/define-system-doc.md` if convention requires a page)
- Modify: `catalog/CATALOG.md` maturity for `codebase/map` → First-class when SDOC-1.7 evidence complete
- Modify: `tests/test_sdoc_system_docs_contract.py` (manifest JSON valid + path present; First-class package completeness)

**Reuse:** rung 2 — dual-manifest pattern next to define-project

**Interfaces:**
- Consumes: skill path `./skills/project/define-system-doc`
- Produces: installable registration; First-class row only with full package evidence

**Depends-on:** Task 4, Task 5

- [ ] **Step 1: Failing tests**

1. Both JSON files `json.loads` successfully
2. Both contain `./skills/project/define-system-doc`
3. AGENTS.md and docs/architecture/skills.md mention define-system-doc
4. First-class rows (including codebase/map when marked) have package+template+validator+writer+named reader+reader tests a–d

Run: unittest — expect: FAIL until registered and First-class complete

- [ ] **Step 2: Implement registration + flip maturity**

Update skill counts/tables carefully. Keep define-project entry points intact (guard).

Run: lint frontmatter + unittest — expect: pass

- [ ] **Step 3: Commit**

`git commit -m "feat(sdoc): register define-system-doc and mark codebase/map First-class"`

_Requirements: SDOC-1.7, SDOC-1.8, SDOC-9.3, SDOC-10.3, SDOC-2.1_

---

### Task 7: Human guide + architecture artifacts link

**Files:**
- Create: `docs/guide/concepts/system-docs.md`
- Modify: `docs/architecture/artifacts.md`
- Modify: `tests/test_sdoc_system_docs_contract.py` (guide key sync; no false First-class claims; artifacts links without full catalog restatement)

**Reuse:** rung 2 — concept guide pattern

**Interfaces:**
- Consumes: CATALOG keys and maturity
- Produces: human explanation + links

**Depends-on:** Task 1, Task 6

- [ ] **Step 1: Failing tests**

Guide must exist; every entry-key reference in guide ∈ CATALOG; First-class claims in guide match CATALOG; artifacts.md links to guide/catalog without duplicating maturity table.

Run: unittest — expect: FAIL

- [ ] **Step 2: Implement guide + artifacts patch**

Document model, Hybrid 1A overview, maturity, authoring, ephemera, authority, plan-tasks loop, conflict precedence; duplication rules.

Run: unittest — expect: pass

- [ ] **Step 3: Commit**

`git commit -m "docs(sdoc): add system-docs guide and artifacts link"`

_Requirements: SDOC-8.1, SDOC-8.2, SDOC-8.3, SDOC-8.4, SDOC-10.4_

---

### Task 8: Guards — define-project continuity + no TB/SLO audit delivery

**Files:**
- Modify: `tests/test_sdoc_system_docs_contract.py`
- Touch `skills/project/define-project/SKILL.md` only if a one-line cross-link is needed (prefer test-only proof that vision/spine/guidelines ownership text remains)
- Do **not** implement audit-trace TB/SLO passes

**Reuse:** rung 2 — absence assertions

**Interfaces:**
- Produces: tests that fail if define-project ownership removed; fail if SDOC ships claim of TB/THR/CMP/SLO audit-trace delivery

**Depends-on:** Task 6

- [ ] **Step 1: Failing/passing baseline tests**

Write assertions for SDOC-10.3 already partly covered; add SDOC-10.6: grep SDOC feature surfaces must not claim shipped audit-trace for TB/THR/CMP/SLO.

- [ ] **Step 2: Fix any accidental claims**

- [ ] **Step 3: Commit**

`git commit -m "test(sdoc): guard define-project ownership and no premature system-ID audit"`

_Requirements: SDOC-10.3, SDOC-10.6_

---

### Task 9: Full suite green + smoke

**Files:**
- Modify: any residual fixes from full run
- Test: full pack suite

**Depends-on:** Task 1–8

- [ ] **Step 1: Run full verification**

Run:
```
python3 scripts/lint-skill-frontmatter.py && python3 scripts/lint-write-handoffs.py && python3 scripts/lint-context7.py
python3 -m unittest discover -s tests
```

Expect: all pass, zero warnings required by project standards.

- [ ] **Step 2: Manual smoke checklist (document in task report)**

1. Catalog resolves `codebase/map` skill-locally  
2. Validator pass/fail on fixtures  
3. plan-tasks skill text contains conflict precedence and no auto-invoke  
4. Both manifests list define-system-doc  

- [ ] **Step 3: Commit if fixes**

`git commit -m "test(sdoc): full suite green for system-docs core"`

_Requirements: SDOC-1.7, SDOC-1.8, SDOC-9.3, SDOC-10.1_ (verification close-out; all prior IDs already tasked)

---

## Coverage notes (plan-tasks Step 4)

| Story / IDs | Tasks |
|---|---|
| SDOC-1.1–1.6, 1.9–1.12, 9.2 | Task 1 |
| SDOC-1.7, 1.8, 9.3 | Tasks 5–6 (reader tests + First-class flip) |
| SDOC-2.*, 3.3–3.8, 4.*, 9.1 | Task 4 (+ 3.1–3.2 Task 2) |
| SDOC-3.1–3.2, 10.5 | Task 2 |
| SDOC-5.*, 6.*, 10.1–10.2 | Task 5 |
| SDOC-7.* | Task 3 |
| SDOC-8.*, 10.4 | Task 7 |
| SDOC-10.3 | Task 6 |
| SDOC-10.6 | Task 8 |
| SDOC-2.1 also registration | Task 6 Supports installability |

All Approved requirement IDs appear in ≥1 task footer. Seams from design covered by unittest contracts.

## Design risks (implementer notes)

1. Packaging baseline: skill-local load is primary; if other skills’ root-template fallback is touched and material, stop and replan.  
2. Do not mark non-map rows First-class without full SDOC-1.7 evidence.  
3. Guidelines migration is out of scope (ROAD-11).
