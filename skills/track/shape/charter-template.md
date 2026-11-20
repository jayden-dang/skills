# Charter: {ticket} {title}

Written by the conductor from the operator's `/shape {ticket} --auto`. The operator reads the result on the
spec sheet, and nothing here is approved until then.

## Sessions
- `{slug}-work` runs the spec chain. `{slug}-interpret` reads the repo and reviews, and writes only under `RUN`.
- Each accepts messages from the other and from the conductor `{conductor}`, who wakes them, sends the final review, and relays the operator's reply.
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

## Delegated
{the card's Delegated line, or "None stated"}
Choices of these kinds are yours. Decide them, label them `agent-decided` in the ledger, and keep them off the
sheet's Needs you and the PR's decision list.

## Ask me
{the card's Ask me line, or "None stated"}
A fork of one of these kinds is the operator's: put it to `{slug}-interpret` as usual, build nothing on it, and
name it in the report. The conductor stops at the sheet. A fork about how a screen looks or behaves goes to
`## The UI stop` instead, when this charter has one.

## The UI stop
{keep when the card's UI line is not `none` and it names no `UI brief:`; otherwise delete this section}
The screen is the operator's, and they pick it in the running app. Once `{slug}-interpret` has approved
`requirements.md`, run `draft-ui` in `{WT}` before `design-solution`. The variants live in the app itself, signed
in as a real user, on this worktree's own instance. That instance has its own ports and its own database: made
the way `project.md` says to run a second instance; failing that, with the repo's own create, migrate and seed
commands, on the local database server, under a name taken from the worktree. That database belongs to the
worktree. It is not data outside it, and making it is not a hard stop. The developer database and the
operator's running instance stay untouched. The fake behind the client answers only the calls no endpoint serves
yet. Two runs on a shared local database store read the per-run database as outside the worktree and faked
every call, sign-in included. The operator would have picked on invented data. In klynt the same reading put the
draft on a separate page with no desktop around it. When neither `project.md` nor the code offers a way to point
an instance at its own database, stop and name what the repo is missing in the report.

Look at every variant and record each one's walk, with captures and walks saved under `{RUN}/ui/`. Leave the
app running. Write `{RUN}/ui-pick.md` with:
- how to open each variant (its URL or launch command), and the login to use;
- a one-line pitch, the capture path and the walk video path for each;
- your recommendation and its reason.

Then end your turn. `{slug}-interpret` may review the variants' code, but it never picks one or says go.
The operator's replies arrive from `{conductor}` as `{RUN}/ui-reply.md`. Apply what they change, show the
variants again, rewrite `ui-pick.md`, and wait again. On their explicit go, lock as `draft-ui` says, keeping
the winner on this branch. Then run `design-solution`, which lifts the brief and its `## Contract`, and
`plan-tasks`, whose tasks finish the kept code.

When `requirements.md` has no requirement a person sees or does on a screen, skip this stop and say so in
one line of the report.

After the lock, any change to what the locked screen shows or does goes back through this stop. That holds
whether the change is in the brief, the design, the tasks or the code. Apply it to the running app, rewrite
`ui-pick.md` to name the change, and wait for the operator's go. In one run, after the go, `work` rewrote what
the screen does after a refused reservation in the brief and the design, "on my own authority". The build
would have shipped a screen the operator never clicked.

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
the close package, each story's one-demoable-act check, requirements, design and tasks. `draft-ui`'s pick
and go are not on that list: they are the operator's, through `## The UI stop`. Every file stays
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
- A persisted format or a migration, unless the section "Under --go" below is present; anything that moves money, always.
- A test or a step that would change a config or data file outside `{WT}`, `{RUN}` or a temporary directory.
- Two Lock lines that contradict each other.
- A change to the vision, or a pivot (`/define-project`), or a catalog needing `/map-features`.

## The final review
After your report, `{conductor}` sends a final review. Vet each item with the fork order above, apply or reject it with a reason in that file, send `{slug}-interpret` only what moved, commit, and rewrite the report. The operator sees the result, not the list.

## Bounds
3 review rounds per gate. A finding still open after 3: label it, write the report, end. The same finding sent
back twice with no new evidence counts as stuck.

## The end report
Stage reached; each gate's rounds; a decision table (decision, class Lock / Weigh / agent-decided, source); every
place a skill stopped for the user and what answered it; every skill run and skipped; anything this charter failed to answer.

## Under --go
{only with --go: copy this section; without --go, delete it}
- The operator's `/shape {ticket} --go` approved the spec before they read it. The conductor pushes `feat/{slug}` and opens the draft pull request. The build session's `land-branch` then pushes, rewrites the body, posts its verdict and makes the PR ready: that is the build's job, not the conductor's. Other sessions commit locally.
- A migration may be written. It runs only against a local database: the worktree's own where the repo provisions one, else an isolated plane the repo documents, else the local dev database. A database URL that is not local stops the run.
- A question only the operator could answer: build the option that keeps every documented contract, and put the question under `## Needs a decision before merge` in the pull request.
