# `trace`

> The vertical traceability check. It answers one question with evidence: does every requirement ID agree across where it is defined, cited, and tested?

|  |  |
|---|---|
| **Bucket** | execution |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | requirements/`fixes.md` definitions under `docs/specs/`, `tasks.md` citations, and the ID strings in the repo's test files; `docs/agents/project.md` for the specs dir, test globs, and ignore list |
| **Writes** | nothing — it gathers evidence with `grep`/`git` and reports a finding set; it produces no files and installs nothing |
| **Calls** | nothing — it is a leaf check |
| **Called by** | [`verify`](verify.md) and [`release`](release.md) (to prove "requirements met"), [`sync-spec`](sync-spec.md) (its before/after picture), and [`write-plan`](write-plan.md) (the coverage check) |

## What it is

`trace` is the deterministic traceability pass. Every input is gathered with `grep` and reads, and every finding follows a fixed rule, so it is **not a judgment call**: two agents running it on the same repo reach the same finding set.

It installs nothing. There is no script to install, no tool to wire, no linter binary — the check is a handful of `grep`/`git` passes over the repo tree plus a small set of rules applied to what they return. A caller that needs it simply runs the passes.

The passes gather four sets:

- **defined** — every bold `**CODE-N.M**` in a `requirements.md` or `fixes.md`, minus any inside a `~~ … ~~` strikethrough (a struck-through ID is retired, not defined), each carrying its file's `Status:`.
- **taskCited** — every ID on a `_Requirements:` line in a `tasks.md`.
- **testCovered** — every ID string that appears anywhere in a test file.
- **statuses** — the `Status:` and `Feature code:` line of each requirements file.

## When it fires

`trace` runs whenever requirements, tasks, and tests may have drifted out of agreement, and it is the traceability engine four other skills lean on:

- [`verify`](verify.md) and [`release`](release.md) run it to prove the "requirements met" claim — any error is a failing gate.
- [`sync-spec`](sync-spec.md) runs it before and after a realignment, printing both reports side by side so the drift closing is auditable.
- [`write-plan`](write-plan.md)'s coverage check runs it to confirm every Approved requirement is cited by a task before the plan ships.

When a caller needs a pass/fail, the gate is simple: **zero errors**.

## The finding set

Each finding is an ERROR or a WARNING. Errors mean the trace is broken; warnings mean it is incomplete but not wrong. `verify` and `release` treat any error as fatal and warnings as reported-not-fatal unless the caller says otherwise.

| Code | Tier | Condition |
|---|---|---|
| **E1** | error | A task or test cites an ID that no requirements file defines |
| **E2** | error | An `Implemented` or `Shipped` requirement has no covering test |
| **E3** | error | The same ID is bold-defined in more than one file |
| **W1** | warn | An `Approved` requirement is cited by no task |
| **W2** | warn | A `requirements.md` is missing its `Status:` or `Feature code:` line |

A task citation never satisfies E2 — only a test does. `fixes.md` is exempt from W2. Two bold occurrences of an ID in the *same* file are not an E3 duplicate.

What each status owes:

| Status | Needs a test (E2) | Needs a task (W1) |
|---|---|---|
| Draft | no | no |
| Approved | no | **yes** |
| Implemented / Shipped | **yes** | no |

## Coverage is textual presence

The load-bearing invariant: **an ID is covered when its string appears in a test file. Full stop.**

`trace` does not read the test to decide whether it "really" exercises the requirement, whether the assertion is meaningful, or whether a commented-out line should count. That judgment is deliberately out of scope, because adding it makes the result depend on the reader — and reader-independence is the one thing this check exists to provide. An ID present in a test file counts; the check never grades the test behind it.

The only sanctioned exclusion is an **ignore list** in `docs/agents/project.md`: a fixture or test-support file that carries IDs as data can be named there and dropped from the test search wholesale — never ID-by-ID by hand. And the passes must gather *every* matching file: missing one test file invents a false E2, missing one requirements file invents a false E1, so the grep covers the whole tree rather than a sample.

## Output

The check prints the counts, then the findings — for example:

```
trace: 24 requirements · 24 task-cited · 22 tested · 18 test files
  ERROR E1 test cites unknown requirement SHELL-9.9 (src/shell.test.ts)
  ERROR E2 SHELL-1.4 (…/requirements.md, Implemented) has no covering test
  warn  W1 NOTES-2.1 (…/requirements.md, Approved) is not cited by any task
```

Exact wording and ordering are not contractual — the **finding set** is. If `docs/specs/` does not exist, there is nothing to check and the pass stops there.

## Why it is written the way it is

`trace` exists so that "requirements met" can be a fact rather than an opinion. Every rule here defends determinism: the passes are pure `grep`/`git` so there is nothing to install or drift; coverage is textual so no two runs disagree; the ignore list is the single sanctioned exclusion so exclusions can't be smuggled in by hand. The temptation the check guards against is the reviewer who reads a test, decides it "basically covers" a requirement, and marks it green from judgment — which is exactly the subjectivity that lets an untested requirement ship as Implemented. By refusing to judge the test and only checking that the ID is present, `trace` stays cheap, repeatable, and impossible to argue with.

## See also

- [Traceability](../concepts/traceability.md) — the invariant this check enforces
- [Requirement IDs](../concepts/requirement-ids.md) — why the ID, not the prose, is the unit of reference
- [`verify`](verify.md) — runs `trace` to prove "requirements met"
- [`sync-spec`](sync-spec.md) — drives the finding set back to clean when it drifts
- [`write-plan`](write-plan.md) — its coverage check runs `trace` before the plan ships
