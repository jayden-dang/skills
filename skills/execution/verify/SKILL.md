---
name: verify
description: Use when about to say anything that implies success — "done",
  "fixed", "passing", "works", or any paraphrase — and before committing,
  opening a PR, closing a task, or reporting a subagent's result.
---

# Verify

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If the proving command did not run just now, in this session, the claim is unavailable to you. An unverified claim isn't optimism — it's a false statement.

## The Gate Function

Before any status claim or expression of satisfaction:

1. **IDENTIFY** — which command proves this exact claim? (Commands come from `docs/agents/project.md`. Missing? Say so, suggest `setup-repo`, and identify the command manually.)
2. **RUN** — execute it fresh and complete. No cached results, no partial scopes, no "it passed earlier".
3. **READ** — the full output: exit code, failure count, warnings. Not the last line.
4. **CONFIRM** — does the output actually support the claim? If no: report the real status, with the evidence. If yes: make the claim, with the evidence.

Skip any step and you are lying, not verifying.

## Claim → evidence

| Claim | Requires | Never sufficient |
|---|---|---|
| "Tests pass" | Full fresh run, zero failures, output read | An earlier run; a subset; "should pass" |
| "Build/lint/typecheck clean" | That command, exit 0, zero warnings | A different tool passing |
| "The feature works" | The affected flow driven through the running system and observed (REQUIRED SUB-SKILL: use `acceptance-check`, or `dogfood` for a manual pass) | Green unit tests alone |
| "The bug is fixed" | Original symptom re-tested and gone | The code changed |
| "The agent/subagent completed X" | You inspected the diff yourself | The agent's own success report |
| "Requirements met" | `python3 scripts/check_trace.py` **and** `python3 scripts/check_graph.py --verify` pass AND each acceptance criterion checked off individually against observed behavior | Green tests alone |

## Regression-proof pattern

A regression test only counts once it has demonstrably caught the bug:

```
write test → passes → revert the fix → test MUST fail → restore fix → passes
```

A test that survives the revert is testing nothing.

## Red flags — stop and run the gate

- "Should work", "probably", "seems to", "I'm confident"
- Satisfaction before evidence ("Great, that's done!")
- Claiming from memory of an earlier run
- About to commit, push, or PR without a fresh run
- Tired and wanting the task over — exhaustion is not evidence

| Thought | Reality |
|---|---|
| "It should pass now" | Run it |
| "I just ran it ten minutes ago" | The code changed since; run it again |
| "The agent said success" | Read the diff |
| "Partial check is enough" | Partial proves nothing about the rest |
| "I'll batch-verify everything at the end" | Each claim is verified when made; a batch at the end lets earlier false claims stand as fact meanwhile |
| "CI will catch it after merge" | CI runs after the claim ships; the gate is before you claim, not after someone else pays |
| "Different phrasing, so the rule doesn't apply" | The rule covers paraphrases and implications |

Run the command. Read the output. Then — and only then — say it.
