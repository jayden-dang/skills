# `polish-diff`

> Four cleanup agents read the diff from four angles; you apply what survives triage. The deliverable is cleaner code that behaves identically — not a report, and not a bug fix.

|  |  |
|---|---|
| **Bucket** | review |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | the pinned diff (`git diff @{upstream}...HEAD`, falling back to `main...HEAD`, then `HEAD~1`, plus `git diff HEAD` when the tree is dirty), the suite covering the changed files |
| **Writes** | the changed files themselves — this skill applies its findings |
| **Calls** | [`test-first`](test-first.md) (its refactor discipline is the apply step), [`prove-claim`](prove-claim.md) (before claiming behavior held) |
| **Called by** | [`build-in-waves`](build-in-waves.md), [`build-by-story`](build-by-story.md), [`build-inline`](build-inline.md) — all three carry it in their Setup Todos gate |

## When it fires

When changed code needs a quality cleanup **actually applied** rather than reported: code that reimplements a helper the repo already has, needless complexity, dead code, wasted work or repeated I/O, a bandaid fix at the wrong depth. It is the last pass over a diff, branch, or PR before merge.

It is not the skill for a correctness bug, a crash, or a merge verdict — those are [`inspect-change`](inspect-change.md) and [`root-cause`](root-cause.md).

## Two boundaries, both load-bearing

```
1. Behavior does not change. The suite green before the cleanup is green after,
   and no test is edited to make that true.
2. Correctness bugs are out of scope. Do not hunt them, and do not fix the ones
   you trip over.
```

The second is the one that feels wrong in the moment, and the rationalization table answers it directly: *"That's obviously a bug — it'd be silly to leave it"* → then it deserves a real review, not a drive-by fix buried in a cleanup commit. **A diff that both restructures and repairs can be reviewed as neither.** The bug gets named for `inspect-change` and left alone.

## The four angles

All four run in **one message** so they are concurrent and neither pollutes the other's context. Every agent is read-only; the controller applies. Each returns `file:line`, a one-line summary, **the concrete cost**, and **the named replacement** — a finding with no named replacement is not actionable and the agent drops it.

| Angle | Looks for |
|---|---|
| **Reuse** | new code reimplementing something the codebase already has — names the existing helper |
| **Simplification** | redundant or derivable state, copy-paste with variation, deep nesting, dead code left behind |
| **Efficiency** | redundant computation, repeated I/O, sequential independent operations, blocking work on a hot path; also long-lived closures holding a whole enclosing scope alive |
| **Altitude** | changes made at the wrong depth — a special case layered onto shared infrastructure is the tell that a fix did not go deep enough |

A fifth pass, **comment discipline**, applies the default-zero rule: delete comments that restate the next line, narrate control flow, cite requirement IDs, or say "as per the plan"; keep non-obvious invariants, hazards, and protocol constraints.

## The test-file rule

This is where cleanups quietly become behavior changes, so the rule is narrow and explicit. Re-running step 2's *exact* command must be green, and the only permitted test-file change in the diff is a **deletion** meeting all three conditions: the code it pinned was removed as dead, the behavior is still covered by a test you **name**, and the deletion is stated in the report.

A test may never be rewritten, retargeted, renamed, or moved. The rationalization table calls out the most reasonable-sounding version of the violation:

> *"I only repointed the test at the canonical function — identical assertion, no coverage lost"* → You deleted the test that stood in the way and wrote a new one that does not. Keep the old symbol as a thin alias instead: the duplicated rule still dies, and the suite never moves.

## Finding nothing is a result

If nothing survives triage, the report says the code was already clean. **That is a successful run, not a failed one** — and manufacturing a finding to justify the pass is the one outcome worse than no findings at all.

Every dropped finding is recorded with its one-line reason, because a silently discarded finding is indistinguishable from a finding you never received. Drops that were judged real and deliberately deferred are exactly the intake for [`record-debt`](record-debt.md).

## Without subagents

The inline fallback runs the four angles sequentially in one context, closing one out completely — findings written down — before opening the next. The whole value of four separate contexts is that no angle sees another's conclusions; finishing one before starting the next is the closest single-context approximation. Step 6 is not optional just because the review was cheaper.

## See also

- [`inspect-change`](inspect-change.md) — the two-axis merge verdict, and where correctness findings go
- [`record-debt`](record-debt.md) — banks the findings this skill deliberately dropped
- [`test-first`](test-first.md) — the refactor discipline the apply step runs on
