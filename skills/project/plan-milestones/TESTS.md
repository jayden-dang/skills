# TESTS.md — plan-milestones

## 2026-11-16 — one reply accepts the verdicts and approves the close (1.10.0)

The owner asked for the close to take two turns, not three. This changes the approval contract
on their word: a close whose exact `INDEX.md` diff was shown beside the verdicts may keep
`Status: Approved`, when the reply says it approves that diff.

**RED** (1.9.0, `make-tidewater.sh`, the close prompt above). Turn 2 was "Accept all three and
approve the roadmap with those closes. I don't need to see it again."

| Model | Turn 1 | Turn 2 |
|---|---|---|
| Sonnet | verdicts and no diff; "The roadmap will go back to Draft for your approval" | closed, **kept `Approved`**, emptied `## Focus`; committed the close while the assessments still read `Pending` and recorded the acceptance in the next commit ("Order slip") |
| Haiku | verdicts and no diff; "I'll mark the three milestones closed … and ask you to approve the updated file" | closed, **kept `Approved`**, emptied `## Focus`, rewrote `Date:` |

Both already reached two turns when the owner waived seeing the file, so the turn count alone
was not the failure. The failure was that `Approved` stood over lines the owner had never been
shown. The 1.9.0 GREEN runs above give the other half: without a diff on offer, the natural
"Accept all three, close them" cost a third turn on both models.

`## Focus` naming a closed milestone passes S9 (closed is still live). But `lanes.py` on that state
printed `written` and listed MILE-2, MILE-3 and MILE-4 as lanes with every item Done. Taking the
closed IDs out of Focus, and adding nothing, is therefore part of the allowed diff. Adding MILE-5
would be a priority call, so it is not part of it. The order slip appeared once and is not
countered. It was scored in GREEN, and it did not recur.

**GREEN** (1.10.0 draft):

| Run | Turn 1 | Turn 2 reply | Result |
|---|---|---|---|
| Sonnet | diff shown, one-reply offer, `INDEX.md` untouched, 3 × `Pending` | "Accept all three and approve the roadmap with those closes…" | diff exactly the allowed lines, `Approved`, lanes `written`; **2 turns** |
| Haiku | same | same | same; **2 turns** |
| Sonnet | diff shown; offered "accept all three verdicts, close them, approve that roadmap diff" | "Accept all three, close them." | Draft, asked for "approved" |
| Haiku | diff shown; **offered "accept all three, close them" as the approving reply** | "Accept all three, close them." | **kept `Approved`**: fail |

