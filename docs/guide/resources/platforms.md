# Running on other platforms

The skill set was built for Claude Code, but nothing in it is Claude-specific.
Everything is plain text a reasoning agent acts on: the skills are `SKILL.md`
files, the portable behavior contract is `AGENTS.md`, and the audit-trace check is a
set of `grep`/`git` passes the agent drives itself — there is no interpreter or
binary to port. There is no session-start injector. The 1% rule lives in `AGENTS.md`;
`/zone-mode` is user-run. This page covers how each platform loads the pack.

The portable contract for every platform is [`AGENTS.md`](../../../AGENTS.md) at
the repo root: the Four Iron Laws, the 1% rule, the trace-spine citation rules,
the subagent protocol, and the full skill inventory. Any harness that can read a
repo file can run this system by reading that one.

## Claude Code (native)

Full support. Install as a plugin so commands are `/jdk:<skill>`:

```text
/plugin marketplace add jayden-dang/skills
/plugin install jdk@jayden-dang-skills
```

Do **not** also run `npx skills add` targeting Claude Code on the same machine —
flatten plus plugin duplicates every skill (`/frame-change` and `/jdk:frame-change`).

Grok reads the same marketplace (`grok plugin marketplace add jayden-dang/skills`
then `grok plugin install jdk --trust`).

## Installing skills for every other agent

The `skills` CLI fans out to agent stores that do **not** load this repo as a
plugin (Cursor, …). Flatten keeps bare skill names, not the `/jdk:` prefix:

```bash
npx skills@latest add jayden-dang/skills -a '*' --copy
```

If you already installed `jdk` as a Claude/Grok/Codex/Kimi plugin, omit those
agents from the fan-out (do not use `-a '*'` blindly). OpenCode should use this
repo's `opencode.json` (or a global copy of its `skills` paths), not a flatten
of the nested `skills/<category>/` tree.

`-a '*'` targets every detected agent, `--copy` writes real directories instead of
symlinks, and `npx skills@latest update` refreshes them later. The CLI records a
`skills-lock.json`, so a second machine reaches the same set via
`experimental_install` rather than by re-deriving it.

| Agent | Store | Form |
|---|---|---|
| Claude Code | plugin `jdk`, or `~/.claude/skills/` | plugin `/jdk:<skill>`; flatten is bare names |
| Codex CLI | plugin `jdk`, or `~/.agents/skills/` | plugin namespace `jdk`; flatten needs `--copy` |
| Kimi Code | plugin `jdk`, or `~/.kimi-code/skills/` | plugin `/skill:<name>`; do not flatten on top |
| OpenCode | `opencode.json` `skills` paths, plus `~/.config/opencode/skills` / `~/.agents/skills` | `skill` tool by folder name; clone this repo or point at category dirs |
| Cursor | `.cursor/skills/` / `~/.agents/skills/` | flatten `/skill-name` |

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

Codex also reads `AGENTS.md` from the repo root natively. After a long session,
re-point it at `AGENTS.md` if it drifts. Run `/zone-mode` when you want the
full gate loaded.

Fallback without the plugin: `npx skills@latest add jayden-dang/skills --copy -a codex`
(bare skill names, not `jdk:`).

## Kimi Code CLI

Install Engineer Pack as a Kimi plugin (slug `jdk`):

```text
/plugins install https://github.com/jayden-dang/skills
```

That uses `.kimi-plugin/plugin.json` (explicit skill paths, same list as Claude)
and optional `.kimi-plugin/marketplace.json` (`version: 2`). After install, run
`/reload` or start a new session.

Kimi **commands** are namespaced `/jdk:<command>`. This pack ships skills, not
command wrappers, so you invoke `/skill:frame-change` (and the model can auto-load
from `description`). That is not `/jdk:frame-change`.

Do not also flatten Engineer Pack into `~/.kimi-code/skills` or `~/.agents/skills`
on the same machine.

## OpenCode

OpenCode discovers `SKILL.md` from `.opencode/skills`, `~/.config/opencode/skills`,
and Claude/agents compatibility dirs, including nested folders. Its **plugins**
are npm/TS hooks, not skill packs — there is no `/jdk:` marketplace.

This repo ships `opencode.json` with `skills` set to the eleven Engineer Pack
category directories (`./skills/discovery`, …), not `./skills` (that would also
load Personal Pack). Clone this repo and run OpenCode in it, or copy those paths
into `~/.config/opencode/opencode.json` pointing at the clone:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "skills": [
    "/absolute/path/to/skills/skills/meta",
    "/absolute/path/to/skills/skills/setup",
    "/absolute/path/to/skills/skills/discovery",
    "/absolute/path/to/skills/skills/spec",
    "/absolute/path/to/skills/skills/execution",
    "/absolute/path/to/skills/skills/review",
    "/absolute/path/to/skills/skills/acceptance",
    "/absolute/path/to/skills/skills/craft",
    "/absolute/path/to/skills/skills/ship",
    "/absolute/path/to/skills/skills/track",
    "/absolute/path/to/skills/skills/project"
  ]
}
```

The skill ID is the folder that contains `SKILL.md` (`frame-change`). Load with
the `skill` tool. OpenCode also reads `AGENTS.md`.

Do not flatten the nested `skills/<category>/` tree into `~/.agents/skills/`
for OpenCode — category names are not skills.

## Cursor

Cursor reads `AGENTS.md`. There is no always-apply rule and no session-start
hook. Run `/zone-mode` when you want the full gate loaded.

## Any other harness

If the harness can load a repo-root convention file (`AGENTS.md`, `CLAUDE.md`,
or similar), point it there. The skills and templates work unchanged.

## What is not portable
- **Subagent dispatch** in `build-in-waves` assumes a harness that can spawn
  fresh, isolated subagents. Where that is unavailable, `build-in-waves`'s inline
  fallback runs the same loop in a single context.
