# `shape`

> What a ticket needs before an agent can build it: the spec triad, or the root cause for a bug. It stops at each approval only you can give.

|  |  |
|---|---|
| **Bucket** | track |
| **Invocation** | `/shape #N` (user-invoked; `disable-model-invocation: true`) |
| **Reads** | the ticket and its comments, `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`, the feature's spec files |
| **Writes** | `shaping` as the ticket's only state role, a comment at each stop saying what waits and on whom, `.skills/<CODE>/tickets.md`, and what the skills below write |
| **Calls** | [`frame-change`](frame-change.md) when the ticket has no tier; [`root-cause`](root-cause.md) for tier 1; [`specify-behavior`](specify-behavior.md), [`design-solution`](design-solution.md) and [`plan-tasks`](plan-tasks.md) for tier 2 |
| **Called by** | nobody — it is user-invoked |

## When it fires

When a ticket sits in Shaping and you want it to reach Ready. It is the second of the [five commands](../workflow.md), after [`/idea`](idea.md).

## What it does

1. **Take the ticket.** It reads the ticket and makes `shaping` its only state role. The ticket's ID goes to `.skills/<CODE>/tickets.md` once the feature has a code.
2. **Route by tier.** Tier 1 goes to [`root-cause`](root-cause.md); the fix requirement and its guard come from that. Tier 2 goes through `specify-behavior`, `design-solution` and `plan-tasks`, each stopping at its own approval gate, and so does this command. The next `/shape #N` resumes at the first piece that is not yet `Approved`.
3. **Ready.** When the plan is approved, `plan-tasks` publishes onto this same ticket and swaps `shaping` for `ready-for-agent`.

At every stop it comments what is waiting and on whom, such as "requirements.md drafted, waiting for Lan's approval", so [`/board`](board.md) shows the ticket under Shaping with that line.

## `--auto`

`/shape #N --auto` writes the whole spec with nobody at the keyboard, then hands you one page. The session you typed in conducts: it checks the road with [`brief-road`](brief-road.md), writes a charter from what the repo already decided, opens a `work` session and a read-only [`interpret-session`](interpret-session.md) session in tmux, keeps the machine awake, and wakes a session that stops. When they finish it reads their transcripts to see which skills really ran, audits the files, runs one outside advisor, and writes `review.html`.

The page says what changes for you, what the agents got wrong, what you decide, what could be cut, what it touches, what happens when it runs, how far to trust it, and what the report after the build will hold. You pick on the page and paste the reply back. Changes go back through both sessions. Every file stays `Status: Draft` until you approve, and only then is the ticket Ready for [`/go`](go.md).

It needs Claude Code's cross-session messaging, `tmux`, and a trusted repo. Tier-1 bugs use the plain command, because a root cause waits on you. A road that is not Ready stops with what it waits on.

## What the tests showed

The RED is in [`plan-tasks`](plan-tasks.md) 1.9.0: publishing onto an existing ticket left two state roles in 2 of 3 runs, and that fix lives in `plan-tasks`. With `/shape #24` on a ticket labelled ready with no spec, both haiku runs made `shaping` the only state role, framed it as tier 2, stopped for the answers before writing any requirements, and commented what waited and on whom. See `skills/track/shape/TESTS.md`.

Not covered: the resume path after approval, and tier 1. `--auto` ran through to its page on Sonnet; its evidence and gaps are in the skill's `TESTS.md`.

## See also

- [The workflow](../workflow.md) — the states and who moves each one
- [`/idea`](idea.md) — where a ticket starts
- [`/go`](go.md) — the next command, once the ticket is Ready
- Design: `docs/design/2026-10-19-closed-workflow.md`
