# B01 — write-design skill

Baseline for Task 1: editing `skills/spec/write-design/SKILL.md` to add a component-level
reuse-before-you-build discipline. Each scenario is walked by hand against the edited skill
body (this repo verifies skills by baseline scenario, not an automated harness — see Global
Constraints). RED = walked before the edit existed (no reuse ladder in the file, every
scenario fails by definition); GREEN = walked after editing, confirmed to hold.

## S1 — Ladder present & scan-fed

Step 2 presents a 7-rung reuse ladder — YAGNI cut, already-in-codebase reuse, stdlib/builtin,
platform/framework feature, already-installed dependency, one-line, only-then new code —
instructing the author to stop at the highest rung that holds. The ladder is fed by the
Step-1 scan digest ("what exists today") and is climbed only after the real flow the change
touches is understood, never as a substitute for understanding the problem first.

**Walk:** Read Step 2. Confirm the 7 numbered rungs appear in order, ending in "the minimum
new code that works." Confirm the "stop at the highest rung that holds" framing. Confirm a
sentence ties the ladder to the Step-1 scan digest, and a sentence states the ladder runs
only after the problem is traced/understood, not before.

`[REUSE-1.1] [REUSE-1.2]`

## S2 — Carve-outs

The ladder never licenses cutting a corner that matters: it must not prune away input
validation at trust boundaries, error handling that prevents data loss, security,
accessibility, or any behavior the requirements explicitly asked for.

**Walk:** Read the ladder paragraph following the 7 rungs. Confirm an explicit carve-out
sentence names all four: trust-boundary validation, data-loss-preventing error handling,
security, accessibility — plus explicitly-requested requirements behavior.

`[REUSE-1.3]`

## S3 — Reuse line + justification + new-dep callout, advisory

Every architecture section carries a `Reuse: <rung> — <concrete target>` line beside its
`Satisfies:` line, naming the highest rung that held and the concrete existing artifact
built on. A rung-7 (no lower rung held) line carries a one-line reason. A component that
introduces a brand-new third-party dependency gets a distinct callout, visible at the
approval gate. Both the `Reuse:` line and the new-dependency callout are advisory — never a
hard blocker — matching the Satisfies-line paragraph's existing house style.

**Walk:** Read the Satisfies-line paragraph in Step 2. Confirm the `Reuse:` line is
described alongside `Satisfies:`, with an example naming a rung and a concrete target.
Confirm the `Reuse: none — new code (rung 7)` form carries a required one-line reason.
Confirm the distinct new-dependency callout is named. Confirm a sentence states both are
advisory, never a hard blocker.

`[REUSE-2.1] [REUSE-2.2] [REUSE-2.3] [REUSE-2.4]`

## S4 — Step-4 reuse coverage

The Step-4 coverage self-check gains a bullet verifying every architecture section carries
a `Reuse:` line, and every rung-7 or new-dependency line carries its one-line
justification — alongside the existing "every ID appears in exactly one Satisfies line"
walk.

**Walk:** Read Step 4's opening coverage-check paragraph. Confirm a `Reuse coverage:`
bullet is present, stated separately from but alongside the Satisfies-line ID walk, and
that it checks both line presence and rung-7/new-dependency justification.

`[REUSE-4.1]`

## S5 — Chain stated, deletion test rescoped

Step 2 states the three-lever chain explicitly: the Step-1 **scan** gathers what exists,
the **ladder** decides whether to build, and the **deletion test** refines how deep to
build. The deletion-test paragraph is rescoped to apply only to rung-7 (new-component)
output — its opening sentence now reads "for a rung-7 new component" — while the Step-1
scan subagent and the deletion test's own mechanics are otherwise unchanged from before
this edit.

**Walk:** Read the ladder block's closing paragraph. Confirm it names scan / ladder /
deletion-test as three distinct levers with distinct jobs, in that order. Then read the
deletion-test paragraph immediately following: confirm its opening sentence now reads
"Design for depth: for a rung-7 new component, a module's interface…" and the rest of the
paragraph (the deletion-test question itself) is unchanged. Confirm the Step-1 scan
subagent instructions (Step 1) are untouched.

`[REUSE-5.1] [REUSE-5.2]`

## Coverage self-check

Every one of Task 1's 10 IDs appears in at least one tag above: 1.1, 1.2, 1.3, 2.1, 2.2,
2.3, 2.4, 4.1, 5.1, 5.2 — 10 of 10, none missing, none double-defined.
