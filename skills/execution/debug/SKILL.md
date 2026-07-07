---
name: debug
description: Use when anything behaves unexpectedly — a failing test, a reported
  bug, a crash, wrong output, a performance regression, a flaky CI job — and
  before proposing or applying any fix.
---

# Debug

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

Guess-and-patch wastes hours and plants new bugs. This process applies to every technical issue — and applies hardest when it's tempting to skip: emergencies, "obvious" one-liners, and the moment right after a previous fix didn't work.

## Phase 1 — Build the feedback loop (the gate)

Before ANY theory-building, construct and RUN a **red-capable signal**: one command — a test invocation, a script, a curl — that is red now because of this exact bug and will go green when it is fixed. Build the right feedback loop and the bug is 90% fixed; every later phase merely consumes it.

Catch yourself reading code to form a theory before this command exists? Stop. No red-capable command, no Phase 2.

Tactics for constructing one, in rough order of preference:

1. Failing test at whatever seam reaches the bug (unit, integration, e2e)
2. curl / HTTP script against a running dev server
3. CLI invocation on a fixture input, diffed against known-good output
4. Headless browser script asserting on DOM/console/network
5. Replay of a captured trace (saved request, payload, event log) through the code path
6. Throwaway harness: a minimal slice of the system exercising the bug path
7. Property/fuzz loop over random inputs when output is "sometimes wrong"
8. Bisection harness (`git bisect run`) when the bug appeared between two known states
9. Differential loop: same input through old vs new version, diff the outputs
10. Human-in-the-loop script — last resort, only when a human must physically act; script their steps so the loop stays structured

Then **tighten it**: faster (cache setup, narrow scope — seconds, not minutes), sharper (assert the user's exact symptom, not "didn't crash"), deterministic (pin time, seed randomness, isolate filesystem). Non-deterministic bug? Don't chase a clean repro — raise the reproduction rate (loop the trigger 100x, add stress, shrink timing windows) until it's high enough to debug against.

Genuinely cannot build one? Say so explicitly, list what you tried, and ask the user for a reproducing environment, a captured artifact, or permission to add temporary instrumentation. Do not proceed on vibes.

**Gate check:** name the command, paste one run of its red output.

## Phase 2 — Reproduce and minimise

Run the loop; watch it go red with the failure the user described (a nearby different failure = wrong bug = wrong fix). Read the complete error — full message, full stack trace, line numbers; errors often contain the answer. Check recent changes: git diff, new dependencies, config, environment.

Shrink the repro one cut at a time (inputs, config, callers, steps), re-running after each cut, until **every remaining element is load-bearing** — removing any one turns it green. A minimal repro shrinks the hypothesis space and becomes the regression test.

For multi-component systems (CI → build → deploy, API → service → DB): instrument each boundary — log what enters and exits every layer — and run once to see WHERE it breaks, before touching any fix. When the error surfaces deep in a call chain, trace the bad value backward through its callers to the ORIGINAL trigger. Never fix only where the error appears; that is treating the symptom.

## Phase 3 — Hypothesise

Write 3–5 ranked hypotheses before testing any (a single hypothesis anchors you to the first plausible idea). Each must be falsifiable with a stated prediction: "if X is the cause, then changing Y makes the bug disappear". If you cannot state the prediction, it is a vibe — sharpen it or discard it. Show the ranked list to the user (they often re-rank it instantly); don't block if they're away.

Test the smallest hypothesis first. ONE variable at a time — never stack changes. Instrument with a debugger/REPL when available (one breakpoint beats ten logs), else targeted logs with a unique prefix per probe (e.g. `[DBG-x7q2]`) so cleanup is one grep — never log-everything-and-grep. Performance bugs: measure a baseline first (profiler, timing harness), then bisect; logs mislead here. Don't understand something? Say "I don't understand X" and investigate — never pretend and guess.

Hypothesis falsified? Strike it, move to the next. Don't pile a new fix on top of a failed one.

## Phase 4 — Fix

1. **Failing regression test first.** REQUIRED SUB-SKILL: use `tdd`. The test goes at a CORRECT seam — one that exercises the real bug pattern as it occurred. If no correct seam exists, that is itself a finding: document it and flag it for the post-mortem; a shallow test there is false confidence.
2. **One fix** addressing the root cause. No "while I'm here" improvements, no bundled refactoring.
3. Watch the regression test pass, re-run the full suite, re-run the Phase 1 loop against the original un-minimised scenario.

**Three failed fix attempts = STOP.** The architecture is in question, not your latest hypothesis — especially if each fix reveals new coupling somewhere else. Discuss with the user before attempt 4.

## Exit — mini-spec, cleanup, post-mortem

- Tier-1 mini-spec: add a fix requirement plus a `SHALL CONTINUE TO` guard requirement to the owning feature's `requirements.md` (or `docs/specs/fixes.md` if no feature owns it). Tag the regression test with the new ID.
- Remove ALL instrumentation: grep for your `[DBG-...]` prefixes; delete throwaway harnesses.
- State the confirmed root cause in the commit message.
- Ask: "what would have prevented this bug?" If the answer is architectural (no good seam, hidden coupling, tangled callers), hand the specifics to `improve-architecture` — after the fix lands, when you know the most.
- REQUIRED SUB-SKILL: use `verify` before claiming the bug fixed.

## Rationalizations

| Thought | Reality |
|---|---|
| "Emergency, no time for process" | Root-cause debugging is FASTER than guess-and-check thrashing |
| "It's obviously X, let me just fix it" | Seeing a symptom is not understanding a cause |
| "Quick patch now, investigate later" | The patch becomes permanent and the cause strikes again |
| "Try several changes at once to save time" | You can't tell which one worked, and one of them broke something |
| "Too simple to need a repro" | Simple bugs have root causes too; the loop takes minutes |
| "I'll add the regression test after the fix" | Untested fixes regress; the red test is the proof the fix fixes |
| "One more attempt" (after 2+ failures) | Attempt 4 without an architecture discussion is thrashing |

## User signals — return to Phase 1

| The user says | It means |
|---|---|
| "Stop guessing" | You proposed fixes without a root cause — back to Phase 1 |
| "Is that actually happening?" | You assumed without verifying — gather evidence |
| "Will that show us anything?" | Your probe maps to no prediction — restate hypotheses |
| "We're going in circles" | Count your failed fixes; you're probably at the architecture gate |
