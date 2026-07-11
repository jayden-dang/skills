# Running on other platforms

The skill set was built for Claude Code, but nothing in it is Claude-specific:
the skills are plain `SKILL.md` files, the linters are Python 3.9+ stdlib, and
the shell tooling is bash. The only platform-specific part is *how the gate gets
injected* — the mechanism that reminds the agent to check for a skill before it
acts. This page covers that per platform.

The portable contract for every platform is [`AGENTS.md`](../../../AGENTS.md) at
the repo root: the Four Iron Laws, the 1% rule, the trace-spine citation rules,
the subagent protocol, and the full skill inventory. Any harness that can read a
repo file can run this system by reading that one.

## Claude Code (native)

Full support. The `SessionStart` hook in `hooks/hooks.json` injects
`meta/using-skills` on every `startup | clear | compact`, so the gate survives
compaction automatically. Install as a plugin, or symlink the skills:

```bash
git clone https://github.com/jayden-dang/skills ~/dev/skills
~/dev/skills/scripts/link-skills.sh   # symlinks into ~/.claude/skills
```

## Codex CLI

Codex reads `AGENTS.md` from the repo root natively — no extra file needed. It
picks up the behavior contract on its own. Codex has no session-start hook, so
the gate is enforced by `AGENTS.md` being in context rather than by re-injection
after compaction; after a long session, re-point it at `AGENTS.md` if it drifts.

## Cursor

Cursor loads `.cursor/rules/*.mdc`. This repo ships
[`.cursor/rules/using-skills.mdc`](../../../.cursor/rules/using-skills.mdc) as an
`alwaysApply` rule that carries the gate and points at `AGENTS.md`. Copy the
`.cursor/` directory (and `AGENTS.md`, `skills/`, `scripts/`) into the target
repo, or open this repo directly. That rule is Cursor's substitute for the
session-start hook.

## Any other harness

If the harness can load a repo-root convention file (`AGENTS.md`, `CLAUDE.md`,
or similar), point it there. If it supports an always-on rule or system-prompt
append, give it the gate paragraph from `.cursor/rules/using-skills.mdc`. The
skills, linters, and templates work unchanged — only the injection path differs.

## What is not portable

- **Automatic re-injection after compaction** is a Claude Code hook feature.
  Elsewhere the gate lives in an always-on rule or the root contract file, which
  is durable but not self-healing across a context reset — re-anchor manually if
  the agent drifts.
- **Subagent dispatch** in `execute-plan` assumes a harness that can spawn
  fresh, isolated subagents. Where that is unavailable, `execute-plan`'s inline
  fallback runs the same loop in a single context.
