# `build-by-story` — test evidence

## Edit — occupancy red-flag pointer (v2.0.1)

Red flag now names skipping occupancy. Kickoff write lives in
`execute-common` Session preflight. RED/GREEN:
`skills/execution/execute-common/TESTS.md` § catalog occupancy.

---


## GREEN — shared task lifecycle inside review units (structural, 2026-08-26)

Fresh frontmatter/eval lint returned exit 0. The skill delegates task execution
to the shared lifecycle, reuses a clean single-task verdict, and keeps
multi-task synthesis plus the human unit barrier. Live multi-model execution
was unavailable; this records structural GREEN only.

## RED — shared continuous task lifecycle (current v1.2.0)

**Protocol:** `author-skills` / `pressure-testing.md`
**Pressure stack:** human waiting at the unit gate + serial tasks share one
semantic lane + a later independent task is safe to parallelize + token budget
pressure.

**Current-version failure.** The per-unit section repeats the implementer,
reviewer, diff, and fix-loop recipe locally and explicitly says parallel waves
inside a unit are out of scope. A worker/reviewer lease cannot be reused through
related tasks without inventing a second contract, and the same task lifecycle
can drift from `build-in-waves`.

**RED verdict:** fail. Story-unit mode needs to load the shared task lifecycle
and scheduler, then add only its derived-unit and human-unlock barrier.

**Protocol:** `author-skills` / `pressure-testing.md`  
**Scenario files:** removed in `2338b34` ("remove test scenarios") — the runnable prompts now live in `eval.json` beside this file.  

## RED summary (2026-07-30, grok-4.5)

| Failure | Class | Owns this text |
|---|---|---|
| All plan-execution intents route only to `build-in-waves` | Distinct trigger (split case 1) | description + opening "not continuous / not inline" |
| Unit STOP message variance (mode-change write-back sometimes omitted) | Wrong/unstable shape → REQUIRED slots | `story-unit-mode.md` Unit summary contract |
| Quiz gates S-STORY-1..6 already A with dual-mode skill | No new iron laws | Extracted existing laws/rationalizations verbatim |

## GREEN — authoring targets

1. Skill exists and is discoverable for story-unit intent.
2. Unit summary contract binds all REQUIRED slots (technique re-test).
3. Iron laws / mode-change / derive-not-authored preserved from dual-mode text.

## GREEN retest log (2026-07-30, grok-4.5)

### Technique — bare unit summary (with skill)

| Rep | Model | Mode-change write-back? | All core slots? | Notes |
|---|---|---|---|---|
| 1 | grok-4.5 | yes | yes | Full contract; minors + unlock semantics |
| 2 | grok-4.5 | yes | yes* | *Stories set `{N}` omitted when prompt gave title only — title present |

**Vs RED bare:** mode-change write-back was Partial/missing under dual-mode freeform; both GREEN reps include `write Execution-mode: continuous into tasks.md` + write-handoff to build-in-waves.

### Quiz S-STORY-1, S-STORY-2 (with skill)

| Scenario | Model | CHOICE | Cite skill? |
|---|---|---|---|
| S-STORY-1 | grok-4.5 | A | yes — iron law + EOD rationalization |
| S-STORY-2 | grok-4.5 | A | yes — mode change + build-in-waves write-handoff |

### Description routing

| Query | Expected | Result |
|---|---|---|
| continuous + subagents | build-in-waves | build-in-waves |
| story-unit + review after each story | build-by-story | build-by-story |
| no subagents | build-inline (future) | build-inline named (not shipped) |
| suite failing mid-run | root-cause | root-cause |
| continuous just run it | build-in-waves | build-in-waves |
| story-unit unit barriers | build-by-story | build-by-story |

## Edit — polish-diff always + setup todo (2026-08-07)

**RED (structural + production).** Same failure as execute-family siblings:
`polish-diff` already REQUIRED in After the last unit, but Setup Todos listed
only plan tasks — post-plan polish dropped when task todos went green.

**GREEN form.** Todos GATE: one todo per task **and** terminal **Polish Diff**.
After-last step 3 mandatory + mark todo; red flags; rationalization rows.

## Edit — polish predicate + execute-common (2026-08-16)

Supersedes the always-polish GREEN. Shared controller recipe lives in
`../execute-common/SKILL.md`. Terminal todo is **Close branch**. Polish / product-walk
are observable conditionals; EOD is not a predicate.

## Ship gate

- [x] Technique bare summary binds mode-change write-back (B2 fix)
- [x] Quiz gates remain A with skill citation
- [x] Description routes story-unit vs continuous (B1 fix)
- [x] Mode ownership: invoke story skill → write `story-unit` if header missing
- [x] Setup preflight is tracker sync + workspace
- [x] No-op + duplication: per-task loop inlined intentionally until build-in-waves narrow extracts shared home; templates pointer to `../build-in-waves/*-prompt.md`
- [x] build-in-waves continuous-only; build-inline shipped
- [x] plan-tasks / AGENTS / templates family wire
