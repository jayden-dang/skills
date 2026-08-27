# Learning ledger

## Contents

- [Location](#location)
- [States](#states)
- [Checkpoint close](#checkpoint-close)

## Location

`.skills/study/<slug>/ledger.md` (+ optional `checkpoints/*.md`) under the
**consuming** repo. Gitignored via `.skills/`. Never write under `docs/`.

## States

| State | Meaning |
|---|---|
| `visited` | Stop opened; no graded production yet |
| `in_progress` | Checkpoint/journey open |
| `demonstrated` | Graded production closed **and** claim verified |
| `contradicted` | Claim checked against evidence and failed |
| `unverified` | Claim stated but no readable oracle yet |
| `open_gap` | Missing knowledge; non-blocking unless marked blocking |

Missing evidence must **not** be recorded as `contradicted`.

## Checkpoint close

A **semantic checkpoint** is one mental unit (e.g. finished neighbor cluster,
finished journey leg) — **not** “N files”.

On close, require **exactly one** graded production:

1. Purpose in the learner’s own words
2. One reachability claim
3. Optional blast prediction

Verify the claim with **source, test, or runtime** evidence. `load-subgraph` is
advisory context only — never sole proof.

- Pass → `demonstrated` + evidence cites
- Fail → `contradicted` + evidence + `next_probe` (no teach-pack loop)
- Atlas-only or abandoned mid-stop → may end without production; **never**
  `demonstrated`
- When the user asked the agent to walk the tour for them, an agent-authored
  production may close as `demonstrated` **only** with the same
  source/test/runtime cites — never from chat paraphrase alone
