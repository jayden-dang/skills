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
