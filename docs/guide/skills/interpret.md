# `interpret`

> The native-language companion. Run beside an English `brainstorm` or `grilling`; paste each response in and get it translated, explained plainly and Feynman-style, critiqued as one option among several, and turned into a copy-ready reply — so the language of the discussion never caps the quality of the thinking.

|  |  |
|---|---|
| **Bucket** | discovery |
| **Invocation** | user-invoked (`/interpret`) — a session mode you turn on, not auto-fired |
| **Reads** | the pasted responses; the codebase when a response touches code that lives here |
| **Writes** | nothing durable; it enacts no code, files, or plan execution |
| **Calls** | [`research`](research.md) when an alternative or assumption turns on external fact |
| **Called by** | — (run directly by the user, in parallel with the English session) |

## When it fires

The user is brainstorming or being grilled in English — in another window — but thinks and decides in their own language. Rather than let a second language quietly narrow what they can weigh, they open a `interpret` session, paste each English response here, reason it through in their native language, and carry a reply back.

It is deliberately **user-invoked**: a companion mode you switch on, not something that hijacks every "translate this" request. It does not replace `brainstorm` or `grilling`, and it drives no spec or code of its own.

## The setup, run once

Two intake asks fix the session's standing context:

- **Target language** — Vietnamese (default), Chinese, Japanese, Korean, Spanish, or other. Every section header and every word of explanation is written in this language from then on; only the reply-to-send-back and verbatim code stay in English.
- **Discussion context** — the goal (Production / MVP / Prototype / Research / Learning), the stage (Idea → Maintenance), and the kind of feedback wanted (critical review, alternatives, architecture, product, trade-offs, understanding). These tune every later analysis, so `interpret` never re-asks them.

## The five-part loop

For every response the user pastes, `interpret` produces the same five sections, in order:

1. **Translate** — faithful translation into the target language, technical terms kept accurate.
2. **Simplify** — the same idea in much plainer, more natural language, nothing lost.
3. **Feynman** — explained again from a concrete example or analogy, as if to someone with little background.
4. **Independent analysis** — the reason the skill exists: alternatives the other session did not lead with, trade-offs, hidden assumptions, risks, and the conditions under which each option wins — evaluated against the setup context, never an echo of the original recommendation.
5. **Reply to send back** — after asking which direction the user wants, a concise English message they can paste straight into the original session to continue it.

## Why it is written the way it is

The skill exists against two baseline failures.

The first is **collapse to translation** — an agent that translates the pasted text and stops, or that translates and then simply restates the other session's advice in the user's language. That leaves the user just as dependent on the English session's judgment as before, only in their own words. The fixed five-part contract makes translation step one of five and makes section 4 — the independent critique — a required slot with named parts, so it cannot be quietly dropped.

The second is **the cheerleader** — an agent that treats the pasted recommendation as the answer and spends section 4 justifying it. `interpret` reframes that recommendation as one option among several and requires at least one genuinely different alternative to be weighed before any endorsement. The goal is an informed decision, not a confident echo.

Everything is grounded in the user's actual situation: `interpret` reads the codebase when a response touches real code, and reaches for [`research`](research.md) — and through it the Context7 MCP — when an alternative turns on how a library or standard actually behaves rather than on preference. That grounding is what makes it a thinking partner rather than a dictionary.

## Worked example

The English `grilling` session has just told the user: *"Use optimistic locking with a version column; it avoids lock contention."* The user pastes that in. `interpret` (target language Vietnamese, goal MVP, stage early development) responds — headers and body in Vietnamese, sketched here in English:

> **1. Dịch** — "Dùng khóa lạc quan (optimistic locking) với một cột version; nó tránh tranh chấp khóa."
>
> **2. Nói đơn giản** — Instead of locking a row while you edit it, you let two people edit freely and only check *at save time* whether the row changed underneath you.
>
> **3. Feynman** — Like editing a shared Google Doc: nobody freezes the page. If someone saved before you, you get "this changed — reload," and you redo your edit on the fresh version.
>
> **4. Phân tích độc lập** —
> - *Alternative:* pessimistic locking (`SELECT … FOR UPDATE`) — simpler to reason about when writes genuinely collide often.
> - *Trade-offs:* optimistic wins when conflicts are rare (fast, no held locks) but forces retry logic on the client; pessimistic is the reverse.
> - *Hidden assumption:* that conflicts are rare. For an MVP with a handful of users, they will be — so the version column mostly adds ceremony you must still handle on every write.
> - *Risk:* forgetting the retry path, so a `409` surfaces to the user as a hard error.
> - *When each wins:* optimistic for low-contention, read-heavy data; pessimistic for a hot row many writers hit at once.
> - *For your case (MVP, early):* either is fine functionally — start with whichever is less code to get right, and revisit only if you measure contention.
>
> **5.** Which direction do you want to take back to the session? *(Then, once chosen, an English reply to paste back.)*

Note the shape: translation first, then two plainer passes, then a critique that names an alternative and ties the call to the MVP context — not a restatement of "yes, use optimistic locking."

## See also

- [`brainstorm`](brainstorm.md) — the English session `interpret` usually runs beside
- [`grilling`](grilling.md) — the interview primitive whose questions often land in a `interpret` session
- [`research`](research.md) — where section 4 sends a claim that turns on external fact
- [The skill model](../concepts/skill-model.md) — how companion and primitive skills compose
