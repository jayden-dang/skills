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
