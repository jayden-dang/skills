---
name: forge-goal
version: 1.0.0
description: Turns an outcome you want an agent to chase unattended into one launch-ready goal — checks, guards, a bound, and stop lines a separate judge can settle — for Claude Code /goal, Codex /goal, or any agent CLI. Run it with /forge-goal.
disable-model-invocation: true
---

# Forge Goal

Turn "keep going until X" into **a goal that ends** — read the territory, ask the user only what is theirs to decide, prove every check runs, and hand over one block they paste into `/goal`.

**Where this sits:** beside `/forge-prompt`, in no chain. That one forges a prompt a person will steer; this one forges a goal nobody steers — no one answers questions mid-run, and on Claude Code a different model decides when it is over.

## The Iron Law

```
EVERY LINE OF THE GOAL IS SETTLED BY OUTPUT THE RUN PRINTS.
```

On Claude Code, `/goal` hands the condition and the conversation to a small model (Haiku by default) after every turn. It "doesn't run commands or read files independently" — it reads only what the working session already printed. A clause no command can print is a clause nobody can settle: the run either never ends or ends on the worker's say-so. A goal that "renders correctly at 375px" in a repo with no browser tooling is that clause.

<HARD-GATE>
Edit NO file and start NO part of the goal's work. You read, you ask, you run checks that change nothing. Doing the work belongs to the `/goal` run.
</HARD-GATE>

## 1. Read before you ask

Before the first question, read what answers itself: the files the ask names, `package.json` scripts / `Makefile` / CI config, the test and bench commands that already exist, comments that mark a contract (`Do not rename fields`, `published contract`). A goal written without reading invents its own benchmark and tunes queries a repo without a database does not have.

**Done when:** you can name the existing commands that could prove done, and the objects the ask touches, with paths.

## 2. One objective per goal

A goal is bigger than one prompt and smaller than a backlog. When the ask carries outcomes that do not depend on each other — "fix mobile, clear lint, document env vars" — it is several goals. Say so, and ask which one this run is. The rest are listed back to the user as separate goals; they never ride along.

**Done when:** the goal has one outcome, or the user has chosen one.

## 3. Ask what only the user owns

REQUIRED SUB-SKILL: use `clarify-decisions` for the **channel** — one card per message, inline chat, open-set stop. Its card shape and stop rule apply; the questions below are what the open set holds here.

Ask only the user's calls — never what step 1 can read:

| Slot | Why it is theirs |
|---|---|
| **The bar** — the number or state that means done (p95 under what, which list empty) | A threshold you pick is a goal you wrote for them |
| **Guards** — what must not change on the way | They know which consumer breaks |
| **Stop calls** — which situations need a person, not a guess | Authority, not technique |
| **The bound** — how many turns or hours it may run | Their money and their night |

"Don't grill me" means fewer cards, never zero: the bar and the bound are still theirs. An answer of "your call" on **how** to do the work is right — method stays out of the goal. An answer of "your call" on **the bar** is not yours to fill: it becomes a stop line ("`BLOCKED:` name the bar you would need").

**Done when:** the four slots are answered, or each unanswered one is a stop line.

## 4. Turn each done criterion into a check

A check is **a command plus the output that proves it**: `` `npm run bench` prints p95 under 50 ms ``, `` `grep -rn "from 'moment'" src` prints nothing ``. "Verify it works", "check by loading the page", and "a benchmark you add" are not checks — the judge cannot see the first two, and the worker grades its own homework with the third.

When no command in the territory can show a criterion (the look of a page with no browser tooling, "feels faster"), it is not goal material yet. Tell the user, and let them pick: name a check they accept, or move the criterion out of this goal. Never write it in as if it were checkable.

**Done when:** every done line and every guard is a command with its expected output.

## 5. Probe every check now

Run each check that changes nothing (tests, lint, bench, `grep`, `git diff --stat`) once, and record what it printed. Each must **run**, and the done checks must **not pass yet** — a check that errors burns turns on setup; a check already green ends the goal on turn one. A missing dependency or install step found here goes to the user, not into a hidden first step. A check that writes (migrate, deploy, seed) is never run; mark it `[unprobed]`. So is every check you did not actually run — blocked by a permission, failed on setup, or skipped because its output "is obvious": a predicted output is not a probe result.

