---
name: scan-architecture
version: 1.6.0
description: "Use when someone asks where refactoring would pay, for an architecture review, or for a codebase-health or technical-debt scan across the whole repo. Produces a posture reading, ranked candidates in an HTML report and one follow-up on the board, and applies one direction only when asked to."
---

# Improve the Architecture

Scan the codebase for accumulated friction, present deepening candidates as a visual report, and carry the one the user picks into the normal spec cycle. The goal is testability and navigability — modules deep enough that their interface is the test surface.

Vocabulary is strict throughout: **module, interface, implementation, seam, adapter** (plus depth/locality/leverage as qualities) — a *seam* is a public surface where behavior is both observable and substitutable (the same seam `test-first` and `design-solution` name). Never drift into "component", "service", "layer", or "boundary" — precision in the nouns is what keeps the findings comparable run over run.

## 1. Take the posture

The scan opens here, before any reading. Run it, do not estimate:

```
cd <repo root> && python3 <skill-root>/scripts/posture.py --days 180
```

The working directory decides which repo is measured — run it from the repo under scan, never from the skill's own folder.

It prints and records four things: rules `mechanised/total` with the prose-only IDs named, change locality (median files and modules per commit, and the share of commits spanning more than one module), cross-module co-change pairs, and the most-changed files. A rule no check defends is a wish, and this count says how many the repo is carrying.

The record lands in `.skills/scan-architecture/posture.json` (local, never committed). When one already exists, every number comes back with its delta since the previous scan — that delta is the only evidence that the last scan's pick moved anything.

Then read `CONTEXT.md` (the domain names good seams) and `docs/adr/` (decisions not to re-litigate), with the numbers already in hand. Co-change pairs and the most-changed files name the modules to open first: design defects that only history reveals never surface in a reading pass.

If the project links approved engineering or operating targets to saved
measurements, read the relevant pair before ranking. Compare scope,
environment and revision or measurement window. A frequent edit is a lead,
not evidence of a measured quality gap. Check the measured stage before
attributing a delay to code structure. Per-stage percentiles diagnose stages;
use the separately measured end-to-end percentile for the improvement target.

**Done when:** `posture.json` is written, and you can name the prose-only rule IDs aloud.

## 2. Explore for friction

Dispatch an explore subagent to walk the codebase, starting at the modules the posture named — then onward organically, no rigid checklist, just noting where work hurts:

- **Shallow modules** — an interface nearly as complex as the implementation behind it
- **Poor locality** — one conceptual change fans out across many files
- **Missing or weak seams** — places substitution is needed but impossible, or a seam exists with only one hypothetical adapter
- **Untested-through-interface** — code only testable by reaching past its interface into internals
- **Measured quality gap** — a project target misses on comparable evidence. Trace
  the cost or failure to the relevant module, setup, or runtime path before ranking.

Apply the **deletion test** to anything suspect: if this module vanished, how much would its callers need to know to rebuild the behavior? "Almost everything" means the module was shallow — deleting it would concentrate complexity rather than lose it. That concentration point is your candidate.

**Done when:** you hold 3–7 candidates, each tied to specific modules and a named kind of friction.

## 3. Present the report

REQUIRED SUB-SKILL: use `craft-page` before writing any markup. The treatment is utilitarian — a real type scale, a chosen palette, no hero — and the report is scanned, not read: the confidence badge and the before/after sketch have to read at a glance. The sketch is a primary figure: name the job `before/after structure` and follow `craft-page`'s diagram recipe (recipe-authored inline SVG is hand-built).

Write a **self-contained HTML file** (inline CSS/SVG only — no external scripts, stylesheets, or CDNs) to the OS temp directory (`$TMPDIR`, falling back to `/tmp`; `%TEMP%` on Windows) as `architecture-review-<timestamp>.html`, so nothing lands in the repo. Open it (`open` / `xdg-open` / `start`) and tell the user the absolute path.

REQUIRED — the report opens with a **posture strip**, before any candidate: rules `mechanised/total` with the prose-only IDs named, the three locality numbers, and any outstanding exception list the repo's own checks carry. Each with its delta when a previous posture exists. This is the part a later scan compares against, so it is numbers, not prose.

Build the strip by reading `posture.json` field by field — every figure on the page is copied from that file, never recalled from earlier in the session. A strip reading `0/0`, `first scan`, or a dash while the file holds real numbers is a fabricated posture, and it poisons the delta of every scan that follows.

One card per candidate:

- **Files** — the modules involved (monospaced list; this report is ephemeral, so paths are fine here)
- **Problem** — one sentence: what hurts and which friction kind it is
- **Proposed direction** — one sentence: what would deepen or which measured gap the change addresses
- **Win** — bullets of at most 6 words each, named as qualities ("locality: change lands in one module", "interface shrinks, tests hit one seam")
- **Confidence badge** — exactly one of `Strong` / `Worth exploring` / `Speculative`
- **Before/after sketch** — for structure use the `before/after structure` figure. For a measured gap use the observed path with the bottleneck and proposed change marked. Label a predicted result as a target until measured.

