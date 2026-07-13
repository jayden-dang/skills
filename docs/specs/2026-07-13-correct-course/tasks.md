# Tasks: Correct-course — mid-flight plan-invalidation router

> **For agentic workers:** REQUIRED SUB-SKILL: use `execute-plan` to implement
> this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

Feature code: CCOURSE
Status: Approved
Date: 2026-07-13
Requirements: ./requirements.md
Design: ./design.md

**Goal:** Add a model-invoked `correct-course` skill that, when a mid-execution
discovery invalidates an approved plan, diagnoses it, classifies the lowest
invalidated artifact with evidence, and routes to the right re-entry point —
delegating all content and reconciliation to existing skills.

**Architecture:** One new skill (`skills/track/correct-course/SKILL.md`, a
three-phase thin router), a guarded two-point edit to `execute-plan`'s hand-off
signals, and roster registration moving the skill count 35 → 36. Everything is
pure `SKILL.md` / markdown — no executable code ships.

**Tech Stack:** Markdown skills (`SKILL.md`), markdown guide pages, JSON plugin
manifest. No test runner — see Global Constraints.

## Global Constraints

Copied verbatim from the design and repo conventions; every task inherits these.

- **Zero consuming-repo tooling.** This feature adds no script, linter, CI, or hook
  to a consuming repo. Skills are pure `SKILL.md`; the deliverable is markdown.
- **Verification is baseline scenarios, not automated tests.** This repo has no test
  harness for skill behavior. Each task's "test" step writes a numbered baseline
  scenario — tagged with its `[CCOURSE-N.M]` IDs — to **its own file**
  `docs/specs/2026-07-13-correct-course/baselines/BNN-<slug>.md` (NN = task number, so
  no two tasks share a Test file and same-wave tasks don't collide), then "runs" it by
  walking the scenario against the authored skill/edit. `trace`'s E2 (needs a test
  file) is documented-exempt for this repo; baseline scenarios are the covering
  evidence.
- **House style for skills** (`writing-skills`, `AGENTS.md`): frontmatter
  `description` states *triggers + outcome noun only, never the workflow*; body is
  imperative with **Done when:** per step, a `## Red Flags` block, and a
  `| Thought | Reality |` rationalization table where useful; cross-references are
  `REQUIRED SUB-SKILL: use \`x\`` prose, never `@`-links; body under 500 lines.
- **Frontmatter colon-space lint (hard).** `scripts/lint-skill-frontmatter.py` (wired via
  `lefthook.yml` pre-commit) parses the frontmatter with `yaml.safe_load` and rejects any
  `SKILL.md` whose frontmatter is not valid YAML — an unquoted colon-space (`": "`) in a
  plain-scalar `description` breaks YAML parsing and fails the commit. Write the description
  with em-dashes/commas, never a raw `: ` — keep it valid YAML.
- **`correct-course` is a thin router.** It NEVER itself edits a `requirements.md`,
  `design.md`, `tasks.md`, or trace metadata — all spec-content generation delegates to
  the `write-*` skills and all reconciliation to `sync-spec`. Its only writes are the
  ephemeral in-conversation diagnosis/proposal and the git-ignored `.skills/corrections.md`
  ledger.
- **Model-invoked composition** (`AGENTS.md`, ARCH-precedent): `correct-course` is
  model-invoked (NO `disable-model-invocation`); it may only `REQUIRED SUB-SKILL` into
  other model-invoked skills — all of `write-requirements`, `write-design`, `write-plan`,
  `brainstorm`, `sync-spec`, `domain-modeling`, `execute-plan`, `tdd` are model-invoked
  (verified in design review).
