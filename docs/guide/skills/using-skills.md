# `using-skills`

> The skill-check gate. Relevant skills are found and invoked before any response, any action, even any clarifying question.

|  |  |
|---|---|
| **Bucket** | meta |
| **Invocation** | model-invocable, but injected into every session by the `session-start.sh` SessionStart hook — so in practice it is always present, surviving `/clear` and context compaction |
| **Reads** | the incoming task, and CLAUDE.md (which outranks it in the precedence order) |
| **Writes** | nothing — it produces the *act* of invoking the right skill, not an artifact |
| **Calls** | [`brainstorm`](brainstorm.md), [`debug`](debug.md), [`amend`](amend.md) (auto-invoked when they fit); names [`ask`](ask.md), [`triage`](triage.md) for the user to run |
| **Called by** | nothing — it is session-injected, not reached through a hand-off |

## When it fires

At the start of every conversation, and again on every turn, because the SessionStart hook re-injects its full text after `/clear` and after compaction. The hook wraps the skill body in an `<IMPORTANT>` block and hands it to the model as additional context, so the skill-check rule is present before the agent has read a single file.

The one carve-out is stated in the skill itself: a `<SUBAGENT-EXEMPT>` block tells any agent dispatched as a subagent to execute one specific task to ignore the skill and follow its brief instead. That is what keeps a task-scoped subagent from re-entering the whole discovery flow on work its parent already framed.

## The Rule

> Invoke relevant or requested skills BEFORE any response or action — before clarifying questions, before exploring the codebase, before checking a single file.

The `<NON-NEGOTIABLE>` framing is deliberate: if there is even a one-percent chance a skill applies, the agent must invoke it first. The skill states plainly that this is not a per-task judgment call the agent gets to make, and that it cannot reason its way out of it. If a skill turns out not to fit once read, the agent may set it aside — but only after reading it.

The invocation ritual is fixed: announce "Using [skill] to [purpose]", then follow the skill exactly, and if the skill carries a checklist, create one todo per item.

## Priority

The skill orders the search: process skills first, then implementation skills. It carries a short routing table for the common openings:

- "Build X" routes to [`brainstorm`](brainstorm.md) before anything else.
- "This is broken" routes to [`debug`](debug.md) before any fix.
- A small in-scope change to an already-shipped, spec'd feature — a tweak, recolor, or follow-on — routes to [`amend`](amend.md), not `brainstorm`.
- An incoming issue or external PR routes to [`triage`](triage.md), which the agent names for the user because it is user-invoked and cannot be auto-invoked.
- When the fit is unclear, the agent suggests [`ask`](ask.md).

The dividing line runs through model-invocability: the agent auto-invokes only model-invocable skills, and names a user-invoked one for the user to run. There is also a plan-mode clause — if the work is creative (new behavior, a new feature), run `brainstorm` first, because plans come only after approved requirements.

## Red flags — you are rationalizing

The skill carries a six-row table pairing the tempting thought with the reality that answers it:

| Thought | Reality |
|---|---|
| "This is just a quick question" | Questions are tasks. Check for skills. |
| "Let me look around first" | Skills define HOW to look. Check first. |
| "This is too small for process" | Small things grow. The tier system handles size — the skill decides, not you. |
| "I remember what that skill says" | Skills change. Read the current text. |
| "I'll do this one step, then check" | The check comes before the first step. |
| "Being helpful means answering fast" | Being helpful means following the process that works. |

## Precedence

The skill closes by ranking the three sources of instruction: the user's explicit instructions, including CLAUDE.md, override skills; skills override the agent's own defaults. A skill's workflow may be skipped only when the user has explicitly told the agent to skip it.

## Worked example

A session opens with: "Quick one — can you bump the retry limit in the payment client from 3 to 5?"

The tempting move is to open the file and make the edit. The skill blocks it: the change is a small in-scope tweak to already-shipped behavior, so the agent's first act is not the edit but the announcement —

> Using amend to route this in-scope change.

`amend` reads the owning spec, decides the tier, and sends the work down the light lane. Had the agent instead treated "quick one" as a licence to skip the check, it would have hit the first two rows of the red-flags table at once: a question is still a task, and looking around first is exactly what the skill defers until after a skill is chosen.

## Why it is written the way it is

`using-skills` is the session-injected entry gate, and per [`writing-skills`](writing-skills.md) that dictates two things. First, its baseline failure is an agent that knows skills exist and skips the check under the pressure of seeming helpful and fast — a pressure-gate failure, which is why the page carries a `<NON-NEGOTIABLE>` absolute plus a rationalization table rather than soft "prefer" guidance. Second, because it is paid on every turn of every session, its token budget is unforgiving: the body stays minimal, and every line has to survive the no-op test. The whole skill is a single rule with just enough scaffolding — priority order, red flags, precedence — to make that one rule hold under pressure without bloating the per-turn cost.

## See also

- [The skill model](../concepts/skill-model.md) — how skills are discovered, loaded, and invoked
- [`ask`](ask.md) — the router the agent names when the right flow is unclear
- [`writing-skills`](writing-skills.md) — the authoring doctrine behind this gate's shape
- [Methodology overview](../methodology/overview.md) — the idea-to-ship chain this gate opens
