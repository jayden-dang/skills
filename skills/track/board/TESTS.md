# TESTS.md — board

## 2026-10-19 — 1.0.0 (closed workflow W6)

Fixture: `harbor-ledger` + overlays `latefee-plan`, `fmt-plan`, then `scenarios/gh-board.sh`
(the board on a stateful `bin/gh`, never GitHub) and `scenarios/gh-roles.sh` (the four
newer state roles mapped to `status:*` labels). Scored by `scenarios/wf-score.py` and the
final report. Design: `docs/design/2026-10-19-closed-workflow.md`.
Before the run, `/tmp/wf-pre-pr.sh` opens PR #14 for #21 with "Closes #21" and a "Needs a
decision before merge" section, and takes #21 off the ready column without adding
`in-review`. The board then has:
- PR #14 with its parked decision;
- #25 `needs-info`, with a question to Lan;
- #26 `ready-for-human`, held by Minh;
- #27 untriaged;
- #22 and #23 eligible, with #22 blocked by #21;
- #24 `ready-for-agent` with no spec.

**RED, no skill.** Prompt: "What's waiting on me this morning? Standup is in ten minutes."

| | h1 | h2 | s1 |
|---|---|---|---|
| PR #14's decision | yes | yes | yes |
| #25's question | yes | yes | yes |
| #27 untriaged | no | no | yes |
| #24 ready with no spec | no ("approved for November") | no | no |

**GREEN (1.0.0).** `scripts/board.py` prints every section, always. A `Board and repo
disagree` section catches a ready ticket with no approved spec, an open PR's ticket with
no `in-review` role, an open ticket whose spec is `Implemented` or `Shipped`, and a ticket
with two state roles. Prompt: "/board — What's waiting on me this morning? …"

| | h1 | h2 | s1 |
|---|---|---|---|
| ran `board.py` | yes | yes | yes |
| PR decision quoted, #25 question, #27 to triage | yes | yes | yes |
| #24 named as not eligible, spec missing | yes | yes | yes |
| #21's PR without `in-review` named | yes | yes | yes |
| tracker writes | 0 | 0 | 0 |

Not covered: Linear (run with `--issues` and `--prs` files), Notion drafts passed with
`--drafts`, and a board of more than 30 tickets.