End with the first candidate and why, then the measurement that should move.
Use the project target and comparable baseline when available. Otherwise use
the posture measure or one prose-only rule to mechanize. Ask the user which
candidate they want to pursue.

**Do not propose concrete interfaces yet** — the report names directions, not designs. Interface shape belongs to the clarify-decisions step, with the user in the loop.

**ADR conflicts:** a candidate that contradicts an existing ADR is included only when its evidence carries a `Strong` confidence badge; below that it is dropped, not listed. An included one is marked with the ADR reference and why the decision deserves revisiting. Do not list every refactor an ADR forbids.

REQUIRED — the top recommendation leaves the session as one follow-up, in the Issue format of `docs/agents/issue-tracker.md`: a ticket created with that file's tracker ops, or the file `.skills/inbox/<slug>.md` (first line `# <title>`) and no ticket WHERE that file sets **Follow-up filing** to `draft`. Problem is the measured friction; Outcome is the proposed direction; Acceptance is the baseline, desired movement and comparable measurement to repeat; Out of scope names the other candidates. One follow-up, not one per candidate. The report sits in a temp directory and the question in one reply: a scan run for an operator who was out until morning ended "Nothing proceeds until Lan picks one", with nothing on the board for her to pick from.

**Done when:** the posture strip carries every count from step 1, the report is open in the user's browser, the follow-up is a ticket number read back from the tracker or a path under `.skills/inbox/`, and you have asked which candidate to pursue.

## 4. Shape the chosen candidate

Once the user picks:

- REQUIRED SUB-SKILL: use `clarify-decisions` — walk the shape of the deepened module one question at a time: constraints, what sits behind the new seam, which adapters are real, which tests survive.
- REQUIRED SUB-SKILL: use `define-domain` for side effects as decisions land — new module named after a concept missing from `CONTEXT.md`? Add the term. Fuzzy term sharpened mid-conversation? Update it now, not later. User rejects a candidate for a load-bearing reason? Offer a 1–3 sentence ADR so future scans do not re-suggest it (skip ephemeral or self-evident reasons).
- State the ceremony tier aloud — 0 for a change small enough to go straight to `test-first`, 1+ for one needing requirements first.

**Done when:** `clarify-decisions` has no unexplored branch left, and the ceremony tier is stated aloud as 0 or 1+.

## 5. Feed the spec cycle

They have already named one direction and told you to apply it? Step 6 owns the run. The hand-off below does not close it.

Tier 0 (mechanical, no behavior change) can proceed directly under `test-first`/`prove-claim` discipline. Anything tier 1 or above: REQUIRED SUB-SKILL: use `frame-change` — hand it the shaped improvement and let it run the normal cycle to requirements; architecture work earns no exemption from the spec gate.

**Done when:** the work has an owner flow — either in progress under tier 0 discipline, or handed to `frame-change` — or step 6 has taken the run because they asked to apply.

## 6. Apply when they ask for one direction

They asked only for the scan? Stop after the question in step 3. Leave the repo's tracked files as you found them.

They named one direction and told you to apply it:

1. Before any edit, run the repo's whole test command. Save the full output at `.skills/scan-architecture/suite-before.log`. Write `.skills/scan-architecture/suite-before.note.md` with the command and every test that failed.
2. From `posture.json`, pick the one figure the next scan should see move because of this direction. Write `.skills/scan-architecture/prediction.md` with that figure, the direction, and the sentence "This figure has not moved yet."
3. The direction changes what a user or a test can observe? Write the requirements for that direction in `.skills/scan-architecture/apply.md` before any production edit. A deferred writeup does not make the change tier 0. Then REQUIRED SUB-SKILL: use `test-first`.
4. Nothing observable changes? REQUIRED SUB-SKILL: use `test-first`, and leave the existing assertions intact.
5. Run the same test command. Save it at `.skills/scan-architecture/suite-after.log`. The failing set matches `suite-before.log`, or you put the direction back. A new failure you can reproduce only with the direction in the tree sends the direction back out.
6. Do not report the posture figure as moved.

**Done when:** both logs and `prediction.md` are on disk, production edits exist only for the named direction, and a behavior change has `apply.md` written before those edits.

## Rationalizations

| Thought | Reality |
|---|---|
| "Priya deferred the writeup, so I'll treat this as tier 0" | Harbor Desk, 7 Nov 2026. Focus timing changed. `apply.md` was never written. The deferral was the reason given. |
| "The new test failed, so I have a before" | The first command was `node --test test/focus.test.js` after `test/focus.test.js` was already rewritten. `npm test` was not saved before the production edit. |

## Red Flags

- Relabeling a behavior change as tier 0 because a writeup was deferred.
- A proof note whose only test log was taken after the production edit.
