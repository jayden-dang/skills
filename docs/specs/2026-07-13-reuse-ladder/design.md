# Design: Reuse-first ladder in write-design and write-plan

Feature code: REUSE
Status: Implemented
Date: 2026-07-13
Requirements: ./requirements.md

## Context

The methodology already fights duplication at two altitudes. At the **feature**
level, `brainstorm` step 1 and `code-review` step 3a grep `docs/specs/` for a spec
that already owns the surface, and `code-review` emits a **reuse-miss** finding when
a diff rebuilds what a neighbour feature owns (`code-review/SKILL.md:54`). At the
**interface** level, `write-design` Step 2 applies the deletion test
(`write-design/SKILL.md:56-59`) to keep a module's interface deeper than what it
hides. Between them sits an unguarded gap: nothing checks, for a *single component*,
whether a helper three files over, the stdlib, a platform feature, or an
already-installed dependency already does the job. That gap is where an agent
designs a new component — and then `write-plan` emits a "create X" task an
implementer dutifully writes from scratch. This is the from-scratch/over-build
failure mode the feature targets, imported as a discipline from the external
Ponytail skill (`.skills/ponytail-research.md`).

The governing constraint is **additivity without a new gate** — the repo's optionality
principle. `write-design` Step 1 already dispatches a scan subagent that maps "what
exists today" (`write-design/SKILL.md:16-18`); the ladder is cheap precisely because
it *consumes that existing evidence* rather than launching its own research pass. So
every part of this feature is a prose extension to two existing skills at their
existing steps, emitting advisory findings through the Step-4 coverage passes those
skills already run — no new machinery, no new skill (the count stays 36), and a
feature with no reuse opportunity produces byte-identical output to today.

The second constraint is that the ladder must not become a *third* fuzzy "think about
reuse" instruction competing with the scan and the deletion test. The three are kept
on a stated **scan → ladder → deletion-test** chain, each answering a different
question: the scan *gathers* what exists, the ladder decides *whether* to build, and
the deletion test (scoped now to rung-7 new code) decides how to build it *deep*.

This is single-design work: the shape is established (prose edits to two skills at
named steps), the interface is not in question, so there is no multi-variant bake-off.
No `docs/architecture/` spine drives it, so the sections below carry `Satisfies:` lines
only.

## Decisions

1. **The ladder is a Step-2 sub-gate in `write-design`, placed *before* the deletion
   test**, and the deletion-test paragraph is rescoped to apply to rung-7 new code. The
   ladder decides whether to build; the deletion test refines only what survives to
   rung 7. This ordering is stated in the skill so the three levers stay distinct.
2. **One shared `Reuse: <rung> — <concrete target>` line** in both skills — beside each
   `Satisfies:` line in `write-design`, and in each task's Files block in `write-plan`.
   Identical grammar means the plan's line is the design's line carried down, which is
   exactly what the plan's consistency check compares.
3. **Everything is advisory.** The Step-4 checks emit findings (a missing/justification-
   less `Reuse:` line; a component-level reuse-miss; a design↔task `Reuse:` mismatch) but
   nothing blocks approval or a commit — consistent with the optionality principle and
   REUSE-2.4 / REUSE-5.3.
4. **Enforcement reuses each skill's existing Step-4 pass**; no new check step is added.
   The plan's finding reuses `code-review`'s **reuse-miss** term at component granularity
   (the glossary now defines both granularities).
5. **No roster/count/guide changes.** This extends two existing skills; `plugin.json`,
   `AGENTS.md`, `DESIGN.md`, and the guide counts are untouched (still 36). No ADR is
   warranted — every choice follows an existing idiom (a Step sub-section, the existing
   coverage pass, the advisory-finding pattern).

## Architecture

### 1. `write-design` Step 2 — the reuse-ladder sub-gate

Satisfies: REUSE-1.1, REUSE-1.2, REUSE-1.3, REUSE-5.1, REUSE-5.2

Insert a labelled sub-gate into Step 2 (`write-design/SKILL.md`, after the "design it
twice" guidance and *before* the "Design for depth / deletion test" paragraph at line
56). It instructs: before committing to build any component, climb a seven-rung reuse
ladder, stopping at the highest rung that holds —

