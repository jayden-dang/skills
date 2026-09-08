# `build-by-story` — test evidence

## Edit — length pass to 195 lines (v2.0.2, 2026-09-07)

**Why:** SKILL.md was 208 lines / 1573 words, 8 over the 200-line lint limit.
Target was ≤195 (five under, per the length-pass brief). No sibling `.md` was
added — every cut was same-file or cross-file (`execute-common`) duplication,
or a same-file forward-reference collapsed into its one detailed statement.
Atom count: 86 → 85 (one true duplicate atom removed; see below).

**Deleted as duplicate, with surviving home confirmed by grep:**

- Intro clause "If the header already says `continuous`, hand off to
  `build-in-waves`." — duplicate of the **Mode ownership** table two sections
  down (`| continuous | REQUIRED SUB-SKILL: use build-in-waves |`, SKILL.md).
- "**Context rule:**" paragraph (workers/reviewers resume only within a valid
  lane lease; hard rotation triggers start fresh from the feature capsule and
  task delta; bulk artifacts travel as paths). Surviving home:
  `../execute-common/task-lifecycle.md` Dispatch contract ("Resume the worker
  only while the lease preflight remains clean. Start a fresh worker context
  after a semantic-unit boundary or any hard rotation trigger.") and Lease
  handoff ("start fresh from the feature capsule plus the next task delta"),
  both loaded by this file's own Section A of the Per-unit loop and by "use
  the continuous scheduler rules from `build-in-waves` inside each unit."
- Setup step 3's second sentence ("Resume also honors complete unit lines —
  skip units already ledgered complete.") — duplicate of
  `../execute-common/ledger-check.md`: "Every task (and, on story-unit, every
  unit) it marks complete IS complete — resume at the first item it does not
  list." (that file is loaded by this same step).
- Setup step 8's parenthetical "(edge if any task in U depends on any task in
  V); tie-break lowest story number" — duplicate of `story-unit-mode.md`
  **Derive partition** step 8: "Unit order — edge U→V if any task in U has
  `Depends-on` naming a task in V. Topo-sort; tie-break **lowest story
  number**." (loaded by this file's own Setup step 5, run before step 8 is
  ever reached). This is the atom the `--diff` tool flagged as "no home" at
  40% word overlap — confirmed by grep, home is `story-unit-mode.md:41-42`.
- Per-unit loop Section A's forward-reference ("If U contains one task, its
  Standards/Spec verdicts also close the unit; a multi-task U receives the
  synthesis described below.") and Section B's full restatement of the same
  rule — collapsed to one pointer in each section. Surviving home:
  `../execute-common/task-lifecycle.md` Task barrier: "For a unit containing
  exactly one task, this task's clean Standards and Spec verdicts also close
  the unit. Do not dispatch a duplicate unit reviewer over the same diff,
  brief, and evidence." (loaded by Section A itself, before Section B is ever
  reached in the same iteration).
- Durable progress bullet "Start: read `.skills/<CODE>/progress.md`; trust it
  and `git log` over memory." — this is the second atom the `--diff` tool
  flagged as "no home" (25% overlap, no strong match). Deliberate no-op:
  Setup step 3 already applies `../execute-common/ledger-check.md` at session
  start, which reads the same file and asserts "Every task... it marks
  complete IS complete" (i.e., trust it); the remaining three Durable-progress
  bullets (never re-dispatch complete work, what unit-complete means on
  compaction resume, `.skills/` is git-ignored/reconstructible) carry the
  bullet's operational content forward.

**Tightened wording only (no fact removed), Universal bucket:**

- Shared controller recipe paragraph: replaced the listed trigger points
  ("when Setup preflight / ledger / todos or After the last unit starts")
  with a pointer to "each Setup step below" — those steps already name their
  own execute-common application explicitly.
- Setup step 4 ("Read the plan"): merged two sentences, no fact dropped
  (Global Constraints path/hash, dispatch reference instead of pasting,
  verify commands from it, `docs/agents/project.md` fallback, Team
  band/Solo rule all still present).

**Not touched, and why:** the Iron Law / "Iron laws (story-unit)" section and
its Thought|Reality table (Gate bucket — the "stop stopping" mode-change rule
and the unlock-table overlap in Section B is the pressure-point restatement,
not filler); the Implementer-status-handling table, Model tiering, and
Reviewer-prompt-hygiene sections (Universal, and duplicated verbatim in
`build-in-waves` too, but `execute-common` does not yet own them — moving
them there is out of this skill's directory and out of scope); the Red Flags
list (Gate bucket, verbatim).

**Verification:**

- `python3 scripts/skill-rule-inventory.py skills/execution/build-by-story/SKILL.md`
  → 85 atoms (was 86).
- `python3 scripts/skill-rule-inventory.py --diff` against `SKILL.md` +
  `story-unit-mode.md` → 3 reworded (100% word survival, re-checked, no
  shift), 2 no-home — both accounted for above with grep-confirmed homes.
- `python3 scripts/lint-skill-length.py skills/execution/build-by-story/SKILL.md`
  → OK, 195 lines / 1464 words (was 208 / 1573). Removed this file's entry
  from `scripts/skill-length-budget.json` (targeted single-entry edit, not
  `--write`, to avoid touching other skills' in-flight budget entries).
- `lint-skill-evals.py`, `lint-skill-frontmatter.py`, `lint-skill-templates.py`,
  `lint-write-handoffs.py`, `lint-context7.py` — all clean for this file.
- `lint-skill-length.py` run with no args still fails, but only on
  `skills/execution/execute-common/SKILL.md` (198 lines, stale budget entry)
  — a different skill's uncommitted, in-progress edit, out of this trim's
  directory scope.
- All three eval.json anchors confirmed present verbatim: `SKILL.md § Shared
  controller recipe`, `SKILL.md § Per-unit loop`, `SKILL.md § Setup`.

Version bumped 2.0.1 → 2.0.2 (patch: wording/location changed, no behavior
change).

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
