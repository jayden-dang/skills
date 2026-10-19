---
name: idea
version: 1.0.0
description: Puts an idea on the board as a ticket and frames it, so it waits in Shaping with its tier and open questions. Run it with /idea <the idea>.
disable-model-invocation: true
---

# Idea

The first of the five commands (`/idea`, `/shape`, `/go`, `/board`, `/cut-release`). It
takes an idea from the operator's head onto the board, where the workflow can track it.
States and owners: `docs/guide/workflow.md`.

1. **File it.** Create one ticket with the tracker ops in `docs/agents/issue-tracker.md`.
   The title is the idea in a line. The body is the operator's words verbatim, plus
   anything they linked. Give it exactly one state role, `needs-triage`, from
   `docs/agents/triage-labels.md`. If the repo's working agreement gates new tickets,
   follow the agreement: draft the ticket, create nothing, and say who must approve it.
   *Done when: the ticket exists with one state role, or the draft names its approver.*
2. **Frame it.** REQUIRED SUB-SKILL: use `frame-change` on the ticket's idea.
3. **Record the frame on the ticket.** In one edit, swap `needs-triage` for `shaping`.
   Then comment the stated tier, the neighbours `frame-change` found, and the open
   questions, numbered. Tier 0 skips Shaping: swap to `ready-for-agent` and say so.
   *Done when: the ticket carries one state role and the comment.*

One ticket, one state role. One baseline run that filed an idea labelled it `needs-info`
and `status:shaping` at once, and the board then showed it in two columns.

End with the ticket's URL and the next command: `/shape #N`.
