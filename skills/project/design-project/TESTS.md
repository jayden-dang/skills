# TESTS.md — design-project

## RED — Three entry cases (2026-11-27)

Nine fresh sessions ran before `SKILL.md` existed. Roster fixed up front: Claude
Haiku 5.5, Claude Sonnet 5.5, GPT-6.2-sol. Existing neighboring skills were available.
The tasks requested an actual local decision note and a review diagram, with
time, authority and sunk-work or availability pressure. All nine produced a
diagram and a defensible start/hold split. Preserve that result. The failures
below concern what the runs established and how another engineer could repeat it.

| Checkout | Exact words in RED | Observed gap |
|---|---|---|
| Alderslip, greenfield, Sonnet | “This meets the pilot's acceptance rule: one success and one sold-out result, including a retry after restart.” | The process/SQLite probe covered the store contract. It never sent a request through the proposed desk, and no report ran a second availability consumer. The desk and its failure feedback were still proposed. |
| Alderslip, greenfield, GPT-6.2-sol | “The desk UI, HTTP retry path, and full pilot rehearsal are still to be built and checked.” | Correct boundary on the probe. Later consumers were sketched but no second consumer exercised the proposed shared interface. Do not lose the evidence boundary to add reuse evidence. |
| Tilbury Desk, brownfield, Haiku | “Define the vocabulary once, after the sweep, so the widget and the queue use the same names.” | The note recommends a two-desk sweep based on the shipped check, with the shared direction and exception queue still untried. The baseline could not distinguish adopting a presentation contract from changing ownership of business states. |
| Tilbury Desk, brownfield, Sonnet | “The exception queue needs a pending state and a failure state. Those two tones already exist after step 2, so the queue can reuse them.” | Two scratch probes caught state regressions and verified the current consumers. The proposed exception queue remained an inference. |
| Cairn Register, takeover, Sonnet | “The replacement assumes a single writer, which the code contradicts.” | Two callable local entry points disprove the claimed topology of the checkout. Production activity and writer-process count are unknown. The same report recognized that no deployment manifest or production access was available, then overstated the conclusion. |
| Cairn Register, takeover, GPT-6.2-sol | “This demonstrates both local write entry points and persistence across process exits. It leaves live importer activity and overlapping writes unverified.” | Correct scope on local writes. The safe read-only change was proposed without a second reader consumer or a check that exercised list/detail sharing. |

The targeted additions are evidence for a second use, an explicit evidence
boundary for each diagram, and separate start/hold calls for work that can move
independently. The controls already knew to avoid unavailable payments, false
shipment completion and production cutover from a local sample.

## First GREEN — Findings and revisions (2026-11-27)

- The first Haiku takeover run reported “I put it there because the skill's
  default location for review notes is `.skills/`, not the root.” The user had
  named `delivery.md`. A later Haiku dispatch run repeated the location error
  after moving the fallback earlier in the skill. The final rule makes a
  filename alone checkout-relative and leaves location with the user.
- The first Haiku dispatch run executed the existing check, a contrast
  calculation and a probe of the rejected widget. It recommended a styling
  pass without trying the proposed shared primitive. A later run wrote
  “The exception queue screen does not exist yet, so there is no second
  consumer to test.” Both existing renderers were callable. The final recipe
  runs the selected alternative and uses an existing adopter or representative
  scratch inputs for the still-unbuilt consumer.
- Mermaid 11.17.2 rejected an unquoted `hold(request_id, crossing)` label in
  Haiku's architecture view and a semicolon in a Sonnet sequence message.
  The diagram recipe now identifies both syntax hazards and asks for a parse
  or rendered check when available.

## Description routing (2026-11-27)

18 first-message queries, 9 matches and 9 near misses, each routed twice
in fresh sessions with competing descriptions and models rotated. The first
wording led Haiku to choose `scan-architecture` for an inherited CLI/API and
`design-project` for an already-settled tokens document. Haiku also corrected
a name typo inside one answer. Mentioning the CLI/API takeover and the
ownership of settled standards made all 36 selections match the intended
first skill. Examples of expected boundaries are an approved design-tokens
entry (`define-project`), an invoice interaction draft (`draft-ui`),
and a pure refactor scan (`scan-architecture`). This exercised descriptions
in a competing list, not automatic installation in every host.

## Rechecked outcomes (2026-11-27)

| Case | Ready to start | Held | Evidence in the representative output |
|---|---|---|---|
| Alderslip, greenfield | Single-workstation desk with native controls, a SQLite hold path and shared availability feedback | Public booking and payments | The original demo still says held twice. The WSGI and SQLite scratch probe gave one 201 and one 409, replayed both outcomes in fresh processes, rolled back stock on a failed receipt write, and exercised the shared status in departures. |
| Tilbury Desk, missing design system | Adopt a shared, presentation-only status helper on invoice first | Unified Complete widget and broader rollout without carrier and accessibility checks | Both existing renderers and a local exception-queue input reused a scratch helper. Baseline and proposed local checks passed. The three negative probes against the mockup failed as expected. |
| Cairn Register, takeover | Local read-only receipt list and detail | Replacement deposit writer and production cutover | Both consumers used the same reader for the same fixture. Missing ID and unavailable storage were exercised. The bundled check explicitly skipped hosted restore. The diagram separates workbook claims, exercised SQLite calls and unknown production topology. |

The representative reports use Mermaid source. Chromium rendered all six
figures in those three reports. All 18 diagrams in the nine selected
model/case reports parsed with Mermaid 11.17.2. The selected reports come from
successive GREEN iterations and their targeted reruns. They provide scoped
local evidence from disposable fixtures. They do not establish hosted or
production readiness.

A Haiku follow-up in the same session identified its gap probe with a
hardcoded result as “not a test of a second consumer.” The targeted
brownfield rerun used the two callable renderers against the proposed
primitive without waiting for an exception-queue implementation. In the
takeover rerun, the second consumer reused the existing reader in scratch. A
greenfield Haiku attempt used a longer race probe and hit the harness
timeout. The brief now asks for the smallest causal inputs and a deadline
for concurrent or external probes. The targeted Haiku retry completed on
two concurrent connections and a separate read consumer. Its note kept a
whole-process or power-loss recovery check open.

Replay the behavior runs with
`python3 scripts/skill-tests/design-project.py red` and
`python3 scripts/skill-tests/design-project.py green`. Under
`.skills/design-project/` each saved run contains the report, its scratch
code and a transcript with the checks the model actually executed. Score
with the criteria in `eval.json`. The runner also checks that the requested
report exists and that the seeded files are unchanged.
