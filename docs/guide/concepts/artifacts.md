# The artifact model

Everything the skill set produces lands in a known place with a known shape. This page is the map.

## In a consuming repo

```
docs/specs/
  INDEX.md                     # feature-code registry — a code is registered here before use
  fixes.md                     # optional shared home for tier-1 fix/guard requirements
  <YYYY-MM-DD>-<feature>/
    requirements.md            # WHAT — EARS acceptance criteria with hierarchical IDs
    design.md                  # HOW — each section cites the REQ IDs it Satisfies
    tasks.md                   # PLAN — checkbox tasks, each ending _Requirements: CODE-N.M_

CONTEXT.md                     # domain glossary: terms, tight definitions, _Avoid_ lists
docs/adr/NNNN-slug.md          # live ADRs — 1–3 sentences, behind a three-part write gate
docs/adr/archived/             # ADRs that no longer guide a future change (define-domain prune)

docs/product/vision.md         # optional project layer — repo-level product vision
docs/architecture/INDEX.md     # optional project layer — IDed **ARCH-N** invariant spine
docs/product/guidelines.md     # optional project layer — engineering guidelines

docs/agents/                   # per-repo config, written once by configure-repo
  project.md                   #   verify commands, test annotation conventions,
                               #   release steps, "Run locally (dev)",
                               #   audit-trace test globs + ignore list
  issue-tracker.md             #   tracker choice + its wayfinding operations
  triage-labels.md             #   canonical role → this repo's label strings

.out-of-scope/                 # rejection knowledge base — one file per concept
.skills/                       # git-ignored ephemera (see below)
.worktrees/                    # git-ignored isolated workspaces
```

## The spec triad

The three files are written in order, each gated on the user's approval of the *previous file*, not on conversational agreement.

**`requirements.md`** — the durable source of intent. A feature code, a `Status:` line, numbered stories, and [EARS](../resources/ears.md) acceptance criteria carrying [hierarchical IDs](requirement-ids.md). Guard criteria (`SHALL CONTINUE TO`) protect existing behavior the feature touches. An explicit **Out of Scope** section defends against scope creep during implementation and review — and it is read again later by `inspect-change` and `write-flow-guide`.

**`design.md`** — how the approved requirements get satisfied. Every `###` architecture section carries a `Satisfies: CODE-N.M, CODE-N.M` line. A section with no `Satisfies:` line is either infrastructure (and says so) or does not belong in this feature.

It also carries the **Seams for testing** table, which is a contract rather than documentation: [`test-first`](../skills/test-first.md) refuses to write a test at a seam this table does not confirm. Prefer existing seams; the ideal number of new seams is zero or one.

**`tasks.md`** — written for an implementer who is skilled but knows *nothing* about this codebase and will see only their own task plus the Global Constraints. That constraint drives its shape:

- A canonical **Global Constraints** source recorded by path and content hash.
  Briefs and reviewer prompts carry that reference plus a compact task delta;
  they do not duplicate the same constraint prose.
- A **File Structure** map written before any task. A file not in the map should not be touched.
- Tasks as **vertical slices** — demoable end to end. If a slice needs prefactoring, that prefactoring is its own earlier task ("make the change easy, then make the easy change").
- Per task: **Files** (create/modify/test), **Interfaces** (Consumes / Produces — how an isolated implementer learns what to call things), bite-sized TDD **Steps** with exact commands and expected output, and a `_Requirements: CODE-N.M_` **footer**.
- **No placeholders.** "TBD", "add appropriate error handling", "similar to Task 3", or a type referenced but defined in no task — each is a plan bug, fixed before the plan ships.

Templates for all three live in [`templates/`](../resources/templates.md).

## `docs/specs/INDEX.md` — the registry

The sole feature registry. A feature code is unique repo-wide, forever. `specify-behavior` registers it here *before* writing the requirements file, and never reuses a retired code.

```markdown
| Code | Feature | Spec | Status | Roadmap item |
|---|---|---|---|---|
| SHELL | Left icon rail for module switching | ./2026-07-09-shell/ | Implemented | ROAD-3 |
```

The last column binds the feature **CODE** (delivery unit) to the [roadmap](../skills/plan-milestones.md) **ROAD-N slot** it implements, or `—` when the project has no roadmap layer. ROAD and CODE are different objects even when the slug looks like the feature name; at most one live CODE binds a ROAD. It is the join [`refresh-roadmap-status`](../skills/refresh-roadmap-status.md) reads to tell a planned item from a specced one.

