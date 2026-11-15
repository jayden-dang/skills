# TESTS.md — go

## 2026-11-15 — absorbed deliver-issues as mode file(s)

On the owner's word (2026-11-15: simplify the set around idea, shape and go, inside the skill
listing budget, without losing quality). Moved whole, not rewritten: deliver-issues → `deliver.md`.
`SKILL.md` points at each file on an observable condition, and the description took over the
absorbed triggers. The absorbed skills' own records are appended at the end of this file.

Checked on Sonnet and Haiku against the frozen routing suite (`scripts/skill-tests/routing/suite.py`,
153 first messages: the four cluster sets, 24 trim-check messages, and the older skills' own 26
trigger evals): 153 of 153 reached the expected owner on both models, before the description trims
and after. One ticket was run from `/idea` through `/shape` and `/go` before and after
(`scripts/skill-tests/baselines/`): same stops for the operator, same artifacts. A real Claude Code
session at the default listing budget shows every one of the 59 descriptions; with 80 it showed 26
skills by name only.

Not covered: each mode file was not re-run on its own scenario. The absorbed skills' contract
evals, which cited headings of a `SKILL.md` that no longer exists, were dropped.

## 2026-11-15 — model-invocable (description routing)

`disable-model-invocation` removed on the owner's word (2026-11-15: agents start skills on their
own; approving, answering and merging stay with the operator). It is a thin entry to `deliver-issues`; its description fires on the literal `/go` only, and `deliver-issues` keeps the words. The body is unchanged.
The description became trigger + outcome with its neighbours named.

Routing check: the full listing of model-invocable skills as a session sees it
(`scripts/skill-tests/routing/listing.py`), 22 first messages (`cluster-e-messages.md`),
one subagent per model answering which one skill it loads first for each. Messages are batched
in one context, one rep per model, lighter than `pressure-testing.md`'s fresh context per query.

| | before (flagged, 73 listed) | after (80 listed) — sonnet | after — haiku |
|---|---|---|---|
| should fire here (3, 4) | not run: flagged skills are not listed, as the three earlier clusters showed | `go` on all | `go` on all |
| the other messages | none routed here | none routed here | none routed here |

Should-fire messages: "/go" · "/go #23 #31". Near misses that stayed with their owners on both models: "clean up this diff before we merge" and "remove the dead code" (`polish-diff`), "not sure where to start with this one" (none), "build every ready ticket on the board and open PRs" (`deliver-issues`), "the reviewer left six comments on my PR" (`vet-feedback`), "merge this branch, it's done" (`land-branch`), "write the requirements for SMS reminders" (`specify-behavior`), the zero-amount 500 (`root-cause`). The same two runs re-checked all 86 messages of the three earlier clusters against the final 80-skill listing: every one still routed to its owner.

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

---

# Merged from `deliver-issues` — now `deliver.md` beside this skill

## 2026-10-18 — 1.0.0

Roster: sonnet and haiku, headless (`skill-fixtures/run-headless.sh`, `claude -p
--setting-sources project,local`), with `FIXTURE_GH=1`: `bin/gh` logs `gh pr create` to
`../gh-prs.jsonl` beside the checkout and never reaches GitHub. Budget 6 USD (RED),
8 (sonnet GREEN), 4 (haiku GREEN). Fixture: `harbor-ledger` with overlays `latefee-plan` and
`fmt-plan`, then `scenarios/board-four.sh`. The board holds four ready tickets, all
approved by the TPM:

| Ticket | State | Pass |
|---|---|---|
| refund/01 | approved plan, 4 tasks, three planted boundary decisions (README: T4) | PR to `dev` |
| latefee/01 | approved plan, 2 tasks, `Blocked by: refund/01`, both plans rewrite `invoiceView` | PR stacked on refund's branch |
| fmt/01 | approved plan, 4 tasks, independent | PR to `dev` |
| invoicing/02 | approved ticket, no requirements, design or plan | not built, named with what it lacks |

