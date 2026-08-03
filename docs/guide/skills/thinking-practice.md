# `thinking-practice`

> Native-language **thinking practice** beside discovery or technical work. It equips grounded territory, named unknowns, question scaffolds, and evidence calibration — **without recommending a choice**. When you explicitly switch from training to shipping, it emits a neutral `thinking-handoff/v1` packet for [`interpret-session`](interpret-session.md) and terminates. What it owes you is material you can think with, so the model does not own the judgment.

|  |  |
|---|---|
| **Bucket** | discovery |
| **Invocation** | user-invoked (`/thinking-practice`) — a session mode you turn on, not auto-fired |
| **Reads** | pasted content or direct hypotheses; the codebase when territory touches real code; optional `research` notes |
| **Writes** | nothing tracked; may disclose git-ignored `.skills/research/` notes only via `research` |
| **Calls** | [`research`](research.md) when a named external unknown has an owning source |
| **Called by** | — (run directly by the user; may run parallel to an English discovery/technical session) |
| **Hands off to** | [`interpret-session`](interpret-session.md) via `thinking-handoff/v1` only |

## When it fires

You are doing real discovery or technical work — often beside an English `frame-change`, `clarify-decisions`, or co-brainstorm — and the risk is **cognitive offloading**: following the other agent's pick instead of owning the reasoning. You open `/thinking-practice`, work in your language, and stay in training until *you* open the gate.

It does **not** replace interpret-session. Use interpret when you want a committed stance and an English reply to paste back. Use thinking-practice when you want to train judgment: facts, unknowns, good questions, and calibration against evidence.

## The setup, run once

- **Target language** — all analysis labels and explanation; code/paths/ids stay verbatim.
- **Project posture** — reuses delivery intent + lifecycle from `docs/agents/project.md` when present (same as interpret-session); asks only when absent.

No “feedback wanted” intake that steers a review persona — this skill equips thinking, not a second opinion.

## Shape follows the message

| Message | Output |
|---|---|
| Paste from another session | Adaptive evidence/understanding pass |
| Direct hypothesis or question | Territory, claim map, unknowns, checks, question scaffold |
| Follow-up / challenge | Direct answer |
| Evidence return | User-first calibration (after-loop) |
| Explicit hand-off | Path A checkpoint or Path B escape → packet → **terminate** |
| Session end (no evidence cycle) | One soft reflection; dual-status close block |

**Iron laws (summary):** never encode a preferred choice *anywhere* in this skill; never invent options/unknowns to fill a template; never auto-switch train→ship from urgency or deadlines; never claim learning-complete or ship-ready from single-session proxies. A hand-off **terminates** the skill — there is no post-gate recommendation mode here.

## Gate — dual path, hand-off only

- **Path A:** user-authored checkpoint (`position_kind`, `position`, `basis`, `open_or_ask`) then neutral packet.
- **Path B:** unambiguous ship escape; checkpoint `explicitly_skipped`; missing list only among `position` / `basis` / `open_or_ask` that are actually absent.

Ambiguous “just finish this” + demo pressure does **not** open the gate. Stance, ranking, recommendation, dissent, and English reply stay with interpret-session.

Packet contract: skill-local `references/thinking-handoff-v1.md` (field-level provenance required).

## After-loop

When material is the result of a **named check** (or bears on a named hypothesis) with source and scope, the skill hard-triggers calibration: qualify evidence → ask what held/broke → audit → update open map → never recommend. Skip is allowed; status becomes `reflection explicitly skipped` (not `calibrated`). Other agents' opinions are source claims, not evidence alone.

## Session status (v1)

Two axes, not dual “success”:

- **Hand-off:** not requested → … → delivered | closed without hand-off  
- **Calibration:** not reached → … → calibrated | reflection explicitly skipped | …

Operational done when a Path A/B packet is **delivered**, or you end training with the open map named.

## Why it is written the way it is

Baselines without the skill, under combined pressure (deadline + senior + “just tell me which”), pick an option or skip reflection and recommend. With the skill, the same scenarios stay equip-only or run the after-loop. Path B ambiguous language stays in training; only an explicit escape emits a neutral packet. Evidence lives in the skill’s `TESTS.md`.

## See also

- [`interpret-session`](interpret-session.md) — stance + English reply; receives `thinking-handoff/v1`
- [`research`](research.md) — external owning-source facts
- [`run-spike`](run-spike.md) — user-invoked throwaway check; evidence can return here for calibration
- [`clarify-decisions`](clarify-decisions.md) / [`frame-change`](frame-change.md) — common other-window discovery skills
- [Discovery phase](../process/discovery.md) — where companion sessions sit in the chain
