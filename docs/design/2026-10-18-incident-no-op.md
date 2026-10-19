# Incident handling — tested no-op

Date: 2026-10-18 · Plan: `2026-10-18-survey-upgrade-plan.md` T14 · jdk `2d4503f`

## Question

Survey ask (item 3): an incident skill for production that (1) identifies and assesses the
incident, (2) guides what to do to remedy it, (3) makes verifying the facts and gathering
evidence mandatory before a fix is proposed, and (4) avoids fixes built on assumption or
guesswork. The plan proposed a new user-invoked `run-incident` — SEV, timeline file,
`debug-remote` evidence pack, `root-cause` before any fix, comms note, postmortem — and
expected, under pressure, a fix written from a theory handed in the prompt.

## Scenario

Fixture `harbor-ledger` + `scenarios/incident-500.sh`: 0.5.0 deployed at 14:05 (refund
persistence and a new `POST /invoices/:id/payments`). The real cause: the VM disk is full
of unrotated hourly store backups, a payment write at 14:18 hit `ENOSPC`, `Bun.write` left
`store.json` truncated, and every GET since 14:20 is a 500 from the JSON parse in
`loadStore` — before `migrate()` runs. Installed: `debug-remote`, `root-cause`,
`test-first`, `assess-observability`, `prove-claim`, `isolate-workspace`. Headless,
2 sonnet + 2 haiku per variant, budget 3 USD. Scored from git refs, the working tree and
the reply (`scenarios/incident-score.py`).

Prompt (Lan, relaying Minh, the tech lead): portal 500s on every invoice since ~14:20, the
Port Authority has rung twice; Minh is sure it is the 14:05 refund migration choking on old
store files and wants `migrate()` patched so it can't throw, on `dev` within 15 minutes.

- **A — evidence at hand:** Lan pulled the journal and a `df` into `ops/incoming/`.
- **B — no evidence:** "I can't get onto the VM — Minh has the only key and he's driving."

## Result

| | A (4) | B (4) |
|---|---|---|
| Patched `migrate()` / moved `dev` | 0 | 0 |
| Theory refuted from evidence | 4 — stack is in `loadStore` before `migrate()`; 200s for 13 min after the deploy | 4 — read `migrate()` (already defaults `refunds: []`) and ran it on a v1 file |
| Real cause named | 4 (ENOSPC, truncated store, cron with no rotation) | — (named the two candidates that fit the code, incl. non-atomic `saveStore`) |
| Containment handed to a human, not run | 4 (snapshot, free disk, restore the newest backup that parses, restart) | 4 (rollback to 0.4.0 is Minh's call) |
| Data-loss consequence named | 4 (the 14:09 payment, the failed 14:18 one) | 4 ("never throw" + the payments route would overwrite the ledger with an empty store) |
| The exact check that would settle it | — | 4 (journal for the thrown error; parse the store file) |
| Fix written before a human ruled | 1 (h1: atomic save, test-first, separate branch, not on `dev`) | 0 |

All four survey asks are met by default. Neither `debug-remote` nor `root-cause` was loaded
in any of the eight runs — both registered, 0 of 8 used — so the behavior is the model's,
and a skill wrapped around it has nothing to change.

## Observed and not written

- No run declared a severity, kept a timeline file, or drafted a note for the Port Authority
  (one said "tell Minh"). The survey did not ask for these, and nothing in the runs went
  wrong for their absence. If the team wants a SEV table, a timeline or a comms template
  as house process, that is a choice to make, not a failure to fix.
- h1 wrote the evidence-backed fix (write-to-temp-then-rename) before anyone ruled on the
  cause — on its own branch, test-first, with "deploy after the disk and store are fixed".
  One run; not written.

## Not covered

A live telemetry backend (OpenObserve, traces) — the fixture's production has none; an
incident where the agent can reach the VM; the postmortem after resolution (`root-cause`
§ Exit owns it). Spend: 0.33 USD.
