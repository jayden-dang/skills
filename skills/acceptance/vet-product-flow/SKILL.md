---
name: vet-product-flow
description: >-
  Use when a review-product-flow run file (`.skills/<CODE>/review-product-flow.json`)
  already exists and needs an isolated implementation-surface judgment / missing-situation
  map before agent dogfood or run-product-walkthrough — producing
  `.skills/<CODE>/vet-product-flow.md` with code-grounded findings. Triggers on “vet
  the guide”, “missing situations”, “guide complete for the implementation?”,
  “re-vet after guide gaps”, or hand-off after authoring when isolation is
  required. Not for authoring cases (`review-product-flow`) or driving cases
  (`run-product-walkthrough`).
---

# Vet Product Flow

Map the **implemented** user-observable product surface against cases in a
review-product-flow run file. Write a findings report. Stay **read-only** on
product code and the run file. This is judgment, not an ARCH-1 vertical check
and not a substitute for dogfood.

## The Iron Law

```
JUDGMENT IS ISOLATED — NOT A LONGER SAME-SESSION §4 SELF-CHECK
FINDINGS ARE CODE-GROUNDED — NO UNINSPECTED SURFACES
REPORT WRITE ONLY — NEVER MUTATE PRODUCT CODE OR THE RUN FILE
PATCHED CASES ARE NOT CLEAN UNTIL A NEW REPORT SAYS SO
```

## 1. Inputs

Require a **run-file path** (`.skills/<CODE>/review-product-flow.json`). Load
JSON. If missing or invalid, refuse and point the caller back to
`review-product-flow` — do not invent cases.

Optional triad (for OOS / persist claims only, never as a substitute for
opening product code on implementation claims):

- `docs/specs/<feature>/requirements.md`
- `design.md` / `tasks.md` when present

*Done when: run file is loaded or the pass refuses with a clear pointer.*

## 2. Isolation (mandatory)

Perform the judgment pass in a **fresh isolated** context. Never as a longer
same-session §4 self-check after authoring, and never by self-clearing findings
without a new report.

### Preferred: read-only subagent

1. Fill `references/judgment-brief.md` with run path, optional triad paths,
   report path, product paths from design/tasks/known layout, and read-only
   rules.
2. Dispatch a **read-only** subagent. The subagent runs the map (step 3) and
   writes the report (step 5), or returns full report text for the controller
   to write **verbatim** — the controller does not re-judge content.
3. Writing the **vet report** is allowed. Product code and the run file stay
   unmodified.

### Inline fallback (no subagents)

State out loud:

```
AUTHORING CLOSED — starting isolated vet-product-flow pass
```

Load only the brief inputs. Run steps 3–5. Forbidden: continuing from open
case-authoring todos, “just also count kinds,” or declaring clean without a
report file.

*Done when: isolation mode is stated and the map runs outside open authoring.*

## 3. Implementation-surface map (product claim)

This skill’s product claim is an **implementation-surface map**, not authoring
hygiene counts.

1. Enumerate **user-observable** paths and states from **opened** product code:
   routes, primary actions, empty/error/role UI the code actually renders, and
   other UI-exposed states. Skip internal branches, helpers, and service
   conditionals that never surface to a user.
2. For each surface, search the run file for a corresponding case (setup / try /
   expect / kind — judgment match, not string equality only).
3. When a shipped user-observable path or state has no corresponding case
   (including non-happy paths real use can hit on that surface), emit a
   **missing-situation** finding with:
   - stable `surface_key`
   - severity (`Critical` / `Important` / `Minor`) — **orders the fix loop
     only**; severity does **not** soften or clear the dogfood gate
   - situation prose
   - **evidence**: file / symbol / route / state pointers the reviewer
     **opened** (and/or triad when the claim is spec / Out-of-Scope / persist)
4. IF code for a candidate surface was **not inspected**, THEN do **not** assert
   that surface as a missing-situation finding. Skip uninspected candidates.
