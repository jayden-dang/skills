# Tasks: Skills ephemera namespace

> **For agentic workers:** after plan approval, pick one execute skill —
> `build-in-waves` (subagent waves), `build-by-story` (human-gated story review
> units), or `build-inline` (controller implements, no implementer subagents).
> The chosen skill writes `Execution-mode:`. Steps use checkbox (`- [ ]`) syntax
> for tracking.

Feature code: SKNS
Status: Implemented
Date: 2026-08-01
Execution-mode: continuous
Requirements: ./requirements.md
Design: ./design.md

**Goal:** Relocate feature-scoped `.skills/` ephemera under `.skills/<CODE>/` with
shared roots preserved, pending/adhoc rules, and skill-set contract + docs
updated — no consumer auto-migrate, no runtime path library.

**Architecture:** Path grammar SSOT in `templates/skills-ephemera-paths.md`.
Every skill that wrote flat feature paths is rewritten to CODE (or
`_pending-` / `_adhoc`). Verification is source-contract + scenario unittest in
`tests/skills-namespace/` only (ARCH-3).

**Tech Stack:** Markdown skills/docs/templates; Python 3 `unittest` for
contract tests; scenario markdown. No consumer Python dependency.

## Global Constraints

Copied from `docs/agents/project.md`, `docs/product/guidelines.md`, and
`docs/architecture/INDEX.md`.

**verify commands** — run in this order; all must pass before any completion claim:

| Check | Command |
|---|---|
| Typecheck | *(none)* |
| Lint | `python3 scripts/lint-skill-frontmatter.py && python3 scripts/lint-handoffs.py && python3 scripts/lint-context7.py` |
| Unit tests | `python3 -m unittest discover -s tests` |
| E2E / smoke | *(none)* |

Single test file: `python3 -m unittest tests.<module>`  
(e.g. `python3 -m unittest tests.test_skills_namespace_contract`)

**Test annotation conventions:**

| Layer | Requirement-ID convention |
|---|---|
| Unit (`unittest` under `tests/`) | ID in method name or first-line docstring greppable `SKNS-N.M` |
| Scenario / acceptance markdown | Greppable bare `SKNS-N.M` in `tests/skills-namespace/scenarios*.md` |

**Coding standards / house rules:**

- Skill bodies: imperative voice; hard gates in dedicated blocks; rationalization tables in `| Thought | Reality |` form.
- SKILL.md under 500 lines (prefer under 300); split into `references/` when needed.
- **No** `*.py` under `skills/` for this feature — tests only under `tests/`.
- Skills: verb-first kebab-case; cross-skill `REQUIRED SUB-SKILL:` prose, never `@`-links.
- Skill `description` frontmatter states triggering conditions only.
- Iron Law gates are not weakened by convenience path shortcuts.

**Architecture invariants** (verbatim):

- **ARCH-1** Audit Trace and other vertical checks MUST be exact `grep`/`git`/file-read passes with fixed extraction rules and set differences — never an LLM judgment of whether a test "really" covers an ID.
- **ARCH-2** Optional project layers and config sections MUST no-op when absent: skills CONTINUES TO run without inventing vision, architecture invariants, team roster, or other standing facts that were never written.
- **ARCH-3** Consumer-repo adoption MUST require only the skills (plugin or npx) and markdown config — never mandate Python, vendored linters, CI jobs, or git-hook wiring for the full methodology; any hard headless gate is an optional documented add-on only.
- **ARCH-4** Requirement IDs (`CODE-N.M`) and architecture IDs (`ARCH-N`) are immutable once defined: never renumber or reuse; retire only by strikethrough; every task, test, commit trailer, and `Respects:` line MUST use the same greppable string as the definition.
- **ARCH-5** User-invoked skills may invoke model-invoked skills only; model-invoked skills must never invoke user-invoked skills; agents must never auto-invoke a skill marked `disable-model-invocation: true`.
- **ARCH-6** Skills MUST enforce and record only actions this skill set mediates; membership is never inferred from repository membership, roster, CODEOWNERS, branch ownership, PR authorship, or supplied artifacts.

