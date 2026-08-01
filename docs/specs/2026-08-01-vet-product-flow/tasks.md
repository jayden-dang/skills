# Tasks: Vet product flow

> **For agentic workers:** pick the execute skill from `Execution-mode` and the
> run route — `build-in-waves` (continuous + subagents), `build-by-story`
> (story-unit + human review units), or `build-inline` (controller implements,
> no implementer subagents). Steps use checkbox (`- [ ]`) syntax for tracking.

Feature code: VPF
Status: Approved
Date: 2026-08-01
Execution-mode: continuous
Requirements: ./requirements.md
Design: ./design.md

**Goal:** Ship isolated `vet-product-flow` judgment (implementation-surface map +
report), wire author hand-off and dogfood hard gate, and separate guide-gap
re-vet from product-defect subagent fix during walkthrough.

**Architecture:** New model-invoked skill under `skills/acceptance/vet-product-flow/`
writes `.skills/<slug>-vet-product-flow.md` with code-grounded missing-situation
findings and an authored-cases fingerprint. `review-product-flow` hands off to
vet before dogfood; `run-product-walkthrough` refuses drive until fresh clean
report or named override. Guide-gap fixes patch the run file and re-vet;
product defects stay master re-test + subagent `root-cause`. Judgment is not an
ARCH-1 vertical check (ADR-0009).

**Tech Stack:** Markdown skills/docs; Python `unittest` + stdlib `hashlib`/`json`
for fingerprint; scenario markdown under `tests/vet-product-flow/`. No product
app runtime; no new consumer CLI for the product claim.

## Global Constraints

Copied from `docs/agents/project.md`, `docs/product/guidelines.md`, and
`docs/architecture/INDEX.md`.

**verify commands** — run in this order; all must pass before any completion claim:

| Check | Command |
|---|---|
| Typecheck | *(none)* |
| Lint | `python3 scripts/lint-skill-frontmatter.py && python3 scripts/lint-write-handoffs.py && python3 scripts/lint-context7.py` |
| Unit tests | `python3 -m unittest discover -s tests` |
| E2E / smoke | *(none)* |

Single test file: `python3 -m unittest tests.<module>`  
(e.g. `python3 -m unittest tests.test_vet_product_flow_fingerprint`)

**Test annotation conventions:**

| Layer | Requirement-ID convention |
|---|---|
| Unit (`unittest` under `tests/`) | ID in method name or first-line docstring greppable `CODE-N.M` |
| Scenario / acceptance markdown | Greppable bare `CODE-N.M` in `tests/vet-product-flow/scenarios*.md` |

**Coding standards / naming / house rules** (from `docs/product/guidelines.md`):

- Skill bodies: imperative voice; hard gates in dedicated blocks; rationalization tables in `| Thought | Reality |` form.
- SKILL.md under 500 lines (prefer under 300); split implementer/reviewer prompts into sibling files when needed.
- Python linters for this repo only: frontmatter parse safety, dead handoffs to user-invoked skills, Context7 references on library-reasoning skills.
- No production app code in this repository — content is skills, templates, hooks, and docs.
- Deterministic checks driven by an LLM (fixed `grep`/`git` under a precise skill) are a first-class form — do not replace them with freeform judgment when a set-difference will do.
- Skills: verb-first kebab-case; cross-skill `REQUIRED SUB-SKILL:` prose, never `@`-links.
- Skill `description` frontmatter states triggering conditions only — never summarize the workflow.
- Iron Law gates are not weakened by workflow band, ceremony tier, or convenience.

**Architecture invariants** — every task inherits (verbatim from `docs/architecture/INDEX.md`):

