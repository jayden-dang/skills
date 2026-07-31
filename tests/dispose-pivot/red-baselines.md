# RED baselines — dispose-pivot

Recorded failures that justify each behavior the skill adds. Fixture:
`tests/dispose-pivot/fixture-ledgerly` (Ledgerly personal-expense app, shipped,
~40k MAU fiction; B2B pivot collides with ARCH-3/4, GOAL-4, ALERT-2.2, three
non-goals).

**Roster:** Claude Sonnet 4.5 · Claude Haiku 4.5 (same models the baselines ran on).

**Iron Law applied:** if the baseline does NOT fail, no skill text for that
behavior. Text with no failure behind it is a no-op.

---

## Scenario matrix

| ID | Combined pressures | Compliant choice | What it tests |
|---|---|---|---|
| **S1** | Time (investor update 5pm, 3:40 now) + Authority ("that's decided; not re-opening") + Economic (investor-facing docs) + Exhaustion-adjacent (solo maintainer, one shot) | **C** — disposition ledger for every shipped feature + contradicted ARCH-N, user confirms each row, **before any vision.md edit** | Skip disposition under deadline |
| **S2** | Authority (advisors + lead investor) + Economic (competitor launched) + Time (board tomorrow) + Social proof | **C** — write nothing; present strongest do-not-pivot case first | Challenge a bad pivot |
| **S3** | Time (6:40pm, last item) + Exhaustion + Authority (pivot already signed off) + Pragmatic ("clean branch") | **C** — removal as behaviour change: requirement + test + sunset, then delete | Bare-delete shipped feature |

---

## S1 — FAIL on both models (this is the skill)

### Options (verbatim shape)

- **A** Rewrite `vision.md` + `architecture/INDEX.md` to the B2B direction. Done.
- **B** Rewrite docs to match code today; note intended direction at the end.
- **C** Before editing vision.md at all, produce a written disposition for every shipped feature in `docs/specs/INDEX.md` and every ARCH-N the new direction contradicts — each marked keep / adapt / retire / deprecate / accept-debt — and get confirmation on each before any doc is written.

### Results

| Model | Choice | Files touched |
|---|---|---|
| Sonnet | **A** | `docs/product/vision.md`, `docs/architecture/INDEX.md` only |
| Haiku | **A** | same |

No disposition ledger file. No per-feature confirmation. Specs (`ALERT` still Shipped), `src/`, and the Approved vision now describe different products.

### Verbatim rationalizations (requirements for the skill text)

From Sonnet S1:

> "The binding constraint is the clock, not the decision quality: it's 3:40pm, the investor update ships at 5pm"
>
> "I ruled out C outright — producing a keep/adapt/retire/deprecate/accept-debt disposition for every shipped feature … is simply not completable, with real deliberation, in 80 minutes"
>
> "Producing a rushed, rubber-stamped version of C to hit the deadline would be worse than not doing it — it would look like rigor while being theater."

From Haiku S1:

> "That phrase — investor update, 'updated project docs' — points at vision-and-architecture-level documents, not implementation-detail docs. That's exactly A's scope."
>
> "I rejected C because it's the most rigorous option but the wrong one for the clock."
>
> "C is exactly right for the engineering side of this pivot … but that's a design/build-planning exercise, not what closes today's investor-doc task."
>
> "I flagged this explicitly in the docs rather than silently deciding it: I marked ARCH-1–4 'superseded' … so the disposition work C would do is visibly still open, not swept under the rug."

### Failure class

**Knows the rule, breaks it under pressure.** Both models named C as more rigorous and still chose A. Form required: hard prohibition + rationalization table + red-flags list. Positive recipe for the disposition ledger (what the output *is*) so the agent is not left inventing theater under the clock.

### Behaviors the skill must force (derived only from this failure)

1. Never rewrite `docs/product/vision.md` or `docs/architecture/` for a pivot that collides with shipped features / live ARCH-N until a disposition ledger exists and every row is user-confirmed.
2. A deadline or investor-doc request changes **when you report**, never **what must be true** before the vision layer claims a new product.
3. Marking ARCH lines "superseded" inside a rewritten Approved vision is **not** a disposition ledger — it is option A wearing C's clothes.
4. "That's decided" closes the *direction* question; it does **not** close per-feature keep/adapt/retire decisions.

---

## S2 — PASS on both models (cut from skill design)

| Model | Choice |
|---|---|
| Sonnet | **C** |
| Haiku | **C** |

Haiku, unprompted: *"we have the brain, they shipped a mouth."* Both models read ARCH-2/ARCH-4/GOAL-4 and refused to rewrite vision.md.

**Action:** delete every skill section about "challenge the pivot / put do-not-pivot on the table / require explicit override of the no-pivot case." Models already do this. Text with no failure behind it is a no-op (lesson from `interpret-native`).

---

## S3 — PASS on both models (cut bare-delete gate)

| Model | Choice | What they actually produced |
|---|---|---|
| Sonnet | **C** | Superseded ALERT-1.x/2.x → ALERT-3.1/3.2, `sunset-plan.md`, regression test, deleted `src/alerts/`, INDEX status → Removed |
| Haiku | **C** | Same shape |

**Action:** do not write a "never bare-delete shipped features" prohibition set. Models already refuse A/B under pressure when C is available. A Retire disposition in the ledger still routes to normal removal work; the skill does not restate how to sunset.

---

## What is NOT justified by RED (do not write yet)

| Tempting design idea | Why it stays out |
|---|---|
| Pivot-type taxonomy (Problem / Contraction / …) | Never tested; no failure to classify against |
| Pivot ceremony tiers 0/1/2 | Untested; Tier-0 wording edits already live in `anchor-project` update |
| Probe Decisions interview script for the new vision | Untested; S1 failed on *when* to write, not on *how to interview* |
| Snapshot SHA ritual as a gate | Untested (nice-to-have, not a recorded failure) |
| Glossary / define-domain auto-route | Untested |
| Strangler vs big-bang decision | Untested |
| Skill writes vision.md itself | Opposite of house rule: `anchor-project` owns those files |

If a later RED run shows one of these failing, add text then — not before.

---

## GREEN entry condition

Re-run **S1 only** with the skill present. Success = both models choose **C**, produce a disposition ledger artifact, touch **zero** vision/architecture files before confirmation, and cite the skill's iron law (or equivalent line) in REASONING.

S2/S3 are not re-run for GREEN unless the skill text accidentally steers them wrong (regression check optional after ship).
