# Execute family split — design (author-skills)

**Date:** 2026-07-30  
**Protocol:** `author-skills` + `pressure-testing.md`  
**Status:** Design locked · all three execute skills GREEN · plan-tasks/AGENTS/docs wire complete (2026-07-30)  
**Decisions (user 2026-07-30):** three independent skills; inline = sequential only; author `build-story-units` first

---

## 1. Why the current design fails

`build-continuous` is one skill with **two competing process cores**:

| Core | Dominant rule |
|---|---|
| **continuous** | Never pause between tasks; wave dispatch; subagent factory |
| **story-unit** | Stop after every review unit; human is the unlock; derive units from stories |

Pressure findings (`tests/pressure/reviewable-delivery/`) show the **barrier gate holds when loaded** — but production quality of story-unit runs is still weak for structural reasons that a rationalization table cannot fix:

### Failure classification (form match)

| Observed failure class | Form that fixes it | Why dual-mode text fails |
|---|---|---|
| Agent knows barrier rule, skips under EOD / "agent review clean" | Hard prohibition + rationalization table | Rule is a *mode branch* off continuous body; continuous narrative is default attention |
| Output shape wrong for unit summary / human unlock | Positive recipe | Unit barrier recipe lives in `story-unit-mode.md`; agents that only skim SKILL.md miss the recipe |
| Omits unit agent review before human | REQUIRED slot in barrier template | Buried after "same as task loop" |
| Picks continuous path when user wanted story stops | Distinct **trigger** (separate skill) | One description fires for both; process specialization never loads |
| Inline path is half-subagent loop | Separate skill + sequential recipe | "Inline Fallback" is a late section (~line 130), not a first-class entry |

**author-skills "When to split" — case 1 applies (genuinely distinct trigger):**

1. **continuous + subagents** → user/plan wants unattended multi-task orchestration  
2. **story-unit + subagents** → user wants human review units derived from stories  
3. **inline (no subagent)** → user or environment cannot/will not fan out implementers  

Case 2 (hiding post-completion steps) is secondary: `After the Last Task` chain is shared; the *mid-run* barrier is what competes with continuous "don't pause".

---

## 2. Target architecture (locked)

```
tasks.md header:
  Execution-mode: continuous | story-unit     # review-barrier policy only
                                              # never "inline"

plan-tasks Exit routes (how to run):
  1. build-continuous     if Execution-mode: continuous  (subagent waves)
  2. build-story-units    if Execution-mode: story-unit  (subagent + unit barriers)
  3. build-inline   user/capability choice         (controller implements;
                                                     sequential; ignores mode for barriers)
```

| Skill | Trigger (description outcome) | Owns | Does not own |
|---|---|---|---|
| **build-continuous** | Approved plan, continuous mode, subagent orchestration through finish chain | Per-task loop, parallel waves, continuous-only red flags | Unit barriers, story derivation |
| **build-story-units** | Approved plan, story-unit mode, human-gated review units | Unit partition recipe, per-unit barrier, mode-change write-back | Continuous "never pause", parallel waves (v1: serial units; waves *inside* a unit optional later) |
| **build-inline** | User chose inline / no subagent capability | Controller implements via `test-first`, same ledger shape, end `inspect-change` | Subagent dispatch, unit barriers |

### Shared assets (one home each — no meaning duplication)

| Asset | Home | Consumers |
|---|---|---|
| Implementer dispatch template | `execution/build-continuous/implementer-prompt.md` | build-continuous, build-story-units (pointer) |
| Task reviewer template | `execution/build-continuous/task-reviewer-prompt.md` | build-continuous, build-story-units (pointer) |
| Unit derivation + barrier recipe | moves to `execution/build-story-units/story-unit-mode.md` | build-story-units only; build-continuous drops preflight that requires it |
| Progress ledger contract | Document once in build-continuous Setup step 2; others pointer "same ledger line shape" | all three |
| After-last-task chain | build-continuous body; build-story-units/inline `REQUIRED SUB-SKILL` or short pointer to same sequence | all three |

Do **not** create `execution/shared/` until a fourth consumer appears — one extra folder for two pointers fails the token budget test.

---

## 3. `build-story-units` product shape (first to author)

**Leading words:** review unit · unit barrier · human unlock · mode change · ledger

**Iron laws (gates — authority form):**

1. Review units are **derived**, never authored in tasks.md  
2. After unit tasks clean: **unit agent review → STOP for human → unlock**  
3. "continue" after looking = next unit; "stop stopping" / "just run it all" = write `Execution-mode: continuous` then hand off to `build-continuous` (or continue continuous rules) — chat-only is not a mode change  
4. Ledger `Unit <k>: complete (...)` — resume reads it  
5. Whole-branch agent review still runs after last unit  

**Loop (recipe form):**

Setup (workspace, ledger, plan, todos, preflight partition, wave-of-units) →  
for each unit in order: for each task in unit: (shared per-task loop) → unit barrier →  
after last unit: whole-branch chain (same as build-continuous)

**Narrow vs current:**  
- No continuous path in this skill  
- No "Inline Fallback" section  
- Parallel waves: **out of scope for v1** unless unit has file-disjoint tasks — if needed, pointer to build-continuous Parallel waves recipe; default serial per unit to keep barrier simple  

**Description (draft — trigger-test before ship):**

```yaml
description: Use when an approved tasks.md has Execution-mode story-unit and
  needs human-gated review-unit execution — derived units, unit barriers,
  mode-change write-back, resume via unit ledger lines — through whole-branch
  review.
```

Must not summarize the full workflow as steps the agent can obey without the body.

---

## 4. Later: narrow `build-continuous` + add `build-inline`

**build-continuous edit (second):**

- Drop Story-unit mode section and story-unit red flags  
- Drop Setup step 4 dependency on unit derivation (or keep optional size-only table without barriers)  
- Description: continuous-only keywords  
- Redirect: if header is story-unit → tell controller to use `build-story-units`; if user wants no subagents → `build-inline`  
- Keep Inline Fallback **deleted** once `build-inline` ships (not before — leave fallback until replacement is GREEN)

**build-inline (third):**

- Elevate current Inline Fallback to first-class skill  
- Sequential tasks, `test-first` every step, ledger, stop on blocker  
- No unit barriers (user decision)  
- End: `inspect-change` → polish-diff/acceptance/prepare/finish as appropriate (subset of After the Last Task)

---

## 5. Downstream edits — DONE (2026-07-30)

- [x] `plan-tasks` Exit: three routes matching mode + inline choice  
- [x] `templates/tasks.md` agent blurb  
- [x] `AGENTS.md` skill table + main flow + execute family table  
- [x] `docs/architecture/*`, `docs/guide/*`, README, roadmap ROAD-2/3 surfaces  
- [x] `build-continuous` continuous-only; story/inline redirects  

---

## 6. Authoring order (no batch)

1. **RED** scenarios for `build-story-units` gates (this folder)  
2. Baseline RED on current dual-mode `build-continuous` (old version = control)  
3. GREEN: write minimal `build-story-units` skill + move recipe  
4. REFACTOR loopholes  
5. Then RED/GREEN for `build-continuous` narrow  
6. Then RED/GREEN for `build-inline`  
7. Wire plan-tasks / docs once all three hold  

---

## 7. Explicit non-goals

- No fourth skill for "hybrid continuous with optional human checkpoints"  
- No project-level default Execution-mode  
- No authored "Human review order" field in tasks.md (still derived)  
- No `disable-model-invocation` on these three — they remain model-invoked  
