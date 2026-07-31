# Design: Roadmap layer

Feature code: RMAP
Status: Implemented
Date: 2026-07-25
Requirements: ./requirements.md

## Context

The skill set today is a vertical feature pipeline with an optional layer above it.
`define-project` writes the north star (`docs/product/vision.md`), an `ARCH-N`
invariant spine, and engineering guidelines. `specify-behavior` opens a feature,
registers its code in `docs/specs/INDEX.md`, and starts the `CODE-N.M` traceability
spine that `audit-trace` verifies. Between those two there is nothing: no artifact decides
which features exist, in what order, grouped into what shippable milestone.

That gap is not hypothetical — it is a step the set already performs and immediately
discards. `frame-change` step 5 (`skills/discovery/frame-change/SKILL.md:115`) decomposes
multi-subsystem work into named sub-features with relationships and build order, then
says "frame-change continues with the first one only". The other sub-features exist in
the conversation and nowhere else. This feature gives that decomposition a durable
home and a way to check it against reality later.

The constraint that shapes the whole approach is `feature-graph.md`'s principle —
*"there is no derived copy of anything to fall behind"* — reinforced by **ARCH-1**
(vertical checks are exact `grep`/`git` passes, never LLM judgment) and **ARCH-2**
(optional layers no-op when absent). BMAD, the researched prior art, stores progress in
a `sprint-status.yaml` whose own reader warns "may be stale" when its timestamp is more
than seven days old. That warning is the design flaw admitting itself. So this design
splits the two things BMAD conflates: **intent** (a human decided to commit to a
milestone — underivable, therefore written down) and **progress** (derivable from
`Status:` plus git — therefore never written down).

`refresh-roadmap-status` is consequently shaped as *`audit-trace` for the horizontal layer*: the same
structure of finding codes, fixed passes, and set-difference rules that makes two agents
running `audit-trace` on one repo reach the same finding set. It is read-only by contract, and
it reports rather than repairs — repair belongs to `realign-spec`, which already owns
`Status:` realignment and the INDEX update (`skills/track/realign-spec/SKILL.md:43,45`).

## Decisions

1. **Progress is derived, never stored.** No file of the `sprint-status.yaml` shape.
   `refresh-roadmap-status` recomputes from `docs/roadmap/INDEX.md`, `docs/specs/INDEX.md`, each
   feature's `requirements.md` `Status:`, `git`, and optionally `.skills/progress.md`.
   This is hard to reverse, surprising against the prior art, and a real trade-off —
   **it needs an ADR** (see *Open action* below).
2. **Three namespaces, three owners.** `GOAL-N` in `vision.md` (`define-project`),
   `MILE-N` and `ROAD-N` in `docs/roadmap/INDEX.md` (`plan-milestones`), feature codes and
   `CODE-N.M` in `docs/specs/` (`specify-behavior`). No skill writes another's
   namespace.
3. **The binding is a column in `docs/specs/INDEX.md`, written by the registrar.**
   `specify-behavior` already writes that row; adding `Roadmap item` there means
   `refresh-roadmap-status` joins plan to spec with one `grep` and no name-matching heuristic.
   `plan-milestones` never touches the file.
4. **`plan-milestones` is model-invocable; `refresh-roadmap-status` is user-invoked.** `frame-change`
   must be able to reach the first (RMAP-1.13); nothing needs to reach the second, so it
   pays no context load (RMAP-3.13). Consequence, from **ARCH-5**: `plan-milestones` may
   not invoke `refresh-roadmap-status` — it may only name it.
5. **The artifact's structural rule list lives in the template comment.** Because of
   decision 4 the two skills cannot share validation by invocation, and cross-folder file
   links are forbidden. `templates/roadmap-INDEX.md` carries the authoritative rule block
   — the same house pattern as `templates/architecture-INDEX.md`, whose comment holds the
   `ARCH-N` grammar and immutability rules. Both skills read the template; each names the
   defect categories in one line for reliability. Trade-off stated in *Known duplication*.
6. **No new architecture invariant.** `ARCH-4` covers `CODE-N.M` and `ARCH-N` only, and
   this design does not extend it. `MILE-N`/`ROAD-N`/`GOAL-N` stability is a skill-local
   rule (RMAP-1.11, RMAP-2.9). Nothing here contradicts a live invariant, so no
   supersede event.
