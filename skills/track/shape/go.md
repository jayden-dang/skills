# /shape #N --auto --go — on to a pull request

Read from `auto.md` step 1. Steps 1 to 9 run as written there. These steps replace 10 and 11.
The operator typed `--go`. That command is their approval of the spec, given before they read it.
They will read the pull request, and nothing else, so everything they need goes onto it.

## The Iron Law

```
THE CONDUCTOR WRITES NO CODE, AS IT WRITES NO SPEC.
THE BUILD IS A SESSION OF ITS OWN, RUNNING deliver-issues.
```

One baseline conductor told to carry on to a PR wrote every line itself. It loaded 0 skills and
dispatched 0 subagents. Nothing reviewed the code, nothing drove acceptance, and `land-branch` never
ran. Its demo was 15 seconds of stitched screenshots. Its ticket read `shaping` from start to end.

## Steps

10. **Stop or approve.** A charter hard stop or an Ask me fork ended the work, or `tasks.md` holds more
    than 8 tasks (`grep -c '^### Task' tasks.md`) → run `auto.md` steps 10 and 11 as written, and say
    that `--go` stopped at the sheet and why. A plan over 8 tasks is more than one unattended run
    should carry: name `plan-milestones` to split the road. Agents' success falls as tasks grow
    (METR's 80% horizon is far shorter than its 50% one), and a 5-task build here took about an hour. Otherwise write the command, verbatim, to
    `RUN/operator-reply.md`. `work` sets `Status: Approved` on the three files quoting it, adds
    `Approval: the operator's /shape --go, before reading the spec`, commits, and drafts `plan-tasks`
    Step 5's publish into `RUN/ticket-body.md`; a `work` session that is gone comes back with
    `claude --resume <slug>-work`, and one never opened here is opened as in `auto.md` step 5. Publish it onto the ticket yourself, which makes it
    Ready. Read the ticket back. Close `work` and `interpret`.
    *Done when: the read shows `ready-for-agent` and the three files read `Approved`.*
11. **The draft.** Push `feat/<slug>`. Open a draft PR to `<Default PR base>` with the forge from
    `docs/agents/issue-tracker.md`, title and body through REQUIRED SUB-SKILL `speak-outer`, no
    tool signature. The body opens with `## Needs a decision before merge`, holding the sheet's
    Needs you items, then one line saying no person has read the spec and `--go` approved it.
    Attach the spec film per **Attach a film** below, when there is one.
    *Done when: `gh pr view --json isDraft,url` shows a draft, and the body read back carries the decisions.*
12. **The build.** Fill `build-prompt.md` into `RUN/`. In the tmux session `<slug>`, from `WT`:
    `claude --name <slug>-build --model <build model> --permission-mode auto "$(cat RUN/build-prompt.md)"`.
    Watch it with `auto.md` step 6's loop, with two changes: the end file is `RUN/build-report.md`,
    and STALL means 30 minutes with no new commit on `feat/<slug>` and no file changed under `WT/.skills`.
    A build is long: one klynt lock push took 7.5 minutes, one lane ran 13 hours. Restart `caffeinate`
    for this stage. When the report exists, run the receipt from `WT`:

    ```sh
    python3 -I <this skill>/scripts/skill_receipt.py --cwd WT --name <slug>-build \
      --require deliver-issues,build-in-waves,inspect-change,validate-feature,land-branch --min-subagents 2
    ```

    Add `write-dogfood,run-dogfood` to `--require` when `git diff --name-only <base>...HEAD` lists an
    `.html`, `.css`, `.scss`, `.jsx`, `.tsx`, `.vue`, `.svelte` or template file.
    Exit 1 → send the build its `missing:` line once, re-arm the watch, and wait for the report
    to change: one conductor sent the line and ended its turn, and nothing woke it when the build
    finished a minute later. Still missing → it goes into the PR's decision section. The PR still a
    draft after the build's `land-branch` ran → send the build that line once, the same way. Read the PR back: `gh pr view --json isDraft,url,headRefOid`.
    *Done when: the PR reads ready, not draft, its body is the one `land-branch` wrote, and the
    receipt's lines are in hand.*
13. **Acceptance from the card, by a session that did not build.** The builder checked what it read
    in its own spec, and passed 11 of 11 while 8 product decisions sat unread. Dispatch one fresh
    subagent, not the build session, with the card's Examples, `docs/agents/verify.md` and the branch
    at `CODE_SHA`, the newest commit that is not `docs(<CODE>): record delivery`: REQUIRED SUB-SKILL: use `validate-feature`, with its checklist exactly the
    card's Examples, one item each, driven in the running app with nobody at the keyboard. It reads no
    test, plan or report of the build. A name in an Example stands for a seeded record of the same
    kind. State no screen shows is read the way `run-dogfood`'s probe ladder says, down to a wrapper
    outside the repo that leaves product code untouched; "not run" is for an Example nothing can
    reach. One drive marked all four Examples not run because the offer token never reaches a client;
    another wrapped the server, read the offers, and found Example 4 fail: a passenger accepted onto a
    sailing staff had cancelled. A failed Example → send the build session that example and what
    was seen, once, re-arm the watch, and rerun this step on the new head. Still failing → it heads the
    PR's decision section, as an Example the build does not meet.
    *Done when: `RUN/acceptance.md` has a result per Example, from the drive.*
14. **Evidence on the PR.** `land-branch` adds the delivery line after the PR opens, so the film
    and the model are taken at `CODE_SHA`.
    - **The demo film.** REQUIRED SUB-SKILL: use `make-video` on the branch, kind `pr`, `$REF` =
      `CODE_SHA`, narrated in `LANG`, recorded in the running app, signed in as the build's
      acceptance was. A migration runs only on a local database, as the charter says. A refused
      voice call, or no `PASS` after 3 renders, ends the film: attach what the check drew and say why.
    - **The data model.** A repo with a database: dump the schema of the local database at the base
      and at `CODE_SHA`, with the command `project.md` names or the database's own dump tool. Draw
      the Mermaid `erDiagram` and the list of changed tables and columns from the two dumps, and head
      it `From the schema at <sha7>`. No database: real JSON from the running app, under the words
      "No schema exists". A diagram an agent drew from reading code is headed `Drawn from the code`.
      One baseline headed a hand-written diagram "generated by scripts/data-model.js".
    - **Onto the PR.** `land-branch` wrote the body, so add a block of your own after it, between
      `<!-- shape-go evidence -->` and `<!-- /shape-go evidence -->`: the spec film from step 11, the
      card's Examples with step 13's result for each, the demo film, the data model,
      the dogfood report's four sections in short when a walk ran, the receipt's `missing` line,
      and what nobody ran. Keep the decision section on top: `land-branch`'s, then the spec's
      Needs you items. Nothing from this step is committed to the branch.
    *Done when: the body read back holds the block, the film plays from its attachment URL, and the
    branch's files match `CODE_SHA` plus the delivery line.*
15. **Hand over.** Stop `caffeinate`. Close `<slug>-build`. Comment on the ticket: the PR, and that it
    waits on the operator's review. End with five lines at most: the PR, what it delivers, how many
    decisions wait, what was not run, and that merging is theirs.

## Attach a film

Never commit a film or a screenshot to the branch: one baseline committed 7.3 MB of video under
`docs/specs/` and linked `blob/…mp4`, which GitHub does not play. Attach it:
`gh pr edit <N> --attach <file>`, on its own line in the body as a bare URL. Over 9.5 MB → re-encode
with `ffmpeg -crf 30` and check again: GitHub refuses video over 10 MB on a free plan. Still over →
attach the contact sheet `check_video.py` wrote, and say the film was too large. Read the body back.

## Rationalizations

| Thought | Reality |
|---|---|
| "The tasks are small, I can build them here" | The baseline said nothing and did exactly that. No review ran on any line |
| "`--go` means skip the sheet" | The sheet still gets written: the hard stops are judged on it, and its Needs you items head the PR |
| "Commit the film so the PR links to it" | A link to a committed MP4 does not play, and the binary rides into the base on merge |
| "The script prints the diagram, so it is generated" | Only what came from a dump or a run is. Say which |

## Red flags

- A line of product code written in the conductor session
- The PR made ready by the conductor before `land-branch` ran in the build
- A `.mp4`, `.png` or diagram script added to `feat/<slug>` by this step
- The demo film's `$REF` equal to the `record delivery` commit
- A migration run against a database that is not local
