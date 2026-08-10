#!/usr/bin/env bash
#
# Install a skill pack into every agent skill store present on this machine.
#
#   Claude Code   ~/.claude/skills/<name>      symlink   live — repo edits apply at once
#   Codex CLI     ~/.agents/skills/<name>      copy      re-run after editing a skill
#   Kimi          ~/.kimi-code/skills/<name>   copy      re-run after editing a skill
#
# Why Codex gets copies rather than a symlink: it resolves skills from
# <project>/.agents/skills, then $CODEX_HOME/skills (deprecated), then $HOME/.agents/skills,
# then its own system cache — and it does not follow symlinked skill directories. Verified on
# codex-cli 0.147.0: a symlinked skill was absent from the list, and the same skill copied in
# was found. Kimi is given copies for the same reason, untested.
#
# opencode has no skills mechanism (it exposes `agent` and `plugin`); it reads AGENTS.md
# instead, so nothing is installed for it here.
#
# Usage:
#   scripts/install-skills.sh fluency
#   scripts/install-skills.sh personal engineer
#   scripts/install-skills.sh all
#
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENGINEER_CATS="meta discovery spec execution review acceptance craft ship track project setup"

# store:mode — only stores whose parent already exists are used, so this never invents a
# config directory for an agent that is not installed.
STORES=(
  "$HOME/.claude/skills:link"
  "$HOME/.agents/skills:copy"
  "$HOME/.kimi-code/skills:copy"
)

pack_dirs() {
  case "$1" in
    fluency)  printf '%s\n' "$REPO"/skills/fluency/*/ ;;
    personal) printf '%s\n' "$REPO"/skills/personal/*/ ;;
    engineer) for c in $ENGINEER_CATS; do printf '%s\n' "$REPO"/skills/"$c"/*/; done ;;
    *) echo "unknown pack: $1 (want fluency, personal, engineer, or all)" >&2; return 1 ;;
  esac
}

[ $# -gt 0 ] || { sed -n '3,24p' "$0" | sed 's/^# \{0,1\}//'; exit 1; }
packs=("$@"); [ "${packs[0]}" = "all" ] && packs=(fluency personal engineer)

for entry in "${STORES[@]}"; do
  dest="${entry%:*}"; mode="${entry##*:}"
  if [ ! -d "$(dirname "$dest")" ]; then
    printf 'skip   %-28s (agent not installed)\n' "$dest"; continue
  fi
  mkdir -p "$dest"
  for pack in "${packs[@]}"; do
    n=0
    while IFS= read -r d; do
      [ -f "$d/SKILL.md" ] || continue
      name="$(basename "$d")"; src="${d%/}"
      case "$mode" in
        link) ln -sfn "$src" "$dest/$name" ;;
        copy) rm -rf "$dest/$name"; cp -R "$src" "$dest/$name" ;;
      esac
      n=$((n + 1))
    done < <(pack_dirs "$pack")
    printf '%-6s %-28s %2d skills (%s)\n' "$pack" "$dest" "$n" "$mode"
  done
done

echo
echo "Claude Code reads the repo through a symlink and needs no re-run."
echo "Copy-based stores hold a snapshot — re-run this script after editing a skill."
