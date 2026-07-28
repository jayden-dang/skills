# Micro-test + description trigger results

**Date:** 2026-07-28  
**Model:** grok-4.5  
**Protocol:** `writing-skills` pressure-testing.md (micro-tests 5+ reps; description should-fire / should-not-fire)

## 1. finish-branch micro-test (single-task + auth)

**Scenario:** 1 task, diff `skills/auth/session.ts`, menu Keep, social/time pressure.  
**Compliant:** A = name both `/comprehend-change` and `/explain-change`.

| Rep | CHOICE | Pass |
|-----|--------|------|
| 1 | A | yes |
| 2 | A | yes |
| 3 | A | yes |
| 4 | A | yes |
| 5 | A | yes |

**Score: 5/5.** Variance: zero. Agents cited worked case + `risk_hit` + red flags. **No wording change required.**

## 2. write-plan description triggers

**Description under test:**  
`Use when a design is approved and the tasks.md implementation plan (Execution-mode, vertical-slice tasks, requirement-tagged tests) needs writing, after write-design and before execute-plan.`

### Should-fire (expect write-plan) — 8/8

| Q | Result |
|---|--------|
| design approved, write tasks.md plan | write-plan |
| Execution-mode continuous vs story-unit on plan | write-plan |
| vertical-slice tasks with requirement tags | write-plan |
| tasks.md draft after write-design | write-plan |
| plan work items before execute-plan | write-plan |
| fill tasks.md template | write-plan |
| implementation plan for subagents | write-plan |
| write the plan file before coding next session | write-plan |

### Should-not-fire (expect neighbor, not write-plan) — 8/8

| Q | Expected | Result |
|---|----------|--------|
| write design.md | write-design | write-design |
| tasks Approved, implement | execute-plan | execute-plan |
| resume after crash | execute-plan | execute-plan |
| failing test first | tdd | tdd |
| brainstorm new feature | brainstorm | brainstorm |
| merge/PR menu | finish-branch | finish-branch |
| story-unit barrier mid-execute | execute-plan | execute-plan |
| write requirements EARS | write-requirements | write-requirements |

**No over/under-trigger.** Description OK as-is.

## 3. execute-plan description triggers

**Description under test:**  
`Use when an approved tasks.md needs executing — continuous or story-unit Execution-mode, task waves, dual-verdict review, resume after crash/compaction — through whole-branch review and finish-branch.`

### Should-fire — 8/8 (all execute-plan)

Including: Approved tasks.md run; resume/ledger; story-unit barriers; continuous mode; crash mid-wave; dispatch implementers; plan ready to build; implement on worktree.

### Should-not-fire — 8/8 (none execute-plan)

| Q | Result |
|---|--------|
| write tasks.md + Execution-mode | write-plan |
| merge/PR | finish-branch |
| design.md | write-design |
| debug root cause | debug |
| failing test implement | tdd |
| plan only no code | write-plan |
| requirements.md | write-requirements |
| PR two-axis review | code-review |

**No over/under-trigger.** Description OK as-is.

## Verdict

| Eval | Result | Action |
|------|--------|--------|
| Micro 5-rep finish-branch | **5/5 A** | None — wording holds |
| write-plan triggers | **16/16** | None |
| execute-plan triggers | **16/16** | None |

Harden pass not required from this eval.
