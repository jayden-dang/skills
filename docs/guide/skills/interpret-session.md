# `interpret-session`

> The companion session beside `frame-change` / `clarify-decisions` (or any parallel technical window). Choose **English** as a second-opinion debate partner, or a **native language** to think and decide in L1 — a mental model you can reason with, then a committed stance, then a carry-back reply once you settle. What it owes you is a decision you own and can defend, not a set of sections.

|  |  |
|---|---|
| **Bucket** | discovery |
| **Invocation** | user-invoked (`/interpret-session`) — a session mode you turn on, not auto-fired |
| **Reads** | the pasted responses; the codebase when a response touches code that lives here |
| **Writes** | nothing in the product repo; it enacts no code, files, or plan execution. One optional gitignored note at `.skills/interpret-session/<slug>/model.md`, offered once and written only if the user asks |
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

- **A paste from the other session** — live-choice: the fork, the lean, the graph you must hold, one walk, the pick. No-choice: the short path.
- **A message addressed to `interpret-session`** — a follow-up, a challenge, a new fact, "research this", thinking aloud. Gets a direct answer in the thread: no translation section, no re-explaining, no reply-to-send-back. If the new information moves the stance, the skill leads with that.
- **A settled direction** — an explicit decision, or "write the reply". Only this produces the English reply.

For a paste that puts a **live choice** on the table, the turn **is** the card,
and its bar is that the user can retell it in three sentences with no hop taken.
The first two lines are the **fork** (one sentence that distinguishes the options)
and the **lean** (the shape plus the repo fact that decides it, marked not locked).
Then the **graph** of parts the question stands on (how they connect, where the
picture stops, one system diagram); **one walk** of a named person through that
graph; the **full pick** with each loser judged on the same fact; **where the
paste disagrees with the code**, as facts with `file:line`; **what a `0` would
freeze**, as commitments; and a **fence** for what this card does not decide.
Facts and commitments are two headings because a user does not confirm a fact.
The first live-choice of a session also carries a four-line note on how to read
the card; later ones do not repeat it.

Today / Architect / the seven stance slots are computed, not shown. **Go deeper**
is two hops — the system in more detail, then the `file:line` walk — then `0`
writes the carry-back. Every heading and menu label the user reads is a question
in the companion language: `Gist`, `Lock strip`, `Fence`, `Deeper` and `Lowest`
are the skill's internal names and never appear on the card.

Nothing durable is emitted on a schedule. When the user asks for the picture they
could carry into a coding session — or after the third live-choice on the same
neighborhood — the companion makes **one** offer to write a **model note**: the
four-to-seven-part picture, the locks the user already settled, what is still
open, and what the paste got wrong, with `file:line` on every code claim. It is
off by default, written only on a yes, and lands at
`.skills/interpret-session/<slug>/model.md`; the product repo is untouched unless
the user names a path. A tour of the whole system is [`tour-system`](tour-system.md),
and a foundation with no pick is [`deepen-codebase`](deepen-codebase.md).

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

