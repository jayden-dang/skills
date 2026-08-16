# Execute-family controller recipe

**One home** for the controller steps that are identical across
`build-in-waves`, `build-by-story`, and `build-inline`. Each of those
SKILL.md files owns only its mode iron law and per-task / per-unit loop.
Load this file when that skill's Setup or After-last step says to.

## Contents

- Session preflight
- Ledger check
- Todos — GATE
- Close sequence (after the last task / last unit)
- Polish predicate
- Product-walk predicate

---

## Session preflight

Two questions, before any dispatch or first production edit:

1. **Issue tracker sync.** Read `docs/agents/issue-tracker.md` when present.
   IF a tracker is configured (github / gitlab / linear / local / other named
   backend) → ask whether this build should sync with that tracker (bind
   issues to the branch, pull ticket IDs into briefs/ledger, use the
   tracker's wayfinding ops for status). IF yes → resolve ticket IDs from
   branch name, plan, or a short user list; record them under `.skills/` for
   implementer briefs and later `package-change`. IF no, or the file is
   absent / declares no tracker → empty ticket set; continue (unconfigured
   tracker is normal, not a failure).
2. **Workspace / branch.** If no isolated workspace exists yet: isolate in a
   worktree, or implement on the current branch? Do not create a worktree
   unasked. Isolation → REQUIRED SUB-SKILL: use `isolate-workspace`. Current
   branch is main/master → separate explicit consent before implementing;
   "no worktree" is not consent to touch main/master.

*Done when: tracker choice (or empty set) and workspace choice are clear.*

## Ledger check

Make `.skills/` local-only:

```
grep -qxF '.skills/' .gitignore 2>/dev/null || { printf '.skills/\n' >> .gitignore && git commit -m 'chore: ignore local skills artifacts' -- .gitignore; }
```

Read `.skills/<CODE>/progress.md` if it exists. Every task (and, on
story-unit, every unit) it marks complete IS complete — resume at the first
item it does not list. *Done when: next task / unit is known.*

## Todos — GATE

Via TodoWrite before any dispatch or Task 1: **one todo per task** **and**
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
   `skip: no polish predicate` on the Close branch notes (file count, no
   new public API, no user ask, no inspect Important leftovers). EOD, demo
   pressure, "inspect was clean", and "small enough to feel optional" are
   **not** predicates.
4. **Acceptance.** REQUIRED SUB-SKILL: use `validate-feature`. Breaks →
   `root-cause`, then promote passing checks to committed tests that describe
   the domain behavior (docs-only spine — no requirement-ID tags required in
   test files). Optional: name `/select-review-sample` (not a gate).
5. **Product walk — observable conditional.** Evaluate the **walk
   predicate** below. IF any clause is true → REQUIRED SUB-SKILL: use
   `review-product-flow` (it owns vet + naming the walkthrough). IF no
   clause is true → do not open the product-walk trio.
6. **Prepare.** REQUIRED SUB-SKILL: use `package-change`.
7. **Finish.** REQUIRED SUB-SKILL: use `land-branch`.

Mark the **Close branch** todo done only after steps 1–7 have each run or
been skipped under their predicate.

| Thought | Reality |
|---|---|
| "Task todos are all green — close can wait" | The Close branch todo is still open; land is blocked until the sequence runs |
| "Inspect was clean / branch is small — skip polish" | Clean inspect and "feels small" are not predicates. Count files; check public API; read inspect leftovers |
| "EOD / demo — skip polish on a 40-file branch" | Time pressure is not a predicate. File count is |
| "Always run polish so we cannot forget" | Four cleanup agents on a three-file typo is the cost this conditional exists to drop. The skip must be written, never silent |
| "Acceptance green — also walk the product" | Walk is a separate predicate. validate-feature already drove API/UI |

## Polish predicate

True when **any** of:

- the user asked for polish, cleanup, or tidy
- `inspect-change` Standards leftovers include an Important-or-higher
  finding that is behavior-preserving (reuse, dead code, needless
  complexity, wasted I/O)
- `git diff --name-only $(git merge-base main HEAD) HEAD` lists **more
  than 15 files**
- the branch adds a new public API or exported surface (new HTTP route,
  new package export, new CLI command)

## Product-walk predicate

True when **any** of:

- the user asked for a product walk, dogfood, or walkthrough
- `validate-feature` reports neither-API-nor-UI
- an approved requirement uses visual / feel / eyeball language the
  automated surfaces cannot judge

## Red flags — never

- Skip the tracker-sync or workspace preflight
- Invent a tracker or ticket set when config is absent or the user declined
- Start implementation on main/master without explicit consent
- Create a worktree without asking, or treat "current branch" as consent
  for main/master
- Dispatch the first task before the todo list exists (tasks **and** Close
  branch)
- Silent-skip polish (no written `skip: no polish predicate`)
- Treat EOD, demo, or "inspect was clean" as a polish predicate
- Move to package/land with the Close branch todo still open
- Promote checks as "ID-tagged tests" — IDs stay in docs
