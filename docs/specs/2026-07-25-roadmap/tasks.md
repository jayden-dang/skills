# Tasks: Roadmap layer

> **For agentic workers:** REQUIRED SUB-SKILL: use `build-in-waves` to implement
> this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

Feature code: RMAP
Status: Implemented
Date: 2026-07-25
Requirements: ./requirements.md
Design: ./design.md

**Goal:** Add the program band — `plan-milestones` authors milestone intent in
`docs/roadmap/INDEX.md`; `refresh-roadmap-status` derives roadmap health read-only and
recommends one next action.

**Architecture:** One new durable artifact (`docs/roadmap/INDEX.md`, from a new
template whose comment block holds the authoritative structural rules S1–S7), one
model-invocable authoring skill in `skills/project/`, one user-invoked derivation
skill in `skills/track/` shaped as `audit-trace` for the horizontal layer (fixed passes →
finding codes R1–R11 → set-difference rules → a ten-row priority ladder). Three
existing skills gain one edit each: `frame-change` persists its decomposition,
`specify-behavior` writes the `ROAD-N` binding column, `define-project` gives
vision goals `GOAL-N` IDs.

**Tech Stack:** Markdown skills and templates. Python 3 `unittest` under `tests/`
for the deterministic rule tests; scenario markdown under `tests/roadmap/` for
behavior coverage. No runtime dependencies — the skills are markdown only.

## Global Constraints

Every task's requirements implicitly include this section.

**verify commands — run in this order; all must pass before any completion claim**
(from `docs/agents/project.md`):

| Check | Command |
|---|---|
| Lint | `python3 scripts/lint-skill-frontmatter.py && python3 scripts/lint-handoffs.py && python3 scripts/lint-context7.py` |
| Unit tests | `python3 -m unittest discover -s tests` |

Single test file: `python3 -m unittest tests.<module>`

**Test annotation conventions** (from `docs/agents/project.md`):

| Layer | Requirement-ID convention |
|---|---|
| Unit (`unittest` under `tests/`) | Requirement ID in the test method name or first-line docstring as greppable `RMAP-N.M` |
| Scenario / acceptance markdown | Greppable bare `RMAP-N.M` tokens in the scenario file |

Use the **docstring** form for Python: `audit-trace`'s coverage pass matches
`[A-Z][A-Z0-9]{1,11}-[0-9]+(\.[0-9]+)+`, which a method name like
`test_RMAP_1_2` cannot satisfy.

**Existing test-tree convention** (declared by `docs/agents/project.md`'s Audit Trace-ignore
list): per-area directory holding `scenarios.md` (coverage tokens),
`red-baselines.md` (recorded RED failures — ignore-listed, its IDs are baseline
records not coverage), and `fixtures/` (ignore-listed, its IDs are data). Follow it:
this feature's area is `tests/roadmap/`.

**Engineering rules copied verbatim from `docs/product/guidelines.md`:**

- Skill bodies: imperative voice; hard gates in dedicated blocks; rationalization tables in `| Thought | Reality |` form.
- SKILL.md under 500 lines (prefer under 300); split implementer/reviewer prompts into sibling files when needed.
- Python linters for this repo only: frontmatter parse safety, dead handoffs to user-invoked skills, Context7 references on library-reasoning skills.
- No production app code in this repository — content is skills, templates, hooks, and docs.
- Deterministic checks driven by an LLM (fixed `grep`/`git` under a precise skill) are a first-class form — do not replace them with freeform judgment when a set-difference will do.
- Skills: verb-first kebab-case (`specify-behavior`, `build-in-waves`).
- Cross-skill references use `REQUIRED SUB-SKILL:` prose, never `@`-links.
- Skill `description` frontmatter states triggering conditions only — never summarize the workflow.
- Additive edits to consumer-facing config: never clobber existing user content when writing templates.
- Iron Law gates (NO-CODE, TEST-FIRST, ROOT-CAUSE, EVIDENCE) are not weakened by workflow band, ceremony tier, or convenience.

**Architecture invariants this feature inherits** (from `docs/architecture/INDEX.md`;
every task is bound by them):

- **ARCH-1** Audit Trace and other vertical checks MUST be exact `grep`/`git`/file-read passes with fixed extraction rules and set differences — never an LLM judgment of whether a test "really" covers an ID.
- **ARCH-2** Optional project layers and config sections MUST no-op when absent: skills CONTINUES TO run without inventing vision, architecture invariants, team roster, or other standing facts that were never written.
- **ARCH-3** Consumer-repo adoption MUST require only the skills (plugin or npx) and markdown config — never mandate Python, vendored linters, CI jobs, or git-hook wiring for the full methodology; any hard headless gate is an optional documented add-on only.
- **ARCH-4** Requirement IDs (`CODE-N.M`) and architecture IDs (`ARCH-N`) are immutable once defined: never renumber or reuse; retire only by strikethrough; every task, test, commit trailer, and `Respects:` line MUST use the same greppable string as the definition.
- **ARCH-5** User-invoked skills may invoke model-invoked skills only; model-invoked skills must never invoke user-invoked skills; agents must never auto-invoke a skill marked `disable-model-invocation: true`.
- **ARCH-6** Skills MUST enforce and record only actions this skill set mediates; membership is never inferred from repository membership, roster, CODEOWNERS, branch ownership, PR authorship, or supplied artifacts.

