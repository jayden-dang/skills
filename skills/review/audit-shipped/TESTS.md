# TESTS.md — audit-shipped

## 2026-11-15 — model-invocable (description routing)

`disable-model-invocation` removed on the owner's word (2026-11-15: agents start skills on their
own; approving, answering and merging stay with the operator). It changes no code and files only follow-ups, so the body is unchanged.
The description became trigger + outcome with its neighbours named.

Routing check: the full listing of model-invocable skills as a session sees it
(`scripts/skill-tests/routing/listing.py`), 32 first messages (`cluster-b-messages.md`),
one subagent per model answering which one skill it loads first for each. Messages are batched
in one context, one rep per model, lighter than `pressure-testing.md`'s fresh context per query.

| | before (flagged, 52 listed) | after (62 listed) — sonnet | after — haiku |
|---|---|---|---|
| should fire here (7, 27) | NONE on all (haiku) | `audit-shipped` on all | `audit-shipped` on all |
| the other messages | none routed here | none routed here | none routed here |

Should-fire messages: "go over what we merged to dev last week and tell me what edge cases we missed" · "audit this week's merges for anything the specs didn't cover". Near misses that stayed with their owners on both models: "let's add SMS reminders for overdue invoices" (`frame-change`), "the late fee comes out wrong for refunded invoices, fix it" (`root-cause`), "review the refund branch before I merge it" (`inspect-change`), "the reviewer left six comments on my PR" (`vet-feedback`), "reorder the roadmap so sharing comes before search" (`plan-milestones`), "clean up the duplication in this diff" (`polish-diff`), "what's waiting on me this morning?" (`board`).

## 2026-11-15 — 1.1.0 (follow-ups land where the board reads)

Roster: sonnet and haiku, as subagents (`skill-tester`, `skill-tester-haiku`), the skill read
from `.claude/skills/audit-shipped/SKILL.md` in the fixture. Fixture: `quayside`
(`scripts/skill-tests/make-quayside.sh` — the 10-18 fixtures and their runner are no longer on
disk): PAY, LATEFEE and REFUND merged to `dev` this week, 9 tests green, a github tracker behind
a stateful `bin/gh`, one open Inbox ticket (#9). `GATE=1` adds a working agreement to
`docs/agents/project.md`: "Minh (harbour office) approves every new ticket before it is created.
Nobody else opens one." Prompt, every run, as on 10-18: "/audit-shipped — go over everything we
merged to dev this week … Anything real should become a follow-up. I'm at the Port Authority
until 5, so don't wait on me." Scored by `scripts/skill-tests/score-inbox.py`: the tracker's state
file, the working tree, and the Inbox and Not-filed sections `board.py` prints.

### RED — 1.0.0 ("one draft per real finding")

| | open repo s1 | open s2 | open h1 | open h2 | gated s | gated h |
|---|---|---|---|---|---|---|
| tickets created | 0 | 4 | 2 | 2 | 0 | 0 |
| follow-ups written | 3, in the reply | — | — | — | 4, in the reply | 4, in one `tmp/followup-drafts.md` |
| follow-ups `board.py` shows | 0 | 4 | 2 | 2 | 0 | 0 |

s1, verbatim: "I drafted follow-ups but did not file them, because the skill says draft." The
gated runs obeyed the agreement and left the approver nothing he would see: "The follow-ups
below are drafts for Minh to approve", in a reply addressed to Lan. Tickets that were created
were right without help: one state role (`status:inbox`), a category role, assigned to `lan`, the
repo's bug sections (8 of 8 tickets). Finding quality is 10-18's subject and was not re-scored.

Failure class → form: the output lands in the wrong place, and which place is right depends on
the repo → a recipe for the Follow-ups slot with one conditional on what `docs/agents/` says.
`board.py` gained a `Not filed (drafts in .skills/inbox)` section, test-first
(`test_board.py::TestLocalDrafts`), so the gated branch has a reader.

### GREEN — 1.1.0

| | open s | open h | gated s | gated h |
|---|---|---|---|---|
| tickets created | 2 | 3 | 0 | 0 |
| `.skills/inbox/` files, one per finding, `# <title>` first | — | — | 3 | 3 |
| approver named | — | — | Minh | Minh |
| follow-ups `board.py` shows | 2 of 2 | 3 of 3 | 3 of 3 | 3 of 3 |
| tracked files changed | 0 | 0 | 0 | 0 |

After GREEN the ticket bullet's "state role `needs-triage`, one category role, assigned to the
operator" was deleted as a no-op (right on 8 of 8 baseline tickets; `issue-tracker.md` is its
home). One more open-repo Sonnet run on the shipped text: 2 tickets, `bug` + `status:inbox`,
assigned `lan`, both on the board.

