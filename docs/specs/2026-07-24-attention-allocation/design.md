# Design: Attention Allocation (`allocate-attention`)

Feature code: ATTN
Status: Approved
Date: 2026-07-24
Requirements: ./requirements.md

## Context

The skill set already owns three of the four outer-loop jobs Osmani names.
`verify` and `trace` hold the audit loop; `finish-branch` and `record-decision`
hold the ownership loop; `comprehend-change` cures cognitive debt after the fact.
Nothing holds the **sampling loop** — deciding what gets human eyes when the
agent has produced more than one person can read. ATTN is that piece, and only
that piece.

The shaping constraint is that this must be a *thin* skill. Every mechanism it
needs already exists somewhere in the repo, and the reuse ladder lands on rung 2
for almost all of it. `scripts/lint-handoffs.py` already fails any skill body
that invokes a `disable-model-invocation` target, which mechanically enforces
ATTN-1.2, ATTN-9.4, ATTN-10.4, and ATTN-12.7 across the whole tree with zero new
code — the skill only has to carry the flag. `scripts/lint-skill-frontmatter.py`
and `tests/test_plugin_manifest.py` cover packaging. The base-branch resolution
in ATTN-2.3 is the same two-pass cascade already written in
`skills/ship/finish-branch/SKILL.md:41` and
`skills/review/comprehend-change/SKILL.md:124-126`. The in-tree output hard-fail
in ATTN-8.3 is XDIFF's rule. What is genuinely new is small: a partition rule, a
binding table, a floor selector, and a presenter.

The second constraint is ARCH-1. Sample membership is a *vertical check* in the
same family as `trace`, so the binding decision must be exact `git`/`grep` passes
with fixed extraction rules — never a model verdict about whether a change
"looks risky". This is also what makes ATTN-3.6 (same range, same hits)
achievable at all. Model judgment survives only in the add-only lane of
ATTN-4.1, where it can widen the human's view but never narrow it.

The third is ARCH-2 and ARCH-3. Risk globs differ per repo, so they come from an
optional `## Attention signals` section in `docs/agents/project.md` with a
built-in default set, and the skill runs unchanged when that section is absent.
Nothing is installed into an adopting repo and no headless gate exists.

## Decisions

1. **Sampling unit = path prefix at depth 2, not file and not commit.** Per-file
   units make a 200-file range unreadable and defeat ATTN-7.4; per-commit units
   cannot satisfy ATTN-3.1, because a file touched by three commits would sit in
   three units. Depth-2 path prefixes partition cleanly and stay human-meaningful
   (`skills/execution`, `docs/specs`, `tests`).
2. **Binding is a fixed pass; the model may only add.** Five mechanical signals
   admit units with no cap (ATTN-3.3, ATTN-3.4). Model judgment enters solely
   through ATTN-4.1's add-only lane. This is the same monotone shape
   `record-decision` uses for depth ("agent only raises depth, never lowers it",
   `skills/ship/record-decision/SKILL.md:74`).
3. **ATTN-4.3 is enforced by two greppable tests, not by a cap.** An
   agent-admitted reason must be unique after normalization *and* must name a
   concrete path present in that unit's diff. A cap on agent adds was considered
   and **rejected**: it would contradict ATTN-4.1's `SHALL admit`, and the
   requirement is already approved. Distinctness plus concreteness bounds spam
   without needing the contradiction.
4. **Size is a score signal, never a binding one.** Line-count thresholds are
   arbitrary across repos and would fire constantly; size earns its keep only in
   the floor selector (ATTN-5.1) where a total order is needed and no risk claim
   is being made.
5. **Risk globs are repo-configurable with a built-in default.** Optional
   `## Attention signals` in `docs/agents/project.md`; absent → defaults, no
   warning, no failure (ARCH-2).
6. **The unit is the sampling grain; the firing file is the pointer.** A unit is
   admitted because specific files in it matched. The presenter names those
   files, so grouping never buries the landmine that caused the admission.
