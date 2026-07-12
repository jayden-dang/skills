---
name: prototype
description: Use when a design question needs a runnable answer — the user wants to
  prototype, spike, or mock up a state model or piece of logic to feel out
  whether it holds up, or to see what a screen could look like, before
  committing to a real implementation.
---

# Prototype

A prototype is throwaway code whose only job is to answer one design question. The question decides the shape.

## Pick a branch

Identify the question first — from the request, the surrounding code, or by asking:

- **"Does this logic / state model hold up?"** → read `LOGIC.md`.
- **"What should this look like?"** → read `UI.md`.

Read that branch's file end to end before writing a line of prototype code — the constraints that keep the prototype throwaway live there, not here.

Picking the wrong branch wastes the whole prototype. If it's genuinely ambiguous and the user is unreachable, choose by proximity (backend module → logic; page or component → UI) and record the assumption at the top of the prototype.

## Rules for both branches

1. **Throwaway from day one, and marked as such.** Put it near the code it's exploring so context is obvious, but name it so nobody mistakes it for production (`prototype` in the path or filename). Follow the project's existing conventions — never invent new top-level structure for it.
2. **One command to run.** Register it with the project's existing task runner (read commands from `docs/agents/project.md` when present). The user starts it without thinking.
3. **No persistence.** State lives in memory. Persistence is what the prototype is *testing an idea against*, not something it depends on. If the question is explicitly about storage, use a scratch store with an unmistakable "prototype — safe to wipe" name.
4. **Skip the polish.** No tests, no abstractions, no error handling beyond staying runnable. Speed of learning is the whole point.
5. **Surface internal state.** After every action or variant switch, show the full relevant state. Hidden state hides the answer.
6. **Delete or absorb when done.** Once the question is answered, remove the prototype or fold the validated piece into real code — REQUIRED SUB-SKILL: use `tdd` when reimplementing it as production code; the prototype's logic is a reference, not tested code. Never leave it to rot.

## The answer is the only deliverable

Nothing about the prototype's code matters afterward — only what it taught you. Capture the question and its answer somewhere durable: an ADR (if it clears the ADR gate in `domain-modeling`), a requirement in the feature's requirements.md, or the commit message that deletes/absorbs the prototype. If the user isn't around to give the verdict, leave a clearly-marked placeholder for it next to the prototype so it gets filled in before deletion.
