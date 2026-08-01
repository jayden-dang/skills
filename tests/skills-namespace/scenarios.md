# SKNS scenarios — greppable requirement tokens

Every Approved `SKNS-N.M` appears once below for audit-trace coverage.

## Layout

- **SKNS-1.1** Feature-scoped ephemera writes under `.skills/<CODE>/`
- **SKNS-1.2** Directory segment is Feature code only (no long slug)
- **SKNS-1.3** CODE resolve: brief/plan → Feature code line → INDEX
- **SKNS-1.4** Progress ledger is `.skills/<CODE>/progress.md` only for that feature

## Shared

- **SKNS-2.1** pathfind stays under `.skills/pathfind/`
- **SKNS-2.2** research stays under `.skills/research/`
- **SKNS-2.3** decisions stay under `.skills/decisions/`
- **SKNS-2.4** pr-packages stay under `.skills/pr-packages/<stable-id>/`

## Pre-CODE / adhoc

- **SKNS-3.1** Pre-CODE feature ephemera under `.skills/_pending-<slug>/`
- **SKNS-3.2** On INDEX registration, promote pending → `.skills/<CODE>/`
- **SKNS-3.3** Ad-hoc work under `.skills/_adhoc/<short-slug>/`

## Legacy

- **SKNS-4.1** Legacy root may be read once for resume
- **SKNS-4.2** New writes never grow bare-root feature dumps
- **SKNS-4.3** No auto-migrate of consumer trees

## Contract surface

- **SKNS-5.1** Execute/ship/track prescribe CODE paths for progress/brief/report/review/notes
- **SKNS-5.2** Discovery/spec prescribe CODE or pending for digests
- **SKNS-5.3** Acceptance/product-flow under CODE
- **SKNS-5.4** AGENTS/guide describe per-CODE layout

## Guards

- **SKNS-6.1** Shared roots continue for pathfind/research/decisions/pr-packages
- **SKNS-6.2** Resume trusts `.skills/<CODE>/progress.md` + git log
- **SKNS-6.3** `.skills/` remains git-ignored before writes
- **SKNS-6.4** audit-trace / load-subgraph semantics unchanged (no layout E-codes)

## NFR

- **SKNS-7.1** Two features → two distinct progress ledgers
