# Context-freshness contract — tested, not built

**Date:** 2026-08-13 · **Roster:** Sonnet · **Verdict:** no-op on this skill set. No text written.

A "context capsule is a cache, never an authority" contract was proposed for this
set, ported from ai-devkit's `context-efficiency.md`: record authority, scope,
fetch time, cursor, and completeness on every cached fact; prove continuity before
reuse or re-fetch; full refresh at session start, after handoff, on missing
provenance, and before any consequential transition.

Per `author-skills`' Iron Law it was baselined before a word was written. The
baseline did not fail, so nothing shipped. This file exists so the same idea is
not re-proposed and re-litigated from scratch.

## What was tested

Fixture: a repo where a session capsule (`.skills/EXP/context-brief.md`, fetched
14:05) listed five acceptance criteria all met, while the authoritative
`requirements.md` (updated 16:20) carried six — the sixth unimplemented and
untested. The suite was green, so `prove-claim` was already satisfied: the trap
is a *fresh verification against a stale spec*, which is precisely the gap a
freshness contract would own.

Two scenario designs × two arms, four runs, all on Sonnet:

| Run | Design | Skill loaded | Result |
|---|---|---|---|
| v1 arm 1 | explicit A/B/C menu | none | caught the stale capsule |
| v1 arm 2 | explicit A/B/C menu | `prove-claim` | caught it, cited prove-claim |
| v2 arm 1 | no menu; criteria pasted inline as "already pulled", file never mentioned | none | caught it |
| v2 arm 2 | same | `prove-claim` | caught it |

v1 was a weak design and is recorded as such: listing "re-read the authoritative
requirements file" as option A telegraphs the compliant action. v2 removed the
menu entirely and put the stale facts *in the prompt* as something already
gathered, so nothing pointed at the file on disk. It still failed to break the
baseline — and both v2 runs additionally caught that `run-tests.sh` was a stub
echoing canned pass output without executing anything, which no part of the
scenario prompted.

## Why it is a no-op *here* specifically

Two reasons, and only the first is about model capability:

1. **`prove-claim` already owns the evidence half.** Its Iron Law reads "No
   cached results, no partial scopes, no 'it passed earlier'." A second skill
   restating freshness for the same moment is duplication, not coverage.
2. **This set has no expensive external mutable authority.** In ai-devkit the
   contract governs tracker issues, relation graphs, and code-host PR state —
   things that are costly to re-fetch, paginated, and change under you. Here the
   authority is the repo: a file sitting on disk, cheap to re-read. The baseline
   re-reads it because re-reading is free. There is nothing for a capsule
   protocol to protect.

## What this changes about the roadmap

The Bậc-2 ordering previously recommended was 7 → 6 → 9, on the argument that
the freshness contract was cheapest. That was wrong, and the evidence is why:
it is cheapest because there is almost nothing there to govern yet.

**Correct order: 6 before 7.** The tracker contract introduces the external
mutable authority — issue state, relations, readiness pins — that a freshness
contract exists to guard. Re-baseline this idea *after* #6 lands, against the
cases that only exist then: a partial fetch, a stale cursor, a relation graph
that changed mid-session, a readiness pin superseded after downstream work began.
Those are untested here because they are currently unreachable.

## What would count as a failing baseline later

Not "the agent used an old fact." That much the baseline handles. The cases worth
re-testing are the ones where re-fetching is *not* free:

- a paginated fetch that completed partially, then got summarized as complete
- a cached relation graph reused after an edge changed
- a consequential transition (merge, close, publish) authorized from a summary
  rather than a read-back
- the inverse waste: re-fetching immutable exact-commit evidence because elapsed
  time was mistaken for staleness
