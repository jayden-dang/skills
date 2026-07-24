# Architecture: Skills

Status: Approved
Date: 2026-07-22

<!--
The architecture SSOT for this skill set.

1. This file is the INVARIANT SPINE — greppable **ARCH-N** rules that feature
   design.md files cite as `Respects: ARCH-N`. The `trace` check verifies those
   citations (E4/E5/W3). Semantic conformance is advisory via `check-invariants`.
2. Domain files under this directory hold the rest of the system design (SSOT;
   no parallel design doc at repo root). Product north star remains
   docs/product/vision.md; engineering house rules remain docs/product/guidelines.md.

Rules for invariants:
- ID grammar: **ARCH-<n>**, flat and repo-wide (unique forever, never reuse).
- One rule per invariant. If it needs "and", it is usually two invariants.
- IDs are immutable once relied upon. Retire by strikethrough, never renumber.
  Example form (do NOT use a real struck **ARCH-N** token in comments — it pollutes
  the retired-set grep): write "struck ARCH-N superseded by ARCH-M" in prose only.
- Large project? Domain files hold narrative design; the ARCH-N namespace stays flat
  and is defined only under "## Invariants" below (do not re-bold ARCH definitions
  in domain files).

Dogfood set: ARCH-1..6 = determinism-of-trace, optionality, zero-tooling,
ID immutability, sub-skill composition, participant boundary.
-->

## Invariants

- **ARCH-1** Trace and other vertical checks MUST be exact `grep`/`git`/file-read passes with fixed extraction rules and set differences — never an LLM judgment of whether a test "really" covers an ID.
- **ARCH-2** Optional project layers and config sections MUST no-op when absent: skills CONTINUES TO run without inventing vision, architecture invariants, team roster, or other standing facts that were never written.
- **ARCH-3** Consumer-repo adoption MUST require only the skills (plugin or npx) and markdown config — never mandate Python, vendored linters, CI jobs, or git-hook wiring for the full methodology; any hard headless gate is an optional documented add-on only.
- **ARCH-4** Requirement IDs (`CODE-N.M`) and architecture IDs (`ARCH-N`) are immutable once defined: never renumber or reuse; retire only by strikethrough; every task, test, commit trailer, and `Respects:` line MUST use the same greppable string as the definition.
- **ARCH-5** User-invoked skills may invoke model-invoked skills only; model-invoked skills must never invoke user-invoked skills; agents must never auto-invoke a skill marked `disable-model-invocation: true`.
- **ARCH-6** Skills MUST enforce and record only actions this skill set mediates; membership is never inferred from repository membership, roster, CODEOWNERS, branch ownership, PR authorship, or supplied artifacts.

## Domains

System design of this skill set (single source of truth):

| Domain | File | Holds |
|---|---|---|
| System | [`system.md`](./system.md) | Principles, repo layout, install, conventions, project layer |
| Artifacts | [`artifacts.md`](./artifacts.md) | Consumer artifact model, requirement IDs, trace, overlap, ceremony tiers |
| Skills | [`skills.md`](./skills.md) | Skill inventory by category |
| Workflows | [`workflows.md`](./workflows.md) | Idea→ship / bugfix / maintenance chains and boundaries |

Related product-layer docs (not architecture domains):

- [`docs/product/vision.md`](../product/vision.md) — product north star
- [`docs/product/guidelines.md`](../product/guidelines.md) — engineering house rules
