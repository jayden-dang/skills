# TESTS.md — record-debt

## 2026-11-15 — 1.3.0 (a schedulable item gets its ticket in the same run)

Reverses the red flag "Open a tracker ticket from inside this skill" for one branch, on the
owner's word (2026-11-15). The evidence that the hand-off was dead: klynt's ledger holds 65
`DEBT-N` rows and all 65 read `Ticket: none`.

Roster: sonnet and haiku, as subagents, the skill read from `.claude/skills/record-debt/SKILL.md`.
Fixture: `quayside` (`.skills/fixtures/make-quayside.sh`): a github tracker behind a stateful
`bin/gh`, no ledger yet. Prompt, every run (Lan): "/record-debt — bank these two from the review
of the refund branch; we judged both real and left them out of that branch on purpose. (1) 'Is
this invoice paid in full' is worked out in three places … a proper piece of work that should be
scheduled this month. (2) [a test-file nit]. Tiny, not worth scheduling. I'm at the Port
Authority until 5, so don't wait on me." Scored from `docs/quality/debt.md`, the tracker's state
file and `board.py` (`.skills/fixtures/score-inbox.py`).

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
