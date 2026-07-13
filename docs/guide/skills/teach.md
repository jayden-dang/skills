# `teach`

> Teaches you something and makes it stick, by refusing to end a lesson until you have produced something and reality has graded it.

|  |  |
|---|---|
| **Bucket** | meta |
| **Invocation** | user-invoked — you type `/teach`; the agent never reaches for it |
| **Reads** | the codebase, the learner's own prior work, trusted sources |
| **Writes** | a teaching workspace under `.skills/teach/<topic>/` (git-ignored) |
| **Calls** | [`research`](research.md), when a topic needs a trusted source before it can be taught |
| **Called by** | — (nothing; it owns its own session) |

## When to reach for it

Type `/teach` when you want to *learn* something and have it survive the week — a subsystem of your codebase, a library, a language, a design tradeoff, a soft skill. It runs across sessions and accumulates.

Do not reach for it for a one-off explanation. If you just need something clarified, ask — the agent will explain, which is what you actually want. `teach` exists for when explanation has already failed you: when you have read the file three times, nodded along, and lost it again by morning.

## The Iron Law

```
NO LESSON ENDS WITHOUT A GRADED PRODUCTION
```

A **production** is something *you* made: a prediction, an answer in your own words, a line of code, a diff. The agent's explanation is not a production. Your "got it" is not a production.

**Graded** means checked against reality — the command ran, the source said otherwise — not against the agent's approval.

## Why it is written the way it is

The skill exists against one baseline failure, and it is remarkably robust: **explanation is terminal.**

Given "teach me this file," an agent with no skill writes an outstanding explainer — a mental model, a phase-by-phase walkthrough, every trap pre-solved, a memorable closing line. It asks nothing. It waits for nothing. Across ten baseline runs on a real file in this repo, not one agent asked the learner a single question, and not one produced any evidence the learner had understood anything.

The second failure follows from the first. Asked point-blank to certify that you have learned something, an agent will honestly refuse — *"that's a record of me explaining, not a record of you understanding"* — and then hand you a notes file and leave. It knows it has no evidence. It says so, eloquently. It still does not go and get any.

So the gate is not "don't claim they learned it." Agents already won't. The gate is **run a loop that produces evidence**, because the default is to substitute a beautiful explanation for your production and then apologise for the resulting ignorance.

## The oracle

The idea that makes this skill different from every other teaching skill: **grade against something that can contradict you.**

In a codebase you have the strongest oracle there is. Commit to a prediction — *what line number will this print?* — and then run the thing. The output grades you, and the agent's opinion never enters. A wrong prediction is worth more than a right explanation, because the surprise is what makes it stick.

When nothing runs, you **manufacture** the oracle: decompose the question until you reach something checkable, then build the thing that grades you. "Is event sourcing right for billing?" settles nothing. "Write the CRUD schema you'd reach for, then answer these three real billing questions with SQL against it" settles something — the schema either answers them or it does not.

Two disciplines come with that. The agent must **name what the oracle does not cover** — SQL can prove a schema fails a query; it cannot price the operational cost on the other side of the tradeoff. And it must **never reshape your mission to fit its oracle**, which is the seductive failure: steering you toward the half it can measure protects its grade and abandons your goal.

## When you ask for the answer

You will — tired, rushed, stuck. And you are often right that a question would be worse than an answer in that moment.

So the skill lets the agent answer. What it forbids is *ending there*. The answer comes in the fewest true words and is immediately converted into a production; the shortest one costs ninety seconds. **Time pressure shrinks the production. It never skips it.**

This is a deliberate departure from the strict-Socratic teaching skills, which forbid the direct answer outright. Under pressure testing, agents demolished that rule on the merits — *"holding the question hostage prioritises my method over his situation; that's not rigor, it's theater"* — and they were right. A rule the agent can out-argue is not a gate.

## The workspace

`/teach` owns `.skills/teach/<topic>/`, which is git-ignored and accumulates across sessions:

- **`MISSION.md`** — why you want this. Concrete: "extend the linter tomorrow" beats "understand the linter". Everything traces back to it.
- **`LEARNING.md`** — one entry per graded production, in a fixed shape: the production, the oracle, the observed result, what it is evidence *for*, and the next probe. Never an entry for material merely covered.
- **`evidence/`** — the fixture, the pulled corpus, the seeded rows: whatever the lesson was graded against when the oracle is not a command you can re-run for free.
- **`GLOSSARY.md`** — a term is added only once you can use it correctly.
- **`NOTES.md`** — how you want to be taught.

`LEARNING.md` is what the agent reads to pick the next lesson, which is why an entry it did not earn misaims every session after it. "Covered" is not "demonstrated," and only the second one goes in the file.

## See also

- [`research`](research.md) — where a topic goes when it needs a trusted source before it can be taught
- [`grilling`](grilling.md) — the interview primitive; shares the one-question-then-stop discipline, but elicits *your* intent rather than building *your* knowledge
- [`writing-skills`](writing-skills.md) — the doctrine this skill was built under: no text ships without an observed baseline failure
- [The skill model](../concepts/skill-model.md) — why `teach` is user-invoked
