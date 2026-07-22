# Tasks: Team structure in setup-repo

> **For agentic workers:** REQUIRED SUB-SKILL: use `execute-plan` to implement
> this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

Feature code: TEAM
Status: Approved
Date: 2026-07-22
Requirements: ./requirements.md
Design: ./design.md
Execution: inline (no worktree)

**Goal:** Persist a confirmed team roster and workflow band in `docs/agents/project.md`, capture it during `setup-repo` from local metadata, and have high-impact skills package collaboration by band without weakening Iron Laws.

**Architecture:** Extend the posture pattern: a structured `## Team` section is the single source of truth for roster, ownership notes, band derivation, and the packaging matrix. `setup-repo` Decision **H** (infer-then-confirm; former project-docs renumbered to **I**) writes that section. High-impact skills read `## Team` when present and package outputs by band; they do not re-author band rules. Inference detail lives behind a disclosed pointer beside setup-repo to keep the skill body lean (`writing-great-skills` hierarchy).

**Tech Stack:** Markdown skills/templates/guides; verification via structural greps, scenario fixtures under the feature spec, and `writing-skills` RED/GREEN pressure scenarios (no app runtime). Leading words (use consistently in skill text): **roster**, **band**, **packaging**, **infer-then-confirm**, **posture pattern**.

## Global Constraints

Copied for every implementer brief:

1. **writing-great-skills / writing-skills quality bar (mandatory on every skill edit):**
   - **Predictability** over identical output — same *process* every run.
   - **Single source of truth:** band derivation + packaging matrix live **only** in `templates/agents/project.md` `## Team` (and thus in written `docs/agents/project.md`). Consumers **read** that section; they do **not** re-copy the derivation algorithm. (Improves design Approach A’s seven-way copy — same Satisfies IDs, less **duplication** / **sediment**.)
   - **Progressive disclosure:** long inference recipe → `skills/setup/setup-repo/team-inference.md` with a strong context pointer (“WHEN Decision H runs, read `team-inference.md` beside this file and follow it exactly”). Keep setup-repo `SKILL.md` under ~500 lines.
   - **Form matches failure:** wrong output *shape* → positive **recipe** (ordered slots); conditional behavior → observable predicate (`IF ## Team present…`); pressure-resistant gates → hard rule + rationalization row only where agents rationalize past the rule.
   - **Leading words:** prefer **band**, **roster**, **packaging**, **infer-then-confirm** over restated multi-sentence synonyms.
   - **Completion criteria:** every new/edited step ends with a checkable **Done when**.
   - **No-op sweep:** delete whole sentences that don’t change behavior vs default.
   - **Negation:** state the positive packaging recipe; keep hard “never skip Iron Laws” as an explicit gate (allowed exception for pressure gates).
   - **Description discipline:** setup-repo stays user-invoked (`disable-model-invocation: true`); description = trigger + outcome noun, **no workflow steps**. Add human-facing keywords: team, CODEOWNERS, contributors, roster — not a process summary.
   - **RED before GREEN:** for each skill body change, baseline the scenario against the *current* text first; record verbatim failures; write minimal text; re-run. Do not author skill prose before RED for that slice. Methodology: `skills/meta/writing-skills/pressure-testing.md` (or the installed sibling under writing-skills).
   - **Cross-refs:** `REQUIRED SUB-SKILL: use \`name\`` prose only; no `@` links into other skill folders.

2. **Design lettering:** Decision **H = Team**, Decision **I = project-docs (optional)**. Renumber every former “decision H” project-docs reference.

3. **Local-only inference:** git / CODEOWNERS / AUTHORS / CONTRIBUTORS / package.json only. No `gh`/`glab` collaborator APIs. CODEOWNERS: all tokens → Ownership notes; human-like only → Roster.

4. **Band precedence (must match template prose exactly):** override if set → headcount (1 Solo / 2–4 Small / ≥5 Multi; empty roster = no band) → specialty upgrade Small→Multi if ≥3 distinct role titles.

5. **Packaging only:** Solo does not skip code-review, tdd, verify, or root-cause. No new mandatory `tasks.md` Owner field; optional freeform notes only.

6. **Additive write:** never clobber non-Team sections of `project.md`.

