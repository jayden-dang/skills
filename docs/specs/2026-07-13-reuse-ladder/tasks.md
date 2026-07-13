# Tasks: Reuse-first ladder in write-design and write-plan

> **For agentic workers:** REQUIRED SUB-SKILL: use `execute-plan` to implement
> this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

Feature code: REUSE
Status: Implemented
Date: 2026-07-13
Requirements: ./requirements.md
Design: ./design.md

**Goal:** Bake a component-level reuse-before-build ladder into `write-design` and
`write-plan` so the methodology stops designing and tasking new code where a helper,
the stdlib, a platform feature, or an installed dependency already does the job.

**Architecture:** Prose edits to two existing skill files — `write-design` gains a
7-rung reuse-ladder sub-gate in Step 2, a `Reuse:` line beside each `Satisfies:`, and a
Step-4 reuse-coverage check; `write-plan` gains the same `Reuse:` line in each task's
Files block and a Step-4 component-level reuse-miss + consistency check. Everything is
additive and advisory. No new skill; no executable code.

**Tech Stack:** Markdown skills (`SKILL.md`). No test runner — see Global Constraints.

## Global Constraints

Copied verbatim from the design and repo conventions; every task inherits these.

- **Verification is baseline scenarios, not automated tests.** No test harness exists for
  skill behavior. Each task's "test" step writes a numbered baseline scenario — tagged
  with its `[REUSE-N.M]` IDs — to its own file
  `docs/specs/2026-07-13-reuse-ladder/baselines/BNN-<slug>.md`, then walks it against the
  edited skill. `trace`'s E2 is documented-exempt; baselines are the covering evidence.
- **Everything additive and advisory.** The ladder, the `Reuse:` line, the new-dependency
  callout, and the Step-4 reuse findings are advisory — surfaced at the existing approval
  gate, NEVER a new hard blocker. A feature with no reuse opportunity must produce today's
  `write-design`/`write-plan` output unchanged.
- **Compose, don't duplicate.** The scan subagent (Step 1) gathers what exists; the ladder
  (Step 2) decides whether to build; the deletion test (Step 2) refines rung-7 output. The
  scan subagent and deletion test keep running unchanged.
- **House style for skills** (`writing-skills`, `AGENTS.md`): imperative voice, **Done
  when:** per step, `` REQUIRED SUB-SKILL: use `x` `` prose not `@`-links, body under 500
  lines.
- **Do NOT touch either file's frontmatter.** Both `write-design` and `write-plan` have a
  frontmatter `description`; the pre-commit lint (`scripts/lint-skill-frontmatter.py`)
  rejects an unquoted colon-space (`": "`) there. The edits are all body prose — leave
  frontmatter alone.
- **No roster/count/guide/plugin.json changes** — this extends two existing skills; the
  skill count stays 36. **No `code-review` or `execute-plan` edits** — out of scope.
- Commit each task with an `Implements: REUSE-N.M` trailer.

## File Structure

**Modify:**
- `skills/spec/write-design/SKILL.md` — Step 2 ladder sub-gate + `Reuse:` line + Step-4
  reuse-coverage bullet.
- `skills/spec/write-plan/SKILL.md` — Step 3 task `Reuse:` line + Step-4 reuse-miss +
  consistency bullets.

**Create:**
- `docs/specs/2026-07-13-reuse-ladder/baselines/BNN-<slug>.md` — one baseline file per task
  (B01–B03), so no two tasks share a Test file and the declared parallel wave holds.

---

### Task 1: `write-design` — reuse ladder, `Reuse:` line, Step-4 coverage

**Files:**
- Modify: `skills/spec/write-design/SKILL.md` (Step 2 insert before the deletion-test
  paragraph ~line 56; Satisfies-line paragraph ~line 38-40; Step-4 coverage self-check
  ~line 71-75)
- Test: `docs/specs/2026-07-13-reuse-ladder/baselines/B01-write-design.md`

**Interfaces:**
- Reuse: existing — edits `skills/spec/write-design/SKILL.md` prose (rung 2); consumes the
  existing Step-1 scan subagent and Step-2 deletion-test paragraph, unchanged.
