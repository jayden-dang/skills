# `interpret-session`

> The companion session beside `frame-change` / `clarify-decisions` (or any parallel technical window). Choose **English** as a second-opinion debate partner, or a **native language** to think and decide in L1 — a mental model you can reason with, then a committed stance, then a carry-back reply once you settle. What it owes you is a decision you own and can defend, not a set of sections.

|  |  |
|---|---|
| **Bucket** | discovery |
| **Invocation** | user-invoked (`/interpret-session`) — a session mode you turn on, not auto-fired |
| **Reads** | the pasted responses; the codebase when a response touches code that lives here |
| **Writes** | nothing durable; it enacts no code, files, or plan execution |
| **Calls** | [`research`](research.md) when an alternative or assumption turns on external fact |
| **Called by** | — (run directly by the user, in parallel with the other session) |

## When it fires

The user is frame-changeing or being grilled in another window and wants a **companion** mind: either (1) they think in L1 while that window is English, or (2) they want an **English second opinion / debate partner** while the main session is also English (or mixed). They open `/interpret-session`, paste each response here, reason with a committed stance, and carry a reply back.

It is deliberately **user-invoked**: a companion mode you switch on, not something that hijacks every "translate this" request. It does not replace `frame-change` or `clarify-decisions`, and it drives no spec or code of its own.

## The setup, run once

Three intake asks fix the session's standing context:

- **Companion language** — first-class **English** (full critique/debate in English) **or** a native language (Vietnamese, Chinese, Japanese, Korean, Spanish, … / other). No default; when the user already wrote in L1, propose that language but still show English as an equal option. Every section header, label, and word of analysis uses the companion language from then on. Carry-back is usually English for the main window; if companion language ≠ reply language, a short commitment restatement stays in the companion language.
- **Project posture** — the delivery intent (Production / MVP / Run Spike / Research / Learning), lifecycle stage (Idea → Maintenance), and compat obligation (None / Internal / External). `interpret-session` *reuses* these from the **Project posture** section of `docs/agents/project.md` when it is present — reading, not re-asking — and only falls back to asking when the repo has no posture recorded. Delivery intent is the quality bar, not a release state; **compat obligation** is what tunes migration, backward-compat, and deprecation. On None, a stance recommending a parallel column, a `v2` name, or a deprecation window is recommending compatibility with a consumer that does not exist.
- **Feedback wanted** — critical review, alternatives, architecture, product, trade-offs, or understanding. This one is per-session, so it is always asked. Answers become standing session context and are not re-asked.

## Shape follows the message

An interpret-session session is one conversation, not a queue of independent pastes. Each message the user sends is one of three kinds, and the skill decides which before writing anything:

- **A paste from the other session** — live-choice: comprehension then stance. No-choice: the short path.
- **A message addressed to `interpret-session`** — a follow-up, a challenge, a new fact, "research this", thinking aloud. Gets a direct answer in the thread: no translation section, no re-explaining, no reply-to-send-back. If the new information moves the stance, the skill leads with that.
- **A settled direction** — an explicit decision, or "write the reply". Only this produces the English reply.

For a paste that puts a **live choice** on the table, comprehension comes first —
what the card actually decides, in 1–2 plain sentences; one mental model mapped
back to canonical terms; on a real architecture fork, a compact table of the
dimensions that differ — *then* the seven-slot stance (pick, decisive reason,
strongest runner-up, cost accepted, confidence with the check that earned it,
what would flip it, and an **Agree / Amend / Reject** diff). After the stance,
2–4 **pressure-test** questions the user can use to attack the pick. Stance-first
is a format failure even when standup is two minutes; skip the tutorial, not the
model. Depth is a predicate: a simple yes/no stays decision → model → stance; a
complex boundary/state/security card also gets one picture or one scenario and a
decision boundary. Surface the paste as **Translate** or **Restate** only when the
decision sentence is not enough. Detail behind the stance stays: alternatives the
other session did not lead with, trade-offs that add mechanism, hidden
assumptions, risks, and when each option wins. A verified fact still ends with
its consequence; a concept the analysis introduces from outside the repo still
gets its minimal model at first use; implementation-grade constraints still wait
in a *for the spec* tail.

