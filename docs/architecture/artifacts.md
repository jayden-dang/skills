# Architecture domain: Artifacts

Status: Approved
Date: 2026-07-22
Part of: [`INDEX.md`](./INDEX.md) (architecture SSOT)

How work is recorded in a **consuming** repo: the feature triad, requirement IDs,
the audit-trace check, horizontal overlap search, and ceremony tiers.

## The artifact model (in consuming repos)

```
docs/specs/<YYYY-MM-DD>-<feature>/
  requirements.md      # WHAT — EARS acceptance criteria with hierarchical IDs
  design.md            # HOW — architecture, each section cites the REQ IDs it satisfies
  tasks.md             # PLAN — checkbox tasks, each ending `_Requirements: CODE-N.M, ..._`
  discovery.md         # optional, non-normative discovery write-handoff
docs/specs/INDEX.md    # the feature registry — feature codes, names, statuses (LLM-maintained)
CONTEXT.md             # domain glossary (terms + tight definitions + Avoid-lists)
docs/adr/NNNN-slug.md  # minimal ADRs (1–3 sentences; three-part gate)
docs/agents/           # per-repo config written by configure-repo:
  project.md           #   verify commands (typecheck/lint/test/e2e), release steps
  issue-tracker.md     #   tracker choice + wayfinding operations
  triage-labels.md     #   canonical role → label mapping
.out-of-scope/         # rejection knowledge base (one file per concept)
.skills/               # git-ignored: feature ephemera under .skills/<CODE>/;
                       #   shared pathfind/, research/, decisions/, pr-packages/,
                       #   system-docs/ (define-system-doc digests)
  decisions/           #   boundary decision records (DEC-*.md) + adoption anchor
  research/            #   cited research notes (<date>-<topic>.md)
docs/codebase/map.md   # optional Codebase Map (Approved + structural validator)
```

Optional Hybrid 1A system docs (vision, architecture shape, codebase map, security,
standards, ops, …) are catalogued in the pack under
`skills/project/define-system-doc/catalog/` — see the human guide
[`docs/guide/concepts/system-docs.md`](../guide/concepts/system-docs.md). Do **not**
restate catalog rows here; the pack catalog is the SSOT for entry keys and maturity.

Everything under `.skills/` is **local to one working copy**: git-ignored, so it
does not survive a clone and is invisible to CI and to every other contributor.
Decision records and research notes are durable *relative to the conversation
that produced them* — they outlive the session, not the checkout. Nothing that
must reach a reviewer, an auditor, or a build may live there alone.

`requirements.md` remains the **sole normative specification** for a feature; a
`discovery.md` record is never required. `docs/specs/INDEX.md` is the sole feature
registry. Feature overlap is discovered on demand via `load-subgraph` (P0 terms +
P1 Files-derived OWNS/OVERLAPS) — a live read of the specs themselves, not a
generated artifact that has to be kept fresh.

## Participant roles (skill-mediated boundary)

Three roles qualify who is accountable for methodology discipline:

1. **Skill-mediated actor** — a human (or agent on their behalf) acting *through*
   this skill set's workflows. Skills may enforce gates and emit decision records
   for these actions only.
2. **External contributor** — someone contributing outside this skill set's
   mediation (e.g. an inbound PR author who never adopted the process). Absence of
   decision records, requirement IDs, or TDD reports on their contribution is
   **not** a methodology violation.
3. **Accountable reviewer** — the person responsible for accepting or rejecting
   work at a boundary; judgment provenance is theirs when they act through a
   mediated workflow.

Membership in the skill-mediated set is never inferred from repository membership,
roster, CODEOWNERS, branch ownership, PR authorship, or supplied artifacts alone
(see **ARCH-6**).

## Requirement IDs and the trace spine

`requirements.md` format — acceptance criteria use EARS (Easy Approach to
Requirements Syntax) with hierarchical IDs:

