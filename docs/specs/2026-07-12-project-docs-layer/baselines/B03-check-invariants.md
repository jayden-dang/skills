# B03 — check-invariants skill

Covers: `[PROJDOC-8.1]` `[PROJDOC-8.4]`

**Scenario:** Given a design citing `Respects: ARCH-2` and the spine,
`check-invariants` returns a per-citation verdict + rationale; it is model-invoked and
advisory (no pass/fail gate).

**Walk (verify):**
1. `skills/review/check-invariants/SKILL.md` exists; frontmatter is model-invoked (no
   `disable-model-invocation`), description states triggers + the verdict outcome. ✅
2. Body defines inputs (spine + design/diff), the per-citation judgment, and the
   verdict vocabulary `respects | violates | unclear` with rationale `[PROJDOC-8.1]`. ✅
3. Body states it is advisory, LLM-judged, and explicitly distinct from the
   deterministic `trace` check — never a hard gate `[PROJDOC-8.4]`. ✅
4. No-op branch: if `docs/architecture/` is absent, say so once and stop. ✅
5. Registered in `.claude-plugin/plugin.json` and the AGENTS.md review inventory. ✅

**Result:** PASS.
