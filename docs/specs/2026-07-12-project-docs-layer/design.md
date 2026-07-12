# Design: Optional project-documentation layer

Feature code: PROJDOC
Status: Approved
Date: 2026-07-12
Requirements: ./requirements.md

## Context

The skill set persists intent per feature (the `docs/specs/<feature>/` triad),
cross-feature vocabulary (`CONTEXT.md`), and point decisions (`docs/adr/`). It has
no repo-level product or architecture artifact — `DESIGN.md:287` lists
"multi-session planning maps" as deliberately deferred. On large projects, feature
work drifts from product intent and from a coherent architecture because nothing
above the feature loop states either. This feature adds that missing layer.

The governing constraint is that the layer must be **invisible to any repo that
does not opt in**. The skill set's whole value proposition is zero mandatory tooling
and ceremony that scales with the task (`DESIGN.md:34,36`). So every touchpoint is
an *observable-predicate consult* — "if the doc exists, use it; else say so once and
continue" — copied from the idiom already at `brainstorm/SKILL.md:53`, never a new
gate. A small repo never creates `docs/product/` or `docs/architecture/`, so every
hook takes its no-op branch and behavior is identical to today.

The second constraint is the determinism principle (`DESIGN.md` principle 3): the
`trace` check is `grep`/set-difference, never judgment. Architecture invariants get
IDs and a *referential-integrity* trace pass (does a cited `ARCH-N` exist and is it
live?), exactly parallel to how requirement IDs are checked. The *semantic* question
— does this design genuinely respect the invariant? — is judgment, so it lives in a
**separate, advisory, LLM-judged** skill (`check-invariants`) beside `trace`, never
inside it.

## Decisions

1. **Invariants are first-class greppable IDs** (`**ARCH-N**`), cited by feature
   `design.md` as `Respects: ARCH-N` — the requirement-ID spine extended one level
   up. This is what lets `trace` check them deterministically.
2. **`trace` gets referential integrity only** (new passes + codes E4/E5/W3), gated
   on `docs/architecture/` existing; semantic conformance is a separate advisory
   skill. Keeps principle 3 intact.
3. **One tri-modal authoring skill** (`establish-project`, create/update/validate),
   not a mirrored `write-vision`/`write-architecture` pair — vision, spine, and
   guidelines are authored in one conversation and read by the same hooks.
4. **Engineering guidelines become a durable artifact** (`docs/product/guidelines.md`);
   `docs/agents/project.md` keeps machine-config + a pointer. A back-compat guard
   keeps reading from `project.md` when the guidelines doc is absent.
5. **Opt-in defaults to No** in `setup-repo`; `scaffold-project` seeds only when
   opted in. Migration of existing guidelines is offered, never forced.
6. **The layer governs this repo too**: §10 sketches `ARCH-1..5` for the skill set
   itself (determinism-of-trace, optionality, zero-tooling, ID immutability,
   sub-skill composition). No ADR is warranted — every decision here follows an
   existing principle rather than overturning one.

None of these parts puts a new *interface* in question — each follows an established
shape (a new SKILL.md, a new `trace` pass, the existing no-op consult idiom), so
this is single-design work, not a 3-variant interface bake-off.

## Architecture

### Artifacts and paths (infrastructure)

Infrastructure — no Satisfies line. Three durable, optional docs under `docs/`:

- `docs/product/vision.md` — the repo-level PRD/north-star.
- `docs/architecture/INDEX.md` (+ optional `docs/architecture/<domain>.md`) — the
  invariant spine.
- `docs/product/guidelines.md` — human-facing engineering guidelines.

Each ships as a `templates/` seed (`templates/product-vision.md`,
`templates/architecture-INDEX.md`, `templates/product-guidelines.md`), resolved the
way existing spec templates are (`${CLAUDE_PLUGIN_ROOT}/templates` when a plugin,
else `../../../templates`). `docs/adr/` is unchanged — ADRs remain the *decisions*;
the spine is the *current invariant set* those decisions produced.

### establish-project — the tri-modal authoring skill

Satisfies: PROJDOC-1.1, PROJDOC-1.3, PROJDOC-1.4, PROJDOC-2.1, PROJDOC-2.3, PROJDOC-7.1, PROJDOC-8.3

