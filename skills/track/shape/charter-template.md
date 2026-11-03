# Charter: {ticket} {title}

Written by the conductor from the operator's `/shape {ticket} --auto`. The operator reads the result on the
review page, and nothing here is approved until then.

## Sessions
- `{slug}-work` runs the spec chain. `{slug}-interpret` reads the repo and reviews, and writes only under `RUN`.
- Each accepts messages from the other and from the conductor `{conductor}`, who may only wake them.
- Recovery resumes the same session name.

## Paths
- Worktree `{WT}`, branch `feat/{slug}`. Local commits only: no push and no PR.
- `RUN` = `{RUN}`, absolute. `scan.md`, `knowns.md` and `close-package.md` go there, not under `.skills/<CODE>/`.
  - `ledger.md`: every Lock, Weigh, Still-open and Unverified line, with its source.
  - `rounds.md`: one line per exchange: output of `date +%T`, gate, round, verdict.
  - `report.md`: the end report.
- Messages carry a path and a one-line ask, never a document's body.

## What counts as decided (Lock)
{each line: statement — file:line}

## What is evidence, not decided (Weigh)
Research notes, and anything either session derives.

## Out of scope
{from the road, the milestone and earlier close packages; "none stated" if none}

## Deciding a fork, in this order
1. A Lock answers it: cite the line.
2. The code, the history or a primary source answers it: cite it. Before writing that a file is absent or
   a fact unverified, open the file or run the command. An external fact takes `research`.
3. Neither: put it to `{slug}-interpret`. Its pick is Weigh.
4. Still open: take the option that leaves every documented contract as it is, label it `agent-decided` in
   the ledger and in the file it lands in, and keep going.

A Weigh or `agent-decided` value may enter a requirement only with that label beside it. Never word one as
the operator's own choice.

## Gates in this run
Where a skill stops for the user, `{slug}-interpret`'s `approve` on the file on disk opens the next step:
the close package, each story's one-demoable-act check, requirements, design and tasks. Every file stays
`Status: Draft`, and `plan-tasks` does not publish or offer routes in this run. Evidence rules stay in force:
a claim about the code needs the file opened.

## Required steps
`clarify-decisions`, `load-subgraph` and the scan subagent run as their skills say, and the conductor checks
the transcript. An interview's questions go to the fork order above.

## Other skills
Use any model-invocable skill the way a person would. `plan-milestones` may add, split or defer a roadmap item;
the roadmap stays Draft and every change goes in the report. A milestone is never closed in this run.

## Tracker
This ticket is the only one. Create no issue. A skill that wants a claim uses this ticket.

## Hard stops: write the report and end
- A persisted format or a migration, or anything that moves money.
- A test or a step that would write outside `{WT}`, `{RUN}` or a temporary directory.
- Two Lock lines that contradict each other.
- A change to the vision, or a pivot (`/define-project`, `/assess-pivot-impact`), or a catalog needing `/map-features`.

## Bounds
3 review rounds per gate. A finding still open after 3: label it, write the report, end. The same finding sent
back twice with no new evidence counts as stuck.

## The end report
Stage reached; each gate's rounds; a decision table (decision, class Lock / Weigh / agent-decided, source); every
place a skill stopped for the user and what answered it; every skill run and skipped; anything this charter failed to answer.
