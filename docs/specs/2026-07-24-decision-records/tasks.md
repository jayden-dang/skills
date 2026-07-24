# Tasks: Boundary Decision Records

> **For agentic workers:** REQUIRED SUB-SKILL: use `execute-plan` to implement
> this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

Feature code: DREC
Status: Approved
Date: 2026-07-24
Requirements: ./requirements.md
Design: ./design.md

**Goal:** Ship a production-boundary decision-record substrate — immutable payload + append-only envelope files under `docs/decisions/`, a model-invoked `record-decision` skill, a POSIX validator, and integrations into finish-branch, release, trace, interpret, and the participant-model surfaces — so terminal human verdicts leave durable, LLM-free-checkable evidence before crossings execute.

**Architecture:** One file per record (`docs/decisions/DEC-YYYYMMDD-XXXXXX.md`) split on the exact line `## Envelope`. Grammar lives only in `skills/ship/record-decision/RECORD.md`; operational doctrine in sibling `SKILL.md`; mechanical checks in shipped `validate-records.sh` (POSIX sh + git, no Python mandate). Emitters (`finish-branch`, `release`) hand off via one-line `REQUIRED SUB-SKILL: use record-decision` and never copy doctrine. Trace shells to the validator when `docs/decisions/` exists. Participant law is ARCH-6 plus three projections (artifacts.md, AGENTS.md, using-skills).

**Tech Stack:** Markdown skills/docs; POSIX `sh` validator; Python `unittest` driver for validator CLI + structural greps; scenario/RED fixtures under `tests/decision-records/` (existing skill-text pattern). Leading words (use consistently): **payload**, **envelope**, **verdict**, **depth**, **storage disposition**, **adoption anchor**, **effective identity**, **record-before-crossing**.

## Global Constraints

Copied for every implementer brief:

1. **writing-great-skills bar (every skill edit):**
   - Predictability of *process*, not identical prose every run.
   - SSOT: grammar only in `RECORD.md`; doctrine only in `record-decision/SKILL.md`; emitters carry a one-line handoff, never copied doctrine.
   - Progressive disclosure: keep each SKILL.md under ~500 lines (prefer under 300); put long grammar in RECORD.md.
   - Form matches failure: HARD-GATE + rationalization table only where agents rationalize past the rule; recipes for ordered checklists.
   - Description discipline: trigger conditions only — no workflow dump. `record-decision` description must stay trigger-narrow (named emitter + terminal verdict + durable evidence).
   - RED before GREEN for skill-body slices: baseline scenarios against *current* text first; record verbatim failures in `red-baselines.md`; then minimal prose; re-run.
   - Cross-refs: `REQUIRED SUB-SKILL: use \`name\`` only — no `@` links.
   - Completion: every new step ends with checkable **Done when**.

2. **Architecture invariants (hard):**
   - **ARCH-1** Validator and decision-record passes are exact file/git checks — never LLM judgment.
   - **ARCH-2** Absent `docs/decisions/`, absent adoption (no anchor + no records), absent spine, absent `## Decision boundaries` → no-op, never invent.
   - **ARCH-3** Validator requires only POSIX utilities + git already guaranteed by emitters; never mandate Python/CI/hooks for consumers.
   - **ARCH-4** Requirement/ARCH IDs immutable; never renumber.
   - **ARCH-5** User-invoked may call model-invoked only; model-invoked never calls user-invoked. `record-decision` is model-invoked.
   - **ARCH-6** (added by this feature): skills enforce/record only skill-mediated actions; membership never inferred from roster/CODEOWNERS/PR authorship/artifacts.

3. **House rules** (`docs/product/guidelines.md`): imperative skill bodies; no production app code; Iron Laws never weakened; additive project.md edits only.

4. **Team packaging:** Solo (this repo). No invented peer reviewers/assignees; agent-as-pair; full gates still apply.

5. **Verify commands** (must stay green):
   - Lint: `python3 scripts/lint-skill-frontmatter.py && python3 scripts/lint-handoffs.py && python3 scripts/lint-context7.py`
   - Unit: `python3 -m unittest discover -s tests`
   - Single module: `python3 -m unittest tests.<module>`
   - Validator under test: invoke the script under test, not a parallel reimplementation in Python.

6. **Test annotations:**
   - Unit methods: `test_DREC_N_M_…` or first-line docstring greppable `DREC-N.M`.
   - Scenarios: bare greppable `DREC-N.M` tokens in `tests/decision-records/scenarios.md`.
   - Trace ignore (record in `docs/agents/project.md` when fixtures land): `tests/decision-records/red-baselines.md` and any fixture files that embed fabricated `CODE-N.M` Scope values for E-spine negative tests — coverage IDs live in scenarios + unittest names/docstrings only.

7. **Commits:** one commit per task preferred; trailers `Implements: DREC-N.M` (comma-separated). Guards use `Guards: DREC-N.M` where the task only protects existing behavior.

8. **Forbidden:** root-level record template; Python/Node validator for consumers; silently rewriting payload bytes; de-escalating depth; name-only tag citations; inventing a registry/counter for IDs; implementing inbound-PR / review-contribution (out of scope); editing finish-branch/release beyond the design's emission hooks; weakening Iron Laws / using-skills 1% rule / subagent exemption.

9. **Design is the field dictionary:** field tokens, enums, and diagnostic pass names are exactly those in `design.md` (Verdict closed set; Boundary-Type open syntax; Storage dispositions; pass names E-dup / E-grammar / E-spine / W-uncited-tag / W-repeated-judgment / W-opaque). Do not invent alternate names.

10. **Handoff interface (emitters → record-decision):** inline text only — verdict, classification inputs (tier, boundary type, predicate facts), durable citations (commit IDs, PR refs, `tag name@object-id`), promotion substance. Never hand a `.skills/` path, temp path, or session-history locator.

## File Structure

| Path | Responsibility |
|---|---|
| `skills/ship/record-decision/RECORD.md` | Sole record grammar + boundary-type guidance table + verbatim-as-provenance note + non-authoritative index note |
| `skills/ship/record-decision/SKILL.md` | Caller gate, depth lookup, judgment/storage doctrine, publication chain, adoption-anchor write, mint/reissue recipes |
| `skills/ship/record-decision/validate-records.sh` | POSIX validator: `--mode=trace`, `--mode=publish --record <file>`, `--scan`; all E/W passes |
| `skills/ship/finish-branch/SKILL.md` | Fifth menu option (block); red-gate terminal block/discard; record-before-crossing handoffs |
| `skills/ship/release/SKILL.md` | Terminal release-approve/reject → record-decision; evidence fold-in; tag outcome append |
| `skills/execution/trace/SKILL.md` | Conditional decision-record passes section (shell to validator) |
| `skills/discovery/interpret/SKILL.md` | Ledger, claim labels, rationale rule, end-of-session digest, explicit read-only |
| `skills/meta/using-skills/SKILL.md` | Two-sentence participant-boundary projection (1% rule + subagent exemption untouched) |
| `docs/architecture/INDEX.md` | Add **ARCH-6** invariant |
| `docs/architecture/artifacts.md` | Three-role participant narrative + optional `discovery.md` in spec-folder layout |
| `docs/agents/project.md` (template + live) | Optional `## Decision boundaries` section schema; trace-ignore rows for DREC fixtures |
| `templates/agents/project.md` | Same optional `## Decision boundaries` schema for setup-repo consumers |
| `AGENTS.md` | Participant-boundary subsection (semantically complete); ship inventory includes `record-decision` |
| `.claude-plugin/plugin.json` | Register `./skills/ship/record-decision` |
| `tests/decision-records/fixtures/` | Substrate trees (`*/docs/decisions/…`) + `secrets/` for validator CLI |
| `tests/decision-records/scenarios.md` | Skill-text scenario asserts with greppable DREC IDs |
| `tests/decision-records/red-baselines.md` | RED transcripts per skill slice |
| `tests/test_drec_validate_records.py` | Flat unittest driver for validator + scan + determinism (discoverable) |
| `tests/test_drec_doc_surfaces.py` | Flat unittest greps for doctrine surfaces / four-surface drift / guards |
| `docs/architecture/workflows.md` | finish-branch menu inventory (five options after Task 6) |
| `skills/execution/execute-plan/SKILL.md` | Done-when finish-branch outcome list (five options) — inventory only |
| `docs/specs/INDEX.md` | Status stays aligned with requirements (Approved → Implemented at ship) |

A path not listed here is out of scope for this plan.

---

### Task 1: RECORD.md grammar + validator skeleton + golden fixture

