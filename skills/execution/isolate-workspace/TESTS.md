# `isolate-workspace` — tests

## Edit — seed a Rust worktree with cargo-hive before its first build (v1.2.0)

**Origin.** User request: integrate cargo-hive (`cargo-hive` 0.1.0, installed, with its
`hive` skill) so Rust worktrees reuse the main checkout's built dependencies. Question
asked first: does the installed `hive` skill already make agents seed?

**Scenario (RED and GREEN, unchanged between them).** A fresh git repo
`~/Developer/clients/<random>/ledgerline`: one Rust crate depending on `anyhow`,
`serde`, `serde_json`, with the main checkout already built. `.claude/skills/` holds
`isolate-workspace`, `hive` (cargo-hive's plugin skill, verbatim) and `test-first`, all
three listed with name, description and path. The user asks for `feat/csv-export` in an
isolated worktree, ready to implement. No native worktree tool. The prompt never mentions
seeding, cache or hive. Roster: Sonnet (`skill-tester`), Haiku (`skill-tester-haiku`).
Three runs per model, one fixture per run. Scored from hive's own record:
`cargo hive status <main> --json`, counter `reused_fresh:<worktree>/target` > 0, plus
the command order.

**RED (v1.1.0 Step 2: `Cargo.toml` → `cargo build`).** 2 of 6 seeded (Sonnet 1/3, Haiku
1/3). All six read the `hive` SKILL.md. The four that built cold, verbatim:

- Sonnet: "`cargo hive` 0.1.0 is installed, but I built before considering `seed`, so the
  worktree has already done its own full build. Seeding no longer applies to it." (ran
  `cargo hive --version` and `cargo build` in one command)
- Sonnet: "I read it but didn't use it: I wasn't reclaiming disk and the build took 2.5s."
- Haiku: "hive is for reclaiming disk space and seeding target/ dirs … The worktree built
  from scratch in about 3s, so seeding wasn't worth it"
- Haiku: "I did not use it: this is a plain `cargo build` with no seeding or disk reclaim"

Classified as an omitted step in something the skill already produces (Step 2), and the
behaviour depends on an observable condition. Form: a conditional keyed to `Cargo.toml`
present, no `target/` yet, and `cargo hive --version` exiting 0, with the exact commands,
placed ahead of the existing manifest table. The counter carries the recorded excuses
(3 s build, disk-reclaim reading, built-first). A first draft also told the agent what to
do on a seed refusal and pointed at the `hive` skill for receipts. Both were cut, because
no run reached either case. The refusal recovery belongs to the `hive` skill, which says
to build the main checkout and seed again. Rerun on the trimmed text, one run per model on a fresh
fixture: both seeded before building (`reused_fresh` 26 each).

**GREEN (v1.2.0).** 6 of 6 seeded before the first `cargo build` (Sonnet 3/3, Haiku 3/3).
Every worktree target reads `reused_fresh` 26, with 27 units cloned and 0 failed. Every
run ran `repo add` on the main checkout, then `seed`, then `cargo build` (0.23–0.39 s).
One Haiku run cited the rule: "I seeded the worktree with hive before the first build, as
the isolate-workspace skill requires." No new rationalization appeared. Not tested: a
machine without `cargo-hive` (the predicate fails and Step 2 is unchanged), and the seed
refusal path.

**Measured alongside, left unchanged: `build-in-waves` lanes.** Lanes are made with a
plain `git worktree add` (step 4) and never pass through this skill, so they got their
own RED with v1.2.0 here installed. Fixture: a feature worktree off a built main, Task 1
ledgered clean, Tasks 2 and 3 ready with disjoint `Files:`. The controller is asked to
take the run up to dispatch. Of the six runs, four created two lanes, and all four seeded
every lane before its first build (Sonnet 2/2, Haiku 2/2). Each followed the `hive`
skill's own rule, "seed one lane first, build it, then seed the other lanes". The other
two went serial because both tasks need a `pub mod` line in `src/export.rs`, which
neither `Files:` list names (a fixture flaw), and both said they would seed the lanes in
the parallel case. That makes the lanes a no-op, so `build-in-waves` text was not written.
Confound: every run had also read this skill's v1.2.0 Step 2. Limit: the prompt asked the
controller to get everything in place "so its implementers can start at once", which
invites prep work. A real run dispatches straight after `git worktree add`, and the
implementer's first build comes from its brief, so a check on a real run is still owed.
Side finding: three runs put the lanes beside the feature worktree and one nested them
inside it. Step 4's `.worktrees/<branch>-lane<k>` does not say which root it is relative to. `land-branch` cleanup was
not tested. `git worktree remove` already deletes the worktree's `target/`, and a `gc`
scenario would act on the machine's real hive registry and store.

## Edit — share `.worktrees/` instead of minting `.isolate-workspace/` (v1.1.0)

**Origin.** User request: isolation for skills / execute / check should live
under `.worktrees/`, the conventional project-local worktree parent, instead of
a parallel `.isolate-workspace/` directory and gitignore entry.

**RED (v1.0.0 text).** Git fallback priority:

1. explicit user instruction
2. existing `.isolate-workspace/`
3. existing `isolate-workspace/`
4. neither → **create `.isolate-workspace/`**

`configure-repo` and `land-branch` restated the same parent. A repo that already
ignored `.worktrees/` still got a second ignored path.

**GREEN (v1.1.0).** Default parent is `.worktrees/`. Reuse an existing
`.worktrees/` (or `worktrees/`) rather than minting another directory. Append
`.gitignore` only when `$DIR` is not already ignored. Reuse a legacy
`.isolate-workspace/` / `isolate-workspace/` if one is already on disk, so a
second parent is not created beside it.
