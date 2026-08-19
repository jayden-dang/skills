---
name: speak-outer
version: 1.0.0
description: Use when writing anything a person will read — a status, a reply,
  a standup note, a PR body — produces outer-register prose with no process
  machinery.
---

# Speak Outer

Anything a person reads is the outer register. The switch is total.

## The Iron Law

```
NOTHING A PERSON READS CARRIES PROCESS MACHINERY
```

A status, a reply, a standup note, a PR description, and any other text
aimed at a human is spoken sentences in the domain. Skill names, pass
labels, requirement-citation grammar, and ledger jargon stay off the page.

## The Sequence

1. **NAME THE READER** — a person, not the next skill. *Done when: you can
   say who will read this out loud.*
2. **WRITE THE OUTER** — what is in, what is next, in the words of the
   work (invoice, report, PDF, test). *Done when: a manager could read it
   without knowing this skill set exists.*
3. **SWEEP** — delete every process token before the file lands. *Done
   when: the sweep list below is empty in the outgoing text.*

## Sweep list

These tokens do not appear in anything a person reads:

- skill names (`build-inline`, `test-first`, `prove-claim`, `frame-change`)
- `REQUIRED SUB-SKILL`
- `Pass:`, `Tier 2`, `Satisfies:`, `Core hub`
- "closed the loop", "execute loop", "prove the claim" as process talk

The ledger, session notes, and inner working set may still use those
tokens. They are not the reply.

## Rationalizations

| Thought | Reality |
|---|---|
| "She already knows how we work" | She asked what happened, not which skill is loaded. |
| "test-first, then prove the claim" is just being precise | Those are skill names. The domain sentence is "next is the failing PDF-export test." |
| "Core hub is how we say where rounding lives" | Say `report.js`. "Hub" is inner register. |
| "build-inline / Pass: loop belongs in a status" | That is the inner track leaking. The outer names the work, not the protocol. |
| "I'll leave the jargon; she can skip it" | If she has to skip it, it should not have been written. |

## Red Flags — stop and rewrite the outer

- You are about to paste session notes or a skill checklist into a reply
- The draft contains `REQUIRED SUB-SKILL`, `Satisfies:`, or a skill name
- You wrote "closed the loop" or "execute loop" to a human
- The first sentence names a skill instead of the work

If a leak already landed, rewrite the file before doing anything else.

## Worked example

Session notes still on screen:

`Using build-inline` · `REQUIRED SUB-SKILL: use test-first` · `Pass: loop` ·
`Satisfies: BILL-1.4` · `Core hub: rounding lives in report.js`

Maya: "I'm back. What happened?"

Outer:

> Still on BILL-1.4 — invoice totals should round once, in `report.js`.
> Next is a failing test for PDF export on the unrounded path.

