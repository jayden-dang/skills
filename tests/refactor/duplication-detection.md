# REFACTOR — does the Duplication entry make duplication findable?

Closes the debt left open when `Duplication` was added to `author-skills`
Vocabulary: GREEN scored 2/3, which is not bulletproof, and one REFACTOR
iteration was owed. Audit Trace-ignored.

## Fixture

`fixture-release-notes/SKILL.md` — a plausible skill carrying planted defects:
two rules each stated three times (intro / Step 2 / Checklist), two dead
sections, and one no-op line as a control. The control matters: it distinguishes
"the reviewer found nothing" from "the reviewer used the tool the standard gives
it and lacked the one it doesn't."

## Method

The open-ended reviewer prompt, not the four-category rubric used in the
64-skill sweep. Handing a reviewer the category "duplication" tests whether it
can apply a category; withholding it tests what this file is actually about —
whether the standard alone drives a reviewer to run the sweep.

10 fresh-context reps: haiku ×5, sonnet ×3, opus ×2. Weakest model carries the bar.

## Result — 10/10

Every rep named duplication explicitly and quoted at least two of the three
homes; several found all three and one caught two further duplicated rules the
fixture author did not plant deliberately. Several cited the exemption clause
verbatim while doing it.

Meta-test on the original 2/3 miss (agent resumed from its own transcript) came
back in the first class of the three-answer table — *not a documentation
problem*:

> "Neither. The standard's text was not the failure… There is no clearer way to
> flag 'this is a distinct required step'… The gap was not in the standard's
> presentation. It was in my execution: I never ran that pass."

It also corrected the premise of the question it was asked — the group-by-impact
rule has three homes, not the two the meta-test asserted.

## Why the score moved, and what that costs the earlier number

The 2/3 was measured on text that no longer exists, with 3 reps on one model.
Between then and now the entry gained its gate-form exemption — added during
tier 1 to stop false positives on `## Red Flags` lists. That clause did more
than remove noise: by naming what does *not* count, it sharpened what does, and
reviewers now cite it while making the catch.

So the REFACTOR debt was discharged as a side effect of an unrelated fix. That
is only knowable by re-running; it was not predictable, and the old 2/3 would
have kept looking like an open failure indefinitely.

## Recorded, not acted on

The meta-test's mechanism diagnosis is sharper than the three-answer table and
is worth keeping even though no text was written for it:

> "Duplication requires a different operation — not scanning the file once
> against many lenses, but scanning the file's own rules against each other…
> That's a search-and-collate pass, not a read-and-classify pass."

> "Higher-effort, novel findings crowded out the lower-effort,
> checklist-mandated one — which is backwards, since the checklist made the
> second one non-optional."

This suggests a live tension: the `Duplication` entry *describes* its sweep in
prose, while the standard's own failure table says a check that must never be
skipped earns "a recipe of deterministic primitives… plus fixed rules on their
output," not prose. The skill arguably fails its own table here.

It was not fixed. At 10/10 there is no failure behind the fix, and an argument —
however well-reasoned, however self-consistent — is not a baseline. If a future
run drops below the bar, this is the first hypothesis to test, and the recipe
form is the candidate to A/B against the current prose.