Because it enumerates every feature, it is what [`load-subgraph`](../skills/load-subgraph.md) reads first when [`frame-change`](../skills/frame-change.md) or [`inspect-change`](../skills/inspect-change.md) asks which neighbors share an idea or a diff — see [feature overlap](feature-graph.md).

## `CONTEXT.md` — the glossary

Maintained by [`define-domain`](../skills/define-domain.md), and **a glossary only**. No implementation details, no decisions, no spec fragments, no scratch notes — those belong in specs and ADRs.

```markdown
**Workspace**:
The top-level container a team collaborates in; owns all Notes and Folders.
_Avoid_: project, space, tenant
```

Be opinionated: one canonical term, competitors banished to the `_Avoid_` list. Definitions stay to one to three tight lines — what the thing *is*, not how it is built. Only project-specific concepts belong; general programming vocabulary does not.

It is updated **inline, the instant a term settles** — never batched, because batched terms get forgotten. `inspect-change`'s Standards axis treats a diff that renames or re-terms a glossary concept as a finding.

Monorepos may instead use a root `CONTEXT-MAP.md` pointing at per-context `CONTEXT.md` files; `configure-repo` asks which.

## `docs/adr/` — architecture decision records

Offered only when **all three** hold:

1. **Hard to reverse** — changing course later carries real cost.
2. **Surprising without context** — a future reader would ask "why on earth this way?"
3. **A real trade-off** — genuine alternatives existed and one was chosen for specific reasons.

Any one missing means no ADR. The body is a short title plus **one to three sentences**: context, decision, why. Recording *that* and *why* is the value, not filling sections.

A new decision that contradicts an existing ADR supersedes it explicitly by number. Never silently override a recorded decision.

When an existing ADR no longer guides a future change, [`define-domain`](../skills/define-domain.md) moves it to `docs/adr/archived/` — word count and age are not the test. Classification lives in that skill; this page only names the path.

## `docs/product/` and `docs/architecture/` — the optional project layer

For large or long-lived projects only, and **absent by default**. Authored and maintained by [`define-project`](../skills/define-project.md):