A 2026-08 field session added the volume-calibration rules. Over ten decision cards the companion worked exactly as designed — it verified claims against the repo and caught real defects in the other window's cards — but the carry-back blocks grew from seven bullets to seventeen, every stance read "high" confidence, and the user's approvals shrank to a single word with the rationale question skipped five times. Each behavior was locally fine; the sum was decision laundering by volume — the user was approving blocks they could no longer be weighing. Hence the Decision / Suggested-guards split in the carry-back, the calibrated confidence line, the Agree / Amend / Reject diff, the skip-streak adaptation, and the digest offered on an export request. (That session's cumulative knowledge map has since become the opt-in model note described above — emitted on request, not on a count.)

A 2026-09 baseline on v1.4.0 showed the remaining gap: under a two-minute standup the companion *correctly* led with the pick, because the skill required it — so the user got the letter C before they could say what actually changed or why the runner-up lost. Asking "explain this more simply" already produced the better session (a stable analogy, then the architecture). v1.5.0 makes that order the default: comprehension, then the seven-slot stance, then handles to challenge it. The no-choice short path is unchanged.

Two further rounds cut what the user was reading. v3.0.0 moved Today, the architect comparison and the seven stance slots off turn 1 into the depth hops, because a ten-card field session showed the user asking for the card and the pick again, more simply, and then never taking a hop. v3.1.0 finished the job on the layer they read. The card still failed for two reasons that had nothing to do with which blocks were shown: its headings were the skill's own protocol (`Gist`, `Lock strip`, `Fence`) — a second vocabulary to learn before you can read your own decision — and the pick sat behind the whole argument, so a reader scanning the first screen could not tell what was being chosen or which way the session leaned. So the headings became questions in the companion language, the fork and the lean became the first two lines, and paste-vs-repo corrections got their own heading, separate from what a `0` would freeze — because a user does not confirm a fact, and a correction mixed into a list of things to approve arrives as something to approve. The first card of a session also explains in four lines how to read itself, since progressive disclosure that depends on the user taking a hop is not disclosure at all when nobody takes one. And because every picture used to die with the session, the model note exists to carry the four-to-seven-box picture plus the locks already settled into the next session — off by default, offered once, and never written into the product repo unless the user names the path.

Everything is grounded in the user's actual situation: `interpret-session` reads the codebase when a response touches real code, and reaches for [`research`](research.md) — and through it the Context7 MCP — when an alternative turns on how a library or standard actually behaves rather than on preference. That grounding is what makes it a thinking partner rather than a dictionary.

## Worked example

The other window has just pasted three shapes for a webhook relay's retry policy:
per-endpoint `maxAttempts` / `baseDelay` fields, a circuit breaker on top of the
existing global constants, or per-endpoint policy plus a global ceiling on the
drain loop. It recommends the first, "purely additive", and states that the relay
retries three times on a fixed one-second delay. **In a real session every heading
and every line below is written in the user's chosen companion language** — it is
English here because this guide is:

> **What this session is about**
> - **The problem:** one slow endpoint delays every other endpoint's deliveries, and the other window wants retry policy made configurable.
> - **What we'll settle here:** where retry policy lives — per endpoint, or bounded globally. The reply that leaves carries that one decision.
> - **What we have:** `src/retry.ts`, `src/drain.ts`, `src/store.ts` and their history; posture MVP / Early / compat None.
> - **What we don't have yet:** whether any endpoint actually needs a different bound. Nobody in the thread holds that number; the choice between per-endpoint and global turns on it.
>
> How to read this card:
> 1. The first two lines are what is being chosen, and which way I lean
> 2. The picture is the system around the decision, not the options
> 3. "I'd pick" locks nothing — 0 is what writes the reply that goes back
> 4. 1 = the system in more detail · 2 = walk it file by file
>
> **What is being chosen**
> Whether each endpoint carries its own retry bound, or the bound stays one number the whole drain loop shares.
>
> **Which way I lean** (not locked)
> Keep one bound and add the ceiling on the loop. The loop is sequential (`src/drain.ts:7`), so per-endpoint tuning cannot stop one endpoint from delaying the rest.
>
> **Hold this picture**
> - "how many times we retry" → `shouldRetry` + `MAX_ATTEMPTS = 5` (`src/retry.ts:4`, `:13-15`) → the bound, exponential with jitter
> - "one pass over everything pending" → `drain` → sequential `for` loop, awaits each delivery
> - "what a delivery remembers" → `Delivery.attempt` → per-row counter, no global counter exists
> - "what an endpoint knows" → `Endpoint` (`src/store.ts:10`) → id, url, secret — no retry fields today
>
> Where the picture stops: this is one relay process. It says nothing about two relays draining the same queue.
>
> ```
> Endpoint { id, url, secret }      no retry fields today
>       |
>       v
> drain() — sequential for-loop over pending      [*] where the ceiling would land
>       |
>       +--> shouldRetry(attempt, status) — MAX_ATTEMPTS = 5, 429 + 5xx   [!] bounded since the 2026-05 stall
>       |
>       `--> save() — per-delivery attempt counter, no global ceiling
> ```
>
> **One person walking through it**
> Ren has one endpoint returning 503 all morning.
> Today: each delivery to it burns 5 attempts with exponential backoff, and because the loop is sequential every other endpoint waits behind it.
> Under per-endpoint fields: Ren can set that endpoint to 1 attempt — but only once someone notices and edits it, and every other endpoint still waits during the attempt.
> Under a loop ceiling: the pass stops spending time on the bad endpoint whether or not anyone tuned it.
>
> **Why not the other one**
> I'd pick the ceiling on `drain`, because the guarantee the code makes today is a bounded pass (`src/retry.ts:4`, `src/retry.ts:13-15`), and the bound the incident set was about the loop, not about one endpoint.
> Not per-endpoint fields alone: they are additive, and they leave the shared loop exactly as slow.
> Not the circuit breaker alone: it parks an endpoint after the damage, and needs consecutive-failure state nothing in `store.ts` keeps yet.
> Who it hits: whoever operates the relay. No API consumer changes.
>
> **Where the paste disagrees with the code**
> The paste says three attempts on a fixed one-second delay; `src/retry.ts:4-5` sets `MAX_ATTEMPTS = 5` with a 250 ms base, and `src/retry.ts:8-11` is exponential backoff with full jitter.
> The paste calls option A purely additive; the commit that bounded attempts records the 2026-05 stall, so the bound is a decision this fork would reopen, not empty space.
>
> **If you confirm, this freezes**
> The retry bound stays one number, and the ceiling lands on the drain loop rather than on endpoint config.
> Accepted cost: an endpoint that genuinely needs a different bound has no way to say so until someone reopens this.
>
> **This card does not decide**
> Whether the drain loop becomes concurrent per endpoint. The paste implies it; this card does not answer it.
>
> **Go deeper**
> 1 · The system in more detail — what the 2026-05 commit bounded, and what the sequential loop costs
> 2 · Walk it file by file — `drain.ts:7` through `shouldRetry` with the numbers
> ───
> 0 · Write the reply to carry back

A reader who stops after the first two lines already knows the fork and the lean.
A reader who also holds the four boxes can retell the system to tomorrow's coding
session — which is the bar the card is written to. The reply back to the other
window comes later, on the turn the user actually settles it.

## See also

- [`deepen-codebase`](deepen-codebase.md) — sibling learning companion (any subject foundation); may share an optional knowledge-only `foundation-note/v1`
- [`work-the-problem`](work-the-problem.md) — multi-round deep solve + in-service teaching + disk artifacts when overview is not enough
- [`frame-change`](frame-change.md) — the English session `interpret-session` usually runs beside
- [`clarify-decisions`](clarify-decisions.md) — the interview primitive whose questions often land in a `interpret-session` session
- [`research`](research.md) — where the analysis sends a claim that turns on external fact
- [The skill model](../concepts/skill-model.md) — how companion and primitive skills compose
