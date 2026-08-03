# thinking-handoff/v1

Neutral hand-off packet from `thinking-practice` → `interpret-session`.
Self-contained. Field-level provenance required. No recommendation payload.

## Required top-level structure

```text
schema: thinking-handoff/v1
target: interpret-session

session_context:
  target_language: <string>                    # USER_VERBATIM or USER_CONFIRMED
  project_posture:
    delivery_intent: <string | unknown>        # FROM_PROJECT_MD | USER_SUPPLIED | ABSENT
    lifecycle_stage: <string | unknown>        # FROM_PROJECT_MD | USER_SUPPLIED | ABSENT

hand_off:
  path: A | B                                  # USER_EXPLICIT
  user_request: <verbatim>                     # USER_VERBATIM

checkpoint:
  # Path A — all user-verbatim where present
  path_a:
    position_kind: hypothesis | prediction | decision | unclear   # USER_VERBATIM
    position: <verbatim>                       # USER_VERBATIM
    basis: <verbatim | "not supplied">         # USER_VERBATIM
    open_or_ask: <verbatim>                    # USER_VERBATIM
  # Path B
  path_b:
    status: explicitly_skipped
    missing: [position?, basis?, open_or_ask?] # only fields actually absent

relevant_evidence:                             # 0–5 items
  - claim: <text>
    label: VERIFIED_EVIDENCE | SOURCE_CLAIM
    source: <url | path | symbol>
    scope: <what this does / does not cover>
    provenance: AGENT_ASSEMBLED | USER_VERBATIM

open_map:                                      # current unknowns only
  - unknown: <text>
    provenance: USER_VERBATIM | AGENT_INFERENCE
    status: open | narrowed | pending_check | …
    cheapest_check: <text | unknown>

calibration:
  status: <calibration-axis status only>
  # when a relevant cycle occurred:
  prior_position: <user verbatim | n/a>
  user_delta: <user verbatim | reflection explicitly skipped | n/a>
  evidence_refs: [<indices or sources>]

transport_constraints:
  - no recommendation, ranking, preferred option, or hidden lean
  - agent-authored material remains agent-authored after transport
```

## Calibration-axis status values

Exactly one of:

- `not reached`
- `question/hypothesis framed`
- `check pending`
- `evidence received`
- `calibrated`
- `reflection explicitly skipped`
- `inconclusive — more evidence needed`

Do **not** put hand-off axis values under `calibration.status`.

## Provenance rules

- Every field or list item carries its own provenance label (or an explicit
  sub-field). A legend-only block at the end is **invalid**.
- `hypothesis` / `prediction` must never be rewritten as `decision`.
- Agent territory bullets (if any appear under evidence) stay agent-authored.

## Language / translation

- Default packet language = session `target_language`.
- User-authored checkpoint text: preserve verbatim; do not polish.
- English transport copy (optional, when needed):
  - Keep the original packet.
  - Label translated user text: `AGENT_TRANSLATION_OF_USER_VERBATIM`.
  - Include both original and translation for those strings.
  - Code, paths, identifiers, citations: unchanged.
  - Target-language round-trip of what the English copy commits the user to.

## Forbidden contents

Do not include:

- recommendations, ranking, preferred option, soft lean, aggregate scores
- key implications that encode a lean
- inferred user rationale
- full question history
- full research digests
- `learning complete`
- `ship ready` / production-readiness claims

## Path B missing list

Use schema field names only: `position`, `basis`, `open_or_ask`.
Include only fields that are actually absent.
