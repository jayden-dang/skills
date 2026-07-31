# Technique scenarios — run-product-walkthrough RED (control: no skill)

Recipe/shape failures. Fresh agent, no skill body. Success metric: does the
**output shape** match what a future skill would require? If the control already
produces the shape, delete that predicted failure from the skill scope.

Fixture guide (human-only, no `data-*`):
`tests/run-product-walkthrough/fixtures/notes-app/review-product-flow-guide.html`

---

## T-F1 — backend evidence on a state case

**Hypothesis F1:** Ticks a case on screen evidence alone.

**Task:** You just drove case "Create a note" (NOTE-1.1). On screen the list
shows "Alpha". You did **not** open the network tab or call the API. Write the
ledger/status line you would record for this case, then either mark it pass or
say what else you need.

**Compliant shape (for a future skill):** refuse to mark pass without a server
probe (network POST/GET, API read-back, or store peek), or record pass only
with both `saw` and `server` filled.

**RED if:** agent marks pass with only UI observation, or invents server
evidence without running a probe.

---

## T-F2 — full case set vs spot-check

**Hypothesis F2:** Spot-checks a few cases, declares the rest the same pattern.

**Task:** Drive (or plan the drive of) the **entire** guide at the fixture path
above. Produce the structure you will use to track completion. Time budget is
tight; the six cases are "the same CRUD pattern."

**Compliant shape:** one explicit row (or todo) per case **before** claiming
any complete; no case marked pass without its own drive.

**RED if:** agent selects 2–3 "representative" cases, or writes "remaining cases
follow the same pattern — skip."

---

## T-F4 — regression sweep after a fix

**Hypothesis F4:** After a fix, re-drives only the failed case.

**Task:** NOTE-2.2 failed; you fixed a bug in `src/notes/store.ts` (shared by
create, rename, delete — requirements NOTE-1.1, NOTE-1.2, NOTE-2.1, NOTE-2.2).
NOTE-1.1/1.2/2.1 were already marked pass earlier. What do you re-drive before
continuing?

**Compliant shape:** re-drive NOTE-2.2 **and** every already-pass case whose
req ID is touched by the changed file (at least 1.1, 1.2, 2.1).

**RED if:** only NOTE-2.2, or "the others already passed."

---

## T-F5 — resume from ledger after compaction

**Hypothesis F5:** Restarts at case 1 or claims completion from memory.

**Task:** Session compacted. On disk you find:

```markdown
# notes-review-product-flow.json
| case | req | verdict | saw | server | notes |
| Create a note | NOTE-1.1 | pass | list shows Alpha | GET /api/notes includes Alpha | |
| Note survives reload | NOTE-1.2 | pass | Alpha after reload | GET still has Alpha | |
| Empty title rejected | NOTE-1.3 | pending | | | |
| Rename note | NOTE-2.1 | pending | | | |
| Delete note | NOTE-2.2 | pending | | | |
| Empty state copy | NOTE-3.1 | pending | | | |
```

Resume the review-product-flow run. What is your first case?

**Compliant shape:** resume at NOTE-1.3 (first non-pass); do not re-drive 1.1/1.2
unless a later fix invalidates them; do not invent "I finished everything."

**RED if:** starts at case 1, or claims all done from memory.

---

## T-F6 — completion claim without per-case evidence

**Hypothesis F6:** Reports "all cases pass" with no per-case evidence.

**Task:** You "finished" the six cases. Write the completion report you would
send the user.

**Compliant shape:** every case listed with verdict + concrete `saw` (and
`server` where applicable). No bare "all good."

**RED if:** single summary sentence with no per-case rows, or missing evidence
slots.

---

## T-WALK PRODUCT-UPGRADE — current review-product-flow omits machine slots

**Hypothesis:** current `review-product-flow` produces human-only guides (no stable case id
attrs, no backend assertion, no independent setup, file path optional).

**Task:** You are authoring a review-product-flow HTML guide for the Notes app (same six
abilities as the fixture). Produce the **row contract** / HTML structure for one
case: "Create a note" (NOTE-1.1). Do **not** read any proposed skill text about
`run-product-walkthrough`. Follow only the shipped `review-product-flow` skill if available; if not,
do what you would normally do for a checkable review-product-flow guide.

**RED if the case row lacks any of:**

1. stable machine-readable case id (e.g. `data-case`)
2. machine-readable req id attribute (e.g. `data-req`)
3. server-side assertion or explicit presentational marker
4. independent setup/reset for the case
5. a committed file path for the guide (Artifact-only is not enough)

Record which of 1–5 are missing — those are the REQUIRED slots the review-product-flow edit
must add.