| File | Contents | Read by |
|---|---|---|
| `docs/product/vision.md` | the repo-level product north star — problem, users, goals, non-goals, scope | `frame-change` (checks a new idea's product scope) |
| `docs/architecture/INDEX.md` (+ per-domain files) | the architecture spine: cross-cutting invariants, each a bold `**ARCH-N**` ID plus one imperative rule | `design-solution` (cites `Respects: ARCH-N`), `plan-tasks`, `build-in-waves`, `inspect-change`, `audit-trace` |
| `docs/product/guidelines.md` | human-facing engineering guidelines — coding standards, naming/i18n, house rules | `plan-tasks` (sources Global Constraints from here, else `project.md`) |

ADRs are the *decisions*; the architecture spine is the *current invariant set* those decisions produced. Every consult is no-op-if-absent, so a repo that never creates these files behaves exactly as it did before the layer existed. See [`define-project`](../skills/define-project.md) and the [traceability spine](traceability.md).

## `docs/agents/` — the per-repo config

Written once by [`configure-repo`](../skills/configure-repo.md) and then read by nearly everything. This is what makes the skill set tracker-agnostic and toolchain-agnostic: no skill hardcodes a test command or a label string.

| File | Contents | Read by |
|---|---|---|
| `project.md` | verify commands (typecheck/lint/unit/e2e), the single-test-file pattern, test annotation conventions per layer, release steps, `## Run locally (dev)`, the audit-trace check's test globs + ignore list | `test-first`, `prove-claim`, `build-in-waves`, `isolate-workspace`, `cut-release`, `acceptance-*`, `write-flow-guide`, `realign-spec`, the [audit-trace check](../resources/scripts.md#the-trace-check) |
| `issue-tracker.md` | tracker choice, operations, PR surface, **Publish unit** (default feature), **Program sync** (default local), close linkage | `triage`, `plan-tasks`, `land-branch`, `cut-release` |
| `triage-labels.md` | canonical role → this repo's label strings | `triage` |

`## Run locally (dev)` is notable because it is written *by* the acceptance skills rather than by `configure-repo`: if `validate-api` or `validate-ui` has to discover how to start the app, it records the command it found, so the next run is cheap.

## `.out-of-scope/` — the rejection knowledge base

One file per **concept**, kebab-case (`plugin-system.md`), never one per issue. Repeat requests append to the existing file's prior-request list.

Each file carries the concept, the decision, a **durable** reason — project scope, an architectural constraint, a deliberate trade-off — and a `Prior requests` list linking every issue that asked. "No time right now" is a deferral, not a rejection, and does not belong here.

One subtlety [`triage`](../skills/triage.md) is emphatic about: an **already-implemented** close does *not* write to `.out-of-scope/`. That knowledge base records rejections; logging built features there poisons future dedup checks.

`frame-change` reads it. So does `triage`, matching by idea rather than keyword.

## `.skills/` — git-ignored ephemera

Feature-scoped working files live under **`.skills/<CODE>/`** (Feature code only),
not as a flat dump at the root. Shared trees stay at `.skills/pathfind/`,
`research/`, and `decisions/`. Full grammar:
[`templates/skills-ephemera-paths.md`](../../../templates/skills-ephemera-paths.md).

| Path under `.skills/<CODE>/` | Written by | Purpose |
|---|---|---|
| `progress.md` (under `<CODE>/`) | execute family | Per-feature ledger — source of truth after compaction |
| `task-N-brief.md` / `task-N-report.md` | execute family | Task contract and report |
| `review-<base7>..<head7>.diff` | execute family | Review package |
| `implementation-notes.md` | implementer | Mid-build deviations |
| `knowns.md` / `scan.md` | discovery / design | Digests |
| `acceptance.md` / product-flow artifacts | acceptance | Ledgers and run files |

Pre-CODE: `.skills/_pending-<slug>/`. Ad-hoc: `.skills/_adhoc/<short-slug>/`.



Working artifacts that pass between agents as **file paths**, never as pasted text. `configure-repo` and `build-in-waves` both ensure the directory is git-ignored, idempotently.

| File | Written by | Purpose |
|---|---|---|
| `progress.md` (under `<CODE>/`) | execute family | The ledger. One line per completed task (and unit lines under `build-by-story`). **Source of truth after compaction** |
| `task-N-brief.md` | execute family | Task N + Global Constraints. The implementer's (or controller's) contract |
| `task-N-report.md` | the implementer subagent | Status, TDD evidence (RED and GREEN commands and outputs), files changed, concerns |
| `review-<base7>..<head7>.diff` | `build-in-waves` | Commit list, diffstat, and full diff — assembled by the agent from `git log`/`git diff` as the reviewer's view |
| `<slug>-scan.md` | scan subagents | A findings digest of a touched surface, so raw source never floods the controller's context |
| `<slug>-req-review.md`, `<slug>-design-review.md`, `<slug>-plan-review.md` | review subagents | Independent verification of a spec/design/plan's code-facing claims. One file **per phase** so the requirements, design, and plan reviews never clobber each other |
| `<slug>-acceptance.md` | `validate-feature` | The acceptance ledger, sliced between `validate-api` and `validate-ui` |

Every per-feature scratch file is keyed by `<slug>` — the feature's short identifier (its feature code once one exists) — and suffixed by the phase that writes it, so concurrent features and successive phases never share a filename.

## What deliberately does *not* land in the repo

Two artifacts go to the OS temp directory instead, because they are session ephemera rather than project artifacts:

- [`write-handoff`](../skills/write-handoff.md) writes `handoff-<topic>-<timestamp>.md` to `$TMPDIR`.
- [`scan-architecture`](../skills/scan-architecture.md) writes `architecture-review-<timestamp>.html` there too.

And [`run-spike`](../skills/run-spike.md) code is throwaway by contract: named so nobody mistakes it for production, deleted or absorbed once the question is answered. Only the *answer* is durable, captured in an ADR, a requirement, or the commit message that deletes the run-spike.

## See also

- [Traceability](traceability.md) — how these artifacts cite each other
- [Requirement IDs](requirement-ids.md) — the string that links them
- [Templates](../resources/templates.md) — the seed files
- [Feature overlap](feature-graph.md) — how `INDEX.md` and the specs answer "does this already exist?"
