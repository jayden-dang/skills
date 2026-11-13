# `specify-behavior` — Open Questions ownership (2026-08-27)

## v1.4.0 — NFR thought-table trim (2026-09-14)

NFR consult already lives in `nfr-grounding.md`. The five-row thought table
was a second home. Root still walks the four attributes, keeps
`Section-kind: nfr`, and forbids inventing TB/THR/CMP/SLO IDs.


Companion to clarify-decisions v1.2.0 Owned unknowns. Model roster: grok-class.

## Baseline failure (pre-1.2.0)

| Scenario | Pressures | Observed | Rationalization |
|---|---|---|---|
| **S-OWNED-TBD-APPROVE** | authority + pragmatic | Bare `- TBD: SLO window` in Open Questions could reach Approve; clarify unknowns dropped | "Open Questions can stay messy" / "later NFR" |

## GREEN — v1.2.0 / wording 1.2.1

| Scenario | Required | Observed |
|---|---|---|
| S-OWNED-TBD-APPROVE | Block Approve on bare TBD; require owner · date · forbid-guess (`cấm đoán`) or resolve | **Pass** — agent refused Approve; cited Placeholder scan |

Wording 1.2.1: English **forbid-guess** primary; `cấm đoán` gloss retained.

## Rules this evidence owns

| Rule | Evidence |
|---|---|
| Bare TBD without owner/date/cấm đoán blocks `Status: Approved` | GREEN S-OWNED-TBD-APPROVE |
| Paste Owned unknowns from clarify close package into Open Questions | SKILL.md Step 5 Placeholder scan |
| Do not mark Reliability NFR `None` when close package already locked reliability | SKILL.md Step 5 Close-package ingest |

## Length pass (2026-09-07) — 271 → 195 lines

Trim to bring SKILL.md under the 200-line lint limit (`scripts/lint-skill-length.py`),
per `author-skills`' bucket rules. No behavioral atom lost — every flagged
diff atom below is a reword-in-place or a verbatim move, confirmed by grep.

**Moved verbatim to new sibling files** (Conditional bucket — each fires only
under a named skip predicate; SKILL.md keeps the heading, the condition, and a
one-line pointer):

- Step 2b's "System docs for NFR grounding" subsection (which system doc to
  consult per quality attribute, hard constraints, write rules, worked
  example) → `nfr-grounding.md`. Fires only when an attribute is material —
  the brief's flagged case: the heading reads universal but the content is
  conditional in effect.
- Step 1's roadmap-bind procedure (WHERE `docs/roadmap/INDEX.md` exists) →
  `roadmap-bind.md`.
- Step 5's Code-claim check and Close-package ingest recipes (both already
  opened with an `if` / `(when present)` skip predicate) → one shared
  `self-review-conditional.md` (two sections).

**Never moved or thinned** (Gate bucket): the `SECTION-KIND IRON LAW` fenced
block in Step 2b, the NFR `| Thought | Reality |` table, and the Placeholder
scan's GREEN-tested TBD-block rule (S-OWNED-TBD-APPROVE) — all still verbatim
in SKILL.md.

