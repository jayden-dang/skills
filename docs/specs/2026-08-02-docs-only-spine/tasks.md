# Tasks: Docs-only spine

> **For agentic workers:** after plan approval, pick one execute skill —
> `build-in-waves` (subagent waves), `build-by-story` (human-gated story review
> units), or `build-inline` (controller implements, no implementer subagents).
> The chosen skill writes `Execution-mode:`. Steps use checkbox (`- [x]`) syntax
> for tracking.

Feature code: DOSP
Status: Implemented
Date: 2026-08-02
Approved: 2026-08-02 (user)
Execution-mode: continuous
Requirements: ./requirements.md
Design: ./design.md

**Goal:** Make vertical trace docs-only (no requirement IDs in code/commits), keep Spec review + path ownership, and add comment discipline across the pack.

**Architecture:** Reshape `audit-trace` (drop E2 + test greps); rewrite execute/plan/ship prompts and doctrine so IDs stay in `docs/specs/**`; changelog from specs; comment rules in implementer + polish-diff + guidelines. FSUB left alone. Verify with pack unit source-contracts (ARCH-3).

**Tech Stack:** Markdown skills; Python 3 unittest under `tests/`.

## Global Constraints

From `docs/agents/project.md`, `docs/product/guidelines.md`, `docs/architecture/INDEX.md`, and DOSP design.

| Check | Command |
|---|---|
| Lint | `python3 scripts/lint-skill-frontmatter.py && python3 scripts/lint-handoffs.py && python3 scripts/lint-context7.py` |
| Unit | `python3 -m unittest discover -s tests` |

Single test examples:

- `python3 -m unittest tests.test_dosp_docs_only_spine`
- `python3 -m unittest tests.test_audit-trace_scope`

**ARCH-1..6** apply. After Task 5, ARCH-4 means docs-side greppable citations only.

- No `skills/**/*.py`.
- No new consumer runtime tooling.
- **This feature’s own pack tests** may embed greppable `DOSP-N.M` tokens in test method names / docstrings / scenario markdown (product fixtures — DOSP-2.5). Do **not** teach consumer apps to do the same.
- **Commits for this plan:** conventional subjects only — **no** `Implements:` / `Guards:` trailers (DOSP-2.3; do not reintroduce them while implementing their removal).
- **Team:** Solo — no fake multi-assignee theater.
- Iron Laws unchanged: still TDD at agreed seams; tests prove behavior without requiring IDs in application source.

## File Structure

**Create:**

| File | Responsibility |
|---|---|
| `tests/test_dosp_docs_only_spine.py` | Source-contract unit tests for DOSP skill/doctrine edits |
| `tests/docs-only-spine/scenarios.md` | Greppable DOSP-N.M scenario tokens for pack fixtures |
| `tests/docs-only-spine/scenarios-pressure.md` | Pressure: fake ID only in code-like path must not E1; unknown task cite must E1 |

**Modify (by task):**

