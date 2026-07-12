# B07 — write-plan constraint sourcing + guidelines split

Covers: `[PROJDOC-4.4]` `[PROJDOC-7.2]` `[PROJDOC-7.3]` `[PROJDOC-7.5]`

**Scenario:** With a spine + `guidelines.md` present, write-plan's Global Constraints
include the spine's hard rules and read engineering rules from `guidelines.md`; with
neither, it reads from `project.md` as today. The `project.md` template frames itself as
machine-config and points to `guidelines.md`.

**Walk (verify):**
- `write-plan/SKILL.md` Step 1: `WHERE docs/architecture/ spine exists` folds ARCH-N
  hard rules into Global Constraints `[PROJDOC-4.4]`. ✅
- Same clause sources engineering rules from `docs/product/guidelines.md` when present
  `[PROJDOC-7.2]`, else `docs/agents/project.md` `[PROJDOC-7.5]`. ✅
- `templates/agents/project.md` header reframed as machine-config with a pointer to
  `docs/product/guidelines.md`, and Paths lists the layer docs `[PROJDOC-7.3]`. ✅
- No-op: absent spine/guidelines → sourcing is exactly today's (design + project.md). ✅

**Result:** PASS.