- Produces: the 7-rung ladder sub-gate; the shared `Reuse: <rung> — <concrete target>` line
  grammar (also consumed by Task 2); the reuse-coverage self-check.

**Depends-on:** none

- [x] **Step 1 (scenario):** Write baseline B01 to `baselines/B01-write-design.md`:
  (a) Step 2 presents a 7-rung ladder (need-it/in-codebase/stdlib/platform/installed-dep/
  one-line/new-code), stop at highest rung that holds, fed by the Step-1 scan digest and
  climbed after understanding the problem `[REUSE-1.1] [REUSE-1.2]`; (b) the ladder must not
  prune away validation-at-trust-boundaries / data-loss error handling / security /
  accessibility / explicitly-requested behavior `[REUSE-1.3]`; (c) every architecture
  section carries a `Reuse: <rung> — <concrete target>` line beside Satisfies; rung-7 new
  code carries a one-line justification; a brand-new dependency gets a distinct callout;
  both advisory `[REUSE-2.1] [REUSE-2.2] [REUSE-2.3] [REUSE-2.4]`; (d) Step-4 self-check
  verifies every section has a Reuse line + justification `[REUSE-4.1]`; (e) the
  scan→ladder→deletion-test chain is stated and the deletion test is scoped to rung-7 output,
  with the scan subagent and deletion test otherwise unchanged `[REUSE-5.1] [REUSE-5.2]`.
- [x] **Step 2 (implement):** In `skills/spec/write-design/SKILL.md`: (a) insert the
  ladder sub-gate into Step 2 after the "design it twice"/"single-design job" guidance and
  BEFORE the "Design for depth / deletion test" paragraph — the 7 rungs, "stop at highest
  rung that holds", "fed by the Step-1 scan digest, applied after tracing the real flow — a
  reflex, not a research project", the when-NOT-to-be-lazy carve-outs, and the explicit
  scan→ladder→deletion-test chain; then reword the deletion-test paragraph's opening to scope
  it to "a rung-7 new component". (b) Add one sentence to the Satisfies-line paragraph: every
  `###` section carries a `Reuse: <rung> — <concrete target>` line beside its `Satisfies:`
  line (or `none — new code (rung 7)`), a rung-7 line carries a one-line why-no-lower-rung
  justification, a brand-new third-party dependency gets a distinct callout, and the line +
  callout are advisory (never a hard blocker). (c) Add a bullet to the Step-4 coverage
  self-check: verify every architecture section has a `Reuse:` line and every rung-7/new-dep
  line has its justification. Touch no frontmatter.
- [x] **Step 3 (verify + commit):** Walk B01 against the edited skill; confirm frontmatter
  untouched and `python3 scripts/lint-skill-frontmatter.py skills/spec/write-design/SKILL.md`
  passes. Commit `Implements: REUSE-1.1, REUSE-1.2, REUSE-1.3, REUSE-2.1, REUSE-2.2,
  REUSE-2.3, REUSE-2.4, REUSE-4.1, REUSE-5.1, REUSE-5.2`.

_Requirements: REUSE-1.1, REUSE-1.2, REUSE-1.3, REUSE-2.1, REUSE-2.2, REUSE-2.3, REUSE-2.4, REUSE-4.1, REUSE-5.1, REUSE-5.2_

---

### Task 2: `write-plan` — task `Reuse:` line and Step-4 reuse-miss check

**Files:**
- Modify: `skills/spec/write-plan/SKILL.md` (Step 3 task Files bullet ~line 48; Step 4
  coverage/consistency check ~line 70-88, near the "Type/name consistency" bullet)
- Test: `docs/specs/2026-07-13-reuse-ladder/baselines/B02-write-plan.md`

**Interfaces:**
- Reuse: existing — edits `skills/spec/write-plan/SKILL.md` prose (rung 2); consumes the
  shared `Reuse:` line grammar from Task 1 and `code-review`'s existing "reuse-miss" term
  (`skills/review/code-review/SKILL.md:54`) at component granularity.
