# TEAM structural and scenario checks

Coverage annotations use greppable `TEAM-N.M` tokens so `trace` can find them under `tests/`.

## S-template

### S-TEAM-2.1 template has ## Team
<!-- TEAM-2.1 TEAM-2.3 TEAM-2.4 TEAM-2.6 -->

Assert `templates/agents/project.md` contains:

- heading `## Team` after `## Project posture` and before `## Verify commands`
- `### Roster` with Role — Name | N × Role guidance
- suggested roles list: Tech Lead, Backend Engineer, Frontend Engineer, Full-stack Engineer, Designer, Product Manager, QA, DevOps/SRE, Docs
- `### Ownership notes`
- `### Workflow band` with override + derive precedence (SSOT; no “copy into consumers”)
- **packaging matrix** table for Solo / Small / Multi / (no band)

```bash
rg -n "^## Team|^### Roster|Workflow band|packaging|Solo|Small|Multi" templates/agents/project.md
# expect: ## Team present between Project posture and Verify commands
```

**Pass when:** all bullets above are present; band rules are SSOT (no instruction to re-copy into skills).

## S-setup-repo

### S-TEAM-1.x Decision H and inference
<!-- TEAM-1.1 TEAM-1.2 TEAM-1.3 TEAM-1.4 TEAM-1.5 TEAM-1.6 TEAM-1.7 TEAM-1.8 TEAM-2.2 TEAM-2.5 TEAM-5.1 TEAM-6.1 TEAM-6.3 -->

Assert `skills/setup/setup-repo/SKILL.md`:

- `### H. Team` after posture; `### I. Project-docs` (not Team as I)
- pointer to load `team-inference.md` when Decision H runs
- Step 1 gap detection for missing `## Team`
- Step 3 draft includes confirmed Team; Step 4 fills Team then decision I project-docs
- Agent-skills bullet for Team composition / `## Team`
- description keywords: team, CODEOWNERS, contributors, roster
- nine decisions A–I; Step-1 still file-only (no service probe)

Assert `skills/setup/setup-repo/team-inference.md`:

- local git shortlog / 12-month window / top 10 / bot drop
- CODEOWNERS → Ownership notes (all tokens) vs human Roster only
- confirm gate; forbidden collaborator APIs
- no invent titles from commit volume

```bash
rg -n "### H\. Team|### I\. Project-docs|team-inference|Team composition|nine decisions" skills/setup/setup-repo/SKILL.md
rg -n "CODEOWNERS|confirm|Forbidden|shortlog|top 10" skills/setup/setup-repo/team-inference.md
```

**Pass when:** all greps match; no `### H. Project-docs`.

## S-consumers

### S-TEAM-3.x packaging conditionals
<!-- TEAM-3.1 TEAM-3.2 TEAM-3.3 TEAM-3.4 TEAM-3.5 TEAM-3.6 TEAM-6.2 TEAM-6.4 -->

Each skill must mention `## Team` (or team band/packaging) and not invent a team when absent:

- `skills/discovery/brainstorm/SKILL.md`
- `skills/discovery/grilling/SKILL.md` (posture orthogonal; additive Small/Multi probes)
- `skills/spec/write-plan/SKILL.md` (optional freeform notes only)
- `skills/execution/execute-plan/SKILL.md` (load band; dual review never skipped)
- `skills/review/code-review/SKILL.md`
- `skills/ship/finish-branch/SKILL.md` (Option 2 PR packaging)
- `skills/track/handoff/SKILL.md` (Team context content line)

```bash
for f in skills/discovery/brainstorm/SKILL.md skills/discovery/grilling/SKILL.md \
  skills/spec/write-plan/SKILL.md skills/execution/execute-plan/SKILL.md \
  skills/review/code-review/SKILL.md skills/ship/finish-branch/SKILL.md \
  skills/track/handoff/SKILL.md; do
  rg -q "Team|packaging|band" "$f" || echo "MISS $f"
done
```

**Pass when:** zero MISS; execute-plan still requires dual-verdict language; no skill requires a new Owner task field.

## S-docs
<!-- Task 4 appends here -->

## Coverage
<!-- Task 5 fills full ID matrix -->
