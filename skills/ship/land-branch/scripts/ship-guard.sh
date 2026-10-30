#!/usr/bin/env bash
# ship-guard.sh <base> [<tasks.md>] — what in <base>...HEAD should not cross unexamined.
#
# One tab-separated row per finding, then "# clean" or "# findings: N". Read-only.
#
#   lockfile     <path>  lockfile changed, no manifest beside it changed
#   generated    <path>  build/test output or a file marked generated
#   out-of-plan  <path>  changed, but in neither the plan's File Structure nor a task's
#                        **Files:** block (needs <tasks.md>)
#   behind-base  <n>     commits on <base> this branch does not have
set -euo pipefail
base="$1"; plan="${2:-}"
files="$(git diff --name-only "$base"...HEAD)"   # bash 3.2 (macOS) has no mapfile
n=0; flagged=""
row() { printf '%s\t%s\t%s\n' "$1" "$2" "$3"; n=$((n+1)); flagged="$flagged$2"$'\n'; }
changed() { grep -qxF -- "$1" <<< "$files"; }

while IFS= read -r f; do
  [[ -n "$f" ]] || continue
  d="$(dirname "$f")"; [[ "$d" == . ]] && p="" || p="$d/"
  case "$(basename "$f")" in
    bun.lock|bun.lockb|package-lock.json|npm-shrinkwrap.json|yarn.lock|pnpm-lock.yaml) m=package.json ;;
    Cargo.lock) m=Cargo.toml ;;  go.sum) m=go.mod ;;  poetry.lock|uv.lock|Pipfile.lock) m=pyproject.toml ;;
    Gemfile.lock) m=Gemfile ;;  composer.lock) m=composer.json ;;  *) m="" ;;
  esac
  [[ -n "$m" ]] && ! changed "$p$m" && row lockfile "$f" "no change to $p$m"

  gen=""
  [[ "/$f" =~ /(coverage|dist|build|out|target|node_modules|\.next|__generated__|generated)/ ]] && gen="path"
  [[ "$f" =~ \.(min\.js|min\.css|map)$ || "$(basename "$f")" == lcov.info ]] && gen="name"
  [[ -z "$gen" && "$(git check-attr linguist-generated -- "$f" | awk '{print $NF}')" == true ]] && gen=".gitattributes"
  if [[ -z "$gen" ]] && git cat-file -e "HEAD:$f" 2>/dev/null; then
    git show "HEAD:$f" 2>/dev/null | head -5 | grep -qiE '@generated|do not edit|code generated' && gen="header"
  fi
  [[ -n "$gen" ]] && row generated "$f" "$gen"
done <<< "$files"

if [[ -n "$plan" && -f "$plan" ]]; then
  # no match must not end the script: grep exits 1 under pipefail when the plan lists no paths
  planned="$( { sed -n '/^## File Structure/,/^---/p' "$plan"
                sed -n '/^\*\*Files:\*\*/,/^$/p' "$plan"; } | { grep -oE '`[^`]+`' || true; } | tr -d '`')"
  plandir="$(dirname "$plan")"; specs="$(dirname "$plandir")"
  code=""   # a plan with no requirements.md beside it has no code, so no registry exemption
  [[ -f "$plandir/requirements.md" ]] && code="$(sed -n 's/^Feature code:[[:space:]]*\([A-Z][A-Z0-9]*\).*/\1/p' "$plandir/requirements.md" | head -1)"
  # a registry file (spec INDEX, catalog shard) is the feature's own when every changed line is its row
  own_row() {
    [[ -n "$code" && ( "$1" == "$specs/INDEX.md" || "$1" == "$specs"/catalog/*.md ) ]] || return 1
    # no -q: an early exit would SIGPIPE git diff and, under pipefail, exempt the file by mistake
    [[ -z "$(git diff -U0 "$base"...HEAD -- "$1" | { grep -E '^[+-]' || true; } \
             | { grep -vE '^(\+\+\+|---) ' || true; } | { grep -vF "| $code |" || true; })" ]]
  }
  if [[ -z "$planned" ]]; then
    echo "# out-of-plan not checked: $plan lists no File Structure or Files paths"
  else
    while IFS= read -r f; do
      [[ -n "$f" && "$f" != "$plandir"/* ]] || continue
      grep -qxF -- "$f" <<< "$flagged" && continue      # already reported as lockfile/generated
      own_row "$f" && continue
      grep -qxF -- "$f" <<< "$planned" || row out-of-plan "$f" "not in $plan File Structure or Files blocks"
    done <<< "$files"
  fi
fi

behind="$(git rev-list --count HEAD.."$base")"
[[ "$behind" -gt 0 ]] && row behind-base "$behind" "$base has $behind commit(s) this branch lacks"
[[ $n -eq 0 ]] && echo "# clean" || echo "# findings: $n"
