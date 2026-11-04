# `shape`

> What a ticket needs before an agent can build it: the spec triad, or the root cause for a bug. It stops at each approval only you can give.

|  |  |
|---|---|
| **Bucket** | track |
| **Invocation** | `/shape #N` (user-invoked; `disable-model-invocation: true`) |
| **Reads** | the ticket and its comments, `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`, the feature's spec files |
| **Writes** | `shaping` as the ticket's only state role, a comment at each stop saying what waits and on whom, `.skills/<CODE>/tickets.md`, and what the skills below write |
| **Calls** | [`frame-change`](frame-change.md) when the ticket has no tier; [`root-cause`](root-cause.md) for tier 1; [`specify-behavior`](specify-behavior.md), [`design-solution`](design-solution.md) and [`plan-tasks`](plan-tasks.md) for tier 2; [`make-video`](make-video.md) under `--auto --video` and `--go`; [`deliver-issues`](deliver-issues.md) in a build session under `--go` |
| **Called by** | nobody — it is user-invoked |

## When it fires

When a ticket sits in Shaping and you want it to reach Ready. It is the second of the [five commands](../workflow.md), after [`/idea`](idea.md).

## What it does

1. **Take the ticket.** It reads the ticket and makes `shaping` its only state role. The ticket's ID goes to `.skills/<CODE>/tickets.md` once the feature has a code.
2. **Route by tier.** Tier 1 goes to [`root-cause`](root-cause.md); the fix requirement and its guard come from that. Tier 2 goes through `specify-behavior`, `design-solution` and `plan-tasks`, each stopping at its own approval gate, and so does this command. The next `/shape #N` resumes at the first piece that is not yet `Approved`.
3. **Ready.** When the plan is approved, `plan-tasks` publishes onto this same ticket and swaps `shaping` for `ready-for-agent`.

At every stop it comments what is waiting and on whom, such as "requirements.md drafted, waiting for Lan's approval", so [`/board`](board.md) shows the ticket under Shaping with that line.

## `--auto`

`/shape #N --auto` writes the whole spec with nobody at the keyboard, then hands you one technical sheet of the spec. The session you typed in conducts: it checks the road with [`brief-road`](brief-road.md), writes a charter from what the repo already decided, opens a `work` session and a read-only [`interpret-session`](interpret-session.md) session in tmux, keeps the machine awake, and wakes a session that stops. When they finish it reads their transcripts to see which skills really ran, audits the files, and runs one outside advisor. It sends those findings straight to `work`, which fixes or rejects each with a reason and has `interpret` review what moved. Only then does it write `sheet.html`.

The sheet is one page of lettered panels in a ruled frame, like an engineering drawing: a map of every requirement, one example you step through with Back and Next, the rules that matter most with their clauses labelled, what happens when something fails, what agents decided for you, the plan, and the few things that need you. Three collapsed parts sit under it: what the final review changed, what the spec touches, and how far to trust it. Only the two walk buttons are controls, so there is nothing to fill in. It stays in the run folder, uncommitted, and is written again when the spec changes. Type `approve`, or say what to change in plain words, and changes go back through both sessions. Every file stays `Status: Draft` until you approve, and only then is the ticket Ready for [`/go`](go.md).

More flags go with `--auto`:

- **`--video`** adds a film that explains the closed spec, up to 120 seconds, made by [`make-video`](make-video.md). The sheet embeds it in its first panel, links each step of its example to the film's moment, and marks which requirements the film leaves out, then says on the sheet what each of those asks. There is no film without this flag, and a film that cannot be made leaves the sheet with the reason in that panel. The spec's narration goes to Vibi and the provider behind it, so leave this flag off a repo whose specs must stay on the machine.
- **`--project-style`** gives that film your project's fonts, colors and radii. Without it the film has `make-video`'s default look, in any repo.
- **`--vi`** writes the film and the sheet in Vietnamese. `--en` is the default, whatever language you type the command in. The spec, the charter and both sessions stay in English under either flag.

- **`--go`** carries on past the sheet to a pull request. The command is your approval of the spec, given before you read it. A charter hard stop (money, two decisions that contradict, a vision change) still ends at the sheet. Otherwise the spec is stamped `Approved` quoting your command, the ticket goes Ready, and a draft PR opens with the spec film and a picture of the sheet. A third session then runs [`deliver-issues`](deliver-issues.md) on the same branch: per-task review, the whole-branch review, acceptance in a browser it signs into itself on localhost, a product walk when the front end changed, and `land-branch`, which makes the PR ready. Last, the conductor adds a film of the real app at the last code commit and the data model, drawn from a schema dump when there is a database, and attaches both to the PR. Nothing of that is committed to the branch. Migrations run only on a local database. Merging stays yours.
- **`--work=`, `--interpret=`, `--build=`** pick each session's model, such as `--work=claude-opus`. A `Shape roles:` line in `docs/agents/project.md` sets your usual ones. Without either, work and interpret run on Opus and the build on Sonnet. Codex and Grok are not supported yet.

It needs Claude Code's cross-session messaging, `tmux`, and a trusted repo. Expect about 45 minutes for even a small feature, so start it when you are leaving the machine. Tier-1 bugs use the plain command, because a root cause waits on you. A road that is not Ready stops with what it waits on.

## What the tests showed

The RED is in [`plan-tasks`](plan-tasks.md) 1.9.0: publishing onto an existing ticket left two state roles in 2 of 3 runs, and that fix lives in `plan-tasks`. With `/shape #24` on a ticket labelled ready with no spec, both haiku runs made `shaping` the only state role, framed it as tier 2, stopped for the answers before writing any requirements, and commented what waited and on whom. See `skills/track/shape/TESTS.md`.

Not covered: the resume path after approval, and tier 1. `--auto` ran through to its page on Sonnet, before the sheet replaced that page; its evidence and gaps are in the skill's `TESTS.md`.

## See also

- [The workflow](../workflow.md) — the states and who moves each one
- [`/idea`](idea.md) — where a ticket starts
- [`/go`](go.md) — the next command, once the ticket is Ready
- Design: `docs/design/2026-10-19-closed-workflow.md`
