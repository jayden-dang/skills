# `grilling`

> The interview primitive. One question per message, each shipping a recommended answer, until you and the user hold the same picture of the plan.

|  |  |
|---|---|
| **Bucket** | discovery |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | the codebase and docs — to look up every fact before asking about it |
| **Writes** | nothing; it enacts no code, files, or plan execution |
| **Calls** | — (a pure interview primitive) |
| **Called by** | [`brainstorm`](brainstorm.md) (its required interview step); any skill whose work calls for an interview |

## When it fires

Whenever intent is underspecified and the decisions must be drawn out of the user: to stress-test a plan, design, or feature idea before anything is built, when the user asks to be grilled or interviewed, or when another skill calls for an interview.

[`brainstorm`](brainstorm.md) invokes it as a required sub-skill for its whole interview step, and other design skills reach for it the same way. It is a primitive — it does one thing, holds no state of its own, and hands the picture it draws to whatever skill called it.

## The six rules

The skill is short and every line is load-bearing.

- **One question per message.** Ask, then wait for the answer before the next question. A wall of questions is bewildering; a single question gets a real answer.
- **Every question ships with your recommended answer** and a one-line reason. The user can accept in two words or push back.
- **Walk every branch of the decision tree.** Decisions depend on each other — an early answer opens some branches and closes others. Resolve them in dependency order and keep going until no unexplored branch remains.
- **Right-size to the project's posture.** When the parent supplies it or `docs/agents/project.md` carries a **Project posture** section, prune branches that do not apply: skip data migration, backward compatibility, and deprecation on a Prototype / Research / Learning project; press on them for a Released / Scaling / Maintenance one. Absent a posture, walk every branch.
- **Facts are yours; decisions are the user's.** If the answer already exists in the codebase or the docs, look it up — never ask the user to recall what you can read. Anything that is a judgment call goes to the user, one at a time, and you wait.
- **Do not enact anything** — no code, no files, no plan execution — until the user explicitly confirms you have reached a shared understanding.

## One question per message

The first rule is the one most easily broken under time pressure, and the one that most changes how the interview feels.

A batch of ten questions reads as an interrogation. The user skims, answers the easy three, and the hard ones — the ones the plan actually turns on — get a shrug or silence.

A single question with a recommendation attached is a different act: it is a proposal the user confirms or corrects. Most answers become two words, and the few corrections are exactly the signal you were after.

## The fact/decision split

The rule that does the most work is the fourth: **facts are yours, decisions are the user's.**

A fact is anything with a knowable answer — which auth library the repo already uses, whether a table has an index, what the current timeout is. Those you look up; asking the user to recall them wastes their attention and invites a wrong answer that then poisons the plan.

A decision is a judgment call — whether to paginate, which trade-off to accept, what "done" means for this feature. Those go to the user, one at a time, and you wait for each before moving on.

The split is not about politeness; it is about routing each question to whoever can answer it correctly. A fact asked of the user invites a guess; a decision made for the user takes away a call that was theirs.

## Walking the tree in order

Decisions are not a flat list. An early answer opens some branches and closes others, so the order matters: resolve dependencies first, then the branches they unlock.

When an answer opens a new sub-branch, walk that before returning to the trunk. The interview is done only when no unexplored branch remains — not when the obvious questions run out, and not when the user seems to have had enough.

## Worked example

The user wants to add rate limiting to an API. Rather than dumping a questionnaire, `grilling` walks the tree in dependency order, one message at a time. Facts are resolved silently by reading the code; only decisions are surfaced.

> **You:** Rate limiting needs a shared store across instances. I checked — you're already running Redis for sessions (`src/cache/redis.ts`), so I'd reuse it rather than add a dependency. Reuse the existing Redis? *(Recommended: yes — no new infra, and the connection pool is already tuned.)*
>
> **User:** yes
>
> **You:** Next branch: what's the limit scoped to — per API key, per IP, or per user? *(Recommended: per API key — your public endpoints authenticate by key, so it's the unit a client actually controls.)*
>
> **User:** per key, but unauthenticated routes should fall back to IP
>
> **You:** Good — that opens a sub-branch. For the `/health` and `/status` routes that are intentionally unauthenticated, exempt them entirely or IP-limit them too? *(Recommended: exempt — they're polled by your own uptime monitor and limiting them would page you at 3am.)*
>
> **User:** exempt them
>
> **You:** Last branch on this path: when a client is over the limit, `429` with a `Retry-After` header, or silently drop? *(Recommended: `429` with `Retry-After` — it's the standard clients already handle, and silent drops look like outages.)*

Note the shape of every message. It looks up the fact (Redis is present, endpoints authenticate by key), states exactly one decision, ships a recommendation with a one-line reason, and stops. The IP-fallback answer opened a new sub-branch that got walked before anything else. Nothing is built, and no file is touched, until the user confirms the picture is complete.

## Why it is written the way it is

The skill exists against two baseline failures.

The first is the **question dump** — an agent that fires ten questions at once, which reads as an interrogation and gets shallow or skipped answers. One-per-message with a recommendation turns each into a two-word confirmation or a real correction, and the reason line means the user can push back on the merits rather than guess at intent.

The second is the **agent that guesses** — either guessing a fact it could have read, or guessing a decision that was the user's to make. The fact/decision split assigns each question to whoever can answer it correctly, so neither kind of guess is needed.

The no-enactment rule keeps `grilling` a pure interview: it draws the picture, and another skill builds from it. That boundary is what lets it be reused everywhere an interview is needed without ever surprising the user with a side effect they did not confirm.

The confirmation step at the end is not a formality either. "Do you have any other questions" is not the same as "have we reached a shared understanding" — the skill waits for the explicit yes before anything downstream begins, because a picture that only one of you holds is not shared.

## See also

- [`brainstorm`](brainstorm.md) — the primary caller; grilling is its interview step
- [`research`](research.md) — where a factual question too big to just look up gets sent
- [`domain-modeling`](domain-modeling.md) — runs alongside grilling to settle terms mid-interview
- [The skill model](../concepts/skill-model.md) — how primitives like this compose
