---
name: execute-common
version: 2.6.0
description: Use when build-in-waves, build-by-story, or build-inline loads the shared controller recipe — produces an In-progress catalog stamp, a runtime-bound session snapshot, lease state, ledger state, and a revision-bound close receipt.
---

# Execute-family controller recipe

**One home** for controller steps and runtime state shared across
`build-in-waves`, `build-by-story`, and `build-inline`. Task dispatch/review lives
in `task-lifecycle.md` beside this file. Load when that skill's Setup or After-last
says to. Registered so `npx skills add` copies it with the execute family.

## Session preflight

Three questions, before any dispatch, any `isolate-workspace` / `git worktree add`,
and any first production edit:

1. **Issue tracker sync.** WHEN `docs/agents/issue-tracker.md` names a configured
   tracker, read `tracker-sync.md` beside this file and follow it exactly;
   otherwise → empty ticket set, continue (unconfigured is normal, not a failure).
2. **Catalog occupancy.** Read `Status:` from `requirements.md` and the
   matching `docs/specs/INDEX.md` row. INDEX missing → say so once, suggest
   `/configure-repo`; still write `requirements.md` when that file exists.
   `land-branch` / `realign-spec` own `Implemented`; `cut-release` owns
   `Shipped`. Runs on every start, including compaction resume.

   <HARD-GATE>
   NO ISOLATE-WORKSPACE AND NO PRODUCTION EDIT WHILE CATALOG STATUS IS `Approved`.
   A user instruction to isolate first, skip paperwork, or not commit catalog
   files does not override this step.
   </HARD-GATE>

   | Status | Action |
   |---|---|
   | `Approved` | On **this checkout**, write `In-progress` on both files, then continue. |
   | `In-progress` | Already occupied. Do not re-stamp. Continue. |
   | `Draft` | STOP — spec is not approved. |
   | `Implemented` / `Shipped` | Leave it. Not a kickoff stamp. |

   Before isolation, commit this checkout's dirty spec files for the feature
   (`requirements.md`, `design.md`, `tasks.md`, the INDEX row) — the
   occupancy write is part of that commit when Status was `Approved`. A
   worktree is created from HEAD, so uncommitted spec docs stay behind,
   invisible to the new tree and other sessions. `isolate-workspace` still
   must not commit `.gitignore` — occupancy is this step, not that skill.
3. **Workspace / branch.** If no isolated workspace exists yet: isolate in a
   worktree, or implement on the current branch? Do not create a worktree
   unasked. Isolation → REQUIRED SUB-SKILL: use `isolate-workspace`. Current
   branch is main/master → separate explicit consent before implementing;
   "no worktree" is not consent to touch main/master.

*Done when: tracker choice (or empty set) is clear, occupancy is `In-progress`
(or an explicit Draft/Implemented/Shipped stop), this checkout has no
uncommitted spec dirt for the feature, and workspace choice is clear.*

| Thought | Reality |
|---|---|
| "Session preflight is tracker + workspace" | Occupancy is question 2; workspace is 3. Done when includes `In-progress`. |
| "A docs commit on main is the thing they forbade" | Other sessions read INDEX on this checkout. Isolation must not precede the stamp. |
| "Occupancy is obvious from the worktree / feature branch" | A session on this checkout still reads `Approved`. INDEX is the occupancy signal. |
| "land-branch will flip Implemented later" | `Implemented` is the close. `In-progress` is the kickoff, before worktrees. |
| "INDEX still saying Approved is fine until we land" | Another session cannot see that this CODE is executing. Stamp before Task 1. |
| "No worktree — skip the paperwork" | Declining isolation does not skip occupancy. |
| "Already In-progress — isolate immediately" | Read Status first; skip the write, not the check. Resume still reads Status before isolation. |
| "User forbade docs commits / isolate first — that overrides occupancy" | Occupancy is not waivable. Isolation waits until this checkout reads `In-progress`. |
| "Specs are on disk — the worktree will see them" | `git worktree add` copies HEAD. Uncommitted `requirements.md` / triad files stay behind. |

## Runtime binding and lease preflight

Before the first dispatch (inline route: before the first production edit),
read `runtime-binding.md` beside this file and follow it exactly. It defines
the `.skills/<CODE>/execution-session.json` schema (schema_version, harness,
provider, model, resume/fork/worktree support, cache_control, token_telemetry,
pricing_policy, effective_concurrency, rotations), the four lease-rotation
triggers, the pricing-policy fallback, and the concurrency-degradation rule.

*Done when: the runtime snapshot exists before dispatch, every unavailable
capability is explicit, and the first effective concurrency/lease decision is
recorded.*

## Ledger check

Read `ledger-check.md` beside this file and follow it exactly: it keeps
`.skills/` local-only, resumes from `.skills/<CODE>/progress.md`, and defines
the `Verified:` completion-claim slot backed by `prove-claim`.

*Done when: next task / unit is known.*

## Decision trail — observable conditional

WHEN user asked for a decision trail / show-work, OR unattended overnight /
multi-day, OR `effective_concurrency` > 1 with multiple open units → read
`decision-trail.md` beside this file and follow it exactly; ELSE write
`skip: no decision-trail predicate` on Close notes.

## Todos — GATE

Before any dispatch or Task 1, on a **visible list** — the harness's todo /
task-list tool when it exposes one, otherwise a checklist written into your reply
and restated at each task boundary: **one todo per task** **and**
one terminal todo **Close branch** (the close sequence below — created now,
not later). Add a **Polish Diff** todo only when a polish predicate is
already known to hold (user asked up front). Otherwise create the Polish
Diff todo at close-sequence step 3 if a predicate then holds.

