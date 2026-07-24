# ATTN behavioural scenarios

Agent-run scenarios. Each carries the requirement IDs it exercises as greppable
bare tokens.

## S1 — explicit range wins over the cascade

Given `/allocate-attention abc123..def456` on a repo whose `origin/HEAD` is set,
the allocation covers exactly that range and no default cascade runs. ATTN-2.1

## S2 — omitted range resolves to the branch point

Given `/allocate-attention` on a feature branch three commits ahead of `main`,
the range resolves to `merge-base(main, HEAD)..HEAD`. ATTN-2.2

## S3 — same range, same hits

Running `/allocate-attention` twice over an unchanged range and repo state admits
the identical binding set both times. ATTN-3.6

## S4 — agent add with a vacuous reason is refused

Given a unit the binding pass did not admit, an agent add reasoned "this looks
risky" is refused (no path from the unit's diff appears in the reason) and the
unit stays in the residue. ATTN-4.1 ATTN-4.3

## S5 — user add is unquestioned

The user names any unit; it joins the sample with no reason required. ATTN-4.4

## S6 — declining a bound unit

The user declines a B1 hit and asks "so we're good?". The unit is reported as
residue, not as sampled, and the reply does not call the range reviewed.
ATTN-4.5 ATTN-1.4

## S7 — written artifact only on request, never in-tree

Asked for the allocation "as a file at docs/attention.md", the skill hard-fails
naming the in-tree path and does not fall through to a temp location. ATTN-8.2

## S8 — allocation summary promoted at a terminal boundary

The user runs `/allocate-attention`, then reaches `finish-branch` in the same
session and chooses merge. The allocation summary ("2 of 5 units agent-verdict
only") is carried into `record-decision` as inline promotion substance the agent
already holds — no file is cited, no new emitter is added, and
`record-decision`'s caller set stays `{finish-branch, release}`. ATTN-10.3

---

# Executed acceptance run — 2026-07-24, range `72b8178..HEAD`

Driven against the real repository by following `SKILL.md` verbatim. Observed
results, not projections.

## A1 — range resolves and partitions

`default_base()` returned `main` via `refs/remotes/origin/HEAD`. 16 changed
files partitioned into 10 depth-2 unit keys, each file in exactly one.
ATTN-2.2 ATTN-2.3 ATTN-3.1

## A2 — clean tree emits no dirty notice

`git diff --quiet HEAD` clean and no untracked files, so the exclusion notice
was correctly *not* printed. ATTN-2.7

## A3 — binding pass under default globs UNDER-SAMPLED (finding, then fixed)

First run admitted 2 of 10 units — `.claude-plugin/plugin.json` (B2) and
`docs/specs` (B5) — leaving the 290-line `skills/review` unit, the feature
itself, in the residue. The default risk globs watch auth/migrations/payments;
this repo's risk is skill bodies. Fixed by declaring `## Attention signals` in
`docs/agents/project.md`; re-run admitted 5 of 10 including `skills/review` and
`skills/execution`. ATTN-3.2 ATTN-3.3 ATTN-3.4

## A4 — determinism

Two consecutive runs over the unchanged range admitted the identical set both
times; the floor ordering was likewise stable across two evaluations.
ATTN-3.6

## A5 — residue is itemised and counted

Residue reported as 5 of 10 units, each named with its file and line counts,
labelled *agent verdicts only*. ATTN-7.1 ATTN-7.2

## A6 — one allocation for the whole range

A single allocation covered all 10 units; no per-unit presentation was emitted
even with 5 binding hits. ATTN-7.4

## A7 — empty range hard-fails

`git rev-list --count HEAD..HEAD` returned `0`; the run stopped with no
allocation rather than substituting another range. ATTN-2.6

## A8 — in-tree output path hard-fails

A requested path under `git rev-parse --show-toplevel` was rejected outright
with no fallthrough; a `/tmp` path was allowed. ATTN-8.3

## A9 — floor pick is exactly one and total

On a slice where nothing bound, the three-key order produced exactly one pick,
identically across runs. ATTN-5.1 ATTN-5.2

## A10 — nothing written by default

The whole run wrote no file. ATTN-8.1

## Not exercised — open risks

- ATTN-4.1 ATTN-4.3 agent-add reason tests (distinct + concrete) — needs a live
  interactive run with a real agent proposing an add.
- ATTN-6.1 ATTN-6.2 ATTN-6.3 ATTN-6.4 claim / refuter / disposition capture —
  needs a human in the loop; not mechanically drivable.
- ATTN-8.2 writing the artifact on request — only the path *rejection* half was
  exercised.
- ATTN-2.4 base-resolution hard-fail — this repo always resolves a base.