7. **Test annotations:** every requirement ID appears in a scenario or structural check tagged with the ID string `TEAM-N.M` under **`tests/team-structure/`** (repo-root `tests/` so the `trace` skill’s default roots include them; path segment `/tests/` counts as a test file).

8. **Commits:** include `Implements: TEAM-N.M` (or multiple) trailers. Prefer one commit per task.

9. **Forbidden:** new model-invoked team-context skill; `docs/agents/team.md`; weakening Iron Laws by band; inventing names/roles not in metadata or user confirm.

10. **No docs/agents/project.md verify commands in this skill-set repo** — structural/scenario checks are the proving commands for this feature.

## File Structure

| Path | Responsibility |
|---|---|
| `templates/agents/project.md` | Canonical `## Team` schema, band rules, packaging matrix (SSOT) |
| `skills/setup/setup-repo/SKILL.md` | Decision H, renumber I, Step 1 gap, Step 4 write, Agent-skills bullet, description keywords |
| `skills/setup/setup-repo/team-inference.md` | Disclosed inference recipe (git/CODEOWNERS/manifests, confirm gate) |
| `skills/discovery/brainstorm/SKILL.md` | Read Team → packaging by band |
| `skills/discovery/grilling/SKILL.md` | Additive Small/Multi ownership probes |
| `skills/spec/write-plan/SKILL.md` | Optional freeform owner notes by band |
| `skills/execution/execute-plan/SKILL.md` | Load band; brief packaging; dual review untouched |
| `skills/review/code-review/SKILL.md` | Ownership-aware packaging |
| `skills/ship/finish-branch/SKILL.md` | PR reviewer packaging prose |
| `skills/track/handoff/SKILL.md` | Team/band line in handoff contents |
| `docs/guide/skills/setup-repo.md` | Human guide for Decision H/I |
| `docs/guide/resources/adopting.md` | Brief team composition mention; fix decision count |
| `docs/guide/skills/establish-project.md` | Project-docs decision letter → I |
| `AGENTS.md` | Per-repo config blurb includes Team |
| `tests/team-structure/scenarios.md` | Tagged scenario/structural checks covering all TEAM IDs |
| `tests/team-structure/red-baselines.md` | RED transcripts / expected baseline failures per skill slice |

---

### Task 1: Team SSOT in project template + scenario harness

**Files:**
- Create: `tests/team-structure/scenarios.md`
- Create: `tests/team-structure/red-baselines.md` (stub sections for later tasks)
- Modify: `templates/agents/project.md` — insert `## Team` after `## Project posture`, before `## Verify commands`
- Test: `tests/team-structure/scenarios.md`

**Reuse:** existing — mirrors `## Project posture` block in `templates/agents/project.md` (rung 2)

**Interfaces:**
- Consumes: design §1 schema + band precedence + packaging matrix
- Produces: canonical `## Team` shape that every later task’s skills must read (not re-author)

**Depends-on:** none

- [ ] **Step 1: Write the failing structural checks**

In `tests/team-structure/scenarios.md`, create harness skeleton with partitioned sections (later tasks append only to their section):

```markdown
# TEAM structural and scenario checks

## S-template
### S-TEAM-2.1 template has ## Team
<!-- TEAM-2.1 TEAM-2.3 TEAM-2.4 TEAM-2.6 -->
Assert `templates/agents/project.md` contains:
- heading `## Team` after `## Project posture` and before `## Verify commands`
- `### Roster` with Role — Name | N × Role guidance
- suggested roles list (Tech Lead, Backend/Frontend/Full-stack Engineer, Designer,
  Product Manager, QA, DevOps/SRE, Docs)
- `### Ownership notes`
- `### Workflow band` with override + derive precedence (SSOT; no “copy into consumers”)
- **packaging matrix** table for Solo / Small / Multi / (no band)

## S-setup-repo
<!-- Task 2 appends here -->

## S-consumers
<!-- Task 3 appends here -->

## S-docs
<!-- Task 4 appends here -->

## Coverage
<!-- Task 5 fills -->
```

Also create `tests/team-structure/red-baselines.md` with empty `## RED-setup-repo` and `## RED-consumers` stubs.

Also assert IDs appear as greppable comments or headers: `TEAM-2.1`, `TEAM-2.3`, `TEAM-2.4`, `TEAM-2.6`.

