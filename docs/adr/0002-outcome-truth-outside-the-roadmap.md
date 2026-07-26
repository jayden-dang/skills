# 0002 — Milestone outcome truth lives outside the roadmap

`docs/roadmap/INDEX.md` owns planning intent only, so a milestone's verdict — was
the outcome achieved — had no home. **Decision:** outcome truth lives in
append-only `docs/roadmap/assessments/<MILE-N>.md` files, one assessment event
per block, each pairing an agent-authored verdict with a separately attributed
human disposition; the roadmap records only `Commitment: Closed` and the closing
revision. **Why:** the alternatives each broke something — a slot in the roadmap
block collided with its intent-only ownership split, reusing `record-decision`
meant reopening a caller set deliberately closed to `finish-branch` and
`release`, and a conversational report let a one-time judgment die on compaction.