| File | Task |
|---|---|
| `skills/execution/audit-trace/SKILL.md` | 1 |
| `tests/test_audit-trace_scope.py` | 1 |
| `skills/spec/plan-tasks/SKILL.md` | 2 |
| `templates/tasks.md` | 2 |
| `skills/execution/test-first/SKILL.md` | 2 |
| `skills/execution/build-in-waves/implementer-prompt.md` | 2 |
| `skills/execution/build-in-waves/task-reviewer-prompt.md` | 2 |
| `skills/execution/build-by-story/**` (prompts/SKILL if they restate ID-in-test) | 2 |
| `skills/execution/build-inline/SKILL.md` | 2 |
| `skills/ship/package-change/SKILL.md` | 3 |
| `skills/ship/cut-release/SKILL.md` | 3 |
| `tests/package-change/scenarios.md` | 3 |
| `tests/package-change/scenarios-pressure.md` | 3 |
| `tests/test_prepare_change_contract.py` | 3 |
| `skills/review/polish-diff/SKILL.md` | 4 |
| `docs/product/guidelines.md` | 4 |
| `AGENTS.md` | 5 |
| `CONTEXT.md` | 5 |
| `docs/architecture/INDEX.md` | 5 |
| `docs/architecture/artifacts.md` | 5 |
| `docs/guide/concepts/requirement-ids.md` | 5 |
| `docs/guide/concepts/traceability.md` | 5 |
| `docs/guide/resources/scripts.md` | 5 |
| `docs/guide/examples/tier-*.md` | 5 |
| `docs/guide/process/**` (ID-in-code / Implements teaching) | 5 |
| `docs/guide/skills/**` (stubs that teach trailers/REQ tags) | 5 |
| `skills/setup/configure-repo/SKILL.md` | 5 |
| `templates/agents/project.md` | 5 |
| `docs/agents/project.md` | 5 |
| `skills/execution/prove-claim/SKILL.md` | 6 |
| `skills/track/realign-spec/SKILL.md` | 6 |
| `skills/track/amend-feature/SKILL.md` | 6 |
| `skills/ship/land-branch/SKILL.md` | 6 |
| `docs/guide/concepts/feature-graph.md` | 7 (cross-link only if needed) |

**Leave (guard):** `skills/execution/load-subgraph/**`, `skills/track/map-features/**` bodies — Task 7 verifies no functional change.

---

### Task 1: Docs-only audit-trace + scope contracts

**Files:**
- Create: `tests/test_dosp_docs_only_spine.py`
- Create: `tests/docs-only-spine/scenarios.md`
- Create: `tests/docs-only-spine/scenarios-pressure.md`
- Modify: `skills/execution/audit-trace/SKILL.md`
- Modify: `tests/test_audit-trace_scope.py`
- Test: `tests/test_dosp_docs_only_spine.py`, `tests/test_audit-trace_scope.py`

**Reuse:** rung 2 — design §1; pattern of `tests/test_audit-trace_scope.py` and IMPN source contracts

**Interfaces:**
- Consumes: none
- Produces: docs-only finding set (no E2); DOSP contract harness entry points other tasks extend

**Depends-on:** none

- [x] **Step 1: Write the failing tests**

In `tests/test_dosp_docs_only_spine.py` and/or `tests/test_audit-trace_scope.py`:

- Assert `skills/execution/audit-trace/SKILL.md` does **not** contain a test-coverage pass that greps application/test trees for IDs (no “test coverage” pass 4; no default roots like `crates` used for coverage).
- Assert finding table does **not** define **E2**.
- Assert E1 is described as task citations (and ARCH/decision as today), not union with test files.
- Assert frontmatter `description` does not say “covering test” as the purpose.
- Assert decision-record validator section still present.
- `scenarios.md` lists greppable tokens for DOSP-1.1 … DOSP-1.6, DOSP-6.3, DOSP-7.1, DOSP-7.2.
- Pressure: document that ID string only under a synthetic path outside `docs/specs` must not create E1; unknown ID on `_Requirements:` must.

Run: `python3 -m unittest tests.test_dosp_docs_only_spine tests.test_audit-trace_scope` — expect fail until skill body matches.

- [x] **Step 2: Implement** audit-trace reshape per design §1 (delete pass 4 + E2; rewrite E1, status table, NON-NEGOTIABLE, output example; update description; keep ARCH + decision passes). Update `test_audit-trace_scope.py` `AUDIT TRACE_FINDINGS` to drop E2.

Run: same unittest — expect pass.

- [x] **Step 3: Commit**

```bash
git add skills/execution/audit-trace/SKILL.md tests/test_audit-trace_scope.py tests/test_dosp_docs_only_spine.py tests/docs-only-spine/
git commit -m "$(cat <<'EOF'
feat(dosp): reshape audit-trace to docs-only vertical check

Drop E2 and test-tree greps; keep task/ARCH/decision integrity passes.
EOF
)"
```