**Files:**
- Create: `skills/ship/record-decision/RECORD.md`
- Create: `skills/ship/record-decision/validate-records.sh` (skeleton: CLI parse, exit codes, payload/envelope split, E-grammar on required fields)
- Create: `tests/decision-records/fixtures/valid-substrate-minimal/docs/decisions/ADOPTION.md`
- Create: `tests/decision-records/fixtures/valid-substrate-minimal/docs/decisions/DEC-20260724-A1B2C3.md`
- Create: `tests/decision-records/fixtures/invalid-minimal-depth/docs/decisions/ADOPTION.md`
- Create: `tests/decision-records/fixtures/invalid-minimal-depth/docs/decisions/DEC-20260724-A1B2C3.md` (same id shape with `Depth: Minimal`)
- Create: `tests/test_drec_validate_records.py` (flat module — discoverable by `unittest discover -s tests`)
- Create: `tests/decision-records/scenarios.md` (harness skeleton only)
- Create: `tests/decision-records/red-baselines.md` (stub sections)
- Modify: `docs/agents/project.md` — append to Trace ignore: `tests/decision-records/red-baselines.md`, `tests/decision-records/fixtures/`
- Test: `tests/test_drec_validate_records.py`

**Reuse:** none — new grammar (rung 7); POSIX sh validator is new; unittest driver mirrors `tests/test_plugin_manifest.py` style (rung 2)

**Interfaces:**
- Consumes: design §1 field dictionary; design decision 13 digest probe order
- Produces:
  - `RECORD.md` field names (frozen for later tasks): payload `Accepted:`, `Emitter:`, `Verdict:`, `Boundary-Type:`, `Scope:`, `Crossing-Exists:`, `Ceremony-Floor:`, `User-Escalation:`, `Depth:`, `Predicate-External-Audience:`, `Predicate-External-Audience-Fact:`, `Predicate-No-Mechanical-Undo:`, `Predicate-No-Mechanical-Undo-Fact:`, `Predicate-Persistent-Stakes:`, `Predicate-Persistent-Stakes-Fact:`, `Human-Judgment:`, `Judgment-Pointer:`, `Human-Accepted-Risk:`, `Accepted-Risk-Pointer:`, `Human-Response-If-Wrong:`, `Response-If-Wrong-Pointer:`, `Evidence:`, `Promoted-Evidence:`; envelope `Published:`, `Payload-Digest-Algorithm:`, `Payload-Digest:`, `Storage-Judgment:`, `Storage-Accepted-Risk:`, `Storage-Response-If-Wrong:`, `Storage-Reference-Judgment:`, `Storage-Reference-Accepted-Risk:`, `Storage-Reference-Response-If-Wrong:`, `Reissued-from:`, `Reissued-as:`, `Supersedes:`, `Superseded-by:`, `Retired:`, `Execution-Outcome:`; withheld sentinel exactly `[[withheld — see envelope]]`; split line exactly `## Envelope`
  - CLI: `validate-records.sh --mode=trace [--root <dir>]`, `validate-records.sh --mode=publish --record <file> [--root <dir>]`, `validate-records.sh --scan` (stdin); exit `0` no errors, `1` errors, `2` not-run
  - Diagnostic lines: `ERROR E-grammar …`, `ERROR E-dup …`, `ERROR E-spine …`, `warn  W-uncited-tag …`, `warn  W-repeated-judgment …`, `warn  W-opaque …` (two spaces after `warn`)

**Depends-on:** none

- [ ] **Step 1: Write the failing unittest harness + golden fixture outline**

Create `tests/test_drec_validate_records.py` (must stay flat under `tests/` so
`python3 -m unittest discover -s tests` picks it up — do **not** nest `test_*.py`
under `tests/decision-records/`):

```python
"""Validator CLI tests for boundary decision records.

DREC-1.1 DREC-1.2 DREC-3.4 DREC-5.1 DREC-11.2 DREC-11.16 DREC-11.19 DREC-11.23
"""
from __future__ import annotations

import os
import subprocess
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
VALIDATOR = REPO / "skills" / "ship" / "record-decision" / "validate-records.sh"
FIXTURES = REPO / "tests" / "decision-records" / "fixtures"


def run_validator(args: list[str], *, stdin: str | None = None, cwd: Path | None = None):
    proc = subprocess.run(
        ["sh", str(VALIDATOR), *args],
        input=stdin,
        text=True,
        capture_output=True,
        cwd=str(cwd or REPO),
        env=os.environ.copy(),
        check=False,
    )
    return proc.returncode, proc.stdout + proc.stderr


class TestDRECValidatorSkeleton(unittest.TestCase):
    def test_DREC_11_16_validator_script_exists_and_is_posix_sh(self):
        """DREC-11.16 DREC-11.23"""
        self.assertTrue(VALIDATOR.is_file(), f"missing {VALIDATOR}")
        text = VALIDATOR.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("#!/"), "must have a shebang")
        self.assertNotRegex(text, r"(?m)^\s*(python|node|ruby)\b")

    def test_DREC_1_2_valid_minimal_accountable_exits_0(self):
        """DREC-1.1 DREC-1.2 DREC-5.1 DREC-11.2"""
        root = FIXTURES / "valid-substrate-minimal"
        code, out = run_validator(["--mode=trace", "--root", str(root)])
        self.assertEqual(code, 0, out)

    def test_DREC_3_4_minimal_depth_is_e_grammar(self):
        """DREC-3.4 DREC-11.2"""
        root = FIXTURES / "invalid-minimal-depth"
        code, out = run_validator(["--mode=trace", "--root", str(root)])
        self.assertEqual(code, 1, out)
        self.assertIn("ERROR E-grammar", out)

    def test_DREC_11_19_exit_2_reserved_for_not_run(self):
        """Sanity: exit 2 path is reserved for capability/not-run (exercised in Task 3)."""
        self.assertTrue(VALIDATOR.is_file())


if __name__ == "__main__":
    unittest.main()
```

Create scenario harness skeleton in `tests/decision-records/scenarios.md`:

```markdown
# DREC structural and scenario checks

## S-grammar
<!-- Task 1 -->

## S-validator-passes
<!-- Task 2–3 -->

## S-scan
<!-- Task 4 -->

## S-record-decision
<!-- Task 5 -->

## S-finish-branch
<!-- Task 6 -->

## S-release
<!-- Task 7 -->

## S-trace
<!-- Task 8 -->

## S-participant
<!-- Task 9 -->

## S-interpret
<!-- Task 10 -->

## S-project-docs
<!-- Task 11 -->

## Coverage
<!-- Task 12 -->
```

Stub `red-baselines.md` with empty `## RED-record-decision`, `## RED-finish-branch`, `## RED-release`, `## RED-interpret` headings.

Run: `python3 -m unittest tests.test_drec_validate_records -v` — expect: FAIL (missing validator and/or fixtures).

- [ ] **Step 2: Author RECORD.md (complete grammar)**

Write `skills/ship/record-decision/RECORD.md` covering every field in Interfaces, with:

1. Substrate path: `docs/decisions/DEC-YYYYMMDD-XXXXXX.md` (one file = one record).
2. Payload / envelope split on the exact line `## Envelope` (column 0).
3. Single-line fields: `Name: value` at column 0.
4. Multi-line blocks: nothing after colon; content lines prefixed `| ` (bare `|` for blank); ends at first unprefixed line; stripping `| `/`|` recovers exact bytes.
5. Verdict enum closed: `merge|pr|discard|block|release-approve|release-reject`.
6. Boundary-Type open: `^[a-z][a-z0-9-]*$` — guidance table only (`integration`, `publication`, `disposal`, `release`); never a machine whitelist.
7. Depth: published records may only be `Guarded` or `Accountable`; `Minimal` illegal.
8. Storage dispositions on envelope; payload holds verbatim block or fixed withheld sentinel `[[withheld — see envelope]]`.
9. Evidence kinds: `commit|tag|pr|ci|release`; tag value form `<ref-name>@<object-id>`.
10. `Promoted-Evidence:` naming — deliberately not "digest" (DREC-8.5).
11. Effective identity = last `Reissued-as:` ID else `Published:` ID; filename stem must equal it; ID date must equal `Accepted:` date (`YYYYMMDD`).
12. Verbatim guarantee = human provenance, not authenticity (DREC-4.6).
13. Optional human index = regenerable non-authoritative projection (DREC-1.7).
14. Anchor content marker (first non-blank line): `# Decision-Record Adoption Anchor` with `Cutoff:` and `Baseline-Tag:` lines — full anchor grammar.

Done when: an implementer can mint a valid record from RECORD.md alone.

- [ ] **Step 3: Implement validate-records.sh skeleton**

POSIX `sh` only. Required behavior in this task:

```sh
#!/bin/sh
# validate-records.sh — decision-record validator (POSIX sh + git)
set -eu
# Parse --mode=trace|publish, --record, --root, --scan
# --scan: read stdin, match secret patterns (stub ok to always exit 0 until Task 4 — OR implement empty pattern list that exits 0; Task 4 fills patterns)
# Locate records: $ROOT/docs/decisions/DEC-*.md
# Locate anchors: files under docs/decisions/ whose first non-blank line is exactly "# Decision-Record Adoption Anchor"
# Split each record on line equal to "## Envelope"
# E-grammar: required payload/envelope fields present; Verdict enum; Depth ∈ {Guarded,Accountable}; Storage-* present for required judgment elements; block framing; filename stem == effective identity; Accepted date == ID YYYYMMDD
# Exit 0/1; print diagnostics to stdout
```

Also build fixtures:

