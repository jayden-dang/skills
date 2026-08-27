# `map-features` — Recognized cards + OBS disposition + catalog sync modes

**Roster:** grok-4.6, grok-4.5.
**Scenario:** `.skills/_pending-reconcile/red-map-features-scenario.md`.

## Failure class

**Omits proposal kinds the brownfield reverse-track path needs.** v1.0.0 only
emitted Missing Feature code / Empty ROAD / OWNS gap / DEPENDS_ON. OBS promote
and Recognized-without-triad became first-class **gaps**, so `/map-features`
could not complete the user’s ask after `reconcile-features` indexed OBS.

Form: extend the kinds table (REQUIRED slots) + scan active OBS + forbid triad
scaffold **in dispose**.

### RED (v1.0.0)

| Run | Model | PROPOSAL_KINDS | HANDLES_OBS_PROMOTE |
|---|---|---|---|
| promote OBS + register SEND | grok-4.5 | none | no |
| same | grok-4.6 | none | no |

Verbatim: "Recognized capability and OBS promote are not table kinds, so they
are not proposed." / "Not a table kind. CODE unset → first-class gap."

Both: `WROTE_BEFORE_CONFIRM: no`, `TRIAD_SCAFFOLD: no` (ethics held; kinds
missing).

### GREEN (v1.1.0)

| Run | Model | PROPOSAL_KINDS | HANDLES_OBS_PROMOTE |
|---|---|---|---|
| same | grok-4.5 | Recognized capability, OBS disposition | yes |
| same | grok-4.6 | Recognized capability, OBS disposition | yes |

Both: `WROTE_BEFORE_CONFIRM: no`, `TRIAD_SCAFFOLD: no`. CODE remains
confirm-gated; flat Domain boundary deferred.

## Quality pass (v1.1.1) — author-skills wording sweep

User-invoked description reduced to one human line; catalog grammar pointed at
catalog-query.md; tombstone file named; promote/absorb CODE confirm clarified.

## Catalog sync modes (v1.2.0) — INDEX-only opt-in

**Decisions:** `.skills/research/2026-08-27-catalog-sync-index-only.md`.

**Baseline gap (no skill text for modes):** agents either refuse any triad touch
forever, or scaffold triads during dispose / when Catalog sync is unset —
both wrong for teams that sync INDEX only.

**Contract (GREEN text):**

- Modes `dispose` | `export` | `materialize`; export/materialize require
  `Catalog sync: index-only` in `docs/agents/project.md`.
- dispose never scaffolds triad; materialize writes Draft stubs from
  `templates/triad-stub/` only after confirm.
- export refreshes INDEX cells from local triad; never stages triad.
- configure-repo Decision L + gitignore snippet when index-only.

**Eval:** behavior assertions added for mode gating; dispose triad-scaffold
forbid retained.
