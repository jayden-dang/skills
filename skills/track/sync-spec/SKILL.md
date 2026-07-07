---
name: sync-spec
description: Use when a feature's spec and its reality have diverged — requirements changed mid-implementation, the implementation deviated from the plan with approval, the feature just shipped, or check-trace is failing in CI — and the requirements/design/tasks triad needs realigning.
---

# Sync a Spec

Realign one feature's spec triad (`docs/specs/<date>-<feature>/{requirements,design,tasks}.md`) with what is actually true — in the code, the tests, and the tasks. Specs that are not resynced after change become fiction, and fiction is worse than no spec.

Work one feature at a time. Identify the spec directory first (from the user, the current branch, or `docs/specs/INDEX.md`).

## Iron rules

- **Never renumber requirement IDs.** IDs are immutable once approved; everything downstream cites them.
- **Never delete a requirement.** Retire it: `~~**CODE-N.M**~~ <reason>` — struck-through IDs stop counting as defined, but the history stays legible.
- New requirements get the next free number under their story; new tasks match the existing task format exactly.

## Steps

**a. Baseline.** Run `check-trace.mjs` (path per `docs/agents/project.md`) and capture the output — this is the "before" picture.

**b. Requirements ↔ tasks.** Compare `requirements.md` against `tasks.md`:

- A live requirement no task cites → append a covering task in the same format as the rest of the file, ending with its `_Requirements: CODE-N.M_` footer.
- Work that is verifiably complete (implemented and its verify evidence exists) but whose task box is unchecked → check the box.

**c. Requirements ↔ design.** Compare requirement IDs against the `Satisfies:` lines in `design.md`. Any live requirement appearing in no `Satisfies:` line gets flagged to the user — either the design needs a section (extend it) or the requirement is aspirational (consider retiring it). Do not invent design content silently.

**d. Orphans.** List every task footer and test annotation citing an ID that is struck through or does not exist. Present the list to the user with a suggested disposition per item (repoint to a live ID, retire the test, or resurrect the requirement) — orphans are decisions, not cleanup.

**e. Status transitions — with evidence only.**

| Transition | Required evidence |
|---|---|
| Draft → Approved | the user explicitly approved the spec — never inferred |
| Approved → Implemented | every task box checked AND check-trace shows every live requirement covered by a test |
| Implemented → Shipped | the feature went out in a release (this step is normally invoked by `release`) |

Apply any transition whose evidence exists: update the `Status:` line in `requirements.md` and the feature's row in `docs/specs/INDEX.md`. If evidence is partial, say exactly what is missing instead of transitioning.

**f. After picture.** Re-run `check-trace.mjs` and print both reports side by side — errors and warnings resolved, anything remaining, and what you changed to get there.

**Done when:** the after-report is no worse than the before-report on errors, every flagged item has either an edit or an explicit user decision pending, and INDEX.md agrees with every spec's `Status:` line.