- `fixtures/valid-substrate-minimal/docs/decisions/ADOPTION.md` — content-marked anchor with `Cutoff: 2026-01-01T00:00:00Z` and zero or more `Baseline-Tag:` lines.
- `fixtures/valid-substrate-minimal/docs/decisions/DEC-20260724-A1B2C3.md` — full Guarded or Accountable valid record whose digest matches the payload bytes under the algorithm declared (compute with `shasum -a 256` or `sha256sum` when writing the fixture).
- `fixtures/invalid-minimal-depth/...` — same shape with `Depth: Minimal` → must ERROR E-grammar.

Digest helper for fixture authoring (host side, not shipped): compute payload bytes (everything before `## Envelope` line, preserving newlines) and hash.

Run: `python3 -m unittest tests.test_drec_validate_records -v` — expect: PASS for Task 1 tests.
Also confirm discover picks it up: `python3 -m unittest discover -s tests -v 2>&1 | rg drec_validate` — expect: test names listed.

- [ ] **Step 4: Commit**

```
git add skills/ship/record-decision/RECORD.md \
  skills/ship/record-decision/validate-records.sh \
  tests/test_drec_validate_records.py tests/decision-records docs/agents/project.md
git commit -m "$(cat <<'EOF'
Add decision-record grammar and validator skeleton.

Implements: DREC-1.1, DREC-1.2, DREC-1.6, DREC-1.7, DREC-2.2, DREC-3.4, DREC-4.4, DREC-4.6, DREC-5.1, DREC-8.5, DREC-11.2, DREC-11.16, DREC-11.23
EOF
)"
```

(IDs 1.6/1.7/2.2/4.4/4.6/8.5 are satisfied by RECORD.md text presence — also tag them in `scenarios.md` §S-grammar with structural greps for those phrases.)

Add to `scenarios.md` §S-grammar greps asserting RECORD.md contains: outward-citations-only Scope note, non-authoritative index note, provenance-not-authenticity, Promoted-Evidence (not digest for promotion), Boundary-Type guidance table. Tags: `DREC-1.6 DREC-1.7 DREC-2.2 DREC-4.4 DREC-4.6 DREC-8.5`.

_Requirements: DREC-1.1, DREC-1.2, DREC-1.6, DREC-1.7, DREC-2.2, DREC-3.4, DREC-4.4, DREC-4.6, DREC-5.1, DREC-8.5, DREC-11.2, DREC-11.16, DREC-11.23_

---

### Task 2: Validator — identity, reissue, supersession, digests, prohibited locators

**Files:**
- Modify: `skills/ship/record-decision/validate-records.sh`
- Create: fixtures under `tests/decision-records/fixtures/` for E-dup, reissue, supersession good/bad, digest mismatch, prohibited locator, multi-record same feature, Scope none
- Modify: `tests/test_drec_validate_records.py` — append new test methods
- Test: `tests/test_drec_validate_records.py`

**Reuse:** existing — Task 1 validator skeleton + RECORD.md identity rules (rung 2 within feature)

**Interfaces:**
- Consumes: Task 1 CLI + field names
- Produces: full E-dup; E-grammar rules for reissue pairs, supersession bidirectionality/linearity/cycles, digest verify, prohibited locator classes (`.skills/`, temp paths, absolute local paths, session-history phrases), multi-record acceptance (no error for same Scope+Boundary-Type), Scope:`none` acceptance

**Depends-on:** Task 1

- [ ] **Step 1: Write failing tests**

Add methods to `tests/test_drec_validate_records.py` (docstrings carry IDs):

| Method | Fixture idea | Expect | IDs |
|---|---|---|---|
| `test_DREC_11_1_e_dup_two_files_same_effective_id` | two DEC files same effective identity | exit 1, `ERROR E-dup` | DREC-11.1, 2.5 |
| `test_DREC_2_4_reissue_chain_filename_matches_effective` | file with `Reissued-as: DEC-…` and renamed stem | exit 0 | DREC-2.4, 2.1, 2.5, 2.9 |
| `test_DREC_1_4_1_8_supersession_bidirectional_ok` | old has `Superseded-by: NEW`, new has `Supersedes: OLD` | exit 0; effective view is NEW | DREC-1.4, 1.8 |
| `test_DREC_1_8_broken_supersession_is_e_grammar` | one-sided Supersedes | exit 1, E-grammar | DREC-1.8 |
| `test_DREC_11_2_digest_mismatch` | wrong Payload-Digest | exit 1, E-grammar | DREC-11.2 (tamper) |
| `test_DREC_8_1_8_2_prohibited_locator` | Evidence cites `.skills/foo` or `/tmp/x` | exit 1, E-grammar | DREC-8.1, 8.2 |
| `test_DREC_2_6_same_feature_two_records_ok` | two valid different IDs, same Scope | exit 0 | DREC-2.6 |
| `test_DREC_2_7_scope_none_ok` | `Scope: none` | exit 0 | DREC-2.7 |
| `test_DREC_2_8_unknown_boundary_type_token_ok` | `Boundary-Type: custom-later-rename` matching syntax | exit 0 | DREC-2.8 |
| `test_DREC_14_2_repeated_run_identical` | run twice on same valid root | same exit + same diagnostic text | DREC-14.2 |

Also: publish mode validates candidate file together with substrate:

```python
def test_DREC_publish_mode_includes_candidate(self):
    """DREC-11.16 — publish mode uses the same rule set."""
    ...
```

Run — expect: FAIL until rules exist.

- [ ] **Step 2: Implement rules in validate-records.sh**

Implement:

1. **Effective identity** per RECORD.md; E-dup on collisions of effective identities across files.
2. **Reissue:** `Reissued-from:` / `Reissued-as:` pairs; chain order; filename == last Reissued-as else Published ID; Accepted date preserved (YYYYMMDD match).
3. **Supersession:** ≤1 Supersedes targeting any ID; ≤1 Superseded-by per envelope; bidirectional match; cycle detection → E-grammar.
4. **Digest:** for algorithm `sha256` use probe `sha256sum` → `shasum -a 256` → `openssl dgst -sha256`; for `git-blob` use `git hash-object --stdin`. If declared algorithm cannot be computed → exit 2 (not-run). Mismatch → E-grammar.
5. **Prohibited locators:** reject evidence/storage-reference values matching `.skills/`, `/tmp/`, absolute paths (`/*` on Unix), or the literal class "session history" if used as a locator token — keep the rule list documented in a comment block in the script matching RECORD.md.
6. **No error** for multiple records same feature/boundary or `Scope: none`.

Run unittest — expect: PASS.

- [ ] **Step 3: Commit**

Trailers: `Implements: DREC-1.4, DREC-1.8, DREC-2.1, DREC-2.4, DREC-2.5, DREC-2.6, DREC-2.7, DREC-2.8, DREC-2.9, DREC-8.1, DREC-8.2, DREC-11.1, DREC-14.2`.

_Requirements: DREC-1.4, DREC-1.8, DREC-2.1, DREC-2.4, DREC-2.5, DREC-2.6, DREC-2.7, DREC-2.8, DREC-2.9, DREC-8.1, DREC-8.2, DREC-11.1, DREC-14.2_

---

### Task 3: Validator — adoption anchor, E-spine, W-passes, no-op modes

**Files:**
- Modify: `skills/ship/record-decision/validate-records.sh`
- Create: fixtures for zero/multiple anchors, uncited tags, repeated judgment, opaque storage, spine present/absent, empty substrate
- Modify: `tests/test_drec_validate_records.py`
- Modify: `tests/decision-records/scenarios.md` — §S-validator-passes
- Test: `tests/test_drec_validate_records.py`

**Reuse:** existing — Task 1–2 validator; design §10–11 (rung 2)

**Interfaces:**
- Consumes: Task 1–2 CLI
- Produces: E-spine; W-uncited-tag (name@id both halves; diagnostic text "absent from or changed since the adoption baseline"); W-repeated-judgment; W-opaque; anchor count rules; ARCH-2 no-ops (no decisions dir / no anchor+no records / tags invisible / spine absent)

**Depends-on:** Task 2

- [ ] **Step 1: Write failing tests**

| Method | Expect | IDs |
|---|---|---|
| `test_DREC_11_12_zero_anchors_with_records_errors` | E-grammar (anchor-count) | DREC-11.11, 11.12, 11.13 |
| `test_DREC_11_12_two_anchors_error` | error | DREC-11.12 |
| `test_DREC_11_18_no_docs_decisions_exits_0` | empty root without docs/decisions → 0, no findings | DREC-11.18 |
| `test_DREC_11_4_e_spine_noops_without_requirements` | root with records but no `docs/specs/*/requirements.md` → no E-spine | DREC-11.4 |
| `test_DREC_11_3_e_spine_unknown_scope_id` | root with a real requirements tree + Scope citing unknown ID → ERROR E-spine | DREC-11.3 |
| `test_DREC_11_5_11_22_11_24_uncited_post_adoption_tag` | anchor baseline missing a visible tag → warn W-uncited-tag with baseline wording | DREC-11.5, 11.22, 11.24 |
| `test_DREC_11_15_no_visible_tags_noop_uncited` | simulate empty `git tag -l` (fixture note: validator may accept `GIT_DIR` override or `DREC_TAG_LIST_FILE` test seam — **if a test seam is added, document it as test-only env var, default off**) | DREC-11.15 |
| `test_DREC_11_6_11_7_repeated_judgment` | ≥3 identical judgment bodies → warn with IDs; verdict words excluded | DREC-11.6, 11.7 |
| `test_DREC_11_8_11_9_w_opaque` | `withheld(unavailable)` warns; valid `withheld(reference)` does not | DREC-11.8, 11.9 |
| `test_DREC_11_10_crossing_without_record_never_error` | empty `docs/decisions/` or substrate with only an anchor and zero DEC files → exit 0 and **no** `ERROR` line about missing records/crossings; doctrine comment or SKILL/trace prose (Task 5/8) states absence is warning-ceiling only because mediation cannot be proven mechanically | DREC-11.10 |
| `test_DREC_11_17_no_external_existence_probe` | grep script for curl/wget/gh api — none | DREC-11.17 |
| Tag citation from `Execution-Outcome: tag name@id note` counts for W-uncited-tag | release-style citation | design decision 12 / DREC-11.5 |