Run: `rg -n "TEAM-2\.[1346]" tests/team-structure/scenarios.md` — expect: present.  
Run: `rg -n "^## Team" templates/agents/project.md` — expect: no match (RED).

- [ ] **Step 2: Implement template `## Team`**

Insert the full section per design §1 **as SSOT**: include packaging matrix table (Solo / Small / Multi / no band) in this section. **Do not** include any “copy into every consumer” wording — consumers only **read** this section. Intro blurb: skills read this for **packaging** only; Iron Laws unchanged; edit freely or re-run `/setup-repo`.

Run structural asserts — expect: pass.

- [ ] **Step 3: No-op / leading-word pass on template prose**

Apply writing-great-skills: collapse restated synonyms to **roster** / **band** / **packaging**; delete pure no-op sentences; keep completion-facing edit guidance.

- [ ] **Step 4: Commit**

`git commit` with message noting Team SSOT template + scenario harness; trailers `Implements: TEAM-2.1, TEAM-2.3, TEAM-2.4, TEAM-2.6`.

_Requirements: TEAM-2.1, TEAM-2.3, TEAM-2.4, TEAM-2.6_

---

### Task 2: setup-repo Decision H + disclosed inference + write path

**Files:**
- Create: `skills/setup/setup-repo/team-inference.md`
- Modify: `skills/setup/setup-repo/SKILL.md` (Step 1 gap, Step 2 H/I, Step 3 draft includes Team, Step 4 Team fill + renumber write items + Agent-skills bullet, description keywords)
- Modify: `tests/team-structure/scenarios.md` — **append only** section `## S-setup-repo` (do not edit Task 1 or Task 3 sections)
- Modify: `tests/team-structure/red-baselines.md` — **append only** `## RED-setup-repo`
- Test: scenario + structural greps under `## S-setup-repo` in `tests/team-structure/scenarios.md`

**Reuse:** existing — Step 2 decision pattern A–G and Step 4 additive write in `skills/setup/setup-repo/SKILL.md` (rung 2)

**Interfaces:**
- Consumes: Task 1 `## Team` SSOT shape
- Produces: Decision **H** contract; Decision **I** = project-docs; inference pointer; Agent-skills Team bullet text

**Depends-on:** Task 1

- [ ] **Step 1: RED baselines for setup-repo**

Scenarios (record under `## RED-setup-repo` in `red-baselines.md` before editing SKILL.md):

1. **Rich metadata (TEAM-1.1–1.4, 1.6–1.7, 5.1):** agent runs setup-repo on a fixture with multi-author git + CODEOWNERS; pressure: time + “just invent roles from commits” + “use gh api for collaborators”. Expect baseline: invents titles, skips confirm, and/or calls remote APIs.
2. **Empty metadata (TEAM-1.5, 1.7):** no CODEOWNERS, single unknown email; expect invents people/roles or writes without confirm.
3. **Fill-the-gaps (TEAM-1.8, 2.2):** project.md complete except no `## Team`; expect skips Team or rebuilds whole file.
4. **Guards (TEAM-6.1, 6.3):** Step 1 still file-only; walk decisions **A–I** one-at-a-time (H = Team, I = optional project-docs); Step 6 still required; no Step-1 service probe.

Tag scenario headers with `TEAM-1.1` … as applicable. Do **not** write Decision H text until baselines are recorded.

- [ ] **Step 2: Write failing structural asserts for Decision H**

In `scenarios.md`, asserts that must fail pre-edit:

- SKILL.md contains `### H. Team` and `### I. Project-docs` (not Team as I)
- pointer to `team-inference.md` with load condition “WHEN Decision H runs…”
- Agent-skills block bullet mentioning `## Team`
- description includes keywords team / CODEOWNERS / contributors / roster without listing workflow steps
- no collaborator API in inference path

Run greps — expect: RED.

- [ ] **Step 3: Author `team-inference.md` (disclosed reference)**

Recipe only (TOC if >100 lines): repo age; shortlog top 10; bot drop; CODEOWNERS paths; Ownership notes vs human Roster split; manifests; role defaults (Contributor, never invent titles); present draft; **confirm gate**; forbidden remote APIs. End each major step with **Done when**.

- [ ] **Step 4: Patch `setup-repo/SKILL.md` (minimal GREEN)**