**ARCH-4 does not extend to `GOAL-N`, `MILE-N`, or `ROAD-N`.** Their stability is a
skill-local rule (RMAP-1.11, RMAP-2.9). Do not cite ARCH-4 for them and do not add a
new invariant.

**Skill-authoring tasks read `docs/specs/2026-07-25-roadmap/design.md`** for the
authoritative S1–S7 rule list, the R1–R11 finding table, the six pass recipes, and
the ten-row priority ladder. Those tables are the single source of truth — transcribe
them, do not re-derive them.

**Skill TDD is mandatory and is the Iron Law of `author-skills`:** no new skill and
no edit to a skill ships without a failing test first. RED means running the scenario
*without* the skill (for an edit, with the current version) and recording the failures
and rationalizations **verbatim** into `tests/roadmap/red-baselines.md`. A baseline
that does not fail means there is nothing to write — stop and report it.

**Do not batch-create skills.** Finish, test, and validate one skill completely before
starting the next. Task order below is the approved sequence.

**Team band: Solo** (derived, headcount 1, from `docs/agents/project.md`). Lean
peer-coordination language; do not invent reviewers or assignees. Gates unchanged.

## File Structure

**Create**

| Path | Responsibility |
|---|---|
| `templates/roadmap-INDEX.md` | Roadmap artifact template; its comment block is the authoritative S1–S7 structural rule list |
| `skills/project/plan-milestones/SKILL.md` | Model-invocable authoring skill: create/update modes, decomposition discipline, structural gate |
| `skills/track/refresh-roadmap-status/SKILL.md` | User-invoked derivation skill: six passes, R1–R11, priority ladder, standup mode |
| `docs/guide/skills/plan-milestones.md` | Human documentation page |
| `docs/guide/skills/refresh-roadmap-status.md` | Human documentation page |
| `tests/roadmap/red-baselines.md` | Recorded RED failures per skill task (Audit Trace-ignored) |
| `tests/roadmap/scenarios-plan-milestones.md` | Behavior coverage tokens for the authoring skill |
| `tests/roadmap/scenarios-frame-change.md` | Behavior coverage tokens for the decomposition write-handoff |
| `tests/roadmap/scenarios-binding.md` | Behavior coverage tokens for the binding column |
| `tests/roadmap/scenarios-vision.md` | Behavior coverage tokens for `GOAL-N` authoring and migration |
| `tests/roadmap/scenarios-refresh-roadmap-status.md` | Behavior coverage tokens for derivation, safety, standup |
| `tests/roadmap/fixtures/` | Fixture roadmaps: clean, one per S-defect, premature closure, status mismatch, duplicate goal (Audit Trace-ignored) |
| `tests/roadmap/fixtures/scale/` | 200-feature / 50-milestone scale fixture (Audit Trace-ignored) |
| `tests/test_roadmap_template.py` | Template required-slot contract |
| `tests/test_check_roadmap_rules.py` | R1–R11 rule application over fixtures |
| `tests/test_priority_ladder.py` | State → recommendation table |
| `tests/test_check_roadmap_scale.py` | Bounded-pass budget at scale |
| `tests/test_trace_scope.py` | Guard: `audit-trace` still covers `CODE-N.M` and `ARCH-N` only |

**Modify**

| Path | Change |
|---|---|
| `skills/discovery/frame-change/SKILL.md` | Step 5/6: persist a multi-subsystem decomposition through `plan-milestones` before the first item continues |
| `skills/spec/specify-behavior/SKILL.md` | Step 1: record the item's `ROAD-N` in the new INDEX column |
| `skills/project/define-project/SKILL.md` | Step 3 + Update: `GOAL-N` IDs, and the un-IDed migration |
| `templates/specs-INDEX.md` | Add the `Roadmap item` column |
| `templates/product-vision.md` | `## Goals` becomes bold-IDed `**GOAL-N**` |
| `docs/product/vision.md` | Migrate this repo's own goals to `GOAL-N` |
| `docs/specs/INDEX.md` | Add the column; bind `RMAP` once a roadmap exists here |
| `docs/guide/concepts/artifacts.md` | Stale four-column INDEX table |
| `docs/guide/concepts/feature-graph.md` | Stale four-column INDEX table (lines 42-46) |
| `AGENTS.md` | §3 invocation lists, §8 file organization, §11 table and main flow; fix the 42/43 count drift to 45 |
| `skills/meta/ask-me-bro/SKILL.md` | Name `/refresh-roadmap-status` in the user-invoked list and add a roadmap on-ramp |
| `docs/guide/skills/README.md` | Count and the two new entries |
| `docs/agents/project.md` | Test globs: declare the scenario-markdown include; add this feature's fixtures and `red-baselines.md` to Audit Trace ignore |