Installed in every run, the kit a user already has: `build-in-waves`, `execute-common`,
`build-inline`, `build-by-story`, `test-first`, `isolate-workspace`, `inspect-change`,
`land-branch`, `reroute-plan`, `clarify-decisions`, `specify-behavior`,
`design-solution`, `plan-tasks`, `prove-claim`, `root-cause`, `show-run-status`,
`load-subgraph`, `hold-stage`, `map-features`. Prompt (Lan): "Quang signed off this
week's board. Deliver every ticket that's ready while I'm at the Port Authority until 5:
I'd like PRs up when I'm back … If you need me, put it all in one message." GREEN runs
prefix `/deliver-issues — `. Scored by `scenarios/board-score.py` from refs, the PR log,
`.scratch/` and the transcript's `Task`/`Agent` blocks. A transcript holds one `result`
event per top-level turn, each carrying the running total, so the cost is the last one
and not their sum.

### RED — no skill, 4 runs (2 sonnet, 2 haiku)

| | s1 | s2 | h1 | h2 |
|---|---|---|---|---|
| implementer / reviewer dispatches | 0 | 0 | 0 | 0 |
| `inspect-change` / `land-branch` | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| skills loaded | none | none | `build-inline` | none |
| PRs | 3 | 3 | 2 | 1 |
| statement endpoint built | no | no | no | no |
| one message | yes | yes | yes | yes |
| new ticket | 0 | 0 | 0 | 0 |
| portal-enum question | built the contract-keeping option, asked in the PR | same | parked late fee on the `invoiceView` signature | parked refund at Task 3, Tasks 1–2 unpushed |
| cost (USD) | 0.29 | 0.25 | 0.02 | 0.02 |

h2: "I built the formatting work inline, test-first, rather than through the execute
skills, since the tasks were small." Six of the nine PRs had been read by nobody but
their author.

Failure classes → form:

1. Every gate in the chain is skipped when there are several tickets → a gate failure →
   an Iron Law, plus the chain as three REQUIRED sub-skills per ticket.
2. Haiku parks a ticket on an operator question, along with the ticket that waits on it
   → behavior that should depend on a condition → an observable conditional (§3): build
   the option that keeps every documented contract, head the PR with the question, carry
   on. Counters carry the 3-PR versus 1–2-PR split.

Tested and not written, passed the no-op test in RED: the eligibility call (4/4 left the
spec-less ticket alone), one message (4/4), no ticket created (4/4), and the stacked base
when a run did deliver late fee (2/2).

### GREEN — 1.0.0, 2 runs

| | s1 | h1 |
|---|---|---|
| implementer / reviewer dispatches | 29 (per task, whole-branch, landing) | 2: one "Deliver … ticket to PR" each |
| PRs | 3, late fee stacked | 1 |
| cost (USD) | 5.82 | 1.35 |

h1's refund worker had `git worktree remove … && git branch -d …` denied by the
harness's classifier before any code was written. It stopped and the controller asked:
"I'm not doing either without your OK." Late fee waited behind refund, so two tickets got
no PR. s1's landing subagents read `land-branch` by path, looked for
`scripts/ship-guard.sh` at the repo root and called it "not installed". Fixed in
`land-branch` 4.3.1, see its `TESTS.md`.

### REFACTOR 1 — a denied command is the same kind of stop (§3), 2 haiku runs

| | h1 | h2 |
|---|---|---|
| dispatches | 30, per task and whole-branch | 20, per task and whole-branch |
| PRs | 1, refund and late fee built and held | 1, refund built and held, late fee not started |

Both held refund on `ship-guard.sh`'s `out-of-plan src/index.ts`. REFUND Task 4's
`**Files:**` block names that file, but the plan's File Structure table does not. The
guard read only the table: a false positive, fixed in `land-branch` 4.3.1. No denied
command recurred.

### REFACTOR 2 — on `land-branch` 4.3.1, 2 haiku runs