Every third or fourth decision—or whenever the user asks where the system
stands—the companion emits a cumulative **knowledge map**, not merely decision
history. When three or more decisions interact through a flow, boundary, or
dependency, one small system sketch exposes the edges. The table then carries
mechanism, dependency, decisive reason plus accepted cost, evidence/confidence,
and the remaining unknown or reopen trigger.

For a paste that puts **no choice** on the table — a procedural question, a confirmation, a status line — there is no alternatives table, no trade-off matrix, no risk list, and none of the live-choice comprehension slots. Just what it means, what it is really asking, and either the answer to give or the one thing worth settling first.

The carry-back reply is a **terminal action, not the close of a turn**. The skill never ends an analysis turn with a menu of directions; while something material is unresolved it names what is still open and stops. When the reply is written, it is round-tripped — one or two lines in the companion language stating what that message commits them to (still done when both sides are English; never invent an L1 the user did not choose). A lock-carrying reply speaks as the user — the other window reads it as the user's own answer, so it carries no authorship labels, no rationale bookkeeping, and no directing of that window's next step — and is written in three receiver-native slots: **Lock** (what the approval freezes), **Weigh** (proposed constraints the other session tests through its own process), **Still open** (what must not be silently closed). A long block's round-trip names its highest-blast bullets specifically.

## It carries through the approval gates

The companion session does not end when the frame-change does. `specify-behavior` and `design-solution` both **present the artifact and stop**, waiting on the user — and that is where an English-language spec meets a reader who decides in another language, with the stakes at their highest: criterion IDs go immutable on approval, and every later task, test, and commit cites them.

`interpret-session` needs no extra machinery for this, which a baseline run confirmed: handed a `requirements.md`, it walks the criteria, keys its findings to IDs, and checks each one against **its own ledger of what the user actually decided earlier in the session**. That last check is the one no other reviewer can run — a criterion contradicting a recorded decision, and a decision no criterion covers, are both invisible to anyone who was not in the discussion. The one rule the phase added is that an approval which freezes identifiers must be named as such before it is given.

The boundary is firm: `interpret-session` never edits the spec, never sets `Status: Approved`, never emits or renumbers IDs, and never runs `audit-trace`. It helps the user form the verdict; the verdict itself happens at the gate the spec skill owns.

## Why it is written the way it is

The skill exists against two original baseline failures. The first is **collapse to translation** — an agent that translates the pasted text and stops, or that translates and then restates the other session's advice in the user's language, leaving them just as dependent on the English session's judgment as before. The second is **the cheerleader** — an agent that treats the pasted recommendation as the answer and spends the analysis justifying it. `interpret-session` reframes that recommendation as one option among several and requires a genuinely different alternative to be weighed before any endorsement.

A later baseline run on the v1 text surfaced a third failure, and it is the reason the shape is now conditional. Handed a paste with no decision in it — *"Sounds good — want me to write the requirements for that now?"* — v1 produced a thousand words: a Feynman analogy, a four-option comparison table of job-queue libraries, trade-offs, risks, when-each-wins, and then the hedge *"both are reasonable — it's your call."* The fixed five-slot contract **demanded** an alternatives-and-trade-offs analysis where no choice existed, so the agent invented four options it had no basis to choose among, and then had to refuse to pick. The fake balance and the padding were one defect with one cause: unconditional structure. Hence the split between a paste that puts a live choice on the table and one that does not, and hence the Iron Law's two halves — never manufacture a choice, never withhold your pick on a real one.

Two further findings shaped smaller rules. Across every run, v1 closed its analysis with a three-or-four-item menu of directions, because the reply was section 5 of a loop and the skill needed a decision to emit it — so the reply became a terminal action gated on convergence instead. And when the user overrode the recommendation with no reason given, v1 complied in total silence: it recorded the decision and wrote the reply without once saying it still disagreed. Hence **dissent, then comply** — one objection, at most two sentences, naming what it expects to go wrong and the earliest signal, and then no re-litigating.

A 2026-08 field session added the volume-calibration rules. Over ten decision cards the companion worked exactly as designed — it verified claims against the repo and caught real defects in the other window's cards — but the carry-back blocks grew from seven bullets to seventeen, every stance read "high" confidence, and the user's approvals shrank to a single word with the rationale question skipped five times. Each behavior was locally fine; the sum was decision laundering by volume — the user was approving blocks they could no longer be weighing. Hence the Decision / Suggested-guards split in the carry-back, the calibrated confidence line, the Agree / Amend / Reject diff, the cumulative knowledge map, the skip-streak adaptation, and the digest offered on an export request.

