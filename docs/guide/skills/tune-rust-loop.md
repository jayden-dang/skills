# `tune-rust-loop`

> Find where a Rust repo's builds and tests eat agent time, keep the config changes that pay, and rank the code changes that would.

|  |  |
|---|---|
| **Bucket** | setup |
| **Invocation** | user-invoked — run as `/tune-rust-loop`; no skill may auto-invoke it |
| **Reads** | `Cargo.toml`, `.cargo/config.toml`, `.config/nextest.toml`, `docs/agents/project.md` (suite and single-test commands), nextest logs or JUnit, `cargo metadata`, `cargo build --timings` |
| **Writes** | a `tune-rust-loop/<date>` branch with kept config changes; `.skills/tune-rust-loop/<date>/` (`baseline.md`, `list.md`, logs) |
| **Calls** | nothing; it names `/publish-issues` for the list |
| **Called by** | nothing — user-invoked |

## When to run it

When a Rust repo feels slow for agents: tasks spend their time compiling, or the end-of-feature suite
runs for half an hour. Run it again after the list's big items land, to see what moved.

## What it does

1. **Baseline.** Runs the whole suite with output captured and profiles it per binary and per test
   (`scripts/suite_profile.py`, nextest log or JUnit), profiles a build (`scripts/build_profile.py`
   over the `--timings` report), ranks crates by how many others rebuild when they change
   (`scripts/fan_in.py`), and times the single-test loop. If the suite cannot run on this machine it
   uses the newest saved nextest run, or stops and asks for one.
2. **Match.** Checks each lever in `levers.md` against those numbers. Only levers whose trigger holds
   fire. Nothing fires: the repo is already fast, and the run ends there.
3. **Apply config.** Profiles, `.cargo/config.toml`, nextest config, toolchain file, one change at a
   time, rerun twice, kept only when both reruns beat both baseline runs.
4. **List.** Every code change — test database harness, injectable clocks, hub crates, one test binary
   per crate — becomes a ranked entry with its measured cost, files, what the tests must still prove,
   and the expected gain.
5. **Close.** Whole suite on the final tree when anything was kept; one report.

It never edits `.rs` files, the repo's verify or gate commands, or database and container settings:
those go on the list.

## Why it is shaped this way

Three baseline runs without the skill (Sonnet, on clones of klynt and navori, plus a klynt control
handed a saved per-test report so missing data could not explain the result) measured their builds
well but put "share a target directory across worktrees" on their list — a setup Cargo reproduces as one
worktree silently running another's code — kept a change they never re-ran, wrote an unmeasured
number into the repo's docs, and, once the suite could not run, ranked the list by guess and missed
the two costs that made up most of klynt's suite. Evidence: `skills/setup/tune-rust-loop/TESTS.md`.
