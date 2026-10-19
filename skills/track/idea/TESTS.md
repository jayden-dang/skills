# TESTS.md — idea

## 2026-10-19 — 1.0.0

Fixture: `harbor-ledger` with overlays `latefee-plan` and `fmt-plan`, plus
`scenarios/gh-board.sh` (the board on a stateful `bin/gh`, never GitHub) and
`scenarios/gh-roles.sh`. `/tmp/wf-pre-open.sh` replaces the working agreement with
"Anyone — people and agents — may file, comment on, update status of, and link
tickets." The design is `docs/design/2026-10-19-closed-workflow.md` (W7); the workflow
page is `docs/guide/workflow.md`.

**RED (no skill; `frame-change` installed).** Prompt: "/frame-change — Vessel owners should
get an SMS when one of their invoices goes overdue. Get it onto the board so Quang sees it
at planning on Thursday."
- **Agreement gating new tickets** (Quang approves every new ticket): 0/2 filed a ticket.
  Both drafted it and named Quang as approver, which is correct.
- **Open agreement:** 3/3 filed a ticket, so filing is a no-op. One haiku labelled it
  `needs-info` and `status:shaping` at once, and nothing recorded the frame on the ticket.

**GREEN (1.0.0).** Prompt: "/idea Vessel owners should get an SMS …". 2 haiku and 1 sonnet,
open agreement.
- Filed with `needs-triage`: 3/3.
- `frame-change` ran and the tier was stated (tier 2): 3/3.
- Swapped to `status:shaping` as the only state role: 3/3.
- Frame comment with the tier and numbered open questions: 3/3.

Not covered: tier 0, which should go straight to Ready.
