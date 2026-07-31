# RED baseline log — build-story-units gates

**Roster:** grok-4.5  
**Date:** 2026-07-30  
**Protocol:** `author-skills` / `pressure-testing.md`

---

## A. Quiz-form gates (S-STORY-1..6)

### Control with dual-mode `build-continuous` loaded

| Scenario | Reps | CHOICE | Fail? |
|---|---|---|---|
| S-STORY-1 unit barrier | 1 | A | no |
| S-STORY-2 stop-stopping mode change | 1 | A | no |
| S-STORY-3 normal continue | 1 | A | no |
| S-STORY-4 derived units | 1 | A | no |
| S-STORY-5 whole-branch | 1 | A | no |
| S-STORY-6 resume ledger | 1 | A | no |

**Verdict:** Gate *rules already in dual-mode text hold under quiz pressure when the skill is loaded.* Do not invent new iron laws for failures that did not appear. Re-use proven wording when extracting into `build-story-units`.

### Control with skills/ withheld (no-skill)

| Scenario | CHOICE | Notes |
|---|---|---|
| S-STORY-1 | A | Mode name alone enough for this model |
| S-STORY-2 | A | Correctly preferred plan-file write over chat-only |
| S-STORY-4 | A | Preferred story chunks over PM batching |

**Honest limit:** On grok-4.5, quiz options restating the rule still bias toward A (same limitation as `reviewable-delivery/PRESSURE-FINDINGS.md`). Quiz RED does **not** prove the dual-mode skill is unnecessary; it fails to prove gate text is broken.

---

## B. Failures that *did* appear (these own the split)

### B1 — Routing collapse (distinct trigger missing)

**Setup:** five user intents (continuous / story-unit / inline / root-cause mid-run / continuous again).

**Observed:** intents 1, 2, 3, 5 all route to **`build-continuous` only**. Story-unit and inline cannot fire a specialized skill because none exists.

**author-skills class:** **When to split — case 1 (genuinely distinct trigger).**  
Not fixed by more rationalization rows inside one description.

### B2 — Unit summary shape variance (recipe hole)

**Setup:** three fresh agents, EOD pressure, “present unit summary / STOP”, no self-score checklist in prompt. Source text only says: `STOP. Present unit summary. Wait.`

| Rep | unit id | stories | tasks | range | verdicts | minors | unlock wait | continue vs mode-change semantics |
|---|---|---|---|---|---|---|---|---|
| 1 | Y | Y | Y | Y | Y | Y | Y | **Partial** — “switch to continuous” without “write tasks.md” |
| 2 | Y | title only | Y | Y | Y | Y | Y | Y (mentions tasks.md write) |
| 3 | Y | Y + merge reason | Y | Y | Y | Y | Y | Y |

**author-skills class:** *Complies, but output has wrong/unstable shape* → **positive recipe / REQUIRED slots**, not more prohibitions.  
`story-unit-mode.md` step 5 has no contract for the human-facing summary.

### B3 — User production report (external)

User: story-unit via dual-mode `build-continuous` “không thực sự cho lại kết quả quá tốt”. Compatible with B1+B2: attention stays on continuous subagent factory; barrier is a mode branch; summary recipe unbound.

### B4 — Structural (design diagnosis, not quiz)

| ID | Symptom | Dual-mode contribution |
|---|---|---|
| STRUCT-1 | Continuous “never pause” competes with unit STOP | Same SKILL.md body |
| STRUCT-2 | Inline Fallback buried ~line 130 | Third path not first-class |
| STRUCT-3 | Preflight unit table both modes | Signal without barrier ownership |

---

## C. What GREEN may write (and must not)

**May write (backed by B1–B2):**

1. New skill `build-story-units` with its own description (routing fix for story-unit intent)
2. Move unit derivation + barrier recipe into that skill’s home
3. REQUIRED unit-summary template (slots from B2 table)
4. Extract *existing* iron laws / rationalization rows verbatim (already GREEN under quiz) — do not “harden” with invented counters

**Must not write:**

- New gate rules for S-STORY-1..6 “because we split”
- Batch `build-inline` + `build-continuous` narrow in the same authoring pass

---

## D. Overall RED verdict for authoring `build-story-units`

| Claim | Status |
|---|---|
| Quiz gates fail without/with dual-mode skill | **No** — A across runs |
| Distinct-trigger failure (routing) | **Yes** — B1 |
| Unit summary recipe failure (variance) | **Yes** — B2 |
| Proceed to GREEN for `build-story-units` | **Yes** — minimal text for B1+B2 + extract proven gates |
| Proceed to invent new barrier iron laws | **No** |