- **ARCH-1** Audit Trace and other vertical checks MUST be exact `grep`/`git`/file-read passes with fixed extraction rules and set differences — never an LLM judgment of whether a test "really" covers an ID.
- **ARCH-2** Optional project layers and config sections MUST no-op when absent: skills CONTINUES TO run without inventing vision, architecture invariants, team roster, or other standing facts that were never written.
- **ARCH-3** Consumer-repo adoption MUST require only the skills (plugin or npx) and markdown config — never mandate Python, vendored linters, CI jobs, or git-hook wiring for the full methodology; any hard headless gate is an optional documented add-on only.
- **ARCH-4** Requirement IDs (`CODE-N.M`) and architecture IDs (`ARCH-N`) are immutable once defined: never renumber or reuse; retire only by strikethrough; every task, test, commit trailer, and `Respects:` line MUST use the same greppable string as the definition.
- **ARCH-5** User-invoked skills may invoke model-invoked skills only; model-invoked skills must never invoke user-invoked skills; agents must never auto-invoke a skill marked `disable-model-invocation: true`.
- **ARCH-6** Skills MUST enforce and record only actions this skill set mediates; membership is never inferred from repository membership, roster, CODEOWNERS, branch ownership, PR authorship, or supplied artifacts.

**Team packaging:** Solo — lean multi-person language; full gates; no invented peer assignees.

**Forbidden in every task:**

- Selling schema/kind/req-id counts as “guide complete for real users” (ARCH-1 / ADR-0009).
- Writing a `review-product-flow` CLI `check` completeness command as the product claim.
- Mutating product app code or run-file cases from inside the vet judgment pass (report write only).
- Softening the dogfood gate by severity labels.
- Auto-invoking user-invoked skills.
- Colliding finding ids `VPF-N` with criterion ids `VPF-N.M` (findings are integer-only).
- Touching files outside the File Structure map.

## File Structure

**Create:**

| File | Responsibility |
|---|---|
| `skills/acceptance/vet-product-flow/SKILL.md` | Isolation map, non-claims, report write, guide-gap loop |
| `skills/acceptance/vet-product-flow/references/report-schema.md` | Report fields + fingerprint recipe + finding shape |
| `skills/acceptance/vet-product-flow/references/judgment-brief.md` | Subagent brief template |
| `docs/guide/skills/vet-product-flow.md` | Human-facing skill page |
| `tests/test_vet_product_flow_fingerprint.py` | Authored-cases fingerprint unit tests |
| `tests/test_vet_product_flow_contract.py` | Skill text + wiring contracts |
| `tests/vet-product-flow/fixtures/minimal-run.json` | Minimal v2 run file for fingerprint goldens |
| `tests/vet-product-flow/fixtures/minimal-run-ticked.json` | Same authored slots + different run/human/rev |
| `tests/vet-product-flow/fixtures/sample-report.md` | Golden report shape (fields present) — pass 1 |
| `tests/vet-product-flow/fixtures/sample-report-recheck.md` | Re-check report: same `surface_key` keeps `VPF-1`; new miss gets next id |
| `tests/vet-product-flow/scenarios.md` | Greppable ID layer — all VPF-N.M |
| `tests/vet-product-flow/scenarios-pressure.md` | Same-agent / false-confidence / mid-run plan pressure |
| `tests/trigger/vet-product-flow-routing.md` | Author vs vet vs walkthrough vs validate-ui |

**Modify:**

| File | Change |
|---|---|
| `skills/acceptance/review-product-flow/SKILL.md` | §5 hand-off orders vet before dogfood; rationalization if needed |
| `skills/acceptance/run-product-walkthrough/SKILL.md` | Precondition gate (fresh report); §4 product-defect subagent isolation |
| `tests/trigger/run-product-walkthrough-routing.md` | Add vet as peer disambiguator |
| `AGENTS.md` | acceptance inventory + skill count |
| `README.md` | acceptance roster |
| `docs/architecture/skills.md` | Inventory row for vet-product-flow |
| `docs/architecture/system.md` | acceptance/ list includes vet-product-flow |
| `docs/architecture/workflows.md` | acceptance chain: author → vet → walkthrough when relevant |
| `.claude-plugin/plugin.json` | Register skill if other acceptance skills are listed |
| `.claude-plugin/marketplace.json` | Same if applicable |
| `docs/agents/project.md` | audit-trace ignore for vet-product-flow fixtures/scenarios as needed |