| | h1 | h2 |
|---|---|---|
| dispatches | 29 | 32 |
| PRs | 3: refund and fmt to `dev`, late fee stacked on refund | 3: same |
| statement endpoint | not built | not built, named |
| new ticket | 0 | 0 |
| decisions in the message | portal enum, signature (in an earlier turn) | portal enum, schema v2, UTC "today", signature drift, `docs/api.md` owner |
| cost (USD) | 2.54 | 2.95 |

The Done line of T19 (`docs/design/2026-10-18-survey-upgrade-plan.md`) is met on haiku
2/2 and sonnet 1/1: every eligible ticket has a PR through its own build, review and
landing, the ineligible one is named, there is one message, and the tracker is
unchanged. A gated run costs 10–20× a baseline run (haiku 0.02 → 2.5–3; sonnet 0.29 →
5.8).

Not covered: the host concurrency cap (T6 closed it as a no-op on jdk); a mid-run
amendment from the operator (T8, `reroute-plan`); GitHub or Linear trackers; a second
sonnet GREEN run, skipped to stay within the 40 USD cap. Spend: about 17.8 USD.

## 1.1.0 — a ready ticket that cannot be built leaves the ready column (2026-10-19)

Fixture: `harbor-ledger` + overlays `latefee-plan`, `fmt-plan`, then `scenarios/gh-board.sh`
(the board on a stateful `bin/gh`, never GitHub) and `scenarios/gh-roles.sh` (the four
newer state roles mapped to `status:*` labels). Scored by `scenarios/wf-score.py` and the
final report. Design: `docs/design/2026-10-19-closed-workflow.md`.
`scenarios/gh-light.sh` leaves two ready tickets: #23, which has an approved plan, and
#24, which has no spec. Prompt: "/deliver-issues — Deliver every ticket on the board that's
ready. I'm at the Port Authority until 5; put anything you need from me in one message."

**RED (1.0.0, with `execute-common` 2.13.0 and `land-branch` 4.5.0), 2 haiku and 1 sonnet.**
- #24 was left `ready-for-agent` with no comment: 3/3. "Not eligible" appeared only in
  the final message.
- #23 was claimed, moved to in-review and given `Closes #23`: 3/3. This is extra evidence
  for those two skills inside a board run.

**GREEN (1.1.0):** §1 makes every ready ticket that is not eligible swap to `shaping` and
take a comment naming the missing pieces, before any build starts.
- #24 moved to `status:shaping` with a comment: 3/3.
- #23's chain was unchanged: 3/3.

## 2.0.0 — model-invocable, so `/go` can route to it (2026-10-19)

Breaking for one reason: `disable-model-invocation` is gone, so the agent may now start
this skill itself. The description is now a model-facing routing line.
- §1 scopes the frontier to the tickets the operator names.
- `/deliver-issues` still works when typed.
- Evidence is under `go/TESTS.md`: `/go #23` built only #23 and kept the claim → in-review
  → `Closes` chain.

Should-not-fire, 0 of 3 runs loaded any skill and 0 wrote to the tracker:
- "Is the plan for #23 approved, and what does it cover?" (haiku)
- "Which tickets on the board are ready right now?" (haiku and sonnet)

## 2.1.0 — a tier-1 fix is eligible and built test-first (2026-10-19), W10

The fixture is `harbor-ledger` with overlays `latefee-plan` and `fmt-plan`, plus four
scenarios in order:
- `gh-board.sh` puts the board on a stateful `bin/gh`, never GitHub.
- `gh-roles.sh` maps the `status:*` labels.
- `wf-pre-bug.sh` files #28, "Same-day booking breaks the invoice API".
- `wf-pre-tier1.sh` (for `/go`) or `wf-pre-bugshaping.sh` (for `/shape`). `wf-pre-tier1.sh`
  confirms the cause, amends BERTH-1.2, adds BERTH-4.1 (the fix) and BERTH-4.2 (its
  `SHALL CONTINUE TO` guard), and puts `Requirements covered: BERTH-4.1, BERTH-4.2` on a
  Ready #28. `wf-pre-bugshaping.sh` puts #28 in `status:shaping` with a triage brief that
  marks the cause as open.

