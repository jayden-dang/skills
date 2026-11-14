---
name: evolve-system
version: 1.2.1
description: Measures how reliably a repo's delivery loop holds, settles what earlier runs set out to improve, and opens at most one new improvement with a prediction. Run it with /evolve-system.
disable-model-invocation: true
---

# Evolve System

One run of a measured loop: read the sensor, settle earlier improvements against their own
predictions, and open **at most one** new improvement whose effect the next run can check.
The improvement is built later through the repo's normal chain (`/idea` → `/shape` → `/go`, or
`/author-skills` for this skill set). This run changes nothing else.

## The Iron Law

```
THIS RUN WRITES ONLY .skills/evolve/ AND ONE TICKET. IT NEVER APPLIES THE IMPROVEMENT.
```

Twelve of twelve runs without this skill rewrote the repo's close command in
`docs/agents/project.md` themselves, and eleven of them recorded no number the edit should move.
Nothing could later tell whether it worked, and the change skipped the test-first and review the
build chain gives every other change. A verify command, CI file, Makefile, source file, test or
agent config edited by this run is a failed run, however direct the evidence.

## 1. Sense

Run the sensor beside this file and read its output:

```bash
python3 -I <this dir>/scripts/sense.py --repo . --write --out .skills/evolve/signals.json
```

Exit `0` nothing new · `10` a new signal is flagged · `20` an earlier improvement was reverted ·
`2` the sensor could not run (report its stderr and stop). `--write` saves each earlier cycle's
new state to `.skills/evolve/cycles.json`; the script settles them, never you.

*Done when: `signals.json` exists and you have its `flagged`, `tracked`, `settled_now`, `cycles` and
`pick_order`.*

## 2. Report what settled

For each entry in `settled_now` (cycles this run moved to `kept`, `reverted`, `inconclusive` or
`expired`), add its `why` as a comment on its ticket (read the comment back; a `draft:` ticket gets
the line appended). Earlier verdicts are not repeated.

*Done when: every settled cycle's ticket carries its verdict.*

## 3. Open at most one

Open nothing when any of these holds; say which, with the report path, and stop:
- a cycle in `cycles` is `open` (one improvement at a time per repo; the sensor expires one that
  nothing delivered within 30 days);
- `pick_order` is empty;
- `pick_order` starts with `ci:configured`: tell the user to add these lines to
  `docs/agents/project.md` (the command prints JSON runs; the jobs line is optional):

  ```markdown
  - **Integration CI:** `gh run list --workflow <name> --branch <integration branch> --limit 1000 --json databaseId,conclusion,headSha,createdAt`
  - **Integration CI jobs:** `gh run view {run_id} --json jobs`
  ```

Whichever way the run ends, a flagged `ci:latest_red` or `ci:runs_real` (the integration branch is
red now, or CI is not running) is the first line of the run summary, even when an open cycle means
nothing new is opened.

Otherwise take the **first** key in `pick_order` (the sensor's fixed order). Every other key in it
goes in the run summary under "not this run". It is not filed: the next run sees it again.

Add the cycle to the `cycles` list inside `.skills/evolve/cycles.json` (the sensor created the file
as `{"schema_version": 1, "cycles": []}`; keep that shape). Every slot is required:

```json
{"schema_version": 1, "cycles": [
  {"key": "ci:change_fail", "rung": "ci", "state": "open", "opened_at": "<UTC now>",
   "baseline": "3/6 (LEDGER, REFUND, AUDIT)",
   "change": "<one sentence: the single change the build should make>",
   "predicted": "<key> goes from <baseline> to <target>",
   "settle": "<the key's settle.observations> landings after the change, within <settle.days> days",
   "ticket": "<tracker id or ticket file path, or draft:.skills/evolve/drafts/<key>.md>"}
]}
```

Re-run the same sensor command (with `--write`): the key must now appear in `tracked`, not `flagged`.

## 4. File the ticket

Write it in the **Issue format** of `docs/agents/issue-tracker.md` (the non-bug body), state role
`needs-triage`:

- **Problem** — the signal, its value and its events, from `signals.json`.
- **Outcome** — the `change`, in plain words.
- **Acceptance** — one checkbox: the `predicted` movement, observed as `settle` says.
- **Out of scope** — the other flagged keys ("not this run").

The build that delivers it names the ticket in its commit (the tracker's close linkage), or for a
local tracker edits the ticket file; that is how the next run's sensor moves the cycle from `open`
to `awaiting`. A `draft:` ticket waits until someone files it and writes the real ID into `ticket`.

- **`docs/agents/issue-tracker.md` has the line `**Evolve filing:** tracker`:** create it on the
  configured tracker, read it back, and put its ID in `ticket`.
- **Otherwise** (the default, in every mode, because a filed ticket is read by the repo's team):
  write it to `.skills/evolve/drafts/<key>.md` (`:` in the key becomes `-`), set `ticket` to
  `draft:<path>`, and name the draft in the run summary for the user to file.

Commit nothing, on any branch. With `--unattended`, nothing else differs: the run never asks.

*Done when: the ticket (or draft) exists and `cycles.json` names it.*

## Red Flags

- Editing a verify command, CI, Makefile, source, test or agent config "because it is one line"
- A second improvement opened in the same run, or the rest filed "while I'm here"
- A `predicted` without a number, or a `settle` without a count and a deadline
- Any commit or merge; a tracker ticket without `**Evolve filing:** tracker`

| Thought | Reality |
|---|---|
| "The evidence is direct, so I can apply this one fix" | Direct evidence is why it gets a ticket with a prediction. Applied here, it lands untested and unmeasured — eleven of twelve baseline runs did exactly that |
| "It is small and safe to merge without anyone reviewing it first" | A baseline run said this and fast-forwarded an unreviewed verify-command change into `dev` |
| "Filing all the findings saves a week" | Several at once makes the next run unable to say which change moved which number |
