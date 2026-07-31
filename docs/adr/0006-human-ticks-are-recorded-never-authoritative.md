# 0006 — A human dogfood tick is recorded, never authoritative

Moving human ticks out of browser `localStorage` and into the shared run file makes them
readable by the agent for the first time, which invites the obvious simplification: let a
tick be a `pass` carrying a `by: human` label. **Decision:** the run file gives each case two
field spaces that share no key — `run` for the agent's evidence-backed verdict, `human` for
the person's tick — and no code path promotes one into the other; `dogfood next` disregards
`human` entirely. **Why:** `drive-dogfood`'s Iron Law does not say "avoid localStorage", it
says the screen is necessary and not sufficient, and that is enforced mechanically by
`validate_mark` (`skills/acceptance/dogfood/scripts/dogfood:447`) refusing a `pass` with an
empty `--saw` or `--server`; a provenance label would make "the screen is sufficient" true
through a door that gate cannot see, and once written, runs recorded that way cannot be told
apart from probed ones afterwards. This **amends** decision D1 in
`docs/specs/2026-07-26-drive-dogfood/research.md:231` rather than reversing it — D1's
conclusion that a tick is never authoritative survives intact; only where the tick is stored
and who may read it change. The disjointness is also load-bearing beyond policy: it is what
lets two writers merge without conflict, and it is enforced at the HTTP boundary by an
allowlist that rejects any attempt to write `verdict`, `saw`, `server`, or `notes`.
