# `interpret-session`

> The native-language companion. Run beside an English `frame-change` or `clarify-decisions`; paste each response in and get it translated, explained plainly, and answered with a committed second opinion — then, once you have decided, an English reply to carry back. What it owes you is not a set of sections but a decision you own and can defend, so the language of the discussion never caps the quality of the thinking.

|  |  |
|---|---|
| **Bucket** | discovery |
| **Invocation** | user-invoked (`/interpret-session`) — a session mode you turn on, not auto-fired |
| **Reads** | the pasted responses; the codebase when a response touches code that lives here |
| **Writes** | nothing durable; it enacts no code, files, or plan execution |
| **Calls** | [`research`](research.md) when an alternative or assumption turns on external fact |
| **Called by** | — (run directly by the user, in parallel with the English session) |

## When it fires

The user is frame-changeing or being grilled in English — in another window — but thinks and decides in their own language. Rather than let a second language quietly narrow what they can weigh, they open a `interpret-session` session, paste each English response here, reason it through in their native language, and carry a reply back.

It is deliberately **user-invoked**: a companion mode you switch on, not something that hijacks every "translate this" request. It does not replace `frame-change` or `clarify-decisions`, and it drives no spec or code of its own.

## The setup, run once

Three intake asks fix the session's standing context:

- **Target language** — Vietnamese, Chinese, Japanese, Korean, Spanish, or any other; no language is privileged as a default, and when the user has already written in theirs the skill proposes that one for a one-tap confirm. Every section header, label, and word of explanation is written in this language from then on; only the reply-to-send-back and verbatim code stay in English.
- **Project posture** — the delivery intent (Production / MVP / Run Spike / Research / Learning) and lifecycle stage (Idea → Maintenance). `interpret-session` *reuses* these from the **Project posture** section of `docs/agents/project.md` when it is present — reading, not re-asking — and only falls back to asking when the repo has no posture recorded. They tune how hard the analysis leans on migration, backward-compat, and deprecation.
- **Feedback wanted** — critical review, alternatives, architecture, product, trade-offs, or understanding. This one is per-session, so it is always asked. Answers become standing session context and are not re-asked.

## Shape follows the message

An interpret-session session is one conversation, not a queue of independent pastes. Each message the user sends is one of three kinds, and the skill decides which before writing anything:

- **A paste from the other session** — gets the understanding pass plus a stance.
- **A message addressed to `interpret-session`** — a follow-up, a challenge, a new fact, "research this", thinking aloud. Gets a direct answer in the thread: no translation section, no re-explaining, no reply-to-send-back. If the new information moves the stance, the skill leads with that.
- **A settled direction** — an explicit decision, or "write the reply". Only this produces the English reply.

For a paste that puts a **live choice** on the table, the stance comes *first* — pick, the one dominant reason, confidence, what would flip it, and where it lands relative to the other session — because the user may be reading with two minutes before a standup. Then the understanding pass: a faithful **translation**, and one **explain** pass in plain language built from a single concrete example. Then the detail behind the stance: alternatives the other session did not lead with, trade-offs, hidden assumptions, risks, and when each option wins.

For a paste that puts **no choice** on the table — a procedural question, a confirmation, a status line — there is no alternatives table, no trade-off matrix, no risk list. Just what it means, what it is really asking, and either the answer to give or the one thing worth settling first.

The English reply is a **terminal action, not the close of a turn**. The skill never ends an analysis turn with a menu of directions; while something material is unresolved it names what is still open and stops. When the reply is written, it is round-tripped — one or two lines in the user's own language stating what that English commits them to.

## It carries through the approval gates

The companion session does not end when the frame-change does. `specify-behavior` and `design-solution` both **present the artifact and stop**, waiting on the user — and that is where an English-language spec meets a reader who decides in another language, with the stakes at their highest: criterion IDs go immutable on approval, and every later task, test, and commit cites them.

`interpret-session` needs no extra machinery for this, which a baseline run confirmed: handed a `requirements.md`, it walks the criteria, keys its findings to IDs, and checks each one against **its own ledger of what the user actually decided earlier in the session**. That last check is the one no other reviewer can run — a criterion contradicting a recorded decision, and a decision no criterion covers, are both invisible to anyone who was not in the discussion. The one rule the phase added is that an approval which freezes identifiers must be named as such before it is given.

The boundary is firm: `interpret-session` never edits the spec, never sets `Status: Approved`, never emits or renumbers IDs, and never runs `audit-trace`. It helps the user form the verdict; the verdict itself happens at the gate the spec skill owns.