**Team packaging:** Solo.

**Design constants:**

- Feature root: `.skills/<CODE>/` (CODE only — no long slug in path segment)
- Pending: `.skills/_pending-<slug>/`
- Adhoc: `.skills/_adhoc/<short-slug>/`
- Shared: `.skills/pathfind/`, `.skills/research/`, `.skills/decisions/`, `.skills/pr-packages/`
- CODE resolve: plan/brief context → `Feature code:` → INDEX
- Legacy: read once allowed; write only under CODE; no auto-migrate

**Forbidden in every task:**

- Creating `skills/**/*.py`
- Auto-migrating consumer `.skills/` trees
- Moving pathfind / research / decisions / pr-packages under `<CODE>/`
- Weakening gitignore requirement for `.skills/`
- Changing audit-trace E-codes or load-subgraph edge semantics
- Touching files outside the File Structure map

## File Structure

**Create:**

| File | Responsibility |
|---|---|
| `templates/skills-ephemera-paths.md` | Path grammar SSOT (CODE / pending / adhoc / shared / basenames / resolve / legacy) |
| `tests/test_skills_namespace_contract.py` | Source-contract unittest suite |
| `tests/skills-namespace/scenarios.md` | Greppable SKNS-N.M scenarios |
| `tests/skills-namespace/scenarios-pressure.md` | Dual-CODE, legacy write, root-dump pressure |

**Modify (by task clusters):**

| Cluster | Files |
|---|---|
| Execute | `skills/execution/build-in-waves/SKILL.md`, `implementer-prompt.md`, `task-reviewer-prompt.md`, `TESTS.md`; `build-by-story/SKILL.md`, `story-unit-mode.md` if it cites paths; `build-inline/SKILL.md` |
| Discovery/spec | `skills/discovery/frame-change/SKILL.md`; `skills/spec/specify-behavior/SKILL.md`, `design-solution/SKILL.md`, `plan-tasks/SKILL.md`; `skills/discovery/clarify-decisions/SKILL.md` (knowns path load only if hard-coded) |
| Acceptance | `skills/acceptance/validate-feature/SKILL.md`; `review-product-flow/SKILL.md`, `references/cases-schema.md`; `vet-product-flow/SKILL.md`, `references/judgment-brief.md`, `references/report-schema.md`; `run-product-walkthrough/SKILL.md` |
| Ship/track | `skills/ship/package-change/SKILL.md`; `land-branch/SKILL.md`; `skills/review/brief-team/SKILL.md`; `skills/track/write-handoff/SKILL.md`, `reroute-plan/SKILL.md`, `refresh-roadmap-status/SKILL.md` |
| Project scan | `skills/project/define-project/SKILL.md`, `brownfield-scan.md` (if `.skills/<slug>-scan` hard-coded) |
| Docs | `AGENTS.md`; `docs/guide/concepts/artifacts.md`; `docs/guide/process/execution.md`; `docs/guide/examples/tier-2-feature.md`; `docs/guide/resources/troubleshooting.md`; `docs/architecture/artifacts.md`; guide skill pages for build-in-waves / build-by-story / build-inline / frame-change as needed |
| Config | `docs/agents/project.md` — Audit Trace ignore for `tests/skills-namespace/` |

No file outside these tables.

---

### Task 1: Path grammar SSOT + contract harness

**Files:**
- Create: `templates/skills-ephemera-paths.md`
- Create: `tests/test_skills_namespace_contract.py`
- Create: `tests/skills-namespace/scenarios.md`
- Create: `tests/skills-namespace/scenarios-pressure.md`
- Modify: `docs/agents/project.md` (audit-trace ignore for skills-namespace tests)
- Test: `tests/test_skills_namespace_contract.py`

**Reuse:** rung 2 — FSUB/PCHG source-contract pattern under `tests/`

**Interfaces:**
- Consumes: design grammar table
- Produces: SSOT template; contract test module; scenario skeletons with every SKNS-N.M token once

**Depends-on:** none

- [ ] **Step 1: Write the failing test**

