# /shape --auto in Codex

Read from `auto.md` step 1 when this session runs in Codex. Every step of `auto.md` holds as written,
except for what this file replaces. The peers are `spawn_agent` children of this session. They live as long
as this session does, so keep it open until step 10.

**Names.** Codex takes lowercase letters, digits and `_` in a task name and refuses `-`. Build `<slug>` from
those characters only. The peers are `<slug>_interpret`, `<slug>_work` and, with `--go`, `<slug>_build`. Use
those names wherever `auto.md` and `go.md` write `<slug>-interpret`, `<slug>-work` and `<slug>-build`.

**Filling the prompts.** `{work}`, `{interpret}`, `{build}` are those names. `{send}` is "`followup_task` with
the peer's task name". `{load}` is "Load every skill a step names by reading its `SKILL.md` from the skills
folder, never from memory." A prompt's first line `/<skill> …` becomes "Read and follow the skill `<skill>`: …".
The peers start in this session's checkout, not `WT`, so add one line to each: "Work only in `WT`: `cd WT`
before every command, and use paths under it." Codex keeps `.git` read-only inside its sandbox, so add a second
line to `work`'s and `build`'s prompts: "A `git` command that writes (`add`, `commit`, `branch`) runs with
escalated permissions and a one-line reason." In a smoke run a peer without that line had its commit refused
("Unable to create … index.lock: Operation not permitted") and reported it instead of asking.

**The session's approvals.** Escalated commands are reviewed automatically only in a session started with
`codex --approve-for-me`. In any other session each commit waits on a person: say so at step 1, and run the
plain `/shape` unless the operator says to go on.

**Step 5, open the peers.** `spawn_agent` with `task_name` `<slug>_interpret`, the interpret row's `model`
and `reasoning_effort` from `model-routing.md`, `fork_turns` `none`, and the filled `interpret-prompt.md` as
`message`. Then the same for `<slug>_work`. Every field is written on every spawn: a spawn with no `model`
runs on whatever this session runs on.
*Done when: `list_agents` lists both.*

**Step 6, watch.** In a loop: `wait_agent` with `timeout_ms` 600000. After each return, run these checks once:

```sh
[ -f RUN/report.md ] && echo REPORT
[ -f RUN/ui-pick.md ] && { [ ! -f RUN/ui-reply.md ] || [ RUN/ui-pick.md -nt RUN/ui-reply.md ]; } && echo UI
[ -z "$(find RUN WT/docs/specs WT/.skills -type f -mmin -10 2>/dev/null | head -1)" ] && echo STALL
```

`REPORT` and `UI` go on as in `auto.md`. A peer that has finished its turn is not stuck: the prompts tell
both to end their turn and wait. Only `STALL` wakes one: `followup_task` to `<slug>_work`, naming what
stopped, to continue under the charter; `<slug>_interpret` only when `work`'s last message waits on its reply. A peer waiting on
an approval is a dialog: stop and tell the operator. Each peer gets 3 wakes, as in `auto.md`.

**Step 7, the receipt.** Add `--harness codex` and pass `--name <slug>_work`. `--cwd` is this session's
checkout, where the peers' rollouts are recorded. Its `model:` line shows what the peer ran on. A model that
is not its row, nor a value the operator gave, goes on the sheet.

**Step 8 and `go.md` step 12.** The advisor is one `spawn_agent` on the advisor row. The build is
`spawn_agent` `<slug>_build` on the build row, with the filled `build-prompt.md`; watch it with the loop above.
Its end file is `RUN/build-report.md`, and its STALL is `go.md`'s.

**Hand over.** Closing a peer means `interrupt_agent` and nothing more. A message to the operator is the reply.