A file not in this map should not be touched by any task.

---

### Task 1: Roadmap artifact template

**Files:**
- Create: `templates/roadmap-INDEX.md`
- Create: `tests/test_roadmap_template.py`

**Reuse:** existing — `templates/architecture-INDEX.md` (rung 2): summary table + per-item block + a comment block carrying ID grammar and stability rules, transcribed from `design.md`'s "The roadmap artifact and its template" section.

**Interfaces:**
- Consumes: nothing.
- Produces: the slot names `**Outcome:**`, `**Goals:**`, `**Members:**`, `Surfaces:`, `**Depends-on:**`, `**Commitment:**`, `**Closed:**`, `**Deferred:**`, `**Blockers:**`, `## Goal dispositions`, the top-level `Status:` field, and the rule tokens `S1`–`S7` — all consumed by Tasks 2 and 6.

**Depends-on:** none

- [x] **Step 1: Write the failing test**

```python
"""Roadmap template slot contract."""
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TEMPLATE = REPO / "templates" / "roadmap-INDEX.md"

SLOTS = [
    "Status:",
    "**Outcome:**",
    "**Goals:**",
    "**Members:**",
    "Surfaces:",
    "**Depends-on:**",
    "**Commitment:**",
    "**Closed:**",
    "**Deferred:**",
    "**Blockers:**",
    "## Goal dispositions",
]


class RoadmapTemplateSlots(unittest.TestCase):
    def test_template_exists_with_status_field(self):
        """RMAP-1.1 RMAP-1.16 — the template exists and carries a top-level Status field."""
        self.assertTrue(TEMPLATE.is_file(), f"missing {TEMPLATE}")
        self.assertRegex(TEMPLATE.read_text(), r"(?m)^Status: Draft$")

    def test_every_required_slot_present(self):
        """RMAP-1.2 RMAP-1.3 RMAP-1.15 RMAP-1.20 — milestone, item, disposition and surface slots."""
        text = TEMPLATE.read_text()
        missing = [s for s in SLOTS if s not in text]
        self.assertEqual([], missing, f"template is missing slots: {missing}")

    def test_structural_rule_block_is_complete(self):
        """RMAP-1.2 — the comment block defines S1 through S7 as the authoritative rule list."""
        text = TEMPLATE.read_text()
        missing = [f"S{n}" for n in range(1, 8) if f"S{n}" not in text]
        self.assertEqual([], missing, f"rule block is missing: {missing}")


if __name__ == "__main__":
    unittest.main()
```

Run: `python3 -m unittest tests.test_roadmap_template` — expect: `ModuleNotFoundError` or three failures on the missing template.

- [x] **Step 2: Implement**

Create `templates/roadmap-INDEX.md` exactly as specified in `design.md` §"The roadmap
artifact and its template", including the `S1`–`S7` comment block verbatim and the
retirement rule (`~~**MILE-3**~~ superseded by MILE-5`; never renumber, never reuse;
a `ROAD-N` keeps its ID across a milestone move).

Run: `python3 -m unittest tests.test_roadmap_template` — expect: pass.

- [x] **Step 3: Full prove-claim and commit**

Run: `python3 scripts/lint-skill-frontmatter.py && python3 scripts/lint-handoffs.py && python3 scripts/lint-context7.py && python3 -m unittest discover -s tests` — expect: pass, output pristine.

`git commit -m "feat(roadmap): add roadmap artifact template with S1-S7 rule block" # trailer: Implements: RMAP-1.1`

_Requirements: RMAP-1.1, RMAP-1.2, RMAP-1.3, RMAP-1.15, RMAP-1.16, RMAP-1.20_

---

### Task 2: `plan-milestones` skill

**Files:**
- Create: `skills/project/plan-milestones/SKILL.md`
- Create: `docs/guide/skills/plan-milestones.md`
- Create: `tests/roadmap/scenarios-plan-milestones.md`
- Create: `tests/roadmap/red-baselines.md`
- Modify: `AGENTS.md` (§3 model-invoked list, §8 tree, §11 table and main flow, count → 45)
- Modify: `docs/guide/skills/README.md` (count and entry)

**Reuse:** existing — `skills/project/define-project/SKILL.md`'s create/update mode split and `skills/spec/specify-behavior/SKILL.md`'s present-the-file-and-STOP gate (rung 2).

**Interfaces:**
- Consumes: Task 1's slot names and `S1`–`S7` tokens.
- Produces: the skill name `plan-milestones` (model-invocable, no `disable-model-invocation`), reached by Task 3's handoff; and `docs/roadmap/INDEX.md` as a written artifact for Task 6 to read.

