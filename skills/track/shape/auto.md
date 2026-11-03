# /shape #N --auto

The operator asked for the whole spec with nobody at the keyboard, then one page to review it on.
The session they typed in is the **conductor**. It opens two more sessions, watches them, checks
what they really ran, and writes the page. It writes no spec itself.

| Role | Where | Job |
|---|---|---|
| **conductor** | this session | charter, peers, watching, receipt, audit, page |
| **work** | new session | `frame-change` through `tasks.md` |
| **interpret** | new session, read-only | answers forks from the code, reviews each file |
| **advisor** | one subagent, once | what the person really needs, what could go |

## The Iron Law

```
AGENTS REVIEW. ONLY THE OPERATOR APPROVES.
EVERY SPEC FILE STAYS Status: Draft UNTIL THE OPERATOR HAS ANSWERED THE PAGE.
```

`--auto` replaces every stop before the page, and no stop after it. Without this file, one run on
`--auto` stopped at requirements ("`--auto` doesn't waive that per-story yes") and another skipped
the interview outright. An earlier run stamped `Approved` on three files its operator had never
read, so the word meant nothing when they opened them.

## Steps

1. **Check.** Tools `SendMessage` and `Monitor`, commands `tmux` and `claude`. Any missing, or a tier-1
   bug (its root cause waits on the operator's disposition) → say which, and run the plain `/shape`.
   A ticket naming a `ROAD-N`: REQUIRED SUB-SKILL: use `brief-road`. Any verdict but **Ready** → comment on
   the ticket what it waits on, say so, and end. A run on a road whose `After:` was still in progress
   opened a worktree and wrote "follows ROAD-3" as a Lock without looking up ROAD-3.
   Otherwise step 1 of `SKILL.md`. Pick a short `<slug>` from the ticket.
   `RUN` = absolute path of `.skills/_pending-<slug>/auto/` in this checkout. Create it.
   *Done when: the ticket's only state role is `shaping` and `RUN` exists.*
2. **Charter.** Copy `charter-template.md` to `RUN/charter.md` and fill every `{slot}`. `{conductor}` is this
   session's name, from the first line `ListAgents` prints. For Locks, read:
   the ticket; its `ROAD-N` line and milestone outcome in `docs/roadmap/INDEX.md`; every line
   `grep -n` finds for the road's name or feature in `docs/ARCHITECTURE.md`, `docs/architecture/`,
   `CONTEXT.md`, `docs/adr/`; every `close-package.md` under `.skills/` naming that `ROAD-N`.
   *Done when: no `{slot}` remains and each Lock carries `file:line`.*
3. **Workspace.** `git worktree add .worktrees/<slug> -b feat/<slug> <Default PR base>`. `WT` = its absolute path.
4. **Keep the machine awake.** Where `caffeinate` exists, start `caffeinate -i -t 21600` in the
   background and stop it at step 9. A run with nothing holding the Mac died mid-response when it slept.
5. **Open the peers.** Fill `interpret-prompt.md` and `work-prompt.md` into `RUN/`. In one tmux session
   `<slug>`, from `WT`:
   `claude --name <slug>-interpret --model sonnet --permission-mode auto "$(cat RUN/interpret-prompt.md)"`,
   wait until `ListAgents` shows it idle, then the same for `<slug>-work`. Both flags are fixed: a peer on
   `default` sat 26 minutes on a prompt to read its own charter, and two with no `--model` ran on the
   machine's Opus default. Other sessions `ListAgents` shows are not part of this run, whatever they are named.
   A pane asking to trust the folder → stop and tell the operator to trust it; answering it is theirs.
   *Done when: `ListAgents` lists both.*
6. **Watch.** Start `Monitor` with this command, filled in, and re-arm it whenever it expires:

   ```sh
   while :; do
     [ -f RUN/report.md ] && { echo REPORT; exit 0; }
     tmux has-session -t <slug> 2>/dev/null || { echo GONE; exit 1; }
     [ -z "$(find RUN WT/docs/specs WT/.skills -type f -mmin -10 2>/dev/null | head -1)" ] && echo STALL
     sleep 300
   done
   ```

   On `STALL` read both panes with `tmux capture-pane -p`. An ended turn, an API error, or one peer
   waiting on the other → `SendMessage` to the stuck peer: what stopped, continue under the charter.
   A dialog in a pane → stop and tell the operator. Each peer gets 3 wakes; the 4th `STALL` or a `GONE`
   ends the run at step 8 with what exists. Two of two silent stops in one run never recovered alone.
7. **Receipt and audit**, when `RUN/report.md` exists. Run, from `WT`:

   ```sh
   python3 -I <this skill>/scripts/skill_receipt.py --cwd WT --name <slug>-work \
     --require frame-change,clarify-decisions,load-subgraph,specify-behavior,design-solution,plan-tasks --min-subagents 1
   ```

   Exit 1 → send `work` the `missing:` line once: run them now against the current files, say what
   changed, and rewrite the report. Still missing → it goes on the page. The session's own report is
   not evidence: one listed two skipped steps, and the transcript showed a third.
   Then audit the files yourself, and write each result to `RUN/audit.md`:
   - every statement that a file is absent, or a fact unverified, in `RUN/scan.md`, `RUN/knowns.md` and
     Open Questions: open that file, run that command. One run wrote `~/.codex/hooks.json` as absent; it
     had existed for six weeks, and neither session looked.
   - every `Weigh` line in `RUN/ledger.md`: `grep` its value in `requirements.md` and `design.md`. Present
     with no `agent-decided` label → a finding.
   - every `Status:` line reads `Draft`, and a sample of ten `file:line` citations open to what they claim.
   *Done when: `RUN/audit.md` holds each pass's result, and the receipt prints `missing: none` or its line is on the page.*
8. **Advisor, then the page.** Dispatch one read-only subagent with `advisor-prompt.md` filled in, on a
   mid-tier model. Do not send its answer to the peers. Open what each claim cites and mark any that
   the file contradicts. Then read `review-page.md` beside this file and write `RUN/review.html`.
   *Done when: the page exists with every slot.*
9. **Hand over.** Stop `caffeinate`. Leave the peers open. Comment on the ticket, tracker ops as usual:
   what waits and on whom, with the page's path. End with five lines at most: what was written, the
   decision count, anything missing, the page's path.
10. **The operator's reply.** Changes → send them to `work`, have `interpret` review only what moved,
    rerun step 7's audit, rewrite the page. Approval of the page → have `work` set `Status: Approved`
    on the three files quoting the operator's words, then finish `plan-tasks` Step 5 publishing onto this
    ticket, which makes it Ready. Close the peers. Name `/go #N`.

## Rationalizations

| Thought | Reality |
|---|---|
| "`--auto` doesn't waive the per-story yes" | It moves it. The operator gives it on the page, once, for the whole spec |
| "Interpret approved it, so it is `Approved`" | Interpret's verdict opens the next gate in this run. The word on the file is the operator's |
| "I will just write the spec here, it is faster" | Then nothing independent read it. Work and interpret are separate sessions so that one can catch the other |
| "The report says everything ran" | Run the receipt |
| "The advisor's cut is obviously right, I will send it to work" | Every cut in the measured run came from a document the operator had approved. Only they can cut it |

## Red flags

- A spec file reading `Approved` before the operator answered the page
- The conductor writing `requirements.md`, `design.md` or `tasks.md`
- A step 7 result taken from `report.md` instead of the command's output
- Answering a dialog in a peer's pane
- A second advisor round, or advisor findings sent to a peer