_Requirements: DOSP-1.1, DOSP-1.2, DOSP-1.3, DOSP-1.4, DOSP-1.5, DOSP-1.6, DOSP-6.3, DOSP-7.1, DOSP-7.2_

---

### Task 2: Plan, TDD, and execute prompts — no ID-in-code

**Files:**
- Modify: `skills/spec/plan-tasks/SKILL.md`
- Modify: `templates/tasks.md`
- Modify: `skills/execution/test-first/SKILL.md`
- Modify: `skills/execution/build-in-waves/implementer-prompt.md`
- Modify: `skills/execution/build-in-waves/task-reviewer-prompt.md`
- Modify: `skills/execution/build-inline/SKILL.md`
- Modify: `skills/execution/build-by-story/SKILL.md` (and any sibling prompts that require test ID tags)
- Modify: `tests/test_dosp_docs_only_spine.py`
- Modify: `tests/docs-only-spine/scenarios.md`
- Test: `tests/test_dosp_docs_only_spine.py`

**Reuse:** rung 2 — design §2 (+ comment seeds for §4 in implementer)

**Interfaces:**
- Consumes: Task 1 contract harness
- Produces: plan/execute doctrine without mandatory test annotations or commit trailers

**Depends-on:** Task 1

- [x] **Step 1: Write the failing tests**

Assert source contracts:

- `plan-tasks/SKILL.md`: coverage check requires task footers; **no** “test annotation inside steps” / E2 freeroll language; **no** mandatory `Implements:` trailer in Steps recipe.
- `templates/tasks.md`: commit step example has **no** Implements trailer.
- `test-first/SKILL.md`: does not require every test to carry requirement ID via project.md annotation table as a hard gate (behavior tests at seams remain; pack-fixture exception may be noted).
- `implementer-prompt.md`: no “every test carries its requirement ID”; includes domain naming ban (no tables/modules named from feature codes); includes comment default-zero + forbidden list (DOSP-4.1/4.2).
- `task-reviewer-prompt.md`: Spec Compliance still walks requirement IDs vs diff; Quality axis does not require ID on each test.
- build-inline / build-by-story aligned (no trailer / no ID-in-test mandate).
- Scenario tokens: DOSP-2.1, DOSP-2.2, DOSP-3.1, DOSP-3.3, DOSP-4.1, DOSP-4.2, DOSP-6.2.

Run: unittest fail until edits.

- [x] **Step 2: Implement** all prompt/skill/template edits.

Run: `python3 -m unittest tests.test_dosp_docs_only_spine` — pass.

- [x] **Step 3: Commit**

```bash
git commit -m "$(cat <<'EOF'
feat(dosp): drop ID-in-test and trailer mandates from plan/execute

Spec review still walks requirement IDs; tests describe domain behavior.
EOF
)"
```

_Requirements: DOSP-2.1, DOSP-2.2, DOSP-3.1, DOSP-3.3, DOSP-4.1, DOSP-4.2, DOSP-6.2_

---

### Task 3: Ship path — package-change and cut-release without trailers

**Files:**
- Modify: `skills/ship/package-change/SKILL.md`
- Modify: `skills/ship/cut-release/SKILL.md`
- Modify: `tests/package-change/scenarios.md`
- Modify: `tests/package-change/scenarios-pressure.md`
- Modify: `tests/test_prepare_change_contract.py`
- Modify: `tests/test_dosp_docs_only_spine.py`
- Modify: `tests/docs-only-spine/scenarios.md`
- Test: `tests/test_prepare_change_contract.py`, `tests/test_dosp_docs_only_spine.py`

**Reuse:** rung 2 — design §3

**Interfaces:**
- Consumes: none from Task 2 interfaces (file-disjoint from Task 2 skill paths except shared test harness)
- Produces: trailer-free package/cut-release procedures