**Tightened in place** (Universal bucket — prose narrowed, no fact dropped):
Two modes' tier-1 and new-feature paragraphs, Step 2's Story-line intro
(fenced example folded into one sentence), Step 2b's "additive, never a new
gate" paragraph, the Story-quality gate (numbered recipe → one prose
paragraph, same four rules), the post-approval paragraph (dropped one
sentence restating `Status: Approved`'s trigger — a duplicate of the
Story-quality gate's own approval line, same fact, one home), ID immutability,
Step 1's intro, and several list items rewrapped onto wider lines with no
wording lost (pure line-wrap, e.g. Placeholder scan, Bind-the-roadmap-item).

**`skill-rule-inventory.py --diff` result:** 59 atoms at HEAD, 59 across the 4
files now; 11 flagged as "no home" because wording changed on the tighten-in-place
edits above (fuzzy text match, not a lost rule). Each confirmed present by
grep: the fix-requirement/guard bullets (Two modes, now inline prose, SKILL.md
lines 18-19), the REQUIRED-slot sentence (line 31), the Accessibility bullet
(line 103, "screen-reader" → "SR"), the Placeholder-scan bullet (lines 163-164,
rewrapped), the Close-package-ingest bullet (heading kept in SKILL.md line 171,
body moved verbatim to `self-review-conditional.md` line 17), and the four
Story-quality-gate numbered items (now one prose paragraph, SKILL.md lines
175-179 — list-every-story, confirm-one-act, split-on-fail, approve-only-after,
never-silent-approve all present).

**Atom count:** 59 before (single file) → 41 in SKILL.md + 18 across the three
siblings = 59 after.

**Contract-eval anchors confirmed present verbatim:** `SKILL.md § Step 1:
Register the feature code`, `§ Step 2: Write stories and EARS criteria`,
`§ Step 3: Guard existing behavior`, `§ Step 4: Out of Scope`. `lint-skill-evals.py`
and the rest of the `lint-*.py` suite pass clean.

**Line count:** 271 → 195 (SKILL.md). `lint-skill-length.py` budget entry
cleared for this file.


## Template sync — R11 names S8 (2026-10-14)

The shared `roadmap-findings.md` now lists `S8` (the roadmap's `After:` item-order
rule, added in plan-milestones 1.2.0) among the structural rules `R11` reports. No
behavior of this skill changes beyond reading the longer rule list.

## v1.5.0 — one rule, many inputs, one criterion (2026-10-15)

Companion to plan-tasks 1.7.0: per-input criteria become per-input IDs, which become
per-input tests. Shape check only (see plan-tasks TESTS.md RED: 10 criteria → 10 tests).
Contract eval asserts the SKILL.md sentence.

## 2026-10-30 — a roadmap item delivered by amending a feature (1.5.0 → 1.6.0)

Source: the klynt frame-change on MILE/ROAD meaning. klynt ROAD-219 and ROAD-220 were built as
amendments of CPLAN and CBUILD. The single-value binding cell could not record them, so every
derivation showed them as unspecced, and the hand-kept lanes table wrote "CBUILD Implemented
(amend)" in prose.

**Scenario.** An `academy` fixture where PLAN is Implemented and bound to ROAD-2, and ROAD-5 is
live and unbound. amend-feature has routed a tier-1 change: "This is how roadmap item ROAD-5
gets delivered — there will be no separate feature for it; it's a change to PLAN." The owner
has pre-approved the wording. The prompt never says amends, binding or task group. Scored from
`git diff` and from the chart-progress extractor's reading.

**RED, 1.5.0** (sonnet 1, haiku 1). 2/2 appended a fix and a guard to PLAN's
requirements.md and left the catalog cell at `ROAD-2`. Neither wrote any tasks. Quoted:
- haiku: "a two-valued cell would break R5 … the roadmap tooling will report ROAD-5 as
  unspecced (R7) … For now the link between ROAD-5 and PLAN exists only as prose."
- sonnet: "R5 requires each binding to resolve to exactly one ROAD. Writing ROAD-5 there would
  break that rule."

**Form.** The output had the wrong shape because the grammar had no slot for an amend:
- `roadmap-bind.md` gains an amend paragraph (`ROAD-2 amends ROAD-5`, plus a
  `## ROAD-N amendment` task group written before code) that carries the recorded R5 quote.
- The tier-1 mode gains a WHEN pointer to it.
- R5, R6 and R7 in `roadmap-findings.md` now judge the primary part and the amends list
  separately.
- The template comment and `specs-INDEX.md` name the grammar.

**GREEN, 1.6.0** (sonnet 1, haiku 1). 2/2 wrote `ROAD-2 amends ROAD-5` in the catalog cell and
appended `## ROAD-5 amendment: brief-outside-default`, with an unticked task citing the new
criteria. Neither touched the roadmap. The extractor then reads ROAD-5 as `building` on PLAN.
Haiku also mirrored the cell into the requirements.md `Roadmap item:` header, which is harmless.

## 2026-10-30 — claim the ROAD before writing its spec (1.6.0)

Source: the same frame-change. Several people and agents frame specs in parallel, and nothing
stopped two sessions from specifying the same ROAD. The claim is a tracker issue assigned
before the spec starts.

**Scenario.** An `academy` fixture with `docs/agents/issue-tracker.md` (GitHub) and a stubbed
`gh` on PATH that logs every call. #301 "ROAD-6 desktop foundation" is open, assigned to alice,
labelled shaping. Jayden asks the agent to write ROAD-6's requirements from a confirmed close
package and says he is in meetings. The prompt never says claim, assignee or issue.

**RED, 1.5.0 text** (sonnet 1, haiku 1). 2/2 never ran `gh` (the call log was empty), and both
registered a Draft card for ROAD-6 and wrote its requirements: DESK on a new branch, DESKTOP
in the working tree.

**Form.** A step was omitted, so the fix is a deterministic recipe: a `**Claim first.**` block
at the top of `roadmap-bind.md`, with fixed `gh` reads and four outcomes. Step 1's pointer
moved to the start of the step, so the check runs before a row is written. The counter carries
the #301 / alice case.

**GREEN** (sonnet 1, haiku 1). 2/2 ran exactly `gh issue list --state open --json
number,title,assignees` and `gh api user --jq .login`, stopped, named #301 and alice, and left
the tree clean. Neither reassigned the issue or opened a competing one.

**No-claim path, then REFACTOR** (haiku). With no ROAD-6 issue in the stub, the harness's
permission classifier denied `gh issue create`. The run then wrote the card and the
requirements anyway and reported "the claim is missing". The counter added: "Continue means
the issue now exists and is assigned to you … stop as on someone else's claim and name the
command", carrying that run. Re-run: the create was denied again, the run stopped with an
empty `git status`, and it named the `gh issue create` command for the user.

Not covered: the create-and-assign success path, because the classifier denies writes from
test agents, and the tier-1 amend path's claim check (only the binding half was run there).

## 2026-11-01 — a roadmap claim follows reach (1.6.0 → 1.7.0)

Design: `docs/design/2026-11-01-issue-format.md`. Fixture: a generated repo with an in-repo tracker CLI and the new
`Issue format` seed.

**RED, `roadmap-bind.md` on the new seed, private roadmap.** The seed carried most of it. Sonnet 1 and haiku 1 titled
the ticket "Weekly digest" and wrote `road: ROAD-6` to `.skills/DIGEST/tickets.md`, each saying the skill's title
rule was overridden. On a rerun, sonnet 1 found the claim from that line and created no second ticket. With the
ticket reassigned to alice, haiku 1 stopped. One failure remained: the two runs chose `needs-triage` and `shaping`.

**Form.** The claim rule now states both reach paths, so the file stops contradicting the seed, and the create names
its state.

**GREEN.**
- Shared, alice holds the `ROAD-6` issue, haiku 1: stopped and wrote nothing.
- No `Issue format` section, sonnet 1: created nothing and named `/configure-repo`.
- `test_lanes.py`: passes, unchanged.
- **Not proven.** Private and shared with no existing ticket, haiku 1 each: the permission classifier denied `tools/tix
  create` both times, so the create never ran. Both drafted the expected title, state and assignee. The private run left no
  `road:` line, since it had no ticket number. The create path rests on the RED runs above.

`notion-draft.md` is unedited, so its sign-off list behaves as before.


## 2026-11-13 — the ROAD binding refreshes the lanes (1.7.0 → 1.8.0)

Step 1 calls `refresh-lanes` once the card's Roadmap item cell holds a `ROAD-N`. RED on
Sonnet and Haiku (tier-2 hand-off for ROAD-2, leave Draft): both wrote the Draft card bound
to ROAD-2, left the repo uncommitted, and left `docs/roadmap/lanes.md` untouched, without
mentioning it. GREEN round 1: both called `refresh-lanes`, which printed `unchanged` —
`lanes.py` showed a ready item with a spec as plain "Ready", so the binding was invisible
in the file. `lanes.py` now writes "Ready · spec written" (test-first). GREEN round 2: both
printed `written`; ROAD-2 reads "Ready · spec written", left uncommitted beside the card.
Details: `skills/track/refresh-lanes/TESTS.md` § 2026-11-13.
