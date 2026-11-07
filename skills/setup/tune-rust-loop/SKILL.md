---
name: tune-rust-loop
version: 1.1.0
description: Measures where a Rust repo's builds and tests spend agent time, keeps the config changes that pay, and ranks the code changes that would.
disable-model-invocation: true
---

# Tune the Rust Loop

Agents in a Rust repo wait on three things: the inner loop (edit, build one test binary, run it),
the task gate, and the whole suite at the end of a feature. This skill finds which one costs the
time, applies the configuration changes that measurably cut it, and hands back a ranked list of the
code changes that would cut the rest. Every number in the output was measured here, on this commit.

Not a Cargo workspace (no `Cargo.toml` at the root)? Say so and stop.

## Where the run sits

First, record these in `baseline.md`:

```
git branch --show-current
git rev-parse --show-toplevel
```

That branch and that directory are the starting checkout. `git status --porcelain` shows a path → stop and name the files. The starting checkout stays on that branch until the run ends.

No repo file is left changed (baseline, matching levers, the list, or a config lever reverted with nothing committed): do the work in the starting checkout. Reports go in its `.skills/tune-rust-loop/<date>/`.

A config lever fired (step 3): add the worktree at the start of step 3, not during baseline or the list. Run this in the starting checkout. Do every edit, rerun, revert, and commit in that worktree.

```
TOP=$(git rev-parse --show-toplevel)
git worktree add -b tune-rust-loop/<date> "$(dirname "$TOP")/$(basename "$TOP")-tune-rust-loop-<date>" HEAD
```

The worktree keeps its own `target/`. Write every report, including logs from commands run in the worktree, into the starting checkout's `.skills/tune-rust-loop/<date>/`.

Every config lever reverted and the worktree has no commit past the starting HEAD → remove it and delete the branch:

```
git worktree remove "$(dirname "$TOP")/$(basename "$TOP")-tune-rust-loop-<date>"
git branch -d tune-rust-loop/<date>
```

A change kept → leave the worktree and the branch, and report both paths. Merging is the operator's.

**Done when:** `git -C <starting toplevel> branch --show-current` prints the name recorded above.

| Thought | Reality |
|---|---|
| Create the branch first so the scan has somewhere to live | fieldkit changed no file and the checkout still moved to `tune-rust-loop/2026-11-07` while HEAD stayed `7f54155`. The report lives under `.skills/` |
| The edit gets reverted, so moving the checkout does not matter | harbor wrote `.config/nextest.toml` in the checkout it had just switched, then deleted the file. That checkout sat on the new branch the whole time |

## 1. Baseline — before any file changes

Follow **Where the run sits.** Put every output under `.skills/tune-rust-loop/<date>/` in the starting checkout and run the scripts beside this file with `python3 <this dir>/scripts/<name>.py`.

1. **Suite.** Run the repo's whole-suite command (`docs/agents/project.md` names it; else
   `cargo nextest run --workspace`) with its output captured to `suite.log`, and record `uptime` and
   any other `cargo`/`rustc` processes alongside it. Then `suite_profile.py suite.log`.
2. **Suite blocked?** IF the suite cannot run here — a service is down, a permission check refuses
   it, it needs infrastructure you may not touch — THEN use the newest nextest JUnit or log you can
   find (`target/nextest/*/junit.xml`, saved logs), state its date and commit, and profile that. None
   → stop and ask the operator to run the suite command with its output saved. Do not rank suite
   work without per-test durations: the one baseline that tried ranked by "I think" and missed both
   costs that mattered — a harness at 65% of the suite and real-clock waits at 28%.
3. **Build.** `cargo build --workspace --tests --timings` → `build_profile.py
   target/cargo-timings/cargo-timing.html`. Then `fan_in.py`. A cached build gives an empty
   profile; for a cold one, build into a scratch dir (`CARGO_TARGET_DIR=$(mktemp -d)`) and keep the
   repo's `target/` — `cargo clean` throws away a warm cache that took minutes to build.
4. **Loop.** Touch one source file of the crate `fan_in.py` ranks first, run the repo's single-test
   command on a test binary that depends on it, time it twice, then restore that file.

**Done when:** `baseline.md` holds the suite profile, the build profile, the fan-in table, the two
loop timings, the commit, the host load, and the exact commands that produced each.

## 2. Match levers

Open `levers.md` and check every trigger against `baseline.md`. A lever fires only when its trigger
holds on a measured number; write the lever, its class (config / code) and that number.
A binary or test family holding ≥ 5% of test-seconds that no fired lever covers: read why (the
test body, the crate's profile) and treat the cause as a lever of its own — config or code by the
rules in step 3. One run listed 330 test-seconds of image tests as "not in the catalog"; reading the
crate's profile gave a config fix worth 16.7 s → 1.1 s on its slowest test.
Nothing fires → report the repo as already fast with the baseline numbers, change nothing, stop.

**Done when:** every row of `levers.md` is marked fired (with its number) or not fired.

## 3. Apply config levers, one at a time

Config here means `Cargo.toml` profiles, `.cargo/config.toml`, `.config/nextest.toml` and
`rust-toolchain.toml`. Edit those files only in the worktree from **Where the run sits.** For each fired config lever:

1. Make the one change.
2. Rerun the command that produced its trigger number, twice.
3. Keep it only if both runs beat both baseline runs; otherwise revert it. A change that breaks the
   build is reverted on the spot.
4. Record `uptime` with every run. A win measured under at least the baseline's load stands. After
   runs under clearly lighter load are not a result: wait and rerun, or revert and mark the lever
   unmeasured. Wall times on klynt moved 50% on one commit as other sessions built (load 5 → 61).

Everything else that would change behavior or a gate goes to the list in step 4 instead of being
edited: any `.rs` file, the repo's verify or gate commands (`docs/agents/project.md`, `justfile`,
`moon.yml`, `xtask` test steps, CI workflows), and container or database server settings.
A number written into a repo file is one this run measured, with the command beside it.

**Done when:** each fired config lever is kept with before/after numbers or reverted with its numbers.

## 4. The list

One entry per fired code lever, ranked by measured cost. Each entry has these parts, in order:

- **Cost:** the measured seconds it accounts for (test-seconds, or rebuild seconds × dependents) and
  the artifact the number came from.
- **Change:** what to do, with the files or crates involved.
- **Must still prove:** the behavior the affected tests check today, which the change keeps.
- **Expected gain:** the estimate and what it rests on (measured here / measured elsewhere /
  source only).

Write it to `list.md`. Publishing it is the operator's call (`/publish-issues`).

## 5. Close

IF any config change was kept THEN run the whole suite once on the final tree and profile it, and
compare its failing tests with the baseline's. The same set is no regression. For each failure the
baseline did not have, rerun that test alone on the final tree and once with the kept changes
reverted: a failure that only the final tree reproduces reverts the change. One run committed over two
new failures because "neither touches image code" and never finished the reruns.
Commit a kept change in the worktree, then close **Where the run sits.**

Report, in this order: baseline (suite wall, test-seconds, loop timing); kept changes with
before → after; reverted changes with their numbers; the list; anything not measured and why.

## Red Flags

- A list entry or kept change with no number from this run behind it.
- Sharing a target or build directory across checkouts, sccache, or a new linker on the list — see
  the last table in `levers.md` for what each cost when tried.
- A kept change whose rerun you did not do, or a gate command edited "because it is redundant".
- The starting checkout's branch differs from the name recorded at the start.
- A config path (`Cargo.toml`, `.cargo/config.toml`, `.config/nextest.toml`, `rust-toolchain.toml`) differs inside the starting toplevel.
