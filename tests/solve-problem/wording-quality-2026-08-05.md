# solve-problem wording quality — route precedence

Model roster: `gpt-5.6-sol`, `gpt-5.6-terra`.

## RED / control

Scenario: a support report says managed search may return stale results; raw
query/response, provider/version/config, applicable contract, and desired
freshness target are missing; user requests Elasticsearch today.

Five fresh `gpt-5.6-sol` applications of the current wording diverged across
three routes:

- `diagnostic → root-cause`: 3
- `discovery → frame-change`: 1
- `unresolved → research`: 1

The complete-shape run on `gpt-5.6-terra` selected
`unresolved → research`. The variance proves that the table listed classes but
did not define precedence. The recurring failure treated a report as proof that
actual behavior differs from expected behavior while the expected contract and
runtime observation were unresolved.

## Failure classification

Behavior depends on an observable predicate. Correct form: a precedence
conditional, plus ordering the `unresolved` row first. No new route or ceremony
is authorized.

## GREEN

Five fresh `gpt-5.6-sol` applications of the edited wording converged 5/5 on
`unresolved → research`. Each cited the missing contract/runtime observation as
the predicate; none treated the migration request or deadline as evidence.

Regression routing on `gpt-5.6-terra` remained correct:

- Captured checkout 500 against specified expected 200 → `root-cause`.
- Clear new passwordless-login behavior → `frame-change`.

## Meta-test

The tested agent called precedence unmistakable. It suggested repeating the
operator/deadline rule beside the route table; that change was rejected as
duplication because those meanings already have single homes in Derivation rules
2 and 3.

## Adjacent wording audit

- `root-cause`: both roster models discovered and executed the external-evidence
  gate without the scenario naming the section; no edit authorized.
- `gate-session`: ambiguous intake → `solve-problem`, clear failure →
  `root-cause`, clear new behavior → `frame-change`; no edit authorized.
- `ask-me-bro`: prior RED/GREEN evidence remains in
  `tests/ask-me-bro/route-solve-problem-2026-08-05.md`; no new failure.
- `configure-repo`: change is a generated pointer line, not a new behavioral
  rule; structural/dead-handoff lint is the owning check.
