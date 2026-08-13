# Tracker contract (Bậc 2 #6) — what was built, and what was not

**Date:** 2026-08-13 · **Roster:** Sonnet · **Outcome:** one rule shipped into
`prove-claim`. No new skill. Two of the three proposed parts were not written,
because they did not fail.

The proposal, ported from ai-devkit's `delivery-workflow`, had three parts:

1. **write → read-back** — never claim a tracker change from the write's own
   success signal.
2. **continuous reconciliation** — record every material discovery on its owning
   issue as it arises, not at ship time.
3. **readiness vocabulary** — *execution-ready* (downstream may proceed) vs
   *ship-ready* (may merge), each with its own evidence bar.

Each was baselined before anything was written. Only part 1 failed.

## Part 1 — shipped

3/3 baseline reps claimed a ticket was updated and moved to `in-review` on the
strength of a `✓` line from a write command that wrote nothing. The ticket file
was byte-identical to its starting state in all three. Full record, including a
contaminated first batch that was discarded, in
`skills/execution/prove-claim/TESTS.md`.

Shipped as one row in `prove-claim`'s `Claim → evidence` table plus a red flag,
and — after meta-testing found the 4-step gate reads as a single command — one
clause in IDENTIFY saying a claim about a *record holding a change* resolves to a
pair, the write and the read. 3/3 GREEN, plus a confirmation run after the fix.

**No new skill.** `prove-claim` already owned the trigger ("about to say something
that implies success") and already had a row of exactly this shape for subagent
reports. A separate tracker skill would have been a second home for one rule.

## Part 2 — not written, did not fail

Every baseline rep, with no skill loaded, wrote a substantive comment about the
material discovery (an acceptance criterion the existing implementation could not
satisfy) and escalated it to the user unprompted. The failure a reconciliation
loop exists to prevent — valuable delivery knowledge left only in chat — did not
reproduce. Writing the rule anyway would have been a no-op, and `author-skills`
is explicit that text with no observed failure behind it does not ship.

What was *not* tested, and would be the place to look next: reconciliation across
a **session boundary**, where the discovering context is gone. Every rep here
discovered and reported inside one session, which is the easy case.

## Part 3 — not written, unreachable

The readiness vocabulary distinguishes "a blocker is done enough that dependent
work may start" from "this may merge." That distinction only pays for itself when
several tracked issues execute concurrently against each other's partial output —
Bậc-2 #9, cluster mode, which does not exist here. `build-in-waves` parallelises
tasks *inside* one feature against one plan, where the frontier is the plan's own
dependency edges and no cross-issue readiness question arises.

There is currently nothing in this set that would consume the vocabulary, so
there is no scenario in which an agent can misuse it. Re-baseline with #9.

## Correction this run produced

The Bậc-2 ordering was revised once already, after #7 came back a no-op: from
7 → 6 to 6 → 7. This run refines it again. #6 turned out to be mostly two parts
that depend on things that do not exist yet:

- part 2 needs **cross-session** delivery work to be a real risk
- part 3 needs **#9 cluster mode** to have a consumer

So #6 is now largely discharged, and #7's re-baseline condition is unchanged —
it still waits on an expensive external mutable authority, which part 1 alone
does not introduce. The next item with an actual failing baseline behind it is
more likely **#9** or **#5** (vendoring, which is mechanical and needs no
behavioral baseline at all) than either remaining half of #6 or #7.