**Depends-on:** Task 1

- [x] **Step 1: Write the failing test — RED baseline**

Author `tests/roadmap/scenarios-plan-milestones.md` with one scenario per behavior,
each carrying its bare ID token: deferral records date and reason
(`RMAP-1.7`), goal citation present / `None` without a vision (`RMAP-1.8`,
`RMAP-1.9`), `Closed:` records the tag (`RMAP-1.10`), retirement by strikethrough
(`RMAP-1.11`), ID survives a milestone move (`RMAP-1.12`), model-invocable
frontmatter (`RMAP-1.13`), `docs/specs/INDEX.md` untouched (`RMAP-1.14`), present-and-STOP
gate (`RMAP-1.17`), each S-defect withholds the gate (`RMAP-1.18`), material change
demotes to `Draft` and re-enters the gate (`RMAP-1.19`), items identified by `ROAD-N`
and slug only (`RMAP-1.4`).

Run each scenario against a fresh agent with **no** `plan-milestones` skill present.
Record every failure and rationalization verbatim in `tests/roadmap/red-baselines.md`.

Expect: the baseline agent invents its own roadmap shape, skips the approval gate, and
renumbers freely. If any scenario passes without the skill, delete it — there is
nothing to fix there.

- [x] **Step 2: Implement**

Write `skills/project/plan-milestones/SKILL.md`: frontmatter with a trigger-and-outcome
`description` naming the `docs/roadmap/INDEX.md` deliverable and **no**
`disable-model-invocation`; Create and Update modes; the decomposition discipline as
positive rules (user-value grouping, standalone-and-enabling, `Surfaces:` overlap
consolidation, fewer-and-larger when settled); the structural gate over `S1`–`S7`; and
an exit that **names** `/refresh-roadmap-status` for the user rather than invoking it. Body under
300 lines; move the decomposition discipline to a sibling reference file if it pushes past
that.

Register in `AGENTS.md` §3/§8/§11 and `docs/guide/skills/README.md`; write the guide page.

Run each scenario again with the skill present — expect compliance. Then REFACTOR: capture
each new rationalization verbatim, add an explicit counter, re-run until none appear.

Run: `python3 scripts/lint-skill-frontmatter.py && python3 scripts/lint-handoffs.py && python3 scripts/lint-context7.py && python3 -m unittest discover -s tests` — expect: pass.

- [x] **Step 3: Commit**

`git commit -m "feat(roadmap): add plan-milestones authoring skill with approval gate" # trailer: Implements: RMAP-1.4`

_Requirements: RMAP-1.4, RMAP-1.7, RMAP-1.8, RMAP-1.9, RMAP-1.10, RMAP-1.11, RMAP-1.12, RMAP-1.13, RMAP-1.14, RMAP-1.17, RMAP-1.18, RMAP-1.19_

---

### Task 3: `frame-change` persists the decomposition

**Files:**
- Modify: `skills/discovery/frame-change/SKILL.md` (step 5 at line 115, step 6 at lines 119-124)
- Create: `tests/roadmap/scenarios-frame-change.md`

**Reuse:** existing — the `REQUIRED SUB-SKILL:` prose mechanism already used at `frame-change/SKILL.md:74,78,90,91,121,122` (rung 2).

**Interfaces:**
- Consumes: the model-invocable skill name `plan-milestones` from Task 2.
- Produces: nothing downstream tasks consume.

**Depends-on:** Task 2

- [x] **Step 1: Write the failing test — RED baseline**

Author `tests/roadmap/scenarios-frame-change.md`: a multi-subsystem request that must
persist its decomposition (`RMAP-2.1`), a second one against an existing roadmap that
must append `ROAD-N` items rather than start fresh (`RMAP-2.2`), and a
single-subsystem request that must reach `specify-behavior` or `test-first` with no roadmap
authored (`RMAP-2.3`).

Run against the **current** `frame-change`. Append failures verbatim to
`tests/roadmap/red-baselines.md`. Expect: the decomposition is named in conversation and
never written down.

- [x] **Step 2: Implement**

Add one conditional to step 5: when the decomposition names two or more independent
sub-features, `REQUIRED SUB-SKILL: use \`plan-milestones\`` to persist them as `ROAD-N`
items — appending to an existing roadmap when one exists — before step 6 continues the
first item. Leave step 6's existing exits unchanged.

Run the scenarios — expect compliance, including the single-subsystem case taking the
unchanged path. REFACTOR against new rationalizations.

Run: full prove-claim — expect pass.

- [x] **Step 3: Commit**

`git commit -m "feat(roadmap): persist frame-change decomposition through plan-milestones" # trailer: Implements: RMAP-2.1`

_Requirements: RMAP-2.1, RMAP-2.2, RMAP-2.3_

---

### Task 4: `Roadmap item` binding column

