---
name: shape
version: 1.1.0
description: Writes what a ticket needs before an agent can build it — the spec triad, or the root cause for a bug — and stops at your approval. Run it with /shape #N.
disable-model-invocation: true
---

# Shape

The second of the five commands. It moves a ticket from Shaping to Ready, and stops at
each gate that only the operator may pass. The states are the roles in `docs/agents/triage-labels.md`.

1. **Take the ticket.** Read it and its comments with the tracker ops in
   `docs/agents/issue-tracker.md`. In one edit, make `shaping` its only state role
   (`docs/agents/triage-labels.md`). Write its ID to `.skills/<CODE>/tickets.md` once the
   feature has a code.
2. **Route by tier.** Use the tier the ticket's frame comment states. If it has none,
   REQUIRED SUB-SKILL: use `frame-change` first.
   - **Tier 1:** REQUIRED SUB-SKILL: use `root-cause`. The fix requirement and its guard
     come from that.
   - **Tier 2:** REQUIRED SUB-SKILL: use `specify-behavior`, then `design-solution`, then
     `plan-tasks`. Each one stops at its own approval gate, and so does this command. The
     next `/shape #N` resumes at the first piece that is not yet `Approved`.
3. **Ready.**
   - **Tier 2:** when the plan is approved, `plan-tasks` publishes onto this same ticket and
     swaps `shaping` for `ready-for-agent`.
   - **Tier 1:** the fix is ready once the operator accepts the cause and approves the
     mini-spec: the fix requirement and its `SHALL CONTINUE TO` guard. An approval given
     up front for a stated fix counts when the drafted text says exactly that; quote it
     in the comment. Then, in one edit, write `Requirements covered: <fix ID>, <guard ID>`
     into the ticket body and swap `shaping` for `ready-for-agent`. `/go` reads that line
     to recognise a tier-1 fix.

   In three baseline runs, Lan had approved #28's fix up front. One kept it in Shaping. One
   made it Ready but wrote no `Requirements covered:`, so `/go` would have sent it back. One
   left the mini-spec as Draft and waited.

At every stop, comment on the ticket what is waiting and on whom: "requirements.md
drafted, waiting for Lan's approval". `/board` then shows the ticket under Shaping with
that line.

End with what was written, what waits on the operator, and the next command: `/shape #N`
again, or `/go #N` once Ready.