New user-invoked skill at `skills/project/establish-project/SKILL.md` (new `project/`
bucket), frontmatter `disable-model-invocation: true`. Three modes routed on entry:

- **create** — interview via `grilling` (REQUIRED SUB-SKILL), keeping
  `domain-modeling` active as a passive side-effect (glossary + ADR gate), then write
  `vision.md`, seed `docs/architecture/INDEX.md`, and write `guidelines.md` from the
  templates. Brownfield det, cheap: if `src/`-style code already exists, the spine
  *ratifies* the current structure rather than designing greenfield.
- **update** — revise against a change signal; any hard-to-reverse decision routes
  through the ADR gate (`domain-modeling`); retired invariants are struck, not
  renumbered (§ spine format).
- **validate** — run a checklist over `vision.md`/spine and invoke `check-invariants`
  (REQUIRED SUB-SKILL) across the specs, reporting findings.

It is user-invoked because it is a conscious once-per-project act, siblings with
`setup-repo`/`scaffold-project`. It composes model-invoked skills (`grilling`,
`domain-modeling`, `check-invariants`) but is never itself a REQUIRED SUB-SKILL
target.

### The architecture spine format — ARCH-N invariants

Satisfies: PROJDOC-1.2, PROJDOC-1.5, PROJDOC-2.2

`docs/architecture/INDEX.md` holds invariants, each a bold `**ARCH-N**` ID followed
by one imperative sentence (the rule) — grammar deliberately parallel to
`**CODE-N.M**` requirements so the same `grep` machinery reads it:

```
**ARCH-2** Every project-context consult is optional — observable-predicate plus
no-op-if-absent, never a hard gate.
```

A large project splits invariants into `docs/architecture/<domain>.md` files, each
listed from `INDEX.md`; the ID namespace (`ARCH-N`) is flat and repo-wide regardless
of file. Retirement mirrors requirement retirement: strike through
(`~~**ARCH-3**~~ superseded by ARCH-7`), never renumber — so `trace` (which deletes
struck spans) stops counting it as defined.

### check-invariants — advisory semantic conformance

Satisfies: PROJDOC-8.1, PROJDOC-8.4