No file outside these tables is touched by any task. ADR-0009 and CONTEXT glossary
terms already exist from design — do not re-litigate; only touch if a task finds
a greppable inconsistency (then fix in that task’s wiring steps).

---

### Task 1: Authored-cases fingerprint + report schema reference

**Files:**
- Create: `skills/acceptance/vet-product-flow/references/report-schema.md`
- Create: `tests/test_vet_product_flow_fingerprint.py`
- Create: `tests/vet-product-flow/fixtures/minimal-run.json`
- Create: `tests/vet-product-flow/fixtures/minimal-run-ticked.json`
- Create: `tests/vet-product-flow/fixtures/sample-report.md`
- Create: `tests/vet-product-flow/fixtures/sample-report-recheck.md`
- Create: `tests/vet-product-flow/scenarios.md` (skeleton: every `VPF-N.M` token once under story headings)
- Test: `tests/test_vet_product_flow_fingerprint.py`

**Reuse:** none — new code (rung 7); design §2 fingerprint recipe; v2 case keys from
`REQUIRED_CASE_KEYS` in `skills/acceptance/review-product-flow/scripts/review-product-flow`

**Interfaces:**
- Consumes: design fingerprint recipe (sorted keys, compact JSON, sha256 hex)
- Produces: `cases_fingerprint(run_dict) -> str` implemented in the test module
  (or a tiny pure function colocated with tests); report-schema.md field list;
  scenarios.md ID index

**Depends-on:** none

- [ ] **Step 1: Write the failing test**

Create fixtures:

`minimal-run.json` — `version: 2`, `rev: 0`, one section, one case with eight
authored slots filled, `run`/`human` defaults.

`minimal-run-ticked.json` — **identical authored slots**, but `rev: 9`, different
`run.verdict`/`saw`/`server`, `human.checked: true`. Fingerprint **must equal**
`minimal-run.json`.

In `tests/test_vet_product_flow_fingerprint.py`:

