# `speak-outer`

> Anything a person reads is the outer register. The switch is total.

|  |  |
|---|---|
| **Bucket** | review |
| **Invocation** | model-invocable |
| **Reads** | the work (goal, next, domain facts) |
| **Writes** | the person-facing text — a reply, status, standup note, or PR prose |
| **Calls** | none |
| **Called by** | description trigger when a human will read the next file; [`land-branch`](land-branch.md) Author PR text |

## When it fires

When writing a status, a reply, a standup note, a PR body, or any other
text a person will read. It does **not** fire on landing a branch
([`land-branch`](land-branch.md)), on a completion claim
([`prove-claim`](prove-claim.md)), or on a handoff
([`write-handoff`](write-handoff.md)).

## The Iron Law

```
NOTHING A PERSON READS CARRIES PROCESS MACHINERY
```

Skill names, `REQUIRED SUB-SKILL`, `Pass:` / `Tier 2` / `Satisfies:`, and
"closed the loop" stay in the inner notes. The outer names the work.

## Why it is written the way it is

A softer prompt ("put status in STATUS.md, I have to read it out loud")
already produced clean prose with no skill. The baseline that failed was
Maya saying only "I'm back. What happened?" with process notes still on
screen: grok-4.6 wrote `Core hub`, `build-inline`, and "prove the claim"
into the manager reply. The skill is a sweep list plus an iron law,
because a "be clear" reminder is a no-op and the leak is specific tokens.

## See also

- [`vet-source`](vet-source.md) — fetched text that instructs; not register
- [`prove-claim`](prove-claim.md) — whether a success sentence is allowed
- [`write-handoff`](write-handoff.md) — a successor agent, not a manager
