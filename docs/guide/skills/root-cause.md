# `root-cause`

> Find the root cause before touching a fix. Build a feedback loop that is red because of this exact bug, then work backward to what actually causes it.

|  |  |
|---|---|
| **Bucket** | execution |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | the failing signal (test, error, trace, log), git history and recent changes, the owning feature's `requirements.md` |
| **Writes** | a red-capable feedback loop and a failing regression test, a causal disposition request (human accept/reject/supersede), one fix commit stating proposition + disposition status, a tier-1 mini-spec (fix requirement + `SHALL CONTINUE TO` guard) in `requirements.md` (or `docs/specs/fixes.md`) |
| **Calls** | [`debug-remote`](debug-remote.md) (when the failure is already deployed and no pack exists), [`test-first`](test-first.md) (the regression test and the fix), [`prove-claim`](prove-claim.md) (before claiming fixed), [`scan-architecture`](scan-architecture.md) (architectural findings) |
| **Called by** | [`test-first`](test-first.md) (when the change is a bugfix), [`amend-feature`](amend-feature.md), [`build-in-waves`](build-in-waves.md), [`validate-feature`](validate-feature.md), [`validate-api`](validate-api.md), [`validate-ui`](validate-ui.md) |

## When it fires

Anything behaves unexpectedly — a failing test, an error or exception, a crash, a reported bug, wrong output, a performance regression, a flaky CI job — and it fires **before** any fix is proposed or applied. If that failure is only on a **deployed** environment and there is no remote evidence pack yet, [`debug-remote`](debug-remote.md) runs first.

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
NO AGENT-AUTHORED AUTHORITATIVE CAUSAL ACCEPTANCE
```

Guess-and-patch wastes hours and plants new bugs. The process applies to every technical issue, and it applies hardest exactly when it is tempting to skip: emergencies, "obvious" one-liners, and the moment right after a previous fix didn't work.

The agent investigates and may **request** a causal strength. An eligible human **accepts, rejects, or supersedes** one exact proposition. Writing `confirmed root cause` into a commit is not that acceptance.

## Phase 1 — build the feedback loop (the gate)

Before any theory-building, construct and RUN a **red-capable signal**: one command — a test, a script, a curl — that is red *now* because of this exact bug and goes green when it is fixed. Build the right feedback loop and the bug is 90% fixed; every later phase merely consumes it. Catch yourself reading code to form a theory before this command exists? Stop — no red-capable command, no Phase 2.

The skill lists ten construction tactics in rough order of preference:

1. Failing test at whatever seam reaches the bug (unit, integration, e2e)
2. curl / HTTP script against a running dev server
3. CLI invocation on a fixture input, diffed against known-good output
4. Headless browser script asserting on DOM / console / network
5. Replay of a captured audit-trace (saved request, payload, event log) through the code path
6. Throwaway harness — a minimal slice of the system exercising the bug path
7. Property / fuzz loop over random inputs when output is "sometimes wrong"
8. Bisection harness (`git bisect run`) when the bug appeared between two known states
9. Differential loop — same input through old vs new version, diff the outputs
10. Human-in-the-loop script — last resort, only when a human must physically act; script their steps so the loop stays structured

Once the loop is red, **tighten it** along three axes:

- **Faster** — cache setup, narrow the scope, so a run takes seconds, not minutes.
- **Sharper** — assert the user's exact symptom, not merely "didn't crash".
- **Deterministic** — pin time, seed randomness, isolate the filesystem.

For a non-deterministic bug, don't chase a clean repro — **raise the reproduction rate** (loop the trigger 100×, add stress, shrink timing windows) until it is high enough to root-cause against. Genuinely cannot build any loop at all? Say so explicitly, list what you tried, and ask the user for a reproducing environment, a captured artifact, or permission to add temporary instrumentation. Do not proceed on vibes.

**Gate check:** name the command, paste one run of its red output.

## Phase 2 — reproduce and minimise

Run the loop and watch it go red with the failure the user described — a nearby *different* failure means the wrong bug and therefore the wrong fix. Read the complete error (full message, full stack, line numbers; errors often contain the answer) and check recent changes: `git diff`, new dependencies, config, environment.

Then shrink the repro **one cut at a time** — inputs, config, callers, steps — re-running after each cut, until every remaining element is load-bearing: removing any one turns it green. A minimal repro shrinks the hypothesis space and becomes the regression test.

Two moves matter when the system has depth:

- **Instrument the boundaries.** For multi-component systems (CI → build → deploy, API → service → DB), log what enters and exits every layer and run once to see *where* it breaks, before touching any fix.
- **Audit Trace backward.** When the error surfaces deep in a call chain, follow the bad value through its callers to the original trigger. Never fix only where the error appears; that is treating the symptom.

## Phase 3 — hypothesise

Write **3–5 ranked, falsifiable hypotheses before testing any** — a single hypothesis anchors you to the first plausible idea. Each needs a stated prediction: "if X is the cause, then changing Y makes the bug disappear." No statable prediction means it is a vibe — sharpen it or discard it. Show the ranked list to the user (they often re-rank it instantly), but don't block if they are away.

Test the smallest hypothesis first, **one variable at a time** — never stack changes, because stacked changes hide which one worked and which one broke something new. A few instrumentation rules keep the search clean:

- Prefer a debugger or REPL when available — one breakpoint beats ten logs.
- Otherwise use targeted logs with a **unique prefix per probe** (e.g. `[DBG-x7q2]`) so cleanup is a single grep — never log-everything-and-grep.
- Performance bugs are the exception: measure a baseline first (profiler, timing harness), then bisect, because logs mislead here.

A falsified hypothesis gets struck; move to the next, and don't pile a new fix on top of a failed one. Don't understand something? Say "I don't understand X" and investigate — never pretend and guess.

## Causal disposition

Keep investigation state independent from requested strength. Before authoritative confirmation, ask an eligible human to accept / reject / supersede one exact proposition against its support set. Operational success (rollback, green error rate) does not promote accepted causal strength. Green Phases 1–3 means ready to request disposition; confirmed means the human accepted.

## Phase 4 — fix

1. **Failing regression test first**, via [`test-first`](test-first.md), once the proposition is on the disposition request — at a **correct seam**.
2. **Human accept** of that exact proposition before landing production-code as a corrective fix. Slack "ship it" on prose is not acceptance; in-session explicit accept of the stated proposition counts.
3. **One fix** addressing the accepted proposition. No "while I'm here" improvements, no bundled refactoring.
4. Watch the regression test pass, re-run the full suite, and re-run the Phase 1 loop against the original un-minimised scenario.

**Three failed fix attempts = STOP.** The architecture is in question, not the latest hypothesis — especially if each fix reveals new coupling somewhere else. Discuss with the user before attempt 4.

## Exit — mini-spec, cleanup, post-mortem

- Add a **tier-1 mini-spec**: a fix requirement plus a `SHALL CONTINUE TO` guard requirement in the owning feature's `requirements.md` (or `docs/specs/fixes.md` if no feature owns it), and tag the regression test with the new ID.
- **Remove ALL instrumentation** — grep for the `[DBG-...]` prefixes, delete throwaway harnesses.
- In the commit/PR: state the **proposition**, requested or **human-accepted** strength, scope, and support pointers — never agent-authored `confirmed root cause` as acceptance.
- Route Task "what would have prevented this bug?" If the answer is architectural (no good seam, hidden coupling, tangled callers), hand the specifics to [`scan-architecture`](scan-architecture.md) — after the fix lands, when you know the most.
- [`prove-claim`](prove-claim.md) is a required sub-skill before claiming the bug fixed.

## Rationalizations it names

| Thought | Reality |
|---|---|
| "Emergency, no time for process" | Root-cause debugging is FASTER than guess-and-check thrashing |
| "It's obviously X, let me just fix it" | Seeing a symptom is not understanding a cause |
| "Quick patch now, investigate later" | The patch becomes permanent and the cause strikes again |
| "Try several changes at once to save time" | You can't tell which one worked, and one of them broke something |
| "Too simple to need a repro" | Simple bugs have root causes too; the loop takes minutes |
| "I'll add the regression test after the fix" | Untested fixes regress; the red test is the proof the fix fixes |
| "One more attempt" (after 2+ failures) | Attempt 4 without an architecture discussion is thrashing |
| "Exit says state the confirmed root cause — that commit line is acceptance" | Exit records proposition + disposition status; only an eligible human accepts |
| "Human disposition is ceremony" | Agent-authored authoritative acceptance is forbidden; the disposition request is the gate |
| "Staff LGTM'd the narrative / ship the Exit" | Prose LGTM ≠ accept of one exact proposition against its support set |

## User signals — return to Phase 1

Certain phrases from the user are a diagnostic that the process was skipped:

| The user says | It means |
|---|---|
| "Stop guessing" | You proposed fixes without a root cause — back to Phase 1 |
| "Is that actually happening?" | You assumed without verifying — gather evidence |
| "Will that show us anything?" | Your probe maps to no prediction — restate hypotheses |
| "We're going in circles" | Count your failed fixes; you're probably at the architecture gate |
| "Who accepted that cause?" | You self-certified — run the disposition request |

## Worked example

A test is flaky in CI and green locally.

- **Phase 1.** The existing test is not red on demand, so it is not yet a signal. The loop becomes `for i in $(seq 200); do npm test -- session.test.ts || break; done`, which reproduces the failure about one run in forty. Tightening it means seeding the clock, and the rate jumps to one in three — high enough to root-cause against. Gate check: the command is named and one red run is pasted.
- **Phase 2.** The stack points at a token comparison, but instrumenting the boundary shows the bad value entering two layers earlier, so the audit-trace goes backward to the original trigger — a timer that fires before hydration.
- **Phase 3.** Five ranked, falsifiable hypotheses; the smallest is tested first with a `[DBG-k9f1]` probe, one variable at a time; the third survives its prediction.
- **Phase 4.** A regression test at the hydration seam fails first via `test-first`, then one fix, then the Phase 1 loop runs 200 clean iterations.
- **Exit.** A `SHALL CONTINUE TO` guard requirement, every `[DBG-...]` line grepped out, the proposition + human disposition status in the commit message, and `prove-claim` before the word "fixed".

## Why it is written the way it is

Root Causeging fails in a predictable way: an agent sees a symptom, forms one theory, and patches where the error appears. Phase 1 is a hard gate placed *before* theory-building precisely because that is the step under pressure everyone skips — and building the loop first is also what makes every later phase cheap. The two tables are not filler; each rationalization row and each user-signal row is a specific real failure the skill turns into a named checkpoint, so the agent can catch itself (or hear the user catching it) and return to the gate.

## See also

- [`test-first`](test-first.md) — writes the failing regression test at a correct seam
- [`prove-claim`](prove-claim.md) — the gate before "fixed" may be said
- [`scan-architecture`](scan-architecture.md) — where architectural root causes go
- [The gates](../concepts/gates.md) — how this Iron Law relates to the others
