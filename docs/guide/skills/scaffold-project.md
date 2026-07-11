# `scaffold-project`

> Bootstrap a greenfield repository to a verified baseline — a skeleton where every quality tool is wired and demonstrably working, so the first feature starts from green.

|  |  |
|---|---|
| **Bucket** | setup |
| **Invocation** | user-invoked — run as `/scaffold-project`; no skill may auto-invoke it, others only name it for the user to run |
| **Reads** | the target directory (`ls -A`, `git rev-parse`, `git ls-files`, manifest presence), the parent repo's shared config in subpackage mode |
| **Writes** | git repo, root manifest, source skeleton, test harness with one passing example test, formatter/linter config, pre-commit hook, CI stub, README, and docs seeds |
| **Calls** | [`grilling`](grilling.md) (Step 1, required), [`verify`](verify.md) (Step 3, required) |
| **Called by** | nothing — it is user-invoked; it hands off to [`setup-repo`](setup-repo.md) at the end |

## When it fires

Run it when starting a brand-new project in an empty or nearly-empty directory and the user wants a working repository skeleton — stack chosen, test harness wired, tooling and CI in place — before any feature work begins. It is also the entry point when the user says "scaffold" while standing in an existing project: the skill detects that and redirects rather than scaffolding on top of real config.

Because `disable-model-invocation` is set, no other skill starts it automatically. The deliverable is the harness, proven by one passing example test — nothing more. The skill explicitly does not skip ahead to feature code. It opens a todo per step (0–4) and completes them in order, checking each off only when its **Done when** is met.

## Step 0 — confirm the target is greenfield — GATE

Scaffolding writes a project root — git repo, root manifest, root README, root CI, root pre-commit hook. Doing that on top of an existing project collides with or overwrites real config, so before anything else the skill resolves **where** it is scaffolding and proves the target is empty. This gate is not optional and not a judgment call made by feel — the check is run.

**Resolve the target directory** first. The default is the current working directory. If the user named a destination ("scaffold a `bot` package under `packages/`"), that path is the target. If the cwd is itself a populated repo root but the user asked for a *new* subpackage, the target resolves to that new subdirectory and **that** is what gets classified — the skill does not stop at the root's verdict.

