# TESTS.md — assess-pivot-impact

## 2026-11-15 — model-invocable (description routing)

`disable-model-invocation` removed on the owner's word (2026-11-15: agents start skills on their
own; approving, answering and merging stay with the operator). After the user has confirmed the ledger it now calls `define-project` (update) as a sub-skill instead of naming it. That hand-off was not run end to end.
The description became trigger + outcome with its neighbours named.

Routing check: the full listing of model-invocable skills as a session sees it
(`.skills/fixtures/routing/listing.py`), 32 first messages (`cluster-c-messages.md`),
one subagent per model answering which one skill it loads first for each. Messages are batched
in one context, one rep per model, lighter than `pressure-testing.md`'s fresh context per query.

| | before (flagged, 62 listed) | after (73 listed) — sonnet | after — haiku |
|---|---|---|---|
| should fire here (7, 28) | NONE on all (haiku) | `assess-pivot-impact` on all | `assess-pivot-impact` on all |
| the other messages | none routed here | none routed here | none routed here |

Should-fire messages: "we're pivoting from marinas to parking garages. what happens to what we've already shipped?" · "the new vision contradicts the offline-first feature we shipped. I need a disposition for each feature it touches". Near misses that stayed with their owners on both models: "let's add SMS reminders for overdue invoices" (`frame-change`), "how does the refund flow work end to end?" (`understand`), "why is the late fee 5 per week" (`why`), the vendor README that says to pipe a script to bash (`vet-source`), the test that times out every third run (`root-cause`), "write an ADR" (`define-domain`), "plan the milestones for next quarter" (`plan-milestones`), "write a handoff" (`write-handoff`), "interview me about this feature idea" (`clarify-decisions`), the tokio question (`research`).
