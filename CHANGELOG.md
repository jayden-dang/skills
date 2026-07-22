# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] — 2026-07-22

First public release of the A-to-Z agentic development skill set: ideation →
spec triad → execution → acceptance → ship, with requirements traceability as
the spine. **40 skills** across **11 categories**, installable as a Claude Code
plugin or via `npx skills@latest add jayden-dang/skills`.

No prior git tag — this entry covers the whole history to `HEAD`.

### Shipped behavior

Grouped from requirement-ID trailers (`Implements:`) against
`docs/specs/2026-07-22-team-structure/requirements.md`.

#### Team structure in setup-repo (TEAM)

- **TEAM-1.1** — `setup-repo` walks a Team decision (same explainer → recommend → wait pattern) before writing team content
- **TEAM-1.2** — Team draft is built from local git / `CODEOWNERS` / common manifests only — never code-host collaborator APIs
- **TEAM-1.3** — Active authors inferred from last-12-month git history (or all history if younger), ranked, capped
- **TEAM-1.4** — `CODEOWNERS` owners surface with path notes even outside top-N commit rank
- **TEAM-1.5** — Incomplete metadata presents an incomplete draft and asks; never invents names/titles
- **TEAM-1.6** — User can add/remove/rename/re-role; named (`Role — Name`) or count (`N Role(s)`) form
- **TEAM-1.7** — User confirmation is the sole write authority for Team
- **TEAM-1.8** — Fill-the-gaps can add or change Team without clobbering other confirmed sections
- **TEAM-2.1** — `templates/agents/project.md` seeds structured `## Team` (roster, ownership, band, packaging matrix)
- **TEAM-2.2** — Confirmed Team is written/merged into `docs/agents/project.md` without clobbering other sections
- **TEAM-2.3** — Roster entries stay structured (`Role — Name` or `N × Role`), not free-text-only blobs
- **TEAM-2.4** — Suggested role vocabulary with freeform roles allowed
- **TEAM-2.5** — Agent-skills block discovers Team composition in `docs/agents/project.md`
- **TEAM-2.6** — Workflow band Solo / Small / Multi derived from headcount (or override)
- **TEAM-3.1** — High-impact skills read `## Team` and right-size packaging (not gates)
- **TEAM-3.2** — Solo packaging: lean multi-person ritual language; no invented reviewers
- **TEAM-3.3** — Small packaging: design-review checkpoints and ownership language
- **TEAM-3.4** — Multi packaging: ownership-aware review and handoff emphasis
- **TEAM-3.5** — Missing Team does not invent a roster or hard-fail
- **TEAM-3.6** — Band never weakens Iron Laws
- **TEAM-4.1** — Setup-repo guide documents Team decision and band packaging
- **TEAM-4.2** — Adopting docs mention team composition as a setup concern
- **TEAM-5.1** — No external identity-service auth required to populate Team

### Protected behavior

- **TEAM-6.1** — `setup-repo` continues A–H one-at-a-time, additive writes, Step-6 wiring, no Step-1 service probing
- **TEAM-6.2** — Project posture remains orthogonal to Team band for brainstorm / grilling / interpret
- **TEAM-6.3** — Step 1 still classifies from repo files only (no remote tracker probe)
- **TEAM-6.4** — Missing `docs/agents/` still suggests setup-repo and proceeds rather than hard-failing on Team alone

### Initial skill set (Misc)

Commits without requirement trailers, summarized for the first cut:

- Full lifecycle skill set: discovery (`brainstorm`, `grilling`, `research`, `prototype`, `domain-modeling`, `interpret`), spec triad, execution (`execute-plan`, `tdd`, `debug`, `verify`, `trace`, `worktrees`), review, acceptance, ship, track, setup, project docs layer (`establish-project`), meta (`using-skills`, `writing-skills`, `ask`, `teach`)
- Requirements traceability spine (`CODE-N.M` through specs → tests → commits) with agent-run `trace` check
- Optional project-docs layer: vision, architecture invariant spine (`ARCH-N`), guidelines
- Project posture (delivery intent + lifecycle stage) captured by `setup-repo` and reused by interview skills
- Context7 MCP preferred for live library facts; lint guards against silent drift
- Plugin manifest integrity tests; handoff and skill-frontmatter linters on lefthook
- Architecture SSOT under `docs/architecture/` (root `DESIGN.md` removed)
- Nested-protocol handoff: `brainstorm` interview applies `grilling` as protocol, not a stage switch (pressure-tested)
- Craft: `design-page` before human-facing HTML; polish lane for behavior-preserving cleanup
- Human guide (`docs/guide/`), `AGENTS.md` constitution, install via plugin or `npx skills`

[0.1.0]: https://github.com/jayden-dang/skills/releases/tag/v0.1.0