```python
"""SKNS-1.1 SKNS-1.2 SKNS-1.3 SKNS-2.1 SKNS-2.2 SKNS-2.3 SKNS-2.4
SKNS-3.1 SKNS-3.3 SKNS-4.1 SKNS-4.2 SKNS-4.3 — path grammar SSOT + harness.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SSOT = ROOT / "templates" / "skills-ephemera-paths.md"
SCEN = ROOT / "tests" / "skills-namespace" / "scenarios.md"
REQ = ROOT / "docs" / "specs" / "2026-08-01-skills-namespace" / "requirements.md"


class TestSkillsEphemeraSsot(unittest.TestCase):
    def test_SKNS_1_1_1_2_ssot_exists_with_code_root(self):
        self.assertTrue(SSOT.is_file())
        text = SSOT.read_text()
        self.assertIn(".skills/<CODE>/", text)
        self.assertRegex(text, r"Feature code only|CODE alone|no long", re.I)

    def test_SKNS_2_shared_roots_documented(self):
        text = SSOT.read_text()
        for token in ("pathfind", "research", "decisions", "pr-packages"):
            self.assertIn(token, text)

    def test_SKNS_3_1_3_3_pending_and_adhoc(self):
        text = SSOT.read_text()
        self.assertIn("_pending-", text)
        self.assertIn("_adhoc/", text)

    def test_SKNS_1_3_resolve_order(self):
        text = SSOT.read_text()
        self.assertRegex(text, r"resolve|resolution order|Feature code", re.I)

    def test_SKNS_4_1_4_2_legacy_read_write_rule(self):
        text = SSOT.read_text()
        self.assertRegex(text, r"legacy", re.I)
        self.assertRegex(text, r"read", re.I)
        self.assertRegex(text, r"write", re.I)

    def test_SKNS_4_3_no_auto_migrate_in_ssot(self):
        text = SSOT.read_text()
        self.assertRegex(text, r"auto-migrate|MUST NOT.*migrat|no auto", re.I)

    def test_SKNS_all_requirement_ids_in_scenarios(self):
        ids = set(re.findall(r"\*\*(SKNS-\d+\.\d+)\*\*", REQ.read_text()))
        scen = SCEN.read_text() if SCEN.is_file() else ""
        missing = sorted(i for i in ids if i not in scen)
        self.assertEqual(missing, [], f"missing from scenarios: {missing}")
```

Skeleton `scenarios.md` listing every bold `SKNS-N.M` from requirements once.
Pressure file: dual-CODE ledgers; “write progress at root for speed”; “auto-migrate mailgate”.

Run: `python3 -m unittest tests.test_skills_namespace_contract` — expect fail (missing SSOT / incomplete).

- [ ] **Step 2: Implement**

Write full `templates/skills-ephemera-paths.md` per design §1 (tables + resolve + legacy + basenames + shared). Fill scenarios. Add project.md ignore paths for `tests/skills-namespace/`.

Run: contract tests pass.

- [ ] **Step 3: Commit**

`Implements: SKNS-1.1, SKNS-1.2, SKNS-1.3, SKNS-2.1, SKNS-2.2, SKNS-2.3, SKNS-2.4, SKNS-3.1, SKNS-3.3, SKNS-4.1, SKNS-4.2, SKNS-4.3`

_Requirements: SKNS-1.1, SKNS-1.2, SKNS-1.3, SKNS-2.1, SKNS-2.2, SKNS-2.3, SKNS-2.4, SKNS-3.1, SKNS-3.3, SKNS-4.1, SKNS-4.2, SKNS-4.3_

---

### Task 2: Execute family paths

**Files:**
- Modify: `skills/execution/build-in-waves/SKILL.md`
- Modify: `skills/execution/build-in-waves/implementer-prompt.md`
- Modify: `skills/execution/build-in-waves/task-reviewer-prompt.md`
- Modify: `skills/execution/build-in-waves/TESTS.md`
- Modify: `skills/execution/build-by-story/SKILL.md`
- Modify: `skills/execution/build-by-story/story-unit-mode.md` (if path strings present)
- Modify: `skills/execution/build-inline/SKILL.md`
- Modify: `tests/test_skills_namespace_contract.py`
- Modify: `tests/skills-namespace/scenarios.md`
- Modify: `tests/skills-namespace/scenarios-pressure.md`
- Test: `tests/test_skills_namespace_contract.py`