7. **`audit-trace` is untouched.** Planning-ID referential integrity lives in `refresh-roadmap-status`
   (RMAP-2.10). `audit-trace` keeps exactly its E1–E5 / W1–W3 finding set.
8. **The priority ladder is a pure function of artifact state**, evaluated top-down with
   first-match-wins and fixed tie-breaks, so identical state yields an identical
   recommendation (RMAP-3.10).

## Architecture

### The roadmap artifact and its template

Satisfies: RMAP-1.1, RMAP-1.2, RMAP-1.3, RMAP-1.15, RMAP-1.16, RMAP-1.20
Respects: ARCH-2
Reuse: existing — extends the `templates/architecture-INDEX.md` shape: summary table + per-item block + a comment block holding the ID grammar and stability rules (rung 2)

New file `templates/roadmap-INDEX.md`, filled to `docs/roadmap/INDEX.md`. Every heading
is a REQUIRED slot; unfilled slots read `None`.

```markdown
# Roadmap: <Project Name>

Status: Draft
Date: <YYYY-MM-DD>

<!-- Structural rules — authoritative. Both plan-milestones and refresh-roadmap-status read this
     block. A roadmap is structurally defective when any of these does not hold:
     S1 every MILE-N and ROAD-N is defined exactly once
     S2 every ROAD-N sits under exactly one milestone
     S3 every milestone carries a non-empty Outcome sentence
     S4 no Depends-on names a milestone appearing later in the table
     S5 every Depends-on resolves to exactly one live, non-struck-through MILE-N
     S6 every GOAL-N in vision.md is cited by a milestone or listed under Goal dispositions
     S7 the milestone table and every milestone block parse
     IDs are stable from first definition. Retire by strikethrough with a reason
     (~~**MILE-3**~~ superseded by MILE-5); never renumber, never reuse. A ROAD-N keeps
     its ID when it moves between milestones. -->

| ID | Milestone | Outcome | Depends-on | Commitment |
|---|---|---|---|---|
| MILE-1 | <name> | <one testable user-value sentence> | none | Committed |

## MILE-1 — <name>

**Outcome:** <one testable user-value sentence>
**Goals:** GOAL-1, GOAL-2
**Members:**
- **ROAD-1** <slug> — Surfaces: `src/a/`, `src/b.ts`
- **ROAD-2** <slug> — Surfaces: None — new subsystem, paths unknown until design
**Depends-on:** none
**Commitment:** Committed <YYYY-MM-DD>
**Closed:** None
**Deferred:** None
**Blockers:** None

## Goal dispositions

| Goal | Disposition | Date | Reason |
|---|---|---|---|
| GOAL-4 | Out-of-scope | <YYYY-MM-DD> | <reason> |
```

Milestone **order is table row order**; identity is the `MILE-N` ID. The two are
independent, so reordering never renumbers (RMAP-1.11, RMAP-1.12). Absent the file, the
whole layer no-ops (ARCH-2).

### `plan-milestones` — authoring and the approval gate

Satisfies: RMAP-1.4, RMAP-1.7, RMAP-1.8, RMAP-1.9, RMAP-1.10, RMAP-1.11, RMAP-1.12, RMAP-1.13, RMAP-1.14, RMAP-1.17, RMAP-1.18, RMAP-1.19
Respects: ARCH-2, ARCH-5
Reuse: existing — `define-project`'s create/update mode split plus `specify-behavior`' present-the-file-and-STOP gate (rung 2)

`skills/project/plan-milestones/SKILL.md`, model-invocable, in `project/` beside
`define-project` because it belongs to the repo-level layer rather than a single
feature's spec triad.

**Create** — fill the template, then run the decomposition discipline, ported from the
researched BMAD `step-02-design-epics.md` and stated as positive rules: group milestones
by user value; make each one standalone and enabling of those after it; prefer fewer and
larger when the design is settled, splitting at a genuine risk boundary. Cite `GOAL-N` per
milestone when a vision exists, else record `Goals: None`.

**Two rules the baseline retired.** Forward-dependency detection (struck RMAP-1.5) and
surface-overlap consolidation (struck RMAP-1.6) are **not** written into this skill: fresh
agents performed both unprompted, so the text would be a no-op. Forward dependencies are
still caught structurally — S4 in the template rule block, enforced by this skill's gate
(RMAP-1.18) and by `refresh-roadmap-status`'s R11. The `Surfaces:` slot stays (RMAP-1.20) because it
is the input that makes overlap visible in the first place; what is retired is the
instruction to reason about it, not the data.

