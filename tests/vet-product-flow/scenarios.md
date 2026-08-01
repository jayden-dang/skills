# Vet product flow — scenarios (ID index)

Greppable requirement-ID layer for feature VPF. Stories 1–8 have behavioral
bullets. Pressure scenarios: `scenarios-pressure.md`.

## Story 1 — Isolated skill and report artifact

- **VPF-1.1** model-invoked skill at `skills/acceptance/vet-product-flow/SKILL.md`
  with frontmatter `name: vet-product-flow` and no `disable-model-invocation`.
  Description triggers judgment / isolation / before dogfood — not a step-by-step
  workflow summary.
- **VPF-1.2** judgment runs in a fresh isolated context: preferred read-only
  subagent with `judgment-brief.md`, or inline fallback that states
  `AUTHORING CLOSED — starting isolated vet-product-flow pass`. Same-session §4
  self-check / self-clear after authoring is forbidden as a substitute.
- **VPF-1.3** completed pass writes `.skills/<slug>-vet-product-flow.md` with
  stamp fields including `run_file`, `cases_fingerprint`, `stamped_at`,
  `pass_kind`, `prior_report`, `open_count`, `gate_hint`, plus open findings.
- **VPF-1.4** findings identified as integer `VPF-N` (not criterion `VPF-N.M`).
- **VPF-1.5** during judgment: product codebase and run file unmodified
  (read-only). Report write is allowed. No self-stamped “clean” without a report.

## Story 2 — Implementation-surface map

- **VPF-2.1** map user-observable shipped paths/states (routes, primary actions,
  empty/error/role UI actually rendered) against run-file cases — not every
  internal branch or helper.
- **VPF-2.2** emit a missing-situation finding when a shipped surface has no
  corresponding case (including non-happy paths real use can hit).
- **VPF-2.3** require opened-code evidence (file / symbol / route / state) for
  any implementation claim that the product already does X.
- **VPF-2.4** if code for a candidate surface was not inspected, do not assert
  that surface as a missing-situation finding.
- **VPF-2.5** severity labels Critical / Important / Minor order the fix loop
  only; severity does not soften or clear the dogfood gate.
- **VPF-2.6** authoring §1 hygiene (schema/kind/status, requirement-ID coverage)
  is not the product claim; never sell mechanical completeness as “complete for
  real users.”

## Story 3 — Explicit non-claims

- **VPF-3.1** no novelty / feel / visual-polish taste as pass/fail outcomes.
- **VPF-3.2** no chaos / load / race / security-fuzz suites required or invented.
- **VPF-3.3** no speculative “users will want X” / “product should do X” when X
  is not already on the shipped user-observable surface.
- **VPF-3.4** no global stamps: “good UX”, “complete for real users”, “ready to
  ship.”
- **VPF-3.5** does not replace dogfood: no drive-app pass/fail ownership, no
  FE+BE (`saw`/`server`) evidence ownership inside `vet-product-flow`.

## Story 4 — Author hand-off

- **VPF-4.1** at `review-product-flow` §5 Hand over, **required next** is
  `vet-product-flow` on the run file before treating the guide as ready for
  agent dogfood; name `run-product-walkthrough` **only after** a clean vet
  report (or named override). Ordered: artifacts → vet → optional serve →
  walkthrough.
- **VPF-4.2** CONTINUE TO apply §1 coverage gate and the seven-kind taxonomy
  (`happy`/`edge`/`error`/`nonbehavior`/`persist`/`visual`/`journey`); coverage
  self-check remains and is not a substitute for vet.
- **VPF-4.3** CONTINUE TO treat the run file as authoring **SSOT** and use
  `review-product-flow render` with the checked-in shell (`shell/guide.html`) —
  no craft-page default.

## Story 5 — Hard gate before walkthrough drive

- **VPF-5.1** before any product case drive, require a **fresh**
  `.skills/<slug>-vet-product-flow.md` for this run file. Freshness =
  `run_file` path match **and** `cases_fingerprint` match (SHA of authored
  cases only) — **not** whole-file `rev`. `init` may seed pending; no product
  click and no `mark` of a driven case until the gate passes.
- **VPF-5.2** if the fresh report has any open missing-situation finding and the
  user has not given an explicit in-thread yes naming each remaining open
  finding, **do not** drive product cases. On STOP, list findings and point to
  the **guide-gap** loop.
- **VPF-5.3** override requires an explicit in-thread yes that **names** each
  remaining open `VPF-N`; write a greppable trail in `.skills/progress.md` (or
  walkthrough close notes). No silent skip; bare “just go” is not enough.
- **VPF-5.4** every open code-grounded finding is **blocking**; severity labels
  do **not** re-soften the gate or reintroduce hard-only-on-Critical.
- **VPF-5.5** CONTINUE TO require local default or explicit non-local origin
  consent naming that origin **before the first product click**.
- **VPF-5.6** CONTINUE TO require non-empty `--saw` and `--server` (Iron Law /
  presentational sentinel) before `mark pass`.

## Story 6 — Guide-gap fix and re-check loop

- **VPF-6.1** walkthrough stays **blocked** while open findings remain (gate
  side); severity does not drop any open finding from the blocking set.
- **VPF-6.2** guide-gap fixes **order by severity** (Critical → Important →
  Minor); patch the **run file only** (add/reshape cases/sections/slots) and
  **re-render** HTML — never product code patches, never mid-drive invent-cases.
- **VPF-6.3** after run-file patches, **re-invoke** `vet-product-flow` in a
  **fresh isolated** pass; the dogfood gate re-evaluates **only against the new
  report**.
- **VPF-6.4** clear a finding only when it is **absent from the new open list**
  or the user names it in an explicit **named override** — never self-declare
  clean without a new report.
- **VPF-6.5** when open count is **≥ 5** OR rewrite spans **≥ 2 ability areas**
  (multi-section), dispatch an **isolated fixer subagent** whose brief is the
  finding set + run-file path (+ evidence), not full session history; then
  re-run fresh `vet-product-flow`. Fixer must not self-declare clean.
- **VPF-6.6** after **2 re-judgment cycles** still open → **stop for the human**
  (fix more, named override listing remaining findings, or shrink surface)
  rather than thrashing.
- **VPF-6.7** non-code-grounded, taste, or out-of-claim items **do not keep the
  fix loop alive** as if they were missing-situation findings.

## Story 7 — Product-defect isolation during dogfood

- **VPF-7.1** during `run-product-walkthrough` §4, **master** owns case
  selection, evidence slots, `mark` pass/fail/blocked, and **re-test** after a
  fix — not the fix subagent.
- **VPF-7.2** product-defect work dispatches a **subagent** with a red-capable
  brief only (repro, saw/server, case id, `req`, try/expect) — **not** the full
  session history or long dogfood context.
- **VPF-7.3** when that subagent reports **DONE**, master re-drives the failed
  case and every already-`pass` case whose `req` the product fix touched
  (existing re-drive rules).
- **VPF-7.4** the subagent still uses **`root-cause`** (+ **test-first**);
  context isolation is not a free pass to patch without root-cause.
- **VPF-7.5** the **guide-gap** fix loop (story 6: patch run file → re-vet) stays
  **separate** from this product-defect dogfood loop; product defects do not
  absorb missing-situation findings; mid-run guide misses re-enter vet, not
  root-cause.

## Story 8 — Reliability (finding id stability)

- **VPF-8.1** re-check reuses `VPF-N` for the same still-open `surface_key`;
  a new surface miss receives the next integer finding id (fixture pair
  `sample-report.md` / `sample-report-recheck.md`).
