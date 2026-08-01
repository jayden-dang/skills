---
name: run-product-walkthrough
description: >-
  Use when a review-product-flow test guide already exists and its cases must be executed
  rather than handed to a human — the agent-driven pass over every case in the
  guide against the running app in a real browser, judging both what the screen
  shows and what the backend actually stored. Produces an evidence-backed run
  file carrying a pass / fail / blocked verdict per case ID, and a guide left
  fully accounted for. Triggers on running or resuming a half-finished test
  guide, working a review-product-flow file end to end, or testing every case in the browser
  and fixing what breaks. Not for authoring the guide (`review-product-flow`) or writing
  committed e2e specs (`validate-ui`).
---

# Run Product Walkthrough

Execute an existing review-product-flow guide against the **product app** in a real browser.
The deliverable is the **run file** — every case ID accounted for with quoted
screen evidence and, when the case touches server-owned state, a server-side
probe that actually ran. A chat summary is not the deliverable.

## The Iron Law

```
NO CASE IS TICKED ON THE SCREEN ALONE
A HUMAN TICK IS RECORDED, NEVER A VERDICT
```

If the case's Expect (or `backend`) touches state the server owns, the case's
`run` block carries **both** `saw` (quoted UI) **and** `server` (probe command +
result) before `verdict: pass`. Pure presentation records
`server: none — presentational`.

"Review Product Flow judges product behavior on screen, not wire traffic" is false for any
case that claims create, update, delete, or persistence. The screen is necessary;
it is not sufficient.

A person's tick in the guide lands in that case's `human` block, which the agent
can read and must never promote: it says someone looked, not that the thing
works. Agents **must not** open the guide in Chrome (or any browser) to mark
progress — that burns tokens and writes to the wrong field space. Use `review-product-flow
mark`.

Probe ladder (strongest first): the request/response the UI just made → read-back
through the app's own API → store peek (DB / file / cache) → reload or restart
for durability. A red console error or 5xx on the wire fails the case even when
the screen looks right. Do not invent probe results you did not run.

## CLI (required for progress)

Resolve the review-product-flow skill root (this monorepo:
`skills/acceptance/review-product-flow`; when installed, the skill package path). Every
subcommand takes the **one** run file — cases and verdicts live in it together:

```bash
DF="python3 <skill-root>/scripts/review-product-flow"
RUN=.skills/<CODE>/review-product-flow.json

$DF list   $RUN
$DF show   $RUN CASE-1
$DF init   $RUN                       # seed pending in place
$DF next   $RUN                       # first case still to prove
$DF mark   $RUN CASE-1 pass --saw '…quoted UI…' --server '…probe…'
$DF status $RUN
$DF report $RUN -o .skills/<CODE>/review-product-flow-report.md
```

`mark pass` refuses empty `--saw` / `--server`. Presentational cases require
`--server 'none — presentational'`, and a case with a real `backend` is refused
that string — the rules cannot be skipped, because `backend` now travels in the
same file as the verdict.

**Optional live guide.** `$DF serve $RUN` binds `127.0.0.1:8787` and serves a
page that follows the run and accepts the person's ticks. It is optional by
construction: `render` bakes current verdicts into the HTML, so a guide opened
by double-click is correct with nothing running. Do not drive the guide; it is
for the human beside you.

## 1. Preconditions — origin and app

Confirm the target origin **before the first product click**:

- Default: local dev from `docs/agents/project.md` (`## Run locally (dev)`).
  Start the app if it is down.
- Non-local origin (staging, production, shared QA): **stop**. Ask for an
  explicit yes in this thread naming that origin. "Whatever is fastest", a demo
  deadline, or an already-open tab is **not** consent.
- Drive a **dedicated product tab**. Do not hijack a tab the user is working in.
- Do **not** open the review-product-flow guide HTML as a drive target.
- Avoid controls that raise native `alert` / `confirm` (they freeze many browser
  bridges); warn the user first if a case requires one.

*Done when: origin is local, or non-local consent is on the record, and the app
loads.*

## 2. Seed the run file before any drive

The run file is the one `review-product-flow` wrote: `.skills/<CODE>/review-product-flow.json`.

```bash
$DF init $RUN
```

If it already holds verdicts, **trust them** — `init` refuses to reset without
`--force`, and that refusal is the resume path, not an obstacle. Create one todo
per case. Resume: `$DF next` (first non-`pass`).

Each case's `run` block:

| field | content |
|---|---|
| `verdict` | `pending` \| `pass` \| `fail` \| `blocked` |
| `saw` | what was on screen — **quoted**, not paraphrased |
| `server` | probe + result, or `none — presentational` |
| `notes` | setup used, fix / `root-cause` hand-off, re-drive |