**Files:**
- Modify: `templates/specs-INDEX.md`
- Modify: `skills/spec/specify-behavior/SKILL.md` (Step 1, lines 39-44)
- Modify: `docs/specs/INDEX.md`
- Modify: `docs/guide/concepts/artifacts.md`
- Modify: `docs/guide/concepts/feature-graph.md` (lines 42-46)
- Create: `tests/roadmap/scenarios-binding.md`

**Reuse:** existing — extends `specify-behavior` Step 1's INDEX row write, already the sole registration point (rung 2).

**Interfaces:**
- Consumes: nothing.
- Produces: the column header `Roadmap item` and the cell grammar (`ROAD-N` or empty) — consumed by Task 6's pass 4.

**Depends-on:** none

- [x] **Step 1: Write the failing test — RED baseline**

Author `tests/roadmap/scenarios-binding.md`: registering a feature that implements a
roadmap item records its `ROAD-N` (`RMAP-2.4`); registering with no roadmap present
leaves the column empty and changes nothing else (`RMAP-2.5`); registration ownership,
code uniqueness, and the `Draft` initial status are unchanged (`RMAP-2.6`).

Run against the **current** `specify-behavior`. Append failures verbatim to
`red-baselines.md`. Expect: no column exists, so no binding is recorded.

- [x] **Step 2: Implement**

Add the fifth column to `templates/specs-INDEX.md` and to `docs/specs/INDEX.md`. Add one
sentence to `specify-behavior` Step 1: record the implemented item's `ROAD-N` in that
column; with no roadmap, leave it empty and register unchanged (ARCH-2). Update the two
guide docs that copy the four-column table.

Verify the negative: no skill parses the table by column position — `frame-change` step 1,
`realign-spec`, `plan-tasks`'s status confirmation, and the feature-overlap search all read
the `Status` cell semantically.

Run: full prove-claim — expect pass.

- [x] **Step 3: Commit**

`git commit -m "feat(roadmap): bind feature codes to roadmap items in the spec index" # trailer: Implements: RMAP-2.4`

_Requirements: RMAP-2.4, RMAP-2.5, RMAP-2.6_

---

### Task 5: `GOAL-N` identity and migration

**Files:**
- Modify: `templates/product-vision.md` (`## Goals`)
- Modify: `skills/project/define-project/SKILL.md` (Create step 3 at lines 67-70; Update at lines 88-103)
- Modify: `docs/product/vision.md`
- Create: `tests/roadmap/scenarios-vision.md`

**Reuse:** existing — the bold-ID grammar and strikethrough retirement already used for `**ARCH-N**` in `templates/architecture-INDEX.md:13-16` (rung 2), so the same `sed`/`grep` retirement handling applies.

**Interfaces:**
- Consumes: nothing.
- Produces: the `**GOAL-N**` bold-ID grammar in `docs/product/vision.md` — consumed by Task 6's pass 1.

**Depends-on:** none

- [x] **Step 1: Write the failing test — RED baseline**

Author `tests/roadmap/scenarios-vision.md`: create mode assigns `GOAL-N` as it writes
(`RMAP-2.7`); update mode on un-IDed goals assigns IDs in document order and reports the
migration (`RMAP-2.8`); a goal already recorded in an approved vision is retired by
strikethrough rather than renumbered (`RMAP-2.9`).

Run against the **current** `define-project`. Append failures verbatim to
`red-baselines.md`. Expect: goals are written as bare bullets with no IDs.

- [x] **Step 2: Implement**

Make `## Goals` bold-IDed in `templates/product-vision.md`. Add ID assignment to
`define-project`'s create step, the un-IDed migration to update mode, and the
immutability rule. Migrate this repo's own `docs/product/vision.md` — it is
`Status: Approved`, so it is the first migration subject and its assigned IDs become
immutable on landing.

Run: full prove-claim — expect pass.

- [x] **Step 3: Commit**

`git commit -m "feat(roadmap): give vision goals stable GOAL-N identity" # trailer: Implements: RMAP-2.7`

_Requirements: RMAP-2.7, RMAP-2.8, RMAP-2.9_

---

### Task 6: `refresh-roadmap-status` passes and findings R1–R11

