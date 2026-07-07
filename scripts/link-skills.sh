#!/usr/bin/env bash
# Dev install: symlink every skill folder into ~/.claude/skills so `git pull`
# keeps installed skills current.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="${HOME}/.claude/skills"
mkdir -p "$TARGET"

count=0
for skill in "$REPO_ROOT"/skills/*/*/; do
  name="$(basename "$skill")"
  ln -sfn "${skill%/}" "$TARGET/$name"
  count=$((count + 1))
done

echo "Linked $count skills into $TARGET"