Beside it sits `human` — `checked`, `at`, `comment` — written only by a person
through the served guide. Read it as a signal about where to look. Never copy it
into `verdict`, and never let it stand in for evidence you did not gather.

**No case, not run.** Skipping a case because it is "the same CRUD pattern",
"only happy paths for the demo", because a lead said spot-check is fine, or to
"save time" leaves it `pending` or `blocked` — never silent `pass`.

*Done when: every case has run state and a todo, all `pending` (or restored).*

## 2a. Hard gate — fresh vet-product-flow report (before any product drive)

<HARD-GATE>
```
NO PRODUCT CASE IS DRIVEN WITHOUT A FRESH CLEAN VET REPORT
(OR AN IN-THREAD YES THAT NAMES EACH REMAINING OPEN VPF-N)
```

`init` may seed pending verdicts before or after this gate. **No product click
and no `mark` of a driven case** until the gate passes. Origin consent (§1)
remains mandatory before product clicks.
</HARD-GATE>

Run this algorithm **before §3** (before the first product click / drive loop):

```
REPORT = .skills/<CODE>/vet-product-flow.md
IF missing REPORT → STOP (run vet-product-flow)
Parse REPORT: run_file, cases_fingerprint, open findings
IF run_file path ≠ this RUN (normalized) → STOP
IF sha256(authored cases of RUN) ≠ cases_fingerprint → STOP (stale; re-vet)
IF open findings non-empty:
  IF chat has explicit user yes naming EACH open VPF-N id → proceed
     (append override line to .skills/<CODE>/progress.md or the walkthrough close notes:
      "VPF override: VPF-1, VPF-4 named by user <timestamp>")
  ELSE → STOP (list open findings; point to guide-gap loop)
ELSE → proceed (origin/app preconditions remain mandatory before product clicks)
```

**Freshness (not whole-file `rev`):** the report is fresh only when its
`run_file` matches this run file path **and** its `cases_fingerprint` matches
the SHA-256 of the run file's **authored** cases. Recipe SSOT (key order,
compact JSON, omit `run`/`human`/`rev`): load
`skills/acceptance/vet-product-flow/references/report-schema.md` (or the skill
package path when installed). Verdict marks and human ticks do **not** stale the
report; authoring edits that change cases **do**. Recompute the fingerprint from
the run file — do not trust a chat claim of freshness.

**Open findings block drive.** Every open code-grounded missing-situation finding
is **blocking** until fixed (guide-gap loop in `vet-product-flow`) or named in
an explicit in-thread yes. Severity labels (Critical / Important / Minor) order
fixes only — severity **does not** soften the gate, drop a finding from the open
set, or reintroduce a hard-only-on-Critical rule. Bare “just go”, “demo in N
minutes”, silent skip, or a yes that does not name each remaining open `VPF-N`
is **not** an override.

**On STOP:** list open findings (ids + severity + situation). Point the user to
the **guide-gap** fix loop in `vet-product-flow` (patch run file by severity →
re-render → re-invoke fresh isolated `vet-product-flow`; gate uses only the new
report). Do not invent cases mid-drive to paper over the gate.

**Override trail:** when the user names each open `VPF-N`, append a greppable
line to `.skills/<CODE>/progress.md` (or walkthrough close notes), e.g.
`VPF override: VPF-1, VPF-4 named by user <timestamp>`.

*Done when: report present, `run_file` + `cases_fingerprint` match, and either
`open_count` is 0 or every open `VPF-N` is named in-thread with an override trail.*

## 3. Drive each pending case

In file order (`$DF next` until empty):

1. `$DF show $RUN <CASE-ID>` — load Try / Expect / setup / backend.
2. Apply setup so the case can run independently.
3. Execute Try against the **product app** only (Chrome extension tools when
   present; else headed Chromium/Playwright). Do not hard-depend on a
   package-external browser skill. Do **not** open the guide HTML to tick boxes.
4. Fill `saw` from what is actually visible on the product.
5. Run the backend probe when required; fill `server`.
6. `$DF mark … pass|fail|blocked --saw … --server …` only when evidence slots
   match the Iron Law. Mark the todo done only on `pass`.

*Done when: the row is `pass`, or routed through §4.*

## 4. Failure routing

Re-drive the failed case once from a clean setup, then classify by observation.
**Master** (this controller) owns case selection, evidence slots, `mark`
pass/fail/blocked, and **re-test** after a fix — never hand those to a fix
subagent.

| Observation | Action |
|---|---|
| Deterministic fail on a real Expect / backend assertion | **Product defect.** Master marks `fail` with full evidence (`saw`/`server`). Dispatch an isolated **subagent** with a red-capable brief only: case id, `req`, try/expect, saw/server, repro — **not** the full session history or long dogfood context. Master does **not** patch product code in the walkthrough session. Subagent **REQUIRED SUB-SKILL: use `root-cause`** (and **test-first**); isolation is **not** a free patch without root-cause. |
| Flaky, or guide wrong (stale label, missing seed, bad Expect) | Fix the case's authored slots in the **run file** (re-`render` the HTML if the human has it open); re-drive. Do not send guide bugs to `root-cause`. |
| Shared precondition broken (login, server down, seed missing) | Stop the run. Leave remaining cases `pending`/`blocked`. Downstream is untested, not passing. |

