---
name: handoff
description: Use when the current conversation must continue elsewhere — context is
  filling up or nearing compaction, the user is ending a session with work
  unfinished, or another agent must pick the work up — to produce a
  self-contained handoff document a fresh agent can resume from.
disable-model-invocation: true
---

# Hand Off

Compact this conversation into a document a fresh agent can resume from. Write it to the **OS temp directory** (`$TMPDIR`, falling back to `/tmp`; `%TEMP%` on Windows), never into the workspace — a handoff is session ephemera, not a project artifact. Name it `handoff-<topic>-<timestamp>.md` and tell the user the absolute path.

If the user passed an argument to this skill, treat it as what the next session will focus on and orient the whole document around that focus — trim anything the focus makes irrelevant.

## Contents

- **Goal** — what the work is ultimately for, in the user's terms.
- **Current state** — what is done, what is in flight, exact branch/worktree, whether the working tree is dirty.
- **Tried and rejected** — every approach that was attempted or considered and dropped, each with *why*. This section saves the successor from re-walking dead ends; it is usually the most valuable one.
- **Next actions** — concrete, ordered, starting with the very next command or edit.
- **Suggested skills** — which skills of this set the successor should invoke, and at which step (e.g. "resume `execute-plan` at task 4", "run `verify` before claiming task 3 done").
- **Team context (when present)** — if `docs/agents/project.md` has `## Team` with a non-empty **roster** or band override, one line: band + how packaging applies; Small/Multi: who owns next actions when the roster/ownership notes make that clear. Missing Team → omit (do not invent a team).

## Rules

- **Reference, never duplicate.** Specs, plans, ADRs, issues, commits, diffs — cite them by path, URL, or hash. Copying their content bloats the handoff and forks the truth; the artifact on disk is authoritative.
- **Redact secrets.** API keys, tokens, passwords, personal data — replace with a placeholder naming where the real value lives. The doc may become another agent's prompt.
- **Decisions the user already made are recorded as settled**, with their rationale — the successor must not re-open them or re-ask.

## Optional: launch the successor

Only if the user asks: start a background agent seeded with the handoff document as its prompt, with a descriptive display name, running in the current working directory. Confirm the mechanism your harness provides before promising it; otherwise just hand the user the file path.

## Completion criterion

Read the finished document as a skeptic: could a fresh agent, given only this file plus the artifacts it references, resume the work without asking the user anything already answered in this conversation? If any question survives that test, the answer belongs in the doc — add it before finishing.