- Description: trigger + outcome; add team/CODEOWNERS/contributors/roster keywords; keep `disable-model-invocation: true`; no workflow dump.
- Step 1: missing `## Team` = gap.
- Step 2: nine decisions A–I; **### H. Team** after G — explainer → recommend → wait; **infer-then-confirm**; pointer MUST load `team-inference.md`; renumber project-docs to **### I**.
- Step 3: draft of `project.md` **includes confirmed `## Team`** before user approves write.
- Step 4 write order: (4) posture G → (5) **Team from H** → (6) project-docs seeds if **I** Yes → (7) Agent-skills (Team bullet; “if decision I was Yes” for project-docs line) → (8) gitignore. Additive merge only.
- Rationalization rows only for failures seen in RED (e.g. “use gh for collaborators” → reality: local only + confirm).
- No-op sweep; leading words; body stays within line budget (detail in team-inference.md).

- [ ] **Step 5: GREEN re-run structural greps + technique check**

Fresh read of Decision H + team-inference: agent produces a draft roster shape without writing before confirm; CODEOWNERS teams stay in Ownership notes. Update scenarios to PASS criteria.

- [ ] **Step 6: Commit**

Trailers covering `Implements: TEAM-1.1, TEAM-1.2, TEAM-1.3, TEAM-1.4, TEAM-1.5, TEAM-1.6, TEAM-1.7, TEAM-1.8, TEAM-2.2, TEAM-2.5, TEAM-5.1, TEAM-6.1, TEAM-6.3`.

_Requirements: TEAM-1.1, TEAM-1.2, TEAM-1.3, TEAM-1.4, TEAM-1.5, TEAM-1.6, TEAM-1.7, TEAM-1.8, TEAM-2.2, TEAM-2.5, TEAM-5.1, TEAM-6.1, TEAM-6.3_

---

### Task 3: High-impact skills — packaging by band

**Files:**
- Modify: `skills/discovery/brainstorm/SKILL.md`
- Modify: `skills/discovery/grilling/SKILL.md`
- Modify: `skills/spec/write-plan/SKILL.md`
- Modify: `skills/execution/execute-plan/SKILL.md`
- Modify: `skills/review/code-review/SKILL.md`
- Modify: `skills/ship/finish-branch/SKILL.md`
- Modify: `skills/track/handoff/SKILL.md`
- Modify: `tests/team-structure/scenarios.md` — **append only** section `## S-consumers` (do not edit S-setup-repo or Task 1 structural sections)
- Modify: `tests/team-structure/red-baselines.md` — **append only** `## RED-consumers`
- Test: `tests/team-structure/scenarios.md` section `## S-consumers` (TEAM-3.x, TEAM-6.2, TEAM-6.4)

**Reuse:** existing — each skill’s project.md / posture read site (rung 2); band/packaging SSOT from Task 1 template

**Interfaces:**
- Consumes: `## Team` SSOT (band + packaging matrix in project.md)
- Produces: per-skill **packaging** conditionals (no gate changes)

**Depends-on:** Task 2

Harness partition: Task 2 owns `## S-setup-repo` / `## RED-setup-repo`; Task 3 owns `## S-consumers` / `## RED-consumers`; Task 4 owns `## S-docs` only.

- [ ] **Step 1: RED baselines (per skill or batched transcripts)**

Scenarios with ≥3 pressures where relevant (Solo skip-review temptation is a gate):

| Case | IDs | Expected baseline failure |
|---|---|---|
| Team present Solo — invent multi-reviewer theater or skip review | TEAM-3.1, 3.2, 3.6 | packaging wrong and/or gate skip |
| Team present Small/Multi — no ownership language when names/notes exist | TEAM-3.3, 3.4 | packaging miss |
| Team absent — invent roster or hard-fail | TEAM-3.5, 6.4 | invent or block |
| Posture Prototype + Multi band — still skips migration questions by posture | TEAM-6.2 | confuses band with posture |

Record verbatim rationalizations in `red-baselines.md`.

- [ ] **Step 2: Failing asserts that skills mention Team packaging**

`rg` each SKILL.md for `## Team` or `Workflow band` / **packaging** — expect missing pre-edit.

- [ ] **Step 3: Minimal consumer patches (positive recipes)**

For each skill, insert an **observable conditional** only:

