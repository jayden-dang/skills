---
name: scaffold-project
description: Use when starting a brand-new project in an empty or nearly-empty directory and the user wants a working repository skeleton — stack chosen, test harness wired, tooling and CI in place — before any feature work begins.
disable-model-invocation: true
---

# Scaffold a Project

Bootstrap a greenfield repository to a verified baseline: a skeleton where every quality tool is wired and demonstrably working, so the first feature starts from green.

Do not skip ahead to feature code. The deliverable is the harness, proven by one passing example test — nothing more.

## 1. Grill the stack

REQUIRED SUB-SKILL: use `grilling` to settle the stack and layout decisions — one question at a time, each with a recommended default and a one-line reason:

- Language and runtime
- Framework (or "none — plain library/CLI")
- Test runner
- Formatter and linter
- Package manager
- Repo layout (single package vs workspace/monorepo; source and test directory shape)
- License

Look up facts yourself (what is already in the directory, what tools the user has installed); bring only judgment calls to the user.

**Done when:** every decision above is explicitly confirmed and restated in one summary block the user approves.

## 2. Scaffold

Build the skeleton with the confirmed choices:

1. **Git** — `git init` if the directory is not already a repo; write a sensible `.gitignore` for the stack.
2. **Project skeleton** — manifest, source directory, minimal entry point.
3. **Test harness** — install and configure the runner, plus **exactly one passing example test**. Its job is to prove the wiring (imports resolve, runner finds files, assertions execute), not to test real behavior.
4. **Formatter + linter config** — committed config files, with `format`, `lint`, and `typecheck` (where applicable) runnable as single commands.
5. **Pre-commit hook** — on every commit: format the staged files, then lint, typecheck, and test. Use the stack's idiomatic hook mechanism (a hook manager if the ecosystem has a standard one, otherwise a plain `.git/hooks/pre-commit` script committed as a setup script). Keep the staged-file scope for formatting so commits stay fast.
6. **CI stub** — one workflow that runs the same verify commands (typecheck, lint, test) on push and pull request. Nothing fancier; `setup-repo` can add the trace check later.
7. **README skeleton** — project name, one-paragraph description placeholder, and the two commands that matter: install and verify.
8. **Docs seeds** — `CONTEXT.md` (from the skill set's `templates/CONTEXT.md`), `docs/specs/INDEX.md` (from `templates/specs-INDEX.md`), and an empty `docs/adr/` directory.

**Done when:** all eight items exist and are committed (or staged, if the user prefers to review first).

## 3. Verify the baseline

REQUIRED SUB-SKILL: use `verify` — run the full verify suite (typecheck, lint, test) fresh and read the output. Also make one throwaway commit or use a dry run to prove the pre-commit hook actually fires and passes.

A scaffold that hands off with a failing or unproven check is not done. Fix or remove the offending piece before proceeding.

**Done when:** every verify command passes, and you have shown the user the passing output.

## 4. Hand off

Tell the user the scaffold is complete and that the next step is to run `setup-repo` to write the agent-facing config (`docs/agents/*.md` — verify commands, tracker, labels, release steps). Do not write `docs/agents/` yourself; that wizard owns it.

**Completion criterion for the whole skill:** a fresh clone of this repo can install dependencies with one command and pass the full verify suite with one command — state both commands explicitly in your final summary.