**Depends-on:** Task 1

- [x] **Step 1: Write the failing tests**

- `package-change` no longer requires/preserves `Implements:` / `Guards:` as the home for IDs; rationalization table updated.
- `cut-release` derives changelog from `docs/specs/**` (Status + requirement prose / tasks), not trailer parse.
- Update PCHG scenarios/pressure that force “ID only in Implements trailers” → “IDs only in specs/process artifacts, never commits”.
- `test_prepare_change_contract.py` must not assert mandatory `Implements:` in skill body.
- Tokens: DOSP-2.3, DOSP-2.4.

Run: fail until edits.

- [x] **Step 2: Implement** package-change + cut-release + test/scenario updates.

Run:

```bash
python3 -m unittest tests.test_prepare_change_contract tests.test_dosp_docs_only_spine
```

expect pass.

- [x] **Step 3: Commit**

```bash
git commit -m "$(cat <<'EOF'
feat(dosp): remove Implements/Guards trailers from package and release

Changelog groups from specs and commit subjects, not ID trailers.
EOF
)"
```

_Requirements: DOSP-2.3, DOSP-2.4_

---

### Task 4: Comment discipline in polish-diff and guidelines

**Files:**
- Modify: `skills/review/polish-diff/SKILL.md`
- Modify: `docs/product/guidelines.md`
- Modify: `tests/test_dosp_docs_only_spine.py`
- Modify: `tests/docs-only-spine/scenarios.md`
- Test: `tests/test_dosp_docs_only_spine.py`

**Reuse:** rung 2 — design §4 (implementer already seeded in Task 2)

**Interfaces:**
- Consumes: implementer comment rules from Task 2
- Produces: polish-diff step + guidelines bullets

**Depends-on:** Task 2

- [x] **Step 1: Write the failing tests**

- `polish-diff/SKILL.md` has an explicit step to strip/flag narrating and process comments (forbidden list), preserve hazard/invariant comments.
- `docs/product/guidelines.md` Coding standards (or House rules) state default-zero comments + allowed/forbidden classes.
- Tokens: DOSP-4.3, DOSP-4.4.

Run: fail until edits.

- [x] **Step 2: Implement** polish-diff + guidelines.

Run: `python3 -m unittest tests.test_dosp_docs_only_spine` — pass.

- [x] **Step 3: Commit**

```bash
git commit -m "$(cat <<'EOF'
feat(dosp): enforce comment discipline in polish-diff and guidelines

Default zero comments; keep only hazard/invariant/why notes.
EOF
)"
```

_Requirements: DOSP-4.3, DOSP-4.4_

---

### Task 5: Doctrine surface — AGENTS, ARCH, guide, configure-repo

**Files:**
- Modify: `AGENTS.md`
- Modify: `CONTEXT.md`
- Modify: `docs/architecture/INDEX.md`
- Modify: `docs/architecture/artifacts.md`
- Modify: `docs/guide/concepts/requirement-ids.md`
- Modify: `docs/guide/concepts/traceability.md`
- Modify: `docs/guide/resources/scripts.md`
- Modify: `docs/guide/examples/tier-0-tweak.md`
- Modify: `docs/guide/examples/tier-1-bugfix.md`
- Modify: `docs/guide/examples/tier-2-feature.md`
- Modify: `docs/guide/process/execution.md`
- Modify: `docs/guide/process/specification.md`
- Modify: `docs/guide/process/ship-and-maintain.md`
- Modify: `docs/guide/process/review-and-acceptance.md`
- Modify: `docs/guide/resources/templates.md`
- Modify: `docs/guide/resources/adopting.md` (if it teaches annotations)
- Modify: `docs/guide/skills/audit-trace.md` (if present)
- Modify: `docs/guide/skills/plan-tasks.md` (if present)
- Modify: `docs/guide/skills/package-change.md` (if present)
- Modify: `docs/guide/skills/configure-repo.md` (if present)
- Modify: `skills/setup/configure-repo/SKILL.md`
- Modify: `templates/agents/project.md`
- Modify: `docs/agents/project.md`
- Modify: `tests/test_dosp_docs_only_spine.py`
- Modify: `tests/docs-only-spine/scenarios.md`
- Test: `tests/test_dosp_docs_only_spine.py`

