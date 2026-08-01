# Requirements: Skills ephemera namespace

Feature code: SKNS
Status: Approved
Date: 2026-08-01

## 1. Per-feature ephemera root

**Story:** As an agent or developer running a feature, I want all feature-scoped working files under `.skills/<CODE>/`, so that I can list, track, and delete one feature's ephemera without combing a flat root dump.

- **SKNS-1.1** WHEN a skill writes feature-scoped ephemera (progress ledger, task brief, task report, review diff package, implementation-notes, feature global-constraints copy, discovery knowns/scan/triad-review digests, acceptance or product-flow run artifacts for that feature) THE SYSTEM SHALL write those files under `.skills/<CODE>/` where `<CODE>` is the feature's registered Feature code (2–12 chars, `A-Z0-9`, starts with a letter, matching `docs/specs/INDEX.md` / the feature `requirements.md` `Feature code:` line).
- **SKNS-1.2** THE SYSTEM SHALL use the Feature code alone as the directory name segment under `.skills/` (e.g. `.skills/SPAY/`), and SHALL NOT encode a long human title or branch name into that path segment.
- **SKNS-1.3** WHEN a skill needs a feature-scoped path THE SYSTEM SHALL resolve `<CODE>` from, in order: the active plan or brief context, the feature's `requirements.md` `Feature code:` line, or the matching `docs/specs/INDEX.md` row — and SHALL NOT invent a second parallel identifier for the same feature.
- **SKNS-1.4** WHILE execute family skills run for a feature THE SYSTEM SHALL treat `.skills/<CODE>/progress.md` as the sole progress ledger for that feature and SHALL NOT append that feature's task-completion lines into a different feature's ledger or a global root `.skills/progress.md`.

## 2. Shared roots that stay outside `<CODE>/`

**Story:** As a maintainer of multi-session or boundary work, I want pathfind, research, decisions, and PR packages to stay in their established shared locations, so that cross-feature artifacts are not forced into one Feature code.

- **SKNS-2.1** THE SYSTEM SHALL CONTINUE TO store pathfind effort packages under `.skills/pathfind/<effort-slug>/` (not under a Feature code directory).
- **SKNS-2.2** THE SYSTEM SHALL CONTINUE TO store dated research notes under `.skills/research/` (not required under a Feature code directory).
- **SKNS-2.3** THE SYSTEM SHALL CONTINUE TO store boundary decision records under `.skills/decisions/` (not under a Feature code directory).
- **SKNS-2.4** THE SYSTEM SHALL CONTINUE TO store PR packages under `.skills/pr-packages/<stable-id>/` and MAY record a `Feature-code:` field in the package manifest when a code is known, without relocating the package tree under `.skills/<CODE>/`.

## 3. Pre-CODE and ad-hoc sessions

**Story:** As an agent in discovery before a Feature code exists, I want a temporary ephemera home that promotes cleanly to `.skills/<CODE>/` once the code is registered, so that early scan/knowns work is not lost and does not pollute the flat root forever.

- **SKNS-3.1** WHEN feature-scoped ephemera must be written before a Feature code is registered THE SYSTEM SHALL write it under `.skills/_pending-<slug>/` where `<slug>` is a short kebab-case working name for the idea (not under the bare `.skills/` root as loose files).
- **SKNS-3.2** WHEN `specify-behavior` (or equivalent registration) adds a Feature code to `docs/specs/INDEX.md` and a matching `_pending-<slug>/` directory exists for that work THE SYSTEM SHALL move or rewrite subsequent writes so the active ephemera root becomes `.skills/<CODE>/`, and SHALL NOT leave new feature-scoped writes on the pending path after registration.
- **SKNS-3.3** WHEN work has no Feature code and is not a pending discovery for one (tier-0 ad-hoc / one-off) THE SYSTEM SHALL use `.skills/_adhoc/<short-slug>/` for any ephemera it writes, and SHALL NOT use a registered Feature code directory for that ad-hoc work.

## 4. Legacy flat root

**Story:** As a developer with an existing flat `.skills/` tree (e.g. mailgate, bot), I want agents to stop growing the root dump while still resuming work, so that migration is gradual and I can delete per-CODE folders when done.

- **SKNS-4.1** WHEN `.skills/<CODE>/` does not yet exist but a legacy root path holds usable state for that feature (e.g. root `progress.md` clearly scoped to that feature, or root `task-N-*.md` from its only active plan) THE SYSTEM SHALL be allowed to **read** that legacy path for resume once, and SHALL write all **new** feature-scoped artifacts under `.skills/<CODE>/`.
- **SKNS-4.2** WHEN writing feature-scoped ephemera after this feature ships THE SYSTEM SHALL NOT create new loose files at the bare `.skills/` root for progress, task briefs/reports, review diffs, implementation-notes, or feature knowns/scan/acceptance artifacts (shared roots in story 2 remain allowed).
- **SKNS-4.3** THE SYSTEM SHALL NOT auto-migrate or bulk-move an entire consumer repo's historical `.skills/` tree as part of installing or running this skill set; cleanup and optional moves remain human-initiated (`rm -rf .skills/<CODE>` or manual moves).

