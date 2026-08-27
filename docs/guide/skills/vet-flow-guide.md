# `vet-flow-guide`

> Isolated judgment of a finished write-flow-guide run file against the **shipped** user-observable product surface. The deliverable is a **vet report** — code-grounded missing-situation findings with an authored-cases fingerprint — not a dogfood drive and not a mechanical schema/kind count.

|  |  |
|---|---|
| **Bucket** | acceptance |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | `.skills/<slug>-flow-guide.json` (run file); optional triad for OOS/persist claims; opened product code for surface map |
| **Writes** | `.skills/<slug>-vet-flow-guide.md` (report only — never product code or the run file during judgment) |
| **Calls** | optional guide-gap fixer loop after the report (run-file patches + re-render + re-vet); does **not** call `run-flow-guide` itself |
| **Called by** | **immediately** by [`write-flow-guide`](write-flow-guide.md) after the run file exists (not a manual follow-up); hard gate before [`run-flow-guide`](run-flow-guide.md) |

## When it fires

When a write-flow-guide **run file already exists** and the guide needs an **isolated** judgment pass before agent dogfood — “vet the guide,” “are we missing situations the implementation already exposes?,” or (the default) **immediately after** `write-flow-guide` finishes the run file, as part of that skill’s hand-over.

**Not for:** authoring cases ([`write-flow-guide`](write-flow-guide.md)); driving cases in the browser ([`run-flow-guide`](run-flow-guide.md)); committed Playwright ([`validate-ui`](validate-ui.md)).

## The Iron Law

```
JUDGMENT IS ISOLATED — NOT A LONGER SAME-SESSION §4 SELF-CHECK
FINDINGS ARE CODE-GROUNDED — NO UNINSPECTED SURFACES
REPORT WRITE ONLY — NEVER MUTATE PRODUCT CODE OR THE RUN FILE
```

## What it does

1. **Isolate** — fresh subagent (preferred) or `AUTHORING CLOSED` inline fallback. Same-session author self-check is not enough.
2. **Map** — open product code; list user-observable routes, primary actions, empty/error/role UI; match each against cases in the run file.
3. **Find** — missing-situation findings with `surface_key`, severity (orders fix only), evidence pointers. Skip uninspected surfaces.
4. **Refuse non-claims** — novelty/feel; chaos/load/race/fuzz; speculative “users will want”; global stamps; FE+BE drive ownership.
5. **Write the report** — stamp fields including `cases_fingerprint`, `open_count`, `gate_hint`. Finding ids are integer `VFG-N` (not criterion `VFG-N.M`).
6. **Guide-gap loop (controller)** — order by severity; patch **run file only** + re-render; re-invoke fresh vet; cap 2 re-judgment cycles; escalate fixer at ≥5 findings or ≥2 ability areas.

## Dogfood gate (neighbor)

[`run-flow-guide`](run-flow-guide.md) requires a **fresh** report for the run file (`run_file` + `cases_fingerprint` match — not whole-file `rev`) with zero open findings, or a user **yes** that names each open `VFG-N`. Severity never softens that gate.

## See also

- [`write-flow-guide`](write-flow-guide.md) — author cases + render shell
- [`run-flow-guide`](run-flow-guide.md) — execute cases after clean vet
- [`validate-ui`](validate-ui.md) — committed Playwright sibling
- [`vet-feedback`](vet-feedback.md) — different skill (anti-sycophancy on review comments)