**Reuse:** rung 2 — design §5

**Interfaces:**
- Consumes: docs-only semantics from Task 1
- Produces: pack-wide doctrine aligned with DOSP

**Depends-on:** Task 1

- [x] **Step 1: Write the failing tests**

- `AGENTS.md` spine table: no required Playwright/Vitest/Rust REQ annotation rows; no required Implements trailer row; keep requirements/design/tasks citations; note pack-fixture exception if needed.
- `docs/architecture/INDEX.md` ARCH-4: docs-side citations only (strike obsolete test/trailer clause).
- `CONTEXT.md` Requirement ID: not “must flow through tests and commits”.
- `configure-repo` + `templates/agents/project.md` + `docs/agents/project.md`: no mandatory Test annotation conventions for code-side audit-trace; drop test-glob-as-coverage instructions; optional legacy-ignore note OK.
- Guide concept pages + examples + process: no teaching Implements trailers or required `/// REQ` / test tags as current practice (legacy callouts OK if explicit “retired”).
- Tokens: DOSP-2.5, DOSP-5.1, DOSP-5.2, DOSP-5.3, DOSP-5.4, DOSP-5.5, DOSP-5.6.

Run: fail until edits.

- [x] **Step 2: Implement** all doctrine files. Grep `docs/guide` for `Implements:` and `/// REQ` — only allow explicit legacy/history callouts.

Run:

```bash
python3 -m unittest tests.test_dosp_docs_only_spine
python3 scripts/lint-skill-frontmatter.py && python3 scripts/lint-handoffs.py && python3 scripts/lint-context7.py
```

expect pass.

- [x] **Step 3: Commit**

```bash
git commit -m "$(cat <<'EOF'
docs(dosp): rewrite AGENTS, ARCH-4, guide, and configure-repo for docs-only IDs

Requirement IDs stay in the triad; code and commits stay domain language.
EOF
)"
```

_Requirements: DOSP-2.5, DOSP-5.1, DOSP-5.2, DOSP-5.3, DOSP-5.4, DOSP-5.5, DOSP-5.6_

---

### Task 6: prove-claim, realign-spec, land/amend without E2

**Files:**
- Modify: `skills/execution/prove-claim/SKILL.md`
- Modify: `skills/track/realign-spec/SKILL.md`
- Modify: `skills/track/amend-feature/SKILL.md`
- Modify: `skills/ship/land-branch/SKILL.md`
- Modify: `tests/test_dosp_docs_only_spine.py`
- Modify: `tests/docs-only-spine/scenarios.md`
- Test: `tests/test_dosp_docs_only_spine.py`

**Reuse:** rung 2 — design §6

**Interfaces:**
- Consumes: docs-only audit-trace from Task 1
- Produces: Implemented evidence + “requirements met” without E2

**Depends-on:** Task 1

- [x] **Step 1: Write the failing tests**

- `prove-claim`: “requirements met” still requires audit-trace clean + criteria vs observed behavior; does **not** require test-file ID presence / E2.
- `realign-spec`: Approved→Implemented uses tasks checked + docs-only audit-trace zero errors + verify green — **not** “every live requirement covered by a test string”.
- `amend-feature` / `land-branch`: no “ID traces end to end into test tags/trailers” language; still may require audit-trace clean.
- Tokens: DOSP-3.2, DOSP-3.4.

Run: fail until edits.

- [x] **Step 2: Implement** skill body updates.

Run: `python3 -m unittest tests.test_dosp_docs_only_spine` — pass.

