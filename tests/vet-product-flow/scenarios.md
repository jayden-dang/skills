# Vet product flow — scenarios (ID index)

Greppable requirement-ID layer for feature VPF. Behavioral bullets expand in
later tasks; this skeleton places every `VPF-N.M` once under its story heading.

## Story 1 — Isolated skill and report artifact

- VPF-1.1 model-invoked skill at `skills/acceptance/vet-product-flow/SKILL.md`
- VPF-1.2 judgment in fresh isolated context (subagent or axis-close inline)
- VPF-1.3 report path + stamp fields including `cases_fingerprint`
- VPF-1.4 findings identified as integer `VPF-N` (not criterion `VPF-N.M`)
- VPF-1.5 read-only: no product code or run-file writes during judgment

## Story 2 — Implementation-surface map

- VPF-2.1 map user-observable shipped paths/states against cases
- VPF-2.2 emit missing-situation when surface exists without a case
- VPF-2.3 require opened code evidence for implementation claims
- VPF-2.4 do not assert surfaces that were not inspected
- VPF-2.5 severity orders fix only; does not soften dogfood gate
- VPF-2.6 hygiene is not the product claim / not “complete for real users”

## Story 3 — Explicit non-claims

- VPF-3.1 no novelty/feel/polish taste as pass/fail
- VPF-3.2 no chaos/load/race/fuzz requirement
- VPF-3.3 no speculative “users will want” findings
- VPF-3.4 no global “good UX / ready to ship” stamps
- VPF-3.5 does not replace dogfood (no drive / FE+BE ownership)

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

- VPF-8.1 re-check reuses `VPF-N` for same still-open `surface_key`
