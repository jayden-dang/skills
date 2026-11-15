#!/bin/bash
# make-fernhollow.sh <parent-dir> <skills-repo>   [FILING=draft]
# The evolve-system fixture (github tracker), with the tracker behind a local stateful bin/gh
# and the skill installed where a consuming repo keeps it.
set -euo pipefail
P="$1"; SK="$2"
python3 -I "$SK/skills/track/evolve-system/scripts/build_fixture.py" fernhollow "$P" >/dev/null
cd "$P/fernhollow"
mkdir -p bin .claude/skills
cp "$SK/scripts/skill-tests/gh-shim.py" bin/gh; chmod +x bin/gh
sed -i '' 's#quayside/billing#fernhollow-labs/fernhollow#g' bin/gh
python3 - "${FILING:-}" <<'PY'
import json, subprocess, sys
g = subprocess.run(["git", "rev-parse", "--git-dir"], capture_output=True, text=True).stdout.strip()
S = {"labels": ["status:inbox", "status:ready", "status:shaping", "bug", "enhancement"], "prs": [],
     "issues": [{"number": 41, "title": "Merchants want payout totals by week", "body": "## Problem\nFinance re-adds daily totals by hand.\n",
                 "state": "open", "labels": ["enhancement", "status:inbox"], "assignees": ["lan"], "comments": []}]}
json.dump(S, open(g + "/gh.json", "w"), indent=1)
row = ""
if sys.argv[1]:
    row = ("\n| Field | Values | Default |\n|---|---|---|\n"
           "| **Follow-up filing** | `%s` | `tracker` |\n" % sys.argv[1])
open("docs/agents/issue-tracker.md", "w").write("""# Issue tracker configuration (agent-facing)

**Tracker:** github (`github.com/fernhollow-labs/fernhollow`) — always through `bin/gh` (it carries the host and token for this repo).
%s
## Wayfinding operations

- List open issues: `bin/gh issue list --state open`
- Create: `bin/gh issue create --title <t> --body-file <f> --label <l> --assignee <login>`
- Read back: `bin/gh issue view <n>`
- Comment: `bin/gh issue comment <n> --body-file <f>`

## Issue format

**Body of a bug:** `## What happens`, `## Expected`, `## How to reproduce`, `## Evidence`.

**Body of anything else:**

```markdown
## Problem
## Outcome
## Acceptance
- [ ] Observable, and checkable on its own
## Out of scope
```

- **Assignee:** the requester (`lan`).
- **Status:** one category role and one state role from `triage-labels.md`; the state is `needs-triage` unless the requester named one.
""" % row)
open("docs/agents/triage-labels.md", "w").write("""# Triage label mapping (agent-facing)

| Canonical role | Label in this repo |
|---|---|
| needs-triage | `status:inbox` |
| shaping | `status:shaping` |
| ready-for-agent | `status:ready` |
| bug | `bug` |
| enhancement | `enhancement` |
""")
PY
cp -R "$SK/skills/track/evolve-system" .claude/skills/evolve-system
cp -R "$SK/skills/track/board" .claude/skills/board
rm -f .claude/skills/*/TESTS.md .claude/skills/*/eval.json .claude/skills/evolve-system/scripts/test_sense.py .claude/skills/evolve-system/scripts/build_fixture.py
printf '.claude/\nbin/\ndocs/agents/triage-labels.md\n' >> .git/info/exclude
git update-index --assume-unchanged docs/agents/issue-tracker.md
git rev-parse HEAD > .git/fixture-head
echo "$P/fernhollow"
