# `evolve-system`

> One measured improvement at a time: read the delivery sensor, settle what earlier runs predicted, open at most one new improvement with a number it should move.

|  |  |
|---|---|
| **Bucket** | track |
| **Invocation** | user-invoked — run as `/evolve-system`, or `/evolve-system --unattended` when nobody will answer; no skill may auto-invoke it |
| **Reads** | `.skills/<CODE>/progress.md` and `close-receipt.md`, git history, the CI runs printed by `**Integration CI:**` (and `**Integration CI jobs:**`) in `docs/agents/project.md`, `.github/workflows/*`, `.skills/evolve/cycles.json`, `docs/agents/issue-tracker.md` |
| **Writes** | `.skills/evolve/signals.json`, `.skills/evolve/cycles.json`, and one ticket: a draft at `.skills/evolve/drafts/<key>.md`, or on the configured tracker when `docs/agents/issue-tracker.md` says `**Evolve filing:** tracker` |
| **Calls** | nothing; the improvement is built later through `/idea` → `/shape` → `/go`, or `/author-skills` |
| **Called by** | nothing — user-invoked |

## When to run it

Weekly, or from a scheduler or bot. It is cheap when nothing is wrong: the sensor is a standard-library
script, and a run with nothing flagged opens nothing.

## What it does

1. **Sense.** `scripts/sense.py` reads what the skill set already writes and prints fixed signals:
   - `ci:latest_red`: the integration branch is red right now;
   - `ci:runs_real`: CI jobs that ran zero steps, meaning no runner;
   - `ci:change_fail`: a landing (the receipt's head, else the ledger's last commit range) whose first real CI run was red, counting only landings on a green base;
   - `ci:landed_on_red`;
   - `evidence:receipt_coverage`;
   - `evidence:close_vs_ci_command`: the close ran a different test command than CI;
   - `arch:invariant_violations`: `violates ARCH-N` verdicts in review files;
   - `arch:blast_radius`: the share of commits that touch two or more code modules (the same module rule as `/scan-architecture`); it flags only a rise;
   - `arch:posture`: read from `/scan-architecture`'s `posture.json` when present; never flags;
   - repeated review lanes such as reader-left-behind.

   **Each rate is judged against the repo's own baseline**, the previous window of the same length
   (`previous`, `trend`). It flags only while events remain and the rate is not better than that
   baseline, or when there is no earlier history (fewer than 3 observations counts as none). A repo that is getting better goes quiet without a
   global threshold.
2. **Settle.** The same script moves earlier cycles from `open` to `awaiting` once a commit names their
   ticket, then to `kept`, `reverted` or `inconclusive` by a fixed rule per signal (how many landings, by
   when). The run comments each verdict on its ticket.
3. **Open at most one.** It opens nothing in three cases: a cycle is open (an undelivered one expires after
   30 days), nothing is flagged, or CI is not configured (it names the line to add). Otherwise it takes the
   first key of the sensor's fixed `pick_order` and records `baseline`, `change`, `predicted` and
   `settle` in `cycles.json`.
4. **File it.** One ticket in the tracker's Issue format, whose acceptance line is the prediction. It is a
   draft for you to file unless the repo opts in with `**Evolve filing:** tracker`.

To set a repo up, add to `docs/agents/project.md` (the jobs line is optional; it tells a run that never
started from a real failure):

```markdown
- **Integration CI:** `gh run list --workflow <name> --branch <integration branch> --limit 200 --json databaseId,conclusion,headSha,createdAt`
- **Integration CI jobs:** `gh run view {run_id} --json jobs`
```

## Running it from a bot or scheduler

The runner must be allowed to run `python3` on the sensor and to write under `.skills/evolve/`.
Under `grok -p` with `--always-approve` the run completed: one cycle, a draft, no commit.
With scoped allow rules that did not cover the sensor command, it stopped at step 1, because a
headless run cannot ask for approval.

## Why it is shaped this way

Twelve runs without the skill, on Sonnet and Haiku across four fixture repos:
- all twelve rewrote the repo's close command themselves;
- eleven left no number the change should move;
- none left a record a later run could check;
- every one opened several improvements at once;
- three of six unattended runs wrote to `dev` or tried to file on the forge. One said "It is small and safe to merge without anyone reviewing it first", then fast-forwarded it.

Re-checking an earlier improvement and stopping when everything is green both passed without the skill,
so the skill adds nothing there. Evidence: `skills/track/evolve-system/TESTS.md`.

## What a baseline cannot see

A rate that is bad but improving reads "better" and stays quiet. On klynt, change-fail at 5/10 is not
flagged because the previous window was 8/10. The loop measures direction, not level. A red branch is
caught anyway by `ci:latest_red`, which has no baseline.