A 2026-09 baseline on v1.4.0 showed the remaining gap: under a two-minute standup the companion *correctly* led with the pick, because the skill required it — so the user got the letter C before they could say what actually changed or why the runner-up lost. Asking "explain this more simply" already produced the better session (a stable analogy, then the architecture). v1.5.0 makes that order the default: comprehension, then the seven-slot stance, then handles to challenge it. The no-choice short path is unchanged.

Everything is grounded in the user's actual situation: `interpret-session` reads the codebase when a response touches real code, and reaches for [`research`](research.md) — and through it the Context7 MCP — when an alternative turns on how a library or standard actually behaves rather than on preference. That grounding is what makes it a thinking partner rather than a dictionary.

## Worked example

The English `clarify-decisions` session has just told the user: *"Use optimistic locking with a version column; it avoids lock contention."* The user pastes that in. `interpret-session` (posture MVP, early development) responds. **In a real session every header and every word below is written in the user's chosen language** — the example is shown in English only because this guide is in English:

> **The decision** — When two people edit the same row, do we detect the clash *at save time* from a version the client sent back, or hold a database lock for the whole human edit?
>
> **Mental model** — Like a shared Google Doc: nobody freezes the page, but if someone saved before you, you get "this changed — reload." Plain meaning "check at save, not while editing" → that doc → canonical term: optimistic locking with a `version` column.
>
> | | Detects a stale form across requests? | Simple for a short server mutation? | What you owe the user |
> |---|---|---|---|
> | Optimistic + `version` | Yes | No | A usable `409` + reload |
> | Pessimistic `SELECT … FOR UPDATE` | No (lock is gone before they submit) | Yes | Hold the row the whole time they edit |
>
> **My stance**
> - *What I'd do:* optimistic locking with a `version` column.
> - *Why it wins now:* a human edit spans multiple HTTP requests, so a row lock held only during save cannot detect that the form was read from stale data.
> - *Runner-up:* pessimistic locking (`SELECT … FOR UPDATE`) is simpler for a short server-side mutation, but loses when the client sends back an older snapshot.
> - *Cost I accept:* the MVP needs a clear `409` conflict response and a minimal reload/reapply path.
> - *How sure:* medium — checked the schema and edit flow, but there is no integration proof for the conflict path.
> - *What would flip me:* if every update is computed from a freshly read row inside one short transaction, with no stale client snapshot to write back.
> - *Versus the other session:* **Agree:** keep optimistic locking. **Amend:** it wins because it catches stale human edits, not merely because it avoids lock contention. **Reject:** shipping the column without a usable conflict response.
>
> **Pressure-test**
> - If the client never echoes `version`, does optimistic still catch anything?
> - What is the irreversible cost of teaching users a reload-and-reapply flow now?
>
> **The detail behind it**
> - *Mechanism:* two editors read `version = 7`; the first save advances it to 8, so the second save's `WHERE version = 7` updates zero rows instead of overwriting the first.
> - *Hidden assumption:* the client sends back a snapshot read earlier rather than a server-side mutation calculated from a fresh row.
> - *Risk:* forgetting the retry path, so a `409` surfaces to the user as a hard error.
> - *When each wins:* optimistic for stale forms spanning requests; pessimistic for short server-side mutations that can be completed inside one transaction.

Note the shape: the real decision and one model come first, then the pick,
runner-up, and accepted cost, with a confidence level, the one fact that would
change the choice, and questions the user can use to push back. A user with two
minutes can still skim the stance; they are not asked to sign a letter they
cannot yet defend. There is **one** model, not two. And the turn ends on the
open fact — not on "which direction do you want?" The English reply comes later,
on the turn the user actually settles it.

## See also

- [`deepen-codebase`](deepen-codebase.md) — sibling learning companion (any subject foundation); may share an optional knowledge-only `foundation-note/v1`
- [`work-the-problem`](work-the-problem.md) — multi-round deep solve + in-service teaching + disk artifacts when overview is not enough
- [`frame-change`](frame-change.md) — the English session `interpret-session` usually runs beside
- [`clarify-decisions`](clarify-decisions.md) — the interview primitive whose questions often land in a `interpret-session` session
- [`research`](research.md) — where the analysis sends a claim that turns on external fact
- [The skill model](../concepts/skill-model.md) — how companion and primitive skills compose