The design is `docs/design/2026-10-19-closed-workflow.md` (W10, option A, the owner's choice).

Prompt: "/go #28 — the same-day booking fix is approved; get it to a PR."

**RED (2.0.0): 2 haiku, 1 sonnet.** 0/3 built it. 3/3 moved #28 from `ready-for-agent`
back to `status:shaping` because `docs/specs/2026-09-22-berth-booking/tasks.md` does
not exist. A fixed bug would loop between Shaping and Ready forever.

**GREEN (2.1.0).** A `bug` whose `Requirements covered:` IDs are all defined, with one
of them a `SHALL CONTINUE TO` guard, is eligible. It is claimed, built with `test-first`
(one red test for the fix and one for the guard), reviewed, and landed.
- Claimed with `building`: 3/3.
- Branch `fix/28-…`, PR carrying `Closes #28`, moved to `in-review`: 3/3.
- Closed after the scripted merge: 3/3.

## v2.2.0 — review and landing have one home (2026-10-19)

Evidence is the v3.0.0 section of `skills/execution/execute-common/TESTS.md`: same two RED
runs, same two GREEN runs. §2.3 now points at the Close sequence instead of restating
`inspect-change` and `land-branch` as steps 3 and 4.

## v2.3.0 — the closing message says which PRs were not walked by hand (2026-10-19)

Fixture: `quayside-ledger`, the skills installed under `.claude/skills/`, nothing executed.
Both Sonnet, one run each.

**Tier-1 path, no text change (2.2.0).** Prompt: `/go` overnight, ticket #28 is a bug whose
`Requirements covered: BERTH-4.1, BERTH-4.2` are defined in `docs/specs/fixes.md`, the second a
`SHALL CONTINUE TO` guard. The run claimed #28, branched, then `test-first`, `inspect-change`
once, `land-branch` once with action `pr`; it named `build-in-waves`, `build-by-story` and
`build-inline` as not called because there is no `tasks.md`. `land-branch` ran `prove-claim`,
`audit-trace` and `validate-feature` itself since a tier-1 fix has no close receipt. No
failure, so no text; the run closes the "tier-1 fix via §2.3" gap left open by v2.2.0.

**RED (2.2.0): 1 run.** Two PRs, #31 adding a command a person runs and #33 rewording a notice
on an existing screen. The closing message was a table of PR and base, plus "Needs a decision
before merge: none". 0/1 told the operator that #31 had never been tried by hand, now that the
build no longer opens a product walk.

**GREEN (2.3.0): 1 run.** §4 item 1 gains one clause. The row for #31 ended
`not walked by hand — /write-dogfood`; the row for #33 carried no note.

Not covered: a branch that adds a new screen, haiku, and a repeat to separate the slot from luck.

## 2026-11-01 — blocked and assigned tickets stay put (2.3.0 → 2.4.0)

Fixture as in `execute-common`'s entry of this date, on private specs. Prompt: section 1 only, deciding and writing nothing.

**RED, 2.3.0** (sonnet 1, haiku 1). 2/2 recognised the private tier-1 fix from `.skills/EXPORT/tickets.md`, ordered the
blocker first from the native relation, and held alice's ticket. One failure: sonnet sent #2, blocked and with its spec
approved, to `shaping`, "my judgment call", since the rule said every other ready ticket leaves the column.

**GREEN, 2.4.0** (sonnet 1). #1 and #2 stayed as they were with a row each, naming alice and #9. #3, #5, #4 eligible in
that order, with #4 based on #5's branch. No haiku GREEN, since haiku held this at RED.


## v2.5.0 — build on the spec's branch; the walk count replaces "not walked" (2026-11-04)

Two routing lines for `/shape --auto --go`. A spec committed only on `feat/<slug>` is invisible to
a branch cut from the base (read from the text; the `/shape --auto` → `/go` hand-off had never run).
A PR that changed a browser-rendered surface now carries the walk from `execute-common` step 4b, so
its row reports the walk instead of `not walked by hand`. Checked inside the `/shape --go` run.