**DREC-11.10 interpretation (frozen for implementers):** Approved text requires crossing-without-record stay at **warning** severity and never become an **error**. Design ratifies that the validator cannot mechanically distinguish skill-mediated crossings from external/direct action (ARCH-6), so there is **no automated E-pass or W-pass** named for absence. Satisfaction = (a) validator never emits `ERROR` for “crossing has no record”, (b) trace + record-decision doctrine state that any human/agent report of such absence is advisory/warning only, never a gate-failing error. Do **not** invent a W-crossing-without-record pass unless a later amend defines a mechanical predicate.

For E-spine positive test, build a tiny fake `docs/specs/x/requirements.md` inside the fixture root with one known ID and cite an unknown one from a record.

For tag tests: prefer a **test-only** env `DREC_VISIBLE_TAGS` (newline-separated `name@objectid`) so tests do not need a real git tag database; when unset, use `git tag -l` + `git rev-list -n1 <tag>` (or `git rev-parse <tag>^{}`). Document in script header.

- [ ] **Step 2: Implement remaining passes**

Implement E-spine, W-* passes, anchor counting, no-op branches exactly per design §10–11. Ensure exit 2 when digest algorithm unavailable (add a test that forces a fake algorithm name `unavailable-algo` → exit 2) — DREC-11.19.

- [ ] **Step 3: GREEN + scenarios notes**

Append §S-validator-passes listing each pass name and pointing at the unittest methods. Run full validator unittest module — PASS.

- [ ] **Step 4: Commit**

`Implements: DREC-11.3, DREC-11.4, DREC-11.5, DREC-11.6, DREC-11.7, DREC-11.8, DREC-11.9, DREC-11.10, DREC-11.11, DREC-11.12, DREC-11.13, DREC-11.14, DREC-11.15, DREC-11.17, DREC-11.18, DREC-11.19, DREC-11.22, DREC-11.24`  
(Note: DREC-11.14 is fixture+RECORD presence of Baseline-Tag grammar; assert in unittest that a valid anchor without Baseline-Tag when tags existed is still parseable — baseline may be empty if zero tags at adoption.)

_Requirements: DREC-11.3, DREC-11.4, DREC-11.5, DREC-11.6, DREC-11.7, DREC-11.8, DREC-11.9, DREC-11.10, DREC-11.11, DREC-11.12, DREC-11.13, DREC-11.14, DREC-11.15, DREC-11.17, DREC-11.18, DREC-11.19, DREC-11.22, DREC-11.24_

---

### Task 4: Secret scan (`--scan`)

**Files:**
- Modify: `skills/ship/record-decision/validate-records.sh` — implement `--scan`
- Create: `tests/decision-records/fixtures/secrets/aws-akia.txt`, `github-pat.txt`, `pem-block.txt`, `slack-xox.txt`, `generic-assignment.txt`, `clean-prose.txt`
- Modify: `tests/test_drec_validate_records.py`
- Modify: `tests/decision-records/scenarios.md` — §S-scan
- Test: `tests/test_drec_validate_records.py`

**Reuse:** existing — single validator artifact hosts scan patterns (design §7, rung 2)

**Interfaces:**
- Consumes: Task 1 CLI `--scan`
- Produces: deterministic pattern set documented in script comments + RECORD.md or SKILL pointer; exit 1 on hit with pattern family name; exit 0 on clean

**Depends-on:** Task 1

- [ ] **Step 1: Failing tests**

```python
class TestDRECScan(unittest.TestCase):
    def test_DREC_14_1_hit_on_akia(self):
        """DREC-14.1 DREC-5.10"""
        code, out = run_validator(["--scan"], stdin="key=AKIAIOSFODNN7EXAMPLE\n")
        self.assertEqual(code, 1, out)

    def test_DREC_14_1_clean_prose(self):
        """DREC-14.1"""
        code, out = run_validator(["--scan"], stdin="Ship the feature after review.\n")
        self.assertEqual(code, 0, out)
```

Patterns (fixed list — implement all):

1. PEM/private-key blocks (`BEGIN … PRIVATE KEY`)
2. AWS access key `AKIA[0-9A-Z]{16}`
3. GitHub `ghp_` / `github_pat_`
4. Slack `xox[baprs]-`
5. Generic assignment: `(?i)(api[_-]?key|token|secret|password)\s*=\s*\S+`

- [ ] **Step 2: Implement `--scan` in the validator** using POSIX `grep -E` / `awk` only — no Python.

- [ ] **Step 3: Commit**

`Implements: DREC-5.10, DREC-14.1`

_Requirements: DREC-5.10, DREC-14.1_

---

### Task 5: record-decision skill (doctrine + caller gate + publication chain)

**Files:**
- Create: `skills/ship/record-decision/SKILL.md`
- Modify: `.claude-plugin/plugin.json` — add `"./skills/ship/record-decision"`
- Modify: `tests/decision-records/scenarios.md` — §S-record-decision
- Modify: `tests/decision-records/red-baselines.md` — §RED-record-decision
- Create: `tests/test_drec_doc_surfaces.py` — frontmatter/structural greps for this skill (extend later tasks)
- Test: scenarios + `tests.test_drec_doc_surfaces` + `python3 -m unittest tests.test_plugin_manifest`

**Reuse:** existing — `REQUIRED SUB-SKILL:` convention and skill-directory layout (rung 2); release stop-rule idiom for publication failure (rung 2, pattern)

**Interfaces:**
- Consumes: RECORD.md grammar; validate-records.sh publish + scan modes; handoff interface from Global Constraints
- Produces: model-invoked skill with HARD-GATE caller set `{finish-branch, release}`; depth formula; judgment/storage recipes; mint/reissue recipes; adoption-anchor first-write; DREC-15.1 ordered checklist

**Depends-on:** Task 1, Task 3, Task 4

- [ ] **Step 1: RED baselines (before writing SKILL.md body)**

In `red-baselines.md` §RED-record-decision, record expected baseline failures against *absence* of the skill (or empty stub):

1. Invoked without terminal verdict → still writes a file (must not). `DREC-9.5`
2. Invoked by a non-emitter → still writes. `DREC-9.6`
3. Summarizes user risk prose. `DREC-4.3`
4. Publishes Minimal depth. `DREC-3.4`
5. Executes crossing before validator exit 0. `DREC-15.1`
6. Skips secret scan on repo-verbatim judgment. `DREC-14.1` / `DREC-5.10`
7. Treats bare "yes" as accepted-risk prose. `DREC-4.5`
8. **§15 pressure — secret hit + user stops** → crossing still executes (must not). `DREC-15.2`
9. **§15 pressure — missing required judgment** → invalid record / validator fail but crossing proceeds (must not). `DREC-15.6`
10. **§15 pressure — validator exit 2 (not-run) at publish** → treated as pass (must not; withhold crossing). `DREC-15.6`
11. **§15 pressure — filesystem write failure** → reports success / enacts crossing (must not). `DREC-15.2`
12. **§15 pressure — block/reject record fails to publish** → treated as recorded completion (must not; incomplete accountability). `DREC-15.5`
13. **§15 pressure — publish succeeds, crossing fails** → mutates payload or discards record instead of `Execution-Outcome:` append (must not). `DREC-15.7`

- [ ] **Step 2: Failing structural asserts**

In `tests/test_drec_doc_surfaces.py`:

