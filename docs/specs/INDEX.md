# Spec Index

Feature-code registry: every requirements.md registers its code here before use.
Codes are 2-12 chars, A-Z0-9, start with a letter, unique forever (never reuse a
retired code).

**Roadmap item** binds this feature CODE (delivery unit) to the `ROAD-N` program **slot** it
implements, when the project has a `docs/roadmap/INDEX.md`. Write `—` when there is no
roadmap layer, or when this work was not planned as a roadmap item. At most one live CODE
may name a given ROAD (`R6`). The column is what lets `refresh-roadmap-status` join plan to
spec; `specify-behavior` is the only writer of any cell in this table.

This **flat** table is the default. Agents query it; they must not assume it stays small
enough to paste whole into context. Optional later scale-out: replace this table with a
Domain router plus `docs/specs/catalog/{domain}.md` shards.

| Code | Feature | Spec | Status | Roadmap item |
|---|---|---|---|---|
| DBGREADY | Debugging decision readiness | ./2026-08-27-debugging-decision-readiness/ | Draft | — |
