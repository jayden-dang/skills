# Spec Index

Feature-code registry: every requirements.md registers its code here before use.
Codes are 2-12 chars, A-Z0-9, start with a letter, unique forever (never reuse a
retired code).

**Roadmap item** binds this feature CODE (delivery unit) to the `ROAD-N` program **slot** it
implements, when the project has a `docs/roadmap/INDEX.md`. Write `—` when there is no
roadmap layer, or when this work was not planned as a roadmap item. At most one live CODE
may name a given ROAD (`R6`). The column is what lets `refresh-roadmap-status` join plan to
spec; `specify-behavior` is the only writer of any cell in this table.

| Code | Feature | Spec | Status | Roadmap item |
|---|---|---|---|---|
| <CODE> | <Feature name> | ./<YYYY-MM-DD>-<feature>/ | Draft | — |