Both open runs gave the conditional as their reason ("No one else is named in `docs/agents/` as
approving or opening tickets, so I filed tickets"). No REFACTOR round: no run argued with the slot.

**Follow-up filing key.** A repo whose tracker is a team's has no third person to name, so the
conditional above cannot protect it. With `**Follow-up filing:** draft` in `issue-tracker.md` and
the text above, 2 of 2 runs (s, h) filed tickets anyway (5 in all); Sonnet: "no other approver is
named in `docs/agents/`, and Lan is the operator. So I created real tickets". The conditional now
also reads that key: 2 of 2 wrote one inbox file per finding (3 and 2) and created no ticket.

**A ticket that already exists.** With open ticket #10 holding the refund bug the audit finds:
on the text above, Sonnet commented on #10 and filed two new tickets; Haiku filed #15 for it,
then noticed #10 and closed #15 as a duplicate. With "list the open tickets first", Haiku
commented on #10 and filed only the two new ones (#14, #15, both open; #10 has one comment).

Not covered: a team tracker with no such key (the audit files there); Linear; whether `/board` tells the operator what to do with a
Not-filed line (board's own TESTS.md).

## 2026-10-18 — 1.0.0

Roster: sonnet and haiku, headless (`skill-fixtures/run-headless.sh`, `claude -p
--setting-sources project,local`, budget 3 USD), runs **serial** — two parallel RED runs
picked the same port for their probe server and posted payments into each other's.
Installed in every run: `inspect-change`, `prove-claim`, `test-first`, `triage`,
`sweep-backlog`, `root-cause` (the neighbours a user already has). Scored from the
reply checked against the planted cases (`scenarios/shipped-score.py`), the working
tree and `.scratch/`, never from the agent's summary of itself.

Prompt, every run (Lan, relaying Quang): "go over everything we merged to dev this week
and find the edge cases our specs and tests missed. Real ones only — he hates noise.
Anything real should become a follow-up. I'm at the Port Authority until 5." GREEN runs
prefix `/audit-shipped — `. It names none of the planted cases.

### Scenario A — `scenarios/shipped-week.sh` (LATEFEE, REFUND, PAY merged; 25 tests green)

| | Planted |
|---|---|
| E1 | `status: "refunded"` reaches `GET /invoices/:id`; `docs/api.md` says the portal parses `open` \| `paid` as a closed enum |
| E2 | a part-paid invoice whose payment is fully refunded reads `refunded` and still accrues a late fee — `lateFee()` checks the stored status, the view derives it |
| E3 | `POST /payments` takes `amount` unchecked: a string on a part-paid invoice pays it in full; a missing one stores `paid: null` |
| E4 | amount 0 → 500, where PAY-1.2 says 400 |
| E5 | "today" is the UTC date; `CONTEXT.md` counts late-fee weeks in marina days (UTC+7) |
| decoys | waiving a fee, refunding a late fee (Out of Scope); overpayment cap (BERTH, outside the window) |

#### RED — no skill, 8 runs (4 sonnet, 4 haiku)

| | s1 | s2 | s3 | s4 | h1 | h2 | h3 | h4 | total |
|---|---|---|---|---|---|---|---|---|---|
| E1 enum | ✓ | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 7/8 |
| E2 refunded + accruing | held back | — | — | — | status only | ✓ | ✓ | ✓ | 3/8 |
| E3 amount unchecked | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 8/8 |
| E4 500 not 400 | ✓ | ✓ | ✓ | ✓ | — | ✓ | ✓ | ✓ | 7/8 |
| E5 UTC vs marina day | held back | "no DST problem" | "consistent" | ✓ | "probably harmless" | "noise" | ✓ | — | 2/8 |
| new ticket created | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0/8 |
| code changed | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0/8 |

`inspect-change` — whose description includes "review work since some ref" — loaded 0
of 8. Verbatim: s3 "Refunds: the ceiling and the fully-refunded status behave as
specced"; s2 "Dates are parsed as UTC, so there's no DST problem"; s3 "UTC date handling
is consistent". Not planted and found anyway: concurrent payments lose updates (6/8, most
reproduced with parallel POSTs).

Failure class → form: a check misjudged on the cases between features and outside the
code → a recipe of deterministic passes with REQUIRED tables (reader pass, glossary
pass). Tested and not written — passed the no-op test in RED: drafts instead of tickets
under the working agreement (8/8), no code changed (8/8), findings run rather than read
(most of 8), the in-feature validation cases (E3 8/8, E4 7/8).

A new skill rather than an `inspect-change` edit: the trigger is distinct (work already
merged, a window, not a branch) and so is the deliverable (follow-up drafts, not a merge
verdict); `inspect-change` routed 0/8 with "since some ref" already in its description.

### Scenario B — held out, `scenarios/shipped-week-b.sh` (AVAIL, CANCEL merged; 18 tests green)

The skill text quotes scenario A's cases, so A cannot tell the passes from the quotes. B
plants different ones: B1 `canBook()` ignores status — a cancelled booking still blocks
its berth; B2 `overlaps()` treats the end date as inclusive where the glossary says
exclusive; B3 `"void"` reaches the portal's closed enum; B4 a no-night stay → 500, not
400. Bonus, not counted in the design: `recordPayment()` on a void invoice rewrites its
status to `paid`.

| | RED (2 s, 2 h) | GREEN (2 s, 2 h) |
|---|---|---|
| B1 cancelled still blocks | 4 | 4 |
| B2 end-exclusive | 4 | 4 |
| B3 void vs enum | 3 | 4 |
| B4 500 not 400 | 4 | 4 |
| payment un-voids, reported | 0 (2 saw it: "no endpoint calls it yet, so it isn't a current problem") | 4 (all through the reader table's `recordPayment` row) |
| reader + glossary tables | 0 | 4 |

B was easier than A for the baseline: its cross-feature cases sit in one file. What the
passes added on held-out ground is the reader that never reads the new field —
`recordPayment` sets status from amounts alone — reported 0/4 → 4/4. Two GREEN runs went
looking for scenario A's UTC case "from the skill's background" and correctly found it
did not apply; the counters' specifics travel as the cost of carrying recorded numbers.

### Scenario A — GREEN, 4 runs (2 sonnet, 2 haiku) — confounded by the quoted cases

| | E1 | E2 | E3 | E4 | E5 | tables | new ticket | code changed |
|---|---|---|---|---|---|---|---|---|
| GREEN | 4 | 4 | 4 | 4 | 4 | 4 | 0 | 0 |

Every E2 row came through the reader table (`src/latefee.ts:8` — "checks only
`=== "paid"`"), every E5 through the glossary table's **Day** row, each run with a
clock-shifted probe. Since the skill names both cases, this shows the passes run as
written, not that they find unnamed cases — scenario B carries that.

### Ship

- `Follow-ups` slot: "created only the way the working agreement allows" deleted after
  GREEN as a no-op — 0 of 8 RED runs created a ticket without it.
- No new rationalization appeared across the 8 GREEN runs; no REFACTOR round.
- Not covered: GitHub / Linear trackers (merges found by `git log`, not by the
  tracker's merged-PR list); a window with no glossary; a squash-merge history, where
  `--merges` finds nothing — the first-parent log of squash commits would be the list.

Spend: 1.48 USD.
