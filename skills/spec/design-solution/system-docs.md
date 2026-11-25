# Optional system docs — consult recipe

**Load:** `skills/project/define-project/consult-recipe.md` (authority, hard-constraint
precedence, no-op, once-per-entry suggest, never auto-invoke).

| When the design… | Consult if Approved | Cite as |
|---|---|---|
| Crosses trust / compliance | `docs/security/threat-model.md`, `compliance.md`, `posture.md` | optional `Security:` TB/THR/CMP only — never on `Respects:` |
| Sets reliability targets | `docs/ops/reliability.md` | optional `Reliability:` SLO only |
| Touches API/UI/a11y/security-coding/instrumentation | matching `docs/standards/<name>.md` | design constraints prose |
| Needs system/data/integrations/runtime shape | `docs/architecture/{system,data,integrations,runtime}.md` | narrative; spine ARCH-N stays `Respects:` only |
| Names cross-module structure | `docs/codebase/{modules,ownership,dependencies}.md` | Locality / Reuse guidance |

Do not invent TB/THR/CMP/SLO numbers without bold definitions in Approved docs. Shape docs
never redefine ARCH-N. Suggest `/define-project <entry-key>` only when the gap is material.

When the design changes how a cited material commitment is met, name the
existing check to rerun and the observable result it must show. Record an
unproven assumption or missing check in the affected section of the design.