**On DONE** (subagent reports fixed): control returns to the **master**. Restart
the app if needed, re-drive the failed case from a clean setup, **and** re-drive
every already-`pass` case whose `req` the product fix touched (grep the diff for
requirement IDs or the modules those cases exercise).

**Loops stay separate.** The guide-gap fix loop (`vet-product-flow`: patch run
file → re-vet) is **not** this product-defect dogfood loop. Guide-gap findings
are **not** routed here — the §2a gate should have blocked drive; if a missing
situation is discovered mid-run, treat it as guide wrong / re-enter vet, not as
a product defect. Product defects do not absorb missing-situation findings.

**Caps (D2):** 3 distinct fix attempts on the same case → stop and escalate.
5 product-defect fix cycles in the whole run → stop with a partial run file.
Do not mark untested cases `pass` to clear the board.

Durable asset for a product fix: the regression test `root-cause` already requires
under TDD — not a silent promotion of the whole guide into Playwright
(`validate-ui` is that path, only if the user asks).

## 5. Close the run

When every case is `pass`, or the run stops on a cap / precondition / escalate:

1. The run file is authoritative. A person's ticks are never required, and never
   substitute for a verdict you did not earn.
2. `$DF report $RUN -o .skills/<CODE>/review-product-flow-report.md`
3. **If you started `$DF serve`, ask the user whether to stop it.** Do not stop
   it silently — they may still be reading the guide — and do not walk away
   leaving a process holding a port. On yes: `$DF serve $RUN --stop`. On no:
   hand them that exact command.
4. Hand the user: path to the run file, path to the report, any
   `blocked`/`pending` cases and why.

*Done when: every case ID is accounted for in the run file, the report matches
it, and any server this run started has been stopped or explicitly left up at
the user's word — no bare "all good."*

## Rationalizations

| Thought | Reality |
|---|---|
| "Review Product Flow judges the screen, not wire traffic" | State cases require a server probe. Screen-only is not a pass. |
| "The human ticked it, so the case is done" | A tick says someone looked. `pass` needs `saw` and `server`. The two never merge. |
| "I'll tick the guide too so the human sees progress" | `mark` already writes the file the guide reads. Opening a browser to tick is waste and writes to the wrong field space. |
| "Same CRUD pattern — spot-check is enough" | No case, not run. Every case gets its own evidence. |
| "User said whatever is fastest / demo in N minutes" | Speed is not consent for staging/prod. Route Task, or run local. |
| "Happy paths on staging; skip edges to make the demo" | Partial run: unfinished rows stay pending/blocked, never pass. |
| "I'll tick pass and fill server evidence later" | Evidence slots are full before `pass`, or the verdict stays fail/pending. |
| "The other cases already passed before the fix" | Re-drive every already-pass case whose req the fix touched. |
| "Just go / demo in 5 minutes — skip the open findings" | Not an override. Name each open `VPF-N` or run the guide-gap loop. Severity does not soften the gate. |
| "Report is fine — rev only moved for marks" | Freshness is `run_file` + `cases_fingerprint`, not whole-file `rev`. Recompute fingerprint. |
| "Only Critical findings block drive" | Every open finding blocks. Severity orders fix only. |
| "I'll patch the product in this long dogfood thread" | Master marks fail; dispatch a subagent with a red-capable brief. Master re-tests. |
| "Isolation means skip root-cause / test-first" | Subagent still runs `root-cause` (+ test-first). Isolation ≠ free patch. |
| "Guide-gap miss mid-run — treat as product defect" | Separate loops. Guide wrong / re-enter vet; do not absorb missing-situation findings into root-cause. |

## Red Flags

- Opening the review-product-flow HTML in a browser to tick checkboxes during the run
- Copying a `human` tick into `verdict`, or citing one as evidence
- Ending a run without asking about a server this run started
- Marking `pass` with `server` empty on a create/update/delete/persist case
- Spot-checking a subset while claiming the guide is done
- Driving a non-local origin without an explicit yes naming that origin
- Patching product on a review-product-flow fail without `root-cause` when the fail is deterministic
- Claiming completion from memory after compaction instead of reading the run file
- Driving product cases with a missing, stale, or open-findings vet report and no named override
- Treating bare “just go” or severity=Minor as a gate pass
- Patching product in the master dogfood context instead of a red-capable subagent brief
- Clearing a product defect without `root-cause` / test-first because “it was isolated”
