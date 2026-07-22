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
<!-- Task 2 appends here -->

## S-consumers
<!-- Task 3 appends here -->

## S-docs
<!-- Task 4 appends here -->

## Coverage
<!-- Task 5 fills full ID matrix -->
