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
