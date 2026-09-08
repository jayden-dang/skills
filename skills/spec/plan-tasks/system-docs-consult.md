# System docs consult during File Structure (optional)

**Load:** `skills/project/define-system-doc/consult-recipe.md` (one home for authority,
hard-constraint precedence, no-op, once-per-entry suggest, never auto-invoke).

**Applicability:** this step writes or revises File Structure / path placement.

| Entry | Path | Use when Approved |
|---|---|---|
| `codebase/map` | `docs/codebase/map.md` | Layout and placement rules |
| `codebase/modules` | `docs/codebase/modules.md` | Module boundary placement |
| `codebase/ownership` | `docs/codebase/ownership.md` | Ownership notes (advisory, not authz) |
| `codebase/dependencies` | `docs/codebase/dependencies.md` | Forbidden dependency directions |
| `standards/INDEX` / `testing` / `errors-logging` | `docs/standards/…` | Global Constraints house rules (prefer standards over guidelines) |

**When Approved:** align the plan **within** hard constraints from consult-recipe;
note which docs were consulted. **Conflict** with a hard constraint → surface, keep
hard constraint, suggest `/define-system-doc <entry-key>`.

**When absent / non-authoritative:** CONTINUE (no-op). Suggest only when the gap is
material. Standards fallback chain stays: `docs/standards/` → legacy guidelines →
`docs/agents/project.md`.