- [x] **Step 3: Commit**

```bash
git commit -m "$(cat <<'EOF'
feat(dosp): align prove-claim and realign-spec with docs-only coverage

Implemented no longer depends on grepping IDs out of test files.
EOF
)"
```

_Requirements: DOSP-3.2, DOSP-3.4_

---

### Task 7: FSUB leave-guard, residual greps, full suite green

**Files:**
- Modify: `tests/test_dosp_docs_only_spine.py`
- Modify: `tests/docs-only-spine/scenarios.md`
- Modify: `docs/guide/concepts/feature-graph.md` (only if a single cross-link sentence is required; else no edit)
- Test: full unit suite + lints

**Reuse:** rung 2 — design §7

**Interfaces:**
- Consumes: all prior task contracts
- Produces: green pack gate for DOSP

**Depends-on:** Task 1, Task 2, Task 3, Task 4, Task 5, Task 6

- [x] **Step 1: Write the failing tests**

- Assert `skills/execution/load-subgraph/SKILL.md` still model-invoked and does not require code-side IDs (smoke: skill exists; optional: no new “must annotate tests” language introduced).
- Assert all live DOSP requirement IDs from `requirements.md` appear in `tests/docs-only-spine/scenarios.md` (footer coverage for pack fixtures).
- Optional: `git diff` against baseline of load-subgraph dir is empty or whitespace-only — if any edit was accidental, revert.

Run: fail if scenarios incomplete.

- [x] **Step 2: Implement** scenario completeness; fix any residual teaching strings found by grepping skills for mandatory Implements trailer / “covering test” E2.

Run full gate:

```bash
python3 scripts/lint-skill-frontmatter.py && python3 scripts/lint-handoffs.py && python3 scripts/lint-context7.py
python3 -m unittest discover -s tests
```

expect pass (pristine).

- [x] **Step 3: Commit**

```bash
git commit -m "$(cat <<'EOF'
test(dosp): close scenarios and verify full suite after docs-only spine

Confirm load-subgraph left intact; all DOSP IDs covered in fixtures.
EOF
)"
```

_Requirements: DOSP-6.1_

---

## Coverage map

| IDs | Task |
|---|---|
| DOSP-1.1–1.6, 6.3, 7.1–7.2 | Task 1 |
| DOSP-2.1–2.2, 3.1, 3.3, 4.1–4.2, 6.2 | Task 2 |
| DOSP-2.3–2.4 | Task 3 |
| DOSP-4.3–4.4 | Task 4 |
| DOSP-2.5, 5.1–5.6 | Task 5 |
| DOSP-3.2, 3.4 | Task 6 |
| DOSP-6.1 | Task 7 |

Every Approved live ID appears in exactly one task footer above. Pack fixture scenarios embed the same IDs (DOSP-2.5) — **not** as a consumer code annotation convention.

## Notes for implementers (plan-quality)

- When editing `plan-tasks` itself (Task 2), do **not** leave the old E2 / Implements language in place “for this repo only.”
- Parallelism: Task 3 and Task 6 only depend on Task 1 (can wave with each other after Task 1); Task 2 before Task 4; Task 5 depends on Task 1 only but will conflict with Task 2/3 if both edit AGENTS — **Task 5 may touch AGENTS/guide while Task 2 touches skills** — file-disjoint OK. If Task 5 and Task 2 both need `docs/guide/skills/*`, serialize: Task 5 after Task 2 or assign guide skill stubs only in Task 5.
- Task 2 lists build-by-story SKILL only if it currently mandates trailers/ID tags; if not, leave unchanged and assert in test.

## Exit

Present this file and **STOP** for approval.

On approval: set `Status: Approved`, leave `Execution-mode: unset`, offer:

| Route | Skill |
|---|---|
| Subagent waves | `build-in-waves` |
| Story-gated units | `build-by-story` |
| Controller implements | `build-inline` |
