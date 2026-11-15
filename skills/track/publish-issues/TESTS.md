# TESTS.md — publish-issues

## 2026-11-15 — model-invocable (description routing)

`disable-model-invocation` removed on the owner's word (2026-11-15: agents start skills on their
own; approving, answering and merging stay with the operator). Its step 4 already has the operator approve the breakdown before anything is published. One row that called `triage` user-invoked was corrected.
The description became trigger + outcome with its neighbours named.

Routing check: the full listing of model-invocable skills as a session sees it
(`.skills/fixtures/routing/listing.py`), 32 first messages (`cluster-b-messages.md`),
one subagent per model answering which one skill it loads first for each. Messages are batched
in one context, one rep per model, lighter than `pressure-testing.md`'s fresh context per query.

| | before (flagged, 52 listed) | after (62 listed) — sonnet | after — haiku |
|---|---|---|---|
| should fire here (4, 24) | NONE on all (haiku) | `publish-issues` on all | `publish-issues` on all |
| the other messages | none routed here | none routed here | none routed here |

Should-fire messages: "break the approved billing spec into tickets we can hand out" · "turn everything we just discussed into issues on the tracker". Near misses that stayed with their owners on both models: "let's add SMS reminders for overdue invoices" (`frame-change`), "the late fee comes out wrong for refunded invoices, fix it" (`root-cause`), "review the refund branch before I merge it" (`inspect-change`), "the reviewer left six comments on my PR" (`vet-feedback`), "reorder the roadmap so sharing comes before search" (`plan-milestones`), "clean up the duplication in this diff" (`polish-diff`), "what's waiting on me this morning?" (`board`).

## 2026-11-01 — follow the repo's issue format (1.0.0 → 1.1.0)

Design: `docs/design/2026-11-01-issue-format.md`. Fixture: a generated repo with an in-repo tracker CLI
and the new `Issue format` seed. Prompt: two approved slices, the second blocked by the first. Scored
from the tracker's JSON.

**RED, 1.0.0** (sonnet 1 and haiku 1 with a blocking relation, haiku 1 without).
- Format: 3/3 followed the seed over the skill's own template and marker line, and each said so: "the
  repo's rule wins". The format itself did not fail, so nothing new was written for it. The
  duplicate templates and the marker line were deleted, since they contradict the seed.
- No blocking relation: 1/1 left the blocked slice with `enhancement` alone. "I used `needs-triage`
  nowhere so triage doesn't pick #2 up." That breaks the one-state rule.

**Form.** An observable rule: every slice takes the same state role, and the edge holds it back.

**GREEN, 1.1.0.**
- No blocking relation, sonnet 1 and haiku 1: 2/2 gave both slices `ready-for-agent` with a `Blocked by: #1` line.
- With a blocking relation, haiku 1: both slices `ready-for-agent`, the edge in the tracker's field, and the requester's plan left out.
- Not yet approved, haiku 1: stopped at the breakdown and created nothing.
