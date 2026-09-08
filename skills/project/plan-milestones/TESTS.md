# TESTS.md — plan-milestones

## 2026-09-07 — length pass (221 → 193 lines)

Ran as a batch length pass across several skills, bringing `SKILL.md` under the
195-line target (the mechanical `lint-skill-length.py` ceiling is 200) without
losing any rule. Before: 221 lines / 2149 words / 63 atoms. After: 193 lines /
1926 words / 62 atoms across `SKILL.md` + the new sibling file (one atom —
the `## Who owns what` heading — was folded into the intro paragraph rather
than kept as its own heading; the fact it carried survives, reworded, in that
paragraph, confirmed by `skill-rule-inventory.py --diff`).

**Extracted (conditional branch, genuinely skipped on non-closure updates):**
The closure write-back mechanics — writing the `Closed:` SHA from the
assessment file rather than the write-handoff's copy, never re-running the
assessment, and the note that every other update reaches the approval gate
unaffected — moved verbatim to `closure-writeback.md`, a new sibling file.
`SKILL.md`'s Update section keeps the `<HARD-GATE>` that refuses an
unauthorised `Committed → Closed` transition fully inline and unthinned (per
this batch's rule that gate content never moves), now with an explicit skip
predicate ("only on a `Committed → Closed` transition; skipped for every
other edit") and a one-line pointer to the sibling file for what happens once
the gate clears. Both Create and Update modes stayed fully inline — neither
sits behind a pointer, since both are reached on real runs.

**Deleted as duplication (surviving home confirmed by grep):**
- The Iron Law's justification for "no second copy of status" ("a second
  copy of status drifts from the first, and the moment it drifts nobody can
  tell which one is lying") — surviving home: `## Rationalizations` row
  `"A status column would make this trackable"` → `"It makes it stale...
  /refresh-roadmap-status derives the rest"`.
- The "deferred, not deleted" rationale restatement — surviving home:
  `## Rationalizations` row `"We are not doing it, so remove the line"` →
  `"Defer it with a date and a reason. A deleted item takes its rationale
  with it"`.
- The "material change demotes" rationale restatement — surviving home:
  `## Rationalizations` row `"The user is the approver..."` → `"...Demote to
  Draft and show them what they now own"`.
- The closure section's closing line ("Every other update ... reaches the
  approval gate exactly as before. This gate fires on closure alone.") —
  surviving home: `closure-writeback.md` (relocated verbatim; the main file's
  own "skipped for every other edit" clause in the Closing intro already
  states the same fact for a reader who never opens the sibling file).
- `## Who owns what` as a standalone heading — folded into the "Where this
  sits" paragraph in the intro; same two facts kept (`specify-behavior` is
  the sole registrar of feature codes; this skill never touches
  `docs/specs/INDEX.md`).

**Also tightened (word-level, no fact removed):** the Iron Law's opening
definition of intent/progress, the Create step wording (steps 1, 3, 4), the
Update section's ID-permanence/material-change paragraphs, the ROAD-N
section's supporting prose, the Program-sync note, the approval-gate
trailer, and the No-op paragraph. Several adjacent short paragraphs under the
same heading were merged into one paragraph (Iron Law's two closing
paragraphs; ROAD-N's two closing paragraphs; Update's ID-permanence and
deferred-not-deleted paragraphs) — this removes blank-line separators between
sentences that were already tightened, not a raw rewrap of unchanged prose.
The frontmatter `description` was also trimmed: the long list of verbatim
"update the roadmap"-style trigger examples was cut to a representative
subset plus the existing catch-all ("or any request touching
docs/roadmap/INDEX.md"), which already covers the dropped examples.

**Anchors confirmed present verbatim:** `## The approval gate` (line 122),
`## ROAD-N is a slot, not a feature` (line 139) — both required by
`eval.json`'s `derived_from` fields and confirmed with `grep`.

**Verification run:**
- `skill-rule-inventory.py --diff` (old `SKILL.md` vs new `SKILL.md` +
  `closure-writeback.md`): 63 atoms → 62, all with a home; 6 flagged
  "reworded rather than removed" (all confirmed same rule, different words).
- `lint-skill-length.py`: reports the file now under the 200-line limit and
  says to clear its `scripts/skill-length-budget.json` entry. Left in place
  per instruction — the reviewer runs `--write` once for the whole batch.
- `lint-skill-evals.py`, `lint-skill-frontmatter.py`, `lint-skill-templates.py`,
  `lint-context7.py`, `lint-write-handoffs.py`: all pass.

Not touched: the two `<HARD-GATE>` blocks (closure authorization, approval
gate) and the `## Rationalizations` / `## Red flags` tables — gate content,
never moved or thinned.

### Reviewer note — four trigger phrasings restored

The pass trimmed the frontmatter `description`, dropping "what order should we
build this in", "we're not doing X anymore", "move sharing ahead of search", and
"reword this outcome" as a representative-subset cut. This skill is
model-invocable, so that line routes: every phrasing in it is a way the skill gets
found, and the first of those four was the only one carrying the word "order" at
all.

Restored on review. The four phrasings cost three lines and the file still lands
at 195. `author-skills` calls the description the highest-leverage line in a skill
and the one field that cannot be judged by reading — it has to be trigger-tested,
and a length pass is not the place to spend that budget. The brief for this batch
never mentioned descriptions, which is why the pass had no reason to leave it
alone; it does now.
