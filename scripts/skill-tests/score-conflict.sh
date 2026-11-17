#!/bin/bash
# score-conflict.sh <fixture-dir> <start-sha> — merge state, history kept, both sides of auth.js kept
d="$1"; s="$2"; O=$(git -C "$d" remote get-url origin)
tip=$(git --git-dir "$O" rev-parse feat/booking)
echo "head moved: $([ "$tip" != "$s" ] && echo yes || echo no)  old head kept in history (no force-push): $(git --git-dir "$O" merge-base --is-ancestor "$s" "$tip" && echo yes || echo NO)"
echo "merge state: $(cd "$d" && HL_PENDING=0 bin/gh pr view --json mergeable,mergeStateStatus)"
echo "CI on tip: $(cd "$d" && HL_PENDING=0 bin/gh pr checks | cut -f1,2 | tr '\t\n' '= ')"
echo "auth.js METHODS on tip: $(git --git-dir "$O" show "$tip":src/http/auth.js | grep 'const METHODS')"
echo "DELETE route from main kept: $(git --git-dir "$O" show "$tip":src/routes/passengers.js | grep -c 'route("DELETE"')"
echo "origin main moved past the ACCT commit: $([ "$(git --git-dir "$O" log --oneline -1 main | cut -c9-)" ] && git --git-dir "$O" log --oneline -1 main | cut -c9-60)"
