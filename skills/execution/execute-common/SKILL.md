---
name: execute-common
version: 2.0.0
description: Use when build-in-waves, build-by-story, or build-inline loads the shared controller recipe — produces a runtime-bound session snapshot, lease state, ledger state, and a revision-bound close receipt.
---

# Execute-family controller recipe

**One home** for controller steps and runtime state shared across
`build-in-waves`, `build-by-story`, and `build-inline`. Each route owns only its
mode iron law and scheduler/unit behavior. The shared task lifecycle is in
`task-lifecycle.md` beside this file.
Load this file when that skill's Setup or After-last step says to.

This folder is a registered Engineer Pack skill so `npx skills add`
copies it beside the execute-family skills.

## Contents

- Session preflight
- Runtime binding and lease preflight
- Ledger check
- Todos — GATE
- Close sequence (after the last task / last unit)
- Polish predicate
- Sample predicate
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
   implementer briefs and later `land-branch`. IF no, or the file is
   absent / declares no tracker → empty ticket set; continue (unconfigured
   tracker is normal, not a failure).
2. **Workspace / branch.** If no isolated workspace exists yet: isolate in a
   worktree, or implement on the current branch? Do not create a worktree
   unasked. Isolation → REQUIRED SUB-SKILL: use `isolate-workspace`. Current
   branch is main/master → separate explicit consent before implementing;
   "no worktree" is not consent to touch main/master.

*Done when: tracker choice (or empty set) and workspace choice are clear.*

## Runtime binding and lease preflight

After session preflight and before the first dispatch, bind the execution to the
actual harness and provider/model in use. Planning artifacts remain portable;
the runtime snapshot records what this session can really do.

Write `.skills/<CODE>/execution-session.json` with at least:

```json
{
  "schema_version": 1,
  "harness": "unknown",
  "provider": "unknown",
  "model": "unknown",
  "resume_context": "supported|unsupported|unknown",
  "fork_context": "supported|unsupported|unknown",
  "worktree_isolation": "supported|unsupported|unknown",
  "cache_control": "none|implicit|explicit|unknown",
  "token_telemetry": "none|aggregate|per_turn|unknown",
  "pricing_policy": {
    "source_url": null,
    "observed_at": null,
    "threshold_basis": "input_tokens|prompt_tokens|context_tokens|unknown",
    "repricing_scope": "all_request_tokens|marginal_tokens|flat|unknown",
    "tiers": []
  },
  "effective_concurrency": null,
  "rotations": []
}
```

Use capability facts exposed by the active harness/API. Record `unknown` when a
fact is unavailable; never infer support from a harness name, a model family,
or a cache key. If binding is ambiguous in a way that changes safety or cost,
ask once and persist the answer before dispatch.

Before every worker or reviewer resume, calculate the next-request estimate from
system instructions, tool schemas, retained history, feature capsule, task
delta, cache estimate, and output reserve. Rotate the lease before dispatch if
any hard trigger holds:

- the semantic unit ends or the next task materially changes required context;
- the projected request exceeds the active context safety reserve;
- the provider/model pricing policy predicts an all-token cliff, or continuing
  costs materially more than a fresh role context;
- compaction, harness change, broad scope/invariant change, or context confusion
  invalidates the retained context.

When `pricing_policy` is unknown, use the configured conservative budget and
record the decision as unknown-policy; never invent a provider threshold. Add a
rotation record with reason, previous lease ID, next lease ID, projected input
tokens, and policy/source reference. A fresh context receives the feature
capsule and task delta, not the entire prior transcript.

If a ready set cannot safely fan out because `worktree_isolation` is unsupported
or surfaces overlap, set `effective_concurrency` to one and record the
degradation. Never increase concurrency beyond the approved plan.

*Done when: the runtime snapshot exists before dispatch, every unavailable
capability is explicit, and the first effective concurrency/lease decision is
recorded.*

## Ledger check

Make `.skills/` local-only:

```
grep -qxF '.skills/' .gitignore 2>/dev/null || { printf '.skills/\n' >> .gitignore && git commit -m 'chore: ignore local skills artifacts' -- .gitignore; }
```

Read `.skills/<CODE>/progress.md` if it exists. Every task (and, on
story-unit, every unit) it marks complete IS complete — resume at the first
item it does not list. *Done when: next task / unit is known.*

A `Verified:` line is a completion claim. REQUIRED SUB-SKILL: use
`prove-claim`. The line itself is the slot: `Verified: <what holds> — by
<command>, covering <what>`. An ID alone is not a checkpoint.

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
   test files).
5. **Sample — observable conditional.** Evaluate the **sample
   predicate** below. IF any clause is true → write `sample: required` on
   the Close notes. IF no clause is true → write
   `skip: no sample predicate`. Do not start `/select-review-sample`.
   Silent skip (no notes line) is still a red flag.
   "Inspect was clean" and "always name so we cannot forget" are **not**
   predicates.
6. **Product walk — observable conditional.** Evaluate the **walk
   predicate** below. IF any clause is true → REQUIRED SUB-SKILL: use
   `review-product-flow` (it owns vet + naming the walkthrough). IF no
   clause is true → do not open the product-walk trio.
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
| "A sample skip line invents a predicate this file does not write" | The predicate is below. Silent skip is still a red flag. |

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

## Sample predicate

True when any of: the user asked for a sample or attention allocation; branch
diff paths hit the B1 defaults in
`skills/review/select-review-sample/references/signals.md` extended by project
`Risk globs`; or the branch diff lists more than 15 files. "Always name so we
cannot forget" is not an ask.

## Product-walk predicate

True when **any** of:

- the user asked for a product walk, dogfood, or walkthrough
- `validate-feature` reports neither-API-nor-UI
- an approved requirement uses visual / feel / eyeball language the
  automated surfaces cannot judge
- `review-ui`'s report (via `inspect-change`'s UI lane) lists any
  `needs-human-eyes` item
- the branch adds a **new** user-facing screen or visual surface — not only
  changes within existing ones

## Red flags — never

- Skip the tracker-sync or workspace preflight
- Invent a tracker or ticket set when config is absent or the user declined
- Start implementation on main/master without explicit consent
- Create a worktree without asking, or treat "current branch" as consent
  for main/master
- Dispatch the first task before the todo list exists (tasks **and** Close
  branch)
- Silent-skip polish (no written `skip: no polish predicate`)
- Silent-skip sample (no written `sample: required` or `skip: no sample predicate`)
- Start `/select-review-sample` in this skill
- Treat EOD, demo, or "inspect was clean" as a polish predicate
- Move to land-branch with the Close branch todo still open
- Write a partial receipt or bind it to evidence from before the last mutation
- Promote checks as "ID-tagged tests" — IDs stay in docs