```markdown
# Requirements: <Feature Name>
Feature code: SHELL          ← short unique prefix, repo-wide registry in docs/specs/INDEX.md
Status: Draft | Approved | Implemented | Shipped

## 1. Module switching
**Story:** As a user, I want a left icon rail so I can switch modules.

- **SHELL-1.1** WHEN the app starts with no persisted module THE SYSTEM SHALL
  activate the Notes module.
- **SHELL-1.2** WHEN the user selects a module THE SYSTEM SHALL persist the
  selection and restore it on next launch.
- **SHELL-1.3** (guard) WHEN the user switches modules THE SYSTEM SHALL CONTINUE
  TO preserve unsaved editor state.
```

The ID then flows through the **docs triad** (docs-only spine):

| Artifact | Carries the ID as |
|---|---|
| `design.md` section | `Satisfies: SHELL-1.1, SHELL-1.2` line |
| `tasks.md` task | `_Requirements: SHELL-1.1, SHELL-1.2_` footer |
| Issue (if tracker used) | `Requirements covered` section in issue body |
| Application source / tests / commits | **Not required** — domain language; Spec review maps IDs |

Docs-side uses are **grep-selectable strings**. That is what makes the docs-only
`audit-trace` check reproducible without a bundled linter. Behavior coverage is
tests + Spec review + prove-claim, not ID strings in code.

## The audit-trace check

The `audit-trace` skill (model-invoked, in `execution/`) is the **docs-only**
vertical enforcement layer. It does not eyeball specs — it drives a fixed
sequence of deterministic passes and applies fixed rules:

- **Define:** extract bold requirement IDs (`**CODE-N.M**`) from every
  `requirements.md`/`fixes.md` under `docs/specs/`, dropping any inside strikethrough
  (retired). Read each file's `Status:` and `Feature code:` lines.
- **Cite (tasks):** extract IDs from `_Requirements:` lines in every `tasks.md`.
- **No test-tree pass** — application and test source are not grepped for IDs
  (E2 retired).
- **Diff the sets** and report:
  - **ERROR** — a task cites an ID with no bold definition (E1); the same ID
    bold-defined in two files (E3).
  - **WARN** — an `Approved` requirement cited by no task (W1); a `requirements.md`
    missing its `Status:` or `Feature code:` line (W2).
  - When `docs/architecture/` exists: E4/E5/W3 for ARCH-N `Respects:` integrity.

`prove-claim`, `cut-release`, `realign-spec`, and `plan-tasks`'s coverage check invoke `audit-trace`.
Because the passes are `grep`/read and the rules are set operations, two agents on
the same repo reach the same finding set. Exact message wording and ordering are
not contractual — the *finding set* is.

## Feature overlap (horizontal)

The previous design maintained a generated feature graph to answer "does this idea
already exist?" and "does this diff reimplement a neighbor?". This design answers
both by **ask-time derivation** (`load-subgraph`), not a materialised graph:

- `frame-change`: invoke `load-subgraph` with key terms and candidate paths; report
  neighbors as summary cards plus OWNS coverage — never blocking the gate.
- `inspect-change`: invoke `load-subgraph` with the diff's paths (and optional terms);
  surface neighbors to the Spec subagent for reuse-miss findings.

`docs/specs/INDEX.md` is the registry both consult first. There is no generated
artifact to keep fresh, so nothing can go stale.

## Ceremony tiers

| Tier | When | Artifacts |
|---|---|---|
| **0 — trivial** | typo-level, no behavior change | none — test-first/prove-claim only |
| **1 — bugfix / small change** | behavior change ≤ ~half a day | mini-spec: add a fix REQ + a SHALL-CONTINUE-TO guard to the owning feature's requirements.md (or `docs/specs/fixes.md`), plus a regression test of the behavior; no design.md, task list optional |
| **2 — feature** | multi-task work | full triad + execute family |

`frame-change` and `ask-me-bro` decide the tier explicitly and say so. Never spec what you
don't understand yet — spike via `run-spike`/`research` first.


## Feature ephemera roots

Feature-scoped files live under `.skills/<CODE>/`. See the skill-set template `templates/skills-ephemera-paths.md` (shipped with the pack).
