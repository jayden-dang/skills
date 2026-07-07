#!/usr/bin/env bash
# SessionStart hook: inject the using-skills gate into every session so the
# skill-check rule survives /clear and context compaction.
set -euo pipefail

ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
SKILL_FILE="$ROOT/skills/meta/using-skills/SKILL.md"

if [ ! -f "$SKILL_FILE" ]; then
  exit 0
fi

node -e '
const fs = require("fs");
const text = fs.readFileSync(process.argv[1], "utf8");
const context =
  "<IMPORTANT>\nYou have a lifecycle skill set installed.\n" +
  "Below is the full content of the skills:using-skills skill — your introduction to using skills. " +
  "For all other skills, use the Skill tool:\n\n" + text + "\n</IMPORTANT>";
process.stdout.write(JSON.stringify({
  hookSpecificOutput: {
    hookEventName: "SessionStart",
    additionalContext: context,
  },
}));
' "$SKILL_FILE"
