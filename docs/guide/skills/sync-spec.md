# `sync-spec`

> The anti-spec-rot skill. Specs that are not resynced after change become fiction, and fiction is worse than no spec.

|  |  |
|---|---|
| **Bucket** | track |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | the feature's `requirements.md` / `design.md` / `tasks.md` triad, `docs/specs/INDEX.md`, `docs/agents/project.md` (the `check-trace` path), the code and tests |
| **Writes** | edits to the triad (retired/added requirements, task boxes, `Status:`), the feature's row in `docs/specs/INDEX.md`, a regenerated `GRAPH.md` staged into the same commit |
| **Calls** | [`check-trace`](../resources/scripts.md#check-trace) (before and after), `python3 scripts/check_graph.py --harvest` |
| **Called by** | [`finish-branch`](finish-branch.md), [`amend`](amend.md), [`release`](release.md); or the user when a spec has drifted or CI's trace check is red |

## When it fires

When a feature's spec has drifted from reality. Any of these is a trigger:

- Requirements changed mid-implementation.
- The implementation deviated from the approved plan.
- The feature just shipped and its `Status:` has not caught up.
- The specs have gone stale or out of sync.
- [`check-trace`](../resources/scripts.md#check-trace) is failing in CI.

In each case the requirements / design / tasks triad needs realigning back to what the code and tests actually do. Work **one feature at a time**. Identify the spec directory first — from the user, the current branch, or `docs/specs/INDEX.md`.

## Iron rules

These three rules protect the trace's history. Everything downstream cites requirement IDs, so IDs cannot move:

- **Never renumber requirement IDs.** They are immutable once approved.
- **Never delete a requirement.** Retire it: `~~**CODE-N.M**~~ <reason>`. A struck-through ID stops counting as defined, but the history stays legible.
- **New requirements get the next free number under their story**; new tasks match the existing task format exactly.

Together these mean the requirement set only ever grows or retires — it never shifts under the IDs that tests, commits, and the feature graph already cite.

## Steps

**a. Baseline.** Run `check_trace.py` (path per `docs/agents/project.md`) and capture the output — this is the "before" picture.

**b. Requirements ↔ tasks.** Compare `requirements.md` against `tasks.md`:

- A live requirement no task cites → append a covering task in the file's format, ending with its `_Requirements: CODE-N.M_` footer.
- Work verifiably complete (implemented, with verify evidence) but whose task box is unchecked → check the box.

**c. Requirements ↔ design.** Compare requirement IDs against the `Satisfies:` lines in `design.md`. Any live requirement in no `Satisfies:` line gets **flagged to the user** — either the design needs a section (extend it) or the requirement is aspirational (consider retiring it). **Do not invent design content silently.**

**d. Orphans.** List every task footer and test annotation citing an ID that is struck through or does not exist. Present the list with a suggested disposition per item — repoint to a live ID, retire the test, or resurrect the requirement. **Orphans are decisions, not cleanup**, so they go to the user rather than being auto-fixed.

**e. Status transitions — with evidence only.** Apply any transition whose evidence exists; if evidence is partial, say exactly what is missing instead of transitioning:

| Transition | Required evidence |
|---|---|
| Draft → Approved | the user explicitly approved the spec — **never inferred** |
| Approved → Implemented | every task box checked **AND** check-trace shows every live requirement covered by a test |
| Implemented → Shipped | the feature went out in a release (this step is normally invoked by [`release`](release.md)) |

A transition updates the `Status:` line in `requirements.md` and the feature's row in `docs/specs/INDEX.md`.

**f. After picture.** Re-run `check_trace.py` and print both reports side by side — errors and warnings resolved, anything remaining, and what you changed to get there.

Then regenerate the feature graph:

```bash
python3 scripts/check_graph.py --harvest
```

If `GRAPH.md` changed, stage it into this sync-spec commit alongside the `Status:` / `INDEX.md` edits, so the committed graph tracks the triad.

The steps have a rhythm: read the before-trace, reconcile each pair of the triad against each other and against the code, route every judgment call to the user, transition status only where evidence exists, then prove the result with the after-trace and a fresh graph.

**Done when** the after-report is no worse than the before-report on errors, every flagged item has either an edit or an explicit user decision pending, and `INDEX.md` agrees with every spec's `Status:` line.

## What the skill edits vs. what it asks

The steps split cleanly by whether the fix is mechanical or a judgment about intent:

| Handled directly | Routed to the user |
|---|---|
| Adding a covering task for a live requirement (step b) | A live requirement in no `Satisfies:` line (step c) — extend design or retire |
| Checking a box for verifiably complete work (step b) | Orphaned task footers and test annotations (step d) — repoint, retire, or resurrect |
| Applying a status transition whose evidence exists (step e) | A status transition whose evidence is only partial (step e) — say what is missing |
| Staging a changed `GRAPH.md` (step f) | — |

Design content and orphan dispositions are never silent: the skill proposes, the user decides.

## Worked example

A feature whose code is `SHELL` shipped last week, but during implementation the persisted-key requirement was dropped and a new one added, and CI's trace check is now red.

**a. Baseline.** `check-trace` reports two errors: `SHELL-1.3` is defined but no test tags it, and a test tagged `SHELL-1.9` cites an ID that does not exist in `requirements.md`.

**b. Requirements ↔ tasks.** `SHELL-1.3` turns out to have been superseded — the behavior it described was replaced. Following the iron rules it is **not deleted** but retired as `~~**SHELL-1.3**~~ superseded by SHELL-2.1 (async hydration)`. The replacement `SHELL-2.1` gets the next free number under its story and a covering task with a `_Requirements: SHELL-2.1_` footer; its task box is checked because the code and verify evidence exist.

**c. Requirements ↔ design.** `SHELL-2.1` appears in no `Satisfies:` line. The skill flags this to the user rather than writing design prose itself — the user extends the design's persistence section.

**d. Orphans.** The test tagged `SHELL-1.9` is an orphan (no such ID). The skill presents it with a suggested disposition: repoint the tag to the live `SHELL-2.1` it actually verifies. The user agrees.

**e. Status.** Every task box is now checked and the after-trace covers every live requirement, so `Approved → Implemented` has its evidence; `Implemented → Shipped` waits for [`release`](release.md). The `Status:` line and the `INDEX.md` row are updated to Implemented.

**f. After.** `check-trace` re-runs clean; both reports print side by side. `python3 scripts/check_graph.py --harvest` regenerates `GRAPH.md`, which changed, so it is staged into the same commit as the `Status:` and `INDEX.md` edits.

## Why it is written the way it is

`sync-spec` exists because a spec's value is entirely in being trusted, and one silent divergence between the spec and the code destroys that trust for the whole triad. So the skill is built to never lose or falsify history: IDs are immutable and requirements are struck through rather than deleted, which keeps the record legible while letting the live set shrink. The two things an agent is tempted to do quietly — invent missing design content and clean up orphaned annotations — are exactly the two the skill routes to the user, because both are decisions about intent, not mechanical fixups. Status transitions demand evidence rather than inference for the same reason: a status line that claims more than the tests prove is the precise fiction this skill was written to prevent. The before/after `check-trace` pair makes the whole operation auditable — you can see the drift close.

## See also

- [Traceability](../concepts/traceability.md) — the invariant `check-trace` enforces and this skill restores
- [Requirement IDs](../concepts/requirement-ids.md) — why IDs are immutable and retirement is struck-through
- [The feature graph](../concepts/feature-graph.md) — what `check-graph --harvest` regenerates in step f
- [`finish-branch`](finish-branch.md) — reminds the user to run `sync-spec` after a merge or PR
