# TESTS

## Length pass — 280 to 194 lines (2026-09-07, v2.0.1)

Patch: no new rule, no new evidence slot, no wording changed inside a block
relocated verbatim. The `## 2a. Hard gate` section (fresh vet-flow-guide
report) was left untouched byte-for-byte — see "Gate left alone" below — as
were the `## Rationalizations` and `## Red Flags` tables.

**What moved.** `## 4. Failure routing` was already reached only when a driven
case is not `pass` — a skip predicate that was true of the section but never
said in its own heading. The heading now says so
(`## 4. Failure routing — only when a driven case is not \`pass\``), and the
routing table plus the On-DONE / loops-stay-separate / caps / durable-asset
paragraphs moved verbatim to `failure-routing.md`. `SKILL.md` keeps the
heading, the skip condition, and a one-line summary naming all three routing
outcomes (deterministic defect → isolated `root-cause` subagent, flaky/guide-
wrong → run file, broken shared precondition → stopped run) plus the pointer.

The "Optional live guide" paragraph under `## CLI` already opened with its own
skip predicate ("optional by construction"). It moved verbatim to `serve.md`,
along with the close-section stop instruction (`## 5` step 3) that only
applies when `$DF serve` was started — the two were one topic split across two
sections, now one file. `SKILL.md` keeps the heading-adjacent one-line summary
and the pointer in both places.

**What was deleted as duplication.** Two passages in `## The Iron Law` restated
rules that have a canonical home elsewhere in the same file, confirmed by grep
before deletion:
- `"Write Flow Guide judges product behavior on screen, not wire traffic" is
  false for any case that claims create, update, delete, or persistence...`
  restated the Rationalizations row `"Write Flow Guide judges the screen, not
  wire traffic" | State cases require a server probe...` and the normative
  statement immediately above it in the Iron Law section (state-touching cases
  need both `saw` and `server`). Surviving home: SKILL.md:23 (Iron Law) and
  SKILL.md:166 (Rationalizations row 1).
- `A person's tick in the guide lands in that case's \`human\` block... Agents
  must not open the guide in Chrome... to mark progress` restated the `human`
  field description in `## 2` (`Beside it sits \`human\`... Read it as a
  signal about where to look; never copy it into \`verdict\`...`, SKILL.md:71)
  and the Red Flags bullet `Opening the write-flow-guide HTML in a browser to
  tick checkboxes during the run` (SKILL.md:183) plus the matching
  Rationalizations row (SKILL.md:168). Every fact in the deleted paragraph
  (who writes `human`, what it means, the Chrome prohibition, the recording
  path via `$DF mark`) is present in one of those three surviving homes; the
  CLI section already documents `$DF mark` as the way to record progress.

**No-op deletions.** A duplicate clause "Do not open the guide HTML to tick
boxes" inside `## 3` step 3 was cut for the same reason (Red Flags already
carries it); the numbered step still tells the agent what to drive and how.
The three-example enumeration in "No case, not run" (`## 2`) — same-CRUD-
pattern / happy-paths-demo / lead-said-fine / save-time — collapsed to a
shorter open list, since the CRUD-pattern and happy-paths-demo excuses are
each already a Rationalizations row (SKILL.md:169, SKILL.md:171) naming the
same disposition (`pending`/`blocked`, never silent `pass`).

**Reflow.** Most remaining paragraphs, list items, and `*Done when*` lines
were joined from their ~78-column hard wrap into single lines with light word
trims (dropped redundant connective phrases, no fact removed) — this is what
took the file from 243 to 194 lines after the extractions and dedup above
already carried it from 280 to 243. Words fell from 2394 to 1956 (18%), against
a 31% line cut, so the ratio is not pure rejoining; `skill-rule-inventory.py
--diff` (below) is the mechanical check that no fact rode along with a joined
line.

**Preservation.** `scripts/skill-rule-inventory.py --diff` over the old
`SKILL.md` against the new three-file set (`SKILL.md`, `failure-routing.md`,
`serve.md`): 69 atoms at HEAD, 73 across the three files now. 12 flagged as
"reworded rather than removed" (≥70% of distinctive words survive) — read and
confirmed each is the same rule after the reflow above, not a shifted one.
One flagged "no home": the Preconditions bullet `Drive a **dedicated product
tab**. Do not hijack a tab the user is working in.` merged with the adjacent
`Do not open the write-flow-guide HTML as a drive target.` bullet into `Drive
a **dedicated product tab** — never the user's own tab, and never the
write-flow-guide HTML itself.` (SKILL.md:51) — a reword that fell just under
the 70% word-survival threshold, confirmed by grep, not a deletion.

All three `eval.json` contract anchors still resolve as literal substrings:
`NO CASE IS TICKED ON THE SCREEN ALONE` (Iron Law block, unchanged),
`NO PRODUCT CASE IS DRIVEN WITHOUT A FRESH CLEAN VET REPORT` (`## 2a`
`<HARD-GATE>` block, byte-identical to HEAD), and `4. Failure routing`
(substring of the new heading, which still contains the exact string).
`lint-skill-evals.py` and every other `scripts/lint-*.py` pass; only
`lint-skill-length.py` reports the expected "delete the budget entry" message,
left for the reviewer to clear with `--write` once the batch lands.

**Gate left alone.** `## 2a` (the `<HARD-GATE>` block, its freshness algorithm,
the open-findings/on-STOP/override-trail paragraphs) was not touched. The one
gate exception requires showing the owning file is in context at the moment
the gate line fires, not merely that it exists on disk — this skill's gate
runs at the start of a drive and does not itself load a sibling file that
would carry a moved line into that moment (the one existing pointer inside the
gate, to `vet-flow-guide/references/report-schema.md`, is a load-on-demand
reference for the fingerprint recipe, already extracted before this pass, and
does not cover the rest of the section). The exception could not be satisfied,
so every line of `## 2a` stayed, and the 85-line reduction target was met
entirely from the Iron Law, CLI, Preconditions, `## 2`, `## 3`, `## 4`, and
`## 5` sections instead.


## v2.1.0 — a driver ladder with `kimi-webbridge` first (2026-09-09)

Step 3 read "Chrome extension tools when present; else headed
Chromium/Playwright". It is now an explicit three-rung ladder, resolved once per
run and named in the report, with `kimi-webbridge` first when installed —
detected by its skill being available or `~/.kimi-webbridge/bin/kimi-webbridge`
existing.

The reason it earns the top rung is that it drives the user's own browser in
their real session, so a case that depends on being signed in needs no auth
setup. The same property is its hazard, and the step says so: a mutating case
runs against whatever that session is actually logged into, so the target is
confirmed before the first one.

The existing stance is unchanged and was deliberately preserved — the ladder is a
preference, there is no hard dependency on any package-external browser skill,
and a missing rung is skipped in silence rather than raised as a blocker.

Unmeasured; the change is a capability route, not a gate.
