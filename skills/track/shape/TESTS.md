# TESTS.md — shape

## 2026-10-19 — 1.0.0

Fixture: `harbor-ledger` with overlays `latefee-plan` and `fmt-plan`, plus
`scenarios/gh-board.sh` (the board on a stateful `bin/gh`, never GitHub) and
`scenarios/gh-roles.sh`. `scenarios/wf-pre-open.sh` replaces the working agreement with
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

## 1.0.1 — no pointer to a jdk-repo page (2026-10-19)

The klynt dogfood ran `/idea` and reported that `docs/guide/workflow.md`, which the skill
named for states and owners, "doesn't exist in this checkout". That page lives in the jdk
repo, not in the repos that install the skill. The pointer now names
`docs/agents/triage-labels.md`, which `configure-repo` writes into every repo. Wording
only.

## 1.1.0 — a tier-1 fix leaves Shaping ready for `/go` (2026-10-19), W10

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

Prompt: "/shape #28 — If the cause is nights() rejecting same-day stays, I accept it. For
the fix: a same-day stay counts as one night, and multi-night stays must keep counting as
they do now — I approve a mini-spec saying exactly that as you draft it."

**RED (1.0.1).** 0/3 left a ticket `/go` could take:
- haiku h1 recorded the approval but kept #28 in Shaping;
- haiku h2 made it Ready with no `Requirements covered:` line;
- sonnet kept the mini-spec as Draft and waited for an approval it had been given.

**GREEN (1.1.0).** Step 3 gains a tier-1 branch. An up-front approval counts when the
drafted text matches it, and the approval is quoted. `Requirements covered: <fix>,
<guard>` goes into the body, and `shaping` is swapped for `ready-for-agent` in one edit.
- Ready with `Requirements covered:`: 3/3.
- The IDs are defined, with a `SHALL CONTINUE TO` guard among them: 3/3. Two wrote into
  `berth-booking/requirements.md`. One haiku created `docs/specs/2026-10-19-same-day-stay/`
  and left it uncommitted.

Not covered: that uncommitted spec directory. `root-cause` says the mini-spec goes into
the owning feature's `requirements.md`.

## 2026-11-01 — the tier-1 line follows reach (1.1.0 → 1.2.0)

Design: `docs/design/2026-11-01-issue-format.md`. Fixture: a generated repo with an in-repo tracker CLI, the
new `Issue format` seed, and an approved tier-1 fix in `docs/specs/fixes.md`.

**RED, 1.1.0, private specs** (sonnet 1, haiku 1). 2/2 kept the IDs off the ticket, as the seed says, and
wrote only `#3` to `.skills/EXPORT/tickets.md`. "`/go` may not recognise it as a tier 1 fix." Nothing
recorded the covered IDs, so `/board` and `/go` could not resolve the fix.

**GREEN, 1.2.0.** Private, sonnet 1 and haiku 1: 2/2 wrote `covers: EXPORT-1.1, EXPORT-1.2` on the ticket's
line and no ID on the tracker, and `board.py` prints `eligible, tier-1 fix` from that line. Shared, haiku
1: `Requirements covered:` as the last body line. The swap to `ready-for-agent` held in all three.


## 2026-11-03 — 1.3.0: `--auto`

Asked for by the operator: the whole spec with nobody at the keyboard, by two sessions that check each other, then
one page to review it on. Interpret's picks and an outside advisor stay advisory; only the operator approves.

**RED, a real run.** NAVORI ROAD-9, Sonnet 5.5, two tmux sessions under a hand-written charter, a third session
watching. It reached `tasks.md` in about 40 minutes with no skill edit. From artifacts and transcripts:
- `work` called only `specify-behavior`, `design-solution`, `plan-tasks`. No `clarify-decisions`, no `load-subgraph`,
  no `research`, 0 subagents. Its report listed two of the skips and not the third.
- Two silent stops ("Connection lost mid-response", "Your computer went to sleep mid-response"), about 14 minutes dead. Neither recovered alone.
- `scan.md:16` wrote `~/.codex/hooks.json` as absent; the file was six weeks old. Neither session looked.
- `HOOKS-4.4` froze interpret's own pick into a SHALL with no label, and interpret approved it.
- `specify-behavior`'s claim created a public issue. `rounds.md` timestamps were invented. Files read `Approved` before the operator had seen them.
- The operator's verdict on its `report.md`: they needed to review it easily, see what it touches, and see what the report looks like after a build.