**Update** — a material change (outcome, membership, ordering, commitment state, goal
citations) sets `Status: Draft`, preserves every existing ID, and re-enters the gate
(RMAP-1.19). An item leaving a milestone lands in `Deferred` with a date and reason
rather than disappearing (RMAP-1.7).

**The gate** — validate S1–S7 from the template's rule block; any defect is reported and
withholds the gate (RMAP-1.18, which covers the forward-dependency case as S4). When clean,
present the whole file and STOP; only explicit user approval writes `Status: Approved`
(RMAP-1.17).

`docs/specs/INDEX.md` is outside this skill's write set (RMAP-1.14). Its exit **names**
`/refresh-roadmap-status` for the user rather than invoking it, per ARCH-5 and enforced by the
existing `scripts/lint-handoffs.py`.

### `refresh-roadmap-status` — the passes

Satisfies: RMAP-3.1, RMAP-3.2, RMAP-3.3, RMAP-3.4, RMAP-3.5, RMAP-3.6, RMAP-3.7, RMAP-3.8, RMAP-3.9, RMAP-3.12, RMAP-3.13, RMAP-3.14, RMAP-3.15, RMAP-3.17, RMAP-3.18, RMAP-3.19, RMAP-3.20, RMAP-4.1, RMAP-4.2, RMAP-4.3, RMAP-4.4
Respects: ARCH-1, ARCH-2, ARCH-3, ARCH-5
Reuse: existing — `audit-trace`'s structure wholesale: finding-code table → Inputs → numbered fixed passes → set-difference rules → a non-negotiable no-judgment clause → counts-then-findings output (rung 2)

`skills/track/refresh-roadmap-status/SKILL.md`, user-invoked (`disable-model-invocation: true`),
in `track/` beside `realign-spec` and `reroute-plan`.

Six passes, each one full read of a source, mirroring `audit-trace`'s grammar. `git` is called
a fixed number of times — once for the milestone range when a `Closed` marker exists —
independent of feature and milestone count (RMAP-4.1).

```bash
# 1. Goal definitions — live and retired, strike spans deleted first as in audit-trace pass 5
grep -hoE '~~\*\*GOAL-[0-9]+\*\*~~' docs/product/vision.md | grep -oE 'GOAL-[0-9]+' | sort    # retired
sed -E 's/~~[^~]*~~//g' docs/product/vision.md | grep -oE '\*\*GOAL-[0-9]+\*\*' \
  | grep -oE 'GOAL-[0-9]+' | sort                                                             # live, duplicates kept

# 2. Milestone and item definitions, membership, and order
grep -nE '^\| MILE-[0-9]+ \||^## MILE-[0-9]+|^- \*\*ROAD-[0-9]+\*\*|^\*\*(Outcome|Goals|Depends-on|Commitment|Closed|Deferred):' docs/roadmap/INDEX.md

# 3. Goal dispositions
grep -nE '^\| GOAL-[0-9]+ \| (Deferred|Out-of-scope) \|' docs/roadmap/INDEX.md

# 4. Feature bindings
grep -nE '^\| [A-Z][A-Z0-9]{1,11} \|' docs/specs/INDEX.md

# 5. Feature spec statuses
grep -rnE '^Status:' docs/specs --include='*requirements.md'

# 6. Advisory ledger — only when it exists
test -f .skills/progress.md && grep -nE '^Task ' .skills/progress.md
```

Pass 1 keeps duplicates rather than `sort -u`, because a repeated `GOAL-N` is itself the
R3 finding. Retired IDs are captured before deletion so a citation of a struck ID is a
finding rather than a silent resolution.

Findings, with `defined`, `cited`, `dispositioned`, `bound`, `status` in hand:

