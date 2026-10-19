# TESTS.md — shape

## 2026-10-19 — 1.0.0

Fixture: `harbor-ledger` with overlays `latefee-plan` and `fmt-plan`, plus
`scenarios/gh-board.sh` (the board on a stateful `bin/gh`, never GitHub) and
`scenarios/gh-roles.sh`. `/tmp/wf-pre-open.sh` replaces the working agreement with
"Anyone — people and agents — may file, comment on, update status of, and link
tickets." The design is `docs/design/2026-10-19-closed-workflow.md` (W7); the workflow
page is `docs/guide/workflow.md`.

#24 ("Statement data for one vessel and month") is labelled `ready-for-agent` and has no
spec. **The RED is in `plan-tasks` 1.9.0's TESTS.md.** Publishing onto an existing ticket
left two state roles in 2/3 runs. That fix lives in `plan-tasks`, and this command routes
to it.

**GREEN (1.0.0).** Prompt: "/shape #24 — I'm at the Port Authority until 5; leave me
whatever needs my approval." 2 haiku.
- `shaping` became the only state role: 2/2.
- Framed as tier 2, provisional, and stopped for Lan's answers before any requirements
  were written: 2/2.
- A comment on #24 says what waits and on whom: 2/2. Verbatim (h1): "Shape drafted for
  #24: waiting on Lan Pham (approval of the frame below)."

Not covered: the resume path (`/shape #24` after approval through design and plan), and
tier 1 (`root-cause`).
