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

## 2026-11-01 — the new `Issue format` seed, no edit

RED, 1.1.0 on the new seed, private specs (sonnet 1, haiku 1), step 1 only: 2/2 put the operator's words
verbatim under Problem, `Not decided yet` in the other sections, and set all four fields. No failure, so no
text was written for the create step.

## 2026-11-01 — the claim on a private roadmap (1.1.0 → 1.2.0)

**RED, 1.1.0 on the new seed, private roadmap** (haiku 1). The seed kept `ROAD-6` off the title, and the run recorded it in
`.skills/ROAD-6/tickets.md`, where `/board` would read `ROAD-6` as the feature code.

**GREEN, 1.2.0** (sonnet 1, haiku 1). 2/2 kept the title, wrote `1 road: ROAD-6` to `.skills/_pending-weekly-digest/tickets.md`,
gave ROAD-7 no ticket, and kept the swap to `status:shaping` and the frame comment.


## 1.3.0 — the road card (2026-11-05)

Design: `.skills/research/2026-11-05-agent-strengths-for-go.md`; owner's rulings in memory (card file per road, UI default `reuse`).
Fixture: `quay` (roadmap MILE-1 with ROAD-3 built and ROAD-4 unbuilt, vision, stub tracker with `issue create`). Prompt: "/idea The dock
crew get a text message the evening before a vessel arrives on their berth", then every answer up front, the operator about to board a
flight: 18:00, one message per berth, three examples, no replies or sign-up, `quay list` unchanged, "Which SMS provider and how retries
work: your call", "Ask me before anything that would send more than one message per berth per day", command line only.

**RED, 1.2.0** (Sonnet 1, Haiku 1). Both filed and framed tier 2 with 10 open questions. Neither added a roadmap item or a card. Sonnet's
body read "Outcome: Not decided yet", "Acceptance: Not decided yet", "Out of scope: Not decided yet" above the operator's three examples.
Neither kept "your call" apart from "ask me first"; Sonnet turned the second into open question 5.

**GREEN, 1.3.0.**
- Sonnet: ROAD-5 added with `— Card: [ROAD-5](roads/ROAD-5.md)`, title starts `ROAD-5`, card passes `check_card.py`, every answer in one slot, Delegated "Which SMS provider, and how retries work", Ask me the one cost rule.
- Haiku, first text: card and ROAD-5 made, but its eleven open questions went under Ask me, and the title lacked ROAD-5. Countered both.
- Haiku, after: 3 of 3 runs put only the operator's cost rule under Ask me; the last run's title starts `ROAD-5`.

## 1.4.0 — todos first (2026-11-05)

Fixtures: `quay` for /idea, /shape #4 and /shape #4 --auto (tmux replaced by a stub so the conductor stops after step 1); tidegate with an approved REBOOK triad and #4 ready for /go #4. Scored from `TaskCreate`/`TodoWrite` calls in the transcript.

RED: 0 of 7 runs made a list (/idea Sonnet+Haiku, /shape Sonnet+Haiku, /shape --auto Sonnet+Haiku, /go Sonnet through its first 8 tool calls), even though frame-change, which /idea runs, has its own todos rule.

GREEN, 1.4.0: Sonnet and Haiku each loaded `TaskCreate` and made the four steps by their 5th and 3rd tool calls.
