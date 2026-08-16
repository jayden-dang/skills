# `define-system-doc`

> Authors or updates **exactly one** system-documentation artifact per invocation, at the catalog's canonical path, and only after a human approves a validator-passing proposal.

|  |  |
|---|---|
| **Bucket** | project |
| **Invocation** | `/define-system-doc <entry-key>` — user-invoked; the agent cannot call it |
| **Reads** | `catalog/CATALOG.md` beside the skill, then only the one entry package the key names, and only the templates and validators that package names |
| **Writes** | `.skills/system-docs/<entry-key>/` while working, and the single canonical consumer file on approval |
| **Calls** | the entry package's structural validator |
| **Called by** | nothing — but a dozen skills *consult* its output, via `consult-recipe.md` |

## When it fires

When one system-documentation artifact needs writing or updating — a codebase map, a testing standard, an observability doc, a security posture. One entry key, one invocation, one canonical file.

The catalog is **pack SSOT and is not installed into consumer repos**; the skill reads it from its own directory.

## The Iron Law

```
NEVER SEED AN EMPTY HYBRID 1A TREE
NEVER WRITE CANONICAL DRAFT VIA THIS SKILL
NEVER TREAT proposal.md OR EPHEMERA AS STANDING PROJECT TRUTH
NEVER PROMOTE HIGH-RISK INFERENCE WITHOUT HUMAN CONFIRMATION
```

The first line names the failure the skill exists to prevent — the *empty forest*: an agent asked for one document creating `docs/security/`, `docs/ops/`, and a dozen placeholder siblings "while it is here", leaving a tree of empty files that read as structure and contain nothing.

## Bounded reading

The resolution procedure is deliberately narrow, because the cheap failure is loading the whole documentation tree to write one page:

1. `SKILL_DIR` is the directory containing `SKILL.md`.
2. Read **only** `catalog/CATALOG.md`; find the row for `<entry-key>`.
3. Load **only** that row's entry package.
4. Load **only** the template and validator paths that package names.
5. Do not load the full catalog body, every template, or the whole docs tree.

An entry that is not first-class, or has no authorable template, stops the run — the skill says so rather than inventing content.

## Evidence before facts

Every claim that reaches the artifact is graded **Verified**, **Inference**, or **Open**, recorded in `evidence.md` with its source and the revision it was read at. Verified claims cite `file:line`.

Inference is **not** promotable without explicit human confirmation for the high-risk classes: compliance, SLO targets, trust boundaries, ownership, runtime topology, and ops procedures. These are exactly the facts that look inferable from the code and are not:

> *"The threat boundary is obvious from the code"* → High-risk class — human confirmation before durable text.

Each required slot ends as confirmed content, an explicit `None — <reason>`, or a named `Blocker:`. A slot is never quietly dropped.

## Ephemera, and what is not truth

```
.skills/system-docs/<entry-key>/
  state.md       entry, canonical target, phase, confirmed decisions, None slots,
                 open blockers, rejected assumptions, defer condition, last revision
  evidence.md    claims with grade, source, revision, slot
  proposal.md    preview only — never SSOT
```

Entry keys mirror into paths: `codebase/map` → `.skills/system-docs/codebase/map/`. Resuming reads the entry package, `state.md`, the canonical file if present, open-slot evidence, and the template — never a replay of chat or a whole-repo rescan.

## Authority

| State | Rule |
|---|---|
| **Absent** | the canonical path is missing |
| **Non-authoritative** | present but `Status:` ≠ Approved, or the structural validator fails — this includes an externally written Draft |
| **Approved** | `Status: Approved` **and** the structural validator passes |

Approved-plus-validator-pass is the only SSOT for the subject. Prior Approved content stays authoritative until a new patch is applied, and the skill never writes `Status: Draft` at a canonical path — a mediated workflow that could would make "Approved" meaningless.

Writes are a **targeted patch** by default: add, modify, or remove selected content and preserve the rest. A whole-file replacement is legal only as a fully reviewed new body, never as a clobber.

## How other skills use it

A dozen skills carry a **consult hook** pointing at `consult-recipe.md` beside this file — [`test-first`](test-first.md), [`design-solution`](design-solution.md), [`specify-behavior`](specify-behavior.md), [`plan-tasks`](plan-tasks.md), [`root-cause`](root-cause.md), [`inspect-change`](inspect-change.md), the acceptance suite, and others. Each applies the standing rules found there **in addition to** its own Iron Law, which never weakens, and each is a no-op when the doc is absent. They may suggest `/define-system-doc <entry>` once when it would be material; none of them may invoke it.

## See also

- [`define-project`](define-project.md) — the vision and `ARCH-N` invariant spine
- [`define-domain`](define-domain.md) — glossary terms and ADRs
- [The system docs concept](../concepts/system-docs.md)
