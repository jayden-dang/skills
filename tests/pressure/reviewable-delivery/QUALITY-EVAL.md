# Quality eval — writing-skills pass on touched skills

**Date:** 2026-07-28  
**Standard:** `skills/meta/writing-skills/SKILL.md` + `influence-principles.md`  
**Skills:** finish-branch, write-plan, write-requirements, execute-plan (+ story-unit-mode.md)

## Checklist (post-improve)

| Criterion | finish-branch | write-plan | write-requirements | execute-plan |
|---|---|---|---|---|
| Trigger + outcome description (no workflow dump) | ok | improved (Execution-mode, vertical-slice) | ok | improved (continuous/story-unit) |
| Gate form: authority + rationalization + red flags | ok (risk naming) | ok (Execution-mode) | ok (story quality + section-kind) | ok (barriers) |
| Recipe / contract (not soft prefer) | **recipe 6b** with predicates | vertical-slice **contract** | story-quality **recipe** | iron laws + **story-unit-mode.md** |
| Deterministic primitives where judgment would fail | risk_hit / multi_task steps | footer one-story default | section-kind iron law | partition + file-count regex recipe |
| Completion criteria (Done when) | 6b Done when | Exit Done when | story gate Done when | setup preflight Done when |
| Leading words repeated | risk glob | Execution-mode, review unit | demoable act, Section-kind | review unit, Execution-mode, straddle |
| Token budget / hierarchy | body kept | body kept | body kept | algorithm **out of body** → reference |
| No-op / soft prefer removed | — | Prefer → contract | — | — |
| Contract tests | risk_signal + recipe keys | Execution-mode + no dead fields | section-kind + demoable | story-unit-mode file + barrier |
| Pressure GREEN holds | yes (prior run) | yes | n/a gate shape | yes |

## Eval commands

```bash
python3 -m unittest tests.test_finish_branch_risk_signal tests.test_plan_review_unit_contracts -v
python3 -m unittest discover -s tests
# Pressure scenarios (agent): tests/pressure/reviewable-delivery/scenarios.md
# Findings: tests/pressure/reviewable-delivery/PRESSURE-FINDINGS.md
```

## Eval completed 2026-07-28 (both)

1. **Micro-test 5-rep** finish-branch single-task+auth: **5/5 A** — see `MICRO-AND-TRIGGERS.md`.
2. **Description triggers** write-plan + execute-plan: **16/16 should-fire, 16/16 should-not-fire** — same file.
3. Still open: true RED without AGENTS injection; multi-model roster.
