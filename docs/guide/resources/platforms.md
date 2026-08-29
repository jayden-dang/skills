# Running on other platforms

The skill set was built for Claude Code, but nothing in it is Claude-specific.
Everything is plain text a reasoning agent acts on: the skills are `SKILL.md`
files, the portable behavior contract is `AGENTS.md`, and the audit-trace check is a
set of `grep`/`git` passes the agent drives itself — there is no interpreter or
binary to port. The only platform-specific part is *how the gate gets injected* —
the mechanism that reminds the agent to check for a skill before it acts. This
page covers that per platform.

The portable contract for every platform is [`AGENTS.md`](../../../AGENTS.md) at
the repo root: the Four Iron Laws, the 1% rule, the trace-spine citation rules,
the subagent protocol, and the full skill inventory. Any harness that can read a
repo file can run this system by reading that one.

## Claude Code (native)

Full support. The `SessionStart` hook in `hooks/hooks.json` injects
`meta/gate-session` on every `startup | clear | compact`, so the gate survives
compaction automatically. Install as a plugin so commands are `/jdk:<skill>`
and the hook ships with the pack:

```text
/plugin marketplace add jayden-dang/skills
/plugin install jdk@jayden-dang-skills
```

Do **not** also run `npx skills add` targeting Claude Code on the same machine —
flatten plus plugin duplicates every skill (`/frame-change` and `/jdk:frame-change`).

Grok reads the same marketplace (`grok plugin marketplace add jayden-dang/skills`
then `grok plugin install jdk --trust`).

## Installing skills for every other agent

The `skills` CLI fans out to agent stores that do not load Claude/Grok plugins
(Codex, Cursor, Kimi, …). Flatten keeps bare skill names, not the `/jdk:` prefix:

```bash
npx skills@latest add jayden-dang/skills -a '*' --copy
```

If you already installed `jdk` as a Claude/Grok plugin, omit Claude from that
fan-out (do not use `-a '*'` blindly).

`-a '*'` targets every detected agent, `--copy` writes real directories instead of
symlinks, and `npx skills@latest update` refreshes them later. The CLI records a
`skills-lock.json`, so a second machine reaches the same set via
`experimental_install` rather than by re-deriving it.

| Agent | Store | Form |
|---|---|---|
| Claude Code | `~/.claude/skills/` | symlink is fine — it follows them |
| Codex CLI | `~/.agents/skills/` | needs `--copy` (see below) |
| Kimi | `~/.kimi-code/skills/` | needs `--copy`, same reason, untested |
| opencode | — | no skills mechanism; reads `AGENTS.md` |

**Why `--copy` matters.** Codex resolves skills from `<project>/.agents/skills`, then
`$CODEX_HOME/skills` (deprecated), then `$HOME/.agents/skills`, then its own system
cache. It does **not** follow symlinked skill directories — verified on codex-cli
0.147.0, where a symlinked skill was absent from the list and the same skill copied
in was found. A copy is a snapshot, so re-run `update` after this repo changes; that
is what the lockfile is for.

## Codex CLI

Install Engineer Pack as a Codex plugin (slug `jdk`):

```bash
codex plugin marketplace add jayden-dang/skills
codex plugin add jdk@jayden-dang-skills
```

That uses `.codex-plugin/plugin.json` and `.agents/plugins/marketplace.json`.
Do not also flatten Engineer Pack into `~/.agents/skills` / `~/.codex/skills`
on the same machine.

Codex also reads `AGENTS.md` from the repo root natively. It has no session-start
hook, so the gate is enforced by `AGENTS.md` being in context rather than by
re-injection after compaction; after a long session, re-point it at `AGENTS.md`
if it drifts.

Fallback without the plugin: `npx skills@latest add jayden-dang/skills --copy -a codex`
(bare skill names, not `jdk:`).

## Cursor

Cursor loads `.cursor/rules/*.mdc`. This repo ships
[`.cursor/rules/gate-session.mdc`](../../../.cursor/rules/gate-session.mdc) as an
`alwaysApply` rule that carries the gate and points at `AGENTS.md`. Copy the
`.cursor/` directory (and `AGENTS.md`, `skills/`) into the target repo, or open
this repo directly. That rule is Cursor's substitute for the session-start hook.

## Any other harness

If the harness can load a repo-root convention file (`AGENTS.md`, `CLAUDE.md`,
or similar), point it there. If it supports an always-on rule or system-prompt
append, give it the gate paragraph from `.cursor/rules/gate-session.mdc`. The
skills and templates work unchanged — only the injection path differs.

## What is not portable

- **Automatic re-injection after compaction** is a Claude Code hook feature.
  Elsewhere the gate lives in an always-on rule or the root contract file, which
  is durable but not self-healing across a context reset — re-anchor manually if
  the agent drifts.
- **Subagent dispatch** in `build-in-waves` assumes a harness that can spawn
  fresh, isolated subagents. Where that is unavailable, `build-in-waves`'s inline
  fallback runs the same loop in a single context.
