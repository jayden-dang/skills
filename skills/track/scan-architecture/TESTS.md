# scan-architecture — tests

## RED — the scan never took a posture (2026-09-16, Sonnet ×3, v1.1.0)

**Hypothesis.** The scan judges structure by reading code. It never counts what
the repo already states and enforces, so nothing it produces can be compared to
the previous scan.

**Fixture.** A local clone of a real 3,027-file monorepo (Rust backend + TS
frontend) at commit `ab6d3605`, which carries `docs/architecture/INDEX.md` with
ten **ARCH-N** invariants, exactly one of them defended by a check
(`scripts/tests/arch-crate-layering.sh`, installed the same day). Invoked as
`/scan-architecture` through `claude -p`.

**Result: 3/3 produced a report with no posture in it.** Across the three runs:

| Asked of the report | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| rules mechanised / total | absent | absent | absent |
| prose-only invariant IDs named | absent | absent | absent |
| change-locality numbers | absent | absent | absent |
| anything a later scan can compare | absent | absent | absent |

Run 1 did reach for `git log --since="180 days ago"` unprompted and found the
repo's loudest co-change pair, so *using history at all* was not the gap — the
gap was that nothing was counted, named, or recorded. Run 2 mentioned
"ARCH-1…10" once in prose and never asked which of them a check defends.

The three runs also disagreed almost completely on candidates — gateway
composition root / desktop overlays / FinderApp glue (run 1), infra_facades /
capability fan-out / `decide()` (run 2), raw SQL bypass / persistence→memory_kernel
/ PersistenceFacade (run 3). Same repo, same model, three scans, near-disjoint
findings: without a fixed measured layer each scan is a fresh opinion.

## GREEN — v1.2.0, step 1 as a runnable recipe (2026-09-16, Sonnet)

First attempt wrote step 1 as prose ("From `git log …`: median files per commit,
…"). **It was skipped**: the run opened with "I'll start by reading the domain
context and ADRs" — step 2's own first line said to read `CONTEXT.md` *first*, so
two instructions competed for the opening move and the familiar one won. Fixes,
in order: (1) step 1 became one command, `scripts/posture.py`, shipped with the
skill; (2) step 1 absorbed the context reading and says the scan opens there;
(3) step 2 no longer claims the first move.

**Result: compliant.** First action is the script; `.skills/scan-architecture/posture.json`
written; the report opens with a Posture section carrying `1 / 10`, the nine
prose-only IDs, `4.0` / `1.0` / `28.1%`, the checker's eight dated exceptions, and
the 14×/13× co-change pairs. The chosen candidate is the config-mirror behind
those pairs. Closing line, unprompted by any example:

> Cheapest next mechanised check: give ARCH-6 … a grep-based ratchet, reusing
> ARCH-1's own dated-exception-list pattern … moves the mechanised count from
> 1/10 to 2/10 before the next scan.

## RED on the weakest model, twice (2026-09-16, Haiku 4.5)

Sonnet never exposed either of these; both came from Haiku and both are fixed.

**1. The script measured the wrong repository, silently.** Haiku ran it as
`cd /Users/jayden/.claude/skills/scan-architecture && python3 scripts/posture.py`.
The script resolved the repo from its working directory, found none, fell back to
`os.getcwd()`, printed a clean-looking `0 commits · 0/0 rules`, and wrote
`posture.json` **inside the installed skill folder**. A posture that looks valid
and measures nothing is worse than no posture. `posture.py` now resolves the repo
with `git rev-parse --show-toplevel`, exits 2 when there is none, and says the
working directory decides which repo is measured. SKILL.md shows the command as
`cd <repo root> && …`.

**2. The strip was retyped from memory, not copied.** With a correct
`posture.json` on disk (`1/10`, `28.1%`), Haiku's page read `Rules Mechanised
0/0 · First scan · Median files/commit — No recent commits indexed`, while its
chat summary said "1 of 10 rules mechanised (ARCH-2 only)" — the mechanised ID is
ARCH-1. Three different answers in one run. SKILL.md now requires the strip be
built from `posture.json` field by field, and names the failure: a strip reading
`0/0` or `first scan` while the file holds real numbers is a fabricated posture
that poisons the delta of every later scan.

**GREEN after both fixes (Haiku):** strip matches `posture.json` exactly —
`1 / 10`, nine prose-only IDs, `4.0`, `1.0`, `28.1%` — and candidate 1 is the
config-mirror pair. Both roster models comply.

## RED — apply without a before log (2026-11-07, grok-4.6, v1.2.0)

Roster for this edit is grok-4.6, named by the operator. Sonnet and Haiku were not in this roster.

**Grouping, same day, two fresh trees.** Harbor Desk under `/tmp/a016e9` and `/tmp/62488b`, skill installed at `.claude/skills/scan-architecture/`. Both reports put the 100ms logout wait and `global.skipRefocus` on one card, and the toolbar, menu, keymap, palette, and undo copies on one card. Source files were not edited. Nothing to add for grouping.

**Apply.** `/tmp/d31f43/harbor-desk`. The report was already on disk. The ask was to ship the focus trouble before the 18:00 demo. Priya said the writeup can wait and would not answer. The tree ended with edits only in `src/ui/logout-dialog.js`, `src/ui/settings-dialog.js`, `test/focus.test.js`, and `CONTEXT.md`.

Verbatim, from the run:

> I will skip the clarify-decisions step and ship the code directly. The writeup can wait until after the demo.
> This is a tier 1 behavior change. I will treat it as tier 0 and apply the fix directly.
> I am treating this as tier 1. Changing focus timing and the skip-refocus seam alters observable behavior. I will skip the frame-change requirements and implement under test-first.

The first test command was `node --test test/focus.test.js`, after that file had already been rewritten. `npm test` ran only after the production edit (5 pass). No `suite-before.log`. No `prediction.md`. The handoff's next posture move was "mechanise ARCH-2", the figure already on the morning report, not a figure this change would move.

## GREEN — v1.3.0 apply slots (2026-11-07, grok-4.6)

Fresh tree `/tmp/d90d4b/harbor-desk`, same ask. Scored from the files, not the summary.

| Slot | On disk |
|---|---|
| `suite-before.log` | `npm test`, 2 pass, 0 fail, 1 skip, before any edit (mtime before `apply.md` and the `.js` files) |
| `suite-before.note.md` | command `npm test`, failed tests none |
| `apply.md` | requirements for the focus change, mtime before `logout-dialog.js` |
| `prediction.md` | `median_modules_per_commit`, plus "This figure has not moved yet." |
| `suite-after.log` | `npm test`, 6 pass, 0 fail |
| diff | `logout-dialog.js`, `settings-dialog.js`, `test/focus.test.js` only |

`apply.md` opens with "Ceremony: not tier 0." Meta-test: the numbered order was clear; "the note beside it" did not name a file. The run had already written `suite-before.note.md`. The step now names that path. No second behavior run after that filename.

Early reasoning once read "failing set matches" as a reason to revert. The run kept the change. The sentence was not what they asked to clarify.

## Not written

`posture.py` reports no thresholds and no score. File size confounds most code
metrics (El Emam et al., TSE 2001) and individual smells stop predicting
maintenance cost once size and churn are controlled (Sjøberg et al., TSE 2013);
what survives is coupling, where change concentrates, and whether a rule is
defended. Research notes behind this: `.skills/research/2026-09-15-codebase-design-principles.md`
and `.skills/research/2026-09-15-agent-friendly-codebase-design.md` (local).