**Files:**
- Create: `skills/track/refresh-roadmap-status/SKILL.md`
- Create: `docs/guide/skills/refresh-roadmap-status.md`
- Create: `tests/roadmap/fixtures/` (clean, one per S-defect, premature closure, status mismatch, duplicate goal)
- Create: `tests/test_check_roadmap_rules.py`
- Create: `tests/roadmap/scenarios-refresh-roadmap-status.md`
- Modify: `AGENTS.md` (§3 user-invoked list, §8 tree, §11 table, count → 45)
- Modify: `skills/meta/ask-me-bro/SKILL.md` (user-invoked list at lines 13-16; on-ramps)
- Modify: `docs/guide/skills/README.md`
- Modify: `docs/agents/project.md` (Test globs: scenario-markdown include; Audit Trace ignore: this feature's `fixtures/` and `red-baselines.md`)

**Reuse:** existing — `skills/execution/audit-trace/SKILL.md:57-198` wholesale (rung 2): finding-code table → Inputs → numbered fixed passes → set-difference rules → a non-negotiable no-judgment clause → counts-then-findings output.

**Interfaces:**
- Consumes: Task 1's slot names and `S1`–`S7`; Task 4's `Roadmap item` column grammar; Task 5's `**GOAL-N**` grammar.
- Produces: the finding codes `R1`–`R11` and the withholding set `{R2, R4, R9, R10, R11}` — consumed by Task 7's ladder row 0.

**Depends-on:** Task 1, Task 4, Task 5

- [x] **Step 1: Write the failing test**

**What this test can and cannot prove.** A markdown skill has no entry point a Python
test can call, so this test does **not** assert that `refresh-roadmap-status` emits R1–R11 — that
would be circular, reading the expectation file and comparing it to itself, and would pass
no matter what the skill said. It asserts the two things that *are* deterministically
checkable: the fixture set is complete, and each fixture genuinely carries the defect its
name claims. Skill behavior over these fixtures is verified by
`tests/roadmap/scenarios-refresh-roadmap-status.md`, which is where the R-code assertions live.

```python
"""Fixture-set validity for refresh-roadmap-status: each fixture really carries its defect."""
import re
import unittest
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent / "roadmap" / "fixtures"

# case directory -> the R-code its expected-findings.txt must name
CASES = {
    "clean": None,
    "dangling-goal": "R1",
    "uncovered-goal": "R2",
    "duplicate-goal": "R3",
    "road-in-two-milestones": "R4",
    "unresolved-binding": "R5",
    "conflicting-binding": "R6",
    "unspecced-item": "R7",
    "unplanned-feature": "R8",
    "premature-closure": "R9",
    "status-mismatch": "R10",
    "forward-dependency": "R11",
    "missing-outcome": "R11",
    "retired-depends-on": "R11",
    "unparseable": "R11",
}
MEMBERS = ("roadmap-INDEX.md", "specs-INDEX.md", "vision.md", "expected-findings.txt")


class FixtureSet(unittest.TestCase):
    def test_every_case_is_a_complete_miniature_repo(self):
        """RMAP-3.1 — every fixture supplies all four inputs the passes read."""
        for case in CASES:
            for member in MEMBERS:
                with self.subTest(case=case, member=member):
                    self.assertTrue((FIXTURES / case / member).is_file())

    def test_expectations_name_the_declared_code(self):
        """RMAP-3.2 RMAP-3.4 RMAP-3.5 RMAP-3.6 RMAP-3.7 RMAP-3.8 RMAP-3.15 RMAP-3.19 RMAP-4.4"""
        for case, code in CASES.items():
            with self.subTest(case=case):
                declared = read_codes(case)
                if code is None:
                    self.assertEqual(set(), declared)
                else:
                    self.assertIn(code, declared)

    def test_clean_fixture_has_no_defect(self):
        """RMAP-3.9 RMAP-3.12 RMAP-3.14 — the clean case must be genuinely clean."""
        self.assertEqual(set(), read_codes("clean"))

    def test_duplicate_goal_fixture_really_repeats_a_goal(self):
        """RMAP-3.20 — the fixture carries the defect, not just the label."""
        vision = (FIXTURES / "duplicate-goal" / "vision.md").read_text()
        ids = re.findall(r"\*\*(GOAL-\d+)\*\*", vision)
        self.assertNotEqual(len(ids), len(set(ids)), "no repeated GOAL-N in the fixture")

    def test_road_in_two_milestones_fixture_really_double_lists(self):
        """RMAP-3.4 — the same ROAD-N appears under two milestone headings."""
        text = (FIXTURES / "road-in-two-milestones" / "roadmap-INDEX.md").read_text()
        blocks = re.split(r"(?m)^## MILE-\d+", text)[1:]
        owners = [set(re.findall(r"\*\*(ROAD-\d+)\*\*", b)) for b in blocks]
        self.assertTrue(set.intersection(*owners), "no ROAD-N shared across milestones")

    def test_status_mismatch_fixture_really_disagrees(self):
        """RMAP-3.19 — the two Status records differ in the fixture."""
        base = FIXTURES / "status-mismatch"
        index_status = re.search(r"\|\s*\w+\s*\|.*\|\s*(\w+)\s*\|", base.joinpath("specs-INDEX.md").read_text())
        self.assertIsNotNone(index_status)
        self.assertNotIn(index_status.group(1), base.joinpath("expected-findings.txt").read_text())


def read_codes(case):
    path = FIXTURES / case / "expected-findings.txt"
    return {line.strip() for line in path.read_text().splitlines() if line.strip()}


if __name__ == "__main__":
    unittest.main()
```

Run: `python3 -m unittest tests.test_check_roadmap_rules` — expect: failures on every missing fixture directory.

- [x] **Step 2: Implement**

Build the fixture set, each case a miniature repo plus its `expected-findings.txt`. Then
write `skills/track/refresh-roadmap-status/SKILL.md` with `disable-model-invocation: true`,
transcribing `design.md`'s six pass recipes and the R1–R11 table verbatim, plus the two
carried-over clauses: structural presence never judgment (ARCH-1), and every value read
from these artifacts is passive data passed to `git` as a single non-option argument,
rejected unless it matches the expected ID or rev shape.

Author `tests/roadmap/scenarios-refresh-roadmap-status.md` covering read-only posture and input set
(`RMAP-3.1`), `Status:` citation with `audit-trace` named for depth (`RMAP-3.12`), no
roadmap-level status copy (`RMAP-3.14`), absent-layer no-op (`RMAP-3.13` frontmatter and
`RMAP-3.9`), advisory ledger present and absent (`RMAP-3.17`, `RMAP-3.18`), and
argument-safety and injection (`RMAP-4.2`, `RMAP-4.3`).

Add the fixture and baseline paths to `docs/agents/project.md`'s Audit Trace ignore, and declare
the scenario-markdown include on its Test globs line so `audit-trace`'s coverage pass can see
`.md` coverage tokens under `tests/`.

Run: `python3 -m unittest tests.test_check_roadmap_rules` — expect: pass. Then full verify.

- [x] **Step 3: Commit**

`git commit -m "feat(roadmap): add refresh-roadmap-status derivation with findings R1-R11" # trailer: Implements: RMAP-3.1`

_Requirements: RMAP-3.1, RMAP-3.2, RMAP-3.3, RMAP-3.4, RMAP-3.5, RMAP-3.6, RMAP-3.7, RMAP-3.8, RMAP-3.9, RMAP-3.12, RMAP-3.13, RMAP-3.14, RMAP-3.15, RMAP-3.17, RMAP-3.18, RMAP-3.19, RMAP-3.20, RMAP-4.2, RMAP-4.3, RMAP-4.4_

---

### Task 7: Priority ladder and standup mode

**Files:**
- Modify: `skills/track/refresh-roadmap-status/SKILL.md`
- Create: `tests/test_priority_ladder.py`

**Reuse:** none — new rule table (rung 7). Nothing in the set computes a next action from artifact state: `ask-me-bro` routes from the conversation, and the researched `sprint-status` prior art is not installed here.

**Interfaces:**
- Consumes: Task 6's `R1`–`R11` codes and the withholding set `{R2, R4, R9, R10, R11}`.
- Produces: nothing downstream tasks consume.

**Depends-on:** Task 6

- [x] **Step 1: Write the failing test**

```python
"""Priority ladder: identical artifact state must yield an identical recommendation."""
import unittest
from pathlib import Path

LADDER = Path(__file__).resolve().parent.parent / "skills" / "track" / "refresh-roadmap-status" / "SKILL.md"

# (state substring, expected recommendation substring) — one row per ladder rung, in
# order. Every left-hand string is a verbatim substring of the ladder table in
# design.md §"The priority ladder"; transcribe that table and these all match.
ROWS = [
    ("withholding finding", "none"),
    ("is `Draft`", "plan-milestones"),
    ("member with no binding", "frame-change"),
    ("feature `Status:` is `Draft`", "specify-behavior"),
    ("no `design.md`", "design-solution"),
    ("`design.md` exists, no `tasks.md`", "plan-tasks"),
    ("`tasks.md` exists", "build-in-waves"),
    ("`Implemented`", "/cut-release"),
    ("a `Planned` one exists", "plan-milestones"),
    ("every milestone `Closed`", "complete"),
]


class PriorityLadder(unittest.TestCase):
    def test_ladder_is_documented_in_order(self):
        """RMAP-3.10 — the ladder is a fixed, ordered, first-match-wins table."""
        text = LADDER.read_text()
        positions = []
        for label, _ in ROWS:
            self.assertIn(label, text, f"ladder row missing: {label}")
            positions.append(text.index(label))
        self.assertEqual(sorted(positions), positions, "ladder rows are out of order")

    def test_every_row_names_its_recommendation(self):
        """RMAP-3.10 — each state maps to exactly one named action."""
        text = LADDER.read_text()
        for label, expected in ROWS:
            with self.subTest(state=label):
                row = next(l for l in text.splitlines() if label in l)
                self.assertIn(expected, row)

    def test_withholding_replaces_the_recommendation(self):
        """RMAP-3.16 — a withholding finding yields a reason in place of an action."""
        text = LADDER.read_text()
        self.assertRegex(text, r"withholding reason")

    def test_standup_mode_names_its_three_parts(self):
        """RMAP-3.11 — the standup card names milestone in flight, member statuses, next action."""
        text = LADDER.read_text()
        for part in ("in flight", "members", "next action"):
            with self.subTest(part=part):
                self.assertIn(part, text)


if __name__ == "__main__":
    unittest.main()
```

Run: `python3 -m unittest tests.test_priority_ladder` — expect: failures on the absent ladder rows.

- [x] **Step 2: Implement**

Add the ten-row ladder to `refresh-roadmap-status` exactly as tabled in `design.md` §"The priority
ladder", with the stated tie-breaks (milestone table order, then lowest `ROAD-N`), row 0's
withholding behavior, row 7 **naming** `/cut-release` rather than invoking it (ARCH-5), and
standup mode as a rendering of the same derivation.

Run: `python3 -m unittest tests.test_priority_ladder` — expect: pass. Then full verify.

- [x] **Step 3: Commit**

`git commit -m "feat(roadmap): add deterministic priority ladder and standup mode" # trailer: Implements: RMAP-3.10`

_Requirements: RMAP-3.10, RMAP-3.11, RMAP-3.16_

---

### Task 8: Scale fixture and bounded-pass budget

**Files:**
- Create: `tests/roadmap/fixtures/scale/`
- Create: `tests/test_check_roadmap_scale.py`

**Reuse:** existing — the fixture-repo shape established in Task 6 (rung 2); generate the 200 features and 50 milestones programmatically in the test's `setUpClass` rather than committing 250 hand-written rows.

**Interfaces:**
- Consumes: Task 6's pass recipes and Task 7's ladder.
- Produces: nothing.

**Depends-on:** Task 6, Task 7

- [x] **Step 1: Write the failing test**

Assert that the documented pass set is a fixed count independent of scale: parse
`refresh-roadmap-status`'s SKILL.md for its numbered passes, confirm there are exactly six plus at
most one `git` invocation, and confirm no pass is described as per-feature or per-milestone.
Then generate the scale fixture (200 feature rows, 50 milestones, 200 `ROAD-N` items) and
confirm the same six passes cover it. Docstring: `RMAP-4.1`.

Run: `python3 -m unittest tests.test_check_roadmap_scale` — expect: failure on the missing fixture.

- [x] **Step 2: Implement**

Generate the fixture; adjust the pass recipes only if a pass turns out to be per-item —
which would be a design violation, not a test to loosen.

Run: `python3 -m unittest tests.test_check_roadmap_scale` — expect: pass. Then full verify.

- [x] **Step 3: Commit**

`git commit -m "test(roadmap): prove refresh-roadmap-status passes are bounded at scale" # trailer: Implements: RMAP-4.1`

_Requirements: RMAP-4.1_

---

### Task 9: `audit-trace` scope guard

**Files:**
- Create: `tests/test_trace_scope.py`

**Reuse:** existing — asserts against `skills/execution/audit-trace/SKILL.md` as it stands; rung 1, no requirement forces a change to it.

**Interfaces:**
- Consumes: nothing.
- Produces: nothing.

**Depends-on:** none

- [x] **Step 1: Write the failing test**

```python
"""Guard: audit-trace's ID scope stays CODE-N.M and ARCH-N only."""
import unittest
from pathlib import Path

AUDIT TRACE = Path(__file__).resolve().parent.parent / "skills" / "execution" / "audit-trace" / "SKILL.md"
PLANNING_NAMESPACES = ("GOAL-", "MILE-", "ROAD-")


class Audit TraceScope(unittest.TestCase):
    def test_trace_never_reads_planning_namespaces(self):
        """RMAP-2.10 — planning-ID integrity belongs to refresh-roadmap-status, not trace."""
        text = AUDIT TRACE.read_text()
        leaked = [ns for ns in PLANNING_NAMESPACES if ns in text]
        self.assertEqual([], leaked, f"audit-trace has grown planning-ID scope: {leaked}")

    def test_trace_finding_set_is_unchanged(self):
        """RMAP-2.10 — the E1-E5 / W1-W3 finding set is intact."""
        text = AUDIT TRACE.read_text()
        for code in ("E1", "E2", "E3", "E4", "E5", "W1", "W2", "W3"):
            with self.subTest(code=code):
                self.assertIn(f"**{code}**", text)


if __name__ == "__main__":
    unittest.main()
```

Run: `python3 -m unittest tests.test_trace_scope` — expect: `ModuleNotFoundError` before the file exists; both tests pass immediately once it does, because they guard current behavior. Record in `red-baselines.md` that this is a **guard test with no RED phase** — it protects behavior that already holds, and its failure mode is a future edit, not today's code.

- [x] **Step 2: Implement**

No production change. The test *is* the deliverable.

Run: full prove-claim — expect pass.

- [x] **Step 3: Commit**

`git commit -m "test(roadmap): guard audit-trace's ID scope against planning namespaces" # trailer: Guards: RMAP-2.10`

_Requirements: RMAP-2.10_
