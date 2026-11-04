---
name: shape
version: 1.5.0
description: Writes what a ticket needs before an agent can build it — the spec triad, or the root cause for a bug — and stops at your approval, or with --auto writes the whole spec unattended and hands you one review page, with a film of the spec under --video and in Vietnamese under --vi. Run it with /shape #N.
disable-model-invocation: true
---

# Shape

The second of the five commands. It moves a ticket from Shaping to Ready, and stops at
each gate that only the operator may pass. The states are the roles in `docs/agents/triage-labels.md`.

WHEN the command carries `--auto`, read `auto.md` beside this file and follow it exactly, in place of the steps below.

1. **Take the ticket.** Read it and its comments with the tracker ops in
   `docs/agents/issue-tracker.md`. In one edit, make `shaping` its only state role
   (`docs/agents/triage-labels.md`). Write its ID to `.skills/<CODE>/tickets.md` once the
   feature has a code, keeping any fields already on its line.
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
     in the comment. Then, in one edit, record `<fix ID>, <guard ID>` and swap `shaping` for
     `ready-for-agent`. `/go` reads them to recognise a tier-1 fix. Where specs are shared,
     they are a last body line, `Requirements covered: <fix ID>, <guard ID>`. Where specs are
     private, they go on the ticket's line in `.skills/<CODE>/tickets.md`, as `covers: <fix ID>,
     <guard ID>`. Two baseline runs on private specs rightly kept the IDs off the ticket, wrote
     only `#3` to that file, and left `/go` unable to recognise the fix.

   In three baseline runs, Lan had approved #28's fix up front. One kept it in Shaping. One
   made it Ready but wrote no `Requirements covered:`, so `/go` would have sent it back. One
   left the mini-spec as Draft and waited.

At every stop, comment on the ticket what is waiting and on whom: "requirements.md
drafted, waiting for Lan's approval". `/board` then shows the ticket under Shaping with
that line.

End with what was written, what waits on the operator, and the next command: `/shape #N`
again, or `/go #N` once Ready.