5. Do not emit non-claim categories (step 4).

### Hygiene note (optional, non-blocking)

May list author §1 hygiene observations (requirement-ID coverage, non-happy
kinds, schema/kind/status) under a **separate** report section that does **not**
create open missing-situation findings and does **not** affect the dogfood
gate. Never title that section “complete for real users.” Mechanical
schema/kind/status passes are **not** this skill’s product claim.

*Done when: every inspected surface is matched or filed; uninspected surfaces
are omitted.*

## 4. Explicit non-claims (refuse)

Do **not**:

| Non-claim | Refuse |
|---|---|
| **VPF-3.1** Novelty / feel / visual-polish taste | Not pass/fail outcomes of this skill |
| **VPF-3.2** Chaos / load / race / security-fuzz suites | Do not require or invent them in guide or report |
| **VPF-3.3** Speculative design | “Users will want X” / “the product should do X” when X is not already on the shipped user-observable surface |
| **VPF-3.4** Global stamps | “Good UX”, “complete for real users”, “ready to ship” |
| **VPF-3.5** Dogfood ownership | No drive-app pass/fail; no FE+BE (`saw`/`server`) evidence ownership inside this skill |

This skill does **not** replace dogfood (`run-product-walkthrough`).

*Done when: report and prose contain only code-grounded missing-situation
findings (plus optional non-blocking hygiene notes).*

## 5. Write the report

Write `.skills/<CODE>/vet-product-flow.md` per
`references/report-schema.md`. Required stamp fields:

| Field | Role |
|---|---|
| `slug` | Run slug |
| `run_file` | Path to the JSON run file |
| `cases_fingerprint` | SHA-256 of authored cases (schema recipe) |
| `stamped_at` | ISO-8601 UTC |
| `pass_kind` | `initial` \| `re-check` |
| `prior_report` | Previous report path on re-check, or `—` |
| `open_count` | Open missing-situation count |
| `gate_hint` | `clean` if open_count=0 else `blocked` |

Finding blocks use integer ids **`VPF-N`** (never criterion shape `VPF-N.M`).
Each open finding carries `surface_key`, severity, situation, evidence.

On **re-check**: still-open same `surface_key` **reuses** the same `VPF-N`; new
misses get the next free integer; resolved misses move to `## Cleared this pass`
(open list is authoritative for the gate).

Report write is allowed. Product codebase and the run file remain **unmodified**
during judgment (read-only).

Exit by handing report path + `open_count` to the caller (author fix loop or
walkthrough gate).

*Done when: report exists on disk with stamp fields and open findings list.*

## 6. Guide-gap fix loop

When the report has open missing-situation findings, the **controller** (or
author re-entry) runs this loop. Judgment itself stays read-only on the run
file — patches happen **outside** the vet pass, then a fresh re-check.

| Step | Owner | Rule |
|---|---|---|
| 1. Order | controller | Order open findings by severity: Critical → Important → Minor. Severity orders work only; it does not drop findings from the gate. |
| 2. Patch | controller or fixer | Patch the **run file only** (add/reshape cases, sections, authored slots). Re-render HTML via the review-product-flow `render` path. **No product code patches** and no mid-drive invent-cases. |
| 3. Re-vet | always isolated | **IMMEDIATELY** after run-file patches (before dogfood, before “clean” claims): re-invoke `vet-product-flow` in a **fresh isolated** pass (new subagent or new `AUTHORING CLOSED` pass). Set `pass_kind: re-check` and `prior_report` to the previous report path. The dogfood gate re-evaluates **only against the new report** — never the prior open list, never hand-edited “fixed” marks on the old report. |
| 4. Clear | gate / report | Clear a finding only when it is **absent from the new open list**, or when the user names it in an explicit **named override**. Never self-declare clean without a new report. Never rewrite the old report’s open list by hand and call that a re-check. |
| 5. Escalate | controller | IF open finding count is **≥ 5** OR the required rewrite spans **≥ 2 ability areas** (multi-section rewrite) THEN dispatch an **isolated fixer subagent**. |
| 6. Cap | controller | Cap at **2 re-judgment cycles**. IF 2 full re-judgment cycles complete with open findings still present THEN **stop for the human** (fix more, named override listing remaining `VPF-N`, or shrink surface) rather than thrashing. |

