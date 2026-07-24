---
name: allocate-attention
description: >
  Use when a finished branch or PR holds more change than you can read and you
  must decide what gets human eyes — produces an attention allocation over a
  range: a bounded sample set plus the explicit unsampled residue. Triggers on
  /allocate-attention, "what should I review first", "I can't review all of
  this", "spot check this PR", "too much to review", "sample this branch",
  "which parts actually need me". Not for a Standards+Spec review verdict
  (code-review), a comprehension packet (comprehend-change), verify evidence,
  polish cleanups, or a ship menu.
disable-model-invocation: true
---

# Allocate attention

Turn a resolved range into **one** allocation: a sample set admitted by fixed
rules, and the residue nobody looked at, named as such.

## Posture

This skill is an aid, never a gate. It blocks no merge, no PR, no release, and
no decision record. A range with no allocation is simply a range with no
allocation — that **carries no adverse claim** about the work.

Not running it also never licenses the claim that a range was human-sampled.
Absence is absence.

## Range resolver

**Explicit range wins.** A commit, `base..head`, or a path-filtered range the
user names is used verbatim — skip the cascade below.

Otherwise:

```
BASE  = default_base()
RANGE = merge-base(BASE, HEAD)..HEAD
```

`default_base()` — local git only, **no network**, no `gh`:

1. `git symbolic-ref --quiet --short refs/remotes/origin/HEAD` → strip `origin/`
2. else the first of `main`, `master` that `git rev-parse --verify` accepts
3. else **hard-fail**: ask the user to name an explicit base. Do not
   confirm-and-guess.

**Empty range.** `git rev-list --count RANGE` returning `0` → **hard-fail**
naming the empty range. Produce no allocation. Never substitute a different
range — not recent commits, not the branch name.

**Dirty tree.** When `git diff --quiet HEAD` exits non-zero, or
`git ls-files --others --exclude-standard` is non-empty, print exactly one
line — `uncommitted work is not included in this allocation` — then continue
over the committed range.