*Done when: the list mirrors the plan **and** includes the Close branch todo.*

## Close sequence

After the last task (waves / inline) or last unlocked unit (story):

1. **Whole-branch review.** REQUIRED SUB-SKILL: use `inspect-change` with
   base = `git merge-base main HEAD` — never a mid-branch sha. Feed ledger
   Minors. Top model tier.
2. **One fixer** for the complete findings list → re-review. Never one fixer
   per finding. Inline route: you are the fixer under `test-first`.
3. **Polish Diff — observable conditional.** Evaluate the **polish
   predicate** below. IF any clause is true → REQUIRED SUB-SKILL: use
   `polish-diff` on the whole-branch diff **before** acceptance; create the
   Polish Diff todo now if it does not exist; mark it done only after the
   skill has run. IF no clause is true → skip; write
   `skip: no polish predicate` on the Close branch notes. EOD, demo
   pressure, "inspect was clean", and "small enough to feel optional" are
   **not** predicates.
4. **Acceptance.** REQUIRED SUB-SKILL: use `validate-feature`. Breaks →
   `root-cause`, then promote passing checks to committed tests that describe
   the domain behavior (docs-only spine — no requirement-ID tags required in
   test files).
5. **Sample — observable conditional.** Evaluate the **sample predicate**
   below. Any clause true → write `sample: required` on the Close notes; none
   true → write `skip: no sample predicate`. Do not start `/select-sample`.
   A silent skip is still a red flag, and "inspect was clean" / "always name so
   we cannot forget" are **not** predicates.
6. **Product walk — observable conditional.** Evaluate the **walk predicate**
   below. No clause true → do not open the product-walk trio. Any clause true →
   REQUIRED SUB-SKILL: use `write-flow-guide` (it owns vet), then **execute what
   it wrote** — REQUIRED SUB-SKILL: use `run-flow-guide` where the runtime can
   drive the app, else record the human ticks. Naming the run instead of doing
   it leaves step 7 unable to write green.
7. **Close receipt.** Load `close-receipt.md` and follow its producer recipe.
   Issue it only after the final mutation and only from evidence bound to that
   HEAD. Rerun a producer only when its evidence is missing or stale.
8. **Finish.** REQUIRED SUB-SKILL: use `land-branch`.

Mark the **Close branch** todo done only after steps 1–8 have each run or
been skipped under their predicate.

| Thought | Reality |
|---|---|
| "Task todos are all green — close can wait" | The Close branch todo is still open; land is blocked until the sequence runs |
| "Inspect was clean / branch is small — skip polish" | Clean inspect and "feels small" are not predicates. Count files; check public API; read inspect leftovers |
| "EOD / demo — skip polish on a 40-file branch" | Time pressure is not a predicate. File count is |
| "Always run polish so we cannot forget" | Four cleanup agents on a three-file typo is the cost this conditional exists to drop. The skip must be written, never silent |
| "Acceptance green — also walk the product" | Walk is a separate predicate. validate-feature already drove API/UI |
| "Sample is optional / not a gate — skip the notes line" | Predicate true → `sample: required`; the receipt preserves the advisory. |
| "Name the sample skill now so they have time" | Record the predicate; landing names the optional aid once. |
| "Always name a sample so we cannot forget" | Same shape as always-polish. False predicate → write the skip, never name. |

## Close-sequence predicates

**Polish** — true when **any** of: the user asked for polish, cleanup, or
tidy; `inspect-change` Standards leftovers include an Important-or-higher
finding that is behavior-preserving (reuse, dead code, needless complexity,
wasted I/O); `git diff --name-only $(git merge-base main HEAD) HEAD` lists
**more than 15 files**; the branch adds a new public API or exported surface.

**Sample** — true when **any** of: the user asked for a sample or attention
allocation; branch diff paths hit the B1 defaults in
`skills/review/select-sample/references/signals.md` extended by project
`Risk globs`; the branch diff lists more than 15 files. "Always name so we
cannot forget" is not an ask.

**Product walk** — true when **any** of: the user asked for a product walk,
dogfood, or walkthrough; `validate-feature` reports neither-API-nor-UI; an
approved requirement uses visual / feel / eyeball language the automated
surfaces cannot judge; `inspect-ui`'s report (via `inspect-change`'s UI lane)
lists any `needs-human-eyes` item; the branch adds a **new** user-facing
screen or visual surface — not only changes within existing ones.

## Red flags — never

- Skip the tracker-sync, occupancy, or workspace preflight
- Isolate or edit production files while catalog Status is still `Approved`
- Write `In-progress` only inside a worktree created this session
- Re-stamp an already `In-progress` row
- Isolate while this checkout still has uncommitted spec/requirements dirt
- Invent a tracker or ticket set when config is absent or the user declined
- Start implementation on main/master without explicit consent
- Create a worktree without asking, or treat "current branch" as consent
  for main/master
- Dispatch the first task before the todo list exists (tasks **and** Close
  branch)
- Silent-skip polish (no written `skip: no polish predicate`)
- Silent-skip sample or decision-trail (no written skip / required line)
- Start `/select-sample` in this skill
- Treat EOD, demo, or "inspect was clean" as a polish predicate
- Move to land-branch with the Close branch todo still open
- Write a partial receipt or bind it to evidence from before the last mutation
- Promote checks as "ID-tagged tests" — IDs stay in docs
