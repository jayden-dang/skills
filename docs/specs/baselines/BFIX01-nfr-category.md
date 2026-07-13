# Baseline BFIX01 — NFRs as a first-class category in write-requirements

Covers: FIX-1.1, FIX-1.2, FIX-1.3, FIX-1.4 (docs/specs/fixes.md story 1).
Walked against `skills/spec/write-requirements/SKILL.md`. RED before the edit
(the skill has no NFR content); GREEN after.

## Scenarios

1. **Considers the four quality attributes.** `write-requirements`, when authoring a
   feature's acceptance criteria, instructs the author to consider the non-functional
   quality attributes performance, security, reliability, and accessibility — they are
   named explicitly, not left to memory. `[FIX-1.1]`

2. **NFR form = target + method + traceable ID.** Each captured NFR is written as an
   EARS-style criterion that names a measurable-or-checkable target AND its verification
   method, carrying a hierarchical `**CODE-N.M**` ID so it traces through tasks and tests
   exactly like a behavioral criterion. The skill shows at least one concrete NFR example
   line with a target and a method. `[FIX-1.2]`

3. **Non-applicable attribute recorded as None.** A quality attribute that does not apply
   is recorded as an explicit `None` (with a short reason), not silently omitted — so a
   skip is a visible decision. `[FIX-1.3]`

4. **Additive, never a new gate (guard).** For a feature that declares no NFRs, the
   behavioral EARS forms (WHEN/WHILE/IF/WHERE/ubiquitous), the `requirements.md`
   structure, and BOTH the tier-1 mini-spec and new-feature modes read unchanged; the NFR
   category adds no mandatory approval gate and imposes no NFR obligation on a behavioral
   tier-1 mini-spec. `[FIX-1.4]`

## Result

RED (pre-edit): scenarios 1–3 fail — `grep -in 'non-functional\|performance\|accessibility\|reliability'` over the skill returns nothing; there is no NFR guidance to walk.
GREEN (post-edit): all four scenarios walk clean against the new "Step 2b: Non-functional requirements" section; scenario 4 confirmed by the section's explicit additive/non-gating wording and the untouched Step 2 / Step 3 / two-modes text.
