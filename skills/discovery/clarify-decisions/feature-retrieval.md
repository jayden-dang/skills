# Feature retrieval package

Load this file only for feature interviews involving neighbors, overlap, or
reuse. Hold a `load-subgraph` package containing envelope, seeds, fingerprints,
schema, and recipe for Territory and grounded claims.

| Mode | Rule |
|---|---|
| Nested under a parent package | Reuse it while seeds, source fingerprints (`sha256` + present), schema, and recipe remain valid. Otherwise REQUIRED SUB-SKILL: use `load-subgraph`. |
| Standalone | Before the first card, REQUIRED SUB-SKILL: use `load-subgraph` with terms, paths, and CODE seeds. |
| Interview in progress | Rederive when source inputs change, material scope/terms/paths change, or fingerprints differ. Do not re-run per card while the package remains valid. |

Do not create an on-disk session cache. For every conclusion derived from the
package, follow
`skills/execution/load-subgraph/references/grounded-claims.md`.
