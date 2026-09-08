# TESTS

## Length pass — 233 to 195 lines (2026-09-07, v2.0.1)

Patch: no new rule, no new evidence slot, no wording changed inside a block
relocated verbatim. `## 4. Explicit non-claims (refuse)` (the VFG-3.x table)
was left untouched, as were the `## Rationalizations` and `## Red Flags`
tables — both are Gate-bucket (`| Thought | Reality |` rows and Red Flags
bullets), never moved or thinned.

**What moved.** `## 6. Guide-gap fix loop` opened with its own skip predicate
("When the report has open missing-situation findings...") that was never
named in its own heading. The heading now stays, and the full step table plus
the `### Fixer subagent (when escalated)` subsection moved verbatim to
`references/guide-gap-loop.md`. `SKILL.md` keeps the heading, a one-line
summary naming every step (order by severity, patch run-file-only, re-vet
isolated, clear only via new report/named override, escalate at ≥5 findings
or ≥2 ability areas, cap at 2 cycles), the pointer, and the closing `*Done
when*` line.

`### Inline fallback (no subagents)` under `## 2. Isolation (mandatory)`
already named its skip predicate in the heading. Its body (the `AUTHORING
CLOSED` phrase and the load/forbidden instructions) moved verbatim to
`references/inline-fallback.md`. `SKILL.md` keeps the heading, the skip
condition ("WHEN no subagents are available"), a one-line summary of what the
fallback does, and the pointer — plus the section's existing `*Done when*`
line, which covers both the preferred and fallback paths and was left in
place.

**What was deleted as duplication.** Three passages restated a rule that
already has a canonical home elsewhere in the same file (or, after the move
above, in a sibling reachable only through the surviving pointer):

- `## 2` step 3, "Writing the **vet report** is allowed. Product code and the
  run file stay unmodified." restated the Iron Law line `REPORT WRITE ONLY —
  NEVER MUTATE PRODUCT CODE OR THE RUN FILE` (SKILL.md:27) and is echoed again
  in the new `## 6` pointer paragraph ("only the report gets written",
  SKILL.md:158). Surviving home confirmed by grep: SKILL.md:27.
- `### What does not keep the loop alive` (previously under `## 6`) restated
  the Rationalizations row `"Taste / polish feedback should keep the fix loop
  open"` → `"Non-code-grounded and taste items do not keep the loop alive."`
  (SKILL.md:179) verbatim in substance, plus VFG-3.1/3.3/3.4 in `## 4`.
  Surviving home confirmed by grep: SKILL.md:179 (exact phrase "keep the loop
  alive"); also restated compactly in the new `## 6` pointer paragraph
  (SKILL.md:156-157).
- `### Separation from judgment` (previously under `## 6`) restated "judgment
  stays read-only on product code and the run file; guide-gap patches are a
  separate loop" — already the Rationalizations row `"I'll patch the run file
  from inside the vet pass to clear findings"` → `"Judgment is read-only on
  the run file. Report only; guide-gap patches are a separate loop."`
  (SKILL.md:172), and restated again in `references/guide-gap-loop.md`'s own
  intro line and the `## 6` pointer paragraph. Surviving home confirmed by
  grep: SKILL.md:172.
- The Hygiene note's sentence "Never title that section 'complete for real
  users.'" restated the Red Flags bullet "Titling anything 'complete for real
  users' based on schema/kind counts" (SKILL.md:195). Trimmed to "...and is
  never this skill's product claim (see Red Flags)."; surviving home
  confirmed by grep: SKILL.md:195.

**Preservation.** `scripts/skill-rule-inventory.py --diff` over the old
`SKILL.md` against the new three-file set (`SKILL.md`,
`references/guide-gap-loop.md`, `references/inline-fallback.md`): 88 atoms at
HEAD, 89 across the three files now. 2 flagged "reworded rather than removed"
(the vet-report/product-code line and the "What does not keep the loop alive"
heading) — both read and confirmed as the same rule surviving in place, not a
shift. 1 flagged "no home" (`### Separation from judgment`) — confirmed above
as a deliberate duplicate deletion with its home named and grepped.

All `eval.json` contract anchors still resolve as literal substrings:
`SKILL.md § 2. Isolation (mandatory)` (SKILL.md:45, heading unchanged) and
`SKILL.md § 4. Explicit non-claims (refuse)` (SKILL.md:103, heading and body
untouched). `lint-skill-evals.py` and every other `scripts/lint-*.py` pass;
only `lint-skill-length.py` reports the expected "delete the budget entry"
message, left for the reviewer to clear with `--write` once the batch lands.

**Portability.** Both new sibling files (`references/guide-gap-loop.md`,
`references/inline-fallback.md`) sit one level deep beside `SKILL.md` inside
this skill's own `references/` directory, matching the existing
`judgment-brief.md` / `report-schema.md` convention already in this skill —
no cross-folder pointer into `run-flow-guide` or any other skill. Content
this skill's gate depends on (the Iron Law, the non-claims table, the
Rationalizations and Red Flags tables) stayed inline; only the two
conditional recipes moved.

**Not touched.** `## 1. Inputs`, `## 3. Implementation-surface map`, and
`## 5. Write the report` are Universal sections (every run reaches them) and
were left as-is beyond the one Hygiene-note trim above. The Iron Law,
Rationalizations, and Red Flags blocks were not touched at all — thinning any
of them was not needed to reach 195 lines.

### Reviewer note — a portability question this pass surfaced but did not answer

Checking whether anything here duplicated `run-flow-guide` turned up the reverse:
`run-flow-guide`'s hard gate points into this skill's `references/report-schema.md`
across a folder boundary. An audit of the whole set found nine such pointers, all
in the execution and ship families and all predating this pass:

- `build-by-story` and `build-in-waves` → `../execute-common/task-lifecycle.md`
- `build-by-story` and `build-inline` → `../build-in-waves/implementer-prompt.md`
- `build-by-story/story-unit-mode.md` → `../build-in-waves/task-reviewer-prompt.md`
- `land-branch` → `../../execution/execute-common/close-receipt.md`

`AGENTS.md` forbids the shape, and `npx skills add` copies one skill folder at a
time, so a consumer installing `build-inline` alone gets a pointer to a file that
is not there. But `execute-common` is deliberately the shared controller recipe
for three skills, so this is an architecture choice colliding with a portability
rule, not an accident anyone introduced.

Two ways out, and the choice belongs to whoever owns the set: write the exception
into `AGENTS.md` and say the execute family installs as a unit, or give each skill
its own copy and accept the drift risk that `story-unit-mode.md` already shows,
where two copies of one file have diverged. A length pass cannot pick.
