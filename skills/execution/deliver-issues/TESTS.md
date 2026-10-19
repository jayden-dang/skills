# TESTS.md — deliver-issues

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
