# Tasks: Mid-build implementation notes

> **For agentic workers:** after plan approval, pick one execute skill —
> `build-in-waves`, `build-by-story`, or `build-inline`. The chosen skill writes
> `Execution-mode:`.

Feature code: IMPN
Status: Approved
Date: 2026-08-01
Execution-mode: continuous
Requirements: ./requirements.md
Design: ./design.md

**Goal:** Upgrade mid-build implementation-notes to classified deviations (unknown
class + map impact) on every execute route, and surface them at handoff/package/land.

**Architecture:** Prose contract only — extend implementer-prompt, execute SKILL
bodies, write-handoff, package-change, land-branch; verify with source-contract
unittest + scenarios (ARCH-3).

**Tech Stack:** Markdown skills; Python 3 unittest under `tests/`.

## Global Constraints

From `docs/agents/project.md` and `docs/architecture/INDEX.md`.

| Check | Command |
|---|---|
| Lint | `python3 scripts/lint-skill-frontmatter.py && python3 scripts/lint-write-handoffs.py && python3 scripts/lint-context7.py` |
| Unit | `python3 -m unittest discover -s tests` |

Single test: `python3 -m unittest tests.test_implementation_notes_contract`

Test IDs: greppable `IMPN-N.M` in method names / docstrings / `tests/implementation-notes/scenarios*.md`.

**ARCH-1..6** apply. No `skills/**/*.py`. No second mid-build unknowns file. No auto-edit of triad. Notes path remains `.skills/<CODE>/implementation-notes.md`.

**Team:** Solo.

## File Structure

**Create:**

| File | Responsibility |
|---|---|
| `tests/test_implementation_notes_contract.py` | Source contracts |
| `tests/implementation-notes/scenarios.md` | All IMPN-N.M tokens |
| `tests/implementation-notes/scenarios-pressure.md` | 5-field incomplete; silent stretch; append two |

**Modify:**

| File | Change |
|---|---|
| `skills/execution/build-in-waves/implementer-prompt.md` | Nine-field Deviations recipe + enums + stop rule |
| `skills/execution/build-in-waves/SKILL.md` | DONE_WITH_CONCERNS incomplete-without-notes; map impact stop |
| `skills/execution/build-in-waves/TESTS.md` | Pressure rows for new fields |
| `skills/execution/build-by-story/SKILL.md` | Align DONE_WITH_CONCERNS language |
| `skills/execution/build-inline/SKILL.md` | Deviations step full field set |
| `skills/track/write-handoff/SKILL.md` | Path + count Map impact ≠ none |
| `skills/ship/package-change/SKILL.md` | Mention notes when Map impact ≠ none |
| `skills/ship/land-branch/SKILL.md` | Surface unresolved reroute/realign impacts |
| `templates/skills-ephemera-paths.md` | Short entry-fields blurb under implementation-notes |
| `docs/agents/project.md` | audit-trace ignore for implementation-notes tests |

---

### Task 1: Contract harness + schema SSOT in implementer-prompt

**Files:**
- Create: `tests/test_implementation_notes_contract.py`
- Create: `tests/implementation-notes/scenarios.md`
- Create: `tests/implementation-notes/scenarios-pressure.md`
- Modify: `skills/execution/build-in-waves/implementer-prompt.md`
- Modify: `skills/execution/build-in-waves/TESTS.md`
- Modify: `templates/skills-ephemera-paths.md`
- Modify: `docs/agents/project.md`
- Test: `tests/test_implementation_notes_contract.py`

**Reuse:** rung 2 — extend implementer-prompt Deviations; SKNS path

**Interfaces:**
- Produces: nine-field recipe text; contract tests for field names + enums

**Depends-on:** none

- [ ] **Step 1: Write the failing test**

```python
"""IMPN-1.1 IMPN-1.2 IMPN-1.3 IMPN-1.4 IMPN-1.5 IMPN-2.1 IMPN-2.3 IMPN-4.4 IMPN-5.1"""
# Assert implementer-prompt contains:
# Task, Unknown class, Map said, Territory showed, Deviation, Cause, Choice, Map impact, Revisit
# enums known-unknown, unknown-known, unknown-unknown, assumption-break, blindspot
# enums none, revisit-only, reroute-plan, realign-spec
# conservative choice language
# path .skills/<CODE>/implementation-notes.md
# scenarios list every IMPN-N.M from requirements
# pressure: five-field-only incomplete; silent stretch no
```

