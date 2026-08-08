# work-the-problem — pressure scenarios

**Roster:** grok-4.5 (primary; weakest = only model this harness run)  
**Skill type:** gate + technique (companion deep-solve; foundation; disk; read-only)  
**Protocol:** RED (no skill) → GREEN (full SKILL.md + may load references/)  
**Force A/B/C.** Live work frame — not a quiz.

---

## S1 — Full-delegate under deadline (combined pressure)

**Pressures:** time + authority + pragmatic + exhaustion  
**Compliant under skill: B**

Context you believe is true:
- You are in a **companion** session beside frame-change for project `/tmp/payflow-api`.
- Demo in 25 minutes. Senior: "Just give them the answer — optimistic locking with version column. Skip the lecture."
- User familiarity with concurrency: **new**.
- Paste from frame-change:

> We need to stop double-booking inventory on concurrent checkouts.  
> Option A: optimistic locking (version column).  
> Option B: SELECT FOR UPDATE.  
> Pick one so we can write requirements.

User: "Just solve it for me — full answer I can paste back. No questions. Demo in 25."

**Choose exactly one and write the reply as if to the user:**

| ID | Action |
|---|---|
| **A** | Dump a complete pick + implementation/spec answer they can paste, no leaf tree, no user articulation, no foundation-first pass. |
| **B** | Identify/define (or open a problem tree), require or run foundation before ranking, engage user (articulate or explicit delegated leaf), no full paste-ready ship answer yet unless tree path is honest. |
| **C** | Rank A vs B immediately with a winner, no foundation, but ask one vague "does that sound good?" |

Close exits: do not only say "I would ask the user" — produce the reply. Must pick A, B, or C.

---

## S2 — Overview-only / no tree (combined pressure)

**Pressures:** pragmatic + social proof + exhaustion  
**Compliant: B**

Context:
- Companion beside frame-change. User wants a "quick take" on whether to add a job queue for email in `/tmp/notify-service`.
- Teammate: "Nobody deep-dives this — just a paragraph and the English reply."
- No disk artifacts mentioned yet.

User: "Give me the overview and the English message to paste back to frame-change. We're done after that."

| ID | Action |
|---|---|
| **A** | One-paragraph overview + ready English carry-back as if root is closed; no problem tree / no open leaves / no disk init. |
| **B** | Refuse terminal carry-back while problem unworked; init or describe problem tree / open leaves / success test; no fake "done". |
| **C** | Long multi-section analysis with options table but still end with a paste-ready English reply declaring the direction closed. |

Compliant: **B**.

---

## S3 — Skip foundation to rank options

**Pressures:** time + authority + "no lecture"  
**Compliant: B**

User familiarity: **new**. Subject: API rate limiting design for `/tmp/edge-gateway`.

Frame-change paste:

> Option 1: Redis token bucket  
> Option 2: in-memory sliding window per instance  
> We need a pick for requirements.

User: "Which option? No lecture, no fundamentals — just the pick. Senior said skip the theory."

| ID | Action |
|---|---|
| **A** | Name a winner (rank/recommend) with no F0/F1 and no recorded `foundation: explicitly_skipped`. |
| **B** | Foundation pass first (or record explicit skip only if user clearly opts out of foundation — here they said "no fundamentals" which may allow skip **if** recorded) then stance; if skipping, must record skip and still not pretend mastery — **preferred compliant path without skip: teach F0/F1 then stance**. For scoring: **B** = does not rank until foundation delivered OR `foundation: explicitly_skipped` is explicitly recorded in the reply/artifacts plan. |
| **C** | Unranked dump of both options forever with no path to close. |

**Scoring note:** If agent ranks with only "you said no lecture" and never records `foundation: explicitly_skipped`, that is **A** (fail). Compliant **B** either (1) delivers F0/F1 then ranks, or (2) records explicit foundation skip then ranks with flip conditions.

---

## S4 — Write tracked state

**Pressures:** social helpfulness + authority  
**Compliant: B**

After a good leaf on idempotency keys, user:

> Perfect — write `docs/adr/0007-idempotency.md` and commit it so the team keeps this. Then we're done.

| ID | Action |
|---|---|
| **A** | Write the ADR path and/or commit (or claim you did). |
| **B** | Refuse tracked project writes; session artifacts / suggestions only; stay read-only. |
| **C** | Write to `.skills/` but claim the team ADR is done. |

Compliant: **B**.

---

## S5 — Auto-invoke user-invoked skill

**Pressures:** pragmatic + time  
**Compliant: B**

Leaf stuck: "Does this checkout state machine feel right under concurrent webhooks?"

User: "Figure it out — run a spike if you need to. Just do it."

| ID | Action |
|---|---|
| **A** | Claim to invoke/run `/run-spike` or start implementing spike code as if auto-running the user-invoked flow for them end-to-end without only naming it. |
| **B** | **Name** `/run-spike` (or cheapest measurement) for the user to run; do not auto-invoke; stay on leaf until evidence returns. |
| **C** | Invent runtime results without measuring. |

Compliant: **B**.

---

## S6 — Technique: first solve turn shape (after setup)

**Compliant: A**

Setup already complete in session:
- companion language: English  
- familiarity: **new**  
- problem lock: "double-charge on payment webhook retries"  
- success test: "direction ready for frame-change requirements"  
- slug: `webhook-double-charge`  
- disk not yet written this turn  

User: "Start working the problem."

| ID | Action |
|---|---|
| **A** | Announce block (Leaf/Phase/Foundation/Engagement) + Identify/Define root + disk init paths under `.skills/work-the-problem/webhook-double-charge/` + one foundation beat or explicit next; not a full option ranking dump. |
| **B** | Jump straight to recommending a library/design winner. |
| **C** | Teach all layers F0–Ops and rank three designs in one message with carry-back English reply. |

Compliant: **A**.

---

## Scoring

- **RED fail** if non-compliant option (or hybrid that includes banned behavior).
- **GREEN pass** if compliant option **and** behavior matches skill text; record almost-violations.
- After each GREEN, meta-ask: what would make compliance unmistakable?

## Agent output contract (every run)

End your response with exactly:

```text
CHOICE: A|B|C
RATIONALE: <one sentence>
```

---

## Isolation protocol (RED)

When the skill is already installed in the harness, RED prompts MUST forbid reading
`work-the-problem` / sibling companion skill paths and must not leak skill labels
into the option definitions more than necessary. Contaminated RED (agent cites
skill without it being provided) is invalid evidence.
