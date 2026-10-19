# Dogfood on a real board: `deliver-issues` on klynt

Date: 2026-10-18 · Plan: `2026-10-18-survey-upgrade-plan.md` T20 · jdk `a83d23c`

## Setup

Repo: klynt (`KlyntLabs/klynt`), branch `dev` at `bcc6dd72c`. Tracker: GitHub Issues,
`Default PR base: dev`. The run used a sandbox, so nothing could reach the team:

- **Clone.** A clone in `/tmp/klynt-dogfood/klynt`. Its `origin` is a local bare repo, so
  a push lands on disk only. The operator's working copy was not touched; it had a CPLAN
  build in progress on `dev`.
- **Read-only `gh`.** A guard put ahead of the real `gh`. Reads reach GitHub: `issue` and
  `pr` `list`/`view`, and GET `api` calls. Every write (`pr create`, `issue comment`,
  label edits, any non-GET `api`) is appended to `gh-writes.jsonl` and answered with a
  fake URL.
- **Skills.** All 74 engineering skills at `feat/survey-upgrade` (`a83d23c`), installed
  into the clone's `.claude/skills/`.

Headless haiku (`run-headless.sh`, budget 6 USD). The prompt: "/deliver-issues — Deliver
every ticket on the board that's ready. I'll review the PRs tonight; put anything you
need from me in one message."

## Result

| | |
|---|---|
| Ready tickets on the board | 4: #258 FLASH, #253 PANEL, #252 CFGC, #243 QUOTA |
| Eligible | 0. All four specs read `Status: Implemented`, not `Approved` |
| Proof given per ticket | the triad status, plus the merge or file on `dev` that holds the code |
| Out of scope, named | #262, #261, #260, #242 (not labelled `ready-for-agent`) |
| Writes to GitHub | 0 (`gh-writes.jsonl` empty) |
| Branches, files changed | 0 |
| Messages to the operator | 1: the table, then two asks |
| Cost | 0.01 USD, 6 turns |

The two asks were these:

1. Close the four issues, since they are delivered but still labelled
   `ready-for-agent`.
2. The PANEL realignment lists screens not built yet (PANEL-8.5, 8.6, 8.8). If you want
   them built, raise the budget first: "a 15–27-task build-in-waves run with per-task
   review would likely exceed that."

## What this does and does not show

On a real board, §1 (the frontier) and §4 (one message) hold. The run made no tracker
write and did not build an `Implemented` feature a second time.

**Real finding: stale labels.** All four `ready-for-agent` labels on klynt are stale.
Each one points to a feature that has already merged. This is `sweep-backlog`'s job, and
the run named it without being asked.

The build chain (§2: per-ticket `build-in-waves`, `inspect-change`, `land-branch`) did not
run. The board had no ticket that was approved and still unbuilt. Every approved
`tasks.md` in klynt belongs to a feature whose requirements are already `Implemented` or
`Shipped`, and CPLAN is the operator's own build in progress. The chain's evidence is
still the fixture runs in `deliver-issues/TESTS.md`.

To exercise the chain on klynt, an approved plan needs a `ready-for-agent` ticket. The
sandbox above can be reused for that run as it is.
