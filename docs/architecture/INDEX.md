# Architecture: Agentic Development Skill Set

Status: Approved
Date: 2026-07-12

The architecture spine for this repo: the invariants that keep the skills consistent
with each other. Feature `design.md` files cite the ones they rely on as
`Respects: ARCH-N`; the `trace` check verifies those citations point at a live
invariant. (This spine is itself the first consumer of the PROJDOC project-docs layer —
we dogfood it.)

## Invariants

- **ARCH-1** The `trace` check is deterministic — `grep` and set-difference only. It
  reports textual presence and referential integrity; it never judges whether a test or
  design *meaningfully* satisfies what it cites.
- **ARCH-2** Every project-context consult is optional — an observable-predicate check
  plus a no-op-if-absent branch, never a new hard gate. A repo that opts into nothing
  behaves exactly as before.
- **ARCH-3** A consuming repo installs nothing executable beyond the session-start hook —
  no vendored scripts, linters, or CI. The methodology is pure `SKILL.md` and markdown.
- **ARCH-4** An Approved requirement or architecture invariant ID is immutable — retire
  it by strikethrough, never renumber or repurpose it.
- **ARCH-5** A user-invoked skill is never a `REQUIRED SUB-SKILL` target; only
  model-invoked skills compose as sub-skills. User-invoked skills are named for a human
  to run (e.g. `/establish-project`).

## Domains

None — the invariant set is small enough to live in this single index.