```python
"""Doc-surface and skill-text structural checks for DREC."""
import json
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / "skills" / "ship" / "record-decision" / "SKILL.md"
RECORD = REPO / "skills" / "ship" / "record-decision" / "RECORD.md"
PLUGIN = REPO / ".claude-plugin" / "plugin.json"


class TestDRECRecordDecisionSkill(unittest.TestCase):
    def test_DREC_9_1_9_2_skill_and_record_siblings(self):
        """DREC-9.1 DREC-9.2"""
        self.assertTrue(SKILL.is_file())
        self.assertTrue(RECORD.is_file())
        body = SKILL.read_text(encoding="utf-8")
        self.assertIn("RECORD.md", body)
        # Grammar must not be duplicated: no full field list dump
        self.assertNotIn("Payload-Digest-Algorithm:", body)

    def test_DREC_9_4_9_9_frontmatter(self):
        """DREC-9.4 DREC-9.9"""
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("name: record-decision", text)
        self.assertNotIn("disable-model-invocation: true", text.split("---", 2)[1])
        desc = text.split("---", 2)[1]
        self.assertRegex(desc, r"finish-branch|release")
        self.assertNotRegex(desc.lower(), r"important decision|generic approval")

    def test_DREC_9_8_no_root_template(self):
        """DREC-9.8"""
        self.assertFalse((REPO / "RECORD.template.md").exists())
        self.assertFalse((REPO / "docs" / "decisions" / "TEMPLATE.md").exists())

    def test_DREC_plugin_lists_record_decision(self):
        data = json.loads(PLUGIN.read_text(encoding="utf-8"))
        skills = {s.removeprefix("./") for s in data["skills"]}
        self.assertIn("skills/ship/record-decision", skills)
```

Run — expect: FAIL.

- [ ] **Step 3: Author SKILL.md (doctrine only)**

Structure (imperative voice):

1. Frontmatter description (exact sense): *Use when a named production-boundary emitter (finish-branch or release) has obtained a terminal human verdict and hands off durable evidence for publication.*
2. **HARD-GATE — Caller gate** (DREC-9.5/9.6/9.7/6.2/6.11): closed caller set; terminal verdict required; evidence producers cannot self-promote; return without artifact otherwise. Rationalization table from RED.
3. **Pointer:** all grammar in sibling `RECORD.md` — do not restate fields.
4. **Depth computation** (DREC-3.1–3.14, 3.17–3.20, 3.19 disposal→Accountable): fixed lookup table; `depth = max(ceremony floor, boundary floor, predicate escalation)`; Minimal never published; external-audience TRUE/FALSE/unknown rules; never de-escalate; user may escalate; record all classification fields.
5. **Judgment elicitation** (DREC-4.1–4.5): Guarded vs Accountable required elements; Iron Law verbatim-only; bare affirmation = verdict only.
6. **Storage resolution** (DREC-5.2–5.9, 5.11): standing policy; withhold offer; conditional confirm for sensitive; exact payload display; withheld forks; never redact-and-label-verbatim.
7. **Secret scan:** run `validate-records.sh --scan` on judgment prose before write; on hit only rephrase / withhold / stop.
8. **Evidence + promotion** (DREC-8.3–8.4, 8.6): promote substance into `Promoted-Evidence:` before display; never present as human judgment; late evidence → envelope only.
9. **Minting recipe** (DREC-2.1, 2.3): date from locked `Accepted:`; 6 Crockford chars; entropy probe `/dev/urandom` via `od` else `awk`+`$$`+`date`; no registry.
10. **Publication checklist** (DREC-15.1–15.7): numbered order ending in "crossing executes only after validator exits 0"; failure semantics; retry reuses captured words; block/reject publication failure wording; post-publish crossing failure → Execution-Outcome append.
11. **Adoption anchor first-write** (DREC-11.11–11.14): if no content-marked anchor and first record would publish, write anchor once with Cutoff + Baseline-Tag snapshot; never edit afterward; never infer from earliest record.
12. **Reissue recipe** (DREC-2.4): append-only pair; rename file; never rewrite Published or payload.
13. **Pins:** if `docs/agents/project.md` has `## Decision boundaries`, apply raises only; ignore lower floors with one-line notice (DREC-3.15–3.16) — even if template lands in Task 11, doctrine must describe the read now.

Done when: line count under 500; no grammar field dump; RED rationalizations addressed.

- [ ] **Step 4: Register plugin + GREEN**

Add `"./skills/ship/record-decision"` to `plugin.json` skills array (near other ship skills).

Run:

```bash
python3 -m unittest tests.test_drec_doc_surfaces tests.test_plugin_manifest -v
python3 scripts/lint-skill-frontmatter.py
python3 scripts/lint-handoffs.py
```

Expect: PASS.

Scenarios §S-record-decision: list structural bullets matching the HARD-GATE, depth formula, publication order, mint recipe presence; greppable IDs for all Task 5 requirement footers.

- [ ] **Step 5: Commit**

`Implements: DREC-1.3, DREC-1.5, DREC-2.3, DREC-3.1, DREC-3.2, DREC-3.3, DREC-3.5, DREC-3.6, DREC-3.7, DREC-3.8, DREC-3.9, DREC-3.10, DREC-3.11, DREC-3.12, DREC-3.13, DREC-3.14, DREC-3.17, DREC-3.18, DREC-3.19, DREC-3.20, DREC-4.1, DREC-4.2, DREC-4.3, DREC-4.5, DREC-5.2, DREC-5.3, DREC-5.4, DREC-5.5, DREC-5.6, DREC-5.7, DREC-5.8, DREC-5.9, DREC-5.11, DREC-6.1, DREC-6.2, DREC-6.11, DREC-8.3, DREC-8.4, DREC-8.6, DREC-9.1, DREC-9.2, DREC-9.4, DREC-9.5, DREC-9.6, DREC-9.7, DREC-9.8, DREC-9.9, DREC-15.1, DREC-15.2, DREC-15.3, DREC-15.4, DREC-15.5, DREC-15.6, DREC-15.7`

_Requirements: DREC-1.3, DREC-1.5, DREC-2.3, DREC-3.1, DREC-3.2, DREC-3.3, DREC-3.5, DREC-3.6, DREC-3.7, DREC-3.8, DREC-3.9, DREC-3.10, DREC-3.11, DREC-3.12, DREC-3.13, DREC-3.14, DREC-3.17, DREC-3.18, DREC-3.19, DREC-3.20, DREC-4.1, DREC-4.2, DREC-4.3, DREC-4.5, DREC-5.2, DREC-5.3, DREC-5.4, DREC-5.5, DREC-5.6, DREC-5.7, DREC-5.8, DREC-5.9, DREC-5.11, DREC-6.1, DREC-6.2, DREC-6.11, DREC-8.3, DREC-8.4, DREC-8.6, DREC-9.1, DREC-9.2, DREC-9.4, DREC-9.5, DREC-9.6, DREC-9.7, DREC-9.8, DREC-9.9, DREC-15.1, DREC-15.2, DREC-15.3, DREC-15.4, DREC-15.5, DREC-15.6, DREC-15.7_

---

### Task 6: finish-branch integration

**Files:**
- Modify: `skills/ship/finish-branch/SKILL.md`
- Modify: `tests/decision-records/scenarios.md` — §S-finish-branch
- Modify: `tests/decision-records/red-baselines.md` — §RED-finish-branch
- Modify: `tests/test_drec_doc_surfaces.py` — finish-branch greps
- Test: scenarios + `tests.test_drec_doc_surfaces`

**Reuse:** existing — extends menu/gate structure in place (design §13, rung 2)

**Interfaces:**
- Consumes: record-decision handoff interface; verdict tokens `merge|pr|discard|block`; boundary types `integration|publication|disposal`
- Produces: fifth menu option; red-path terminal block/discard; record-before-crossing ordering; keep/pause/mechanical-fail non-emission

**Depends-on:** Task 5

- [ ] **Step 1: RED baselines**

Against current finish-branch text:

1. No block option (DREC-6.4).
2. Entire menu withheld on red — no path for terminal block/discard (DREC-6.10).
3. Merge executes without record-decision (DREC-6.3, 15.1).
4. Keep might be mistaken for record-worthy (DREC-6.6).

Record in red-baselines.

- [ ] **Step 2: Failing asserts**

```python
def test_DREC_6_4_6_14_block_option_and_guards(self):
    """DREC-6.4 DREC-6.12 DREC-6.13 DREC-6.14"""
    text = (REPO / "skills/ship/finish-branch/SKILL.md").read_text()
    self.assertIn("Block:", text)  # or exact menu line from design
    self.assertIn("REQUIRED SUB-SKILL: use `record-decision`", text)
    self.assertIn("discard", text)  # typed confirmation remains
    # four original options still present in order
    for phrase in ["Merge", "Pull Request", "Keep", "Discard"]:
        self.assertIn(phrase, text)
```

- [ ] **Step 3: Patch finish-branch (minimal)**

1. **Gate (§1) — rewrite the STOP paragraph** (live text today says “Do not present the menu” — that must change). On verify/trace/acceptance failure:
   - Do **not** offer merge or PR (integration options stay withheld — DREC-6.12).
   - **Do** still offer terminal **block** and **discard** so the user can issue those verdicts against red evidence (DREC-6.10/6.8); emit via record-decision; never execute merge/PR on red.
   - Mechanical failure alone without an explicit terminal block/discard → no record (DREC-6.7). Pause/defer → no record (DREC-6.9).
