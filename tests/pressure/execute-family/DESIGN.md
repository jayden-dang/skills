# Execute family split — design (writing-skills)

**Date:** 2026-07-30  
**Protocol:** `writing-skills` + `pressure-testing.md`  
**Status:** Design locked · all three execute skills GREEN · write-plan/AGENTS/docs wire complete (2026-07-30)  
**Decisions (user 2026-07-30):** three independent skills; inline = sequential only; author `execute-story` first

---

## 1. Why the current design fails

`execute-plan` is one skill with **two competing process cores**:

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

**writing-skills "When to split" — case 1 applies (genuinely distinct trigger):**

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

write-plan Exit routes (how to run):
  1. execute-plan     if Execution-mode: continuous  (subagent waves)
  2. execute-story    if Execution-mode: story-unit  (subagent + unit barriers)
  3. execute-inline   user/capability choice         (controller implements;
                                                     sequential; ignores mode for barriers)
```

| Skill | Trigger (description outcome) | Owns | Does not own |
|---|---|---|---|
| **execute-plan** | Approved plan, continuous mode, subagent orchestration through finish chain | Per-task loop, parallel waves, continuous-only red flags | Unit barriers, story derivation |
| **execute-story** | Approved plan, story-unit mode, human-gated review units | Unit partition recipe, per-unit barrier, mode-change write-back | Continuous "never pause", parallel waves (v1: serial units; waves *inside* a unit optional later) |
| **execute-inline** | User chose inline / no subagent capability | Controller implements via `tdd`, same ledger shape, end `code-review` | Subagent dispatch, unit barriers |

### Shared assets (one home each — no meaning duplication)

| Asset | Home | Consumers |
|---|---|---|
| Implementer dispatch template | `execution/execute-plan/implementer-prompt.md` | execute-plan, execute-story (pointer) |
| Task reviewer template | `execution/execute-plan/task-reviewer-prompt.md` | execute-plan, execute-story (pointer) |
| Unit derivation + barrier recipe | moves to `execution/execute-story/story-unit-mode.md` | execute-story only; execute-plan drops preflight that requires it |
| Progress ledger contract | Document once in execute-plan Setup step 2; others pointer "same ledger line shape" | all three |
| After-last-task chain | execute-plan body; execute-story/inline `REQUIRED SUB-SKILL` or short pointer to same sequence | all three |

Do **not** create `execution/shared/` until a fourth consumer appears — one extra folder for two pointers fails the token budget test.

---

## 3. `execute-story` product shape (first to author)

**Leading words:** review unit · unit barrier · human unlock · mode change · ledger

**Iron laws (gates — authority form):**

1. Review units are **derived**, never authored in tasks.md  
2. After unit tasks clean: **unit agent review → STOP for human → unlock**  
3. "continue" after looking = next unit; "stop stopping" / "just run it all" = write `Execution-mode: continuous` then hand off to `execute-plan` (or continue continuous rules) — chat-only is not a mode change  
4. Ledger `Unit <k>: complete (...)` — resume reads it  
5. Whole-branch agent review still runs after last unit  

**Loop (recipe form):**

Setup (workspace, ledger, plan, todos, preflight partition, wave-of-units) →  
for each unit in order: for each task in unit: (shared per-task loop) → unit barrier →  
after last unit: whole-branch chain (same as execute-plan)

**Narrow vs current:**  
- No continuous path in this skill  
- No "Inline Fallback" section  
- Parallel waves: **out of scope for v1** unless unit has file-disjoint tasks — if needed, pointer to execute-plan Parallel waves recipe; default serial per unit to keep barrier simple  

**Description (draft — trigger-test before ship):**

```yaml
description: Use when an approved tasks.md has Execution-mode story-unit and
  needs human-gated review-unit execution — derived units, unit barriers,
  mode-change write-back, resume via unit ledger lines — through whole-branch
  review.
```

Must not summarize the full workflow as steps the agent can obey without the body.

---

## 4. Later: narrow `execute-plan` + add `execute-inline`

**execute-plan edit (second):**

- Drop Story-unit mode section and story-unit red flags  
- Drop Setup step 4 dependency on unit derivation (or keep optional size-only table without barriers)  
- Description: continuous-only keywords  
- Redirect: if header is story-unit → tell controller to use `execute-story`; if user wants no subagents → `execute-inline`  
- Keep Inline Fallback **deleted** once `execute-inline` ships (not before — leave fallback until replacement is GREEN)

**execute-inline (third):**

- Elevate current Inline Fallback to first-class skill  
- Sequential tasks, `tdd` every step, ledger, stop on blocker  
- No unit barriers (user decision)  
- End: `code-review` → polish/acceptance/prepare/finish as appropriate (subset of After the Last Task)

---

## 5. Downstream edits — DONE (2026-07-30)

- [x] `write-plan` Exit: three routes matching mode + inline choice  
- [x] `templates/tasks.md` agent blurb  
- [x] `AGENTS.md` skill table + main flow + execute family table  
- [x] `docs/architecture/*`, `docs/guide/*`, README, roadmap ROAD-2/3 surfaces  
- [x] `execute-plan` continuous-only; story/inline redirects  

---

## 6. Authoring order (no batch)

1. **RED** scenarios for `execute-story` gates (this folder)  
2. Baseline RED on current dual-mode `execute-plan` (old version = control)  
3. GREEN: write minimal `execute-story` skill + move recipe  
4. REFACTOR loopholes  
5. Then RED/GREEN for `execute-plan` narrow  
6. Then RED/GREEN for `execute-inline`  
7. Wire write-plan / docs once all three hold  

---

## 7. Explicit non-goals

- No fourth skill for "hybrid continuous with optional human checkpoints"  
- No project-level default Execution-mode  
- No authored "Human review order" field in tasks.md (still derived)  
- No `disable-model-invocation` on these three — they remain model-invoked  
