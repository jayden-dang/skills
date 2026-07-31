# RED baselines — ASSESS

Recorded failures that justify each behavior the skill adds. Audit Trace-ignored: the requirement
IDs here are baseline records, not coverage.

**Disclosure — the fresh-agent baselines below were not run.** This feature was executed
inline, with no subagent dispatch available, so the "point a fresh agent at the fixture"
baselines that RMAP recorded could not be reproduced here. What *is* recorded is the
mechanical RED for every task: the failing test output captured before each implementation
step. Where a baseline is reasoned rather than observed, it says so. Treat the reasoned ones
as weaker evidence than RMAP's observed ones.

## Task 1 — shared findings reference

**Observed RED.** `python3 -m unittest tests.test_roadmap_findings_reference` →
`FileNotFoundError: templates/roadmap-findings.md`, 4 errors.

The pre-existing state also failed `test_check_roadmap_defers_instead_of_restating`
independently: `status-roadmap/SKILL.md` carried the `R1`–`R11` table inline, so the
`^\| \*\*R\d+\*\* \|` search matched. That is the duplication ASSESS-5.3 removes.

## Task 2 — ladder rung

**Observed RED.** `python3 -m unittest tests.test_priority_ladder` → 1 failure, 2 errors:
`AssertionError: 'all bound and `Shipped`' not found ... ladder row missing`, plus
`StopIteration` from the two tests that look the row up.

**Reasoned baseline (not run).** Before the rung existed, a `Committed` milestone whose
members were all `Shipped` fell through row 7 and matched the old row 8 — "no `Committed`
milestone, a `Planned` one exists" does not hold, so it reached row 9 and reported the
roadmap complete, or stopped with no action. Either way the close was never named. That gap
is what ASSESS-5.2 closes.

## Task 3 — assessment artifact template

**Observed RED.** `python3 -m unittest tests.test_assessment_artifact` →
`FileNotFoundError: templates/milestone-assessment.md`, 8 errors.

## Task 4 — scope resolution pass

**Observed RED.** `python3 -m unittest tests.test_assessment_artifact` →
`FileNotFoundError: skills/track/assess-milestone/SKILL.md`, 1 error, after the eight
template tests had gone green.

**Observed RED, second kind.** `python3 scripts/lint-handoffs.py` failed on the first draft
of the skill body:

```
DEAD HAND-OFF — a skill directs the agent to invoke a user-invoked skill:
  skills/track/assess-milestone/SKILL.md:164
    assess-milestone -> status-roadmap (user-invoked)
    invoke `/status-roadmap`
```

The offending line was a **red flag telling the agent not to do it** — "You are about to
invoke `/status-roadmap` … rather than name them". The linter matches the phrasing, not the
intent, and it is right to: a body that contains the invoking phrase teaches it regardless of
the surrounding negation. Reworded to "run … yourself rather than naming them for the user".
Worth keeping as evidence that ARCH-5's mechanical guard catches its own authors.

**Reasoned baseline (not run).** Against fixture `ambiguous-binding`, an agent asked to close
`MILE-1` with no skill present has no rule forcing it to resolve `ROAD-1` to exactly one
feature code. The expected failure is that it picks one of `CAP`/`CAP2` — most likely the
first row — and proceeds to close, because nothing tells it two claims is not a binding.
ASSESS-1.6 is what withholds instead.
