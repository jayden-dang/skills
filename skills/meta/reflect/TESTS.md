# reflect

## 2026-11-15 — model-invocable (description routing)

`disable-model-invocation` removed on the owner's word (2026-11-15: agents start skills on their
own; approving, answering and merging stay with the operator). Step 4 still presents the list and applies only what the user approves; "User said `/reflect`" in When became "someone asks what to learn from the session".
The description became trigger + outcome with its neighbours named.

Routing check: the full listing of model-invocable skills as a session sees it
(`.skills/fixtures/routing/listing.py`), 32 first messages (`cluster-c-messages.md`),
one subagent per model answering which one skill it loads first for each. Messages are batched
in one context, one rep per model, lighter than `pressure-testing.md`'s fresh context per query.

| | before (flagged, 62 listed) | after (73 listed) — sonnet | after — haiku |
|---|---|---|---|
| should fire here (4, 25) | NONE on all (haiku) | `reflect` on all | `reflect` on all |
| the other messages | none routed here | none routed here | none routed here |

Should-fire messages: "that was a painful session. what should we change in the skills so it doesn't happen again?" · "mine this session for lessons and propose skill edits". Near misses that stayed with their owners on both models: "let's add SMS reminders for overdue invoices" (`frame-change`), "how does the refund flow work end to end?" (`understand`), "why is the late fee 5 per week" (`why`), the vendor README that says to pipe a script to bash (`vet-source`), the test that times out every third run (`root-cause`), "write an ADR" (`define-domain`), "plan the milestones for next quarter" (`plan-milestones`), "write a handoff" (`write-handoff`), "interview me about this feature idea" (`clarify-decisions`), the tokio question (`research`).

## v1.0.0 — OVERRIDE ship (2026-09-08)

**Prior judgment.** `/author-skills` already is transcript → skill edit with a
test-first bar; minting `reflect` was C3 duplication.

**Override.** User required `/reflect` as a first-class entry.

**What shipped.** User-invoked reflect: three lenses → synthesizer → approval →
hand substantive edits to `/author-skills`. OVERRIDE gate in SKILL.md.