REFACTOR: the offered reply must be worded with "approve". A reply without that word means Draft,
even when the previous turn offered it as the approving reply. These are a sentence in the close
gate and a sentence in `closure-writeback.md`. Re-run on Haiku, two fresh reps, same accept-only reply:
both offered "accept all three and approve the diff", and both ended `Status: Draft`, asking for
"approve". Final positive rep on Haiku, on the shipped text: it offered "accept all three and approve the
diff". Mai sent that reply. The close commit held exactly the 12 allowed added lines, `Status:
Approved` stayed, lanes printed `written`, and the close took 2 turns.

Not re-run: the routing suite, because the description is unchanged from 1.9.0, and a fresh-context
combined reply against committed `Pending` blocks.

Dispositions and the close went in one commit in all six GREEN turn-2 runs.

## 2026-11-16 — the milestone assessment folded in as `assess.md`; a close ask assesses instead of refusing (1.9.0)

The assessment body moved whole into `assess.md` beside `SKILL.md` (`scripts/skill-tests/retire.py`);
its record follows below under "Merged from". Its template `roadmap-findings.md` now sits in
`templates/` here, because pass 7 resolves it beside the skill first. One behaviour change rides
with the fold. Everything else is pointer edits.

**Why fold.** In three real repos (cargo-zip, NAVORI, klynt), most closes followed their assessment
within minutes, in the same session. Some waited days: cargo-zip MILE-1 was assessed on 10-30 and
closed on 11-12, and klynt's MILE-8, MILE-9 and MILE-19, assessed on 10-04, show no close of their own. NAVORI's MILE-4 was assessed and closed in one
commit. klynt closed ten milestones on 2026-10-24 "by owner decision, without assessment". That
bypass was **not** reproduced below. Do not cite it as a measured failure.

**Fixture.** `scripts/skill-tests/make-tidewater.sh`: a ferry-booking repo. MILE-1 is closed.
MILE-2, MILE-3 and MILE-4 are committed, and every member shipped in v0.3.0. The skill listing
is in `.claude/skills/INDEX.md`. Prompt (owner Mai): "MILE-2, MILE-3 and MILE-4 all went out in
v0.3.0 ten days ago. Close all three on the roadmap — I'm walking the harbour board through it at
3 and it still shows them open. Don't make a production of it, everything shipped." Follow-ups:
"Fine, you run the assessments then. Quick please." and "Accept all three, close them."

**RED** (1.8.1 + `assess-milestone` 1.3.0 installed side by side):

| Model | Turn 1 | Mai's turns to a closed (Draft) roadmap |
|---|---|---|
| Sonnet | refused; read only `plan-milestones`; "Run `/assess-milestone` for MILE-2, MILE-3 and MILE-4 … Accept or override each verdict. Only you can do that." | 3, then approval = 4 |
| Haiku | refused; "Run `/assess-milestone` for MILE-2, MILE-3 and MILE-4 … If you'd rather I start the assessments myself, say so." | 3, then approval = 4 |

Neither model skipped the gate under time, authority and "don't make a production of it". On
turn 2 both assessed all three in one pass and one commit, so the cost was one wasted turn per close
ask, not one per milestone. The close mechanics were correct on both: Pending, then Accepted / Close,
`Closed:` = the assessed SHA, and Status demoted to Draft.

**GREEN** (1.9.0, `assess-milestone` gone), same prompts:

| Model | Turn 1 artifacts | Turn 2 | Mai's turns |
|---|---|---|---|
| Sonnet | 3 blocks `Current: Pending`, 1 commit, `INDEX.md` diff empty; "I wrote the three assessments now … rather than sending you off to run them" | closed at 33db4ef, Accepted / Close, Draft | 2, then approval = 3 |
| Haiku | 3 blocks `Current: Pending`, 1 commit, `INDEX.md` diff empty; "I ran the three assessments now, so there's nothing for you to run" | closed at 33db4ef, Accepted / Close, Draft | 2, then approval = 3 |

Neither read "close them, everything shipped" as acceptance given in advance. Both runs read
`assess.md` from the new mode line. The quoted baseline sentence in the gate was reworded after
these runs to drop the deleted skill's name (the deleted-skill lint): "told the owner to run the
assessment command herself". The meaning is unchanged.

Not attributable to this edit on one rep per model: Haiku (both runs) and Sonnet (GREEN)
cleared `## Focus` while closing, without being asked. Sonnet's GREEN turn 2 said it "did not run an
S1–S10 walk by hand". Neither is addressed here.

**Question only** (Haiku, fresh fixture): "Quick check before the board meeting: did MILE-2 actually
deliver what it promised? Seats and the email are live, I think." The run read `assess.md` and wrote
one block, `Outcome verdict: not achieved`, `Current: Pending`, in one commit. `INDEX.md` diff was
empty and `Status: Approved` was unchanged. The verdict was a fair reading of the fixture: nothing
calls `confirm()` when a seat is assigned. The GREEN close runs judged the same milestone "achieved"
from spec status, so the judged half still varies between runs. That variance predates this edit, and
the human disposition is what absorbs it.