**RED, current text.** Prompt `/shape #4 --auto`, generated marina repo, interactive in tmux, auto mode.
- Sonnet: stopped at requirements. "`--auto` doesn't waive that per-story yes." No peers, no design, no tasks.
- Haiku: called only `shape`. "I did not run the frame-change interview or the scan subagent." No peers, no design, no tasks.

**Advisor, one run per arm, Sonnet, on the ROAD-9 spec.** Persona (user, BA, PO): 30k tokens, skimmed the design, cited
little, contradicted itself on Story 7. Fixed task walk plus deletion test: 42k tokens, cited evidence, sized three
cuts, one false claim about `HOOKS-5.4`. Each found one gap the other did not. Neither found a large overbuild, and
all three cuts traced to documents the operator had approved. The operator kept all three. Shipped: fixed steps, once, no loop, conductor checks every claim.

**GREEN round 1, Sonnet.** Text said "with this session's permission mode". The conductor could not know it, guessed `default`,
and the peer sat 26 minutes on a prompt to read its charter. The conductor stopped and asked rather than answering the prompt. Fix: always `auto`.

**GREEN round 2, Sonnet, fresh repo, no intervention.** About 45 minutes to a finished page.
- Receipt, `work`: `ran: frame-change, load-subgraph, clarify-decisions, research, specify-behavior, design-solution, plan-tasks, audit-trace`, `subagents: 6`, `missing: none`.
- `research` ran on its own for the `.ics` format. Log times are real clock times.
- Three files `Status: Draft`, `Execution-mode: unset`, five docs-only commits, nothing pushed, one ticket, state `shaping`, one comment saying what waits on whom.
- The page has all ten parts, 12 radio buttons, one figure, the receipt verbatim, a copyable reply.
- The audit found two real problems the sessions had not raised: two criteria edited after approval, and the seeded `scripts/check.sh` ending in `tail`, so its exit code is always 0.
- A change sent as the operator's reply: the conductor said it was not approval, kept the files `Draft`, and passed the change to `work`, which re-sent it for review.

**`skill_receipt.py`.** Tests in `scripts/test_skill_receipt.py`, watched red first, 6/6 green. On the real ROAD-9 sessions it reports `missing: clarify-decisions, load-subgraph; subagents below 1`.

## 2026-11-03 — 1.3.1: what the rest of the runs found

**Sonnet, the operator's reply.** A change: the conductor kept the files `Draft` and did not read it as approval; `work` applied it, `interpret` re-reviewed, the audit reran and found one more gap (a `9999-12-31` date raises `OverflowError`), and the page was rewritten. Then "Approved": the three files read `Approved`, the catalog row too, the ticket reads `ready-for-agent`, the peers closed, and the conductor named `/go #4`.

**Haiku conductor, through to a page** (it started before the `brief-road` step existed). All ten parts, 11 choices, one figure. The receipt worked as the gate it is: it failed on `missing: clarify-decisions`, `work` ran it, and it passed with 7 subagents. Five defects, all in this text:
- No `--model` in the launch line: both peers ran on the machine's Opus 5.5 default.
- "write outside" fired a hard stop on Python's `.pyc` cache under `~/Library/Caches/com.apple.python`, before the tasks gate closed. The peers disagreed on whether it counted.
- `{conductor}` was filled with an invented name, `shape-4-conductor`.
- It asked the operator, three times, whether to stop another run's sessions it saw in `ListAgents`.
- `RUN/audit.md` was never written; the findings went straight onto the page.

Fixes: `--model sonnet` in the launch line, the hard stop now reads "change a config or data file", `{conductor}` comes from `ListAgents`, other sessions are not part of the run, and step 7 has a Done when.

**GREEN, shape check, fresh repos.**
- Blocked road (`After: ROAD-3` is `In-progress`), Sonnet 1, Haiku 1: both called `brief-road`, stopped before any worktree or session, said what it waits on. 2/2 against the RED above.
- Ready road, Haiku conductor: both peers on Sonnet 5.5, charter names the conductor `keelford`. Stopped by hand once the peers were up.

**Timing.** About 45 minutes on Sonnet and over 60 on Haiku with Opus peers, for a one-command feature. `plan-tasks` running the whole plan in a scratch copy took about 15 of those. Not measured: which step could go.

Not covered: the "config or data file" wording through a full run; a hard stop that should fire; a real repo; Haiku conductor with Sonnet peers through to a page; trust dialog handling (every run here had its folder trusted by hand). If a conductor is killed, its `caffeinate` lives up to its 6-hour limit.
