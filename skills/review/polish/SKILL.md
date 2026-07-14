---
name: polish
description: Use when changed code needs a quality cleanup actually applied rather than
  reported — code that reimplements a helper the repo already has, needless
  complexity, dead code, wasted work or repeated I/O, tech debt, a bandaid fix
  at the wrong depth. The behavior-preserving refactor and final tidy pass over a
  diff, branch, or PR before merge, and the last step of execute-plan. For
  correctness bugs, a crash, or a merge verdict use code-review or debug instead.
---

# Polish

Four cleanup agents read the diff from four angles, then you apply what they find. The deliverable is **cleaner code that behaves identically** — not a report, and not a bug fix.

Two boundaries define this skill, and both are load-bearing:

<NON-NEGOTIABLE>
1. **Behavior does not change.** The suite that was green before the cleanup is green after it — and no test is edited to make that true. A cleanup that needs a test rewritten to pass is not a cleanup.
2. **Correctness bugs are out of scope.** Do not hunt them, and do not fix the ones you trip over. Record them and name `code-review` (or `debug`, if something is already broken) for the user to run. A diff that both restructures and repairs can be reviewed as neither.
</NON-NEGOTIABLE>

## 1. Pin the diff — fail fast

Run `git diff @{upstream}...HEAD` (falling back to `git diff main...HEAD`, then `git diff HEAD~1`) to get the diff under review. If there are uncommitted changes, or the range diff comes back empty, also run `git diff HEAD` and fold the working tree into scope — polish usually runs before the commit. A PR number, branch, or file path passed as an argument replaces all of this. An empty diff stops here and says so; it never becomes four agents reviewing nothing. *Done when: the diff is non-empty and its scope is named.*

## 2. Record the green baseline

Find and run the suite covering the changed files, and record the result **before touching anything**. Green is the baseline you must reproduce in step 6. Red here means the branch is already broken — stop and name `debug`; polishing on top of a failing suite destroys the only evidence that your cleanup preserved behavior. *Done when: the suite is green and the command that proved it is written down.*

## 3. Dispatch four cleanup agents in parallel

Send ONE message containing all four dispatches so they run concurrently and neither pollutes the other's context. Every agent is **read-only** — it reports, you apply. Keep each brief under 400 words, and never pre-judge: no "don't flag", no pre-rated severities.

Each agent receives the diff, the repo path, and exactly one angle below. Each returns findings as `file:line`, a one-line summary, **the concrete cost** (what is duplicated, wasted, or made harder to maintain — never a hypothetical crash), and **the named replacement** — the specific helper, simpler form, or cheaper alternative to use instead. A finding with no named replacement is not actionable; the agent drops it.

### Reuse

Flag new code that reimplements something the codebase already has. Grep the shared and utility modules, plus the files adjacent to the change, and name the existing helper to call instead.

### Simplification

Flag unnecessary complexity the diff adds: redundant or derivable state, copy-paste with slight variation, deep nesting, dead code left behind. Name the simpler form that does the same job.

### Efficiency

Flag wasted work the diff introduces: redundant computation or repeated I/O, independent operations run sequentially, blocking work added to startup or a hot path. Also flag long-lived objects built from closures or captured environments — they hold the whole enclosing scope alive for the object's lifetime, which is a memory leak when that scope holds large values; prefer a class or struct that copies only the fields it needs. Name the cheaper alternative.

### Altitude

Flag changes implemented at the wrong depth. Special cases layered onto shared infrastructure are the tell that a fix did not go deep enough — prefer generalizing the underlying mechanism over adding another special case. Name the mechanism that should have absorbed the change.

*Done when: all four agents have reported.*

## 4. Triage

Dedup findings that point at the same line or the same underlying mechanism — four angles routinely see one flaw from four sides. Then drop, without arguing:

- anything whose fix would change observable behavior (that is a design change; route it to `amend` or `correct-course`)
- anything requiring edits well outside the pinned diff
- anything you judge a false positive

