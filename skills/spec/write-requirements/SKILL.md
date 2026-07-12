---
name: write-requirements
description: Use when discovery is complete and a tier-1 or tier-2 change needs its
  requirements written — the user stories and EARS acceptance criteria in
  requirements.md that every later task, test, and commit cites by ID. After
  brainstorm, before any design or code.
---

Produce `docs/specs/<YYYY-MM-DD>-<feature>/requirements.md` from the approved
brainstorm outcome. Requirements are the durable source of intent: they outlive
this conversation, and every task, test, and commit will cite their IDs.

## Two modes — pick by what you were handed

**Tier-1 mini-spec** — a fix plus a guard for an **already-approved** feature
(you came from `amend` or `debug`). You are not authoring a new
`requirements.md`. Append to the owning feature's `requirements.md` (or
`docs/specs/fixes.md` if no feature owns it):

- the **fix requirement** — one EARS criterion (Step 2's forms) for the
  corrected behavior;
- its **`SHALL CONTINUE TO` guard** — Step 3, for the behavior the fix must not
  break.

Then self-review just those two criteria: the ambiguity and testability scans,
plus the code-claim check (Step 5) only when a criterion asserts how the system
*currently* works — a guard usually does. Present the two appended criteria for
approval, keep the feature's `Status`, and exit to `tdd`. **Skip Steps 1 and 4
and the whole-file review** — a new feature code, an Out-of-Scope section, and a
full-file self-review are for a new feature, not a two-line mini-spec.

**New feature** — tier 2, or anything nothing has spec'd yet. Start from
`templates/requirements.md` (in this skill set's repo) and run the full sequence
below. Create a todo per step.

## Step 1: Register the feature code

Pick a short unique prefix (2–12 chars, A–Z0–9, starts with a letter — e.g.
`SHELL`, `SYNC2`). Check `docs/specs/INDEX.md`; add a row there BEFORE writing
requirements. Never reuse a retired code.
**Done when:** the code has a row in INDEX.md with status Draft.

## Step 2: Write stories and EARS criteria

One `## N. <title>` section per user story, each with acceptance criteria as
EARS statements carrying hierarchical IDs `**CODE-N.M**`:

- `WHEN <event> THE SYSTEM SHALL <behavior>` — event-driven
- `WHILE <state> THE SYSTEM SHALL <behavior>` — state-driven
- `IF <unwanted condition> THEN THE SYSTEM SHALL <behavior>` — error handling
- `WHERE <feature enabled> THE SYSTEM SHALL <behavior>` — optional features
- `THE SYSTEM SHALL <behavior>` — always-true invariants

One observable behavior per criterion. If a sentence needs "and", it is
usually two criteria.
**Done when:** every story has ≥1 criterion and every criterion has exactly
one WHEN/WHILE/IF/WHERE/ubiquitous form.

## Step 3: Guard existing behavior

For every existing behavior this feature touches, add a guard:
`**CODE-N.M** (guard) WHEN <condition> THE SYSTEM SHALL CONTINUE TO <existing
behavior>`. Guards are what stop an agent from breaking load-bearing behavior
nobody mentioned. For a tier-1 bugfix this step plus one fix requirement IS the
spec (append to the owning feature's requirements.md, or `docs/specs/fixes.md`
if no feature owns it).
**Done when:** you have actively searched the touched surface for behaviors to
guard — not merely found none by default.

## Step 4: Out of Scope

List what this feature deliberately does NOT do. This section is the defense
against scope creep during implementation and review.

## Step 5: Self-review, then the approval gate

Self-review before showing the user:
- **Ambiguity scan:** could any criterion be read two different ways? Pick one
  reading and write it in.
- **Testability scan:** can each criterion be verified by an automated test or
  a concrete manual check? Rewrite any that can't.
- **Placeholder scan:** no "TBD", "etc.", "handle errors appropriately".
- **Code-claim check (independent):** if any criterion asserts how the system
  currently works — a data format, an existing behavior, a constraint —
  dispatch a review subagent to verify each such claim against the real code
  (grep/read the files, cite `file:line`, flag any that don't hold), writing
  findings to `.skills/<slug>-req-review.md`. A false premise here — "the body is
  ProseMirror-JSON" when it is Markdown — poisons design, plan, and code.
  Correct the criterion before the gate; do not read the code yourself. (No
  subagents? Do the check yourself against the code.)

Then present the FILE to the user for review and STOP. Do not proceed to
design on the strength of conversational agreement — the written requirements
are what get approved. On approval, set `Status: Approved`.
**Done when:** the user has approved the written file.

## ID immutability

Once Status is Approved, IDs never change meaning and are never renumbered.
Retire a requirement by striking it through (`~~**CODE-1.2**~~ superseded by
CODE-1.4`). the `trace` check treats struck-through IDs as undefined, so citing
tests/tasks surface immediately.

## Exit

REQUIRED SUB-SKILL: use `write-design` (tier 2) or hand tier-1 fixes straight
to `tdd` with the new IDs.
