# FSUB scenarios (ID index)

Story 1 load subgraph: FSUB-1.1 FSUB-1.2 FSUB-1.3 FSUB-1.4 FSUB-1.5 FSUB-1.6 FSUB-1.7 FSUB-1.8 FSUB-1.9 FSUB-1.10 FSUB-1.11 FSUB-1.12 FSUB-1.13 FSUB-1.14 FSUB-1.15 FSUB-1.16

Story 2 denoise: FSUB-2.1 FSUB-2.2 FSUB-2.3 FSUB-2.4 FSUB-2.5 FSUB-2.6

Story 3 legacy Files: FSUB-3.1 FSUB-3.2 FSUB-3.3 FSUB-3.4

Story 4 harden grammar: FSUB-4.1 FSUB-4.2

Story 5 no-op: FSUB-5.1 FSUB-5.2 FSUB-5.3

Story 6 map-features: FSUB-6.1 FSUB-6.2 FSUB-6.3 FSUB-6.4 FSUB-6.5 FSUB-6.6

Story 7 guards: FSUB-7.1 FSUB-7.2 FSUB-7.3 FSUB-7.4 FSUB-7.5 FSUB-7.6 FSUB-7.7

Story 8 NFR: FSUB-8.1 FSUB-8.2 FSUB-8.3

## FSUBR Wave A — P1 OWNS (Task 1)

P1 multi-block + classifier: FSUBR-2.1 FSUBR-2.2 FSUBR-2.3 FSUBR-2.4 FSUBR-2.5 FSUBR-2.6 FSUBR-2.7 FSUBR-2.8 FSUBR-2.9

Reliability notes: FSUBR-10.3 FSUBR-10.4

## FSUBR Wave A — Derivation snapshot (Task 2)

Two-stage snapshot + read-once ledger + pure queries: FSUBR-10.1

## FSUBR Wave A — Neighbors envelope 1.1 (Task 3)

Path/term-grounded neighbors: FSUBR-1.1 FSUBR-1.2 FSUBR-1.3 FSUBR-1.4 FSUBR-1.5 FSUBR-1.6 FSUBR-1.7 FSUBR-1.8 FSUBR-1.9 FSUBR-1.10 FSUBR-1.11 FSUBR-1.12 FSUBR-9.3

## FSUBR Wave A — cluster query (Task 4)

Query-local cluster digest: FSUBR-3.1 FSUBR-3.2 FSUBR-3.3 FSUBR-3.4 FSUBR-3.5 FSUBR-3.6 FSUBR-3.7 FSUBR-3.8 FSUBR-3.9 FSUBR-3.10 FSUBR-3.11 FSUBR-3.12 FSUBR-3.13 FSUBR-3.14 FSUBR-3.15

## FSUBR Wave A — callers + grounded claims (Task 5)

Grounded claims protocol: FSUBR-4.1 FSUBR-4.2 FSUBR-4.3 FSUBR-4.4

clarify-decisions nested/standalone package: FSUBR-5.1 FSUBR-5.2 FSUBR-5.3

design-solution Step 1 fresh retrieval: FSUBR-6.1

plan-tasks blast_radius + cluster(feature CODE): FSUBR-7.1 FSUBR-7.2

root-cause after Phase 2 only (never RED loop): FSUBR-8.1 FSUBR-8.2

frame/inspect schema 1.1 + package/no-cache guards: FSUBR-9.8 FSUBR-9.11 FSUBR-9.12 FSUBR-9.13 FSUBR-9.14 FSUBR-9.15

## FSUBR Wave A — guide, inventory, carry-forward guards (Task 6)

No GRAPH.md / no depends_on / oracle pack-only: FSUBR-9.1 FSUBR-9.2 FSUBR-9.4

audit-trace E-codes unchanged; pathfind separate; P3–P5 no-op: FSUBR-9.5 FSUBR-9.6 FSUBR-9.7

Guide + inventory (cluster + callers): FSUBR-9.9 FSUBR-9.10

Passive path/prose data (not instructions): FSUBR-10.2

## FSUB-1.2 skill-path dual-run

Two independent load-subgraph runs against the same frozen fixture (following passes.md only) MUST yield the same edge set and seed set. reference_derive is the oracle for expected math; the skill MUST NOT import it.

## FSUB-1.3 no materialization

load-subgraph MUST NOT write docs/specs/GRAPH.md or any committed graph projection.
