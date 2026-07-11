# `verify`

> No "done", "fixed", or "passing" until the proving command ran fresh, in this session, and its full output was read and confirmed to support the claim.

|  |  |
|---|---|
| **Bucket** | execution |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | `docs/agents/project.md` (the proving commands); the full output of whatever command it runs |
| **Writes** | nothing — it runs proving commands and reads their output; it produces evidence, not files |
| **Calls** | [`acceptance-check`](acceptance-check.md) or [`dogfood`](dogfood.md) (to prove "the feature works"), the `check-trace` and `check-graph` scripts (to prove "requirements met") |
| **Called by** | nearly every skill before a completion claim — [`tdd`](tdd.md), [`debug`](debug.md), [`execute-plan`](execute-plan.md), [`finish-branch`](finish-branch.md), [`handoff`](handoff.md), and more |

## When it fires

Before saying anything that implies success — "done", "fixed", "passing", "works", or any paraphrase — and before committing, opening a PR, closing a task, or reporting a subagent's result. If a status claim is about to be spoken, this skill runs first.

The trigger deliberately covers paraphrases and implications, not just the literal words. "That should be good now", "looks done to me", and a satisfied "great, shipped it" are all completion claims wearing different clothes, and each one puts the gate in front of the sentence.

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If the proving command did not run just now, in this session, the claim is unavailable to you. An unverified claim isn't optimism — it's a false statement.

## The Gate Function

Four steps run before any status claim or expression of satisfaction, and skipping any one of them is lying, not verifying:

1. **IDENTIFY** — which command proves this exact claim? Commands come from `docs/agents/project.md`; if it is missing, say so, suggest `setup-repo`, and identify the command manually.
2. **RUN** — execute it fresh and complete. No cached results, no partial scopes, no "it passed earlier". The code has changed since the last run, so the last run proves nothing.
3. **READ** — the full output: exit code, failure count, warnings. Not just the last line, where a green summary can sit above a stack of warnings or a nonzero exit.
4. **CONFIRM** — does the output actually support the claim? If no, report the real status with the evidence. If yes, make the claim with the evidence.

The steps are ordered on purpose: you cannot run a command you have not identified, and you cannot confirm output you have not read in full.

## Claim → evidence

Each claim has a required proof and a set of things that are never sufficient for it. The last row is the strictest: "requirements met" needs **both** trace scripts to pass **and** every acceptance criterion checked off individually.

| Claim | Requires | Never sufficient |
|---|---|---|
| "Tests pass" | Full fresh run, zero failures, output read | An earlier run; a subset; "should pass" |
| "Build/lint/typecheck clean" | That command, exit 0, zero warnings | A different tool passing |
| "The feature works" | The affected flow driven through the running system and observed ([`acceptance-check`](acceptance-check.md), or [`dogfood`](dogfood.md) for a manual pass) | Green unit tests alone |
| "The bug is fixed" | Original symptom re-tested and gone | The code changed |
| "The agent/subagent completed X" | You inspected the diff yourself | The agent's own success report |
| "Requirements met" | `node scripts/check-trace.mjs` **and** `node scripts/check-graph.mjs --verify` pass, AND each acceptance criterion checked off individually against observed behavior | Green tests alone |

## Regression-proof pattern

A regression test only counts once it has demonstrably caught the bug it guards. The proof is a four-move cycle:

```
write test → passes → revert the fix → test MUST fail → restore fix → passes
```

The load-bearing move is the middle one: revert the fix and confirm the test goes red. A test that stays green with the fix removed is asserting something the bug never touched — it is testing nothing, and it will not catch the regression when it returns. Only after the test has both passed with the fix and failed without it may it be counted as coverage.

## Red flags — stop and run the gate

- "Should work", "probably", "seems to", "I'm confident"
- Satisfaction before evidence ("Great, that's done!")
- Claiming from memory of an earlier run
- About to commit, push, or PR without a fresh run
- Tired and wanting the task over — exhaustion is not evidence

Each of these has a stock rationalization, and each rationalization has a one-line answer:

| Thought | Reality |
|---|---|
| "It should pass now" | Run it |
| "I just ran it ten minutes ago" | The code changed since; run it again |
| "The agent said success" | Read the diff |
| "Partial check is enough" | Partial proves nothing about the rest |
| "Different phrasing, so the rule doesn't apply" | The rule covers paraphrases and implications |

## Worked example

A subagent reports back: "Task done, all tests passing." The controller is about to relay that upward as complete. The gate stops it and runs the four steps:

- **IDENTIFY.** The claim being relayed is really two claims — "tests pass" and "the subagent completed X" — so the proofs are the project's test command *and* an inspection of the diff.
- **RUN.** The controller runs the full suite fresh rather than trusting the report; it comes back green.
- **READ.** The exit code is 0, but the output carries three deprecation warnings the subagent's one-line summary omitted — and the "never sufficient" column already says the agent's own success report does not prove completion.
- **CONFIRM.** The controller reads the actual diff, finds one requirement the report claimed but never implemented, and reports the real status with evidence instead of the optimistic one.

The claim was never the agent's to make from memory. The fresh run and the inspected diff are what make it sayable at all.

## Why it is written the way it is

`verify` is the smallest skill in the set and deliberately so — it is a single gate the whole system routes through before any success is spoken, which is why so many other skills list it as a required last step. Its failure mode is not ignorance but momentum: the agent knows the tests should pass, is tired, and wants the task over, so it claims from memory. Everything here — the four-step function, the "never sufficient" column, the rationalization table that answers each excuse by name — exists to convert that momentum into one concrete action: run the command, read the output, then and only then say it.

## See also

- [The gates](../concepts/gates.md) — how this Iron Law relates to the other three
- [`tdd`](tdd.md) — hands off to `verify` before any completion claim
- [`acceptance-check`](acceptance-check.md) — what proves "the feature works"
- [Traceability](../concepts/traceability.md) — why "requirements met" needs the trace scripts
