---
name: board
version: 1.5.1
description: "Use when someone asks what is waiting on them, what the agents are doing, what is on the board, for a standup summary, or where one feature's build stands right now. Produces the whole board by state, starting with everything waiting on the user, plus where the board and the repo disagree; or one build's status read from its plan, ledger, git, tests, ticket and pull request. Not for the roadmap (refresh-roadmap-status)."
---

# Board

Answer "what's waiting on me, and what are the agents doing?" across every open ticket,
in the time it takes to sit down for standup. The roadmap is `/refresh-roadmap-status`.

**Asked where one feature's build stands** ("where is the SPAY build", "the LATEFEE run
stopped, what is left", `/board <CODE>`): read `run-status.md` beside this file and follow
it in place of the steps below.

## The Iron Law

```
EVERY LINE OF THE REPORT COMES FROM board.py. NO SECTION IS SKIPPED.
```

Three baseline answers to "What's waiting on me this morning?" read the board ad hoc.
All three found the open PR's parked decision and the `needs-info` question. Two never
mentioned #27, a ticket nobody had triaged. None noticed that #24 was labelled
`ready-for-agent` with no spec behind it: one listed it as "approved and ready for you
to pick up".

## 1. Collect

From the repo root, run `scripts/board.py` beside this file.

- **On a github tracker:** run it with no arguments; it asks `gh` itself.
- **On any other tracker:** write the open tickets and open PRs in the JSON shapes its
  docstring names, using the ops in `docs/agents/issue-tracker.md`. Pass them with
  `--issues` and `--prs`.
- **Draft surface `notion`:** also fetch the **Drafts data source** named in
  `docs/agents/issue-tracker.md`. Pass every row not yet signed off as `--drafts`, with
  the sign-off role's newest comment on each.

The script is read-only, and so is this skill: write nothing to the tracker.
*Done when: every section of the output is in front of you.*

## 2. Report: these slots, in this order

1. **Waiting on you.** Every entry under that heading, each with the one thing to do:
   - a PR: review and merge, quoting its decision verbatim when it has one;
   - a question: answer it;
   - Shaping: write the spec (`/shape #N`) or approve it — each line names who is framing it;
   - Inbox: triage it (`/triage`);
   - Human-only: do it (yours), or who holds it;
   - a draft: sign off, or answer its comment;
   - a Not-filed line: open the file, then send it to the approver it names, file it, or delete it.

   Write `none` only for a section that printed `none`.
2. **With agents.** What is being built and by whom. Then the ready tickets that are
   eligible, which `/go` would take next, with any open blocker.
3. **Board and repo disagree.** Each line as printed, plus the edit that fixes it. Give
   the label to swap, or the spec to finish. Do not make the edit.

Then one sentence the operator can say at standup, drawn only from slots 1 and 2.

Asked about one ticket (`/board #23`), report its line from each section it appears in,
and for that feature's build follow `run-status.md`.

## Red Flags

- A line in the report with no section of `board.py` behind it
- "Nothing waiting on you" when any Waiting-on-you section printed an entry
- Calling a ticket ready when the script printed `NOT eligible`
- Editing a label or comment while reporting