New **model-invoked** skill at `skills/review/check-invariants/SKILL.md`. Interface
is deliberately narrow (deletion test: a caller rebuilding it would need only "read
each cited invariant and judge the design against it"):

- **Input:** a `design.md` (or a diff) + the architecture spine.
- **Output:** per `Respects: ARCH-N` citation, a verdict `respects | violates |
  unclear` with a one-line rationale.

It is LLM-judged and **advisory** — its verdicts inform review and never constitute a
hard merge gate (that would violate PROJDOC-6.2 / ARCH-2). It is explicitly *not*
part of `trace`: `trace` stays deterministic, this skill makes the judgment call
`trace` refuses. Callers: `code-review`, `execute-plan`'s task review, and
`establish-project` validate mode.

### trace — referential-integrity extension for ARCH citations

Satisfies: PROJDOC-3.1, PROJDOC-3.2, PROJDOC-3.3, PROJDOC-3.4, PROJDOC-3.5

Extend `skills/execution/trace/SKILL.md` with two passes and three finding codes,
all **gated on `docs/architecture/` existing** — when it does not, the passes are
skipped and the finding set is byte-for-byte today's (PROJDOC-3.5 guard).

- **Pass 5 — invariant definitions:** bold `**ARCH-N**` in `docs/architecture/*.md`.
  This is pass 1's `grep` plus one added capture step: first `grep` the `~~struck~~`
  ARCH IDs into a *retired* set, then `sed`-delete the struck spans (pass-1 idiom) and
  take the survivors as the *live* set. The delete idiom alone only removes struck IDs
  — E5 needs them captured, hence the extra step.
- **Pass 6 — Respects citations:** `grep` `Respects:.*ARCH-N` across `design.md`
  files under `docs/specs/`.
- **E4 (error):** a `Respects: ARCH-N` whose `ARCH-N` is in neither the live nor the
  retired set (never defined). — PROJDOC-3.1
- **E5 (error):** a `Respects: ARCH-N` whose `ARCH-N` is in the *retired* set. —
  PROJDOC-3.2
- **W3 (warn):** a live `**ARCH-N**` cited by no `design.md`. — PROJDOC-3.3

The `<NON-NEGOTIABLE>` block is extended by one sentence: the invariant passes check
citation existence and liveness only — never whether a design *respects* an
invariant; that judgment belongs to `check-invariants`/`code-review` (PROJDOC-3.4).

### Consult hooks — the shared no-op idiom

Satisfies: PROJDOC-4.1, PROJDOC-4.2, PROJDOC-4.3, PROJDOC-4.5, PROJDOC-4.6, PROJDOC-4.7, PROJDOC-6.1

Every hook is `WHERE <doc> exists … ; else say so once and continue`, mirroring
`brainstorm/SKILL.md:53`. Insertion points (verified `file:line`):

- **brainstorm** Step 1 (`brainstorm/SKILL.md:52-53`): if `docs/product/vision.md`
  exists, check the idea's scope against it and state in/out of product scope. —
  PROJDOC-4.1
- **write-design** Step 1 (`write-design/SKILL.md:16-26`): if the spine exists, its
  invariants are design inputs; cite each relied-upon one `Respects: ARCH-N`; a
  design that must contradict one routes through the ADR-or-supersede gate (reusing
  the existing gate at `write-design/SKILL.md:25-26,88-90`). — PROJDOC-4.2, 4.3
- **execute-plan** — in the Per-Task Loop, not the ledger setup: the task-brief
  assembly (`execute-plan/SKILL.md` step 2, ~line 32) surfaces the invariants
  relevant to the task's touched files, and the task review (step 7, ~line 37) runs
  `check-invariants` on the task diff, routing a violation back for fixes. —
  PROJDOC-4.6; guard PROJDOC-4.7.
- Absent-doc guard (PROJDOC-4.5) and the whole-workflow optionality (PROJDOC-6.1) are
  the shared no-op branch across all hooks.

(write-design's own hook is added by this feature to the very skill running now —
noted; it is a prose edit like the others.)

### code-review — advisory invariant lane

Satisfies: PROJDOC-8.2, PROJDOC-8.5

Add a step **3b. Invariant conformance** to `code-review` (after 3a, before the
parallel dispatch at `code-review/SKILL.md:44`): if `docs/architecture/` exists,
invoke `check-invariants` on the diff and carry its verdicts. Report them under a new
`## Invariants (advisory)` section in step 5 — a *third lane*, kept out of the two
hard axes so the deliberate Standards/Spec separation (`code-review/SKILL.md:54-56`)
is preserved and nothing here becomes a hard gate. If `docs/architecture/` is absent,
the step is skipped and code-review is unchanged (PROJDOC-8.5 guard).

### write-plan — constraint sourcing and guidelines split

Satisfies: PROJDOC-4.4, PROJDOC-7.2, PROJDOC-7.3, PROJDOC-7.5

At `write-plan/SKILL.md:22-25`, Global Constraints today copy rules "from the design
and `docs/agents/project.md`". Extend the source list:

- If the architecture spine exists, fold its hard rules into Global Constraints so
  every task brief inherits them (PROJDOC-4.4).
- Source human-facing engineering rules from `docs/product/guidelines.md` when it
  exists (PROJDOC-7.2), else from `docs/agents/project.md` as today (PROJDOC-7.5
  guard). `docs/agents/project.md` is documented as machine-config + a pointer to
  the guidelines doc (PROJDOC-7.3); its template (`templates/agents/project.md`)
  gains the pointer line.

`execute-plan` needs no change to its constraint *sourcing* — it already copies
Global Constraints verbatim (`execute-plan/SKILL.md:23`); the invariant-awareness it
gains is the Per-Task-Loop hook in the section above.

### setup-repo / scaffold-project — opt-in and migration

Satisfies: PROJDOC-5.1, PROJDOC-5.2, PROJDOC-5.3, PROJDOC-5.4, PROJDOC-7.4

- **setup-repo** Step 2 gains decision **G. Project-docs layer** (default **No**),
  after 2F (`setup-repo/SKILL.md:106-114`). On opt-in, Step 4
  (`setup-repo/SKILL.md:125-173`) seeds the three docs from templates and adds a
  project-docs line to the `## Agent skills` block (`:151-169`) — PROJDOC-5.1, 5.2.
  If `docs/agents/project.md` already carries guidelines, Step 2G offers to migrate
  them into `guidelines.md`, leaving a pointer (PROJDOC-7.4).
- **scaffold-project** Step 2.8 (`scaffold-project/SKILL.md:74`) seeds the three docs
  alongside the existing `CONTEXT.md`/`INDEX.md` seeds, only when opted in
  (PROJDOC-5.3).
- Not opting in changes nothing about either skill's output (PROJDOC-5.4 guard).

### Optionality and dogfood invariants

Satisfies: PROJDOC-6.2

The layer adds no mandatory tooling, no artifact that must be kept fresh (the spine
is read live, never generated), and no new hard gate — the one deterministic
addition (`trace` E4/E5/W3) only extends an existing agent-run check. To dogfood the
layer on this repo, a task creates `docs/architecture/INDEX.md` seeded with the skill
set's own invariants:

- **ARCH-1** The `trace` check is deterministic — `grep`/set-difference only, never
  semantic judgment.
- **ARCH-2** Every project-context consult is optional — observable-predicate plus
  no-op-if-absent, never a hard gate.
- **ARCH-3** A consuming repo installs nothing executable beyond the session-start
  hook — no vendored scripts, linters, or CI.
- **ARCH-4** An Approved requirement or invariant ID is immutable — retired by
  strikethrough, never renumbered.
- **ARCH-5** A user-invoked skill is never a REQUIRED SUB-SKILL target; only
  model-invoked skills compose as sub-skills.

Registration: both new skills are appended to `.claude-plugin/plugin.json`'s
`skills` array (so they group under "Jayden Skills" in the picker) and added to the
`AGENTS.md` / `DESIGN.md` inventories. `DESIGN.md` gains a "The project layer"
section recording this. The skill-count drift is three-way and reconciled while
there: `AGENTS.md` says 31, `DESIGN.md` enumerates 32 (missing one), and
`plugin.json` + the guide + the filesystem have 33 — after this feature's two new
skills the true count is **35**, which all surfaces are updated to.

## Seams for testing

Per the approved verification approach (baseline scenarios, no automated test code),
each "seam" is the skill invocation that exercises the requirement; evidence is a
documented baseline scenario, cited as coverage. No new automated test seam is added.

| Seam | Kind | Covers |
|---|---|---|
| `establish-project` create run → three docs produced | baseline | PROJDOC-1.1, 1.2, 1.3, 1.4, 7.1 |
| `establish-project` update/validate runs | baseline | PROJDOC-2.1, 2.2, 2.3, 8.3 |
| architecture spine file (ARCH-N grammar, per-domain, strike) | baseline | PROJDOC-1.5, 2.2 |
| `trace` run on a fixture with ARCH defs + Respects citations | baseline | PROJDOC-3.1, 3.2, 3.3, 3.4, 3.5 |
| `check-invariants` run on a design + spine | baseline | PROJDOC-8.1, 8.4 |
| brainstorm / write-design / execute-plan consult runs | baseline | PROJDOC-4.1, 4.2, 4.3, 4.5, 4.6, 4.7, 6.1 |
| `code-review` run with/without a spine | baseline | PROJDOC-8.2, 8.5 |
| `write-plan` Global Constraints sourcing run | baseline | PROJDOC-4.4, 7.2, 7.3, 7.5 |
| `setup-repo` / `scaffold-project` opt-in + migration runs | baseline | PROJDOC-5.1, 5.2, 5.3, 5.4, 7.4 |
| optionality / no-tooling review of the diff | baseline | PROJDOC-6.2 |

## Coverage check

Every PROJDOC ID appears in exactly one Satisfies line:

- Story 1: 1.1,1.3,1.4 (establish-project) · 1.2,1.5 (spine format)
- Story 2: 2.1,2.3 (establish-project) · 2.2 (spine format)
- Story 3: 3.1,3.2,3.3,3.4,3.5 (trace)
- Story 4: 4.1,4.2,4.3,4.5,4.6,4.7 (consult hooks) · 4.4 (write-plan)
- Story 5: 5.1,5.2,5.3,5.4 (setup/scaffold)
- Story 6: 6.1 (consult hooks) · 6.2 (optionality/dogfood)
- Story 7: 7.1 (establish-project) · 7.2,7.3,7.5 (write-plan) · 7.4 (setup/scaffold)
- Story 8: 8.1,8.4 (check-invariants) · 8.2,8.5 (code-review) · 8.3 (establish-project)

All 36 criteria mapped; none deliberately unmapped.
