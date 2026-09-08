# Guide-gap fix loop — vet-flow-guide

When the report has open missing-situation findings, the **controller** (or
author re-entry) runs this loop. Judgment itself stays read-only on the run
file — patches happen **outside** the vet pass, then a fresh re-check.

| Step | Owner | Rule |
|---|---|---|
| 1. Order | controller | Order open findings by severity: Critical → Important → Minor. Severity orders work only; it does not drop findings from the gate. |
| 2. Patch | controller or fixer | Patch the **run file only** (add/reshape cases, sections, authored slots). Re-render HTML via the write-flow-guide `render` path. **No product code patches** and no mid-drive invent-cases. |
| 3. Re-vet | always isolated | **IMMEDIATELY** after run-file patches (before dogfood, before “clean” claims): re-invoke `vet-flow-guide` in a **fresh isolated** pass (new subagent or new `AUTHORING CLOSED` pass). Set `pass_kind: re-check` and `prior_report` to the previous report path. The dogfood gate re-evaluates **only against the new report** — never the prior open list, never hand-edited “fixed” marks on the old report. |
| 4. Clear | gate / report | Clear a finding only when it is **absent from the new open list**, or when the user names it in an explicit **named override**. Never self-declare clean without a new report. Never rewrite the old report’s open list by hand and call that a re-check. |
| 5. Escalate | controller | IF open finding count is **≥ 5** OR the required rewrite spans **≥ 2 ability areas** (multi-section rewrite) THEN dispatch an **isolated fixer subagent**. |
| 6. Cap | controller | Cap at **2 re-judgment cycles**. IF 2 full re-judgment cycles complete with open findings still present THEN **stop for the human** (fix more, named override listing remaining `VFG-N`, or shrink surface) rather than thrashing. |

### Fixer subagent (when escalated)

Write brief to `.skills/<CODE>/vfg-fix-brief.md`:

- open finding set (`VFG-N`, severity, situation, evidence pointers)
- run-file path
- not full session history

Fixer patches the run file (+ re-render) only. Fixer must **not** self-declare
clean. After fixer DONE, controller always re-invokes fresh `vet-flow-guide`.
