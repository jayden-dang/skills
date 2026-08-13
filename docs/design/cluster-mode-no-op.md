# Cluster mode (Bậc 2 #9) — tested, not built

**Date:** 2026-08-13 · **Roster:** Sonnet · **Verdict:** no-op on the part that
is testable; the rest is a capability question, not a skill-authoring one.

## What was proposed

Ported from ai-devkit's `cluster-mode.md`: deliver several dependent tracked
issues concurrently — transitive dependency closure, a readiness frontier
recomputed after every completion, one worktree per issue, and **pinned handoff
commits** as immutable evidence, where publishing a replacement pin revokes
execution-ready status for every dependent built on the old one.

## What already existed

Surveying first, per the lesson from #7:

- `build-in-waves` already pins a wave base (`WBASE=$(git rev-parse HEAD)`),
  demotes overlapping file scopes to serial, and barriers before merging in task
  order. Intra-feature parallelism is covered.
- `publish-issues` already carries a frontier concept: blocking edges, publishing
  in dependency order, and a `ready-for-agent` label that "must never sit on a
  slice whose blockers are still open," gated on whether the tracker *enforces*
  the edge.
- Nothing records or verifies a base SHA **across** branches.
  `isolate-workspace` runs `git worktree add "$DIR/<branch>" -b "<branch>"` with
  no base argument at all.

So the genuine gap was the cross-branch half: dependent work sitting on a base
that its blocker's branch no longer contains.

## What was tested

The sharpest testable claim in #9, and the one ai-devkit states outright — *"a
handoff pin is immutable evidence, not a floating branch."*

Fixture: `feat/profile` branched from `feat/auth`'s first commit. `feat/auth`
was then reset and recommitted during review, changing `getSession(token)`
into `getSession(token, opts) -> Session | null`. `feat/profile`'s base is
orphaned; its suite is **green in isolation** because it carries its own copy of
the superseded `session.ts`, and `--experimental-strip-types` never type-checks
the signature mismatch. Task: get the branch ready for a PR against main.

**Clean run: 3/3 caught it.** All three drew the divergence graph, identified the
reset-and-replace on `feat/auth`, named both consequences (a superseded
`getSession` landing in main, and `displayName` breaking on the new contract),
and refused the PR. One rebuilt the branch on `feat/auth`'s tip in a scratch
worktree and ran `tsc --strict` to produce the exact TS2554 / TS18047 errors.

No skill text was written.

## Three contaminated fixtures before that result

Recorded because the failures were mine, and each was a different mechanism:

1. **The fixture's own docs telegraphed the answer.** `CLAUDE.md` said "review
   rework rewrites branch history." Two of three reps cited that exact sentence
   as what tipped them off.
2. **Removing the giveaway created a new one.** Amending it out put the
   *deletion* of that sentence into the branch diff, where all three reps found
   it and one called it "the one sentence that would have flagged exactly this
   situation."
3. Only rebuilding the repository from the first commit, with the line never
   present, produced a fixture that tested what it claimed to.

The general lesson, beyond the isolation rule already recorded twice in this
repo: **a fixture can leak its answer through its own documentation, and editing
the leak out can leak it again through the diff.** Build the fixture clean from
the initial commit rather than patching a dirty one.

## The part that is not testable this way

Frontier scheduling, worktree-per-issue orchestration, and pin publication are a
**capability** — something the set cannot currently do — not a rule an agent
rationalizes past. `author-skills` tests whether text changes behavior; it has
nothing to say about a feature that does not exist, and no RED run can manufacture
a baseline failure for one. Whether to build a cluster orchestrator is a product
decision, and it should be taken on those grounds rather than waiting on evidence
this method cannot produce.

Worth weighing against: the drift this orchestration would guard against is
already caught by the baseline, and `publish-issues` already refuses to mark work
grabbable while its blockers are open. The orchestrator would be buying
concurrency, not safety.

## The pattern across Bậc 2

Three items tested, two no-ops (#7, #9), one narrow real finding (#6's
write-then-read-back, 3/3 baseline failure). The original analysis ranked these
by how much *text* ai-devkit devotes to them, which turned out to be a poor proxy
for whether the failure reproduces here. Two reasons recur: this set's authority
is usually the repo itself, which is cheap to re-read, and a modern model already
cross-checks git state without being told to.

The one that did fail had a distinguishing shape worth reusing as a filter: an
**external system that reports success without being observable** — the tracker
CLI printing `✓` while writing nothing. Where the agent can see the ground truth
for free, it checks; where a tool stands between it and the truth and claims
success, it believes the tool. Future ports from ai-devkit should be triaged on
that question first.

Remaining Bậc-2 item: **#5 vendoring**, which is mechanical — a lockfile format
and a reconcile procedure — and needs no behavioral baseline at all.