| Code | Tier | Condition | Withholds |
|---|---|---|---|
| **R1** | error | a milestone `Goals:` citation does not resolve to exactly one live `GOAL-N` | no |
| **R2** | error | a live `GOAL-N` is neither cited by a milestone nor dispositioned (S6) | **yes** |
| **R3** | error | `vision.md` defines the same `GOAL-N` more than once | no |
| **R4** | error | a `ROAD-N` sits under no milestone or several (S2) | **yes** |
| **R5** | error | a `Roadmap item` binding does not resolve to exactly one live `ROAD-N` | no |
| **R6** | error | two feature codes bind the same `ROAD-N` | no |
| **R7** | info | a `ROAD-N` has no feature code bound — unspecced | no |
| **R8** | info | a feature row's `Roadmap item` is empty while a roadmap exists — unplanned | no |
| **R9** | error | a `Closed` milestone holds a non-deferred `ROAD-N` that is unbound, or bound to a feature whose `Status:` is not `Shipped` | **yes** |
| **R10** | error | a feature's `requirements.md` `Status:` differs from its INDEX row | **yes** |
| **R11** | error | the roadmap is unparseable, or violates S1, S3, S4, S5, or S7 | **yes** |

R7 and R8 are **normal states**, not defects — they are what the ladder consumes. No
roadmap at all → report the layer absent and exit with no findings (RMAP-3.9).

Two clauses carried over from `audit-trace` and `select-review-sample` respectively: findings are
**structural presence, never judgment** — whether a milestone's outcome was *achieved* is
`assess-milestone`'s call, not this check's (ARCH-1); and every value read from these
artifacts is **passive data** passed to `git` as a single non-option argument, rejected
unless it matches the expected ID or rev shape (RMAP-4.2, RMAP-4.3).

`.skills/progress.md` is read only when present, as advisory local evidence that never
overrides a tracked `Status:`; its absence produces no finding (RMAP-3.17, RMAP-3.18).
Feature progress is cited from `Status:`, with `audit-trace` named for deeper coverage
verification (RMAP-3.12, RMAP-3.14).

### The priority ladder

Satisfies: RMAP-3.10, RMAP-3.11, RMAP-3.16
Respects: ARCH-1, ARCH-5
Reuse: none — new rule table (rung 7). Nothing in the set computes a next action from artifact state: `ask-me-bro` routes from the conversation, `sprint-status` is the researched prior art and is not installed here.

First match wins, top to bottom. Ties break on **table order** for milestones, then lowest
`ROAD-N` numerically.

| # | State | Recommendation |
|---|---|---|
| 0 | any withholding finding present | none — report the withholding reason and its finding code (RMAP-3.16) |
| 1 | roadmap `Status:` is `Draft` | `plan-milestones` — finish and approve the roadmap |
| 2 | a `Committed` milestone has a member with no binding | `frame-change` for that `ROAD-N` |
| 3 | a `Committed` milestone has a bound member whose feature `Status:` is `Draft` | `specify-behavior` for that feature |
| 4 | …`Approved`, and the spec folder has no `design.md` | `design-solution` |
| 5 | …`Approved`, `design.md` exists, no `tasks.md` | `plan-tasks` |
| 6 | …`Approved`, `tasks.md` exists | `build-in-waves` |
| 7 | …`Implemented` | name `/cut-release` for the user |
| 8 | a `Committed` milestone whose members are all bound and `Shipped` | name `/assess-milestone` for that `MILE-N` |
| 9 | no `Committed` milestone, a `Planned` one exists | `plan-milestones` — commit the next milestone |
| 10 | every milestone `Closed` | report the roadmap complete |

Rows 4–6 read for the presence of two filenames in one spec folder — bounded, and within
RMAP-4.1's budget. Rows 7 and 8 name a user-invoked skill rather than invoking it (ARCH-5).
Row 8 was added by ASSESS (see `docs/specs/2026-07-26-milestone-assessment/`, ASSESS-5.2);
this table remains the ladder's single statement, mirrored into `refresh-roadmap-status`'s body.

**Standup mode** renders the same derivation as a card: the milestone in flight, the
current status of its `ROAD-N` members, and the one next action (RMAP-3.11). One skill,
two renderings — no second skill until team-ceremony responsibilities appear.

### `frame-change` — persist the decomposition

Satisfies: RMAP-2.1, RMAP-2.2, RMAP-2.3
Respects: ARCH-2, ARCH-5
Reuse: existing — the `REQUIRED SUB-SKILL:` prose mechanism already used at frame-change steps 2, 3, and 6 (rung 2)

