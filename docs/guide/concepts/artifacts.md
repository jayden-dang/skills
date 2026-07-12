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
docs/adr/NNNN-slug.md          # minimal ADRs — 1–3 sentences, behind a three-part gate

docs/agents/                   # per-repo config, written once by setup-repo
  project.md                   #   verify commands, test annotation conventions,
                               #   release steps, "Run locally (dev)",
                               #   trace test globs + ignore list
  issue-tracker.md             #   tracker choice + its wayfinding operations
  triage-labels.md             #   canonical role → this repo's label strings

.out-of-scope/                 # rejection knowledge base — one file per concept
.skills/                       # git-ignored ephemera (see below)
.worktrees/                    # git-ignored isolated workspaces
```

## The spec triad

The three files are written in order, each gated on the user's approval of the *previous file*, not on conversational agreement.

**`requirements.md`** — the durable source of intent. A feature code, a `Status:` line, numbered stories, and [EARS](../resources/ears.md) acceptance criteria carrying [hierarchical IDs](requirement-ids.md). Guard criteria (`SHALL CONTINUE TO`) protect existing behavior the feature touches. An explicit **Out of Scope** section defends against scope creep during implementation and review — and it is read again later by `code-review` and `dogfood`.

**`design.md`** — how the approved requirements get satisfied. Every `###` architecture section carries a `Satisfies: CODE-N.M, CODE-N.M` line. A section with no `Satisfies:` line is either infrastructure (and says so) or does not belong in this feature.

It also carries the **Seams for testing** table, which is a contract rather than documentation: [`tdd`](../skills/tdd.md) refuses to write a test at a seam this table does not confirm. Prefer existing seams; the ideal number of new seams is zero or one.

**`tasks.md`** — written for an implementer who is skilled but knows *nothing* about this codebase and will see only their own task plus the Global Constraints. That constraint drives its shape:

- A **Global Constraints** section copied verbatim from the design and `docs/agents/project.md`. It travels with every task brief.
- A **File Structure** map written before any task. A file not in the map should not be touched.
- Tasks as **vertical slices** — demoable end to end. If a slice needs prefactoring, that prefactoring is its own earlier task ("make the change easy, then make the easy change").
- Per task: **Files** (create/modify/test), **Interfaces** (Consumes / Produces — how an isolated implementer learns what to call things), bite-sized TDD **Steps** with exact commands and expected output, and a `_Requirements: CODE-N.M_` **footer**.
- **No placeholders.** "TBD", "add appropriate error handling", "similar to Task 3", or a type referenced but defined in no task — each is a plan bug, fixed before the plan ships.

Templates for all three live in [`templates/`](../resources/templates.md).

## `docs/specs/INDEX.md` — the registry

The sole feature registry. A feature code is unique repo-wide, forever. `write-requirements` registers it here *before* writing the requirements file, and never reuses a retired code.

```markdown
| Code | Feature | Spec | Status |
|---|---|---|---|
| SHELL | Left icon rail for module switching | ./2026-07-09-shell/ | Implemented |
```

Because it enumerates every feature, it is what the [feature-overlap](feature-graph.md) search reads to know the full set of neighbors when [`brainstorm`](../skills/brainstorm.md) or [`code-review`](../skills/code-review.md) checks whether an idea or a diff already exists.

## `CONTEXT.md` — the glossary

Maintained by [`domain-modeling`](../skills/domain-modeling.md), and **a glossary only**. No implementation details, no decisions, no spec fragments, no scratch notes — those belong in specs and ADRs.

```markdown
**Workspace**:
The top-level container a team collaborates in; owns all Notes and Folders.
_Avoid_: project, space, tenant
```

Be opinionated: one canonical term, competitors banished to the `_Avoid_` list. Definitions stay to one to three tight lines — what the thing *is*, not how it is built. Only project-specific concepts belong; general programming vocabulary does not.

It is updated **inline, the instant a term settles** — never batched, because batched terms get forgotten. `code-review`'s Standards axis treats a diff that renames or re-terms a glossary concept as a finding.

Monorepos may instead use a root `CONTEXT-MAP.md` pointing at per-context `CONTEXT.md` files; `setup-repo` asks which.

## `docs/adr/` — architecture decision records

Offered only when **all three** hold:

1. **Hard to reverse** — changing course later carries real cost.
2. **Surprising without context** — a future reader would ask "why on earth this way?"
3. **A real trade-off** — genuine alternatives existed and one was chosen for specific reasons.

