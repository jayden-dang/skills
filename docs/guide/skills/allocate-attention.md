# `allocate-attention`

**User-invoked** — run it yourself with `/allocate-attention`. Agents never
invoke it; they may only name it.

## What it is

An agent can ship more than you can review. This skill decides *what gets your
eyes* on a finished branch, and — just as importantly — states plainly what
nobody looked at.

It produces **one allocation** over a git range:

- a **sample set** — units admitted by fixed, replayable rules
- a **residue** — every other unit, labelled *agent verdicts only*

## When to reach for it

- "What should I review first?"
- "I can't review all of this."
- "Spot check this PR."
- A branch came out of a long agent run and you have twenty minutes, not two hours.

Not for a Standards+Spec merge verdict — that is [`code-review`](code-review.md).
Not for understanding a change deeply — that is
[`comprehend-change`](comprehend-change.md), which this skill will name for you
on a sampled unit.

## Not a gate

This is the part worth repeating. `allocate-attention` blocks no merge, no PR,
no release, and no decision record. Skipping it is free and costs you nothing
downstream.

The one thing it does insist on: not running it never licenses the claim that a
range was human-sampled. Absence is absence, in both directions.

## How the sample is chosen

Membership is a **fixed mechanical pass** — `git` and `grep` with fixed rules,
never a model's impression of what looks risky. Five signals admit a unit, with
no cap on hits:

| ID | Signal |
|---|---|
| B1 | a file matching the risk-glob set (auth, migrations, payments, CI, …) |
| B2 | a dependency manifest changed |
| B3 | production lines added while the whole range adds no test lines |
| B4 | deletion-heavy rewrite |
| B5 | a spec, architecture, or decision-record surface |

On top of that, the agent may **add** units with a reason — it may never
**remove** one. The reason has to name a real path inside that unit's diff,
which is what stops "this looks risky" from padding the sample.

If nothing binds at all, exactly one unit is still sampled, by a deterministic
score. No run ever ends with nobody having looked at anything.

## Configuring it

Optional. A repo can add an `## Attention signals` section to
`docs/agents/project.md` to set the partition depth and its own risk globs. With
no such section the defaults apply silently — see
`skills/review/allocate-attention/references/signals.md`.

## Output

Conversational by default; **no file is written** unless you ask for one, and a
requested path inside the repo hard-fails rather than quietly landing somewhere
else. Want the allocation again next week? Re-run it over the same range — it is
a function of the range, not of a saved artifact.

## Related

- Philosophy: the sampling loop from "Own the Outer Loop" — attention is the
  scarce resource; answerability stays DREC's job and comprehension stays XDIFF's
- [`code-review`](code-review.md) · [`comprehend-change`](comprehend-change.md) ·
  [`execute-plan`](execute-plan.md)
