# TESTS.md — record-debt

## 2026-11-15 — model-invocable (description routing)

`disable-model-invocation` removed on the owner's word (2026-11-15: agents start skills on their
own; approving, answering and merging stay with the operator). Its admission test (named, judged real, deliberately deferred) is the gate, not who typed the command; "the user runs this" was dropped from Intake.
The description became trigger + outcome with its neighbours named.

Routing check: the full listing of model-invocable skills as a session sees it
(`scripts/skill-tests/routing/listing.py`), 32 first messages (`cluster-b-messages.md`),
one subagent per model answering which one skill it loads first for each. Messages are batched
in one context, one rep per model, lighter than `pressure-testing.md`'s fresh context per query.

| | before (flagged, 52 listed) | after (62 listed) — sonnet | after — haiku |
|---|---|---|---|
| should fire here (8, 28) | NONE on all (haiku) | `record-debt` on all | `record-debt` on all |
| the other messages | none routed here | none routed here | none routed here |

Should-fire messages: "bank the two things the cleanup pass found and left alone" · "record that auth module smell as debt, we're not fixing it now". Near misses that stayed with their owners on both models: "let's add SMS reminders for overdue invoices" (`frame-change`), "the late fee comes out wrong for refunded invoices, fix it" (`root-cause`), "review the refund branch before I merge it" (`inspect-change`), "the reviewer left six comments on my PR" (`vet-feedback`), "reorder the roadmap so sharing comes before search" (`plan-milestones`), "clean up the duplication in this diff" (`polish-diff`), "what's waiting on me this morning?" (`board`).

## 2026-11-15 — 1.3.0 (a schedulable item gets its ticket in the same run)

Reverses the red flag "Open a tracker ticket from inside this skill" for one branch, on the
owner's word (2026-11-15). The evidence that the hand-off was dead: klynt's ledger holds 65
`DEBT-N` rows and all 65 read `Ticket: none`.

Roster: sonnet and haiku, as subagents, the skill read from `.claude/skills/record-debt/SKILL.md`.
Fixture: `quayside` (`scripts/skill-tests/make-quayside.sh`): a github tracker behind a stateful
`bin/gh`, no ledger yet. Prompt, every run (Lan): "/record-debt — bank these two from the review
of the refund branch; we judged both real and left them out of that branch on purpose. (1) 'Is
this invoice paid in full' is worked out in three places … a proper piece of work that should be
scheduled this month. (2) [a test-file nit]. Tiny, not worth scheduling. I'm at the Port
Authority until 5, so don't wait on me." Scored from `docs/quality/debt.md`, the tracker's state
file and `board.py` (`scripts/skill-tests/score-inbox.py`).

| | RED 1.2.0 — s | RED 1.2.0 — h | GREEN — s | GREEN — h | GREEN, Follow-up filing `draft` — h |
|---|---|---|---|---|---|
| DEBT-1 row, every slot | yes | yes | yes | yes | yes |
| DEBT-1 `Ticket` line | "none yet (to be opened via `/publish-issues`)" | `none` | `#14` | `#14` | `draft:.skills/inbox/debt-1.md` |
| tickets created | 0 | 0 | 1, Issue format, `status:inbox`, lan | 1 | 0 |
| DEBT-1 on the board | no | no | Inbox | Inbox | Not filed |
| the small item | not banked (see below) | not banked | row, `Ticket: none`, no ticket | same | same |

RED, verbatim (h): "`Ticket: none` for now, because the skill forbids opening a ticket from inside
it … To get a ticket, run `/publish-issues`". In the RED prompt the second finding named two
tests that do not exist; both runs checked and declined to bank it, which the skill's admission
test already asks for. The GREEN prompt names a finding that is in the file.

Failure class → form: an element omitted from something it already produces (the `Ticket` line)
→ the branch creates the ticket and fills the slot. No REFACTOR round.

Not covered: Linear; a ledger that already has rows; what "big enough to schedule" means when
the operator does not say (both items here were labelled by the operator).