Record each drop with its one-line reason. A silently discarded finding is indistinguishable from a finding you never received. *Done when: every finding is queued to apply or recorded as dropped, with a reason.*

## 5. Apply

Fix each surviving finding directly, smallest blast radius first. Stay inside the pinned diff's files. REQUIRED SUB-SKILL: use `tdd` — its refactor discipline is exactly this step: the tests stay fixed while the code underneath them moves. *Done when: every queued finding is applied or has moved to the dropped list with a reason.*

## 6. Prove behavior held

Re-run step 2's exact command. It must be green, and **no test file may appear in `git diff`** for this cleanup. REQUIRED SUB-SKILL: use `verify` — "the cleanup looks safe" is not evidence, and a refactor is the single easiest place to break something while feeling certain you did not. A red suite means revert the offending fix, not repair it forward.

One carve-out, and it is narrow: a test may be **deleted** when the only thing it pinned was code the Simplification angle removed as dead. Deleting it requires all three — the target is gone, the behavior is still covered elsewhere by a test you **name**, and the deletion is stated in step 7's report. A test may never be *rewritten, retargeted, renamed, or moved*; that is the goalpost move rule 1 forbids, and "I retargeted the same assertion at the canonical function" is that move. If a test resists deletion, keep the old symbol as a thin alias delegating to the canonical one — the duplicated *rule* dies, which was the finding, and the suite never moves.

*Done when: the suite is green by the same command that was green in step 2, and any deleted test is named in the report with its replacement coverage.*

## 7. Report

State what was fixed, what was dropped and why, and — separately — any correctness bug an agent noticed in passing, named for `code-review` or `debug` rather than fixed here. If nothing survived triage, say the code was already clean. **That is a successful run, not a failed one**; four agents finding nothing is a real result, and manufacturing a finding to justify the pass is the one outcome worse than no findings at all. *Done when: fixed / dropped / referred-out are all stated.*

## Inline fallback (no subagent capability)

Run the four angles yourself, sequentially, in one context — Reuse, then Simplification, then Efficiency, then Altitude. Close out one angle completely, writing its findings down, before opening the next; the whole value of four separate contexts is that no angle gets to see (and get anchored by) another's conclusions, and finishing one before starting the next is the only way to approximate that in a single context. Steps 1, 2, and 4–7 are unchanged, and step 6 is not optional just because the review was cheaper.

## Red Flags — Never

- Editing a test so the cleaned-up code passes it
- Fixing a correctness bug you noticed "while you were in there"
- Touching a file the pinned diff never touched
- Applying a finding whose concrete cost you cannot state in one line
- Reporting the cleanup done without re-running step 2's command
- Inventing a finding because four agents returning nothing "looks wrong"

## Rationalizations

| Thought | Reality |
|---|---|
| "That's obviously a bug — it'd be silly to leave it" | Then it deserves a real review, not a drive-by fix buried in a cleanup commit. Name it for `code-review`; a diff that restructures *and* repairs can be reviewed as neither |
| "The test asserted the old internals, so I updated it" | You changed behavior and moved the goalposts that would have caught it. Revert. If a test genuinely must change, this is not polish |
| "I only *repointed* the test at the canonical function — identical assertion, no coverage lost" | The most common way this rule is broken, and the most reasonable-sounding. You deleted the test that stood in the way and wrote a new one that does not. Keep the old symbol as a thin alias instead: the duplicated rule still dies, and the suite never moves |
| "It's much cleaner if I also touch these three files" | Outside the pinned diff is outside scope. The cleanup you cannot bound is the cleanup nobody can review |
| "The suite is slow — the affected tests are enough" | The baseline you recorded in step 2 is the only proof you have. A narrower re-run proves something narrower than what you are about to claim |
| "No findings came back, so I'll look harder for something" | Confirming the code is already clean IS the deliverable. A manufactured finding costs a real edit against a fake cost |
| "Behavior technically changed, but strictly for the better" | That is a design change wearing a cleanup's clothes. Route it to `amend` and let it be seen |