**Inspect it directly** — never ask the user what is in the directory, look: `ls -A <target>` for existence and emptiness, `git -C <target> rev-parse --is-inside-work-tree` and `git -C <target> ls-files | wc -l` for repo membership and tracked-file count, and a check for a package manifest (`package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, …).

**Classify and branch:**

| Target state | Meaning | Action |
|---|---|---|
| Does not exist, or exists and is empty / only holds `.git`, `README`, `LICENSE` — and no manifest | **Greenfield** | Proceed to Step 1. |
| A new/empty subdirectory *inside* an existing git repo (e.g. `packages/bot` in a monorepo) | **Subpackage** | Proceed to Step 1 with the subdirectory as target; set `inside-existing-repo = true` (Step 2 skips the root-touching parts). |
| Exists and holds a manifest or many tracked files — a real project | **Not greenfield — STOP** | Do not scaffold. Redirect. |

**When it must stop, it redirects — it does not improvise a menu.** If the user wants to use the skill set in the existing repo (configure tracker, verify commands, docs) that is [`setup-repo`](setup-repo.md), not scaffolding, and they are told to run it. If they want a new package inside the repo, the new subdirectory path is confirmed and the gate is re-run against it (it should land in the Subpackage row). If they arrived by mistake, the skill stops and lets them reconsider. Done when the target is classified greenfield or subpackage and its resolved path is confirmed, or the skill has stopped and named the redirect.

## Step 1 — grill the stack

A **required sub-skill**: [`grilling`](grilling.md) settles the stack and layout decisions for the resolved target, one question at a time, each with a recommended default and a one-line reason — project name, language and runtime, framework (or "none"), test runner, formatter and linter, package manager, repo layout (single package vs workspace, source/test shape), license, and whether to commit or stage the result for review first. The skill looks up facts itself (what tools the user has installed, what the parent repo already uses in subpackage mode) and brings only judgment calls to the user. Done when every decision is explicitly confirmed and restated in one summary block — including the resolved target path — that the user approves.

## Step 2 — scaffold

Build the skeleton with the confirmed choices, at the resolved target. The **root-only vs subpackage** distinction runs through the step: in **subpackage mode** (`inside-existing-repo = true`) the steps marked *(root only)* are skipped because the parent repo already owns them, and the package inherits the parent's shared config instead of creating competing copies.

1. **Git** *(root only)* — `git init` if needed, plus a stack-appropriate `.gitignore`. In subpackage mode: no init, no touching the root `.gitignore`; add a package-local ignore only if needed.
2. **Project skeleton** — manifest, source directory, minimal entry point. In subpackage mode: extend the workspace's shared toolchain config (e.g. a `tsconfig` that `extends` the root) and register the package with the workspace.
3. **Test harness** — install and configure the runner plus **exactly one passing example test**, whose job is to prove the wiring (imports resolve, the runner finds files, assertions execute), not to test real behavior.
4. **Formatter + linter config** — committed config with `format`, `lint`, and `typecheck` (where applicable) as single commands. In subpackage mode: inherit root config, add only package-level overrides.
5. **Pre-commit hook** *(root only)* — on every commit: format staged files, then lint, typecheck, and test, via the stack's idiomatic mechanism. In subpackage mode: integrate with the parent's existing hook scoped to the package, not a competing root hook.
6. **CI stub** *(root only)* — one workflow running the same verify commands on push and PR. In subpackage mode: append a package-filtered job to the existing CI, not a new pipeline.
7. **README skeleton** — project name, a one-paragraph description placeholder, and the install and verify commands, placed at the target (in subpackage mode `<target>/README.md`, never the repo root).
8. **Docs seeds** — `CONTEXT.md` (from `templates/CONTEXT.md`), `docs/specs/INDEX.md` (from `templates/specs-INDEX.md`), and an empty `docs/adr/` directory, all relative to the target.

Done when every applicable item exists and is committed (or staged, per the Step 1 choice).

## Step 3 — verify the baseline

A **required sub-skill**: [`verify`](verify.md) runs the full verify suite (typecheck, lint, test) fresh and reads the output. In root mode it also proves the pre-commit hook actually fires and passes (a throwaway commit or dry run). A scaffold that hands off with a failing or unproven check is not done — the offending piece is fixed or removed first. Done when every verify command passes and the passing output has been shown to the user.

## Step 4 — hand off

Tell the user the scaffold is complete and that the next step is [`setup-repo`](setup-repo.md), which writes the agent-facing config (`docs/agents/*.md` — verify commands, tracker, labels, release steps). This skill does not write `docs/agents/` itself; that wizard owns it. The completion criterion for the whole skill: from the repo root, one command installs dependencies and one command runs the target's verify suite green — both stated explicitly in the final summary (scoped to the new package in subpackage mode).

## Worked example

A greenfield TypeScript CLI in an empty directory.

**Step 0.** `ls -A .` is empty, `git rev-parse` reports not-a-repo, no manifest — the **Greenfield** row. The resolved target is the cwd, confirmed with the user.

**Step 1.** `grilling` settles: name `taskcat`, Node + TypeScript, no framework, Vitest, Prettier + ESLint, pnpm, single package, MIT, commit the result. Restated in one block and approved.

**Step 2.** `git init` and a Node `.gitignore`; `package.json`, `tsconfig.json`, `src/index.ts`; Vitest wired with one `src/smoke.test.ts` asserting `1 + 1 === 2` to prove the runner resolves; `format`/`lint`/`typecheck` scripts; a pre-commit hook that formats staged files then lints, typechecks, and tests; a CI workflow running the same commands on push and PR; a README with install and verify commands; and `CONTEXT.md`, `docs/specs/INDEX.md`, and an empty `docs/adr/`. All committed.

**Step 3.** `verify` runs `pnpm typecheck`, `pnpm lint`, `pnpm test` fresh — all green — and a dry commit proves the pre-commit hook fires.

**Step 4.** Hand off: "scaffold complete; run `/setup-repo` next. Install with `pnpm install`, verify with `pnpm test`."

## Why it is written the way it is

The skill guards two failure modes. The first is scaffolding on top of a real project — irreversible collisions with existing config — which is why Step 0 is a hard gate that inspects rather than asks, resolves the target before judging it, and redirects to `setup-repo` rather than pushing ahead. The second is a skeleton that looks wired but is not, which is why the deliverable is capped at one *passing* example test and Step 3 refuses to hand off on an unproven check. The root-only vs subpackage split keeps the same skill correct in a monorepo, where inheriting the parent's toolchain is right and installing a competing root hook or CI pipeline is wrong. The clean division of labor — this skill owns the harness, `setup-repo` owns `docs/agents/` — keeps each wizard's completion criterion sharp.

## See also

- [`setup-repo`](setup-repo.md) — the hand-off target that writes the agent-facing config
- [`grilling`](grilling.md) — the required interview sub-skill for the stack decisions
- [`verify`](verify.md) — the required baseline-proving sub-skill
- [Templates](../resources/templates.md) — the `CONTEXT.md` and `specs-INDEX.md` seeds this skill copies
