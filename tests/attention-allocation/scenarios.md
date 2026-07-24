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