Run: `python3 -m unittest tests.test_implementation_notes_contract` — expect fail.

- [ ] **Step 2: Implement** full Deviations section in implementer-prompt; example entry optional; TESTS.md pressure rows; ephemera-paths blurb; project.md ignore.

Run: tests for Task1 classes pass.

- [ ] **Step 3: Commit**

`Implements: IMPN-1.1, IMPN-1.2, IMPN-1.3, IMPN-1.4, IMPN-1.5, IMPN-2.1, IMPN-2.3, IMPN-4.4, IMPN-5.1`

_Requirements: IMPN-1.1, IMPN-1.2, IMPN-1.3, IMPN-1.4, IMPN-1.5, IMPN-2.1, IMPN-2.3, IMPN-4.4, IMPN-5.1_

---

### Task 2: Execute routes — waves, story, inline + incomplete rule

**Files:**
- Modify: `skills/execution/build-in-waves/SKILL.md`
- Modify: `skills/execution/build-by-story/SKILL.md`
- Modify: `skills/execution/build-inline/SKILL.md`
- Modify: `tests/test_implementation_notes_contract.py`
- Modify: `tests/implementation-notes/scenarios.md`
- Test: `tests/test_implementation_notes_contract.py`

**Reuse:** rung 2 — design §2

**Depends-on:** Task 1

- [ ] **Step 1: Write the failing test**

Assert build-inline lists all nine fields (or points at implementer-prompt field set).  
Assert waves + story: DONE_WITH_CONCERNS requires notes path; Map impact `reroute-plan` / falsifying plan → `reroute-plan` skill.  
Assert IMPN-1.6, IMPN-1.7, IMPN-2.2, IMPN-4.2, IMPN-4.3 language present.

Run: fail until edits.

- [ ] **Step 2: Implement** skill body updates.

Run: pass.

- [ ] **Step 3: Commit**

`Implements: IMPN-1.6, IMPN-1.7, IMPN-2.2, IMPN-4.2, IMPN-4.3`

_Requirements: IMPN-1.6, IMPN-1.7, IMPN-2.2, IMPN-4.2, IMPN-4.3_

---

### Task 3: Post-build surface + suite close

**Files:**
- Modify: `skills/track/write-handoff/SKILL.md`
- Modify: `skills/ship/package-change/SKILL.md`
- Modify: `skills/ship/land-branch/SKILL.md`
- Modify: `tests/test_implementation_notes_contract.py`
- Modify: `tests/implementation-notes/scenarios.md`
- Modify: `tests/implementation-notes/scenarios-pressure.md`
- Test: full unit suite relevant modules

**Reuse:** rung 2 — design §3

**Depends-on:** Task 1

- [ ] **Step 1: Write the failing test**

Assert write-handoff: notes path + Map impact ≠ none count.  
Assert package-change: mentions notes when mid-build why / Map impact.  
Assert land-branch: notes path; unresolved reroute-plan/realign-spec surface.  
Assert frame-change still owns knowns inventory (IMPN-4.1) — knowns language present; implementer-prompt does not claim to replace discovery.  
All IMPN IDs in scenarios.

Run: fail until edits.

- [ ] **Step 2: Implement** surface skills; run:

```bash
python3 scripts/lint-skill-frontmatter.py && python3 scripts/lint-write-handoffs.py && python3 scripts/lint-context7.py
python3 -m unittest tests.test_implementation_notes_contract
```

- [ ] **Step 3: Commit**

`Implements: IMPN-3.1, IMPN-3.2, IMPN-3.3, IMPN-4.1`

_Requirements: IMPN-3.1, IMPN-3.2, IMPN-3.3, IMPN-4.1_

---

## Coverage map

| IDs | Task |
|---|---|
| 1.1–1.5, 2.1, 2.3, 4.4, 5.1 | Task 1 |
| 1.6–1.7, 2.2, 4.2–4.3 | Task 2 |
| 3.1–3.3, 4.1 | Task 3 |

## Exit

Present and **STOP**.

On approval: `Status: Approved`, leave `Execution-mode: unset`, offer:

| Route | Skill |
|---|---|
| Subagent waves | `build-in-waves` |
| Story units | `build-by-story` |
| Controller implements | `build-inline` |