- Produces: the task-level `Reuse:` line; the component-level reuse-miss + design↔task
  consistency checks.

**Depends-on:** none

- [x] **Step 1 (scenario):** Write baseline B02 to `baselines/B02-write-plan.md`:
  (a) each task's Files block carries a `Reuse:` line naming the concrete existing code/lib/
  pattern the task builds on, and it is kept consistent with the design section it implements
  `[REUSE-3.1] [REUSE-3.2]`; (b) Step-4 flags as a component-level reuse-miss any task whose
  Files Create something the scan digest or an already-installed dependency already provides
  `[REUSE-4.2]`; (c) Step-4 flags any task whose Reuse line is inconsistent with its design
  section `[REUSE-4.3]`.
- [x] **Step 2 (implement):** In `skills/spec/write-plan/SKILL.md`: (d) add a `Reuse:`
  sub-bullet to the task **Files** bullet (beside `Create / Modify … / Test`) — the concrete
  existing code, library, or pattern the task builds on, so the implementer is told to build
  on it, not reimplement it; note it must stay consistent with the design section's `Reuse:`
  line. (e) In the Step-4 coverage/consistency check, add two bullets near "Type/name
  consistency": a **component-level reuse-miss** — flag a task whose Files Create something
  the scan digest or an already-installed dependency already provides (borrowing
  `code-review`'s reuse-miss term at task granularity); and a **Reuse-consistency** check —
  flag a task whose `Reuse:` line disagrees with the design section it implements. Both
  advisory findings in the existing pass. Touch no frontmatter.
- [x] **Step 3 (verify + commit):** Walk B02 against the edited skill; confirm frontmatter
  untouched and `python3 scripts/lint-skill-frontmatter.py skills/spec/write-plan/SKILL.md`
  passes. Commit `Implements: REUSE-3.1, REUSE-3.2, REUSE-4.2, REUSE-4.3`.

_Requirements: REUSE-3.1, REUSE-3.2, REUSE-4.2, REUSE-4.3_

---

### Task 3: Additivity audit — no-reuse feature unchanged, no new gate

**Files:**
- Test: `docs/specs/2026-07-13-reuse-ladder/baselines/B03-additivity.md`

**Interfaces:**
- Reuse: existing — walks the Task 1 + Task 2 edits; adds no new file edit.
- Produces: the cross-cutting additivity baseline covering REUSE-5.3.

**Depends-on:** Task 1, Task 2

- [x] **Step 1 (scenario):** Write baseline B03 to `baselines/B03-additivity.md`: a feature
  with no reuse opportunity walked through the edited `write-design` and `write-plan` produces
  their existing structure unchanged — `Satisfies:` lines, Files Create/Modify/Test,
  Interfaces, Depends-on, Steps, footers — with an empty-or-`none` `Reuse:` line, and NO new
  hard approval gate is introduced (the reuse findings are advisory, never blocking).
  `[REUSE-5.3]`
- [x] **Step 2 (implement):** No new content edit — confirm the additive/advisory/no-new-gate
  wording landed in Task 1's and Task 2's edits (grep both skills for the advisory/"never a
  hard blocker"/additive phrasing), and record the walk as B03. If either edit reads as a hard
  gate rather than advisory, fix the wording in the owning skill (Task 1 or Task 2's file).
- [x] **Step 3 (verify + commit):** Confirm B03 walks clean. Commit `Implements: REUSE-5.3`.

_Requirements: REUSE-5.3_

---

## Coverage self-check

All 15 REUSE IDs cited by exactly one task footer:

- **T1:** 1.1, 1.2, 1.3, 2.1, 2.2, 2.3, 2.4, 4.1, 5.1, 5.2
- **T2:** 3.1, 3.2, 4.2, 4.3
- **T3:** 5.3

Test tags: every ID appears in a `[REUSE-N.M]`-tagged baseline scenario, one file per task
(B01–B03). No two tasks share a Test file, so the declared parallel wave (T1 ∥ T2, then T3)
holds. Matches the design seam table. No ID uncited; none double-cited.
