# TESTS.md — go

## 2026-10-19 — 1.0.0

Fixture: `harbor-ledger` with overlays `latefee-plan` and `fmt-plan`, plus
`scenarios/gh-board.sh` (the board on a stateful `bin/gh`, never GitHub) and
`scenarios/gh-roles.sh`. `scenarios/wf-pre-open.sh` replaces the working agreement with
"Anyone — people and agents — may file, comment on, update status of, and link
tickets." The design is `docs/design/2026-10-19-closed-workflow.md` (W7); the workflow
page is `docs/guide/workflow.md`.

**RED (`deliver-issues` 1.1.0, user-invoked).** Prompt: "/deliver-issues #23 — just this one
today". 1 haiku built only #23, so the scope is a no-op. In that run #23 got
`in-review` and `Closes #23` but no `building` claim at the start. `/go` exists because
the owner chose five short commands (design decision 3). A user-invoked skill cannot be
invoked, so `deliver-issues` dropped `disable-model-invocation` (2.0.0).

**GREEN (1.0.0, with `deliver-issues` 2.0.0).** Prompt: "/go #23 — just this one today."
1 haiku.
- Only #23 was built: yes.
- Claimed with `building` and an assignee: yes.
- Moved to `in-review`: yes.
- PR carries `Closes #23`: yes.

## 1.0.1 — no pointer to a jdk-repo page (2026-10-19)

The klynt dogfood ran `/idea` and reported that `docs/guide/workflow.md`, which the skill
named for states and owners, "doesn't exist in this checkout". That page lives in the jdk
repo, not in the repos that install the skill. The pointer now names
`docs/agents/triage-labels.md`, which `configure-repo` writes into every repo. Wording
only.

## 1.1.0 — todos first (2026-11-05)

Fixtures: `quay` for /idea, /shape #4 and /shape #4 --auto (tmux replaced by a stub so the conductor stops after step 1); tidegate with an approved REBOOK triad and #4 ready for /go #4. Scored from `TaskCreate`/`TodoWrite` calls in the transcript.

RED: 0 of 7 runs made a list (/idea Sonnet+Haiku, /shape Sonnet+Haiku, /shape --auto Sonnet+Haiku, /go Sonnet through its first 8 tool calls), even though frame-change, which /idea runs, has its own todos rule.

GREEN, 1.1.0: Sonnet and Haiku each made the list by their 3rd tool call (Sonnet 2 items: the ticket and the message; Haiku 9).