## 5. Skill-set contract surface

**Story:** As a skill author or agent following the skill set, I want every skill that previously hard-coded flat `.skills/…` paths for feature work to name `.skills/<CODE>/…` instead, so that behavior matches the layout contract end to end.

- **SKNS-5.1** WHEN the skill set documents or implements paths for execute-family progress, task briefs/reports, review diffs, or implementation-notes THE SYSTEM SHALL specify those paths as under `.skills/<CODE>/` (not bare `.skills/progress.md`, bare `.skills/task-N-*.md`, bare `.skills/review-*.diff`, or bare `.skills/implementation-notes.md`).
- **SKNS-5.2** WHEN the skill set documents or implements paths for frame-change/design/plan knowns, scan digests, or triad review digests that are feature-scoped THE SYSTEM SHALL specify those paths as under `.skills/<CODE>/` (or under `.skills/_pending-<slug>/` before CODE registration per SKNS-3.1).
- **SKNS-5.3** WHEN the skill set documents or implements feature acceptance / product-flow artifact paths that are feature-scoped THE SYSTEM SHALL specify those paths as under `.skills/<CODE>/`.
- **SKNS-5.4** WHEN AGENTS.md, guide artifact docs, or skill bodies describe the `.skills/` tree THE SYSTEM SHALL describe the per-CODE layout and the shared roots in story 2, and SHALL NOT document the old flat root as the preferred layout for feature ephemera.

## 6. Guards — existing shared and process behavior

**Story:** As a user of pathfind, research, decisions, PR packages, and the Iron Laws, I want this layout change not to break those contracts.

- **SKNS-6.1** (guard) WHEN skills write pathfind, research, decisions, or pr-packages artifacts THE SYSTEM SHALL CONTINUE TO use the shared roots named in SKNS-2.1–2.4.
- **SKNS-6.2** (guard) WHEN execute family resumes after compaction THE SYSTEM SHALL CONTINUE TO trust the progress ledger and `git log` over conversation memory — with the ledger path now `.skills/<CODE>/progress.md`.
- **SKNS-6.3** (guard) WHEN skills write under `.skills/` THE SYSTEM SHALL CONTINUE TO require that `.skills/` is git-ignored before writing durable package or ledger content that assumes local-only ephemera (same ignore rule as package-change / configure-repo).
- **SKNS-6.4** (guard) WHEN audit-trace, load-subgraph, or requirement ID citation rules run THE SYSTEM SHALL CONTINUE TO leave E1–E5 / W1–W3 semantics and FSUB derivation rules unchanged — this feature only relocates ephemera paths.

Touched surfaces for guard scan (skill-set contract files, not consumer app code):

| Surface | Guard outcome |
|---|---|
| `skills/execution/build-in-waves/**`, `build-by-story/**`, `build-inline/**` | progress/brief/report/review/notes → under CODE (SKNS-5.1); resume trust rule continues (SKNS-6.2) |
| `skills/discovery/frame-change/**`, `clarify-decisions/**`, `pathfind/**` | pathfind stays shared (SKNS-2.1, 6.1); knowns/scan move under CODE or pending (SKNS-5.2, 3.x) |
| `skills/spec/**` | triad review digests under CODE/pending (SKNS-5.2) |
| `skills/acceptance/**` | feature artifacts under CODE (SKNS-5.3) |
| `skills/ship/package-change/**`, `land-branch/**`, `record-verdict/**` | pr-packages + decisions stay shared (SKNS-2.3–2.4, 6.1); implementation-notes path under CODE (SKNS-5.1) |
| `skills/track/reroute-plan/**`, `refresh-roadmap-status/**` | progress path under CODE when consulted |
| `AGENTS.md`, `docs/guide/**` | layout docs (SKNS-5.4) |
| audit-trace / load-subgraph | no behavior change (SKNS-6.4) |

## 7. Quality attributes

**Section-kind:** nfr

**Story:** As a stakeholder, I want measurable quality targets for this feature, so that how-well is not left implicit.

- **Performance:** None — path resolution is filesystem string join; no runtime service.
- **Security:** None — ephemera remain git-ignored local files; no new trust boundary.
- **Reliability:** **SKNS-7.1** WHEN two features run in the same working copy THE SYSTEM SHALL keep their progress ledgers in distinct `.skills/<CODE>/progress.md` files so task-complete lines for one feature cannot be written into the other feature's ledger — verified by skill contract tests (path strings and scenario pressure) and by inspecting two CODE directories.
- **Accessibility:** None — no human-facing UI surface.

## Out of Scope

- Auto-migrating or rewriting historical consumer `.skills/` trees (mailgate, bot, etc.).
- Sharing one `.skills` tree across git worktrees via symlink or network mount.
- Changing PR package directory schema beyond optional `Feature-code:` in the manifest.
- Changing decision-record or research filename grammar.
- Materialized feature graphs (`GRAPH.md`) or load-subgraph edge stores.
- Personal OS / vault paths under `skills/personal/`.
- Requiring Feature code directories for pure shared-only sessions that write nothing feature-scoped.

## Open Questions

None — locked close package from discovery (2026-08-01).
