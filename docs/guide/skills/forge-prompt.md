# `/forge-prompt`

> Vague ask → one paste-ready **prompt block** for a fresh session, via a question-by-question interview in the language you pick. It names no next step, on purpose.

|  |  |
|---|---|
| **Bucket** | discovery |
| **Invocation** | user-invoked (`/forge-prompt`) — agents must never auto-invoke it |
| **Reads** | the repository when the ask is about it (never asks what it can read); otherwise only what the user supplies |
| **Writes** | the prompt block in chat; optionally the block plus the Q&A trail to `.skills/prompts/<slug>.md` |
| **Calls** | `clarify-decisions` for the interview channel |
| **Called by** | nobody — it sits outside every chain by design |

## Why it exists

Underspecification does not make a coding agent stop and ask; it makes it **guess**. Measured
across OpenCode, Claude Code, and Codex, 55.8–67.8% of acted runs violated at least one action
boundary, and target ambiguity dominated: safe success collapses from 67.9% to 8.6% as the
instruction stops naming exactly one object. Agents act at the same rate on shared production
surfaces as on contained ones, so a blast radius nobody wrote down is a blast radius nobody sees.

## Why it hands over no next step

This is the design decision, not an omission.

Models anchor on their own earlier output, and prompt-level instructions not to are largely
ineffective — anchoring is a robust behavioral feature. Transferring an upstream agent's reasoning
and chosen direction to a downstream one helps up to a threshold, then causes premature
convergence on the upstream's assumptions (*the crossover effect*); the rule is **selective
context, not comprehensive history**. And cross-context review beats same-session review precisely
when the reviewing context receives **only the artifact** — not the prompt, the rationale, or the
trace.

So what travels is what is *true*: targets, boundaries, evidence, assumptions, open questions,
done signal. No lane, no skill name, no step list, not even a classification of the request as a
bug or a feature. **The session you paste into decides what the work is and how to open it** — and
because it never saw the interview, it decides on its own reading of the territory.

## How a run goes

1. **Setup, in English** — pick the interview language (English is a first-class choice, no
   default), and say where the territory is: this repo, another codebase, or outside code.
2. **The interview** — one card per message in ordinary chat, ordered by where the measured loss
   is: error information → target identity → boundary and environment → done signal. Never a
   picker that truncates the consequence line; never a question the repo answers.
3. **Stop on the open set**, not on a count. Two "I don't know"s in a row means the frontier is
   behind you — what remains becomes `Open`.
4. **The block**, then one or two lines in the interview language on what pasting it commits them
   to. Then stop.

It never recommends and never decides. A fork the user cannot close becomes an `Open` line.

## What the block looks like

```
<the ask, one line, in the user's own words>

What this touches
- <exact path / object / ID>              [confirmed | unconfirmed]

Off limits
- <what must not be touched>
Must keep working
- <what must not regress>

What is already known
- <fact> — <where it came from, and when>

Not yet checked
- <assumption, including any solution the ask took for granted>

Open — ask me, do not assume
- <question the interview could not close>

Done when
- <the observable that settles it>
```

`[unconfirmed]` is information, not a defect — it tells the receiver exactly where not to guess.

## Using it beside a companion window

It runs in parallel with [`/interpret-session`](interpret-session.md). Hand that window the
finished block and **nothing else** — no interview trail, no reasoning — so it reads the artifact
cold. That is the cross-context review configuration the literature backs.

## When something else fits better

| Situation | Go to |
|---|---|
| You know what you want; you just don't know which entry point applies | [`/ask-me-bro`](ask-me-bro.md) |
| The open item is a design fork, not a missing target | [`clarify-decisions`](clarify-decisions.md) |
| Multi-session destination still foggy | [`/pathfind`](pathfind.md) |
| The ask already names targets, boundaries, and a done signal | just start the work |

## See also

- Skill body: [`skills/discovery/forge-prompt/SKILL.md`](../../../skills/discovery/forge-prompt/SKILL.md)
- Evidence and design record: [`skills/discovery/forge-prompt/TESTS.md`](../../../skills/discovery/forge-prompt/TESTS.md)
- [`clarify-decisions`](clarify-decisions.md) · [`/interpret-session`](interpret-session.md) · [`/ask-me-bro`](ask-me-bro.md)