```
IF docs/agents/project.md has ## Team
   AND (non-empty Roster OR non-blank Workflow band override):
  read Roster, Ownership notes, Workflow band rules IN THAT SECTION
  apply packaging matrix IN THAT SECTION for the derived band
ELSE:
  pre-feature default / (no band) — same as Team absent
  (do not invent a team; do not hard-fail for missing Team)
WHILE packaging:
  Iron Law gates unchanged (Solo still runs review/tdd/verify/root-cause)
```

Skill-specific insertion points (design §5, improved wording):

| Skill | Where | Extra |
|---|---|---|
| brainstorm | Step 1 after posture | state band once; approach language by packaging matrix |
| grilling | posture right-size bullet | **add** ownership/reviewer probes only when Small/Multi; Solo/absent = no multi-person assignee theater |
| write-plan | project.md read / task bodies | optional freeform owner notes only — **no new required task field** |
| execute-plan | (a) after Setup step 3 load band (b) Per-Task brief packaging (c) dual-verdict steps **untouched** | |
| code-review | after gather standards | ownership-note emphasis; dual-axis always |
| finish-branch | Option 2 PR prose | suggest reviewers from roster/notes when Multi/Small; no new menu item |
| handoff | Contents | one-line team/band; Small/Multi ownership of next actions when relevant |

Do **not** paste the full band algorithm into each skill — **pointer:** “band and packaging matrix: `docs/agents/project.md` `## Team`”. That is the writing-great-skills SSOT fix.

Counter only rationalizations seen in RED (especially “Solo can skip review”).

- [ ] **Step 4: GREEN structural + technique spot-check**

Greps pass; one Solo and one Multi scenario shape-check (output packaging differs; gates named as still required).

- [ ] **Step 5: Commit**

`Implements: TEAM-3.1, TEAM-3.2, TEAM-3.3, TEAM-3.4, TEAM-3.5, TEAM-3.6, TEAM-6.2, TEAM-6.4`.

_Requirements: TEAM-3.1, TEAM-3.2, TEAM-3.3, TEAM-3.4, TEAM-3.5, TEAM-3.6, TEAM-6.2, TEAM-6.4_

---

### Task 4: Human docs + AGENTS constitution blurb

**Files:**
- Modify: `docs/guide/skills/setup-repo.md`
- Modify: `docs/guide/resources/adopting.md`
- Modify: `docs/guide/skills/establish-project.md` — project-docs decision letter → **I**
- Modify: `AGENTS.md` only (no separate Agents.md on this repo)
- Modify: `tests/team-structure/scenarios.md` — **append only** section `## S-docs`
- Test: structural greps under `## S-docs` in `tests/team-structure/scenarios.md`

**Reuse:** existing — guide mirrors under `docs/guide/` (rung 2)

**Interfaces:**
- Consumes: Decision H/I lettering and Team SSOT from Tasks 1–2
- Produces: human-facing docs aligned with skill behavior

**Depends-on:** Task 3

- [ ] **Step 1: Failing asserts**

`rg` guide for Decision H Team / band / local inference — expect miss. Same for adopting team composition bullet. AGENTS.md per-repo config mentions Team — expect miss. `establish-project.md` must not claim project-docs is decision G or H after this task (must be **I**).

Tag: `TEAM-4.1`, `TEAM-4.2`. Also structural: `rg -n "decision [GHI]|project-docs" docs/guide skills/setup` — no stale project-docs letter.

- [ ] **Step 2: Update docs**

- `setup-repo.md`: Decision **H** Team (infer-then-confirm, local sources, CODEOWNERS split, named vs count, band, consumers); **I** project-docs; decision count A–I.
- `adopting.md`: brief team composition under setup; fix stale “six decisions” to include G posture, H Team, I project-docs without duplicating the full skill guide.
- `establish-project.md`: project-docs offered by setup-repo as decision **I**.
- `AGENTS.md`: project.md holds verify commands, **Project posture**, and **Team**.

No-op sweep on new prose.

- [ ] **Step 3: Commit**

`Implements: TEAM-4.1, TEAM-4.2`.

_Requirements: TEAM-4.1, TEAM-4.2_

---

### Task 5: Full coverage gate + writing-skills ship checklist