Step 5 already decomposes (`frame-change/SKILL.md:115`). The edit adds one conditional: when
the decomposition names two or more independent sub-features, `REQUIRED SUB-SKILL: use
`plan-milestones`` to persist them as `ROAD-N` items — adding to an existing roadmap rather
than starting a new one (RMAP-2.2) — before step 6 continues the first item into
`specify-behavior`. Single-subsystem work is untouched: step 6's existing exits stand
(RMAP-2.3).

### `specify-behavior` — write the binding

Satisfies: RMAP-2.4, RMAP-2.5, RMAP-2.6
Respects: ARCH-2, ARCH-4
Reuse: existing — extends Step 1's INDEX row write, already the sole registration point (rung 2)

`templates/specs-INDEX.md` gains a fifth column:

```markdown
| Code | Feature | Spec | Status | Roadmap item |
|---|---|---|---|---|
| SHELL | Left icon rail | ./2026-07-09-shell/ | Implemented | ROAD-3 |
```

Step 1 gains one sentence: when the work implements a roadmap item, record its `ROAD-N` in
that column; with no roadmap, leave it empty and register unchanged (RMAP-2.5, ARCH-2).
Registration ownership, code uniqueness, and the `Draft` initial status are unchanged
(RMAP-2.6).

`docs/specs/INDEX.md` in this repo gains the column and the `RMAP` row's own binding once
a roadmap exists here.

**Two guide docs carry a copy of the four-column table** and go stale on this change:
`docs/guide/concepts/artifacts.md` and `docs/guide/concepts/feature-graph.md:42-46`. Both
must be updated in the same change. No skill parses the table by column position — every
consumer reads the `Status` cell semantically — so appending a trailing column is safe for
`frame-change` step 1, `realign-spec`, `plan-tasks`'s status confirmation, and the feature-overlap
search.

### `define-project` — `GOAL-N` identity and migration

Satisfies: RMAP-2.7, RMAP-2.8, RMAP-2.9
Respects: ARCH-2
Reuse: existing — the bold-ID grammar and strikethrough retirement already used for `**ARCH-N**` in `templates/architecture-INDEX.md` (rung 2)

`templates/product-vision.md`'s `## Goals` section becomes IDed, matching the `ARCH-N`
grammar so the same `grep`/`sed` retirement handling applies:

```markdown
## Goals

- **GOAL-1** <concrete, checkable aim>
- **GOAL-2** <concrete, checkable aim>
```

Create mode assigns IDs as it writes (RMAP-2.7). Update mode on a vision whose goals carry
no IDs assigns them in document order and reports the migration (RMAP-2.8) — the accepted
breaking change. Once a goal has been recorded in an approved vision it is immutable across
later updates, retired by strikethrough with a reason (RMAP-2.9). This repo's own
`docs/product/vision.md` is `Status: Approved`, so it is the first migration subject.

### `audit-trace` — unchanged

Satisfies: RMAP-2.10
Respects: ARCH-1
Reuse: existing — `audit-trace` as it stands; this feature adds nothing to it (rung 1 — no requirement forces a change)

`audit-trace` keeps exactly its E1–E5 / W1–W3 finding set over `CODE-N.M` and `ARCH-N`.
Planning-ID referential integrity is `refresh-roadmap-status`'s R1–R11, and the two never overlap:
`audit-trace` never reads `docs/roadmap/INDEX.md` or the `Goals` section of `vision.md`, and
`refresh-roadmap-status` never reads `tasks.md` footers or test annotations. The one place they
touch the same string is a feature's `Status:` line — `audit-trace` uses it for E2/W1 coverage
obligations, `refresh-roadmap-status` for R10 drift and the ladder — and neither writes it.

### Test harness — repo-local infrastructure, never a runtime dependency

Infrastructure — no `Satisfies:` line: this section builds the means of verification, not
a behavior the requirements ask for. The scale fixture it holds is what RMAP-4.1's seam row
is written against.

Respects: ARCH-3
Reuse: existing — `scripts/lint-*.py` plus the `unittest` convention already declared in `docs/agents/project.md` (rung 2)

**ARCH-3 forbids mandating Python for adoption**, so the deterministic rules live in
`refresh-roadmap-status`'s body as `grep` recipes exactly like `audit-trace`'s. The repo-local harness
under `tests/roadmap/` exists only to unit-test those rules against fixtures and to hold
the 200-feature / 50-milestone scale fixture. A consuming repo installs the skills and
markdown alone.

## Seams for testing

