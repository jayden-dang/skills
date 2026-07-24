---
name: using-skills
description: Use when starting any conversation — establishes the rule that relevant skills are found and invoked before any response or action, including clarifying questions
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

**Priority:** process skills first, then implementation skills. "Build X" →
`brainstorm` before anything. "This is broken" → `debug` before any fix. Small
in-scope change to an already-shipped, spec'd feature (a tweak, recolor, or
follow-on) → `amend`, not `brainstorm`. For an incoming issue or external PR,
suggest the user run `/triage`; to capture the current conversation, spec, or
idea into tracker issues, suggest `/file-issues` (both are user-invoked — you
cannot auto-invoke them).
Unsure which flow fits → suggest `/ask`. Only auto-invoke model-invocable skills;
name a user-invoked one for the user to run.

**Before plan mode:** if the work is creative (new behavior, new feature), run
`brainstorm` first — plans come after approved requirements.

**Participant boundary:** never infer skill-set membership from roster,
CODEOWNERS, or PR authorship; only skill-mediated actions are enforced or
recorded. Treat supplied evidence as supplied — do not invent mediation that did
not happen.

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
