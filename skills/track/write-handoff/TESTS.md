# write-handoff — test evidence

## 2026-11-15 — model-invocable (description routing)

`disable-model-invocation` removed on the owner's word (2026-11-15: agents start skills on their
own; approving, answering and merging stay with the operator). It writes one document to the temp directory and never took its consent from being typed, so the body is unchanged.
The description became trigger + outcome with its neighbours named.

Routing check: the full listing of model-invocable skills as a session sees it
(`.skills/fixtures/routing/listing.py`), 32 first messages (`cluster-b-messages.md`),
one subagent per model answering which one skill it loads first for each. Messages are batched
in one context, one rep per model, lighter than `pressure-testing.md`'s fresh context per query.

| | before (flagged, 52 listed) | after (62 listed) — sonnet | after — haiku |
|---|---|---|---|
| should fire here (5, 25) | NONE on all (haiku) | `write-handoff` on all | `write-handoff` on all |
| the other messages | none routed here | none routed here | none routed here |

Should-fire messages: "I have to stop here for today and I'm only half done. write up where things stand so a fresh session can pick it up" · "context is nearly full. hand this off". Near misses that stayed with their owners on both models: "let's add SMS reminders for overdue invoices" (`frame-change`), "the late fee comes out wrong for refunded invoices, fix it" (`root-cause`), "review the refund branch before I merge it" (`inspect-change`), "the reviewer left six comments on my PR" (`vet-feedback`), "reorder the roadmap so sharing comes before search" (`plan-milestones`), "clean up the duplication in this diff" (`polish-diff`), "what's waiting on me this morning?" (`board`).

## 1.0.1 — pointer rename (2026-10-06)

`/study-change` was merged into `understand` along with four other learning
skills (see `understand/TESTS.md`). The suggested-skills line now names
`/understand <range>` for the author self-check. This changes no behavior of
this skill and no baseline was run for it.

## 1.0.2 — brief-team removed (2026-10-06)

The user dropped `brief-team` as no longer needed. The suggested-skills line no
longer names it. No behavior change to this skill; no baseline run.
