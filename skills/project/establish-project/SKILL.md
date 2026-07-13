---
name: establish-project
description: Use at the start of a large or long-lived project, before feature work, to
  establish or maintain the optional repo-level documentation layer — a product vision, an
  IDed architecture-invariant spine, and engineering guidelines. Also use to update that
  layer against a major change of direction, or to validate it. Produces
  docs/product/vision.md, docs/architecture/, and docs/product/guidelines.md. Run it with
  /establish-project.
disable-model-invocation: true
---

# Establish Project

Author and maintain the project-documentation layer that sits ABOVE the feature
workflow — the product north star, and the architecture invariants that keep
independently-built features from drifting apart.

This layer is OPTIONAL and pays off on large, multi-feature projects. A small repo does
not need it — the feature workflow (`brainstorm` → spec → `execute-plan`) works fully
without it, and nothing here is a gate. If the user is not sure they need it, say so and
let them decide.

## Modes

Pick the mode from what the user asked; ask if it is unclear.

- **create** — nothing exists yet. Author the layer from scratch.
- **update** — the layer exists. Revise it against a change signal.
- **validate** — the layer exists. Check it against a checklist and conformance.

Templates resolve as `${CLAUDE_PLUGIN_ROOT}/templates` when installed as a plugin, else
`../../../templates` relative to this file. Every heading in each template is a REQUIRED
slot — fill it or write `None`.

## Create

1. **Brownfield check.** Detect brownfield via the source predicate: at least one
   regular file beneath a source root (`src/`, `app/`, `backend/`, `lib/`, `packages/`,
   `crates/`, or one a manifest or build configuration declares). **Greenfield** (no
   such file) — skip the scan, proceed straight to Step 2. **Brownfield** — dispatch a
   **scan subagent** per `brownfield-scan.md` (beside this file), writing
   `.skills/<slug>-scan.md` before Step 2's interview begins — the architecture spine
   then RATIFIES what already exists (name the invariants the current code already
   honors) rather than designing greenfield. (No subagents? Run the same scan inline
   under the `brownfield-scan.md` contract.) **Failure → blocker:** if the scan fails,
   times out, or cannot write a complete digest, report it as a blocker and STOP here —
   do not proceed to Step 2, do not classify the repo as greenfield, and write nothing
   durable. *Done when: greenfield has proceeded to Step 2, or a complete brownfield
   digest exists at `.skills/<slug>-scan.md` before Step 2 begins, or a blocker has been
   reported and the workflow has stopped.*
2. **Interview.** REQUIRED SUB-SKILL: use `grilling` — one question at a time — to draw
   out the product vision (problem, users, goals, non-goals, scope) and the load-bearing
   architecture invariants. Keep `domain-modeling` active as a passive side effect
   (record glossary terms the instant they settle). *Done when: no open decision remains.*
3. **Write the vision.** Fill `templates/product-vision.md` → `docs/product/vision.md`.
   *Done when: the file exists, every slot filled or `None`.*
4. **Write the spine.** Fill `templates/architecture-INDEX.md` → `docs/architecture/INDEX.md`.
   Each invariant is a bold `**ARCH-N**` ID plus one imperative rule; keep the set small.
   Split into per-domain `docs/architecture/<domain>.md` files only for a large project.
   *Done when: the spine exists with at least one invariant.*
5. **Write the guidelines.** Fill `templates/product-guidelines.md` →
   `docs/product/guidelines.md`. If engineering rules already live in
   `docs/agents/project.md`, move them here and leave a pointer. *Done when: the file
   exists.*
6. **Register.** Add the project-docs line to the `## Agent skills` block so the feature
   skills discover the layer (or suggest `/setup-repo` if no such block exists yet).
   *Done when: the layer is discoverable.*

## Update

The change signal is a new product direction, a new or changed invariant, or drift you
found.

- Revise the affected doc(s) only.
- A hard-to-reverse, surprising architecture decision gets an ADR (REQUIRED SUB-SKILL:
  use `domain-modeling` — it owns the ADR gate).
- **Never renumber an `ARCH-N`.** Retire an invariant by strikethrough
  (`~~**ARCH-3**~~ superseded by ARCH-7`) — the `trace` check then flags any design still
  citing it. Add new invariants with fresh IDs.
- Update mode CONTINUES TO avoid dispatching the create-mode brownfield scan — Step 1
  above is create-only.

*Done when: the docs reflect the change and any superseding ADR is recorded.*

## Validate

- Walk each doc against its template — every REQUIRED slot filled or `None`; the vision
  has real scope boundaries; every invariant is one imperative rule with a unique ID.
- REQUIRED SUB-SKILL: use `check-invariants` across the feature `design.md` files to
  surface any design that violates an invariant it cites.
- Run the `trace` check for invariant referential integrity (E4/E5/W3).
- Validate mode CONTINUES TO avoid dispatching the create-mode brownfield scan — Step 1
  above is create-only.

*Done when: the checklist is walked and the findings are reported.*

## No-op

If asked to consult the layer but neither `docs/product/` nor `docs/architecture/`
exists, say the project has no layer and that `/establish-project` (create mode) can add
one — then stop. The layer is never required.
