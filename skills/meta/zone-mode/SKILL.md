---
name: zone-mode
version: 1.1.0
description: Load the 1% skill-check gate and hand off to the right entry point.
disable-model-invocation: true
---

<SUBAGENT-EXEMPT>
If you were dispatched as a subagent to execute one specific task, ignore this
skill and follow your brief.
</SUBAGENT-EXEMPT>

<NON-NEGOTIABLE>
If there is even a 1% chance a skill applies to what you are about to do, you
MUST invoke that skill first. This is not a judgment call you get to make
per-task. You cannot reason your way out of it.
</NON-NEGOTIABLE>

## The Rule

**Invoke relevant or requested skills BEFORE any response or action** — before
clarifying questions, before exploring the codebase, before checking a single
file. If the skill turns out not to fit, you may set it aside after reading it.

Announce "Using [skill] to [purpose]", then follow the skill exactly. If it has
a checklist, create one todo per item.

**Priority:** process skills first, then implementation skills. When the
entry point is unclear, load `docs/guide/process/on-ramps.md` — that table
is the one home; do not invent a second router.

**Participant boundary:** never infer skill-set membership from roster,
CODEOWNERS, or PR authorship; only skill-mediated actions are enforced or
recorded. Treat supplied evidence as supplied — do not invent mediation that did
not happen.

## Handing off

Once the entry point is named, how you reach it depends on the target:

- **Model-invocable** (no `disable-model-invocation` in its frontmatter) — invoke
  it and let it take over.
- **User-invoked** (`disable-model-invocation: true`) — you cannot invoke it.
  Name it for the user to run: "run `/triage`". Telling the agent to invoke one
  is a dead-end hand-off, a real bug rather than a style nit, and
  `scripts/lint-write-handoffs.py` fails it.

Do not start executing a chosen flow from inside this skill. Route, then hand
over.

**Context hygiene:** keep discovery through plan in one unbroken context window.
If the window is filling before the plan is done, tell the user to run
`/write-handoff`. Execution sessions are context-isolated per task by design.

## Red Flags — you are rationalizing

| Thought | Reality |
|---|---|
| "This is just a quick question" | Questions are tasks. Check for skills. |
| "Let me look around first" | Skills define HOW to look. Check first. |
| "This is too small for process" | Small things grow. The tier system handles size — the skill decides, not you. |
| "I remember what that skill says" | Skills change. Read the current text. |
| "I'll do this one step, then check" | The check comes before the first step. |
| "Being helpful means answering fast" | Being helpful means following the process that works. |

## Precedence

The user's explicit instructions (including CLAUDE.md) override skills; skills
override your defaults. Skip a skill's workflow only when the user has
explicitly told you to.