## Why it is written the way it is

The skill exists against two original baseline failures. The first is **collapse to translation** — an agent that translates the pasted text and stops, or that translates and then restates the other session's advice in the user's language, leaving them just as dependent on the English session's judgment as before. The second is **the cheerleader** — an agent that treats the pasted recommendation as the answer and spends the analysis justifying it. `interpret-session` reframes that recommendation as one option among several and requires a genuinely different alternative to be weighed before any endorsement.

A later baseline run on the v1 text surfaced a third failure, and it is the reason the shape is now conditional. Handed a paste with no decision in it — *"Sounds good — want me to write the requirements for that now?"* — v1 produced a thousand words: a Feynman analogy, a four-option comparison table of job-queue libraries, trade-offs, risks, when-each-wins, and then the hedge *"both are reasonable — it's your call."* The fixed five-slot contract **demanded** an alternatives-and-trade-offs analysis where no choice existed, so the agent invented four options it had no basis to choose among, and then had to refuse to pick. The fake balance and the padding were one defect with one cause: unconditional structure. Hence the split between a paste that puts a live choice on the table and one that does not, and hence the Iron Law's two halves — never manufacture a choice, never withhold your pick on a real one.

Two further findings shaped smaller rules. Across every run, v1 closed its analysis with a three-or-four-item menu of directions, because the reply was section 5 of a loop and the skill needed a decision to emit it — so the reply became a terminal action gated on convergence instead. And when the user overrode the recommendation with no reason given, v1 complied in total silence: it recorded the decision and wrote the reply without once saying it still disagreed. Hence **dissent, then comply** — one objection, at most two sentences, naming what it expects to go wrong and the earliest signal, and then no re-litigating.

Everything is grounded in the user's actual situation: `interpret-session` reads the codebase when a response touches real code, and reaches for [`research`](research.md) — and through it the Context7 MCP — when an alternative turns on how a library or standard actually behaves rather than on preference. That grounding is what makes it a thinking partner rather than a dictionary.

## Worked example

The English `clarify-decisions` session has just told the user: *"Use optimistic locking with a version column; it avoids lock contention."* The user pastes that in. `interpret-session` (posture MVP, early development) responds. **In a real session every header and every word below is written in the user's chosen language** — the example is shown in English only because this guide is in English:

> **My stance**
> - *What I'd do:* pessimistic locking (`SELECT … FOR UPDATE`) for the first pass.
> - *Why:* at MVP scale with a handful of users, conflicts essentially don't happen — so what you're really choosing is which path has less code you must get right, and that's pessimistic.
> - *How sure:* medium.
> - *What would flip me:* if this table is read-heavy with one hot row many writers hit at once — measurable from your logs in ten minutes. Measure before committing.
> - *Versus the other session:* they aren't technically wrong, but the reason they gave ("it avoids lock contention") solves a problem you don't have yet.
>
> **Translate** — "Use optimistic locking with a version column; it avoids lock contention."
>
> **Explain** — Instead of locking a row while you edit it, you let two people edit freely and only check *at save time* whether the row changed underneath you. Like a shared Google Doc: nobody freezes the page, but if someone saved before you, you get "this changed — reload" and redo your edit on the fresh version.
>
> **The detail behind it**
> - *Alternative:* pessimistic locking — simpler to reason about when writes genuinely collide often.
> - *Trade-offs:* optimistic wins when conflicts are rare (fast, no held locks) but forces retry logic on the client; pessimistic is the reverse.
> - *Hidden assumption:* that conflicts are rare — true for your MVP, which is exactly why the version column mostly adds ceremony you still have to handle on every write.
> - *Risk:* forgetting the retry path, so a `409` surfaces to the user as a hard error.
> - *When each wins:* optimistic for low-contention, read-heavy data; pessimistic for a hot row many writers hit at once.

Note the shape: the pick comes first, with a confidence level and the one measurement that would change it, so a user with two minutes gets the answer and a user with twenty gets the reasoning. There is **one** explain pass, not two. And the turn ends on the open measurement — not on "which direction do you want?" The English reply comes later, on the turn the user actually settles it.

## See also

- [`frame-change`](frame-change.md) — the English session `interpret-session` usually runs beside
- [`clarify-decisions`](clarify-decisions.md) — the interview primitive whose questions often land in a `interpret-session` session
- [`research`](research.md) — where the analysis sends a claim that turns on external fact
- [The skill model](../concepts/skill-model.md) — how companion and primitive skills compose
