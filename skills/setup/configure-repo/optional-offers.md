# Optional offers — session-start hook and Context7 MCP

Load this file **only when Step 5 (Offer the session-start hook) runs**.

The skill set installs nothing else into the repo — no linters, no CI steps, no git hooks. Two optional offers remain — one keeps the skill-usage gate alive, the other gives the skills current library facts:

**Session-start hook.** If this skill set was installed without plugin hook support, offer to add a `SessionStart` hook (matcher `startup|clear|compact`) so the gate survives `/clear` and compaction. **Vendor the hook into the repo — never reference a path outside it.** An absolute path (e.g. to the skill set's own working copy) is committed into `.claude/settings.json` and breaks on any other machine, in CI, or if that copy moves. Instead:
   - Copy `templates/session-start.sh` to `.claude/hooks/session-start.sh` in the repo and `chmod +x` it. It is dependency-free (plain `cat`), so it runs in any project regardless of toolchain.
   - Reference it in `.claude/settings.json` via the project-dir variable, not an absolute path:
     ```json
     { "hooks": { "SessionStart": [ { "matcher": "startup|clear|compact",
       "hooks": [ { "type": "command",
         "command": "\"$CLAUDE_PROJECT_DIR/.claude/hooks/session-start.sh\"" } ] } ] } }
     ```
   - Merge into any existing `SessionStart` block additively; do not clobber other hooks.

**Context7 MCP — for live library docs.** Several skills reason about third-party libraries — `research` when a question turns on how a library behaves, `design-solution` when the reuse ladder reaches a new dependency. Left to training knowledge alone, an agent cites versions and APIs that may be months stale. Recommend the user install the **Context7 MCP server**, which serves current, version-specific documentation from the source; explain that the library skills prefer it when present and fall back to fetching official docs when it is absent. It is an agent-environment tool, not a repo file: for Claude Code add it to the project's `.mcp.json` (or the user's MCP config); for another harness (Kimi, Codex, …) add it to that harness's MCP configuration. When the user opts in, record it in `docs/agents/project.md` (a one-line "Library docs: Context7 MCP (preferred)" note) so the skills know to reach for it. This is a recommendation only — never block setup on it, and do not attempt to install or authenticate it yourself.
