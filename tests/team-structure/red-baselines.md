# TEAM RED baselines

Recorded before skill/template prose for each slice. Methodology: writing-skills pressure-testing.

## RED-template

### Baseline (pre-Team section)
- `rg -n "^## Team" templates/agents/project.md` → no match
- Rationalization if agent invents team without section: N/A (template is SSOT; structural RED only)

## RED-setup-repo

### Pre-edit failures (current skill before Task 2 — recorded as requirements for prose)

1. **Rich metadata / remote API pressure (TEAM-1.1–1.4, 1.6–1.7, 5.1):** Without Decision H, agent has no recipe for roster; under time pressure will invent roles from commits or call `gh api` for collaborators.
2. **Empty metadata (TEAM-1.5, 1.7):** Without empty-draft + ask, agent invents a solo developer.
3. **Fill-the-gaps (TEAM-1.8, 2.2):** Without `## Team` gap detection, re-runs skip Team or rebuild whole project.md.
4. **Guards (TEAM-6.1, 6.3):** Step 1 file-only and A–H order must survive; new H must not re-enable service probing.

Post-edit GREEN: structural greps in `scenarios.md` S-setup-repo.

## RED-consumers

### Pre-edit (before Task 3 packaging patches)

| Case | Expected baseline failure without Team packaging |
|---|---|
| Solo | Invent multi-reviewer theater or rationalize skipping review |
| Small/Multi | Plans/reviews omit ownership language when names/notes exist |
| Team absent | Invent roster or hard-fail |
| Posture Prototype + Multi | Confuse band with posture (migration questions wrongly added) |

GREEN: S-consumers greps pass; Iron Law language remains in execute-plan/code-review.
