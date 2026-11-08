# Shared task lifecycle

`build-in-waves` and `build-by-story` load this file after their mode-specific
setup. The scheduler or story-unit wrapper supplies the task, lane, lease IDs,
and paths; this file owns the implementation/review barrier.

## Dispatch contract

Build `.skills/<CODE>/task-N-brief.md` from the task block plus a reference to
the canonical Global Constraints section and its content hash. Include relevant
architecture seams, prior-task interfaces, ambiguity resolutions, and the
task's requirement footer. Do not paste the entire plan or duplicate global
constraints into each reviewer prompt.

Dispatch the worker with:

- the stable role contract;
- the feature capsule path and hash;
- the task delta path and hash;
- the current lane/worker lease ID;
- the report path and explicit model tier.

Resume or start the worker fresh per **Resume or start fresh** in
`runtime-binding.md`.

## Task barrier

1. Record `BASE=$(git rev-parse HEAD)` before the task starts. In an isolated
   lane, record the lane worktree and `WBASE` as well.
2. Dispatch or resume the worker. Answer questions before implementation.
3. Require test-first implementation, a commit on `DONE`, and the report
   contract in `implementer-prompt.md`. The report stores compact evidence:
   command, exit code, warning/error counts, revision, duration, and content
   hash; raw logs stay on disk and are opened only when evidence is missing,
   noisy, mismatched, or needed to investigate a finding.
4. Package `git log $BASE..HEAD`, `git diff --stat $BASE HEAD`, and
   `git diff -U10 $BASE HEAD` into
   `.skills/<CODE>/review-<base7>..<head7>.diff`. Never use `HEAD~1` as base.
5. Dispatch or resume the reviewer with the task brief path, report path, diff
   package path, evidence manifest, reviewer lease ID, and explicit model, against
   the contract in `task-reviewer-prompt.md` beside this file. Open it by that
   path: `find` does not follow the symlinks an install uses, and one controller
   took an empty `find` to mean the template "is not in the install" and wrote
   its own. The reviewer returns separate Standards and Spec verdicts. A task
   review is independent of the whole-branch review. The reviewer is a
   general-purpose subagent carrying that contract, never a named review agent
   from the roster or a plugin (`code-reviewer` and the like), whatever its
   description says: that agent's own instructions run on top of the contract,
   and `pr-review-toolkit:code-reviewer`'s drop every finding it rates under 80%
   confidence. Two builds sent all 22 of their task reviews to it; neither had
   opened the template.
6. Critical/Important findings go through one fix dispatch for the complete
   finding set, then a fresh re-review. Three surviving cycles stop the build
   and escalate. The controller never fixes reviewer findings directly.
   The fix message names its verification: the tests covering the amended code,
   plus `test-first`'s task gate for that amendment only when the fix changes
   production code. Both Haiku baseline controllers sent a test-only fix back
   with the full 14–17 minute gate of the task attached.
7. Resolve ⚠️ items the reviewer could not prove from the diff. Only after both
   verdicts are clean append:

   `Task N: complete (commits <base7>..<head7>, review clean)`

   Then **tick the plan**: mark every step of Task N `- [x]` in `tasks.md` — inside its
   `## ROAD-N amendment` group when the task belongs to one. The ledger is local; the tick
   is the record other people, `land-branch` and `chart-progress` read. WHEN
   `git check-ignore -q <path to tasks.md>` fails (the plan is tracked), commit that file
   alone as `docs(<CODE>): tick Task N` on the feature branch, so the tick reaches the
   integration branch with the code. WHEN it succeeds (specs are kept out of git), edit the
   file and commit nothing — never `git add -f` it. Two baseline controllers ledgered Task 1
   and left every box in `tasks.md` open.

For a unit containing exactly one task, this task's clean Standards and Spec
verdicts also close the unit. Do not dispatch a duplicate unit reviewer over
the same diff, brief, and evidence. A multi-task unit still needs unit
synthesis at its barrier.

## Lease handoff

At task completion, retain the worker and reviewer leases only if the scheduler
will continue on the same semantic lane and **Resume or start fresh** in
`runtime-binding.md` allows it. Otherwise record the rotation and start fresh
from the feature capsule plus the next task delta.
