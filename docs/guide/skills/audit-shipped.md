# `audit-shipped`

> What merged last week, checked for the edge cases its specs and tests missed. Each real one is run, then put on the board as a follow-up.

|  |  |
|---|---|
| **Bucket** | review |
| **Invocation** | `/audit-shipped` (user-invoked; `disable-model-invocation: true`) |
| **Reads** | `git log --first-parent --merges` on the integration branch, each merge's ticket and spec (`requirements.md`, `design.md`), the diff for the window, the whole repo for readers of changed fields, `docs/agents/project.md`, and the glossary (`CONTEXT.md`) |
| **Writes** | one ticket per real finding (Inbox), or one file per finding in `.skills/inbox/` where the repo says someone else approves or opens tickets. No tracked file. It may run probes |
| **Calls** | nothing |
| **Called by** | nobody — it is user-invoked |

## When it fires

When work has already merged and you want to know what it missed. The window is yours, else the last 7 days. The branch is `Default PR base:` in `docs/agents/project.md`, else `main`. A branch that has not merged yet is [`inspect-change`](inspect-change.md)'s job.

## What it does

First it pins the window: each merge, its ticket and its spec, and the diff from before the earliest merge to the branch tip.

Then two passes, both required:

- **Reader pass.** List every new state the window gives an existing field or type, such as a new status value. Search the whole repo, docs included, for everything that reads that field or its record type. Fill one row per reader. When the reader belongs to another feature, build one input that reaches both features, run it and record the output. This catches the case where each feature does what its own spec says and the two together are wrong.
- **Glossary pass.** For each glossary term the window's specs or diff use, quote the definition and the line that implements it. A definition the line does not implement is a finding, however harmless it looks.

## The report

Three parts: the findings, most severe first, each naming the requirement ID or glossary term it breaks and the command that shows it (or "read, not run"). Then the two tables. Then one follow-up per real finding: a ticket in Inbox, or a file in `.skills/inbox/` naming who files it. [`/board`](board.md) lists both under Waiting on you.

## What the tests showed

Eight runs without the skill, on a week with three merged features. The bugs inside one feature were found nearly every time. The cases between features and outside the code were not. A fully refunded part-paid invoice that still accrues a late fee was found 3 of 8 times. A "today" that is the UTC date where the glossary counts marina days was found 2 of 8 times. No run created a ticket.

Six runs of 1.0.0 on a new fixture (2026-11-15): one of four wrote its follow-ups only in the reply "because the skill says draft", and both runs on a repo where someone else approves tickets left them in the reply or one scratch file. The board showed none of those eleven. With 1.1.0, four of four runs put every follow-up where the board lists it.

With the skill, all four runs found both, though the skill names those two cases, so this shows the passes run as written. On a second, held-out week with different planted cases, the reader table found a payment that silently reopens a void invoice in 4 of 4 runs, against 0 of 4 without. See `skills/review/audit-shipped/TESTS.md`.

Not covered by the tests: GitHub or Linear trackers, a window with no glossary, and squash-merge history.

## See also

- [`inspect-change`](inspect-change.md) — the review before merge
- [`board`](board.md) — where the follow-ups show up
- [`triage`](triage.md) — what happens to an Inbox ticket next
