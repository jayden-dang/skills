# `specify-behavior` — Open Questions ownership (2026-08-27)

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

