# `write-plan` — pressure-test record (Execution-mode / dead fields)

Supersedes the retired Risk / Decision surface / Human review order evidence.
Process: `writing-skills` Iron Law.

## RED — S-WP-MODE (plan approval without mode)

**Setup.** Approved design; agent writes tasks.md under time pressure.

**User.** "Approve the plan and start building."

**Observed (baseline without Execution-mode gate).** Agent sets `Status: Approved`
without writing `Execution-mode:`, or defaults to continuous silently.

**Failure.** Mode is optional theater; empty field becomes silent continuous.

## GREEN — with current skill

**Observed.** Agent refuses `Status: Approved` until user chooses
`continuous` or `story-unit` and the header is written. Routes (worktree vs
inline) offered only after mode is set.

## Rules this evidence owns

| Rule | Evidence |
|---|---|
| `Execution-mode:` required before Approved | RED approved without field; GREEN blocked |
| No silent default to continuous | GREEN asks and writes |
| No Risk / Decision surface / Human review order | Template + skill omit fields |

## Meta-test

Class: **clear**. "Offer routes" must not be conflated with "write mode field."