- **Guarded `execute-plan` edits.** Only the two named signals change (BLOCKED "plan is
  wrong" at line 60; circuit breaker at line 38). The pre-flight plan review (line 24) and
  every other stop — a BLOCKED you cannot resolve for another reason, genuine ambiguity,
  all-tasks-complete (line 14) — must CONTINUE TO behave exactly as today.
- **ID immutability:** never renumber an Approved requirement; retire by strikethrough.
- Commit each task with an `Implements: CCOURSE-N.M` trailer.

## File Structure

**Create:**
- `skills/track/correct-course/SKILL.md` — the three-phase router (diagnose → classify →
  route), inline 5-level classifier table, idempotency ledger, boundary Red Flags.
- `docs/guide/skills/correct-course.md` — the human-facing guide page for the skill.
- `docs/specs/2026-07-13-correct-course/baselines/BNN-<slug>.md` — **one baseline file per
  task** (B01–B03), so no two tasks share a Test file and the declared parallel wave holds.

**Modify:**
- `skills/execution/execute-plan/SKILL.md` — line 60 BLOCKED hand-off; line 38
  circuit-breaker root-cause branch; guards on the untouched stops.
- `.claude-plugin/plugin.json` — append `"./skills/track/correct-course"` to `skills[]`.
- `AGENTS.md` — §8 file-org `track/` line, §11 quick-ref `track` row, header (line 3) and
  §8 comment counts 35 → 36.
- `DESIGN.md` — `track/` inventory list and the "35 skills" count → 36.
- `docs/guide/skills/README.md` — `track` table row and the "Thirty-five skills" opening
  count → 36.
- `skills/meta/ask/SKILL.md` — an on-ramp routing "a mid-execution discovery invalidated my
  approved plan" → `correct-course`.

---

### Task 1: Author the `correct-course` skill

**Files:**
- Create: `skills/track/correct-course/SKILL.md`
- Test: `docs/specs/2026-07-13-correct-course/baselines/B01-correct-course-skill.md`

**Interfaces:**
- Consumes: `write-requirements`, `write-design`, `write-plan`, `brainstorm`, `sync-spec`,
  `domain-modeling`, `execute-plan`, `tdd` as REQUIRED SUB-SKILLs (all model-invoked).
- Produces: the model-invoked skill `correct-course` at `skills/track/correct-course/`; the
  five-level classifier (Task-local / Plan / Design / Requirements / Vision) keyed on the
  lowest invalidated artifact with evidence; the ephemeral evidence-ledger format
  `.skills/corrections.md` (fingerprint + level + outcome) consumed by no other task.

**Depends-on:** none

- [ ] **Step 1 (scenario):** Write baseline B01 to
  `baselines/B01-correct-course-skill.md` with scenarios: (a) skill is model-invoked, at
  `skills/track/correct-course/`, frontmatter description has no colon-space
  `[CCOURSE-1.3] [CCOURSE-7.3]`; (b) Phase 1 emits a What/Where/Why/How+impact notice and
  hard-stops for go/no-go; a no-go is a clean no-op `[CCOURSE-2.1] [CCOURSE-2.2]
  [CCOURSE-2.3]`; (c) Phase 2 names the lowest invalidated artifact with evidence, never
  higher; presents an ephemeral proposal and stops for approval `[CCOURSE-3.1] [CCOURSE-3.2]
  [CCOURSE-3.3] [CCOURSE-3.4]`; (d) repeated same-evidence→same-level classification halts
  and escalates via the ledger `[CCOURSE-3.5] [CCOURSE-3.6]`; (e) each level routes to its
  re-entry skill, invoked directly, running that skill's own gate; Vision with no
  `vision.md` escalates to a human `[CCOURSE-4.1] [CCOURSE-4.2] [CCOURSE-4.3] [CCOURSE-4.4]
  [CCOURSE-4.5] [CCOURSE-4.6]`; (f) thin-router exit — delegate, `sync-spec` reconcile,
  conditional ADR, resume `execute-plan` (with ledger re-baselining) `[CCOURSE-5.1]
  [CCOURSE-5.2] [CCOURSE-5.3] [CCOURSE-5.4] [CCOURSE-5.5]`; (g) Red Flags carve it from
  `amend`/`debug`/`sync-spec` `[CCOURSE-6.1] [CCOURSE-6.2]`.
- [ ] **Step 2 (implement):** Write `skills/track/correct-course/SKILL.md`. Frontmatter:
  `name: correct-course`; a `description` (triggers + outcome noun, **no unquoted `: `**)
  keyed to "a mid-execution discovery invalidates an approved plan" with search keywords
  ("the plan is wrong", "re-plan", "mid-execution", "scope changed") and NO
  `disable-model-invocation`. Body: **Phase 1 — Diagnose** (author the What/Where/Why/How +
  impact notice; present; hard-stop **Done when:** the user rules go/no-go; no-go = no
  change, return). **Phase 2 — Classify** (the inline 5-level table from design §Phase 2;
  the "lowest invalidated artifact with evidence — never higher" law; present the ephemeral
  proposal; hard-stop for approval; never write a proposal file). **Idempotency** (read
  `.skills/corrections.md`; if the same evidence would re-classify to the same level with no
  new evidence, halt + escalate; else record a fingerprint line). **Phase 3 — Route** (per
  level, invoke the re-entry sub-skill directly and let it run its own gate; Vision →
  vision layer if `docs/product/vision.md` exists, else escalate to a human, `brainstorm`
  only on user agreement). **Thin-router exit** (delegate content to `write-*`; `sync-spec`
  to reconcile Status/trace; ADR via `domain-modeling` only on architectural consequence,
  never for an unapproved proposal, never for Task-local/Plan; return to `execute-plan`,
  re-baselining `.skills/progress.md` on a tasks.md rewrite; resume). A `## Red Flags —
  wrong skill` block naming `amend`/`debug`/`sync-spec` boundaries. Keep body < 500 lines.
- [ ] **Step 3 (verify + commit):** Walk B01 against the authored skill; confirm the
  frontmatter passes `scripts/lint-skill-frontmatter.py`. Commit `Implements: CCOURSE-1.3,
  CCOURSE-2.1, CCOURSE-2.2, CCOURSE-2.3, CCOURSE-3.1, CCOURSE-3.2, CCOURSE-3.3, CCOURSE-3.4,
  CCOURSE-3.5, CCOURSE-3.6, CCOURSE-4.1, CCOURSE-4.2, CCOURSE-4.3, CCOURSE-4.4, CCOURSE-4.5,
  CCOURSE-4.6, CCOURSE-5.1, CCOURSE-5.2, CCOURSE-5.3, CCOURSE-5.4, CCOURSE-5.5, CCOURSE-6.1,
  CCOURSE-6.2, CCOURSE-7.3`.

_Requirements: CCOURSE-1.3, CCOURSE-2.1, CCOURSE-2.2, CCOURSE-2.3, CCOURSE-3.1, CCOURSE-3.2, CCOURSE-3.3, CCOURSE-3.4, CCOURSE-3.5, CCOURSE-3.6, CCOURSE-4.1, CCOURSE-4.2, CCOURSE-4.3, CCOURSE-4.4, CCOURSE-4.5, CCOURSE-4.6, CCOURSE-5.1, CCOURSE-5.2, CCOURSE-5.3, CCOURSE-5.4, CCOURSE-5.5, CCOURSE-6.1, CCOURSE-6.2, CCOURSE-7.3_

---

### Task 2: Guarded `execute-plan` hand-off edit

**Files:**
- Modify: `skills/execution/execute-plan/SKILL.md` (BLOCKED table row, line 60; circuit
  breaker, step 8 line 38)
- Test: `docs/specs/2026-07-13-correct-course/baselines/B02-execute-plan-edit.md`

**Interfaces:**
- Consumes: the `correct-course` skill by name (Task 1) as the REQUIRED SUB-SKILL hand-off
  target.
- Produces: two guarded hand-off edits; the untouched-stop guarantees.

**Depends-on:** Task 1

- [ ] **Step 1 (scenario):** Write baseline B02 to
  `baselines/B02-execute-plan-edit.md`: (a) the BLOCKED "the plan itself is wrong" branch
  now pauses and hands off to `correct-course` instead of dead-ending at escalate-to-user
  `[CCOURSE-1.1]`; (b) the circuit breaker (finding survives 3 fix→re-review cycles) runs a
  root-cause step and hands off to `correct-course` only when the lowest invalidated
  artifact is above the current task, else continues the existing escalate/fix flow
  `[CCOURSE-1.2]`; (c) GUARD — a BLOCKED status unresolvable for any other reason, genuine
  ambiguity, and all-tasks-complete still behave as today `[CCOURSE-1.4]`; (d) GUARD — the
  pre-flight plan review (step 5) still batches findings into one pre-dispatch question,
  unaffected `[CCOURSE-1.5]`.
- [ ] **Step 2 (implement):** In the BLOCKED table (line 60), change the final diagnose
  branch to "…the plan itself is wrong → pause and REQUIRED SUB-SKILL: use `correct-course`"
  (leave the other three branches and the redispatch cap unchanged). In the Fix-loop
  circuit breaker (line 38), after "stop looping," insert a root-cause step: determine the
  lowest invalidated artifact; IF it is above the current task, REQUIRED SUB-SKILL: use
  `correct-course`; ELSE continue "escalate to the user with the finding and the three
  attempts" as today. Touch nothing at line 24 (pre-flight) or line 14 (legitimate stops).
- [ ] **Step 3 (verify + commit):** Walk B02 (all four scenarios), confirming the guard
  branches read byte-unchanged except the two named edits. Commit `Implements: CCOURSE-1.1,
  CCOURSE-1.2, CCOURSE-1.4, CCOURSE-1.5`.

_Requirements: CCOURSE-1.1, CCOURSE-1.2, CCOURSE-1.4, CCOURSE-1.5_

---

### Task 3: Roster registration, guide page, and `ask` on-ramp

**Files:**
- Create: `docs/guide/skills/correct-course.md`
- Modify: `.claude-plugin/plugin.json` (append skill path), `AGENTS.md` (§8 tree, §11 table,
  and all THREE count surfaces → 36: header line 3, §8 comment line 221, §11 heading line
  299), `DESIGN.md` (BOTH track inventories — compact tree line 58 + numbered list — plus the
  count line 230 → 36), `docs/guide/skills/README.md` (track row + spelled-out count),
  `skills/meta/ask/SKILL.md` (on-ramp line under `## On-ramps`)
- Test: `docs/specs/2026-07-13-correct-course/baselines/B03-registration.md`

**Interfaces:**
- Consumes: the final `correct-course` frontmatter description and purpose (Task 1), mirrored
  in the guide page and quick-ref row.
- Produces: `correct-course` registered across every roster surface at count 36; an `ask`
  on-ramp.

**Depends-on:** Task 1

- [ ] **Step 1 (scenario):** Write baseline B03 to
  `baselines/B03-registration.md`: (a) `correct-course` appears in `plugin.json` `skills[]`,
  the `AGENTS.md` §8 tree and §11 `track` row, both `DESIGN.md` `track/` inventories, and a
  new `docs/guide/skills/correct-course.md` page + README `track` row, with every skill-count
  surface reading thirty-six and none disagreeing `[CCOURSE-7.1]`; (b)
  `skills/meta/ask/SKILL.md` routes "a mid-execution discovery invalidated my approved plan"
  → `correct-course` `[CCOURSE-7.2]`.
- [ ] **Step 2 (implement):** Append `"./skills/track/correct-course"` to `plugin.json`
  `skills[]`. In `AGENTS.md`: add the `track/` tree entry (§8), a `correct-course` row to the
  §11 quick-ref `track` group, and bump **all three** count surfaces 35 → 36 — the header
  (line 3), the §8 comment (line 221), and the §11 heading "The 35 Skills" (line 299). In
  `DESIGN.md`: add `correct-course` to **both** track representations — the compact tree
  (line 58) and the numbered inventory list (`### track/`, lines 314-324), renumbering the
  items after it (e.g. `establish-project` 35 → 36) — and bump the "35 skills" count (line
  230) → 36. Create `docs/guide/skills/correct-course.md` mirroring `amend.md`'s shape (title,
  `>` blurb, metadata table Bucket/Invocation/Reads/Writes/Calls/Called-by, "## When it
  fires", numbered workflow sections with **Done when**, "## Red flags", "## Worked example",
  "## Why it is written the way it is", "## See also"), add its `track` row to
  `docs/guide/skills/README.md`, and change the spelled-out opening count "Thirty-five skills"
  → "Thirty-six skills". In `skills/meta/ask/SKILL.md`, add a bullet under `## On-ramps`
  (line 40) keyed to a mid-execution plan-invalidation discovery → `correct-course`.
- [ ] **Step 3 (verify + commit):** Walk B03; grep every surface to confirm one consistent
  count of 36 (digit forms) / "Thirty-six" (README word form) and no stale "35"/"Thirty-five"
  anywhere. Run `trace` (REQUIRED SUB-SKILL) and confirm no new errors. Commit `Implements:
  CCOURSE-7.1, CCOURSE-7.2`.

_Requirements: CCOURSE-7.1, CCOURSE-7.2_

---

## Coverage self-check

All 30 CCOURSE IDs cited by exactly one task footer:

- **T1:** 1.3, 2.1, 2.2, 2.3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6,
  5.1, 5.2, 5.3, 5.4, 5.5, 6.1, 6.2, 7.3
- **T2:** 1.1, 1.2, 1.4, 1.5
- **T3:** 7.1, 7.2

Test tags: every ID appears in a `[CCOURSE-N.M]`-tagged baseline scenario, one file per task
under `baselines/B01…B03-*.md` — the covering evidence for this repo (Global Constraints). No
two tasks share a Test file, so the declared parallel wave (T2 ∥ T3 after T1) holds. Matches
the design seam table. No ID uncited; none double-cited.