Any one missing means no ADR. The body is a short title plus **one to three sentences**: context, decision, why. Recording *that* and *why* is the value, not filling sections.

A new decision that contradicts an existing ADR supersedes it explicitly by number. Never silently override a recorded decision.

## `docs/agents/` — the per-repo config

Written once by [`setup-repo`](../skills/setup-repo.md) and then read by nearly everything. This is what makes the skill set tracker-agnostic and toolchain-agnostic: no skill hardcodes a test command or a label string.

| File | Contents | Read by |
|---|---|---|
| `project.md` | verify commands (typecheck/lint/unit/e2e), the single-test-file pattern, test annotation conventions per layer, release steps, `## Run locally (dev)`, the trace check's test globs + ignore list | `tdd`, `verify`, `execute-plan`, `worktrees`, `release`, `acceptance-*`, `dogfood`, `sync-spec`, the [trace check](../resources/scripts.md#the-trace-check) |
| `issue-tracker.md` | tracker choice (github / gitlab / linear / local / other), its operations, whether external PRs are a request surface | `triage`, `write-plan`, `release` |
| `triage-labels.md` | canonical role → this repo's label strings | `triage` |

`## Run locally (dev)` is notable because it is written *by* the acceptance skills rather than by `setup-repo`: if `acceptance-api` or `acceptance-ui` has to discover how to start the app, it records the command it found, so the next run is cheap.

## `.out-of-scope/` — the rejection knowledge base

One file per **concept**, kebab-case (`plugin-system.md`), never one per issue. Repeat requests append to the existing file's prior-request list.

Each file carries the concept, the decision, a **durable** reason — project scope, an architectural constraint, a deliberate trade-off — and a `Prior requests` list linking every issue that asked. "No time right now" is a deferral, not a rejection, and does not belong here.

One subtlety [`triage`](../skills/triage.md) is emphatic about: an **already-implemented** close does *not* write to `.out-of-scope/`. That knowledge base records rejections; logging built features there poisons future dedup checks.

`brainstorm` reads it. So does `triage`, matching by idea rather than keyword.

## `.skills/` — git-ignored ephemera

Working artifacts that pass between agents as **file paths**, never as pasted text. `setup-repo` and `execute-plan` both ensure the directory is git-ignored, idempotently.

| File | Written by | Purpose |
|---|---|---|
| `progress.md` | `execute-plan` | The ledger. One line per completed task. **The source of truth after compaction** — trusted over the agent's own memory |
| `task-N-brief.md` | `execute-plan` | Task N copied out with the Global Constraints verbatim, assembled by the agent. The implementer's entire world |
| `task-N-report.md` | the implementer subagent | Status, TDD evidence (RED and GREEN commands and outputs), files changed, concerns |
| `review-<base7>..<head7>.diff` | `execute-plan` | Commit list, diffstat, and full diff — assembled by the agent from `git log`/`git diff` as the reviewer's view |
| `<slug>-scan.md` | scan subagents | A findings digest of a touched surface, so raw source never floods the controller's context |
| `<slug>-req-review.md`, `<slug>-design-review.md`, `<slug>-plan-review.md` | review subagents | Independent verification of a spec/design/plan's code-facing claims. One file **per phase** so the requirements, design, and plan reviews never clobber each other |
| `<slug>-acceptance.md` | `acceptance-check` | The acceptance ledger, sliced between `acceptance-api` and `acceptance-ui` |

Every per-feature scratch file is keyed by `<slug>` — the feature's short identifier (its feature code once one exists) — and suffixed by the phase that writes it, so concurrent features and successive phases never share a filename.

## What deliberately does *not* land in the repo

Two artifacts go to the OS temp directory instead, because they are session ephemera rather than project artifacts:

- [`handoff`](../skills/handoff.md) writes `handoff-<topic>-<timestamp>.md` to `$TMPDIR`.
- [`improve-architecture`](../skills/improve-architecture.md) writes `architecture-review-<timestamp>.html` there too.

And [`prototype`](../skills/prototype.md) code is throwaway by contract: named so nobody mistakes it for production, deleted or absorbed once the question is answered. Only the *answer* is durable, captured in an ADR, a requirement, or the commit message that deletes the prototype.

## See also

- [Traceability](traceability.md) — how these artifacts cite each other
- [Requirement IDs](requirement-ids.md) — the string that links them
- [Templates](../resources/templates.md) — the seed files
- [Feature overlap](feature-graph.md) — how `INDEX.md` and the specs answer "does this already exist?"