**Done when:** every check carries the output you saw it print, or `[unprobed]` — there is no third state.

## 6. Assemble the goal — REQUIRED shape

````markdown
```
<the outcome, one line>

Done when — each shown by command output in this session:
- `<command>` → <the output that proves it>

Must hold throughout:
- `<command>` → <the output that proves the guard held>

Stop early — the goal is also over when the last message starts with one of these:
- BLOCKED: <decision only a person can make> — when <situation from the stop calls>
- STOPPED: <progress and what is left> — after <bound: N turns or H hours>

Read first: <paths the worker needs, pointers not pasted bodies>
```
````

Block rules:
- **Every line is a check, a guard, a stop, or a pointer.** No method, no order, no "profile first", no library pick the user did not make.
- **Stops live inside the goal.** On Claude Code the judge keeps answering "not yet met" to a worker that stopped politely; "stop and tell me" written beside the goal is a loop until the no-progress guard fires. A stop ends the run only because the goal itself says a `BLOCKED:` or `STOPPED:` line ends it.
- **Under 4,000 characters** — both `/goal` commands cap there. Over it, the target is too broad: go back to step 2, do not compress.

## 7. Adapt per runtime

One block; what changes is how it launches and who judges.

| Runtime | Launch | Judged by | Note to give the user |
|---|---|---|---|
| Claude Code | `/goal <block>` (or `claude -p "/goal …"`) | a separate small model reading the transcript | Run in auto mode for unattended turns; manual mode stops on every tool prompt |
| Codex | `/goal <block>` (`features.goals` enabled) | the working model, via its own completion audit | The same block works: an outside judge's checks also satisfy a self-audit |
| Any other agent CLI | paste the block as the prompt | the agent itself | No turn loop is guaranteed; the `STOPPED:` bound is the only bound |

Write one version unless the user's runtimes need different launch text. Never tell the user the runtimes judge alike — they do not, which is why the block is written for the strictest one.

## 8. Hand it over

Render the block in a code block. Below it, these three parts — REQUIRED:

```
Probes — one line for every command in the block, none skipped:
- `<command>` → <what it printed just now>   |   [unprobed] <why>
Launch — one line per runtime the user named
Split off — every goal step 2 set aside, with its check, or "none"
```

Then stop.

## Rationalizations

| Thought | Reality |
|---|---|
| "They said don't grill me — I'll pick a sensible target" | Six of six unskilled runs asked nothing and invented 400 ms or 500 ms. The bar is theirs; ask that one card |
| "The worker can build its own benchmark" | Then it grades itself. The repo already had `npm run bench`; read first |
| "'Check by loading the page' is clear enough" | Clear to a person. The judge sees only printed output, and the repo has no browser |
| "'If stuck, stop and tell me' covers stopping" | Outside the goal, the judge never reads it as an end. Write the `BLOCKED:` line in |
| "Three small tasks are fine in one goal" | One done line stays red and all three keep running. Split them |
| "Both tools take the same block, so they work the same" | Same block, different judges. Say which one decides |
| "The tree is clean, so the guard prints nothing — no need to run it" | Then write `[unprobed]`. Two skilled runs reported unrun checks as holding; one was a pipeline the shell had refused |

## Red Flags

Stop and re-read the Iron Law if you notice yourself:

- Writing a goal before reading the repo's scripts and tests
- Writing a threshold the user never gave
- A done or guard line with no command ("the nav keeps its text"), or a command with no expected output
- A stop condition written outside the block
- No `STOPPED:` bound
- Reporting a check's result from what it *would* print, or handing over an unrun check without `[unprobed]`
- Editing a file, or "just fixing" the failure the probe found

## Completion criterion

Done when the block has one outcome; every done and guard line is a probed (or `[unprobed]`) command with its expected output; the bound and every stop call sit inside the block as `BLOCKED:` / `STOPPED:` lines; it is under 4,000 characters with no method lines; and the user has the launch line for each runtime they named.
