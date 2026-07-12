# B09 — setup-repo opt-in, seed, migration

Covers: `[PROJDOC-5.1]` `[PROJDOC-5.2]` `[PROJDOC-5.4]` `[PROJDOC-7.4]`

**Scenario:** setup-repo offers decision G (project-docs layer, default No). Opting in
seeds vision/spine/guidelines, adds a project-docs line to `## Agent skills`, and offers
to migrate existing `project.md` guidelines into `guidelines.md`. Declining changes
nothing.

**Walk (verify):**
- Step 2 now walks **seven** decisions; decision **G. Project-docs layer** is added
  after F, default No `[PROJDOC-5.1]`. ✅
- Step 4 item 4: on opt-in, seed the three docs from templates (additive, never
  clobber); Agent-skills block gains the project-docs bullet (gated "only if G was Yes")
  `[PROJDOC-5.2]`. ✅
- Decision G offers to migrate existing guidelines into `guidelines.md`, leaving a
  pointer `[PROJDOC-7.4]`. ✅
- Declined → Step 4 item 4 writes none of the files; six→seven is the only wizard change,
  and no seeds are written → output otherwise identical `[PROJDOC-5.4]`. ✅

**Result:** PASS.