```python
"""VPF-1.3 VPF-1.4 VPF-8.1 — authored-cases fingerprint and report field contract."""

import hashlib
import json
import unittest
from pathlib import Path

FIX = Path(__file__).resolve().parent / "vet-product-flow" / "fixtures"

def cases_fingerprint(doc: dict) -> str:
    """Design recipe: sections → {name, cases[eight slots]}; sort_keys; compact; sha256."""
    # Implement per design.md §2 — tests fail until correct.
    ...

class TestCasesFingerprint(unittest.TestCase):
    def test_VPF_1_3_fingerprint_stable_when_only_run_human_rev_change(self):
        a = json.loads((FIX / "minimal-run.json").read_text())
        b = json.loads((FIX / "minimal-run-ticked.json").read_text())
        self.assertEqual(cases_fingerprint(a), cases_fingerprint(b))

    def test_VPF_1_3_fingerprint_changes_when_authored_slot_changes(self):
        a = json.loads((FIX / "minimal-run.json").read_text())
        a["sections"][0]["cases"][0]["title"] = "changed"
        base = json.loads((FIX / "minimal-run.json").read_text())
        self.assertNotEqual(cases_fingerprint(a), cases_fingerprint(base))

    def test_VPF_8_1_surface_key_reuses_id_across_two_fixture_reports(self):
        """VPF-8.1 — same surface_key keeps VPF-N on re-check; new key gets next id."""
        r1 = (FIX / "sample-report.md").read_text()
        r2 = (FIX / "sample-report-recheck.md").read_text()
        # Both reports document the same surface_key under the same ### VPF-1
        self.assertIn("surface_key:", r1)
        self.assertIn("### VPF-1", r1)
        self.assertIn("### VPF-1", r2)
        # Extract first surface_key value from each open VPF-1 block — must match
        import re
        sk1 = re.search(r"### VPF-1\n.*?surface_key:\s*`([^`]+)`", r1, re.S)
        sk2 = re.search(r"### VPF-1\n.*?surface_key:\s*`([^`]+)`", r2, re.S)
        self.assertIsNotNone(sk1)
        self.assertIsNotNone(sk2)
        self.assertEqual(sk1.group(1), sk2.group(1))
        # Recheck introduces a new finding id not in pass 1 (e.g. VPF-2)
        self.assertRegex(r2, r"### VPF-2\s")

    def test_VPF_1_4_finding_id_integer_namespace_not_criterion_shape(self):
        text = (FIX / "sample-report.md").read_text()
        # Finding headers use ### VPF-<int> without .M
        self.assertRegex(text, r"### VPF-\d+\s")
        self.assertNotRegex(text, r"### VPF-\d+\.\d+")
```

Implement `cases_fingerprint` to raise `NotImplementedError` first so tests fail
for the right reason, **or** leave it incomplete until Step 2 — prefer Step 1
RED: function missing / wrong hash.

Also assert `report-schema.md` exists and contains the strings
`cases_fingerprint`, `surface_key`, `pass_kind`, `prior_report` (add a small
test method `test_VPF_1_3_report_schema_documents_stamp_fields`).

Run: `python3 -m unittest tests.test_vet_product_flow_fingerprint` — expect fail.

- [ ] **Step 2: Implement**

Write `report-schema.md` with full field table + fingerprint recipe (verbatim
design §2, including sorted keys: `backend`, `expect`, `id`, `kind`, `req`,
`setup`, `title`, `try`). Write `sample-report.md` (pass_kind: initial, open
`VPF-1` with a `surface_key`) and `sample-report-recheck.md` (pass_kind:
re-check, same `surface_key` still under `VPF-1`, plus a new open miss as
`VPF-2`). Implement correct `cases_fingerprint`. Skeleton `scenarios.md` listing
every requirement id from requirements.md.

Run: same unittest — expect pass.

- [ ] **Step 3: Commit**

`git commit` with trailer `Implements: VPF-1.3, VPF-1.4, VPF-8.1`

_Requirements: VPF-1.3, VPF-1.4, VPF-8.1_

---

### Task 2: `vet-product-flow` skill body — isolation, map, non-claims, report

**Files:**
- Create: `skills/acceptance/vet-product-flow/SKILL.md`
- Create: `skills/acceptance/vet-product-flow/references/judgment-brief.md`
- Create: `tests/test_vet_product_flow_contract.py`
- Modify: `tests/vet-product-flow/scenarios.md`
- Create: `tests/vet-product-flow/scenarios-pressure.md`
- Test: `tests/test_vet_product_flow_contract.py`

**Reuse:** none — new code (rung 7); isolation pattern from `skills/review/inspect-change/SKILL.md`;
prove-against-code posture from `skills/review/vet-feedback/SKILL.md`

**Interfaces:**
- Consumes: report-schema.md field names from Task 1
- Produces: model-invoked skill that controllers invoke with a run-file path

**Depends-on:** Task 1

- [ ] **Step 1: Write the failing test**

In `tests/test_vet_product_flow_contract.py`, assert (by reading SKILL.md text):

| Assert | ID |
|---|---|
| Path exists; frontmatter `name: vet-product-flow`; **no** `disable-model-invocation` | VPF-1.1 |
| Description triggers judgment/isolation/before dogfood — **not** a step-by-step workflow summary | VPF-1.1 |
| Body requires fresh isolated pass: subagent **or** `AUTHORING CLOSED` inline fallback; forbids same-session §4 self-clear | VPF-1.2 |
| Report path `.skills/<slug>-vet-product-flow.md`; fields match schema | VPF-1.3 |
| Finding ids `VPF-N`; surface_key reuse | VPF-1.4, VPF-8.1 |
| Read-only: no product code / no run-file writes; report write allowed | VPF-1.5 |
| Implementation-surface map procedure; user-observable only | VPF-2.1, VPF-2.2 |
| Evidence required (file/symbol/route); no uninspected assert | VPF-2.3, VPF-2.4 |
| Severity Critical/Important/Minor orders fix only; does not soften gate | VPF-2.5 |
| Hygiene not product claim; no “complete for real users” | VPF-2.6 |
| Explicit non-claims: novelty/feel; chaos/load/race/fuzz; speculative design; global stamps; no drive/FE+BE ownership | VPF-3.1–3.5 |
| Rationalization table counters same-agent / CLI-false-confidence | VPF-1.2, VPF-2.6 |
| `judgment-brief.md` exists and lists run path, triad paths, report path, read-only rules | VPF-1.2 |

Run: `python3 -m unittest tests.test_vet_product_flow_contract` — expect fail (missing skill).

- [ ] **Step 2: Implement**

Write SKILL.md checklist covering design modules 1–2 product claim (not guide-gap
loop yet — Task 3). Include Iron Law block for isolation + grounding. Write
judgment-brief.md. Expand scenarios.md with behavioral bullets for stories 1–3.
Write scenarios-pressure.md: same-agent rubber stamp, mechanical completeness
false confidence, inventing chaos mid-vet.

Run: contract tests pass; lint frontmatter.

- [ ] **Step 3: Commit**

`Implements: VPF-1.1, VPF-1.2, VPF-1.5, VPF-2.1, VPF-2.2, VPF-2.3, VPF-2.4, VPF-2.5, VPF-2.6, VPF-3.1, VPF-3.2, VPF-3.3, VPF-3.4, VPF-3.5`

_Requirements: VPF-1.1, VPF-1.2, VPF-1.5, VPF-2.1, VPF-2.2, VPF-2.3, VPF-2.4, VPF-2.5, VPF-2.6, VPF-3.1, VPF-3.2, VPF-3.3, VPF-3.4, VPF-3.5_

---

### Task 3: Guide-gap fix / re-check loop in skill

**Files:**
- Modify: `skills/acceptance/vet-product-flow/SKILL.md` (fix-loop section)
- Modify: `tests/test_vet_product_flow_contract.py`
- Modify: `tests/vet-product-flow/scenarios.md`
- Test: `tests/test_vet_product_flow_contract.py`

**Reuse:** none — new code (rung 7); fixer-brief pattern from `build-in-waves` (prose only)

**Interfaces:**
- Consumes: report open findings + run-file path
- Produces: skill section “Guide-gap fix loop” with escalate rules and caps

**Depends-on:** Task 2

> Serial note: Tasks 3–5 all edit `tests/test_vet_product_flow_contract.py` and
> `scenarios.md`. Run **Task 3 → Task 4 → Task 5** in order (Depends-on edges
> below). Do not parallelize them.

- [ ] **Step 1: Write the failing test**

Assert skill body contains greppable protocol:

- Order by severity; patch **run file only** + re-render; no product patches — **VPF-6.2**
- After patches: re-invoke `vet-product-flow` fresh isolated; gate uses **new** report only — **VPF-6.3**
- Clear finding only when absent from new open list or named override; no self-declare — **VPF-6.4**
- Escalate to fixer subagent when open count ≥ 5 **or** multi-section (≥2 ability areas) rewrite; brief = findings + run path — **VPF-6.5**
- Cap **2** re-judgment cycles then stop for human — **VPF-6.6**
- Non-code-grounded / taste items do not keep the loop alive — **VPF-6.7**
- Skill must not write the run file during judgment (already VPF-1.5; reassert)

Run contract tests — expect fail until section written.

- [ ] **Step 2: Implement** guide-gap section + scenarios.

Run: pass.

- [ ] **Step 3: Commit**

`Implements: VPF-6.2, VPF-6.3, VPF-6.4, VPF-6.5, VPF-6.6, VPF-6.7`

_Requirements: VPF-6.2, VPF-6.3, VPF-6.4, VPF-6.5, VPF-6.6, VPF-6.7_

---

### Task 4: Author hand-off — `review-product-flow` §5

**Files:**
- Modify: `skills/acceptance/review-product-flow/SKILL.md` (§5 Hand over)
- Modify: `tests/test_vet_product_flow_contract.py` (neighbor asserts)
- Modify: `tests/vet-product-flow/scenarios.md`
- Test: `tests/test_vet_product_flow_contract.py`

**Reuse:** existing — extends `review-product-flow` hand-over (rung 2)

**Interfaces:**
- Consumes: skill name `vet-product-flow` from Task 2
- Produces: ordered hand-off: artifacts → vet → optional serve → walkthrough only after vet

**Depends-on:** Task 3

- [ ] **Step 1: Write the failing test**

Assert `review-product-flow/SKILL.md`:

- §5 (or Hand over) names `vet-product-flow` as **required next** before agent dogfood — **VPF-4.1**
- §1 coverage gate / seven-kind taxonomy still present (guard) — **VPF-4.2**
- Run file SSOT + `render` shell path still present (guard) — **VPF-4.3**
- Does **not** remove coverage self-check; rationalization: self-check ≠ vet

Run — expect fail until §5 edited.

- [ ] **Step 2: Implement** ordered hand-off per design module 3. Keep serve and human paths.

Run: pass. Lint if skill frontmatter touched (description may mention dogfood is gated by vet — keep triggers for **authoring**, not walkthrough).

- [ ] **Step 3: Commit**

`Implements: VPF-4.1, VPF-4.2, VPF-4.3`

_Requirements: VPF-4.1, VPF-4.2, VPF-4.3_

---

### Task 5: Hard gate before `run-product-walkthrough` drive

**Files:**
- Modify: `skills/acceptance/run-product-walkthrough/SKILL.md` (new precondition block before product drive)
- Modify: `tests/test_vet_product_flow_contract.py`
- Modify: `tests/vet-product-flow/scenarios.md`
- Modify: `tests/vet-product-flow/scenarios-pressure.md`
- Test: `tests/test_vet_product_flow_contract.py`

**Reuse:** existing — extends walkthrough preconditions; origin consent pattern (rung 2)

**Interfaces:**
- Consumes: report path + fingerprint recipe (Task 1); skill name (Task 2)
- Produces: gate algorithm before any product click / drive loop

**Depends-on:** Task 1, Task 4

- [ ] **Step 1: Write the failing test**

Assert `run-product-walkthrough/SKILL.md` contains:

- Require fresh `.skills/<slug>-vet-product-flow.md` for the run file before drive — **VPF-5.1**
- Freshness = `run_file` match + `cases_fingerprint` match (not whole-file `rev`) — **VPF-5.1**
- Open findings block drive unless user yes **names each** open `VPF-N` — **VPF-5.2**, **VPF-5.3**
- Every open finding blocking; severity does not soften gate — **VPF-5.4**, **VPF-6.1**
- Origin consent gate still present — **VPF-5.5**
- Iron Law / `mark` saw+server / presentational rules still present — **VPF-5.6**
- Override trail: greppable note in `.skills/progress.md` (or documented equivalent) — **VPF-5.3**
- `init` may seed pending, but no product click until gate passes

Pressure scenario: “just go / demo in 5 minutes” without naming findings → must stop.

Run — expect fail until gate section written.

- [ ] **Step 2: Implement** gate section (design module 4 algorithm). Cross-link guide-gap loop on stop.

Run: pass.

- [ ] **Step 3: Commit**

`Implements: VPF-5.1, VPF-5.2, VPF-5.3, VPF-5.4, VPF-5.5, VPF-5.6, VPF-6.1`

_Requirements: VPF-5.1, VPF-5.2, VPF-5.3, VPF-5.4, VPF-5.5, VPF-5.6, VPF-6.1_

---

### Task 6: Product-defect isolation during dogfood

**Files:**
- Modify: `skills/acceptance/run-product-walkthrough/SKILL.md` (§4 Failure routing)
- Modify: `tests/test_vet_product_flow_contract.py`
- Modify: `tests/vet-product-flow/scenarios.md`
- Test: `tests/test_vet_product_flow_contract.py`

**Reuse:** existing — extends walkthrough §4; `root-cause` + `test-first` (rung 2)

**Interfaces:**
- Consumes: existing re-drive rules after product fix
- Produces: master owns mark/re-test; subagent owns isolated root-cause/fix

**Depends-on:** Task 5

- [ ] **Step 1: Write the failing test**

Assert failure-routing prose:

- Master owns case selection, evidence, mark, re-test — **VPF-7.1**
- Subagent brief: repro, saw/server, case id, req — not full session history — **VPF-7.2**
- On DONE: master re-drives failed case + already-pass cases whose `req` the fix touched — **VPF-7.3**
- Subagent still uses `root-cause` (+ test-first); isolation ≠ free patch — **VPF-7.4**
- Guide-gap loop separate from product-defect loop (explicit sentence) — **VPF-7.5**

Run — expect fail until §4 rewritten.

- [ ] **Step 2: Implement** §4 table/rows per design module 6. Preserve flaky/guide-wrong and precondition-stop rows.

Run: pass.

- [ ] **Step 3: Commit**

`Implements: VPF-7.1, VPF-7.2, VPF-7.3, VPF-7.4, VPF-7.5`

_Requirements: VPF-7.1, VPF-7.2, VPF-7.3, VPF-7.4, VPF-7.5_

---

### Task 7: Inventory, human guide, trigger routing

**Files:**
- Create: `docs/guide/skills/vet-product-flow.md`
- Create: `tests/trigger/vet-product-flow-routing.md`
- Modify: `tests/trigger/run-product-walkthrough-routing.md`
- Modify: `AGENTS.md`
- Modify: `README.md`
- Modify: `docs/architecture/skills.md`
- Modify: `docs/architecture/system.md`
- Modify: `docs/architecture/workflows.md` (author → vet → walkthrough when dogfooding)
- Modify: `.claude-plugin/plugin.json` (and `marketplace.json` if skills are enumerated there)
- Modify: `docs/agents/project.md` — add audit-trace ignore globs for
  `tests/vet-product-flow/fixtures/`, `tests/vet-product-flow/scenarios*.md`,
  `tests/trigger/vet-product-flow-routing.md` as appropriate (fixture IDs must not
  create false E2)
- Modify: `tests/test_vet_product_flow_contract.py` (wiring asserts)
- Test: `tests/test_vet_product_flow_contract.py`

**Reuse:** existing — registration pattern from `run-product-walkthrough` / pathfind wiring tests (rung 2)

**Interfaces:**
- Produces: discoverable skill name in inventories; routing matrix includes vet

**Depends-on:** Task 2, Task 4, Task 5, Task 6

- [ ] **Step 1: Write the failing test**

Assert greppable registration:

- `AGENTS.md` acceptance row lists `vet-product-flow` (model-invoked)
- `docs/architecture/skills.md` has an inventory entry
- `docs/architecture/system.md` acceptance/ path list includes it
- Plugin manifest includes the skill path if other acceptance skills are listed
- `tests/trigger/vet-product-flow-routing.md` exists with should-fire for vet
  (finished guide, check missing situations / before dogfood) and should-not
  (author guide → review-product-flow; drive cases → run-product-walkthrough;
  Playwright → validate-ui)
- Triple routing file mentions `vet-product-flow` as disambiguator

Run — expect fail until wired.

- [ ] **Step 2: Implement** all inventory + guide + triggers. Keep skill counts accurate in AGENTS.md.

Run: wiring asserts pass; `python3 scripts/lint-skill-frontmatter.py` pass.

- [ ] **Step 3: Commit**

`Implements: VPF-1.1` (discoverability; packaging)

_Requirements: VPF-1.1_

---

### Task 8: Full verify + scenario completeness close

**Files:**
- Modify: `tests/vet-product-flow/scenarios.md` (confirm every VPF-N.M appears)
- Modify: any skill rationalization gaps found under pressure
- Test: full suite + lints

**Reuse:** n/a

**Interfaces:** none

**Depends-on:** Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7

- [ ] **Step 1: Write the failing test**

Add a contract test method `test_VPF_all_requirement_ids_appear_in_scenarios` that
loads `docs/specs/2026-08-01-vet-product-flow/requirements.md`, extracts every
`VPF-N.M` bold ID, and asserts each appears in `tests/vet-product-flow/scenarios.md`.

Run — fail if any ID missing from scenarios.

- [ ] **Step 2: Implement**

Fill any missing scenario tokens; fix rationalization gaps; run:

```bash
python3 scripts/lint-skill-frontmatter.py && python3 scripts/lint-write-handoffs.py && python3 scripts/lint-context7.py
python3 -m unittest discover -s tests
```

Expect: all pass, pristine.

- [ ] **Step 3: Commit**

`Implements: VPF-1.1` (suite close) — trailers may list residual IDs only covered in scenarios

_Requirements: VPF-1.1, VPF-1.2, VPF-1.3, VPF-1.4, VPF-1.5, VPF-2.1, VPF-2.2, VPF-2.3, VPF-2.4, VPF-2.5, VPF-2.6, VPF-3.1, VPF-3.2, VPF-3.3, VPF-3.4, VPF-3.5, VPF-4.1, VPF-4.2, VPF-4.3, VPF-5.1, VPF-5.2, VPF-5.3, VPF-5.4, VPF-5.5, VPF-5.6, VPF-6.1, VPF-6.2, VPF-6.3, VPF-6.4, VPF-6.5, VPF-6.6, VPF-6.7, VPF-7.1, VPF-7.2, VPF-7.3, VPF-7.4, VPF-7.5, VPF-8.1_

---

## Coverage map (audit)

Every Approved VPF ID must appear in ≥1 task footer **and** in a tagged test
(unittest docstring/method and/or `tests/vet-product-flow/scenarios.md`).

| IDs | Primary task | Test annotation |
|---|---|---|
| VPF-1.3, 1.4, 8.1 | Task 1 | fingerprint unit methods + sample report |
| VPF-1.1, 1.2, 1.5, 2.1–2.6, 3.1–3.5 | Task 2 | contract + scenarios |
| VPF-6.2–6.7 | Task 3 | contract + scenarios |
| VPF-4.1–4.3 | Task 4 | contract + scenarios |
| VPF-5.1–5.6, 6.1 | Task 5 | contract + scenarios + pressure |
| VPF-7.1–7.5 | Task 6 | contract + scenarios |
| VPF-1.1 (wiring) | Task 7 | wiring asserts + trigger file |
| All IDs (close) | Task 8 | scenarios completeness assert + full suite |

Seam table from design: fingerprint unit, contract, scenarios, trigger routing — all mapped.

## Exit

Present this file and **STOP**.

Before `Status: Approved`:

1. User chooses `Execution-mode: continuous` or `story-unit`
2. User approves this written plan
3. Then set Status Approved and offer execute routes:
   - **`build-in-waves`** (continuous + subagents; prefer `isolate-workspace`)
   - **`build-by-story`** (story-unit; prefer `isolate-workspace`)
   - **`build-inline`** (either mode; controller implements; no implementer subagents)

**Do not** set Approved while Execution-mode is `unset`.
