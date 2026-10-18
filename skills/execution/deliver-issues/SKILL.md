---
name: deliver-issues
version: 1.0.0
description: Delivers every eligible ticket on the board to its own reviewed pull request in one unattended run, with one message for whatever needs the operator. Run it with /deliver-issues.
disable-model-invocation: true
---

# Deliver Issues

Take the board's eligible tickets to pull requests while the operator is away. Each one
goes through the same chain a single ticket gets, in dependency order, and the run ends
with one message.

## The Iron Law

```
EVERY TICKET GETS ITS OWN BUILD, REVIEW AND LANDING. A BOARD OF THEM IS NOT A REASON TO SKIP ONE.
```

Four baseline runs on a four-ticket board, ten approved tasks, without this skill: all
four wrote every task in the controller. Across the four there were 0 implementer or
reviewer dispatches, 0 `inspect-change` and 0 `land-branch`, and one run loaded no skill
at all. A haiku run explained: "I built the formatting work inline, test-first, rather
than through the execute skills, since the tasks were small." Six PRs went up that
nobody but their author had read. The operator reviews tonight on the strength of a
review that never ran.

## 1. The frontier

Read the tracker operations from `docs/agents/issue-tracker.md`. A ticket is eligible
when its status is the tracker's ready state and its feature's `requirements.md`,
`design.md` and `tasks.md` all read `Status: Approved`. List each other ready ticket with
the piece it lacks. Order the eligible ones by `Blocked by:`.
*Done when: every ready ticket is eligible, in order, or listed with what it lacks.*

## 2. Each eligible ticket, in order

1. **Branch** from `Default PR base:` in `docs/agents/project.md`. A ticket blocked by
   one delivered in this run branches from that ticket's branch instead.
2. REQUIRED SUB-SKILL: use `build-in-waves` on its `tasks.md`.
3. REQUIRED SUB-SKILL: use `inspect-change` on the ticket's range.
4. REQUIRED SUB-SKILL: use `land-branch` with action `pr`. A stacked ticket's PR is
   based on its blocker's branch.

*Done when: the ticket has a PR whose review and receipt came from those three skills.*

## 3. A question only the operator can answer

A sub-skill would stop to ask the operator, whether in a pre-flight review, a boundary
decision or a review finding that needs a ruling. In this run the stop is a decision
taken and shown:

1. Build the option that leaves every documented contract as it is: a consumer named in
   `docs/`, a test that pins a shape, a persisted format.
2. Head that PR's body with **Needs a decision before merge**, giving the question, the
   option built and the one-line change for the other.
3. Carry on with the ticket and with the rest of the board.

The PR is where the operator decides, so parking the ticket costs them the PR. Two of
the four baseline runs parked refunds on the portal-enum question. One left Tasks 1–2
unpushed in a worktree, and neither started the late-fee ticket that waited on it. The
two that built the contract-keeping option and asked in the PR delivered three PRs each.

A denied command is the same kind of stop. Do not retry it. Take the route that needs
none of it — skip the status stamp, or keep the worktree you already have — and record
the skipped step in that PR. One run had its refund worker's
`git worktree remove … && git branch -d …` denied before any code was written. It
stopped there with "I'm not doing either without your OK", and two tickets with
approved plans ended the afternoon with no PR.

## 4. The message

One message, in this order:

1. A table with one row per ready ticket: PR and base, or not eligible and what it lacks.
2. Every **Needs a decision before merge** item, each with its PR and the option built.

*Done when: the message is sent and every ready ticket has a row.*