**Reuse:** rung 2 — extend execute family; SSOT from Task 1

**Interfaces:**
- Consumes: `.skills/<CODE>/…` grammar; `FEATURE_CODE` in briefs
- Produces: progress/brief/report/review/notes under CODE only

**Depends-on:** Task 1

- [ ] **Step 1: Write the failing test**

Assert each of build-in-waves, build-by-story, build-inline SKILL.md (and implementer-prompt):

| Assert | ID |
|---|---|
| Prescribes `.skills/<CODE>/progress.md` (or equivalent CODE token) as ledger | SKNS-1.4, SKNS-5.1, SKNS-6.2 |
| task brief/report under CODE | SKNS-5.1 |
| review diff under CODE | SKNS-5.1 |
| implementation-notes under CODE | SKNS-5.1 |
| Does **not** prescribe bare `.skills/progress.md` as the sole write target (legacy read ok if labeled) | SKNS-4.2, SKNS-1.4 |
| Dual-feature isolation language or two-CODE pressure scenario | SKNS-7.1 |

Helper: for each path, skill text contains `.skills/<CODE>/` or `` `.skills/<CODE>/progress.md` ``.

Run: fail until rewrites.

- [ ] **Step 2: Implement** path rewrites; point skills at `templates/skills-ephemera-paths.md` via prose; inject CODE into brief assembly steps; update TESTS.md strings.

Run: pass.

- [ ] **Step 3: Commit**

`Implements: SKNS-1.4, SKNS-5.1, SKNS-6.2, SKNS-7.1`

_Requirements: SKNS-1.4, SKNS-5.1, SKNS-6.2, SKNS-7.1_

---

### Task 3: Discovery / spec paths + pending promote

**Files:**
- Modify: `skills/discovery/frame-change/SKILL.md`
- Modify: `skills/discovery/clarify-decisions/SKILL.md` (if hard-coded knowns/scan paths)
- Modify: `skills/spec/specify-behavior/SKILL.md`
- Modify: `skills/spec/design-solution/SKILL.md`
- Modify: `skills/spec/plan-tasks/SKILL.md`
- Modify: `skills/project/define-project/SKILL.md` and `brownfield-scan.md` if they hard-code `.skills/<slug>-scan.md`
- Modify: `tests/test_skills_namespace_contract.py`
- Modify: `tests/skills-namespace/scenarios.md`
- Test: `tests/test_skills_namespace_contract.py`

**Reuse:** rung 2 — design §3

**Interfaces:**
- Consumes: pending + CODE roots
- Produces: promote step on Feature code registration (SKNS-3.2)

**Depends-on:** Task 1

- [ ] **Step 1: Write the failing test**

| Assert | ID |
|---|---|
| frame-change / design-solution / plan-tasks / specify-behavior use CODE or `_pending-` for scan/knowns/reviews — not bare root slug-only as preferred write | SKNS-5.2, SKNS-3.1 |
| specify-behavior has promote/move step after INDEX registration | SKNS-3.2 |
| pathfind still under `.skills/pathfind/` | SKNS-2.1, SKNS-6.1 |

Run: fail until edits.

- [ ] **Step 2: Implement** fixed basenames under CODE/pending; promote step; leave pathfind shared.

Run: pass.

- [ ] **Step 3: Commit**

`Implements: SKNS-3.1, SKNS-3.2, SKNS-5.2, SKNS-2.1, SKNS-6.1`

_Requirements: SKNS-3.1, SKNS-3.2, SKNS-5.2, SKNS-2.1, SKNS-6.1_

---

### Task 4: Acceptance / product-flow paths

