# TESTS.md — idea

## 2026-10-19 — 1.0.0

Fixture: `harbor-ledger` with overlays `latefee-plan` and `fmt-plan`, plus
`scenarios/gh-board.sh` (the board on a stateful `bin/gh`, never GitHub) and
`scenarios/gh-roles.sh`. `scenarios/wf-pre-open.sh` replaces the working agreement with
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

## 1.0.1 — no pointer to a jdk-repo page (2026-10-19)

The klynt dogfood ran `/idea` and reported that `docs/guide/workflow.md`, which the skill
named for states and owners, "doesn't exist in this checkout". That page lives in the jdk
repo, not in the repos that install the skill. The pointer now names
`docs/agents/triage-labels.md`, which `configure-repo` writes into every repo. Wording
only.

## 2026-10-30 — the ticket is the frame's claim (1.0.1 → 1.1.0)

Source: the klynt frame-change on parallel work. A frame is claimed by an assigned ticket. When
the frame mints roadmap items, the ticket carries on as the claim for the item the operator
names, and specify-behavior's claim check finds it by `ROAD-N` in the title.

**Harness.** `gh issue create` from test agents is denied by the harness classifier, even
against a stub. /idea is tracker-agnostic: it uses the ops in `docs/agents/issue-tracker.md`.
So the fixture declares an in-repo tracker CLI, `tools/tix` (JSON in `.tix/issues.json`), and
runs are scored from that file.

**RED, 1.0.1** (sonnet 2, haiku 2).
- Step 1: `/idea Learners should get a weekly digest of what they studied.`, operator about to
  fly, step 1 only. 2/2 filed #7 with `needs-triage` and `"assignees": []`.
- Step 3: #7 exists, assigned to jayden, and the confirmed close package reads: Tier 2, ROAD-251
  digest-content and ROAD-252 digest-delivery, and Jayden says "I'll carry on with the content
  one myself". 2/2 swapped to `shaping` and commented, but left the title unchanged. One run
  wrote "Jayden is taking this one" into the comment instead.

**Form.** An omitted element in steps the skill already runs. Step 1 gets "assign it to the
operator in the same create", and its Done-when names the assignee. Step 3 gets a WHEN
conditional that puts the named `ROAD-N` at the start of the title, with no ticket for the other
items. Both counters carry the recorded runs.

**GREEN, 1.1.0** (sonnet 2, haiku 2). Step 1: 2/2 created #7 with `["jayden"]`. Step 3: 2/2 set
the title to `ROAD-251 Weekly digest of what learners studied` and the label to `shaping` in one
edit, and opened no ticket for ROAD-252.

Not covered: the unnamed branch (frame mints items, operator names none, title left alone).