### Fixer subagent (when escalated)

Write brief to `.skills/<CODE>/vpf-fix-brief.md`:

- open finding set (`VPF-N`, severity, situation, evidence pointers)
- run-file path
- not full session history

Fixer patches the run file (+ re-render) only. Fixer must **not** self-declare
clean. After fixer DONE, controller always re-invokes fresh `vet-product-flow`.

### What does not keep the loop alive

Non-code-grounded items, taste (novelty / feel / polish), and anything outside
the skill claim **do not keep the fix loop alive** as if they were
missing-situation findings. Drop or refuse them; only code-grounded open
findings drive patch → re-vet.

### Separation from judgment

During judgment the product codebase and run file remain unmodified (read-only);
report write only. Guide-gap patches are a **separate** controller loop after a
report exists — never inside the map/write steps above.

*Done when: open findings are fixed and re-checked clean, named-overridden, or
stopped for the human after 2 re-judgment cycles.*

## Rationalizations

| Thought | Reality |
|---|---|
| “I just authored the cases — §4 already counted kinds” | Same-session self-check is not isolation. Fresh subagent or `AUTHORING CLOSED` pass only. |
| “CLI / schema / kind counts prove the guide is complete for real users” | Mechanical hygiene is not the product claim. Map shipped user-observable surfaces; never sell false confidence. |
| “I’ll invent chaos/load/race/fuzz cases so the guide is thorough” | Explicit non-claim. Do not require or invent those suites. |
| “Users will want X even though the code doesn’t show it yet” | Speculative design is out. Only surfaces the implementation already exposes. |
| “Stamp ‘ready to ship’ / ‘good UX’ so stakeholders can move on” | Global stamps are forbidden. Report findings, not product verdicts. |
| “I’ll patch the run file from inside the vet pass to clear findings” | Judgment is read-only on the run file. Report only; guide-gap patches are a separate loop. |
| “Minor findings can soft-pass the dogfood gate” | Severity orders the fix loop only; every open finding blocks until fixed or named-overridden. |
| “I fixed the cases — declare clean without re-vet” | Never self-declare. Re-invoke fresh isolated vet-product-flow; gate uses the new report only. |
| “I hand-edited the old report to mark findings fixed” | That is not a re-check. Only a new report (or named override) clears open findings. |
| “Author and vet in parallel in one stream — faster” | Hybrid same-session author+vet is not isolation. Close authoring first. |
| “Five small misses — keep patching in this long context” | ≥ 5 open findings or ≥ 2 ability areas → isolated fixer subagent with findings + run path brief. |
| “Third re-vet will clear it” | Cap is 2 re-judgment cycles; then stop for the human. |
| “Taste / polish feedback should keep the fix loop open” | Non-code-grounded and taste items do not keep the loop alive. |
| “Dogfood will find gaps mid-run — skip the isolated pass” | Mid-run plan writing is the failure this skill exists to prevent. Vet first. |

## Red Flags — stop and restart isolation

- Extending authoring todos into “also vet” without `AUTHORING CLOSED` or a subagent
- Declaring clean without a report file on disk
- Hand-editing an old report’s open list instead of writing a new re-check report
- Hybrid same-session authoring + “vet complete” chat with no report path
- Asserting a surface never opened in this pass
- Writing product code or mutating the run file during judgment
- Titling anything “complete for real users” based on schema/kind counts
- Owning browser drive or FE+BE evidence inside this skill
- Self-clearing findings without a new re-check report
- Patching product code to “close” a guide gap
- Third+ re-judgment cycle without stopping for the human
- Skipping vet because dogfood “will find gaps mid-run”
