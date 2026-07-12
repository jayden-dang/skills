# B02 — establish-project skill (tri-modal)

Covers: `[PROJDOC-1.1]` `[PROJDOC-1.3]` `[PROJDOC-1.4]` `[PROJDOC-2.1]` `[PROJDOC-2.3]` `[PROJDOC-7.1]` `[PROJDOC-8.3]`

**Scenario:** Create mode produces vision.md + spine + guidelines from templates via
grilling; update mode revises + routes hard decisions to the ADR gate + strikes retired
invariants; validate mode runs check-invariants. Skill is user-invoked, in
`skills/project/`.

**Walk (verify):**
- `skills/project/establish-project/SKILL.md` exists; frontmatter carries
  `disable-model-invocation: true`; located in the `project/` bucket `[PROJDOC-1.4]`. ✅
- Create mode fills `templates/product-vision.md` → `docs/product/vision.md`
  `[PROJDOC-1.1]`, the spine, and `docs/product/guidelines.md` `[PROJDOC-7.1]`, via
  `REQUIRED SUB-SKILL: grilling` `[PROJDOC-1.3]`. ✅
- Update mode revises + routes hard-to-reverse decisions to `domain-modeling`'s ADR gate
  and strikes retired invariants (never renumber) `[PROJDOC-2.1]`. ✅
- Validate mode walks the checklist and invokes `check-invariants` + `trace`
  `[PROJDOC-2.3]` `[PROJDOC-8.3]`. ✅
- Registered in `.claude-plugin/plugin.json` + AGENTS.md `project` bucket row. ✅

**Result:** PASS.
