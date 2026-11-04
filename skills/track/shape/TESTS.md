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

## 2026-11-03 — 1.4.0: the final review goes to `work`, the page shows the closed spec

**RED, the operator's own run.** NAVORI ROAD-9, 1.3.1, on the real repo. The page held 32 choice groups and 5,310 visible words, and its reply box had to be copied back. The audit found ten items, one of them high, and most were a citation or a label. They reached `work` only after the operator read them. The operator's whole answer: "fix the audit findings", then "approve", with no card ever picked. Their words: the review should tell `work` directly, the final page should hold only what is settled, and they should approve only at the last step, with nothing to copy.

**GREEN, Sonnet, fresh repo, no intervention.** About 45 minutes to the page.
- Order on disk: audit, `final-review.md`, then the page. The page names the commit, `0aad3bc`, and that is `HEAD`.
- Receipt: `missing: none`, 6 subagents, `research` ran; the conductor ran `brief-road` and `craft-page`.
- Final review: 13 items, 5 applied, 8 rejected, each with a reason. `interpret` reviewed what moved in 2 rounds. It closed a real gap: a requirement said one event per booking while the design collapsed duplicates.
- Page: 0 radio buttons, 0 checkboxes, 0 text boxes, 516 words before the first collapsed section, 1,606 in all, 4 items under Needs you, ending on "type approve".
- `approve` typed in the chat: three files `Approved` and committed. **The ticket stayed `shaping`.** Auto mode refused `work` the label swap as an external write, though an earlier run's `work` got through. The conductor then asked the operator how to proceed, with the peers still open. The fix moves the publish to the conductor, where the operator's word arrives directly.
- Shape check of that fix, Sonnet, same run, conductor resumed with the new step: it published, the read shows `ready-for-agent`, the peers closed, `/go #4` named. The label swap went through in the conductor session. Title and body stayed as they were, so this check does not cover replacing them.

**A weakness this run showed.** `work` rejected all 7 of the advisor's OPTIONAL cuts, so the session that wrote a requirement judged whether to remove it. Its reasons cite code or a standard, and one rejection corrected the advisor from a command it ran. But nothing was cut, and the largest item (`CALEX-5.2`, about 290 plan lines) only reached the operator because `work` chose to list it. One run on a small fixture does not say whether this is sound judgement or authors defending their text.

**The largest declined cut stays in view.** Same closed run, final review and report edited so `work` no longer lists `CALEX-5.2` itself. Prompt: write only the page's Needs you part. Sonnet, one run per arm. Without the rule: five items, `CALEX-5.2` and its 290 plan lines not among them. With it: item 1 names `CALEX-5.2` and Task 8, about 293 lines, says only the authors argued for keeping it, gives what reversing costs, and keeps a lean of its own. The operator still chooses nothing on the page; they see it and may say so.

Not covered: 1.4.0 on a real repo; 1.4.0's new approval step from a fresh start rather than a resumed session; replacing a ticket's title and body at publish; two final-review rounds with a new audit finding; a final-review item that cannot settle; a hard stop.


## 2026-11-03 — 1.5.0: --video, --en, --vi

Fixture: `tidegate` with a closed triad and a `RUN` holding what step 8 leaves, resumed at step 9 with the peers gone. Peers are
not exercised here.

**RED, on 1.4.0.**
- `--auto --video --vi`, Sonnet and Haiku: no film and an English page. "no skill defines this flag either. I did not guess it meant Vietnamese." (Sonnet).
- `--auto` typed in Vietnamese, no flag, Sonnet: a Vietnamese page, because the page followed "the language the operator writes to you in". The owner wants English unless asked.
- `--auto --vi`, Sonnet, charter and prompts only: it rewrote `interpret`'s prompt to "Companion language Vietnamese (--vi)". The owner wants that session in English.

**GREEN, on 1.5.0, scored from the files.**

| Run | Model | Film | Page |
|---|---|---|---|
| `--video --vi` | Sonnet | 56.0s, `vi`, PASS | Vietnamese, 369 words open, `<video>`, 9 seek links, 3 spec links, 2 collapsed, 0 controls, no other figure |
| `--video --vi` | Haiku | 58.5s, `vi`, PASS | Vietnamese, 331 words open, `<video>`, 9 seek links, 3 spec links, 2 collapsed, 0 controls, no other figure |
| Vietnamese command, no flag | Sonnet | none | English, 453 words open, 6 collapsed |
| `--vi`, peers' files | Sonnet | n/a | Charter and both prompts name neither Vietnamese nor `LANG`; "Companion language English" stands |

Both ticket comments stayed English and every spec file read `Draft`. The first draft asked for under 300 open words and neither
run reached it, since `Needs you` takes most of them. It now says 400, the measured figure.

**Not covered.** A whole `/shape --auto --video` through live tmux peers, about 45 minutes before the film. So `interpret` reading the
script before `voice.py` has never run: both conductors reported the peer gone and read the script themselves. A refused voice
call falling back to the full page. `--en` named explicitly. Rewriting the film after a plain-word change.

