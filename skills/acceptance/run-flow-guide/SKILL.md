---
name: run-flow-guide
version: 2.0.1
description: >-
  Use when a guide from write-flow-guide already exists and its cases must be
  executed against the running app — agent-driven, screen plus backend
  evidence. Produces a run file with a pass / fail / blocked verdict per case.
  Not for authoring the guide (`write-flow-guide`) or committed e2e
  (`validate-ui`).
---

# Run Flow Guide

Execute an existing guide from write-flow-guide against the **product app** in a real browser. The deliverable is the **run file** — every case ID accounted for with quoted screen evidence and, when the case touches server-owned state, a server-side probe that actually ran. A chat summary is not the deliverable.

## The Iron Law

```
NO CASE IS TICKED ON THE SCREEN ALONE
A HUMAN TICK IS RECORDED, NEVER A VERDICT
```

If the case's Expect (or `backend`) touches state the server owns, the `run` block carries **both** `saw` (quoted UI) **and** `server` (probe + result) before `verdict: pass`; pure presentation records `server: none — presentational`. (Rationalizations below name every excuse for skipping this; Red Flags name the Chrome-ticking trap.)
Probe ladder (strongest first): the UI's own request/response → read-back through the app's API → store peek (DB/file/cache) → reload/restart for durability. A red console error or 5xx fails the case even when the screen looks right — never invent a probe result you did not run.

## CLI (required for progress)

Resolve the write-flow-guide skill root (`skills/acceptance/write-flow-guide` in this monorepo, else the installed package path). Every subcommand takes the **one** run file — cases and verdicts live in it together:

```bash
DF="python3 <skill-root>/scripts/flow-guide"
RUN=.skills/<CODE>/flow-guide.json
$DF list   $RUN
$DF show   $RUN CASE-1
$DF init   $RUN                       # seed pending in place
$DF next   $RUN                       # first case still to prove
$DF mark   $RUN CASE-1 pass --saw '…quoted UI…' --server '…probe…'
$DF status $RUN
$DF report $RUN -o .skills/<CODE>/flow-guide-report.md
```

`mark pass` refuses empty `--saw` / `--server`; a presentational case must pass `--server 'none — presentational'`, and a case with a real `backend` is refused that same string — unskippable, since `backend` now travels with the verdict.
**Optional live guide.** WHEN a person will tick cases live while you drive, read `serve.md` beside this file and follow it exactly — not required, since `render` already bakes verdicts into static HTML.

## 1. Preconditions — origin and app

Confirm the target origin **before the first product click**:

- Default: local dev from `docs/agents/project.md` (`## Run locally (dev)`); start the app if it is down.
- Non-local origin (staging, production, shared QA): **stop** and get an explicit in-thread yes naming that origin — "whatever is fastest", a demo deadline, or an already-open tab is **not** consent.
- Drive a **dedicated product tab** — never the user's own tab, and never the write-flow-guide HTML itself.
- Avoid controls that raise native `alert` / `confirm` (they freeze many browser bridges); warn the user first if a case requires one.

*Done when: origin is local, or non-local consent is on the record, and the app loads.*

## 2. Seed the run file before any drive

The run file is the one `write-flow-guide` wrote: `.skills/<CODE>/flow-guide.json`. Seed it: `$DF init $RUN`.

If it already holds verdicts, **trust them** — `init` refuses to reset without `--force`, and that refusal is the resume path, not an obstacle. Create one todo per case; resume with `$DF next` (first non-`pass`).

Each case's `run` block:

| field | content |
|---|---|
| `verdict` | `pending` \| `pass` \| `fail` \| `blocked` |
| `saw` | what was on screen — **quoted**, not paraphrased |
| `server` | probe + result, or `none — presentational` |
| `notes` | setup used, fix / `root-cause` hand-off, re-drive |