**Files:**
- Modify: `tests/team-structure/scenarios.md` (ensure every TEAM ID tagged)
- Modify: `docs/specs/INDEX.md` (status when feature complete — leave until ship; this task only verifies plan coverage)
- Test: full ID list grep

**Reuse:** existing — design coverage table + writing-skills deployment checklist (rung 2)

**Interfaces:**
- Consumes: Tasks 1–4 outputs
- Produces: green coverage matrix in scenarios.md

**Depends-on:** Task 1, Task 2, Task 3, Task 4

- [ ] **Step 1: Coverage grep**

For every ID TEAM-1.1 … TEAM-6.4 (all IDs in requirements.md), assert appearance in `tests/team-structure/scenarios.md` **and** in at least one skill/template/guide path from Tasks 1–4.

```bash
# illustrative — implementer expands to full list
for id in TEAM-1.1 TEAM-1.2 TEAM-1.3 TEAM-1.4 TEAM-1.5 TEAM-1.6 TEAM-1.7 TEAM-1.8 \
  TEAM-2.1 TEAM-2.2 TEAM-2.3 TEAM-2.4 TEAM-2.5 TEAM-2.6 \
  TEAM-3.1 TEAM-3.2 TEAM-3.3 TEAM-3.4 TEAM-3.5 TEAM-3.6 \
  TEAM-4.1 TEAM-4.2 TEAM-5.1 TEAM-6.1 TEAM-6.2 TEAM-6.3 TEAM-6.4; do
  rg -q "$id" tests/team-structure/scenarios.md || echo "MISSING scenario: $id"
done
```

Expect: zero MISSING.

- [ ] **Step 2: writing-skills ship checklist (agent-run)**

For setup-repo + each modified consumer:

- [ ] Description (setup-repo): trigger + outcome, no workflow dump; keywords present
- [ ] Body within ~500 lines; team-inference disclosed one level deep
- [ ] No-op sweep done
- [ ] Cross-refs REQUIRED SUB-SKILL form
- [ ] setup-repo remains user-invoked; no skill auto-invokes it
- [ ] SSOT: no second full copy of band algorithm in consumers

- [ ] **Step 3: Commit coverage/docs-only fixes if any**

If only verification, empty commit not required — record pass in `tests/team-structure/scenarios.md` coverage section. If gaps found, fix in this task and commit with `Implements:` for any repaired IDs.

_Requirements: TEAM-1.1, TEAM-1.2, TEAM-1.3, TEAM-1.4, TEAM-1.5, TEAM-1.6, TEAM-1.7, TEAM-1.8, TEAM-2.1, TEAM-2.2, TEAM-2.3, TEAM-2.4, TEAM-2.5, TEAM-2.6, TEAM-3.1, TEAM-3.2, TEAM-3.3, TEAM-3.4, TEAM-3.5, TEAM-3.6, TEAM-4.1, TEAM-4.2, TEAM-5.1, TEAM-6.1, TEAM-6.2, TEAM-6.3, TEAM-6.4_

---

## Coverage and consistency notes (author)

| ID | Task footer | Tagged test location |
|---|---|---|
| TEAM-1.1–1.8 | Task 2 | scenarios + red-baselines |
| TEAM-2.1, 2.3, 2.4, 2.6 | Task 1 | scenarios structural |
| TEAM-2.2, 2.5 | Task 2 | scenarios |
| TEAM-3.1–3.6 | Task 3 | scenarios + red-baselines |
| TEAM-4.1–4.2 | Task 4 | scenarios |
| TEAM-5.1 | Task 2 | scenarios / RED remote-API pressure |
| TEAM-6.1, 6.3 | Task 2 | scenarios / RED guards |
| TEAM-6.2, 6.4 | Task 3 | scenarios |
| All IDs | Task 5 | full grep gate |

**writing-great-skills refinements (synced into design.md §1/§4/§6):**

1. Band + packaging matrix SSOT in `## Team` (consumers read, do not re-copy).
2. Inference recipe disclosed in `team-inference.md`.
3. Leading words and no-op discipline in Global Constraints and task steps.
4. RED baselines mandatory before skill prose (writing-skills Iron Law).
5. Serial tasks 2→3→4 for harness append partitions; establish-project letter → I.

**Upstream:** requirements.md unchanged. design.md updated for SSOT + establish-project renumber (still Approved; no requirement re-approval needed).