**Files:**
- Modify: `skills/acceptance/validate-feature/SKILL.md`
- Modify: `skills/acceptance/review-product-flow/SKILL.md`
- Modify: `skills/acceptance/review-product-flow/references/cases-schema.md`
- Modify: `skills/acceptance/vet-product-flow/SKILL.md`
- Modify: `skills/acceptance/vet-product-flow/references/judgment-brief.md`
- Modify: `skills/acceptance/vet-product-flow/references/report-schema.md`
- Modify: `skills/acceptance/run-product-walkthrough/SKILL.md`
- Modify: `tests/test_skills_namespace_contract.py`
- Modify: `tests/skills-namespace/scenarios.md`
- Test: `tests/test_skills_namespace_contract.py`

**Reuse:** rung 2 — design §4

**Interfaces:**
- Consumes: CODE root
- Produces: acceptance + product-flow artifacts under `.skills/<CODE>/`

**Depends-on:** Task 1

- [ ] **Step 1: Write the failing test**

Assert acceptance skills prescribe `.skills/<CODE>/` for acceptance and product-flow artifacts; walkthrough overrides append to `.skills/<CODE>/progress.md` not bare root progress; SKNS-5.3.

Run: fail until edits.

- [ ] **Step 2: Implement** path rewrites + schema examples.

Run: pass. Note: existing DFSYNC/VPF contract tests may hardcode old paths — **if they fail**, update those tests' expected path strings in the same task only when they assert artifact paths (File Structure allows only listed files — **exception**: if `tests/test_walk_product_guide_contract.py` or VPF contracts assert exact `.skills/<slug>-…` strings, add those test files to this task's Modify list when RED shows them).

If suite fails on other modules expecting old paths, modify **only** those failing test expectation strings (list each file in the commit message Files). Prefer updating expectations to CODE form, not weakening SKNS.

- [ ] **Step 3: Commit**

`Implements: SKNS-5.3`

_Requirements: SKNS-5.3_

---

### Task 5: Ship / track paths

**Files:**
- Modify: `skills/ship/package-change/SKILL.md`
- Modify: `skills/ship/land-branch/SKILL.md`
- Modify: `skills/review/brief-team/SKILL.md`
- Modify: `skills/track/write-handoff/SKILL.md`
- Modify: `skills/track/reroute-plan/SKILL.md`
- Modify: `skills/track/refresh-roadmap-status/SKILL.md`
- Modify: `tests/test_skills_namespace_contract.py`
- Modify: `tests/skills-namespace/scenarios.md`
- Test: `tests/test_skills_namespace_contract.py`

**Reuse:** rung 2 — design §5

**Interfaces:**
- Consumes: CODE notes/progress/corrections; shared pr-packages/decisions
- Produces: path updates; optional Feature-code in package prose

**Depends-on:** Task 1

- [ ] **Step 1: Write the failing test**

| Assert | ID |
|---|---|
| implementation-notes under CODE | SKNS-5.1 |
| corrections under CODE (reroute-plan) | SKNS-5.1 |
| refresh-roadmap-status does not require only bare `.skills/progress.md` | SKNS-5.1 |
| pr-packages and decisions still shared | SKNS-2.3, SKNS-2.4, SKNS-6.1 |

Run: fail until edits.

- [ ] **Step 2: Implement** rewrites; optional manifest Feature-code mention.

Run: pass.

- [ ] **Step 3: Commit**

`Implements: SKNS-5.1, SKNS-2.3, SKNS-2.4, SKNS-6.1`

_Requirements: SKNS-5.1, SKNS-2.3, SKNS-2.4, SKNS-6.1_

---

### Task 6: AGENTS + guide + architecture + suite close

**Files:**
- Modify: `AGENTS.md`
- Modify: `docs/guide/concepts/artifacts.md`
- Modify: `docs/guide/process/execution.md`
- Modify: `docs/guide/examples/tier-2-feature.md`
- Modify: `docs/guide/resources/troubleshooting.md`
- Modify: `docs/architecture/artifacts.md`
- Modify: `docs/guide/skills/build-in-waves.md` (if path examples)
- Modify: `docs/guide/skills/build-by-story.md`
- Modify: `docs/guide/skills/build-inline.md`
- Modify: `docs/guide/skills/frame-change.md` (if scan path examples)
- Modify: `tests/test_skills_namespace_contract.py`
- Modify: `tests/skills-namespace/scenarios.md`
- Modify: `tests/skills-namespace/scenarios-pressure.md`
- Test: full suite

