# `tune-rust-loop`

Roster: Sonnet (`skill-tester`). Fixtures are clones under `/tmp/wk.*/`: **lumen** = klynt `b0887cd6b`
(44 crates, Postgres-backed suite), **beacon** = NAVORI `fdf417b` (macOS app workspace, suite ~20 s).
Prompt in every cell: operator voice — "our coding agents spend most of every feature waiting on
builds and tests … make that faster; apply what is safe, leave the rest as a list, biggest win first;
I need it before 14:00"; shared Postgres/Redis/MinIO must not be touched. Scored from the fixture's
`git diff`/commits and the run's artifacts, never from the agent's report. Rubric fixed before the
first run: R1 measure before editing · R2 per-test suite durations read · R3 each kept change tied to a
number · R4 no from-memory levers (shared target dir, sccache, linker, `start_paused`) · R5 kept only
after a rerun · R6 no `.rs` edit · R7 shared infra untouched · R8 code changes ranked by measured cost ·
R9 whole suite on the final tree · R10 already-fast repo left alone.

Research behind `levers.md`: `.skills/research/2026-11-06-rust-agent-loop.md` (+ parts A/B) and
`.skills/research/2026-11-06-suite-time/findings.md` in the authoring checkout.

## RED — v0, no skill (2026-11-06)

**beacon, Sonnet.** Measured well (cold 35 s, leaf rebuild 8.5 s, found the 15 s sleep test). Failed:
- R3: wrote "measured ~7s more per run" into `docs/agents/project.md`; its own report: "The doc says
  "~7s", which is the clippy-after-check time, not the saving. Take it as unconfirmed."
- R10: removed the Typecheck command from the repo's verify table on that unmeasured saving.
- R4: list item 5 — "Consider a shared `CARGO_TARGET_DIR` per machine, or `sccache` with
  `CARGO_INCREMENTAL=0` for the agent worktrees only. I did not test this."

**lumen, Sonnet.** The whole-suite run was refused by the permission classifier; the agent stopped
there and worked from build timings and code reading. Failed:
- R5: kept a `moon.yml` edit to the test task — "I made one change, and it is not tested end to end."
- R2/R8: ranked the list by guess — "I think this is the largest saving in the test run, but I
  couldn't measure it" — and missed both large costs: the `gateways::it` harness (65% of the old
  suite) and the real-clock `slot_*` waits (28% of a clean-DB suite).
- R4: "Use sccache or a shared target directory across checkouts and worktrees"; "CI only: use mold
  or lld on Linux" (lld is already the Linux default).

**lumen control with a saved `junit.xml` present, Sonnet, no skill** (to separate "had no data" from
"no skill"). With per-test data it found real costs: `imaging` at opt-level 3 (16.7 s → 1.1 s,
measured) and a database-wide advisory lock queueing 264 `course_build` tests. Still failed R5 (kept a
nextest test group: "I have not measured by how much"), R4 (sccache on the list, no number), R9 (suite
refused, no final run, no hand-off).

What the text had to answer: from-memory levers on the list (3/3 runs), unverified changes kept (3/3),
an unmeasured number or a gate edit written into the repo (1/3), ranking without per-test data when the
suite would not run (1/3).

## GREEN — v1.0.0 draft

**beacon, Sonnet — pass R1–R10.** Kept one change, nextest `priority = 100` for the 17.2 s test (77%
of a 22.2 s wall), after three interleaved off/on pairs (19.3/19.4/18.2 s → 15.0/15.1/15.2 s); final
whole suite 1271 passed, 14.9 s; committed on `tune-rust-loop/2026-11-06`. `list.md` entries all carry
Cost / Change / Must still prove / Expected gain. Every non-fired lever recorded with its number.
Gap: ran `cargo clean` to get a cold build profile.

**lumen (saved junit present), Sonnet — pass R1–R8, R9 n/a (nothing kept).** The suite ran (860.7 /
1296.0 s at host load 5–9 / 14–19). The priority override fired (253.5 s = 29.5% of wall), lost its
rerun at host load 61, and was reverted. `list.md` ranked by test-seconds: `slot_*` waits 2055 test-s
first. Gaps:
1. ~330 test-seconds of image tests listed as "Not in the catalog, so I did not apply it" — the
   control had found the config fix for exactly those tests (16.7 s → 1.1 s).
2. The keep rule compared runs at load 61 against a baseline at 5–9.
3. Both this run and the control found a narrow `-p` run recompiling ~100 registry crates after a
   workspace build (feature set differs; `default-members` is `server`).

## REFACTOR — v1.0.0

Added from the GREEN gaps: the ≥ 5% uncovered-cost rule in step 2 (gap 1, with its numbers); the
host-load rule in step 3 (gap 2); the scratch target dir for a cold profile in step 1 (`cargo clean`);
levers rows "Unoptimised crate on a hot test path", "Tests queued on shared state" (control finding)
and "Feature set drifts between commands" (gap 3).

Re-run: lumen from the morning's step-1 artifacts, carrying on from step 2 (Sonnet).
- Gap 1 closed: applied `[profile.dev.package.imaging] opt-level = 3` and measured it on
  `cargo nextest run -p gateways --test it -E 'test(each_configured_width_serves_its_own_variant)'`:
  131.2 / 135.3 s → 31.1 / 71.7 s; committed. List ranked by test-seconds with the lock + waits first;
  clean-DB item marked unproven on this machine with the template-clone check named.
- New failure, close step: the final suite had 12 failures — 9 present at baseline, 1 known flake,
  2 new. It kept the commit: "Neither touches image code, and both look timing- or
  shared-state-dependent … The commit stands, but please rerun both tests alone before merging."
  (Its background rerun of one later passed in 8.1 s.) v1.0.0-draft said "a red suite reverts" —
  ambiguous when the baseline is already red.
- Load rule too strict: it kept a win measured under heavier load than baseline (45–77 vs 17–22),
  arguing the gain is understated. Correct; the draft rule would have voided it.

Untested wording: the uncovered-cost threshold was lowered from 10% to 5% after this run was
launched with the 10% copy (the imaging win came through the catalog row, not this rule), and the
step-3.4 load wording was never the text a tester read.

Text change: step 5 compares failing sets with the baseline and reruns each new failure on the final
tree and with the change reverted; step 3.4 lets a win under at least the baseline's load stand.

Close-step re-run (Sonnet), same fixture state with the closing `final.log` (12 failures) and a
deadline push ("branch ready to merge before the 15:00 sync … don't re-run the whole suite"):
compared the failing set with the baseline's (9 pre-existing), reran each of the 3 new failures alone
on the final tree (3 PASS) and with the change reverted (2 PASS, `live_faults` FAIL 95 s — the same
test failed in baseline suite 2), kept the commit because nothing reproduced only on the final tree,
and restored HEAD after the revert. Scored from `rerun-final.log` / `rerun-reverted.log`. Pass.

Artifacts kept in the authoring checkout: `.skills/RLOOP/{red,green}/`.
