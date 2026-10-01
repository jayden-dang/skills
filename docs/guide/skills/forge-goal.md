# `/forge-goal`

> Native-language interview that finds **what you want an unattended run to achieve**, then one paste-ready **goal prompt** for a fresh session on any agent: probed checks, guards, a verify-every-round loop, a fresh final audit, and `BLOCKED:` / `STOPPED:` lines.

|  |  |
|---|---|
| **Bucket** | discovery |
| **Invocation** | user-invoked (`/forge-goal`) — agents must never auto-invoke it |
| **Reads** | the repository first — scripts, tests, bench commands, every caller of what the ask names, contract comments — so it never asks what it can read |
| **Runs** | only checks that change nothing, each exactly as it will appear in the goal, to prove it runs and is not already green |
| **Writes** | the goal prompt in chat; edits no file |
| **Calls** | `clarify-decisions` for the interview channel (its own card, no recommendation) |
| **Called by** | nobody — it sits outside every chain, like `/forge-prompt` |

## Why it exists

A long run nobody steers needs two things a normal prompt does not. It needs a **want the user
actually holds**: asked to make a repo "better", unskilled runs offered whatever the repo made easy
to check (lint, README) and one recommended it; the user wanted the settings page usable on a
phone. And it needs **a way to end that someone can verify**: whoever judges the run — Claude
Code's `/goal` evaluator, Qwen's verifier, the agent's own completion audit, or you in the morning
— sees only what the run printed.

## The interview

One card per message, in the language you write in, never a recommendation:

1. **The want** — what bothers you, and what will be different when it is done
2. **One objective** — unrelated outcomes are split into separate goals
3. **The bar** — the state that means done, as a command that exits plus the output that proves it
4. **Guards** — what must not change; what the run may touch (files, dependencies, commits, branch)
5. **Stop calls** — situations that need a person
6. **The bound** — rounds or hours

"Your call" on *how* stays out of the goal. "Your call" on any of the six becomes a `BLOCKED:` line.

## What it hands back

```
GOAL / WHY
DONE WHEN      — numbered checks: `command` → expected output
MUST HOLD      — guards checked every round
EACH ROUND     — orient (progress file, git log, round check) → one smallest step
                 → verify (round check + every guard) → record (progress file, commit or not)
FINISH         — re-run every check fresh in one message, pair each DONE line with its output,
                 then print DONE:
STOP EARLY     — BLOCKED: <decision> when <situation> · STOPPED: <progress> after <bound>
READ FIRST     — paths, not pasted bodies
```

Numbered, under 4,000 characters. Below it: a probe line per check, how to run it (`/goal` where
the agent has one, otherwise the first message of a fresh session in auto-approve mode), split-off
goals, and the two or three lines with the highest blast radius.

## How it differs from `/forge-prompt`

| | `/forge-prompt` | `/forge-goal` |
|---|---|---|
| Reader | a person-steered session | a run nobody steers |
| Open questions | travel as `Open — ask me` | close, or become a `BLOCKED:` line |
| Method | never named | never named — but the round protocol and *how done is proven* are the whole block |
| Done signal | what the user would look at | a command and the output it must print, re-run fresh at FINISH |
