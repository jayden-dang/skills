# B10 — scaffold-project seed

Covers: `[PROJDOC-5.3]`

**Scenario:** On a greenfield scaffold with the layer opted in, Step 2.8 seeds
vision/spine/guidelines beside CONTEXT.md and docs/specs/INDEX.md; not opted in, it seeds
neither.

**Walk (verify):**
- `scaffold-project/SKILL.md` item 8 (Docs seeds): offers the optional project-docs layer
  once; on opt-in, seeds `docs/product/vision.md`, `docs/architecture/INDEX.md`, and
  `docs/product/guidelines.md` from templates, alongside the existing CONTEXT.md /
  docs/specs/INDEX.md seeds `[PROJDOC-5.3]`. ✅
- Declined → "seed none of these"; the setup-repo handoff (decision G) can still enable it. ✅

**Result:** PASS.