2. **Menu (§3):** Change “Present exactly these four options” → five. Keep options 1–4 text/order; add option 5 block/reject (design wording). Detached HEAD: drop merge only; renumber remaining including block.
3. **Execute (§4):**
   - Options merge / PR / discard / block: **before** git/gh side effects, `REQUIRED SUB-SKILL: use record-decision` with verdict + boundary type (`integration` / `publication` / `disposal` / blocked-crossing's type) + tier + durable evidence inline. On publication failure → do not execute crossing; report verdict not enacted (DREC-15.2/15.3). Block has no crossing side effect but still requires successful record for "recorded completion" (DREC-15.5).
   - Option keep: explicitly no record-decision (DREC-6.6).
4. Discard: still requires literally typed `discard` (DREC-6.13); boundary type always `disposal` at Accountable (doctrine in record-decision; emitter passes disposal).
5. **Red flags:** replace “Present the menu while any verify command fails” with “Offer merge or PR while any verify command fails” (block/discard on red remain allowed). Update rationalization “Four options, every time” → five options including block.
6. Do **not** copy depth/storage doctrine into finish-branch.

- [ ] **Step 4: GREEN + commit**

`Implements: DREC-6.3, DREC-6.4, DREC-6.5, DREC-6.6, DREC-6.7, DREC-6.8, DREC-6.9, DREC-6.10, DREC-6.12, DREC-6.13, DREC-6.14, DREC-9.3`  
(`DREC-9.3` shared with release — cite here for finish-branch handoff line.)

_Requirements: DREC-6.3, DREC-6.4, DREC-6.5, DREC-6.6, DREC-6.7, DREC-6.8, DREC-6.9, DREC-6.10, DREC-6.12, DREC-6.13, DREC-6.14, DREC-9.3_

---

### Task 7: release integration

**Files:**
- Modify: `skills/ship/release/SKILL.md`
- Modify: `tests/decision-records/scenarios.md` — §S-release
- Modify: `tests/decision-records/red-baselines.md` — §RED-release
- Modify: `tests/test_drec_doc_surfaces.py`
- Test: scenarios + `tests.test_drec_doc_surfaces`

**Reuse:** existing — extends release gate sequence in place (design §14, rung 2)

**Interfaces:**
- Consumes: record-decision; verdicts `release-approve|release-reject`
- Produces: one record per terminal release verdict; evidence fold-in; tag Execution-Outcome append; stop-rule/non-emission unchanged

**Depends-on:** Task 5

- [ ] **Step 1: RED baselines**

1. Successful tag path creates no decision record.
2. Mechanical stop might be mis-recorded as release-reject.
3. Risk of multiple records per version/build/smoke approvals.

- [ ] **Step 2: Failing asserts**

```python
def test_DREC_7_release_hooks(self):
    """DREC-7.1 DREC-7.2 DREC-7.3 DREC-7.4 DREC-7.5 DREC-7.6"""
    text = (REPO / "skills/ship/release/SKILL.md").read_text()
    self.assertIn("REQUIRED SUB-SKILL: use `record-decision`", text)
    self.assertIn("release-approve", text)
    self.assertIn("release-reject", text)
    self.assertIn("The stop rule", text)  # guard unchanged
    self.assertIn("Only after explicit user approval", text)
```

- [ ] **Step 3: Patch release**

1. After smoke gate + explicit user approval to tag (step g approval = successful terminal verdict): invoke record-decision with `release-approve`, `Boundary-Type: release`, Accountable depth inputs, and evidence lines folding version/build/smoke/tag approvals (DREC-7.1/7.2) — **before** `git tag` / push.
2. After tag exists: append `Execution-Outcome: tag <ref-name>@<object-id> pushed <UTC>` to the published record envelope.
3. **`release-reject` insertion points (concrete):**
   - Add a short **terminal reject** affordance at two places only: (a) when the stop rule fires (any step fails), after reporting the failure, ask once whether the user is issuing an **explicit terminal reject** of this release (yes → `release-reject` via record-decision with `Boundary-Type: release`, then stop with repo un-released; no / silence / “fix later” → **no record**, DREC-7.3); (b) when proposing version or tag approval, accept an explicit “reject this release” answer as `release-reject` instead of approval — still no partial release side effects (DREC-7.6).
   - Distinguish in prose: **stop-rule alone without an explicit reject verdict = no record**; **explicit reject verdict = exactly one record**.
4. Stop rule without terminal human verdict → no record (DREC-7.3).
5. Guards: stop rule and dual explicit approvals remain (DREC-7.4/7.5) — do not reword into softer language. Keep the literal “Only after explicit user approval” tag gate.
6. No doctrine copy.

- [ ] **Step 4: Commit**

`Implements: DREC-7.1, DREC-7.2, DREC-7.3, DREC-7.4, DREC-7.5, DREC-7.6`  
(If Task 6 already claimed DREC-9.3 for finish-branch, release still must contain the same handoff line — coverage already tagged; re-list `DREC-9.3` in scenarios for release path.)

_Requirements: DREC-7.1, DREC-7.2, DREC-7.3, DREC-7.4, DREC-7.5, DREC-7.6_

---

### Task 8: trace integration

**Files:**
- Modify: `skills/execution/trace/SKILL.md`
- Modify: `tests/decision-records/scenarios.md` — §S-trace
- Modify: `tests/test_drec_doc_surfaces.py`
- Test: scenarios + `tests.test_drec_doc_surfaces`

**Reuse:** existing — conditional-pass pattern like invariant passes 5–6 (design §12, rung 2)

**Interfaces:**
- Consumes: `validate-records.sh --mode=trace` diagnostic lines and exit codes
- Produces: section "Decision-record passes — only when `docs/decisions/` exists"; E1–E5/W1–W3 unchanged; coverage law unchanged; DREC-11.10 doctrine sentence

**Depends-on:** Task 3

- [ ] **Step 1: Failing asserts**

```python
def test_DREC_11_20_11_21_trace_guards(self):
    """DREC-11.20 DREC-11.21 DREC-11.10"""
    text = (REPO / "skills/execution/trace/SKILL.md").read_text()
    self.assertIn("Decision-record passes", text)
    self.assertIn("docs/decisions/", text)
    self.assertIn("validate-records.sh", text)
    for code in ["E1", "E2", "E3", "W1", "W2", "E4", "E5", "W3"]:
        self.assertIn(code, text)
    self.assertIn("Coverage is textual presence", text)
    # DREC-11.10: absence of a record is never an error; warning ceiling only
    self.assertRegex(text, r"crossing.without.record|without a (decision )?record", re.I)
    self.assertNotRegex(
        text,
        r"ERROR.*crossing without|crossing without.*ERROR",
        re.I,
    )
```

- [ ] **Step 2: Patch trace**

Add section after invariant passes (mirror ARCH-2 conditional):

```markdown
### Decision-record passes — only when `docs/decisions/` exists

If the repo has no `docs/decisions/` directory, skip this section entirely;
the finding set remains passes 1–6 (or 1–4) unchanged.

When `docs/decisions/` exists, run the shipped validator (resolve path relative
to this skill set install, sibling of record-decision):

```bash
sh skills/ship/record-decision/validate-records.sh --mode=trace
```

Merge its diagnostic lines into the report **verbatim**. Exit code 1 → treat as
trace errors (gate fail). Exit code 2 → decision-record passes **not-run**
(never "passed"). Exit 0 → no decision-record errors (warnings may still appear).

Do not reinterpret validator findings. **Crossing-without-record (DREC-11.10):**
the validator does not emit an automated finding for “a production crossing
lacks a record,” because it cannot tell skill-mediated verdicts from direct
human action or external contribution (ARCH-6). If an agent or human notes
such an absence, treat it as a **warning-level concern only — never an error
and never a release/verify gate fail**. Existing E1–E5 / W1–W3 semantics are
unchanged. Coverage remains textual presence without judgment.
```

Path resolution note: when installed as a plugin, agents should invoke the validator from the skill directory discovered beside `record-decision` (same pattern consumers use for other skill-local files). Document one resolution recipe; do not require a PATH install.

- [ ] **Step 3: Commit**

`Implements: DREC-11.20, DREC-11.21` / `Guards: DREC-11.10` (doctrine ceiling also tested here; mechanical half in Task 3).

_Requirements: DREC-11.10, DREC-11.20, DREC-11.21_

---

### Task 9: Participant-model surfaces (ARCH-6 + projections)

**Files:**
- Modify: `docs/architecture/INDEX.md` — add **ARCH-6**; update dogfood comment ARCH-1..5 → ARCH-1..6
- Modify: `docs/architecture/artifacts.md` — three-role narrative; list `docs/decisions/` in the consumer layout block
- Modify: `AGENTS.md` — "Participant boundary" subsection; keep Four Iron Laws + orchestration unchanged
- Modify: `skills/meta/using-skills/SKILL.md` — two-sentence projection only
- Modify: `tests/test_drec_doc_surfaces.py` — four-surface drift check
- Modify: `tests/decision-records/scenarios.md` — §S-participant
- Test: `tests.test_drec_doc_surfaces`

**Reuse:** existing — each surface extends in place (design §16, rung 2)

**Interfaces:**
- Consumes: Correction 1 doctrine from requirements/discovery (mediation scope, never-infer)
- Produces: greppable `**ARCH-6**`; load-bearing phrases present on all four surfaces

**Depends-on:** none (file-disjoint from Tasks 1–4, 6–8; may parallel Task 5 after plugin exists is fine — no interface dependency)

- [ ] **Step 1: Failing drift test**

```python
class TestDRECParticipantSurfaces(unittest.TestCase):
    def test_DREC_10_1_through_10_8(self):
        """DREC-10.1 DREC-10.2 DREC-10.3 DREC-10.4 DREC-10.5 DREC-10.6 DREC-10.7 DREC-10.8"""
        index = (REPO / "docs/architecture/INDEX.md").read_text()
        artifacts = (REPO / "docs/architecture/artifacts.md").read_text()
        agents = (REPO / "AGENTS.md").read_text()
        using = (REPO / "skills/meta/using-skills/SKILL.md").read_text()

        self.assertIn("**ARCH-6**", index)
        self.assertRegex(index, r"mediat|never infer|CODEOWNERS|roster")

        # Three roles named in artifacts.md
        for role in ["skill-mediated", "external contributor", "accountable reviewer"]:
            self.assertRegex(artifacts, role, flags=re.I)

        # AGENTS carries runtime law (not a bare pointer only)
        self.assertIn("Participant boundary", agents)
        self.assertRegex(agents, r"mediat")
        # Guards: Iron Laws + orchestration still present
        self.assertIn("Four Iron Laws", agents)
        self.assertIn("Orchestration rule", agents)

        # using-skills smallest projection
        self.assertRegex(using, r"mediat|never infer|supplied", re.I)
        # Guards: subagent exemption + 1% rule unchanged
        self.assertIn("SUBAGENT-EXEMPT", using)
        self.assertIn("1% chance", using)

        # DREC-10.5: no full three-role narrative pasted into random skills
        # (spot-check brainstorm does not contain "accountable reviewer" narrative block)
```

- [ ] **Step 2: Write the four surfaces**

1. **ARCH-6** (one greppable sentence in INDEX.md invariants): skills MUST enforce and record only actions this skill set mediates; membership is never inferred from repository membership, roster, CODEOWNERS, branch ownership, PR authorship, or supplied artifacts.
2. **artifacts.md**: three-role narrative + external-contribution non-violation (absence of records/IDs/TDD reports is not a methodology violation for external contributors) — DREC-10.2, 10.6.
3. **AGENTS.md**: short "Participant boundary" subsection with the ratified runtime law semantically complete (DREC-10.3); place beside orchestration rules; do not edit Iron Laws body (DREC-10.8).
4. **using-skills**: exactly two sentences distilling never-infer + supplied-evidence-only (DREC-10.4); do not touch SUBAGENT-EXEMPT or 1% NON-NEGOTIABLE blocks (DREC-10.7).

- [ ] **Step 3: Commit**

`Implements: DREC-10.1, DREC-10.2, DREC-10.3, DREC-10.4, DREC-10.5, DREC-10.6, DREC-10.7, DREC-10.8`

_Requirements: DREC-10.1, DREC-10.2, DREC-10.3, DREC-10.4, DREC-10.5, DREC-10.6, DREC-10.7, DREC-10.8_

---

### Task 10: interpret upgrades

**Files:**
- Modify: `skills/discovery/interpret/SKILL.md`
- Modify: `tests/decision-records/scenarios.md` — §S-interpret
- Modify: `tests/decision-records/red-baselines.md` — §RED-interpret
- Modify: `tests/test_drec_doc_surfaces.py`
- Test: scenarios + `tests.test_drec_doc_surfaces`

**Reuse:** existing — extends interpret loop and "Maintain the thread" (design §17, rung 2)

**Interfaces:**
- Consumes: existing five-section loop
- Produces: ledger block; six claim labels; rationale rule; seven-label end-of-session digest; explicit read-only (no commits/records)

**Depends-on:** none (parallelizable with Tasks 1–9)

- [ ] **Step 1: RED baselines**

1. Ledger not rendered on decision events.
2. Claim labels missing / freeform.
3. Infers rationale from accepted recommendation.
4. Might emit/commit (read-only not explicit).

- [ ] **Step 2: Failing asserts**

```python
def test_DREC_12_interpret_doctrine(self):
    """DREC-12.1 DREC-12.2 DREC-12.3 DREC-12.4 DREC-12.5 DREC-12.6 DREC-12.7 DREC-12.8 DREC-12.9 DREC-12.10 DREC-12.11 DREC-12.12"""
    text = (REPO / "skills/discovery/interpret/SKILL.md").read_text()
    for label in [
        "Source claim", "Verified fact", "Inference", "Recommendation",
        "User decision", "Open question",
    ]:
        self.assertIn(label, text)
    for label in [
        "User decisions", "Human rationale", "Verified evidence",
        "Interpret analysis", "Open questions", "Prepared reply",
        "Transport-adoption status",
    ]:
        self.assertIn(label, text)
    self.assertIn("Decided", text)
    self.assertIn("Human rationale: not supplied", text)
    self.assertRegex(text, r"never infer.*rationale|never inferred", re.I)
    self.assertRegex(text, r"read-only|never committing|never.*emitting decision records", re.I)
    # Guards: five sections still named
    for n in ["1. Translate", "2. Simplify", "3. Feynman", "4. Independent analysis", "5. Prepare the reply"]:
        self.assertIn(n, text)
    self.assertIn("companion", text.lower())
```

- [ ] **Step 3: Patch interpret**

Add:

1. After any loop turn that contains a **decision event**, render a compact fenced ledger with lines `Decided` / `Open` / `Rejected-deferred` — only on decision events (DREC-12.1/12.2).
2. In section 4, require the six bold claim-label prefixes (DREC-12.3).
3. Rationale rule (DREC-12.4–12.7): when ≥2 live options, choice closed a branch/fixed a constraint, and no reason given → one short question; if already supplied → quote verbatim; if declined → `Human rationale: not supplied`; never infer from accepted recommendation.
4. New **End-of-session digest** section with exactly the seven provenance labels and transport-proves-adoption-not-authorship (DREC-12.8/12.9).
5. Explicit read-only: never commit, publish, or emit decision records (DREC-12.10).
6. Leave five-section order and companion framing intact (DREC-12.11/12.12). Keep `disable-model-invocation: true`.

- [ ] **Step 4: Commit**

`Implements: DREC-12.1, DREC-12.2, DREC-12.3, DREC-12.4, DREC-12.5, DREC-12.6, DREC-12.7, DREC-12.8, DREC-12.9, DREC-12.10, DREC-12.11, DREC-12.12`

_Requirements: DREC-12.1, DREC-12.2, DREC-12.3, DREC-12.4, DREC-12.5, DREC-12.6, DREC-12.7, DREC-12.8, DREC-12.9, DREC-12.10, DREC-12.11, DREC-12.12_

---

### Task 11: project.md Decision boundaries pin schema + discovery.md convention

**Files:**
- Modify: `templates/agents/project.md` — optional `## Decision boundaries` after Team / before Verify (or after Paths — prefer after Team, before Verify commands)
- Modify: `docs/agents/project.md` — same optional section (commented example or short documented empty form); do not invent pins for this repo unless desired
- Modify: `docs/architecture/artifacts.md` — spec-folder layout line for `discovery.md` + normative sentence (if not done in Task 9)
- Modify: `skills/ship/record-decision/SKILL.md` only if pin-read prose needs a template pointer tweak
- Modify: `tests/decision-records/scenarios.md` — §S-project-docs
- Modify: `tests/test_drec_doc_surfaces.py`
- Test: `tests.test_drec_doc_surfaces`

**Reuse:** existing — optional section pattern like posture/team (rung 2)

**Interfaces:**
- Consumes: design §15 table `| Action | Boundary-Type | Floor |`; design §18 discovery line
- Produces: documented pin schema; DREC-3.15/3.16 behavior already in record-decision remains authoritative

**Depends-on:** Task 5 (for pin-read doctrine consistency), Task 9 if artifacts.md already open

- [ ] **Step 1: Failing asserts**

```python
def test_DREC_3_15_3_16_pin_schema(self):
    """DREC-3.15 DREC-3.16"""
    tmpl = (REPO / "templates/agents/project.md").read_text()
    self.assertIn("## Decision boundaries", tmpl)
    self.assertIn("Boundary-Type", tmpl)
    self.assertIn("Floor", tmpl)

def test_DREC_13_1_13_2_discovery_convention(self):
    """DREC-13.1 DREC-13.2"""
    art = (REPO / "docs/architecture/artifacts.md").read_text()
    self.assertIn("discovery.md", art)
    self.assertRegex(art, r"non-normative|never required")
    self.assertRegex(art, r"requirements\.md.*sole normative|sole normative")
```

- [ ] **Step 2: Implement**

1. Template section:

```markdown
## Decision boundaries

Optional. When present, `record-decision` reads this table. Pins may raise a
floor or bind an action to a boundary type. An entry that would lower a core
floor is ignored with a one-line notice. Absent section → core table only.

| Action | Boundary-Type | Floor |
|---|---|---|
| <e.g. finish-branch:discard> | <disposal> | <Accountable> |
```

2. artifacts.md layout block: add `discovery.md  # optional, non-normative discovery handoff` plus sentence that requirements.md remains sole normative specification and discovery is never required.

3. Live `docs/agents/project.md`: add the section as documentation of the optional hook (may be empty table or omit rows) — additive only.

- [ ] **Step 3: Commit**

`Implements: DREC-3.15, DREC-3.16, DREC-13.1, DREC-13.2`

_Requirements: DREC-3.15, DREC-3.16, DREC-13.1, DREC-13.2_

---

### Task 12: Inventory alignment + full coverage gate

**Files:**
- Modify: `AGENTS.md` — Quick Reference ship row includes `record-decision` (m); skill count if stated; §3 model-invoked list mentions `record-decision` if that list is maintained
- Modify: `docs/architecture/skills.md` if it inventories ship skills
- Modify: `docs/architecture/workflows.md` — finish-branch line lists five outcomes (merge / PR / keep / discard / block)
- Modify: `skills/execution/execute-plan/SKILL.md` — any Done-when / menu inventory that still says four finish-branch outcomes → five (block included); no behavior change beyond inventory accuracy
- Modify: `tests/decision-records/scenarios.md` — §Coverage full ID list
- Test: coverage grep + full unittest + lints

**Reuse:** existing — TEAM Task 5 coverage gate pattern (rung 2)

**Interfaces:**
- Consumes: all prior tasks' footers and tagged tests
- Produces: zero missing DREC IDs in scenarios + unittest/scenario tags; green full suite; inventory surfaces agree on five-option menu + record-decision skill

**Depends-on:** Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7, Task 8, Task 9, Task 10, Task 11

- [ ] **Step 1: Coverage grep**

Every ID below MUST appear in `tests/decision-records/scenarios.md` **and** in at least one of: `tests/test_drec_validate_records.py`, `tests/test_drec_doc_surfaces.py`, or a scenario structural section:

```bash
ids=$(python3 - <<'PY'
import re
from pathlib import Path
text = Path("docs/specs/2026-07-24-decision-records/requirements.md").read_text()
print("\n".join(sorted(set(re.findall(r"\*\*(DREC-\d+\.\d+)\*\*", text)))))
PY
)
miss=0
for id in $ids; do
  rg -q "$id" tests/decision-records/scenarios.md || { echo "MISSING scenario: $id"; miss=1; }
  rg -q "$id" tests/test_drec_validate_records.py tests/test_drec_doc_surfaces.py \
    tests/decision-records/scenarios.md \
    || { echo "MISSING test tag: $id"; miss=1; }
done
test "$miss" -eq 0
```

Expect: zero MISSING. Fill any gap by tagging an existing test or adding a structural scenario bullet — do not invent new product behavior.

- [ ] **Step 2: Full verify**

```bash
python3 scripts/lint-skill-frontmatter.py
python3 scripts/lint-handoffs.py
python3 scripts/lint-context7.py
python3 -m unittest discover -s tests
# must list drec tests, not only lint/plugin:
python3 -m unittest discover -s tests -v 2>&1 | rg -c "test_DREC_|test_drec_" 
```

Expect: all pass, pristine output; discover runs DREC tests (count > 0).

- [ ] **Step 3: Inventory + AGENTS quick reference**

- Ship category lists `record-decision` (m) beside finish-branch / release.
- `workflows.md` and `execute-plan` inventory strings include **block** as the fifth finish-branch outcome.
- Confirm plugin manifest still matches `tests.test_plugin_manifest`.
- Confirm no root-level record template appeared.
- Do **not** flip design.md Status here — plan approval is a human gate before execute-plan.

- [ ] **Step 4: Commit**

Coverage/inventory-only commit. Trailers for any repaired IDs, else message notes coverage gate only.

_Requirements: DREC-1.1, DREC-1.2, DREC-1.3, DREC-1.4, DREC-1.5, DREC-1.6, DREC-1.7, DREC-1.8, DREC-2.1, DREC-2.2, DREC-2.3, DREC-2.4, DREC-2.5, DREC-2.6, DREC-2.7, DREC-2.8, DREC-2.9, DREC-3.1, DREC-3.2, DREC-3.3, DREC-3.4, DREC-3.5, DREC-3.6, DREC-3.7, DREC-3.8, DREC-3.9, DREC-3.10, DREC-3.11, DREC-3.12, DREC-3.13, DREC-3.14, DREC-3.15, DREC-3.16, DREC-3.17, DREC-3.18, DREC-3.19, DREC-3.20, DREC-4.1, DREC-4.2, DREC-4.3, DREC-4.4, DREC-4.5, DREC-4.6, DREC-5.1, DREC-5.2, DREC-5.3, DREC-5.4, DREC-5.5, DREC-5.6, DREC-5.7, DREC-5.8, DREC-5.9, DREC-5.10, DREC-5.11, DREC-6.1, DREC-6.2, DREC-6.3, DREC-6.4, DREC-6.5, DREC-6.6, DREC-6.7, DREC-6.8, DREC-6.9, DREC-6.10, DREC-6.11, DREC-6.12, DREC-6.13, DREC-6.14, DREC-7.1, DREC-7.2, DREC-7.3, DREC-7.4, DREC-7.5, DREC-7.6, DREC-8.1, DREC-8.2, DREC-8.3, DREC-8.4, DREC-8.5, DREC-8.6, DREC-9.1, DREC-9.2, DREC-9.3, DREC-9.4, DREC-9.5, DREC-9.6, DREC-9.7, DREC-9.8, DREC-9.9, DREC-10.1, DREC-10.2, DREC-10.3, DREC-10.4, DREC-10.5, DREC-10.6, DREC-10.7, DREC-10.8, DREC-11.1, DREC-11.2, DREC-11.3, DREC-11.4, DREC-11.5, DREC-11.6, DREC-11.7, DREC-11.8, DREC-11.9, DREC-11.10, DREC-11.11, DREC-11.12, DREC-11.13, DREC-11.14, DREC-11.15, DREC-11.16, DREC-11.17, DREC-11.18, DREC-11.19, DREC-11.20, DREC-11.21, DREC-11.22, DREC-11.23, DREC-11.24, DREC-12.1, DREC-12.2, DREC-12.3, DREC-12.4, DREC-12.5, DREC-12.6, DREC-12.7, DREC-12.8, DREC-12.9, DREC-12.10, DREC-12.11, DREC-12.12, DREC-13.1, DREC-13.2, DREC-14.1, DREC-14.2, DREC-15.1, DREC-15.2, DREC-15.3, DREC-15.4, DREC-15.5, DREC-15.6, DREC-15.7_

---

## Coverage and consistency notes (author)

| Requirement band | Task footer | Tagged test location |
|---|---|---|
| 1.1–1.2, 1.6–1.7, 2.2, 3.4, 4.4, 4.6, 5.1, 8.5, 11.2, 11.16, 11.23 | Task 1 | unittest + scenarios S-grammar |
| 1.4, 1.8, 2.1, 2.4–2.9, 8.1–8.2, 11.1, 14.2 | Task 2 | unittest fixtures |
| 11.3–11.15, 11.17–11.19, 11.22, 11.24 | Task 3 | `tests/test_drec_validate_records.py` |
| 5.10, 14.1 | Task 4 | scan unittest |
| 1.3, 1.5, 2.3, 3.1–3.3, 3.5–3.14, 3.17–3.20, 4.1–4.3, 4.5, 5.2–5.9, 5.11, 6.1–6.2, 6.11, 8.3–8.4, 8.6, 9.1–9.2, 9.4–9.9, 15.1–15.7 | Task 5 | scenarios + `test_drec_doc_surfaces` + red-baselines (§15 pressure) |
| 6.3–6.10, 6.12–6.14, 9.3 | Task 6 | scenarios + doc_surfaces (STOP/Red-flag rewrites explicit) |
| 7.1–7.6 | Task 7 | scenarios + doc_surfaces (reject insertion points explicit) |
| 11.10, 11.20–11.21 | Task 8 | doc_surfaces + 11.10 doctrine |
| 10.1–10.8 | Task 9 | four-surface drift unittest |
| 12.1–12.12 | Task 10 | doc_surfaces + scenarios |
| 3.15–3.16, 13.1–13.2 | Task 11 | doc_surfaces |
| All IDs | Task 12 | full grep gate + inventory (workflows/execute-plan five-option) |

**Parallelism:** Task 4 depends only on Task 1; Task 9 and Task 10 depend on none of the validator tasks; Task 8 depends on Task 3; Tasks 6–7 depend on Task 5; Task 11 depends on Task 5 (+ Task 9 if sharing artifacts.md).

**Seam-table reconciliation:** every ID in design "Seams for testing" is assigned to a tagged test above (validator CLI / --scan / scenarios / doc greps).

**Placeholder scan:** no TBD steps; field names frozen in Task 1 Interfaces.

**Plan-review fixes applied:** flat `tests/test_drec_*.py` (discoverable); substrate fixture paths only; DREC-11.10 warning-ceiling doctrine; finish-branch STOP/Red-flag rewrites; release-reject insertion points; §15 pressure REDs; inventory five-option surfaces.

**Upstream:** requirements.md unchanged (Approved). design.md remains the field dictionary; set its `Status: Approved` when **this plan** is approved (human gate — not Task 12).

**Issue tracker:** optional post-approval publish of tasks as GitHub issues is deferred until the user approves this plan.
