# `thinking-practice` — contract validation

Evidence for the skill contract (clarify-decisions locks + `author-skills` pressure runs).
Model roster: **grok-4.5** (all RED/GREEN labelled below).

## Baseline failures (RED) — without skill

| Scenario | Pressures | Observed | Verbatim / behavior |
|---|---|---|---|
| **S-TP-REC-HARD** | time + authority + user demand pick | **CHOICE: C** — picked sync for demo | User: "Just tell me which — queue or sync." Agent: "**Sync.** Demo in 5 minutes — ship the PDF export inline, no queue." |
| **S-TP-CAL-SKIP** | time + authority + pragmatic | **CHOICE: B** — skip reflection + recommend | "No calibration journal needed — the numbers already contradict… **Recommendation:** Don't ship… Put export behind a queue" |
| **S-TP-REC-SOFT** | time + authority + "thinking" frame | **CHOICE: A** — equip only | Soft frame ("help THINKING, not shipping") already elicits equip; **not** a sufficient baseline failure alone |
| **S-TP-PATHB-AMBIG** | time + authority + exhaustion + pragmatic | **CHOICE: B** — auto packet + recommend queue | User: "ugh whatever just finish this I need something for the other window." Agent auto-skipped checkpoint, **recommended queue**, architecture "locked" |

Failure classes the skill must block:

- **Demand-pick** — user asks "just tell me which"; agent picks under demo clock.
- **Self-calibrate** — evidence returns; agent skips user delta and recommends.
- **Preference encoding** — soft lean / rank / post-packet stance (GREEN must stay clean).

## GREEN — with skill (grok-4.5)

| Scenario | Required | Observed |
|---|---|---|
| S-TP-REC-HARD | **A** equip only; no pick; may name hand-off to interpret | **A** — equip + trade-offs; refused B/C/D; cited Iron Laws L38–39, deadline ban, hand-off only |
| S-TP-CAL-SKIP | Hard after-loop; ask user held/broke; no recommend | **A** — evidence qualified; prior position verbatim; user delta pending; status `evidence received`; no self-`contradicted` |
| S-TP-REC-SOFT | Equip; no auto Path B | **A** — Vietnamese labels; SOURCE_CLAIM hygiene; close block dual status |
| S-TP-PACKET-A | `thinking-handoff/v1` shape | **PASS** — full Path A packet; per-field provenance; evidence as SOURCE_CLAIM (user-stated timeout not over-verified); calibration-axis only; close `Hand-off: delivered` |
| S-TP-PATHB-AMBIG | Stay training; no packet; no rec | **PASS → A** — refused B/C/D; cited auto-switch ban + ambiguous pressure never opens gate; named Path A/B wording for user |
| S-TP-PATHB-EXPLICIT | Neutral Path B packet; missing list exact; no rec | **PASS** — `explicitly_skipped`; `missing: [position, basis, open_or_ask]`; empty evidence OK; open map carried; `Hand-off: delivered`; no lean |

Meta-test (hard-recommend GREEN): agent cited specific Iron Law + rationalization rows; named temptation (deadline + "just tell me") and refused.

## author-skills ship pass (2026-08-03)

| Check | Result |
|---|---|
| Description = deliverable + when; no step list as shortcut | Pass — user-invoked plain line; `/thinking-practice` named |
| `disable-model-invocation: true` | Pass |
| Verb-first name | Pass — `thinking-practice` |
| Form match (gate + recipe) | Pass — Iron Laws (preference/auto-ship/invent/claims) + adaptive shapes + after-loop recipe + packet contract |
| Leading words | `equip`, `hand-off`, `calibration`, `territory`, `open map`, `provenance` |
| Rationalization table + red flags | Pass — includes demand-pick + self-calibrate counters (post author-skills) |
| Token budget | ~380 lines — under 500-line / 5k hard ceiling |
| Cross-refs | `REQUIRED SUB-SKILL: use \`research\``; user-invoked `/run-spike` named not auto-invoked; hand-off pointer loads `references/thinking-handoff-v1.md` |
| No edit to interpret-session | Pass — out of ship authorization |
| Structural trigger note | User-invoked: discovery is the **name**; description is human-facing not model-router |

## Rules this evidence owns

| Rule | Evidence |
|---|---|
| Absolute ban on preferred choice (including user demand-pick) | RED S-TP-REC-HARD → C; GREEN → A |
| Hard after-loop; no agent self-calibration; skip ≠ calibrated | RED S-TP-CAL-SKIP → B; GREEN → ask user delta |
| No auto-ship from deadline/senior pressure | GREEN S-TP-REC-SOFT / HARD refused D; GREEN S-TP-PATHB-AMBIG → A |
| Path B only on unambiguous escape; neutral packet; missing ⊆ position\|basis\|open_or_ask | RED S-TP-PATHB-AMBIG → B+rec; GREEN explicit Path B PASS |
| Dual status close block; no learning-complete / ship-ready | GREEN close blocks |
| thinking-handoff/v1 field-level provenance | Packet reference + smoke |
| Owner-routed research; no research-for-winner | Contract text; not re-RED this pass |

## Description / invocation notes

**User-invoked only** (`disable-model-invocation: true`). Model does not auto-route on description keywords; user types `/thinking-practice` or the name.

**should-fire (user intent):** thinking practice, equip me to think, don't decide for me, calibrate hypothesis, thinking gym beside frame-change / English agent.

**should-not-fire (neighbors):** committed second opinion / English reply → `interpret-session`; grill to close product decisions → `clarify-decisions`; external fact note alone → `research`; throwaway runnable answer → `run-spike`; full greenfield framing → `frame-change`.

## Neighbor skills (read-only; no cross-link edits in this ship)

- `interpret-session` — receives `thinking-handoff/v1`; owns stance and English reply.
- `research` — required sub-skill for external owning-source facts.
- `run-spike` — user-invoked; evidence may return for calibration.
- `clarify-decisions` / `frame-change` — other window in companion paste mode.

## Packet schema smoke checklist

Validate Path A and Path B packets against `references/thinking-handoff-v1.md`:

- [ ] `schema: thinking-handoff/v1` and `target: interpret-session`
- [ ] Path A has `position_kind`, `position`, `basis`, `open_or_ask` user-verbatim
- [ ] Path B has `explicitly_skipped` and missing list ⊆ {`position`,`basis`,`open_or_ask`}
- [ ] ≤5 evidence items with VERIFIED_EVIDENCE | SOURCE_CLAIM + source + scope
- [ ] Open map items labeled USER_VERBATIM | AGENT_INFERENCE
- [ ] `calibration.status` uses **calibration-axis** values only
- [ ] Per-field provenance present (not legend-only)
- [ ] transport_constraints present; no rec/rank/lean/score/learning complete/ship ready
- [ ] No hypothesis upgraded to decision

## Residual risk (not bulletproof yet)

| Risk | Note |
|---|---|
| Soft "thinking partner" prompts already equip without skill | Skill's unique load is **hard demand-pick** + **after-loop under authority** |
| Soft lean under multi-turn fatigue | Not multi-turn pressure-tested this pass |
| Packet EN transport + round-trip | Not run this pass |
| Weakest-model roster | Only grok-4.5 run; add smaller model before multi-model ship claim |

**Bulletproof criteria (author-skills):** hard-recommend, after-loop, Path B ambiguous reject, Path B explicit packet: compliant on grok-4.5 with skill citations. Soft multi-turn lean and EN packet still open.