**Reuse:** rung 2 — design §6

**Interfaces:**
- Produces: human + agent constitution describing per-CODE layout

**Depends-on:** Task 2, Task 3, Task 4, Task 5

- [ ] **Step 1: Write the failing test**

```python
def test_SKNS_5_4_agents_and_artifacts_describe_per_code(self):
    agents = (ROOT / "AGENTS.md").read_text()
    arts = (ROOT / "docs" / "guide" / "concepts" / "artifacts.md").read_text()
    self.assertIn(".skills/<CODE>/", agents + arts or ".skills/<CODE>" in agents)
    # stronger:
    self.assertTrue(".skills/<CODE>" in agents or "`.skills/<CODE>/" in agents)
    self.assertIn("progress.md", agents)
    arch = (ROOT / "docs" / "architecture" / "artifacts.md").read_text()
    self.assertRegex(agents + arts + arch, r"pathfind|shared", re.I)

def test_SKNS_6_3_gitignore_still_required_language(self):
    # package-change or AGENTS still say .skills is git-ignored
    pchg = (ROOT / "skills" / "ship" / "package-change" / "SKILL.md").read_text()
    self.assertRegex(pchg, r"git-ignor", re.I)

def test_SKNS_6_4_no_new_audit_trace_e_codes_for_layout(self):
    # skills-namespace must not add E6+ layout codes to audit-trace skill
    at = (ROOT / "skills" / "execution" / "audit-trace" / "SKILL.md").read_text()
    # no requirement that audit-trace changes — assert SKNS docs don't invent E6
    scen = (ROOT / "tests" / "skills-namespace" / "scenarios.md").read_text()
    self.assertNotRegex(scen, r"new E-code|E6 layout")
```

Also assert every SKNS ID still in scenarios; pressure covers dual-CODE + no root write + no auto-migrate.

Run: fail until docs updated.

- [ ] **Step 2: Implement** docs; run full verify:

```bash
python3 scripts/lint-skill-frontmatter.py && python3 scripts/lint-handoffs.py && python3 scripts/lint-context7.py
python3 -m unittest discover -s tests
```

Expect: green, pristine. Fix any remaining forbidden bare-path prescriptions discovered by contract greps.

- [ ] **Step 3: Commit**

`Implements: SKNS-5.4, SKNS-6.3, SKNS-6.4`

_Requirements: SKNS-5.4, SKNS-6.3, SKNS-6.4_

---

## Coverage map (audit)

| IDs | Primary task | Test annotation |
|---|---|---|
| 1.1–1.3, 2.1–2.4, 3.1, 3.3, 4.1–4.3 | Task 1 | contract + scenarios |
| 1.4, 5.1 (execute), 6.2, 7.1 | Task 2 | contract + pressure |
| 3.1–3.2, 5.2, 2.1, 6.1 | Task 3 | contract + scenarios |
| 5.3 | Task 4 | contract + scenarios |
| 5.1 (ship/track), 2.3–2.4, 6.1 | Task 5 | contract |
| 5.4, 6.3, 6.4 | Task 6 | contract + full suite |

All Approved SKNS IDs appear in ≥1 footer and in scenarios/unittest names.

## Exit

Present this file and **STOP**.

On user approval of this written plan:

1. Set `Status: Approved` (leave `Execution-mode: unset`).
2. Offer exactly three execute routes:

| Route | Meaning |
|---|---|
| **`build-in-waves`** | Subagent waves (`Execution-mode: continuous`). Prefer `isolate-workspace` first. |
| **`build-by-story`** | Human-gated story units (`Execution-mode: story-unit`). Prefer `isolate-workspace` first. |
| **`build-inline`** | Controller implements with `test-first` (no implementer subagents). |

3. On pick: hand off to that skill.