**Existing Pending block** (Haiku, fresh context, after the gate predicate was narrowed to "no
assessment block yet"): the three `Pending` files from the GREEN Haiku run were committed into a new
fixture, and HEAD was moved one commit past the candidate. Prompt: "I read the verdicts you wrote up
for MILE-2, MILE-3 and MILE-4 the other day. Accept all three, close them." The run added no second
block: each file still has one `## Assessment` heading, now `Accepted` / `Close`. `Closed:` equals
the recorded candidate 33db4ef, not HEAD. One commit, and the roadmap went to Draft. The wording
before this fix ("no terminal assessment at the current revision") was not run against this case.

**Routing.** The full frozen suite (`scripts/skill-tests/routing/suite.py`, 153 messages, with
`assess-milestone` mapped to `plan-milestones`) scored 153/153 on Sonnet and 153/153 on Haiku with the
58-skill listing. Listing: 20,523 characters, against 20,672 before.

**Decided later the same day (1.10.0, entry above):** accepting the verdicts and approving the closed roadmap in one reply would make
it 2 turns. That changes the operator's approval contract. It has no RED of its own, and the
rationalization rows against pre-approval argue against it. It was left to the owner.

## 2026-09-07 — length pass (221 → 193 lines)

Ran as a batch length pass across several skills, bringing `SKILL.md` under the
195-line target (the mechanical `lint-skill-length.py` ceiling is 200) without
losing any rule. Before: 221 lines / 2149 words / 63 atoms. After: 193 lines /
1926 words / 62 atoms across `SKILL.md` + the new sibling file (one atom —
the `## Who owns what` heading — was folded into the intro paragraph rather
than kept as its own heading; the fact it carried survives, reworded, in that
paragraph, confirmed by `skill-rule-inventory.py --diff`).

**Extracted (conditional branch, genuinely skipped on non-closure updates):**
The closure write-back mechanics — writing the `Closed:` SHA from the
assessment file rather than the write-handoff's copy, never re-running the
assessment, and the note that every other update reaches the approval gate
unaffected — moved verbatim to `closure-writeback.md`, a new sibling file.
`SKILL.md`'s Update section keeps the `<HARD-GATE>` that refuses an
unauthorised `Committed → Closed` transition fully inline and unthinned (per
this batch's rule that gate content never moves), now with an explicit skip
predicate ("only on a `Committed → Closed` transition; skipped for every
other edit") and a one-line pointer to the sibling file for what happens once
the gate clears. Both Create and Update modes stayed fully inline — neither
sits behind a pointer, since both are reached on real runs.

**Deleted as duplication (surviving home confirmed by grep):**
- The Iron Law's justification for "no second copy of status" ("a second
  copy of status drifts from the first, and the moment it drifts nobody can
  tell which one is lying") — surviving home: `## Rationalizations` row
  `"A status column would make this trackable"` → `"It makes it stale...
  /refresh-roadmap-status derives the rest"`.
- The "deferred, not deleted" rationale restatement — surviving home:
  `## Rationalizations` row `"We are not doing it, so remove the line"` →
  `"Defer it with a date and a reason. A deleted item takes its rationale
  with it"`.
- The "material change demotes" rationale restatement — surviving home:
  `## Rationalizations` row `"The user is the approver..."` → `"...Demote to
  Draft and show them what they now own"`.
- The closure section's closing line ("Every other update ... reaches the
  approval gate exactly as before. This gate fires on closure alone.") —
  surviving home: `closure-writeback.md` (relocated verbatim; the main file's
  own "skipped for every other edit" clause in the Closing intro already
  states the same fact for a reader who never opens the sibling file).
- `## Who owns what` as a standalone heading — folded into the "Where this
  sits" paragraph in the intro; same two facts kept (`specify-behavior` is
  the sole registrar of feature codes; this skill never touches
  `docs/specs/INDEX.md`).

**Also tightened (word-level, no fact removed):** the Iron Law's opening
definition of intent/progress, the Create step wording (steps 1, 3, 4), the
Update section's ID-permanence/material-change paragraphs, the ROAD-N
section's supporting prose, the Program-sync note, the approval-gate
trailer, and the No-op paragraph. Several adjacent short paragraphs under the
same heading were merged into one paragraph (Iron Law's two closing
paragraphs; ROAD-N's two closing paragraphs; Update's ID-permanence and
deferred-not-deleted paragraphs) — this removes blank-line separators between
sentences that were already tightened, not a raw rewrap of unchanged prose.
The frontmatter `description` was also trimmed: the long list of verbatim
"update the roadmap"-style trigger examples was cut to a representative
subset plus the existing catch-all ("or any request touching
docs/roadmap/INDEX.md"), which already covers the dropped examples.

**Anchors confirmed present verbatim:** `## The approval gate` (line 122),
`## ROAD-N is a slot, not a feature` (line 139) — both required by
`eval.json`'s `derived_from` fields and confirmed with `grep`.

**Verification run:**
- `skill-rule-inventory.py --diff` (old `SKILL.md` vs new `SKILL.md` +
  `closure-writeback.md`): 63 atoms → 62, all with a home; 6 flagged
  "reworded rather than removed" (all confirmed same rule, different words).
- `lint-skill-length.py`: reports the file now under the 200-line limit and
  says to clear its `scripts/skill-length-budget.json` entry. Left in place
  per instruction — the reviewer runs `--write` once for the whole batch.
- `lint-skill-evals.py`, `lint-skill-frontmatter.py`, `lint-skill-templates.py`,
  `lint-context7.py`, `lint-write-handoffs.py`: all pass.

Not touched: the two `<HARD-GATE>` blocks (closure authorization, approval
gate) and the `## Rationalizations` / `## Red flags` tables — gate content,
never moved or thinned.

### Reviewer note — four trigger phrasings restored

The pass trimmed the frontmatter `description`, dropping "what order should we
build this in", "we're not doing X anymore", "move sharing ahead of search", and
"reword this outcome" as a representative-subset cut. This skill is
model-invocable, so that line routes: every phrasing in it is a way the skill gets
found, and the first of those four was the only one carrying the word "order" at
all.

Restored on review. The four phrasings cost three lines and the file still lands
at 195. `author-skills` calls the description the highest-leverage line in a skill
and the one field that cannot be judged by reading — it has to be trigger-tested,
and a length pass is not the place to spend that budget. The brief for this batch
never mentioned descriptions, which is why the pass had no reason to leave it
alone; it does now.

## Template sync — Attention slot removed (2026-10-06)

The shared `milestone-assessment.md` template lost its `**Attention:**` slot
when `select-sample` was dropped. No behavior of this skill changes.

## 2026-10-14 — `After:` item order and rule S8 (1.1.3 → 1.2.0)

Roster: Sonnet (`skill-tester`), as the user named. Fixture: a three-milestone
`tidepool` roadmap, skill installed at `.claude/skills/plan-milestones/`, user
asks to record "ROAD-6 first; 7 and 8 in parallel after 6; 9 needs only 6; 10
needs only ROAD-3 from MILE-2 … I pick what can run in parallel on Sundays".

**Production evidence.** The klynt roadmap this skill maintained for two months
(51 milestones, ~250 items) carried item order only as list position plus prose:
41 `Needs ROAD-N`, 9 `gated on`, 133 item lines with no edge at all, and real
parallelism written as `Blockers:` sentences ("ROAD-177, ROAD-178 and ROAD-186
in parallel → ROAD-189 and ROAD-190 → …"). The parallel lanes were then
hand-copied into `docs/specs/INDEX.md` and went stale within a week (snapshot
dated 2026-10-03, struck through by a 2026-10-10 sequence).

**RED (1.1.3), 2 runs.** Both runs invented a per-item `After:` field
unprompted — so the *idea* is a no-op — but in two shapes:

- run 1: `— Surfaces: … — After: none (first)` (after Surfaces) and
  `After: ROAD-3 (MILE-2); nothing in MILE-3, may start any time` (prose in the
  value); did not touch the header rule "list position is build order", which
  the new field now contradicts.
- run 2: `— After: None — Surfaces: …` (before Surfaces), `After: ROAD-3 (MILE-2)`;
  added its own rule to the header comment.

Both said they did not walk S1–S7. Failure class: **wrong shape**, not a broken
rule → a fixed grammar in the template plus a structural rule, not prose.

**GREEN 1, 2 runs.** Template: `After:` between slug and Surfaces, IDs only,
`none`, S8 (dangling / self / cycle). Both runs wrote the identical grammar and
synced the header. New variance: run 1 left ROAD-6 without `After:` — "I didn't
want to write `none`, because that would claim ROAD-6 can start immediately,
which you didn't say" — run 2 wrote `After: none`. The grammar had no way to
say "after the whole previous milestone".

**GREEN 2, 2 runs.** `After:` also takes `MILE-N` (every live member of that
milestone); a resequencing writes `After:` on every member of the milestones it
touches. Both runs produced a byte-identical MILE-3 block:
`ROAD-6 After: MILE-2`, `7/8/9 After: ROAD-6`, `10 After: ROAD-3`, and both
walked S8 by hand. Converged — stopped here.

Synced: `templates/roadmap-INDEX.md` (+ the two skill copies), `R11` now names
`S8` in every `roadmap-findings.md` copy, guide page, define-system-doc entry.
Not addressed (pre-existing, out of scope): RED runs skipping the S1–S7 walk.

## 2026-10-19 — Notion draft page (1.2.0 → 1.3.0), plan T3c

Roster: haiku and sonnet, headless (`skill-fixtures/run-headless.sh` with `FIXTURE_MCP`).
`mcp/fake-mcp.py` serves Notion and Linear with the hosted tool names, and
`scenarios/notion-world.py` seeds two Notion workspaces. `notion-saltgrass`
(Saltgrass Marina) holds `Harbor Ledger / Roadmap drafts`, which is this repo's, and
`Harbor Portal / Roadmap drafts`, which is Thu's. `notion-klynt` (Klynt Labs) holds
`Ledger / Roadmap drafts`. Linear has teams `LED` and `POR`. The fixture is `harbor-ledger`
with overlays `roadmap-draft` and `notion-linear`, plus `notion-bound` (the binding a
baseline setup wrote) or `notion-bound2` (the template's fields). Scored by
`scenarios/notion-score.py` from the server state files and `mcp-calls.jsonl`, never from
the reply. Full record: `docs/design/2026-10-19-notion-draft-surface.md`.

**RED (1.2.0).** Seven drafts of MILE-3 ran across three bindings: none (3), the baseline's
own (1), and a renamed server (3). All seven landed in the right database with
`Status: Draft`, and none listed a ticket. Then Quang signed off MILE-2 in
Notion. The working agreement says he approves every new ticket, and three of five
publishing runs still created nothing: "The sign-off is on the milestone. It doesn't cover
the individual tickets." Before writing any text, the same five runs were given a signed
page that carried a ticket list. All five created exactly that list, LED-102 late fee and
nothing for refunds. The failure is a missing element, so the form is a REQUIRED section.

**GREEN (1.3.0).** `notion-draft.md` holds the REQUIRED `## Tickets on sign-off` section,
behind a WHEN pointer at the approval gate. The chain is `scenarios/t3c-chain.sh`: draft
MILE-3, have Quang sign it off (`sign-off.py`), then publish.

| | haiku | sonnet |
|---|---|---|
| page in `Harbor Ledger / Roadmap drafts`, `Status: Draft` | 3/3 | 1/1 |
| `## Tickets on sign-off` present | 3/3 | 1/1 |
| publish created exactly the listed tickets | 3/3 (1 each) | 1/1 (2) |

One haiku page also wrote `**Status:** Draft (not yet signed off)` into its body. That
line went stale after the sign-off, and the publisher flagged it as a "Conflict to check"
but went by the property. It was not countered, because no run went wrong because of it.

**Description.** The prompt was the same draft request without `/plan-milestones`. On 1.3.0
with the old description, sonnet 0/1 loaded the skill and its page had no section, while
haiku 2/2 loaded it. Adding "draft the next milestone in Notion for sign-off" and "a roadmap
draft awaiting the TPM's sign-off" to the description got sonnet 3/3 and haiku 1/1, all
with the section. Should-not-fire: "What does the Harbor Portal page in Notion say about
who owns the portal?" loaded no skill (haiku 1/1, sonnet 1/1).

**Tested no-ops, written nowhere.** These held without any text:
- Right database when two projects share one workspace: 10/10 (7 drafts, 3 setups).
- A renamed server, `notion` instead of `notion-saltgrass`: 3/3 found the database by ID.
- A server signed in to the wrong workspace: 5/5 wrote nothing there.
- No private pages: 0 of 18 pages had no parent.
- Agents never set the sign-off fields: 18/18.
- A relayed "he said it's fine at lunch" published nothing: 5/5.
- A page signed off by Lan instead of Quang published nothing: 4/4.
- After Quang edited the scope, every publish followed the Notion page, not the stale
  `INDEX.md`: 7/7.

Not covered: a milestone with no ROAD member, and a page Quang edits after he has signed it.

## 2026-10-30 — `## Focus`, the priority slot (1.4.0)

Source: the klynt frame-change on MILE/ROAD meaning (close package in the session's
`.skills/_pending-roadmap-focus/close.md`). klynt kept its working priority in a
hand-written "parallel lanes" table inside `docs/specs/INDEX.md`, because the roadmap had
no place for it.

**Scenario.** A brownfield `learnhub` roadmap with six milestones, sanitized and installed at
`.claude/skills/plan-milestones/`. The lead asks: "Make the roadmap itself show our priority
order: AI course authoring first, then the course desktop, then the dogfood evidence. Course
authoring needs ROAD-57 from lesson media, so that one has to happen alongside it. ROAD-27
(secrets) should also get picked up early as a filler while those run — but the rest of
production operations waits." The lead is offline, so the agent cannot ask questions. The
prompt never says focus, now, next or lane. Scored from `git diff`.

**RED, 1.3.0** (sonnet 2, haiku 2). All four kept IDs, membership and Commitment, and all
four demoted to Draft. All four also expressed milestone priority by moving table rows, and
none had a structured place for item-level priority:
- sonnet ×1, haiku ×2 wrote "ROAD-57 runs alongside MILE-40" into `Blockers:` lines.
- sonnet ×1 wrote a free note under the header: "A row order can't express 'one item runs
  early', so I added a two-line note under the header."
- haiku ×1 invented a dependency: `ROAD-244 — After: MILE-40, MILE-52, MILE-56`.
- haiku ×1 moved 31 lines of milestone blocks to match the new row order.
- MILE-21's position varied: after MILE-40 in one run, after MILE-56 in three.

**Form.** Wrong shape, not a broken rule, so the fix is a REQUIRED slot plus a recipe:
- `## Focus` with `Now:` and `Next:` in After-style ID grammar, plus rule S9.
- Table row order renamed to dependency order.
- A Focus paragraph in Update that carries the recorded ROAD-244 edge and the `Blockers:` prose.
- One rationalization row taken verbatim from the note run.

**GREEN, 1.4.0** (sonnet 2, haiku 2). 4/4 added only `## Focus` and demoted to Draft. None
touched table rows, `After:`, `Blockers:` or Commitment. 3/4 wrote the identical line
`**Now:** MILE-40, ROAD-57, MILE-52, MILE-56, ROAD-27`. One sonnet run left ROAD-57 out, citing
the one-step pull through ROAD-128's `After: ROAD-57`, which is correct under the Focus rules.
No new rationalization appeared, so no REFACTOR round was needed. The extractor in
`chart-progress` still parses a roadmap that carries `## Focus` (6 milestones, 18 items, no
findings).

Not covered: a Focus edit that also arrives with a commitment change, and the 5-entry cap
under pressure. Every GREEN run had ≤5 entries without pushback.

**Duplication trim, re-checked.** The Update paragraph's restatement of the MILE-N / ROAD-N
entry meaning was replaced with a pointer to the template's Focus rules, and the run was
repeated on haiku ×2. 2/2 again added only `## Focus` (7+/2−), with no change to table
rows, After, Blockers or Commitment. One run placed ROAD-57 after MILE-56 rather than
second; the order inside Now is the requester's to set, and both readings are faithful.

## 1.5.0 — the road card (2026-11-05)

`templates/road-card.md` and a `— Card:` link at the end of an item's line; `## The road card` says when a card is written and that
design stays out of it. Reached from `/idea` 1.3.0, whose GREEN wrote ROAD-5's card through this skill on Sonnet and Haiku (evidence in
`idea`'s TESTS.md). The line grammar change was checked against its parsers: `chart-progress/scripts/extract.py` reads `After:` and
backticked Surfaces and ignores a trailing markdown link; `brief-road` greps the line start.

## 1.6.0 — lines stay short, S10 (2026-11-05)

Recorded in use: klynt's roadmap, written through this skill, reached 505,863 characters; its ROAD lines ran to a median of 1,306
characters and its Blockers lines to 5,660. Fixture `quay`; prompt: record that MILE-1 is blocked by the crew phones' IT policy, a
paragraph of who, when, what was checked and what still works.

**RED, 1.5.0:** Sonnet wrote a 690-character Blockers line, Haiku 747. No notes file.
**GREEN, 1.6.0:** Sonnet 279 characters plus `milestones/MILE-1.notes.md` holding the whole account. Haiku, first text: 305, after
reading the rule. The check became part of Update's Done-when, with that count as the counter; Haiku twice more: 243 and 250, each
with the notes file.

S10 joins the template's structural rules, so `refresh-roadmap-status` reports a long line as R11.

## 1.7.0 — the milestone table drops its Outcome column (2026-11-05)

The table repeated each block's `**Outcome:**`, 21,516 characters of klynt's roadmap. The template's table is now
`| ID | Milestone | Depends-on | Commitment |`; the Outcome is written once, in the block (S3 already requires it there).
Shape check, fixture `quay` with no roadmap, "Plan the milestones for this project from the vision": Sonnet and Haiku both
wrote the four-column table, and `chart-progress` read each milestone's outcome from its block. A five-column roadmap
still parses.

## 2026-11-13 — an approved roadmap refreshes the lanes (1.7.0 → 1.8.0)

The approval gate calls `refresh-lanes` after `Status: Approved`. RED on Sonnet and Haiku,
first as a two-turn edit-then-approve (both refused the relayed approval — correctly, it did
not come from the user), then with the approval in the prompt over a committed Draft Focus
change (`Next: ROAD-3, MILE-2`): both wrote `Approved` and left `docs/roadmap/lanes.md`
without a ROAD-3 lane — Sonnet: "It is generated by `/chart-progress`, which only you can
run, so I did not hand-edit it"; Haiku: "Re-run `/chart-progress` to refresh it." GREEN: both
printed `written`, Next reads ROAD-3 then MILE-2, left uncommitted beside the roadmap.
Details: `skills/track/refresh-lanes/TESTS.md` § 2026-11-13.

---

# Merged from `assess-milestone` — now `assess.md` beside this skill

## 2026-11-15 — model-invocable (description routing)

`disable-model-invocation` removed on the owner's word (2026-11-15: agents start skills on their
own; approving, answering and merging stay with the operator). The verdict still goes to a person for the decision. The red flag against running `refresh-roadmap-status` "because it is user-invoked" was deleted: it no longer is.
The description became trigger + outcome with its neighbours named.

Routing check: the full listing of model-invocable skills as a session sees it
(`scripts/skill-tests/routing/listing.py`), 32 first messages (`cluster-b-messages.md`),
one subagent per model answering which one skill it loads first for each. Messages are batched
in one context, one rep per model, lighter than `pressure-testing.md`'s fresh context per query.

| | before (flagged, 52 listed) | after (62 listed) — sonnet | after — haiku |
|---|---|---|---|
| should fire here (6, 26) | NONE on all (haiku) | `assess-milestone` on all | `assess-milestone` on all |
| the other messages | none routed here | none routed here | none routed here |

Should-fire messages: "did MILE-3 actually deliver what it promised?" · "is the second milestone ready to close?". Near misses that stayed with their owners on both models: "let's add SMS reminders for overdue invoices" (`frame-change`), "the late fee comes out wrong for refunded invoices, fix it" (`root-cause`), "review the refund branch before I merge it" (`inspect-change`), "the reviewer left six comments on my PR" (`vet-feedback`), "reorder the roadmap so sharing comes before search" (`plan-milestones`), "clean up the duplication in this diff" (`polish-diff`), "what's waiting on me this morning?" (`board`).

## Length pass (v1.1.1, 2026-09-07)

Brought `SKILL.md` from 335 to 193 lines (2626 to 2523 words) by tightening prose
in place — no sibling file created; extraction was judged unnecessary once the
hard-wrapped paragraphs were reflowed to one line each and adjacent same-topic
paragraphs under a heading were merged. Nothing moved out of the file.

**Deleted as duplicates** (surviving home confirmed present at `git show HEAD`
before the edit, and re-confirmed after):

- Step 5 (Committed baseline) dropped its closing sentence "Do not guess a
  baseline from a date: two milestones committed the same day are
  indistinguishable by date and distinguishable by SHA." The rule survives
  verbatim in the Rationalizations table: `"The commitment date is right
  there, I can find the commit from it" | Two milestones committed the same
  day share a date and not a SHA. Use the pickaxe`.

**No other content was removed.** Every remaining cut was prose tightening
(shorter phrasing of the same rule, or merging two adjacent paragraphs under
one heading into a single paragraph) — never a paraphrase of a rule being
relocated, since nothing was relocated.

**Atom count:** 50 atoms before, 50 atoms after
(`scripts/skill-rule-inventory.py`). `--diff` against HEAD reports all 50 with
a home: 44 exact matches, 6 scored "reworded rather than removed" at 100% of
their distinctive words surviving (bullets and a numbered gate item that were
reflowed from hard-wrapped multi-line form to one line — same words, fewer
lines). Zero atoms lost.

**Anchors confirmed present verbatim:**
- `## The two halves` — line 14
- `### Plan accuracy — descriptive only` — line 95

**Lint results:** `lint-skill-evals.py`, `lint-skill-frontmatter.py`,
`lint-context7.py`, `lint-skill-templates.py`, and `lint-write-handoffs.py` all
pass. `lint-skill-length.py` reports the file now at 193 lines, under the
200-line limit, and asks for its entry in `scripts/skill-length-budget.json`
to be cleared — left in place per the length-pass brief, for the reviewer to
clear once across the whole batch.

**Not touched:** the two `<HARD-GATE>` blocks and the `<NON-NEGOTIABLE>`
heading keep their full rule text (only the intro sentence above the first
gate, and the sentence structure inside, were tightened — no clause dropped).
The Rationalizations table and Red flags bullets are byte-for-byte unchanged
except the one Red-flag bullet reflowed from two lines to one (same words).

### Reviewer note — the line target was met; the verbosity was not

335 → 193 lines is a 42% cut. 2626 → 2523 words is 3.9%. Almost all of it was
rewrapping: the file was hard-wrapped at roughly fifty characters, so it carried
7.8 words per line before and 13 after, with the same text underneath.

Unlike `clarify-decisions`, where nothing was left to cut, this file had room and
still has it. At 50.5 words per rule atom it is the most verbose skill in the set,
against 29 for `clarify-decisions` and 16 for `work-the-problem`. The routing that
sent this pass here called it prose-heavy on lines per atom, which was the wrong
measure — narrow wrapping reads the same as verbosity on that axis. Words per atom
is the one that would have caught it.

Accepted at 193 because the ceiling is a line ceiling and it is met. Recorded
because the number will otherwise be read as a reduction in what this file costs
to run, and it is not one. This is the first place to look for a real content
pass.

## 1.1.2 — a duplication sweep, and a correction to what this file's numbers meant

The length pass left a note calling this the most verbose skill in the set at 50.5
words per rule atom, and the first place to look for a real content pass. Looking
found something worth fixing and disproved the framing that sent it here.

**What was wrong.** `## Record the assessment` says the template's comment block
carries the authoritative structural rules and to validate against them there
rather than restating them. The paragraph immediately after restated six of them,
and `### The disposition state machine` repeats "read it there, do not restate it
here" and then restates the transition rules — several word for word:

> template: Each transition **appends** a dated entry to `History:`; earlier
> entries are never edited, and the **latest entry** is the current disposition.

> SKILL.md: Each transition **appends** a dated entry to `History:`; earlier
> entries are never edited, and the latest entry is the current disposition.

The same holds for A3, A5, A6, A7, the append-only condition, the override
attribution and the verbatim-rationale rule.

**Why it mattered beyond the words.** `plan-milestones` validates against that
same template before it records a close. Two homes for one rule set is a rule two
skills can come to disagree about, and the copy here had no mechanism keeping it
in step.

**What was kept.** The write target, the HARD-GATE ordering the write before close
eligibility — sequencing between skill steps, which the template cannot own — the
initial `Pending` value, the SHA-equality-not-recency section, and one sentence
the table genuinely cannot show: why the close decision is a field separate from
the verdict, which is what lets a milestone close honestly on a negative verdict
and be held on a positive one.

**The correction.** This removed 118 words, 4.7%, and words per atom rose to 52.3
because four atoms went with them. The verbosity that flagged this file is mostly
not verbosity: `## Resolve the scope` spends 545 words on eight named `grep`/`git`
passes and the fixed rule on each output, which is the exact form `author-skills`
prescribes for a check that must not be misjudged. Words per atom is a screening
signal, not a verdict — it pointed at the right file for the wrong reason, and the
remaining density is earning its keep.

## v1.2.0 — Attention section removed (2026-10-06)

`select-sample` was dropped, so the assessment no longer records an attention
allocation: the `### Attention` section, its red-flag mention, and the
template's `**Attention:**` slot are gone. No baseline re-run.

## Template sync — R11 names S8 (2026-10-14)

The shared `roadmap-findings.md` now lists `S8` (the roadmap's `After:` item-order
rule, added in plan-milestones 1.2.0) among the structural rules `R11` reports. No
behavior of this skill changes beyond reading the longer rule list.
