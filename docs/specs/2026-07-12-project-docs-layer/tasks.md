# Tasks: Optional project-documentation layer

> **For agentic workers:** REQUIRED SUB-SKILL: use `execute-plan` to implement
> this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

Feature code: PROJDOC
Status: Implemented
Date: 2026-07-12
Requirements: ./requirements.md
Design: ./design.md

**Goal:** Add an optional, opt-in project-documentation layer (repo-level vision +
IDed architecture invariants + engineering guidelines) above the feature workflow,
consulted through no-op-if-absent hooks and a deterministic `trace` extension.

**Architecture:** Two new skills (`establish-project`, `check-invariants`), three
doc templates, six hook edits to existing skills, a `trace` referential-integrity
extension, setup/scaffold opt-in, and a dogfood seed of this repo's own invariants.
Everything is pure `SKILL.md` / markdown — no executable code ships.

**Tech Stack:** Markdown skills (`SKILL.md`), markdown templates, JSON plugin
manifest. No test runner — see Global Constraints.

## Global Constraints

Copied verbatim from the design and repo conventions; every task inherits these.

- **Zero consuming-repo tooling.** This feature adds no script, linter, CI, or hook
  to a consuming repo. Skills are pure `SKILL.md`; the layer is markdown.
- **Verification is baseline scenarios, not automated tests.** This repo has no test
  harness for skill behavior. Each task's "test" step writes a numbered baseline
  scenario — tagged with its `[PROJDOC-N.M]` IDs — to **its own file**
  `docs/specs/2026-07-12-project-docs-layer/baselines/BNN-<slug>.md` (NN = task
  number, so no two tasks share a Test file and same-wave tasks don't collide), then
  "runs" it by walking the scenario against the authored skill/doc. `trace`'s E2 (needs a test file) is
  documented-exempt for this repo; baseline scenarios are the covering evidence.
- **House style for skills** (`writing-skills`, `AGENTS.md`): frontmatter
  `description` states *triggers + outcome noun only, never the workflow*; body is
  imperative with **Done when:** per step; cross-references are `REQUIRED SUB-SKILL:
  use \`x\`` prose, never `@`-links; templates resolve as
  `${CLAUDE_PLUGIN_ROOT}/templates` else `../../../templates`.
- **Consult-hook idiom** (mirror `brainstorm/SKILL.md:53`): observable-predicate
  ("WHERE `<doc>` exists …") + no-op-if-absent ("else say so once and continue").
  Never a new hard gate.
- **User-invoked skills** carry `disable-model-invocation: true` and are never
  `REQUIRED SUB-SKILL` targets. `establish-project` is user-invoked; `check-invariants`
  is model-invoked.
- **ID immutability:** never renumber an Approved requirement or invariant; retire by
  strikethrough.
- Commit each task with an `Implements: PROJDOC-N.M` trailer.

## File Structure

**Create:**
- `templates/product-vision.md` — vision/PRD seed.
- `templates/architecture-INDEX.md` — invariant-spine seed (ARCH-N grammar).
- `templates/product-guidelines.md` — engineering-guidelines seed.
- `skills/project/establish-project/SKILL.md` — tri-modal authoring skill.
- `skills/review/check-invariants/SKILL.md` — advisory conformance skill.
- `docs/architecture/INDEX.md` — this repo's own ARCH-1..5 (dogfood).
- `docs/specs/2026-07-12-project-docs-layer/baselines/BNN-<slug>.md` — **one baseline
  file per task** (B01–B12), so no two tasks share a Test file and the declared
  parallel waves stay parallel.

**Modify:**
- `skills/discovery/brainstorm/SKILL.md` — Step 1 vision-scope consult.
- `skills/spec/write-design/SKILL.md` — Step 1 invariant inputs + `Respects:` + ADR-or-supersede.
- `skills/spec/write-plan/SKILL.md` — Global Constraints: spine rules + guidelines sourcing.
- `skills/execution/execute-plan/SKILL.md` — per-task-loop invariant surfacing + review conformance.
- `skills/review/code-review/SKILL.md` — step 3b + advisory `## Invariants` lane.
- `skills/execution/trace/SKILL.md` — passes 5–6, codes E4/E5/W3, gated.
- `skills/setup/setup-repo/SKILL.md` — decision 2G + Step 4 seed + migration.
- `skills/setup/scaffold-project/SKILL.md` — Step 2.8 seed.
- `templates/agents/project.md` — machine-config framing + pointer to guidelines.
- `.claude-plugin/plugin.json` — append the two new skills.
- `AGENTS.md`, `DESIGN.md`, `docs/guide/**` — inventory, count → 35, project-layer section, skill pages.

---

### Task 1: Doc templates (vision, architecture spine, guidelines)

**Files:**
- Create: `templates/product-vision.md`, `templates/architecture-INDEX.md`, `templates/product-guidelines.md`
- Test: `docs/specs/2026-07-12-project-docs-layer/baselines/B01-templates.md`

**Interfaces:**
- Produces: the three template paths; the `**ARCH-N**` invariant grammar (bold ID +
  one imperative sentence; per-domain files listed from `INDEX.md`; retire via
  `~~**ARCH-N**~~ superseded by ARCH-M`).

**Depends-on:** none

- [ ] **Step 1 (scenario):** Write baseline scenario B1 to `baselines/B01-templates.md`:
  "Filling each template yields a well-formed
  vision / spine / guidelines doc; the arch
  template shows the ARCH-N grammar and a per-domain example. `[PROJDOC-1.2]
  [PROJDOC-1.5] [PROJDOC-2.2]`"
- [ ] **Step 2 (implement):** Write the three templates. `architecture-INDEX.md`
  defines the `**ARCH-N**` grammar, a per-domain split example, and the strikethrough
  retirement rule. `product-vision.md` slots: problem, users, goals, non-goals, scope
  boundaries. `product-guidelines.md` slots: coding standards, naming/i18n, house
  rules. Every heading is a REQUIRED slot (fill-or-`None`), matching existing
  `templates/` convention.
- [ ] **Step 3 (verify + commit):** Walk B1 against the templates. Commit
  `Implements: PROJDOC-1.2, PROJDOC-1.5, PROJDOC-2.2`.

_Requirements: PROJDOC-1.2, PROJDOC-1.5, PROJDOC-2.2_

---

### Task 2: `establish-project` skill (tri-modal) + registration

**Files:**
- Create: `skills/project/establish-project/SKILL.md`
- Modify: `.claude-plugin/plugin.json` (append skill path), `AGENTS.md` (inventory), `DESIGN.md` (inventory)
- Test: `docs/specs/2026-07-12-project-docs-layer/baselines/B02-establish-project.md`

**Interfaces:**
- Consumes: the three template paths (Task 1); `check-invariants` (Task 3, called in
  validate mode); `grilling`, `domain-modeling` as REQUIRED SUB-SKILLs.
- Produces: user-invoked skill `establish-project` with modes create / update / validate.

**Depends-on:** Task 1, Task 3

- [ ] **Step 1 (scenario):** Append B2: "Create mode produces vision.md + spine +
  guidelines from templates via grilling; update mode revises + routes hard decisions
  to the ADR gate + strikes retired invariants; validate mode runs check-invariants.
  Skill is user-invoked, in `skills/project/`. `[PROJDOC-1.1] [PROJDOC-1.3]
  [PROJDOC-1.4] [PROJDOC-2.1] [PROJDOC-2.3] [PROJDOC-7.1] [PROJDOC-8.3]`"
- [ ] **Step 2 (implement):** Write `SKILL.md` with frontmatter (`disable-model-invocation:
  true`; description = triggers + "repo-level vision, architecture spine, and
  guidelines" outcome). Body: mode routing; create (grilling interview → fill the 3
  templates; brownfield ratifies existing code); update (change signal → revise; ADR
  gate via `domain-modeling`; strike-don't-renumber); validate (checklist +
  `REQUIRED SUB-SKILL: use \`check-invariants\``). Append its path to
  `plugin.json` `skills[]`; add a row to the `AGENTS.md` and `DESIGN.md` inventories.
- [ ] **Step 3 (verify + commit):** Walk B2. Commit `Implements: PROJDOC-1.1,
  PROJDOC-1.3, PROJDOC-1.4, PROJDOC-2.1, PROJDOC-2.3, PROJDOC-7.1, PROJDOC-8.3`.

_Requirements: PROJDOC-1.1, PROJDOC-1.3, PROJDOC-1.4, PROJDOC-2.1, PROJDOC-2.3, PROJDOC-7.1, PROJDOC-8.3_

---

### Task 3: `check-invariants` skill (advisory conformance) + registration

**Files:**
- Create: `skills/review/check-invariants/SKILL.md`
- Modify: `.claude-plugin/plugin.json`, `AGENTS.md`, `DESIGN.md` (inventory)
- Test: `docs/specs/2026-07-12-project-docs-layer/baselines/B03-check-invariants.md`

**Interfaces:**
- Consumes: the `**ARCH-N**` grammar + spine path (Task 1); a `design.md` or diff.
- Produces: model-invoked `check-invariants`; per `Respects: ARCH-N` citation a
  verdict `respects | violates | unclear` + rationale. Advisory, never a gate.

**Depends-on:** Task 1

- [ ] **Step 1 (scenario):** Append B3: "Given a design citing `Respects: ARCH-2` and
  the spine, check-invariants returns a per-citation verdict + rationale; it is
  model-invoked and advisory (no pass/fail gate). `[PROJDOC-8.1] [PROJDOC-8.4]`"
- [ ] **Step 2 (implement):** Write `SKILL.md`: frontmatter (model-invoked;
  description = triggers + "advisory invariant-conformance verdicts" outcome). Body:
  input (design/diff + spine), per-citation judgment, verdict vocabulary, explicit
  "advisory, LLM-judged, distinct from the deterministic `trace` check — never a hard
  gate." Register in `plugin.json` + inventories.
- [ ] **Step 3 (verify + commit):** Walk B3. Commit `Implements: PROJDOC-8.1, PROJDOC-8.4`.

_Requirements: PROJDOC-8.1, PROJDOC-8.4_

---

### Task 4: `trace` referential-integrity extension

**Files:**
- Modify: `skills/execution/trace/SKILL.md` (add passes 5–6 after pass 4 ~line 108; add E4/E5/W3 to the codes table ~line 24-30 and rules ~line 110-125; extend the `<NON-NEGOTIABLE>` block ~line 135)
- Test: `docs/specs/2026-07-12-project-docs-layer/baselines/B04-trace.md`

**Interfaces:**
- Consumes: `docs/architecture/*.md` (spine), `docs/specs/**/design.md` (`Respects:` lines).
- Produces: finding codes E4 (Respects cites undefined ARCH), E5 (cites retired ARCH),
  W3 (live ARCH cited by no design). All gated on `docs/architecture/` existing.

**Depends-on:** Task 1

- [ ] **Step 1 (scenario):** Append B4: "On a fixture with `docs/architecture/INDEX.md`
  (ARCH-1 live, ARCH-9 struck) and designs citing ARCH-1, ARCH-9, ARCH-5: trace
  reports W3 for an uncited live ARCH, E5 for the ARCH-9 citation, E4 for ARCH-5. On a
  repo with NO `docs/architecture/`, the finding set is byte-identical to today.
  `[PROJDOC-3.1] [PROJDOC-3.2] [PROJDOC-3.3] [PROJDOC-3.4] [PROJDOC-3.5]`"
- [ ] **Step 2 (implement):** Add **Pass 5** (grep struck `~~**ARCH-N**~~` into a
  retired set; then `sed`-delete struck spans and take survivors as live —
  `grep -rnE '\*\*ARCH-[0-9]+\*\*' docs/architecture`). Add **Pass 6** (`grep -rnE
  'Respects:.*ARCH-[0-9]+' docs/specs --include='*design.md'`). Add rules: E4 (cited,
  in neither set), E5 (cited, in retired set), W3 (live, uncited). Guard: skip 5/6
  when `docs/architecture/` absent. Extend `<NON-NEGOTIABLE>` with one sentence:
  invariant passes check existence/liveness only, never semantic respect (that is
  `check-invariants`/`code-review`).
- [ ] **Step 3 (verify + commit):** Walk B4 (both branches). Commit `Implements:
  PROJDOC-3.1, PROJDOC-3.2, PROJDOC-3.3, PROJDOC-3.4, PROJDOC-3.5`.

_Requirements: PROJDOC-3.1, PROJDOC-3.2, PROJDOC-3.3, PROJDOC-3.4, PROJDOC-3.5_

---

### Task 5: Consult hooks in `brainstorm` and `write-design`

**Files:**
- Modify: `skills/discovery/brainstorm/SKILL.md` (Step 1, ~line 52-53), `skills/spec/write-design/SKILL.md` (Step 1, ~line 16-26; ADR-or-supersede reuse ~line 25-26,88-90)
- Test: `docs/specs/2026-07-12-project-docs-layer/baselines/B05-brainstorm-writedesign.md`

**Interfaces:**
- Consumes: `docs/product/vision.md`, the spine + `Respects: ARCH-N` convention (Task 1).
- Produces: the two read-hooks; write-design emits `Respects: ARCH-N` lines.

**Depends-on:** Task 1

- [ ] **Step 1 (scenario):** Append B5: "With a vision.md present, brainstorm Step 1
  states whether a new idea is in product scope. With a spine present, write-design
  cites `Respects: ARCH-N` and routes a contradicting design through the
  ADR-or-supersede gate. `[PROJDOC-4.1] [PROJDOC-4.2] [PROJDOC-4.3]`"
- [ ] **Step 2 (implement):** brainstorm Step 1: after the CONTEXT.md/INDEX.md read,
  add "WHERE `docs/product/vision.md` exists, check the idea's scope against it and
  state in/out of product scope; else continue" (no-op idiom). write-design Step 1:
  add "WHERE a spine exists, its invariants are inputs; cite each relied-upon one
  `Respects: ARCH-N`; a design that must contradict one is an ADR-or-supersede event
  (existing gate)."
- [ ] **Step 3 (verify + commit):** Walk B5. Commit `Implements: PROJDOC-4.1,
  PROJDOC-4.2, PROJDOC-4.3`.

_Requirements: PROJDOC-4.1, PROJDOC-4.2, PROJDOC-4.3_

---

### Task 6: `execute-plan` invariant awareness

**Files:**
- Modify: `skills/execution/execute-plan/SKILL.md` (Per-Task Loop: brief assembly ~step 2 line 32; task review ~step 7 line 37)
- Test: `docs/specs/2026-07-12-project-docs-layer/baselines/B06-execute-plan.md`

**Interfaces:**
- Consumes: the spine (Task 1); `check-invariants` (Task 3).
- Produces: task briefs that surface relevant invariants; task review that runs
  `check-invariants` and routes violations back.

**Depends-on:** Task 3

- [ ] **Step 1 (scenario):** Append B6: "With a spine present, an execute-plan task
  brief lists the invariants relevant to the task's files, and the task review runs
  check-invariants, routing a `violates` verdict back for fixes. With no spine, briefs
  and reviews are unchanged. `[PROJDOC-4.6] [PROJDOC-4.7]`"
- [ ] **Step 2 (implement):** In the brief-assembly step, add "WHERE a spine exists,
  include the invariants relevant to this task's touched files." In the task-review
  step, add "WHERE a spine exists, `REQUIRED SUB-SKILL: use \`check-invariants\`` on
  the task diff; a `violates` verdict routes back for fixes." Both no-op when absent.
- [ ] **Step 3 (verify + commit):** Walk B6 (both branches). Commit `Implements:
  PROJDOC-4.6, PROJDOC-4.7`.

_Requirements: PROJDOC-4.6, PROJDOC-4.7_

---

### Task 7: `write-plan` constraint sourcing + guidelines split

**Files:**
- Modify: `skills/spec/write-plan/SKILL.md` (Step 1 Global Constraints, ~line 22-25), `templates/agents/project.md` (machine-config framing + pointer line)
- Test: `docs/specs/2026-07-12-project-docs-layer/baselines/B07-write-plan.md`

**Interfaces:**
- Consumes: the spine (Task 1); `docs/product/guidelines.md` when present.
- Produces: Global Constraints that fold spine hard-rules and source engineering rules
  from guidelines (else `project.md`).

**Depends-on:** Task 1

- [ ] **Step 1 (scenario):** Append B7: "With a spine + guidelines.md present,
  write-plan's Global Constraints include the spine's hard rules and read engineering
  rules from guidelines.md; with neither, it reads from project.md as today.
  project.md template carries a pointer to guidelines.md. `[PROJDOC-4.4] [PROJDOC-7.2]
  [PROJDOC-7.3] [PROJDOC-7.5]`"
- [ ] **Step 2 (implement):** In Step 1, extend the constraint-source sentence: "WHERE
  a spine exists, fold its hard rules into Global Constraints; source engineering rules
  from `docs/product/guidelines.md` when it exists, else `docs/agents/project.md`."
  Edit `templates/agents/project.md` to frame it as machine-config and add a pointer
  line to `docs/product/guidelines.md`.
- [ ] **Step 3 (verify + commit):** Walk B7 (both branches). Commit `Implements:
  PROJDOC-4.4, PROJDOC-7.2, PROJDOC-7.3, PROJDOC-7.5`.

_Requirements: PROJDOC-4.4, PROJDOC-7.2, PROJDOC-7.3, PROJDOC-7.5_

---

### Task 8: `code-review` advisory invariant lane

**Files:**
- Modify: `skills/review/code-review/SKILL.md` (add step 3b after 3a ~line 42; add `## Invariants (advisory)` to step 5 aggregate ~line 54-56)
- Test: `docs/specs/2026-07-12-project-docs-layer/baselines/B08-code-review.md`

**Interfaces:**
- Consumes: `check-invariants` (Task 3); the spine.
- Produces: an advisory third lane in the review report; the two hard axes untouched.

**Depends-on:** Task 3

- [ ] **Step 1 (scenario):** Append B8: "With a spine present, code-review runs
  check-invariants and reports verdicts under `## Invariants (advisory)`, separate
  from Standards/Spec; with no spine, code-review is unchanged. `[PROJDOC-8.2]
  [PROJDOC-8.5]`"
- [ ] **Step 2 (implement):** Add step "3b. Invariant conformance — WHERE
  `docs/architecture/` exists, `REQUIRED SUB-SKILL: use \`check-invariants\`` on the
  diff; else skip." In step 5, add a `## Invariants (advisory)` section for the
  verdicts, explicitly kept out of the Standards/Spec no-rerank axes.
- [ ] **Step 3 (verify + commit):** Walk B8 (both branches). Commit `Implements:
  PROJDOC-8.2, PROJDOC-8.5`.

_Requirements: PROJDOC-8.2, PROJDOC-8.5_

---

### Task 9: `setup-repo` opt-in, seed, and guidelines migration

**Files:**
- Modify: `skills/setup/setup-repo/SKILL.md` (Step 2 add decision G after 2F ~line 114; Step 4 seed after ~line 132; `## Agent skills` block ~line 151-169; the "six
  decisions" count at ~line 41)
- Test: `docs/specs/2026-07-12-project-docs-layer/baselines/B09-setup-repo.md`

**Interfaces:**
- Consumes: the three templates (Task 1).
- Produces: decision 2G (default No); on opt-in, seeds the 3 docs + an Agent-skills
  line + a migration offer.

**Depends-on:** Task 1

- [ ] **Step 1 (scenario):** Append B9: "setup-repo offers decision G (project-docs
  layer, default No). Opting in seeds vision/spine/guidelines, adds a project-docs
  line to `## Agent skills`, and offers to migrate existing project.md guidelines into
  guidelines.md. Declining changes nothing. `[PROJDOC-5.1] [PROJDOC-5.2] [PROJDOC-5.4]
  [PROJDOC-7.4]`"
- [ ] **Step 2 (implement):** Add decision **G. Project-docs layer** to Step 2 (default
  No, one-at-a-time style), and update the Step 2 "six decisions" count to **seven**
  (`setup-repo/SKILL.md:41`). In Step 4, on opt-in: seed the three docs from templates
  (additive, never clobber), add the Agent-skills line, and — if `project.md` already
  has guidelines — offer migration into `guidelines.md` leaving a pointer.
- [ ] **Step 3 (verify + commit):** Walk B9 (opt-in and decline). Commit `Implements:
  PROJDOC-5.1, PROJDOC-5.2, PROJDOC-5.4, PROJDOC-7.4`.

_Requirements: PROJDOC-5.1, PROJDOC-5.2, PROJDOC-5.4, PROJDOC-7.4_

---

### Task 10: `scaffold-project` seed

**Files:**
- Modify: `skills/setup/scaffold-project/SKILL.md` (Step 2.8 Docs seeds, ~line 74)
- Test: `docs/specs/2026-07-12-project-docs-layer/baselines/B10-scaffold.md`

**Interfaces:**
- Consumes: the templates (Task 1); the opt-in mechanism (Task 9).
- Produces: greenfield seeding of the three docs when opted in.

**Depends-on:** Task 1, Task 9

- [ ] **Step 1 (scenario):** Append B10: "On a greenfield scaffold with the layer
  opted in, Step 2.8 seeds vision/spine/guidelines beside CONTEXT.md and
  docs/specs/INDEX.md; not opted in, it seeds neither. `[PROJDOC-5.3]`"
- [ ] **Step 2 (implement):** In Step 2.8, add "WHERE the layer is opted in, seed the
  three project docs from templates alongside the existing seeds."
- [ ] **Step 3 (verify + commit):** Walk B10. Commit `Implements: PROJDOC-5.3`.

_Requirements: PROJDOC-5.3_

---

### Task 11: Optionality + no-op verification across hooks

**Files:**
- Test: `docs/specs/2026-07-12-project-docs-layer/baselines/B11-optionality.md`

**Interfaces:**
- Consumes: all hooks (Tasks 5–10).
- Produces: baseline scenarios proving the absent-doc no-op branch and whole-workflow
  optionality.

**Depends-on:** Task 5, Task 6, Task 7, Task 8, Task 9, Task 10

- [ ] **Step 1 (scenario):** Append B11: "On a repo with no `docs/product/` and no
  `docs/architecture/`, brainstorm / write-design / write-plan / execute-plan / trace
  / code-review behave identically to pre-feature; each hook takes its no-op branch
  and says so at most once. `[PROJDOC-4.5] [PROJDOC-6.1]`"
- [ ] **Step 2 (implement):** Walk every modified skill's hook and confirm the
  else-branch is a clean no-op matching `brainstorm/SKILL.md:53`; record the walk as
  B11. (No content change expected — this task is the cross-cutting audit; fix any
  hook that gates instead of no-ops.)
- [ ] **Step 3 (verify + commit):** Confirm B11 passes. Commit `Implements:
  PROJDOC-4.5, PROJDOC-6.1`.

_Requirements: PROJDOC-4.5, PROJDOC-6.1_

---

### Task 12: Dogfood spine + DESIGN/AGENTS/guide reconciliation

**Files:**
- Create: `docs/architecture/INDEX.md`
- Modify: `DESIGN.md` (add "The project layer" section; skill count → 35; inventory), `AGENTS.md` (count → 35; inventory; file-org), `docs/guide/**` (overview phase table + `establish-project` and `check-invariants` skill pages)
- Test: `docs/specs/2026-07-12-project-docs-layer/baselines/B12-dogfood.md`

**Interfaces:**
- Consumes: both new skills (Tasks 2, 3).
- Produces: this repo's own `ARCH-1..5`; reconciled docs at count 35.

**Depends-on:** Task 2, Task 3

- [ ] **Step 1 (scenario):** Append B12: "This repo has `docs/architecture/INDEX.md`
  with ARCH-1..5 (determinism-of-trace, optionality, zero-tooling, ID immutability,
  sub-skill composition); DESIGN.md/AGENTS.md/guide agree on 35 skills and describe
  the project layer; adds no mandatory tooling or gate. `[PROJDOC-6.2]`"
- [ ] **Step 2 (implement):** Create `docs/architecture/INDEX.md` with ARCH-1..5 (per
  the design). Add a "The project layer" section to `DESIGN.md`, reconcile the skill
  count to **35** across `DESIGN.md`, `AGENTS.md`, and the guide (fixing the 31/32/33
  drift), add the two skills to the inventories/file-org, and add overview-table rows
  + one guide page per new skill.
- [ ] **Step 3 (verify + commit):** Walk B12; run `trace` and confirm the new spine
  passes (no E4/E5 self-citations). Commit `Implements: PROJDOC-6.2`.

_Requirements: PROJDOC-6.2_

---

## Coverage self-check

All 36 PROJDOC IDs cited by exactly one task footer:

- T1: 1.2, 1.5, 2.2 · T2: 1.1, 1.3, 1.4, 2.1, 2.3, 7.1, 8.3 · T3: 8.1, 8.4
- T4: 3.1, 3.2, 3.3, 3.4, 3.5 · T5: 4.1, 4.2, 4.3 · T6: 4.6, 4.7
- T7: 4.4, 7.2, 7.3, 7.5 · T8: 8.2, 8.5 · T9: 5.1, 5.2, 5.4, 7.4 · T10: 5.3
- T11: 4.5, 6.1 · T12: 6.2

Test tags: every ID appears in a `[PROJDOC-N.M]`-tagged baseline scenario, one file
per task under `baselines/B01…B12-*.md` — the covering evidence for this repo (Global
Constraints). No two tasks share a Test file, so the declared parallel waves hold.
Matches the design seam table. No ID uncited; none double-cited.
