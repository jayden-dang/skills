# B01 — Doc templates

Covers: `[PROJDOC-1.2]` `[PROJDOC-1.5]` `[PROJDOC-2.2]`

**Scenario:** Filling each template yields a well-formed vision / spine / guidelines
doc; the architecture template shows the ARCH-N grammar and a per-domain layout.

**Walk (verify):**
1. `templates/product-vision.md` exists with REQUIRED slots: Problem, Users, Goals,
   Non-goals, Scope boundaries. ✅
2. `templates/architecture-INDEX.md` defines the `**ARCH-N**` grammar (bold ID + one
   imperative sentence), a per-domain split under "Domains" `[PROJDOC-1.5]`, and the
   strikethrough retirement rule `~~**ARCH-N**~~ superseded by ARCH-M` `[PROJDOC-2.2]`. ✅
3. `templates/product-guidelines.md` exists with slots: Coding standards, Naming and
   i18n, House rules. ✅
4. Every heading is a fill-or-`None` REQUIRED slot, matching the existing `templates/`
   convention (`templates/requirements.md`). ✅

**Result:** PASS — the three templates back the vision, spine (`[PROJDOC-1.2]`), and
guidelines docs; ARCH grammar and retirement are specified in the spine template.
