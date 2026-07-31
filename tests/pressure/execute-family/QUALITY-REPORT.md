# Execute-family quality report

**Date:** 2026-07-30  
**Protocol:** `author-skills` deployment checklist + `pressure-testing.md`  
**Roster:** grok-4.5 (session model only)  
**Scope:** `build-in-waves`, `build-by-story`, `build-inline`, `plan-tasks` Exit wire

---

## 1. Structural / Ship checklist

| Check | Result | Notes |
|---|---|---|
| Frontmatter `name` + `description` | **PASS** | All four skills YAML-valid |
| Verb-first names | **PASS** | execute-*, plan-tasks |
| Model-invocable (no DMI) | **PASS** | Correct for routing skills |
| Description = trigger + outcome, not workflow steps | **PASS** | Heuristic: no step/then/dispatch in desc |
| Body ≤ ~500 lines | **PASS** | 181–222 lines |
| Refs one level deep | **PASS** | story-unit-mode; implementer prompts via sibling path |
| Ref >100 lines has TOC | **PASS** | TOC added to `story-unit-mode.md` (120 lines) this pass |
| Cross-refs REQUIRED SUB-SKILL only | **PASS** | No `@skill` links; no user-invoked as SUB-SKILL |
| User-invoked write-handoff named `/select-review-sample` | **PASS** | build-in-waves optional only |
| Gate form (Iron Law / Red Flags / rationalization) | **PASS** | story + inline full; plan has Mode gate + RF + table |
| RED evidence recorded | **PASS** | RED-BASELINE.md, TESTS.md per skill |
| GREEN prior + this pass | **PASS** | See §2 |
| Description trigger-tested | **PASS** | 12-query routing §2.1 |
| Multi-model roster | **LIMIT** | Only grok-4.5; not multi-model |
| 5-rep wording micro-tests | **LIMIT** | Gates retested 1-rep this pass; prior GREEN sessions 1–3 rep |
| Meta-test every sample | **PARTIAL** | META present on gate samples; not every query |

**Fix applied this pass:** TOC on `skills/execution/build-by-story/story-unit-mode.md`.

---

## 2. Pressure panel (this session)

### 2.1 Description routing (12 queries) — all expected

| # | Query intent | Expected | Observed |
|---|---|---|---|
| 1 | continuous + subagents | build-in-waves | build-in-waves |
| 2 | story-unit + human review | build-by-story | build-by-story |
| 3 | no subagents | build-inline | build-inline |
| 4 | watch inline | build-inline | build-inline |
| 5 | continuous parallel waves | build-in-waves | build-in-waves |
| 6 | story-unit resume | build-by-story | build-by-story |
| 7 | write tasks.md | plan-tasks | plan-tasks |
| 8 | plan wrong mid-flight | reroute-plan | reroute-plan |
| 9 | suite red mid-plan | root-cause | root-cause |
| 10 | worktree only | isolate-workspace | isolate-workspace |
| 11 | whole-branch review | inspect-change | inspect-change |
| 12 | opened plan + story header | build-by-story | build-by-story |

**Score: 12/12**

### 2.2 Gate scenarios — all A (compliant)

| ID | Scenario | Expected | Observed |
|---|---|---|---|
| S-NARROW-2 | plan opened, story-unit header | A write-handoff story | **A** |
| S-STORY-1 | unit barrier under EOD | A STOP | **A** |
| S-STORY-2 | stop stopping | A write continuous + plan | **A** |
| S-STORY-3 | looks good continue | A next unit only | **A** |
| S-NARROW-1 | continuous no pause | A continue | **A** |
| S-INLINE-1 | tools + inline | A self test-first | **A** |
| S-INLINE-2 | inline + story header | A no unit barrier | **A** |
| S-INLINE-3 | plan + do it yourself | A write-handoff inline | **A** |
| plan-tasks Exit | story vs continuous routes | mode match + inline | **Correct** |

**Score: 9/9 gates**

### 2.3 Technique — unit summary contract

| Slot | Present? |
|---|---|
| Unit id | Y |
| Stories + merge note | Y |
| Tasks | Y |
| Range | Y |
| Diff package | Y |
| Spec/Quality verdicts | Y |
| Open minors | Y |
| I am stopped | Y |
| continue vs mode-change write-back | Y |

**Score: full contract**

---

## 3. Residual risks (honest)

1. **Roster:** no Haiku/Sonnet/etc. Weakest-model compliance unproven.  
2. **Quiz bias:** options restating rules inflate A rates; production long-horizon runs not re-simulated.  
3. **Duplication debt:** After-last-task chain copied in three skills (by design for standalone load); drift risk if one chain changes.  
4. **`build-by-story` per-task loop** duplicates `build-in-waves` prose (avoids loading continuous skill mid-story); same drift risk.  
5. **Micro-test depth:** not 5-rep wording A/B for every new sentence.

None of these block ship for grok-4.5-targeted use; they are follow-ups if multi-model or long-run flakiness appears.

---

## 4. Verdict

| Claim | Status |
|---|---|
| author-skills structural/ship checks (this roster) | **PASS** (with TOC fix) |
| Pressure routing + gates this session | **PASS 21/21** decision points |
| Ready to use on grok-4.5 | **YES** |
| Ready to claim multi-model bulletproof | **NO** — expand roster if shipping beyond grok-4.5 |

**Overall: quality good for ship on current roster.** Optional next: multi-model pressure batch; extract shared after-last-task recipe if drift appears.
