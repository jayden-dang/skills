# Story-unit mode — derivation and barriers

Load this file when `Execution-mode: story-unit`, or when Setup step 4
(review-unit preflight) runs in **either** mode. SKILL.md owns the iron laws;
this file owns the **recipe**.

## Leading words

| Token | Meaning |
|---|---|
| **review unit** | One non-NFR user story (or merge of stories), one PR into the feature branch, one human review |
| **risk glob** | Path match against allocate-attention B1 + project Risk globs (owned by finish-branch for naming, not here) |
| **Execution-mode** | `continuous` \| `story-unit` header on tasks.md |
| **straddle** | Task `_Requirements:` cites two+ non-NFR story numbers → merge those stories |

## Derive partition (deterministic)

Run against the feature's `requirements.md` and `tasks.md`.

1. **NFR set** — every `## N` section that contains the line `**Section-kind:** nfr`.
   - **absent = story** — section without that line is a behavioral story.
2. **Live IDs** — bold `**CODE-N.M**` not inside `~~…~~` strike spans.
3. **ID → story** — story number is `N` in `CODE-N.M` (same N as `## N`).
4. **Task → stories** — for each task, parse `_Requirements:` IDs; drop IDs whose
   story is in the NFR set for **merge** purposes.
5. **MERGE on straddle** — union-find: if a task's non-NFR story set has size ≥ 2,
   merge those stories. Report merge count and the straddling task numbers.
6. **Assign tasks** — each task joins the unit of its (merged) story set.
7. **NFR-only tasks** — after step 4 the non-NFR story set is empty:
   - join the unit of tasks listed in `Depends-on:`;
   - if `Depends-on: none` / absent → first unit (lowest story number among units);
   - if Depends-on spans multiple units → join the **latest prereq unit in topo
     order** + report line (never rewrite Depends-on to tidy units).
8. **Unit order** — edge U→V if any task in U has `Depends-on` naming a task in V.
   Topo-sort; tie-break **lowest story number**. Cycle → **hard fail** preflight.
9. **Hard fail preflight** — task with zero parseable IDs; task citing only struck
   IDs. **Empty non-NFR story** (no tasks) → omit unit + report (aligns with trace
   W1 — do not promote to hard fail).

## File count (preflight table)

For each unit, cardinality of path strings from that unit's tasks:

```text
lines matching:  ^- (Create|Modify|Test):\s*(\S+)
strip trailing :line-range from capture group 2
dedupe exact path string
directory path counts as one (do not expand trees)
exclude Consumes:/Produces: (Interfaces)
```

## Unit table (print both modes)

```text
unit <k>  stories {…}  "<title>"  <n> tasks  <m> files  merges: <count>
reports: <empty stories | NFR-only placement | straddlers | none>
```

## Per-unit barrier (story-unit only)

After every task in the unit is DONE and ledgered:

1. `UNIT_BASE` = base of first task in unit; `UNIT_HEAD=$(git rev-parse HEAD)`.
2. Package `.skills/review-unit-<k>-<base7>..<head7>.diff` same shape as task package.
3. Dispatch **task-reviewer** once at **unit scope** (two-verdict) over that range.
   Human is never first reviewer of the unit diff.
4. Fix loop until clean (same circuit breaker as tasks).
5. **STOP.** Present unit summary. Wait.
6. Unlock:
   - user continues after looking → next unit;
   - user says stop-stopping / just-run-it-all → write `Execution-mode: continuous`
     into tasks.md, then no further unit barriers. **Chat-only is not a mode change.**
7. Ledger: `Unit <k>: complete (tasks …, range <base>..<head>)`. Resume reads it.
8. Optional PR into feature branch — never the unlock.

## Whole-branch review

After the last unit, **After the Last Task** still runs whole-branch agent review.
Unit reviews (human) and whole-branch (agent) are not substitutes.