1. Does it need to exist at all? (YAGNI)
2. Already in this codebase? (a helper/util/type/pattern the scan found → reuse/extend)
3. Standard library or language builtin?
4. A platform / framework / runtime feature?
5. An already-installed dependency? (don't add a new one for a few lines)
6. Can it be one line?
7. Only then, the minimum new code that works.

The block states three binding qualifiers: the ladder is **fed by the Step-1 scan
digest** and climbed **only after understanding the problem** (trace the real flow — it
is a reflex, not a research project) (REUSE-1.1, REUSE-1.2); and it **must not prune
away** input validation at trust boundaries, error handling that prevents data loss,
security, accessibility, or anything the requirements explicitly requested (REUSE-1.3).
It also states the **scan → ladder → deletion-test chain** explicitly (REUSE-5.1) and
rescopes the existing deletion-test paragraph to "for a rung-7 new component, apply the
deletion test" — leaving the scan subagent and the deletion test themselves running
unchanged, the ladder consuming one and preceding the other (REUSE-5.2 guard).

### 2. `write-design` — the `Reuse:` line, new-code justification, new-dependency callout

Satisfies: REUSE-2.1, REUSE-2.2, REUSE-2.3, REUSE-2.4

Extend the Satisfies-line paragraph (`write-design/SKILL.md:38-40`) so every `###`
architecture section carries a `Reuse: <rung> — <concrete target>` line **beside** its
`Satisfies:` line — naming the highest rung that held and the concrete existing artifact
it builds on, or `none — new code (rung 7)` (REUSE-2.1). A rung-7 line carries a one-line
justification for why no lower rung held (REUSE-2.2). A section that introduces a
brand-new third-party dependency (rung 5 *adding*, not reusing) carries a distinct
callout so the dependency is visible at the design approval gate (REUSE-2.3). The skill
states that the `Reuse:` line and the new-dependency callout are **advisory** — surfaced
at the approval gate, never a hard blocker (REUSE-2.4).

### 3. `write-design` Step 4 — reuse-coverage self-check

Satisfies: REUSE-4.1

Add one bullet to the Step-4 coverage self-check (`write-design/SKILL.md:71-75`, the pass
that already walks "every ID appears in exactly one Satisfies line"): in the same walk,
verify that **every architecture section carries a `Reuse:` line** and that every rung-7
or new-dependency line **carries its justification**. It rides the existing pass — no new
review step.

### 4. `write-plan` Step 3 — the task `Reuse:` line

Satisfies: REUSE-3.1, REUSE-3.2

Add a `Reuse:` sub-bullet to the task **Files** block (`write-plan/SKILL.md:48`, beside
`Create / Modify / Test`): each task names the concrete existing code, library, or
pattern it builds on, so the implementer brief carries "build on these, do not
reimplement" (REUSE-3.1). The skill states that a task's `Reuse:` line must stay
**consistent with the `Reuse:` line of the design section it implements** (REUSE-3.2) —
the same grammar (Decision 2) makes this a direct comparison.

### 5. `write-plan` Step 4 — reuse-miss and consistency check

Satisfies: REUSE-4.2, REUSE-4.3

Add two bullets to the Step-4 coverage/consistency check (`write-plan/SKILL.md:70-88`,
where "Type/name consistency across tasks" already lives): flag as a **component-level
reuse-miss** any task whose Files **Create** something the scan digest or an
already-installed dependency already provides (REUSE-4.2); and flag any task whose
`Reuse:` line is **inconsistent** with the design section it implements (REUSE-4.3). Both
are advisory findings in the existing pass, mirroring how that pass already reports
type/name inconsistencies.

### 6. Additivity guard

Satisfies: REUSE-5.3

The skill wording makes the `Reuse:` line additive: where a feature's design or plan has
no reuse opportunity, `write-design` and `write-plan` produce their existing structure
(`Satisfies:` lines, Files Create/Modify/Test, Interfaces, Depends-on, Steps, footers)
unchanged, and no new hard approval gate is introduced (REUSE-5.3). This is verified by a
baseline that walks a no-reuse feature through both skills and confirms byte-identical
structure plus an empty/`none` `Reuse:` line, not a block.

## Seams for testing

Per the repo's verification approach (baseline scenarios, no test runner), each "seam" is
the skill invocation exercising the requirement; evidence is a documented baseline
scenario tagged with its IDs. No new automated test seam is added.

| Seam | Kind | Covers |
|---|---|---|
| `write-design` Step 2 ladder sub-gate (rungs, scan-fed, carve-outs, chain) | baseline | REUSE-1.1, 1.2, 1.3, 5.1, 5.2 |
| `write-design` `Reuse:` line + rung-7 justification + new-dep callout (advisory) | baseline | REUSE-2.1, 2.2, 2.3, 2.4 |
| `write-design` Step 4 reuse-coverage self-check | baseline | REUSE-4.1 |
| `write-plan` task Files `Reuse:` line + design↔task consistency | baseline | REUSE-3.1, 3.2 |
| `write-plan` Step 4 reuse-miss + consistency findings | baseline | REUSE-4.2, 4.3 |
| no-reuse feature → both skills' structure unchanged, no new gate | baseline | REUSE-5.3 |

## Coverage check

Every REUSE ID appears in exactly one Satisfies line:

- Story 1: 1.1, 1.2, 1.3 (§1)
- Story 2: 2.1, 2.2, 2.3, 2.4 (§2)
- Story 3: 3.1, 3.2 (§4)
- Story 4: 4.1 (§3) · 4.2, 4.3 (§5)
- Story 5: 5.1, 5.2 (§1) · 5.3 (§6)

All 15 criteria mapped; none deliberately unmapped.
