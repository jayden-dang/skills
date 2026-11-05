---
name: idea
version: 1.4.0
description: Puts an idea on the board as a ticket and frames it, so it waits in Shaping with its tier and open questions. Run it with /idea <the idea>.
disable-model-invocation: true
---

# Idea

The first of the five commands (`/idea`, `/shape`, `/go`, `/board`, `/cut-release`). It
takes an idea from the operator's head onto the board, where the workflow can track it.
The states are the roles in `docs/agents/triage-labels.md`.

**Todos first.** Before step 1, put this command's four steps on the harness's todo tool (`TaskCreate` in Claude Code; load it with `ToolSearch` when it is deferred), else a checklist in your first reply, one item each, and
tick each at its Done when. Two baseline runs filed, framed and commented with no list at all.

1. **File it.** Create one ticket with the tracker ops in `docs/agents/issue-tracker.md`.
   The title is the idea in a line. The body is the operator's words verbatim, plus
   anything they linked. Give it exactly one state role, `needs-triage`, from
   `docs/agents/triage-labels.md`, and assign it to the operator in the same create — the
   assignee is how everyone else sees that this idea is being framed. Two baseline runs
   filed it with `assignees: []`. If the repo's working agreement gates new tickets,
   follow the agreement: draft the ticket, create nothing, and say who must approve it.
   *Done when: the ticket exists with one state role and the operator assigned, or the draft
   names its approver.*
2. **Frame it.** REQUIRED SUB-SKILL: use `frame-change` on the ticket's idea.
3. **Write the card.** This is the one moment the operator is at the keyboard, and an
   unattended `/shape --auto` takes the card as their word. Its slots are Outcome, Examples,
   Must keep, Off limits, Decided, Delegated, Ask me and UI (`none`, `reuse`, `reference` or
   `new`). Fill them from their own words and the confirmed close package: what they fixed goes to Decided, what they
   left to you ("your call", "I don't care") to Delegated, and to Ask me only the kinds of choice
   they said to ask them about first. Your own open questions go in the frame comment, never in
   the card: one run filed eleven of them under Ask me, which would stop every unattended run.
   Ask them for what is still empty, Examples first: at least two, with a named person and
   real values. WHERE `docs/roadmap/INDEX.md` exists, REQUIRED SUB-SKILL: use `plan-milestones`
   to add the item when the frame named none, and to write its card; where the roadmap is
   shared, start the ticket's title with that `ROAD-N` in the same pass. Three Haiku runs added
   ROAD-5 and its card and left the title without it, so no claim check could find the ticket. Otherwise the card is a
   `## Card` section of the ticket body. A body slot the card answers never reads "Not decided
   yet": one baseline wrote that under the operator's three examples, and neither baseline
   touched the roadmap or kept "your call" apart from "ask me first".
   *Done when: the card exists, or its empty slots are named in the comment below.*
4. **Record the frame on the ticket.** In one edit, swap `needs-triage` for `shaping`.
   Then comment the stated tier, the neighbours `frame-change` found, and the open
   questions, numbered. Tier 0 skips Shaping: swap to `ready-for-agent` and say so.
   WHEN the frame added roadmap items and the operator named the one they carry on with, or
   step 3 added the one item,
   record the claim in the same edit, for the check before a spec is written. Where the roadmap is
   shared, that `ROAD-N` starts the title (`ROAD-251 Weekly digest…`). Where it is private, the title
   stays and `.skills/_pending-<slug>/tickets.md` gets the line `<ticket id> road: ROAD-N`, since the
   feature has no code yet. Unnamed → change nothing. The other new items get no ticket here. Two runs left the title alone after the operator said
   he would carry on with ROAD-251; one wrote "Jayden is taking this one" into the comment,
   where no claim check reads.
   *Done when: the ticket carries one state role and the comment.*

One ticket, one state role. One baseline run that filed an idea labelled it `needs-info`
and `status:shaping` at once, and the board then showed it in two columns.

End with the ticket's URL and the next command: `/shape #N`.