Beside it sits `human` — `checked`, `at`, `comment` — written only by a person through the served guide. Read it as a signal about where to look; never copy it into `verdict`, and never let it stand in for evidence you did not gather.
**No case, not run.** Skipping a case for any reason — pattern-matching, time pressure, a lead's OK — leaves it `pending`/`blocked`, never silent `pass`.

*Done when: every case has run state and a todo, all `pending` (or restored).*

## 2a. Hard gate — fresh vet-flow-guide report (before any product drive)

<HARD-GATE>
```
NO PRODUCT CASE IS DRIVEN WITHOUT A FRESH CLEAN VET REPORT
(OR AN IN-THREAD YES THAT NAMES EACH REMAINING OPEN VFG-N)
```

`init` may seed pending verdicts before or after this gate. **No product click
and no `mark` of a driven case** until the gate passes. Origin consent (§1)
remains mandatory before product clicks.
</HARD-GATE>

Run this algorithm **before §3** (before the first product click / drive loop):

```
REPORT = .skills/<CODE>/vet-flow-guide.md
IF missing REPORT → STOP (run vet-flow-guide)
Parse REPORT: run_file, cases_fingerprint, open findings
IF run_file path ≠ this RUN (normalized) → STOP
IF sha256(authored cases of RUN) ≠ cases_fingerprint → STOP (stale; re-vet)
IF open findings non-empty:
  IF chat has explicit user yes naming EACH open VFG-N id → proceed
     (append override line to .skills/<CODE>/progress.md or the walkthrough close notes:
      "VFG override: VFG-1, VFG-4 named by user <timestamp>")
  ELSE → STOP (list open findings; point to guide-gap loop)
ELSE → proceed (origin/app preconditions remain mandatory before product clicks)
```

**Freshness (not whole-file `rev`):** the report is fresh only when its
`run_file` matches this run file path **and** its `cases_fingerprint` matches
the SHA-256 of the run file's **authored** cases. Recipe SSOT (key order,
compact JSON, omit `run`/`human`/`rev`): load
`skills/acceptance/vet-flow-guide/references/report-schema.md` (or the skill
package path when installed). Verdict marks and human ticks do **not** stale the
report; authoring edits that change cases **do**. Recompute the fingerprint from
the run file — do not trust a chat claim of freshness.

**Open findings block drive.** Every open code-grounded missing-situation finding
is **blocking** until fixed (guide-gap loop in `vet-flow-guide`) or named in
an explicit in-thread yes. Severity labels (Critical / Important / Minor) order
fixes only — severity **does not** soften the gate, drop a finding from the open
set, or reintroduce a hard-only-on-Critical rule. Bare “just go”, “demo in N
minutes”, silent skip, or a yes that does not name each remaining open `VFG-N`
is **not** an override.

**On STOP:** list open findings (ids + severity + situation). Point the user to
the **guide-gap** fix loop in `vet-flow-guide` (patch run file by severity →
re-render → re-invoke fresh isolated `vet-flow-guide`; gate uses only the new
report). Do not invent cases mid-drive to paper over the gate.

**Override trail:** when the user names each open `VFG-N`, append a greppable
line to `.skills/<CODE>/progress.md` (or walkthrough close notes), e.g.
`VFG override: VFG-1, VFG-4 named by user <timestamp>`.

*Done when: report present, `run_file` + `cases_fingerprint` match, and either
`open_count` is 0 or every open `VFG-N` is named in-thread with an override trail.*

## 3. Drive each pending case

In file order (`$DF next` until empty):

1. `$DF show $RUN <CASE-ID>` — load Try / Expect / setup / backend.
2. Apply setup so the case can run independently.
3. Execute Try against the **product app** only (Chrome extension tools when present; else headed Chromium/Playwright) — no hard dependency on a package-external browser skill.
4. Fill `saw` from what is actually visible on the product.
5. Run the backend probe when required; fill `server`.
6. `$DF mark … pass|fail|blocked --saw … --server …` only when evidence slots match the Iron Law; mark the todo done only on `pass`.