**After the owner's verdict on the film.** The film now explains and does not cover, so the thin page lists the IDs it leaves out (`out/uncited.json`) and keeps parts 4, 6, 7, 8 and 9 collapsed. This page form has not been through a run: it needs a film, and ElevenLabs was refusing calls over an unpaid invoice. Evidence for the film itself is in `make-video`'s `TESTS.md`.

## 1.6.0: `--project-style` (2026-11-04)

The owner reversed the rule that a film follows the project's design system: `make-video` keeps one look, and this flag asks for the project's. A shape check, one Haiku run reading `auto.md` for `--auto`, `--auto --video --vi` and `--auto --video --project-style`: film, language, look and spec language right on all three. Not run through live peers. The look itself is measured in `make-video`'s `TESTS.md`.

## 1.7.0: the spec sheet (2026-11-04)

The owner read Karpathy's ladder for reading model output (controlled language, then a diagram, then an HTML page, then a
3b1b-style explainer video) and its attached STE100 sheet: lettered panels in a ruled frame, a structure tree, annotated
sentences, tables, limit bars, a title block. They asked for that document beside every closed spec, film or not, with a step-through
of one example, kept in `RUN` and never committed. Fixture: `tidegate` with the closed REBOOK triad and a `RUN` holding what step 8
leaves, resumed at step 9 with the peers gone; under `--video` an 86-second explainer of the same spec already at `RUN/film.mp4`,
with its `out/scenes.json` and `out/uncited.json` (4 IDs left out). Every sheet rendered at 1440 wide and read by the scorer.

**RED, on 1.6.0, `--video`.**

| Model | Open words | Figures | Walk | IDs left out by the film |
|---|---|---|---|---|
| Sonnet | 315 | 0 | none | listed bare: "REBOOK-2.4, 3.2, 3.4, 4.2. The film explains; it does not cover." |
| Haiku | 322 | 0 | none | the same bare list |

Both followed the thin form exactly, so this is the text's shape and not a lapse: "Its primary figure is the film, so it draws no other."

**GREEN round 1, first draft, `--video`.** Both drew panels A to I, a map tree, a stepped walk and labelled rules, with every live ID.
Two faults from the renders, both now in the text:
- Labels unreadable. Haiku's map and plan had `viewBox` 640 to 880 wide drawn into a 520 to 630 px panel, so labels rendered at 7.2 to 8.5 px; Sonnet's two half-width figures at 6.0 and 6.6 px.
- Haiku's rule brackets were absolutely positioned and sat on the next line of the rule. Sonnet left the right third of row A empty.
Neither had looked at its own render. Sonnet 1,287 open words, Haiku 1,529, with Needs you items of 80 to 100 words.

**GREEN round 2, the text as shipped.**

| Run | Model | Open words | Figures, smallest label | Walk | Language |
|---|---|---|---|---|---|
| `--video --vi` | Haiku | 912 | 2, 11.8 px | 7 steps, Next changes the SVG and the sentence, 4 film links | English (see below) |
| no film | Sonnet | 1,258 | 2, read off the render | 7 steps, Next changes both | English |
| `--vi`, no film | Haiku | 875 | 3, read off the render | 8 steps | Vietnamese, IDs and rules verbatim |

All three: grid rows as written, no overlap or cut text in the render, 0 inputs, no remote fonts or scripts, the approve line last,
every spec file `Draft`, the sheet untracked. Each conductor rendered its sheet in headless Chrome before handing over. Each ID the film
left out has its meaning in panel C, D or E. The `--vi` Haiku map wrote IDs as `1.1` under a `REBOOK` root, so 2 of 14 never
appeared in full; the map now says "written in full". Not re-run after that word.

**`--video --vi` with a Vietnamese film, Haiku, after "written in full".** The round-2 `--video --vi` run wrote English because the
fixture handed it an English film, which a real run cannot produce. Rerun with a 92-second Vietnamese film and `language: vi` in the
script: a Vietnamese sheet (842 Vietnamese letters in the open part), 1,262 open words, 2 figures, the map writing all 14 IDs in full and
marking the 4 the film leaves out, each explained in C, D or E, 7 seek links, 0 inputs, approve line last, every file `Draft`. A copy
that presses Next six times on load renders step 7 of 7: the cancelled sailing in the warning color, Lan's offer `accepted`, Minh's
`no-seat`, a masked number on the staff list. It added two CSS fixes after its own render and did not render again.

**Not settled.** Every run found the same planted gap (final-review item 3 says applied, the files do
not) and put it under Needs you rather than fixing a spec file, which is right with the peers closed. Not covered: a live run through
peers, a refused film, the walk on a narrow screen, and whether the owner reads the sheet faster than the old page; only they can judge that.
Renders and scores: `.skills/SPECSHEET/` in the authoring checkout.
