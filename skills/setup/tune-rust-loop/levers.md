# Lever catalog

Open this file at step 2 and check **every** row's trigger against the baseline. A lever fires only
when its trigger holds on a number you measured; quote that number beside it.

## Suite execution (from `suite_profile.py`)

| Lever | Trigger | Class | Change |
|---|---|---|---|
| Clean test database per run | ≥ 25% of test-seconds sits in binaries whose tests open a database (`grep -rlE 'migrate!\|CREATE DATABASE\|PgPool' <crate>/tests`) | code | Clone the test DB from a template migrated once per migration hash at suite start; per-test `migrate!` or `CREATE DATABASE` + migrate becomes a template clone (Postgres `CREATE DATABASE … TEMPLATE`, default WAL_LOG strategy; avoid `FILE_COPY`). Prove the gain first: run the slowest DB binary on its current DB and on a fresh clone, same thread count. On klynt this was 7.0 s → 0.37 s median per test |
| Real-clock waits | a test ≥ 10 s whose body or helpers `sleep`/`timeout` for ≥ 1 s, or durations clustered at multiples of one period (85 / 169 / 253 s) | code | Make the duration or clock injectable and pass a short one in tests. Paused tokio time (`start_paused`) only for tests that await no real I/O: around a socket or database it fires timeouts early (measured) |
| Tests queued on shared state | a test group whose durations step in multiples of one period, or whose setup takes a database-wide lock (`pg_advisory_lock`) or claims rows any test could take | code | Scope the shared state to the test (its own tenant, offering, schema) and drop the lock. On klynt 264 `course_build` tests held one advisory lock and claimed the globally oldest row, so short tests sat at 254 s |
| Long tail first | the slowest test ≥ 25% of suite wall | config | `.config/nextest.toml` override with `priority` for those tests so they start first |
| Unoptimised crate on a hot test path | a test family ≥ 5% of test-seconds whose time is CPU work (image, codec, crypto, parsing) inside a workspace crate built at `opt-level` 0 | config | `[profile.dev.package.<crate>] opt-level = 3`; rerun that package's tests before and after. On klynt, `imaging` at opt 3 took its transcode test from 16.7 s to 1.1 s |
| More test threads | wall ≥ 0.8 × test-seconds ÷ threads (saturated) **and** host load < half the cores **and** a sample binary's median at full threads ≤ 1.5× its median at 1 thread | config | Raise `test-threads`; if a database connection cap is why it is low, shrinking the per-test pool is a code lever |

## Compile and link (from `build_profile.py`, `fan_in.py`, the loop timing)

| Lever | Trigger | Class | Change |
|---|---|---|---|
| Hub crate | a crate with transitive dependents ≥ 50% of the workspace **and** ≥ 10 commits touching it in the last 90 days (`git log --since=90.days --oneline -- <path> \| wc -l`) | code | Move the churning items out of it, or cut edges into it; review any new dependency edge |
| One test binary per crate | a crate with ≥ 5 test targets | code | `tests/it/main.rs` with one `mod` per former file (rust-analyzer, uv and Cargo do this); move nextest `binary_id` overrides with it |
| Heavy build scripts and proc-macros | a build-script or proc-macro unit ≥ 20 s in the timings | config | `[profile.dev.package.<name>] opt-level = 3` for runtime-heavy deps, `[profile.dev.build-override] opt-level` for build scripts |
| Debug info on workspace crates | `profile.dev` sets no `debug` and linking test binaries is ≥ 30% of the loop timing | config | `debug = "line-tables-only"` on `[profile.dev]` only |
| Feature set drifts between commands | after a workspace build, the repo's single-test command prints `Compiling` for registry crates | code | One feature set for build, test and list (the same `--workspace --all-features`, a cargo alias, or `default-members`); cost is the extra rebuild seconds. On klynt a narrow `-p` run after a workspace build recompiled about 100 crates (2m46) |
| `CI` set in agent shells | `echo $CI` is non-empty where agents build and Cargo ≥ 1.99 | config | Report it: Cargo 1.99 turns incremental off when `CI` is set |

## Never apply, never list as a win

Both baseline runs put the first row on their list. Each row cost a measured failure:

| Idea | What happened |
|---|---|
| Share `CARGO_TARGET_DIR` or `build.build-dir` across checkouts or worktrees | Reproduced on Cargo 1.99.1 and 1.100-nightly: one worktree's tests ran another worktree's code and Cargo reported `Finished` (cargo#12516, #17312). Keep target and build dirs per checkout |
| sccache to warm new worktrees | 115 of 134 units hit, wall time 1–4 s better: build scripts and links dominate |
| `[profile.dev.package."*"] debug = false` on macOS | Broke both baseline builds: `can't find crate for rustversion`, and `libsqlx_macros` "mis-aligned LINKEDIT string pool" |
| Another linker on macOS | Bundled `rust-lld` fails against the Xcode 27 SDK; mold and wild have no Mach-O support. On Linux x86_64, lld is already the default (1.90) |
| `start_paused` on tests that await a database | Timeouts fire at virtual time while the real reply is still in flight |
