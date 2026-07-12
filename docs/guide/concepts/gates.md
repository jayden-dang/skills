# The gates

Four hard prohibitions. They are not guidance, they are not preferences, and they are not judgment calls the agent gets to make per-task.

| Gate | Skill | Law |
|---|---|---|
| No code before an approved spec | [`brainstorm`](../skills/brainstorm.md) | `<HARD-GATE>` — write no code, scaffold nothing, until the tier is stated out loud |
| No production code before a failing test | [`tdd`](../skills/tdd.md) | `NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST` |
| No fix before a root cause | [`debug`](../skills/debug.md) | `NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST` |
| No completion claim without fresh evidence | [`verify`](../skills/verify.md) | `NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE` |

A fifth sits above them all: [`using-skills`](../skills/using-skills.md), the session gate, which says that if there is even a **1% chance** a skill applies to what you are about to do, you must invoke it first — before clarifying questions, before exploring the codebase, before checking a single file.

## Why they are written as prohibitions

Most process documentation is written as advice: *prefer*, *consider*, *it is usually best to*. That form fails here, and the reason is empirical rather than stylistic.

[`writing-skills`](../skills/writing-skills.md) classifies baseline failures before a word of a skill is written, because **the form that fixes one failure type measurably backfires on another**:

| Baseline failure | Write this | Not this |
|---|---|---|
| Knows the rule, breaks it under pressure | Hard prohibition + rationalization table + red-flags list | Soft "prefer / consider" guidance |
| Complies, but the output has the wrong shape | A positive recipe: what the output **is**, its parts, in order | Prohibitions — under a competing incentive agents negotiate with "don't X"; in head-to-head tests the prohibition arm produced *more* of the unwanted content than no guidance at all |
| Omits an element from something it already produces | A REQUIRED slot in the template it fills | Prose reminders near the template |
| Behavior should depend on a condition | A conditional keyed to an observable predicate | An unconditional rule plus exemption clauses |
| A check that must never be skipped or misjudged | A deterministic check the agent runs — fixed `grep`/`git` passes with fixed rules | Prose steps describing the check |

The four gates all sit in row one. They guard rules the agent *knows* and breaks anyway, under the pressure of wanting to be helpful and fast. So they get the row-one treatment: a prohibition, plus an explicit counter to every rationalization observed in a real baseline run.

There is a matching rule the skill is blunt about: **no nuance clauses.** "Don't X unless it matters" reopens the negotiation the rule just closed. Appending one nuance clause to a winning recipe degrades it from consistent to noisy. A real exception becomes its own conditional keyed to something observable.

## Gate 1 — no code before an approved spec

`brainstorm` opens with a `<HARD-GATE>` block. The only artifacts it may touch are notes, the glossary, ADRs, and — through its sub-skills — research notes and explicitly-marked throwaway prototypes.

Its terminal state is the enforcement: for tier ≥ 1 the **only** permitted exit is `write-requirements`, which carries its own approval gate on the written file. For tier 0 the only permitted exit is `tdd`, and only after the tier has been spoken.

The rationalizations it counters by name:

| Thought | Reality |
|---|---|
| "This is a one-liner, designing it is overhead" | Deciding it is tier 0 **is** the design step |
| "The user already told me exactly what to build" | They told you a solution. You have not confirmed the problem, the constraints, or what must keep working |
| "I'll sketch a little code to clarify my thinking" | That is a prototype. Run the `prototype` sub-skill so it is throwaway by contract, not accidental production code |
| "Scaffolding isn't really implementation" | A repo skeleton is a stack decision enacted without approval. It is implementation |
| "We talked enough, I basically know the answer" | If it is not in an approved `requirements.md`, it lives only in this chat and dies with it |

## Gate 2 — no production code without a failing test

The `tdd` Iron Law, and the part people flinch at:

> Wrote implementation before the test? **Delete it.** Not "keep it as reference", not "adapt it while the tests catch up" — you will end up testing what you built instead of what was required. Delete means delete; implement again from the test.