New seams: one — the fixture-repo tree under `tests/roadmap/`. Everything else reuses the
two existing lint scripts and the scenario-markdown convention declared in
`docs/agents/project.md`.

| Seam | Kind | Covers |
|---|---|---|
| `templates/roadmap-INDEX.md` required-slot lint | unit | RMAP-1.1, RMAP-1.2, RMAP-1.3, RMAP-1.15, RMAP-1.16, RMAP-1.20 |
| `plan-milestones` gate over fixture roadmaps | scenario | RMAP-1.7, RMAP-1.8, RMAP-1.9, RMAP-1.10, RMAP-1.11, RMAP-1.12, RMAP-1.14, RMAP-1.17, RMAP-1.18, RMAP-1.19 |
| `scripts/lint-skill-frontmatter.py` (existing) | unit | RMAP-1.13, RMAP-3.13 |
| `frame-change` decomposition scenarios (multi- and single-subsystem) | scenario | RMAP-2.1, RMAP-2.2, RMAP-2.3 |
| `specify-behavior` Step 1 binding scenarios (roadmap present / absent) | scenario | RMAP-2.4, RMAP-2.5, RMAP-2.6 |
| `define-project` vision scenarios (create / un-IDed migration / approved update) | scenario | RMAP-2.7, RMAP-2.8, RMAP-2.9 |
| `audit-trace` regression over this repo | unit | RMAP-2.10 |
| `refresh-roadmap-status` rule application over `tests/roadmap/` fixtures | unit | RMAP-3.2, RMAP-3.3, RMAP-3.4, RMAP-3.5, RMAP-3.6, RMAP-3.7, RMAP-3.8, RMAP-3.19, RMAP-3.20, RMAP-4.4 |
| `refresh-roadmap-status` read-only + input-set assertion | scenario | RMAP-3.1, RMAP-3.12, RMAP-3.14 |
| `refresh-roadmap-status` absent-layer no-op | scenario | RMAP-3.9 |
| Priority-ladder fixture table (state → recommendation) | unit | RMAP-3.10, RMAP-3.16 |
| Standup-mode rendering | scenario | RMAP-3.11 |
| Premature-closure fixture | unit | RMAP-3.15 |
| `.skills/progress.md` advisory scenarios (present / absent) | scenario | RMAP-3.17, RMAP-3.18 |
| Scale fixture — 200 features, 50 milestones | unit | RMAP-4.1 |
| Argument-safety and injection scenarios | scenario | RMAP-4.2, RMAP-4.3 |
| `scripts/lint-handoffs.py` (existing) | unit | *(ARCH-5 boundary for RMAP-1.13, RMAP-3.13 — no new ID)* |

## Coverage check

All **52 live** requirement IDs appear in exactly one `Satisfies:` line — verified
mechanically by diffing the bold definitions in `requirements.md` against the IDs on every
`Satisfies:` line in this file. Story 1: 18/18 live. Story 2: 10/10. Story 3: 20/20.
Story 4: 4/4. No deliberately unmapped IDs, no ID cited twice, no `Satisfies:` line citing
an ID the requirements do not define.

`RMAP-1.5` and `RMAP-1.6` were retired by strikethrough on 2026-07-25 after their RED
baseline showed no failure. A struck ID counts as undefined, so no `Satisfies:` line, seam
row, or task footer may cite either one.

One section carries no `Satisfies:` line and declares itself infrastructure: the test
harness, which builds the means of verification rather than a required behavior.

## Known duplication

Decision 5's consequence: because `plan-milestones` (model-invocable) may not invoke
`refresh-roadmap-status` (user-invoked) under ARCH-5, the S1–S7 structural rules are authored once
in `templates/roadmap-INDEX.md` and *named* — not restated — in both skill bodies. The
residual risk is that a future edit changes one skill's summary without the template. The
mitigation is that the template is the file both skills load, and the fixture suite tests
both sides against the same fixtures.

## Open action before approval

Decision 1 — derive rather than store — is hard to reverse, surprising against the prior
art, and carries a real trade-off (no baseline for run-to-run diffing; intent that exists
in no artifact is invisible). It meets all three ADR conditions, so it needs an ADR, and
`define-domain` owns that gate. I have not written it yet: it is a separate skill run
with its own gate, and I would rather you see this design first than have an ADR land
inside the same turn. Say the word and I will run `define-domain` before you approve, or
right after.