7. **Two-step output cascade, not XDIFF's five.** ATTN writes nothing by default
   (ATTN-8.1), so an elaborate directory cascade has almost no surface to serve:
   explicit user path, else `$TMPDIR`/`/tmp`. In-tree paths hard-fail with no
   fallthrough, matching XDIFF.
8. **One reference sibling, not four.** The binding table and floor table are
   read on every run and stay inline; the default risk-glob set and the
   `project.md` config grammar are bulk data and move to
   `references/signals.md`.

No ADR is warranted. Every decision above is either reversible (glob sets,
thresholds), or already governed by an existing invariant (ARCH-1, ARCH-2,
ARCH-5), or recorded in requirements Out of Scope. Nothing here contradicts the
architecture spine.

## Architecture

### 1. Skill package and invocation posture

Satisfies: ATTN-1.1, ATTN-1.2, ATTN-1.5, ATTN-12.7
Respects: ARCH-5
Reuse: existing — `scripts/lint-handoffs.py`, `scripts/lint-skill-frontmatter.py`, `.claude-plugin/plugin.json` (rung 2)

New skill at `skills/review/allocate-attention/` with `SKILL.md` and one sibling
`references/signals.md`. Frontmatter carries `name: allocate-attention` and
`disable-model-invocation: true`; the description leads with trigger plus the
outcome noun ("an attention allocation over a range — a bounded sample set and
its explicit residue") and packs the literal phrasings from ATTN's discovery:
*what should I review first*, *I can't review all of this*, *spot check this PR*,
*too much to review*, *sample*, *attention*, *residue*.

The invocation rules need no new enforcement. `lint-handoffs.py` already builds
the set of `disable-model-invocation` skill names and fails any body matching
`REQUIRED SUB-SKILL: use \`x\``, `invoke \`x\``, `hand … to \`x\``, or
`use \`x\`` without the trailing `— user-invoked` escape hatch. Adding the flag
puts `allocate-attention` into that set automatically, so ATTN-1.2 and ATTN-12.7
are enforced repo-wide from the moment the skill lands. ATTN-9.4's prohibition on
`REQUIRED SUB-SKILL` reaching it is the same check.

ATTN-1.5 is a body rule: the skill states that a range without an allocation is
simply a range without an allocation, and carries no adverse claim.

### 2. Range resolver

Satisfies: ATTN-2.1, ATTN-2.2, ATTN-2.3, ATTN-2.4, ATTN-2.5, ATTN-2.6, ATTN-2.7
Reuse: existing — base-branch cascade from `finish-branch/SKILL.md:41` and `comprehend-change/SKILL.md:124-126` (rung 2)

Deliberately thinner than XDIFF's four-branch tree, because ATTN's trigger is a
finished PR-shaped unit.

```
explicit range given?            -> use it verbatim, skip the cascade      (2.1)
else BASE = default_base(),  RANGE = merge-base(BASE, HEAD)..HEAD          (2.2)

default_base():
  1. git symbolic-ref --quiet --short refs/remotes/origin/HEAD  -> strip "origin/"
  2. else first of main, master that `git rev-parse --verify` accepts
  3. else HARD-FAIL: ask for an explicit base                              (2.3, 2.4)

git rev-list --count RANGE == 0   -> HARD-FAIL naming the empty range      (2.6)
working tree dirty                -> one notice, continue on committed range (2.7)
```

Dirtiness is `git diff --quiet HEAD` non-zero OR non-empty
`git ls-files --others --exclude-standard`. Every command is local; no `gh`, no
fetch, no remote ref resolution beyond reading `refs/remotes/origin/HEAD` from
local state (ATTN-2.5).

### 3. Sampling-unit partition

Satisfies: ATTN-3.1
Reuse: none — new code (rung 7); no existing helper groups a diff's paths, and the rule is three lines of shell

Unit key for a repo-relative path:

| Path shape | Unit key | Example |
|---|---|---|
| ≥2 segments | first two segments | `skills/execution/tdd/SKILL.md` → `skills/execution` |
| 1 segment | the segment | `README.md` → `README.md` |
| — | — | `docs/specs/2026-07-24-attn/design.md` → `docs/specs` |

Derived once from `git diff --name-only RANGE`. Every changed file maps to
exactly one key by construction, which is ATTN-3.1. Depth 2 is the choice: depth
1 collapses an entire `skills/` tree into one unit; depth 3+ fragments back
toward per-file. A repo may override depth via `references/signals.md`'s config
grammar; the default is 2.

### 4. Binding pass

Satisfies: ATTN-3.2, ATTN-3.3, ATTN-3.4, ATTN-3.5, ATTN-3.6, ATTN-11.2, ATTN-11.3
Respects: ARCH-1, ARCH-2
Reuse: standard tooling — `git diff` plumbing and `grep` (rung 3)

Five signals. A unit is admitted if **any** fires. No cap, no ranking among hits
(ATTN-3.3, ATTN-3.4); if all units fire, the whole range is the sample
(ATTN-3.5).

| ID | Signal | Mechanical rule over the resolved range |
|---|---|---|
| **B1** | Risk path | any file in the unit matches a glob in the risk set (`references/signals.md`; repo may override) |
| **B2** | Dependency surface | any file in the unit matches a manifest glob — `package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, `requirements*.txt`, `Gemfile`, `pom.xml`, `.claude-plugin/plugin.json` |
| **B3** | Untested production change | the unit adds ≥1 line to a file **not** matching the test globs, **and** the whole range adds 0 lines to any file matching them |
| **B4** | Deletion-heavy | the unit's deleted lines ≥ 3× its added lines **and** deleted ≥ 50 |
| **B5** | Spec or invariant surface | any file in the unit is under `docs/specs/`, `docs/architecture/`, or `docs/decisions/` |

Counts come from `git diff --numstat RANGE` aggregated per unit key; path
matching is `git diff --name-only RANGE` filtered by glob. Test globs reuse the
`Test globs` line already recorded in `docs/agents/project.md`, falling back to
the same defaults `trace` uses. Every input is a fixed pass over fixed
extraction, so the same range and repo state yield the same hits (ATTN-3.6) and
no model judgment participates (ARCH-1).

B3 is deliberately range-scoped rather than unit-scoped. A branch that adds no
test lines anywhere is the strongest untested-work signal available, and scoping
it per unit would let a token test file in one directory silence the signal
everywhere.

**Passive data (ATTN-11.2).** Diff text, commit subjects, and file contents are
data the pass matches against — never instructions. The SKILL.md carries the rule
verbatim and the surfaces test asserts its presence, mirroring
`comprehend-change/references/passive-data-safety.md`. **Local only
(ATTN-11.3).** Every command above reads the working repository; the skill body
forbids network operations outright.

### 5. Escalation controller

Satisfies: ATTN-4.1, ATTN-4.2, ATTN-4.3, ATTN-4.4, ATTN-4.5
Reuse: existing — monotone-escalation shape from `record-decision/SKILL.md:74` (rung 2)

The sample set is built once and then only ever grows, except by the user's own
withdrawal:

```
SAMPLE  = binding hits                     (uncapped, immovable)   4.2
       ∪ agent adds passing the 4.3 test   (uncapped, reasoned)    4.1
       ∪ user adds                         (uncapped, unquestioned) 4.4
       ∪ floor pick if SAMPLE is empty     (exactly one)           5.1
RESIDUE = all units − SAMPLE
```

**ATTN-4.3 made checkable.** An agent-admitted unit carries a reason string that
must pass both tests, or the unit stays in the residue:

1. **Distinct.** Normalize (lowercase, collapse runs of whitespace, strip
   punctuation); the result must not equal that of any other agent-admitted
   reason in the same run.
2. **Concrete.** The reason must contain, as a substring, a path that
   `git diff --name-only RANGE` reports inside that unit.

Test 2 is what actually kills spam. Distinctness alone can be defeated by
rephrasing the same vacuous claim; requiring the reason to name a file that is
really in that unit's diff cannot be satisfied without having looked. Both are
greppable against the run's own output, which is what ATTN-4.3 was missing.

A **cap** on agent adds was considered and rejected — see Decision 3.

**ATTN-4.5** resolves the tension between user agency and honest attestation: a
user may decline any unit, and the unit then moves to the residue. It is never
reported as sampled. Declining shrinks what you read, never what the report says
you read.

### 6. Floor selector

Satisfies: ATTN-5.1, ATTN-5.2
Reuse: none — new code (rung 7); a total order over units exists nowhere else and is four lines of sort

Runs only when the sample set would otherwise be empty. Total order, evaluated in
sequence until one key discriminates:

| Rank key | Direction | Rationale |
|---|---|---|
| 1. changed lines (added + deleted) | descending | most surface for a reader to misjudge |
| 2. files changed | descending | breadth over depth at equal volume |
| 3. unit key | ascending, byte order | a deterministic final tiebreak, never random |

Top-1 is admitted. Key 3 guarantees a total order, so ATTN-5.2 holds for any
non-empty range and ATTN-3.6's determinism extends to the floor path.

### 7. Allocation presenter

Satisfies: ATTN-6.1, ATTN-6.2, ATTN-6.3, ATTN-6.4, ATTN-7.1, ATTN-7.2, ATTN-7.3, ATTN-7.4, ATTN-11.4
Reuse: none — new code (rung 7); no existing skill emits a sample/residue pair

One presentation per run, covering the whole range (ATTN-7.4) — never one per
unit. Fixed shape:

```
Attention allocation — <RANGE>
<U> units · <F> files · <L> changed lines
[uncommitted work is not included in this allocation]        (2.7, if dirty)

SAMPLE — <k> of <U> units
  <unit key>   admitted by B<n> (<firing file>, …)  |  agent add: <reason>
    Claim:     <what this unit's agent verdicts assert>          6.1
    Refuted by: <test / command / file:line to run or read>      6.2
    Disposition: <user's own words>  |  undispositioned          6.3, 6.4

RESIDUE — <U−k> of <U> units, agent verdicts only                7.1, 7.2
  <unit key>  <files> files  <lines> lines
  …

Nothing above says the residue is correct.
```

**ATTN-6.1/6.2.** Every sampled unit pairs its claim with the concrete
observation that would refute it. The refuter must name a runnable or readable
artifact — a test id, a command, a `file:line` — never a paraphrase. This is the
one place ATTN borrows from the rejected falsification-stop primitive: as framing
on a ranked sample, not as an unranked stop-the-world.

**ATTN-6.3/6.4.** Silence is never consent. A unit with no stated disposition
prints `undispositioned`. A stated disposition is recorded in the user's own
words — the same verbatim discipline `record-decision` applies to judgment
elements, for the same reason: an agent paraphrase of a human judgment is not a
human judgment.

**ATTN-7.3.** The words *reviewed*, *cleared*, *approved*, and *safe* are barred
from residue prose. The surfaces test greps the SKILL.md for the prohibition; the
scenario file carries the pressure case.

**ATTN-11.4.** Any step that cannot complete reports the failure and emits no
partial allocation — the same fail-closed shape as XDIFF's Iron Law. A range that
resolves but whose binding pass errors yields an honest stop, not a sample set
built from whatever succeeded.

### 8. Output packaging

Satisfies: ATTN-8.1, ATTN-8.2, ATTN-8.3, ATTN-8.4
Reuse: existing — in-tree hard-fail rule from `comprehend-change/SKILL.md:175-177` (rung 2)

Default is conversational output and **no file written** (ATTN-8.1). On explicit
request only:

```
1. user-supplied path
2. else $TMPDIR, else /tmp
filename: YYYY-MM-DD-attention-<slug>.md      (slug from branch name, else short range)
```

If the resolved path is inside `git rev-parse --show-toplevel`, **hard-fail**
naming the path — no silent fallthrough to another location (ATTN-8.3), which is
XDIFF's rule and for the same reason: an aid that quietly writes into the repo
becomes an archive, then an expectation. Two steps suffice where XDIFF needs
five, because there is no default write path to cascade through.

ATTN-8.4 needs no mechanism: the allocation is a pure function of the git range
and repo state (ATTN-3.6), so re-running reproduces it. The skill body states
this as the recovery path instead of offering an archive.

### 9. Neighbour touchpoint

Satisfies: ATTN-9.1, ATTN-9.2, ATTN-9.3, ATTN-9.4, ATTN-10.5
Respects: ARCH-5
Reuse: existing — extends `execute-plan/SKILL.md:96-97` "After the Last Task" (rung 2)

Exactly one line is added to the skill set, in `execute-plan`'s After-the-Last-Task
sequence, between step 4 (Acceptance) and step 5 (Finish):

> Optional: `/allocate-attention` ranks a human sample over this branch. Not a
> gate — skip it freely.

It is prose naming a slash command, not a `REQUIRED SUB-SKILL` hand-off, so
`lint-handoffs.py` passes and ARCH-5 holds. Placement after `acceptance-check`
means `polish`'s commits are already in the range (ATTN-9.1). ATTN-9.4 is
satisfied by the line being an aside — `execute-plan`'s numbered steps are
unchanged, which is also what keeps ATTN-12.1's guard true.

**ATTN-9.3 and ATTN-10.5.** No mention is added to `finish-branch`,
`code-review`, `release`, or `record-decision`. When a user promotes an
allocation summary into a decision record, it travels as session context they or
the agent already hold — `record-decision`'s existing `Promoted-Evidence:`
mechanism accepts inline agent-authored text, so nothing in its body changes.

### 10. Boundaries and no-op behaviour

Satisfies: ATTN-1.3, ATTN-1.4, ATTN-10.1, ATTN-10.2, ATTN-10.3, ATTN-10.4, ATTN-12.1, ATTN-12.2, ATTN-12.3, ATTN-12.4, ATTN-12.5, ATTN-12.6
Respects: ARCH-2, ARCH-3, ARCH-6
Reuse: existing — participant-boundary and no-op posture already stated in `AGENTS.md` §3 and ARCH-6 (rung 2)

Everything in this section is guaranteed by *absence*: ATTN adds no gate, no
emitter, and no required artifact, so the guarded behaviours continue by
construction. The design's obligation is to keep it that way, and the surfaces
test is where that is held.

| Guarded | Held by |
|---|---|
| ATTN-1.3, ATTN-12.1, ATTN-12.2 | §9 adds one aside; no numbered step is inserted, reordered, or gated |
| ATTN-1.4 | no attestation exists without a run; there is nothing to infer from |
| ATTN-12.3 | ATTN never touches task review; band packaging is not read by this skill at all |
| ATTN-12.4, ATTN-12.5 | ATTN-9.3 forbids any edit to `finish-branch` |
| ATTN-12.6 | ATTN-10.4 names `/comprehend-change`; XDIFF's pipeline is untouched |
| ATTN-10.2 | no write under `docs/decisions/`; `record-decision`'s caller set stays `{finish-branch, release}` (`record-decision/SKILL.md:22`) |
| ATTN-10.1 | ARCH-6 — absence of an allocation on unmediated work is not a finding |
| ATTN-10.3 | inline promotion only; see §9 |

`docs/agents/project.md` without an `## Attention signals` section runs on
defaults with no warning (ARCH-2). No CI job, git hook, or `trace` pass is added
(ARCH-3) — `trace` gains no ATTN pass, because there is no required artifact to
check for.

### 11. Test surfaces (infrastructure)

Satisfies: none — infrastructure supporting every section above
Reuse: existing — extends the XDIFF test pattern, `tests/test_comprehend_change_surfaces.py` (rung 2)

Three artifacts, mirroring what DREC and XDIFF already established:

- `tests/attention-allocation/red-baselines.md` — recorded baseline failures and
  description trigger traps; **trace-ignored** (added to the `Trace ignore` line
  in `docs/agents/project.md`, as XDIFF's is).
- `tests/attention-allocation/scenarios.md` — greppable bare `ATTN-N.M` tokens
  per scenario, the acceptance-markdown convention already recorded in
  `docs/agents/project.md`.
- `tests/test_attn_surfaces.py` — `unittest`, requirement IDs in method names
  (`test_ATTN_1_1_…`), asserting the SKILL.md and reference files carry each
  mechanical rule.

## Seams for testing

Every seam already exists; ATTN adds one new file to an established pattern and
no new interface.

| Seam | Kind | Covers |
|---|---|---|
| `tests/test_attn_surfaces.py` — SKILL.md + `references/signals.md` text assertions | unit | ATTN-1.1, ATTN-1.5, ATTN-2.3, ATTN-2.4, ATTN-2.5, ATTN-2.6, ATTN-2.7, ATTN-3.1, ATTN-3.2, ATTN-3.3, ATTN-3.4, ATTN-3.5, ATTN-4.2, ATTN-4.3, ATTN-5.1, ATTN-5.2, ATTN-6.1, ATTN-6.2, ATTN-6.3, ATTN-7.1, ATTN-7.2, ATTN-7.3, ATTN-7.4, ATTN-8.1, ATTN-8.3, ATTN-8.4, ATTN-11.2, ATTN-11.3, ATTN-11.4 |
| `tests/test_plugin_manifest.py` — plugin skills array | unit | ATTN-1.1 |
| `scripts/lint-skill-frontmatter.py` | unit (lint) | ATTN-1.1 |
| `scripts/lint-handoffs.py` — dead-hand-off scan over the whole tree | unit (lint) | ATTN-1.2, ATTN-9.4, ATTN-10.4, ATTN-12.7 |
| `tests/test_attn_surfaces.py` — neighbour-file assertions on `execute-plan`, `finish-branch`, `code-review`, `release`, `record-decision` | unit | ATTN-1.3, ATTN-9.1, ATTN-9.2, ATTN-9.3, ATTN-10.2, ATTN-10.5, ATTN-12.1, ATTN-12.2, ATTN-12.3, ATTN-12.4, ATTN-12.5, ATTN-12.6 |
| `tests/attention-allocation/scenarios.md` — agent-run behavioural scenarios | acceptance (markdown) | ATTN-1.4, ATTN-2.1, ATTN-2.2, ATTN-3.6, ATTN-4.1, ATTN-4.4, ATTN-4.5, ATTN-6.4, ATTN-8.2, ATTN-10.1, ATTN-10.3 |

`tests/attention-allocation/red-baselines.md` is the RED record required by
`writing-skills`, not a coverage seam; it is trace-ignored for that reason.

## Coverage check

All 56 live criteria are mapped. Two IDs were **retired** by `sync-spec` on
2026-07-24 — `ATTN-11.1` (performance) and `ATTN-11.5` (accessibility) — because
a `None` quality attribute is a recorded non-applicability rather than a
requirement, and giving it an ID created a live requirement no test could cover.
Both attributes remain recorded in `requirements.md` in the house form (no ID),
matching DREC and XDIFF.

Every live ID appears in exactly one `Satisfies:` line. Guard criteria
ATTN-12.1 … ATTN-12.6 map to §10, which holds them by absence rather than by
mechanism; ATTN-12.7 maps to §1, where `lint-handoffs.py` enforces it directly.

**Reuse coverage.** Eleven sections: seven at rung 2 (existing artifact), one at
rung 3 (standard tooling), three at rung 7 with stated reasons — §3 (no existing
path-grouping helper), §6 (no existing total order over units), §7 (no existing
sample/residue presenter). No new third-party dependency is proposed, so no
adoption decision is owed.