Both halves of RED are mandatory and separately verified. Write the failing test, then **run it** and confirm it fails *for the expected reason* — not because of a typo or an import error. A test that passes on its first run is testing behavior that already exists: fix the test, not the code.

Exceptions exist only with the user's explicit permission, and the skill enumerates them: throwaway prototypes, generated code, pure configuration. "Skip it just this once" is named as the rationalization the skill exists to block.

## Gate 3 — no fix without a root cause

`debug`'s Phase 1 is the gate, and it is unusual: before any theory-building, you must construct and **run** a *red-capable signal* — one command that is red right now because of this exact bug, and will go green when it is fixed.

> Build the right feedback loop and the bug is 90% fixed; every later phase merely consumes it.

The check on the check: *name the command, paste one run of its red output*. Catch yourself reading code to form a theory before that command exists, and you stop.

The gate has a second half, further down. **Three failed fix attempts means stop.** At that point the architecture is in question, not your latest hypothesis — especially if each fix revealed new coupling somewhere else. Discuss with the user before attempt four.

## Gate 4 — no completion claim without fresh evidence

`verify` fires before anything that *implies* success — "done", "fixed", "passing", "works", or any paraphrase — and before committing, opening a PR, closing a task, or reporting a subagent's result.

> If the proving command did not run just now, in this session, the claim is unavailable to you. An unverified claim isn't optimism — it's a false statement.

The Gate Function is four steps, and skipping any one of them is named as lying rather than verifying:

1. **IDENTIFY** the command that proves this exact claim.
2. **RUN** it fresh and complete. No cached results, no partial scopes, no "it passed earlier".
3. **READ** the full output — exit code, failure count, warnings. Not the last line.
4. **CONFIRM** the output actually supports the claim.

Its claim-to-evidence table is the most quoted thing in the set:

| Claim | Requires | Never sufficient |
|---|---|---|
| "Tests pass" | Full fresh run, zero failures, output read | An earlier run; a subset; "should pass" |
| "The feature works" | The affected flow driven through the running system and observed | Green unit tests alone |
| "The bug is fixed" | Original symptom re-tested and gone | The code changed |
| "The agent completed X" | You inspected the diff yourself | The agent's own success report |
| "Requirements met" | the trace check passes, **and** each acceptance criterion checked off individually against observed behavior | Green tests alone |

And the regression-proof pattern, which is the only thing that makes a regression test worth its name:

```
write test → passes → revert the fix → test MUST fail → restore fix → passes
```

A test that survives the revert is testing nothing.

## The gate above the gates

`using-skills` is injected into every session by a `SessionStart` hook (matcher `startup|clear|compact`) so the rule survives `/clear` and context compaction. Its `<NON-NEGOTIABLE>` block:

> If there is even a 1% chance a skill applies to what you are about to do, you MUST invoke that skill first. This is not a judgment call you get to make per-task. You cannot reason your way out of it.

Its red-flags table catches the agent mid-rationalization:

| Thought | Reality |
|---|---|
| "This is just a quick question" | Questions are tasks. Check for skills |
| "Let me look around first" | Skills define HOW to look. Check first |
| "This is too small for process" | Small things grow. The tier system handles size — the skill decides, not you |
| "I remember what that skill says" | Skills change. Read the current text |
| "I'll do this one step, then check" | The check comes before the first step |
| "Being helpful means answering fast" | Being helpful means following the process that works |

## Precedence

The gates are not the top of the hierarchy.

> The user's explicit instructions (including CLAUDE.md) override skills; skills override your defaults.

A skill's workflow is skipped only when the user has explicitly said to skip it. The gates constrain the agent, not the human.

## See also

- [Philosophy](../methodology/philosophy.md) — "gates, not vibes", and the five other principles
- [Ceremony tiers](../methodology/ceremony-tiers.md) — what scales down, and what never does
- [`writing-skills`](../skills/writing-skills.md) — why prohibitions work here and backfire elsewhere
- [`verify`](../skills/verify.md) — the gate every other gate eventually calls
