# Vet product flow — scenarios (ID index)

Greppable requirement-ID layer for feature VPF. Stories 1–3 carry behavioral
bullets from Task 2; later stories expand in later tasks.

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

- VPF-4.1 review-product-flow names vet before agent dogfood
- VPF-4.2 CONTINUE TO §1 coverage gate and seven-kind taxonomy
- VPF-4.3 CONTINUE TO run file SSOT + shell render path

## Story 5 — Hard gate before walkthrough drive

- VPF-5.1 require fresh report for run file before any product drive
- VPF-5.2 open findings block drive without named override
- VPF-5.3 override must name each open `VPF-N` with greppable trail
- VPF-5.4 every open finding blocks; severity does not re-soft gate
- VPF-5.5 CONTINUE TO origin consent before product click
- VPF-5.6 CONTINUE TO Iron Law mark evidence (`saw` + `server`)

## Story 6 — Guide-gap fix and re-check loop

- VPF-6.1 keep walkthrough blocked while open findings remain
- VPF-6.2 patch run file only (+ re-render); order by severity
- VPF-6.3 re-invoke fresh isolated vet; gate uses new report only
- VPF-6.4 clear only via new open list absence or named override
- VPF-6.5 escalate fixer subagent at ≥5 findings or ≥2 ability areas
- VPF-6.6 stop for human after 2 re-judgment cycles
- VPF-6.7 non-code-grounded / taste items do not keep the loop alive

## Story 7 — Product-defect isolation during dogfood

- VPF-7.1 master owns selection, evidence, mark, re-test
- VPF-7.2 subagent brief is red-capable only (not full session)
- VPF-7.3 master re-drives failed + related already-pass after DONE
- VPF-7.4 subagent still uses root-cause (+ test-first)
- VPF-7.5 guide-gap loop separate from product-defect loop

## Story 8 — Reliability (finding id stability)

- **VPF-8.1** re-check reuses `VPF-N` for same still-open `surface_key`