*Done when: the row is `pass`, or routed through §4.*

## 4. Failure routing — only when a driven case is not `pass`

**Master** (this controller) owns case selection, evidence, `mark`, and re-test — never a fix subagent. Re-drive once from a clean setup, then read `failure-routing.md` beside this file and follow it exactly: it routes a deterministic defect to an isolated `root-cause` subagent (never patched in this session), a flaky or guide-wrong case back to the run file, and a broken shared precondition to a stopped run with the rest `pending`/`blocked` — plus the post-fix re-test rule, the guide-gap boundary, and the fix-attempt caps.

## 5. Close the run

When every case is `pass`, or the run stops on a cap / precondition / escalate:

1. The run file is authoritative — a person's ticks are never required, and never substitute for a verdict you did not earn.
2. `$DF report $RUN -o .skills/<CODE>/flow-guide-report.md`
3. If you started `$DF serve`, follow the stop step in `serve.md` — never silently, and never leaving a process holding the port.
4. Hand the user: path to the run file, path to the report, and any `blocked`/`pending` cases and why.

*Done when: every case ID is accounted for in the run file, the report matches it, and any server this run started has been stopped or explicitly left up at the user's word — no bare "all good."*

## Rationalizations

| Thought | Reality |
|---|---|
| "Write Flow Guide judges the screen, not wire traffic" | State cases require a server probe. Screen-only is not a pass. |
| "The human ticked it, so the case is done" | A tick says someone looked. `pass` needs `saw` and `server`. The two never merge. |
| "I'll tick the guide too so the human sees progress" | `mark` already writes the file the guide reads. Opening a browser to tick is waste and writes to the wrong field space. |
| "Same CRUD pattern — spot-check is enough" | No case, not run. Every case gets its own evidence. |
| "User said whatever is fastest / demo in N minutes" | Speed is not consent for staging/prod. Route Task, or run local. |
| "Happy paths on staging; skip edges to make the demo" | Partial run: unfinished rows stay pending/blocked, never pass. |
| "I'll tick pass and fill server evidence later" | Evidence slots are full before `pass`, or the verdict stays fail/pending. |
| "The other cases already passed before the fix" | Re-drive every already-pass case whose req the fix touched. |
| "Just go / demo in 5 minutes — skip the open findings" | Not an override. Name each open `VFG-N` or run the guide-gap loop. Severity does not soften the gate. |
| "Report is fine — rev only moved for marks" | Freshness is `run_file` + `cases_fingerprint`, not whole-file `rev`. Recompute fingerprint. |
| "Only Critical findings block drive" | Every open finding blocks. Severity orders fix only. |
| "I'll patch the product in this long dogfood thread" | Master marks fail; dispatch a subagent with a red-capable brief. Master re-tests. |
| "Isolation means skip root-cause / test-first" | Subagent still runs `root-cause` (+ test-first). Isolation ≠ free patch. |
| "Guide-gap miss mid-run — treat as product defect" | Separate loops. Guide wrong / re-enter vet; do not absorb missing-situation findings into root-cause. |

## Red Flags

- Opening the write-flow-guide HTML in a browser to tick checkboxes during the run
- Copying a `human` tick into `verdict`, or citing one as evidence
- Ending a run without asking about a server this run started
- Marking `pass` with `server` empty on a create/update/delete/persist case
- Spot-checking a subset while claiming the guide is done
- Driving a non-local origin without an explicit yes naming that origin
- Patching product on a write-flow-guide fail without `root-cause` when the fail is deterministic
- Claiming completion from memory after compaction instead of reading the run file
- Driving product cases with a missing, stale, or open-findings vet report and no named override
- Treating bare “just go” or severity=Minor as a gate pass
- Patching product in the master dogfood context instead of a red-capable subagent brief
- Clearing a product defect without `root-cause` / test-first because “it was isolated”
