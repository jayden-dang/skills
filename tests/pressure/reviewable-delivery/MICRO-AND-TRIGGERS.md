# Micro-test + description trigger results

**Date:** 2026-07-28  
**Model:** grok-4.5  
**Protocol:** `author-skills` pressure-testing.md (micro-tests 5+ reps; description should-fire / should-not-fire)

## 1. land-branch micro-test (single-task + auth)

**Scenario:** 1 task, diff `skills/auth/session.ts`, menu Keep, social/time pressure.  
**Compliant:** A = name both `/study-change` and `/brief-team`.

| Rep | CHOICE | Pass |
|-----|--------|------|
| 1 | A | yes |
| 2 | A | yes |
| 3 | A | yes |
| 4 | A | yes |
| 5 | A | yes |

**Score: 5/5.** Variance: zero. Agents cited worked case + `risk_hit` + red flags. **No wording change required.**

## 2. plan-tasks description triggers

**Description under test:**  
`Use when a design is approved and the tasks.md implementation plan (Execution-mode, vertical-slice tasks, requirement-tagged tests) needs writing, after design-solution and before build-continuous.`

### Should-fire (expect plan-tasks) — 8/8

| Q | Result |
|---|--------|
| design approved, write tasks.md plan | plan-tasks |
| Execution-mode continuous vs story-unit on plan | plan-tasks |
| vertical-slice tasks with requirement tags | plan-tasks |
| tasks.md draft after design-solution | plan-tasks |
| plan work items before build-continuous | plan-tasks |
| fill tasks.md template | plan-tasks |
| implementation plan for subagents | plan-tasks |
| write the plan file before coding next session | plan-tasks |

### Should-not-fire (expect neighbor, not plan-tasks) — 8/8

| Q | Expected | Result |
|---|----------|--------|
| write design.md | design-solution | design-solution |
| tasks Approved, implement | build-continuous | build-continuous |
| resume after crash | build-continuous | build-continuous |
| failing test first | test-first | test-first |
| frame-change new feature | frame-change | frame-change |
| merge/PR menu | land-branch | land-branch |
| story-unit barrier mid-execute | build-continuous | build-continuous |
| write requirements EARS | specify-behavior | specify-behavior |

**No over/under-trigger.** Description OK as-is.

## 3. build-continuous description triggers

**Description under test:**  
`Use when an approved tasks.md needs executing — continuous or story-unit Execution-mode, task waves, dual-verdict review, resume after crash/compaction — through whole-branch review and land-branch.`

### Should-fire — 8/8 (all build-continuous)

Including: Approved tasks.md run; resume/ledger; story-unit barriers; continuous mode; crash mid-wave; dispatch implementers; plan ready to build; implement on worktree.

### Should-not-fire — 8/8 (none build-continuous)

| Q | Result |
|---|--------|
| write tasks.md + Execution-mode | plan-tasks |
| merge/PR | land-branch |
| design.md | design-solution |
| root-cause root cause | root-cause |
| failing test implement | test-first |
| plan only no code | plan-tasks |
| requirements.md | specify-behavior |
| PR two-axis review | inspect-change |

**No over/under-trigger.** Description OK as-is.

## Verdict

| Eval | Result | Action |
|------|--------|--------|
| Micro 5-rep land-branch | **5/5 A** | None — wording holds |
| plan-tasks triggers | **16/16** | None |
| build-continuous triggers | **16/16** | None |

Harden pass not required from this eval.
