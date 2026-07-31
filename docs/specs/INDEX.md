# Spec Index

Feature-code registry: every requirements.md registers its code here before use.
Codes are 2-12 chars, A-Z0-9, start with a letter, unique forever (never reuse a
retired code).

**Roadmap item** binds the feature to the `ROAD-N` it implements, when the project has a
`docs/roadmap/INDEX.md`. Write `—` when there is no roadmap layer, or when this work was
not planned as a roadmap item.

| Code | Feature | Spec | Status | Roadmap item |
|---|---|---|---|---|
| RMAP | Roadmap layer — milestone intent and derived roadmap health | ./2026-07-25-roadmap/ | Implemented | — |
| ASSESS | Milestone assessment — the pre-close outcome gate and its append-only record | ./2026-07-26-milestone-assessment/ | Implemented | — |
| XPLN | Explain-change — team-shared HTML pitch+map packet under docs/explainers/ | ./2026-07-27-brief-team/ | Implemented | — |
| PCHG | Prepare-change — reviewer-facing commit and PR authoring handed to land-branch | ./2026-07-28-package-change/ | Approved | ROAD-3 |
| DFSYNC | Review Product Flow sync — single JSON run artifact plus optional local serve layer | ./2026-07-30-review-product-flow-sync/ | Implemented | — |
| PFIND | Pathfind layer — multi-session decision map (Layer 0) before program/delivery | ./2026-07-31-pathfind/ | Approved | — |
